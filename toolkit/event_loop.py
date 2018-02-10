import os
import time
import errno
import heapq
import select
import functools
import itertools
import collections

from collections.abc import Coroutine, Iterable

from .tornado.waker import Waker
from .tornado.future import Future
from .tornado.timeout import Timeout
from .singleton import SingletonABCMeta
from .tornado.utils import errno_from_exception

_POLL_TIMEOUT = 3600


def coroutine(func):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__()
        self.gen = func(*args, **kwargs)

    def send(self, result):
        try:
            return self.gen.send(result)
        except (GeneratorExit, StopIteration) as e:
            self.set_result(e.args[0])
            raise

    def throw(self, typ, val=None, tb=None):
        return self.gen.throw(typ, val=None, tb=None)

    def __iter__(self):
        return self.gen

    def __await__(self):
        yield from self

    cls = type(func.__name__,
               (Future, Coroutine, Iterable),
               {"__init__": __init__,
                "send": send,
                "throw": throw,
                "__iter__": __iter__,
                "__await__": __await__})

    return cls
        

class EventLoop(object, metaclass=SingletonABCMeta):
    """
    借鉴Tornado IOLoop实现机制，实现了基于yield from的EventLoop
    """
    _EPOLLIN = 0x001
    _EPOLLPRI = 0x002
    _EPOLLOUT = 0x004
    _EPOLLERR = 0x008
    _EPOLLHUP = 0x010
    _EPOLLRDHUP = 0x2000
    _EPOLLONESHOT = (1 << 30)
    _EPOLLET = (1 << 31)

    NONE = 0
    READ = _EPOLLIN
    WRITE = _EPOLLOUT
    ERROR = _EPOLLERR | _EPOLLHUP

    def __init__(self):
        if hasattr(select, "epoll"):
            self._impl = select.epoll()
        elif hasattr(select, "kqueue"):
            from .tornado.kqueue import _KQueue
            self._impl = _KQueue()
        else:
            from .tornado.select import _Select
            self._impl = _Select()
        self._handlers = {}
        self._events = {}
        self._callbacks = collections.deque()
        self._timeouts = []
        self._cancellations = 0
        self.coroutines = dict()
        self._running = False
        self._stopped = False
        self._closing = False
        self._waker = Waker()
        self._timeout_counter = itertools.count()
        self.add_handler(self._waker.fileno(),
                         lambda fd, events: self._waker.consume(),
                         self.READ)

    def add_coroutines(self, coroutines):
        for coroutine in coroutines:
            self.coroutines[coroutine] = None
        self._waker.wake()

    def close(self, all_fds=False):
        self._closing = True
        self.remove_handler(self._waker.fileno())
        if all_fds:
            for fd, handler in list(self._handlers.values()):
                self.close_fd(fd)
        self._waker.close()
        self._impl.close()
        self._callbacks = None
        self._timeouts = None

    def close_fd(self, fd):
        try:
            try:
                fd.close()
            except AttributeError:
                os.close(fd)
        except OSError:
            pass

    def split_fd(self, fd):
        try:
            return fd.fileno(), fd
        except AttributeError:
            return fd, fd

    def add_handler(self, fd, handler, events):
        fd, obj = self.split_fd(fd)
        self._handlers[fd] = (obj, handler)
        self._impl.register(fd, events | self.ERROR)

    def update_handler(self, fd, events):
        fd, obj = self.split_fd(fd)
        self._impl.modify(fd, events | self.ERROR)

    def remove_handler(self, fd):
        fd, obj = self.split_fd(fd)
        self._handlers.pop(fd, None)
        self._events.pop(fd, None)
        try:
            self._impl.unregister(fd)
        except Exception:
            print("Error deleting fd from EventLoop")

    def process_coroutine(self, coroutine, yielded):
        while True:
            try:
                # 如果当前yield值为Future对象，则判断Future是否完成，进而调用send方法发结果，否则中断本协程的进行。
                # 如果当前yield值不是Future对象, 直接send当前值。
                # 如果期间发生协程运行完毕，则删除该协程。
                if isinstance(yielded, Future):
                    if yielded.done():
                        yielded = self.coroutines[coroutine] = \
                            coroutine.send(yielded.result())
                    else:
                        break
                else:
                    yielded = self.coroutines[coroutine] = coroutine.send(yielded)
            except (GeneratorExit, StopIteration):
                del self.coroutines[coroutine]
                break

    def start(self):
        if self._running:
            raise RuntimeError("EventLoop is already running")
        if self._stopped:
            self._stopped = False
            return
        self._running = True

        try:
            while True:

                if not self._running:
                    break

                due_timeouts = []
                if self._timeouts:
                    now = time.time()
                    while self._timeouts:
                        if self._timeouts[0].callback is None:
                            heapq.heappop(self._timeouts)
                            self._cancellations -= 1
                        elif self._timeouts[0].deadline <= now:
                            due_timeouts.append(heapq.heappop(self._timeouts))
                        else:
                            break
                    if (self._cancellations > 512 and
                                self._cancellations > (len(self._timeouts) >> 1)):
                        self._cancellations = 0
                        self._timeouts = [x for x in self._timeouts
                                          if x.callback is not None]
                        heapq.heapify(self._timeouts)

                for timeout in due_timeouts:
                    if timeout.callback is not None:
                        timeout.callback()

                for coroutine in self.coroutines.copy().keys():
                    self.process_coroutine(coroutine, self.coroutines[coroutine])

                if self.need_stop and not self.coroutines:
                    self.stop()

                if self._timeouts:
                    poll_timeout = self._timeouts[0].deadline - time.time()
                    poll_timeout = max(0, min(poll_timeout, _POLL_TIMEOUT))
                else:
                    poll_timeout = _POLL_TIMEOUT

                try:
                    event_pairs = self._impl.poll(poll_timeout)
                except Exception as e:
                    if errno_from_exception(e) == errno.EINTR:
                        continue
                    else:
                        raise

                self._events.update(event_pairs)
                while self._events:
                    fd, events = self._events.popitem()
                    try:
                        fd_obj, handler_func = self._handlers[fd]
                        handler_func(fd_obj, events)
                    except (OSError, IOError) as e:
                        if errno_from_exception(e) == errno.EPIPE:
                            # Happens when the client closes the connection
                            pass

                fd_obj = handler_func = None
        finally:
            self._stopped = False

    def call_at(self, deadline, callback, *args, **kwargs):
        timeout = Timeout(
            deadline,
            functools.partial(callback, *args, **kwargs),
            self)
        heapq.heappush(self._timeouts, timeout)
        self._waker.wake()
        return timeout

    def stop(self):
        self._running = False
        self._stopped = True
        self._waker.wake()

    def stop_when_finish(self):
        self.need_stop = True

    def run_until_complete(self, *coroutines):
        self.stop_when_finish()
        self.add_coroutines(coroutines)
        self.start()


def sleep(seconds):
    future = Future()

    def callback():
        future.set_result(None)

    EventLoop().call_at(time.time() + seconds, callback)
    yield future


def get_buffer(socket):
    future = Future()

    def callback(fd_obj, events):
        future.set_result(fd_obj.recv(1024))

    EventLoop().add_handler(socket, callback, EventLoop.READ)
    buffer = yield future
    return buffer

