import tornado
from collections import deque
from select import epoll
from tornado.platform.auto import Waker

from toolkit.singleton import Singleton


class EPollIOLoop(metaclass=Singleton):
    _EPOLLIN = 0x001
    _EPOLLPRI = 0x002
    _EPOLLOUT = 0x004
    _EPOLLERR = 0x008
    _EPOLLHUP = 0x010
    _EPOLLRDHUP = 0x2000
    _EPOLLONESHOT = (1 << 30)
    _EPOLLET = (1 << 31)

    # Our events map exactly to the epoll events
    NONE = 0
    READ = _EPOLLIN
    WRITE = _EPOLLOUT
    ERROR = _EPOLLERR | _EPOLLHUP

    def __init__(self):
        self._impl = epoll()
        self._waker = Waker()
        self.add_handler(self._waker.fileno(),
                         lambda fd, events: self._waker.consume(),
                         self.READ)
        self._handlers = {}
        self._events = {}
        self.coroutine_futures = dict()
        self.waits = deque()
        self.callbacks = deque()

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
            print("Error deleting fd from IOLoop")

    def split_fd(self, fd):
        try:
            return fd.fileno(), fd
        except AttributeError:
            return fd, fd

    def start(self):
        while True:
            for i in range(len(self.waits)):
                coroutine = self.waits.popleft()
                if self.coroutine_futures[coroutine].is_ok():
                    self.callbacks.append(coroutine)
                else:
                    self.waits.append(coroutine)

            for i in range(len(self.callbacks)):
                coroutine = self.callbacks.popleft()
                future = self.coroutine_futures[coroutine]
                coroutine.send(future)
                if future.is_ok():
                    self.callbacks.append(future)
                else:
                    self.waits.append(future)
            event_pairs = self._impl.poll(10)

            self._events.update(event_pairs)
            while self._events:
                fd, events = self._events.popitem()
                fd_obj, handler_func = self._handlers[fd]
                handler_func(fd_obj, events)


class Future(object):
    def __init__(self, ok_callback=lambda: True):
        self._done = False
        self._result = None
        self._callbacks = []
        self.ok_callback = ok_callback

    def is_ok(self):
        return self.ok_callback()

    def set_ok_callback(self, ok_callback):
        self.ok_callback = ok_callback

    def cancel(self):
        return False

    def cancelled(self):
        return False

    def running(self):
        return not self._done

    def done(self):
        return self._done

    def result(self, timeout=None):
        if self._result is not None:
            return self._result
        return self._result

    def add_done_callback(self, fn):

        if self._done:
            fn(self)
        else:
            self._callbacks.append(fn)

    def set_result(self, result):
        self._result = result
        self._set_done()

    def _set_done(self):
        self._done = True
        for cb in self._callbacks:
            cb(self)
        self._callbacks = None

import time

def sleep(seconds):
    f = Future()
    f.set_ok_callback(lambda start_time=time.time(): time.time() >= start_time + seconds)
    yield f

def main():
    future = Future()
    def sum(a, b):
        yield future
        yield from sleep(2)
        return a + b
    result = yield from sum(1, 2)
    print(result)

if __name__ == "__main__":
    main()