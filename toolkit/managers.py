import time
import traceback

from . import _find_caller_name

__all__ = ["Blocker", "ExceptContext", "Timer"]


class Blocker(object):
    """
    有的时候我们需要将线程停止一段时间，通常我们选择调用time.sleep(..)，
    当我们需要sleep很长一段时间，比如一分钟以上时，如果这时我们选择关闭程序，
    而我们通过singal注册了关闭信号的监听器，用来改变当时程序的状态，
    如果置self.alive = False,由于time.sleep阻塞导致我们的程序当前线程无法获知alive状态，
    难以被关闭，通过使用Blocker，我们可以避免上述情况发生。
    eg:
    def myfunc(self):
        with Blocker(
        sleep_time, self, interval=1, notify=lambda x: not x.alive) as sm:
            if sm.is_notified:
                `我们知道是被唤醒了，而不是时间到了`
            ....
    """
    def __init__(self, block_time, instance, interval=1,
                 notify=lambda instance: False, immediately=False):
        """
        :param block_time: 需要阻塞的时长
        :param instance: 使用这个对象来动态告知manager什么时候要中断程序了，
        这个对象会被传递给notify回调函数
        :param interval: 如果这要中断程序，那么最长需要等待的时间间隔
        :param notify: 回调函数，接收instance，来决定是否唤醒阻塞。
        :param immediately: 是否不阻塞立即执行。
        """
        self.block_time = block_time
        self.instance = instance
        self.interval = interval
        self.notify = notify
        self.enter_time = time.time()
        self.immediately = immediately
        self.is_notified = True

    def __enter__(self):
        while not self.immediately and time.time() - \
                self.enter_time < self.block_time \
                and not self.notify(self.instance):
            time.sleep(self.interval)
        self.is_notified = self.notify(self.instance)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is None


class ExceptContext(object):
    """
    异常捕获上下文
    eg:
    def test():
        with ExceptContext(Exception, errback=lambda name, *args:print(name)):
            raise Exception("test. ..")
    """
    def __init__(self, exception=Exception, func_name=None,
                 errback=lambda func_name, *args:
                 traceback.print_exception(*args) is None,
                 finalback=lambda got_err: got_err):
        """
        :param exception: 指定要监控的异常
        :param func_name: 可以选择提供当前所在函数的名称，回调函数会提交到函数，用于跟踪
        :param errback: 提供一个回调函数，如果发生了指定异常，
        就调用该函数，该函数的返回值为True时不会继续抛出异常
        :param finalback: finally要做的操作
        """
        self.errback = errback
        self.finalback = finalback
        self.exception = exception
        self.got_err = False
        self.err_info = None
        self.func_name = func_name or _find_caller_name(is_func=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return_code = False
        if isinstance(exc_val, self.exception):
            self.got_err = True
            self.err_info = (exc_type, exc_val, exc_tb)
            return_code = self.errback(self.func_name, exc_type, exc_val, exc_tb)
        self.finalback(self.got_err)
        return return_code


class Timer(object):
    """
    计时器，对于需要计时的代码进行with操作：
    with Timer() as timer:
        ...
        ...
    print(timer.cost)
    ...
    """
    def __init__(self, start=None):
        self.start = start if start is not None else time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time.time()
        self.cost = self.stop - self.start
        return exc_type is None