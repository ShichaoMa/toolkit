import time
import traceback

from . import _find_caller_name


class SleepManager(object):
    """
    有的时候我们需要将线程停止一段时间，通常我们选择调用time.sleep(..)，当我们需要sleep很长一段时间，
    比如一分钟以上时，如果这时我们选择关闭程序，由于time.sleep阻塞导致我们的程序难以被关闭，通过使用
    SleepManager可以解决这个问题
    eg
    def myfunc(self):
        with SleepManager(sleep_time, self, interval=1, notify=lambda x: x.alive) as sm:
            if sm.is_notified:
                `我们知道是被唤醒了，而不是时间到了`
            ....
    """
    def __init__(self, sleep_time, instance, interval=1, notify=lambda x: x.alive):
        """
        :param sleep_time: 需要阻塞的时长
        :param instance: 使用这个对象来动态告知manager什么时候要中断程序了，这个对象会被传递给notify回调函数
        :param interval: 如果这要中断程序，那么最长需要等待的时间间隔
        :param notify: 回调函数，接收instance，来决定是否唤醒阻塞。
        """
        self.sleep_time = sleep_time
        self.instance = instance
        self.interval = interval
        self.notify = notify
        self.enter_time = time.time()
        self.is_notified = True

    def __enter__(self):
        while time.time() - self.enter_time < self.sleep_time and self.notify(self.instance):
            time.sleep(self.interval)
        self.is_notified = self.notify(self.instance)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is None


class ExceptContext(object):
    """
    异常捕捉上下文
    eg:
    def test():
        with ExceptContext(Exception, errback=lambda name, *args:print(name)):
            raise Exception("test. ..")
    """
    def __init__(self, exception, func_name=None, errback=lambda func_name, *args: traceback.print_exception(*args)):
        """
        :param exception: 指定要监控的异常
        :param func_name: 可以选择提供当前所在函数的名称，回调函数会提交到函数，用于跟踪
        :param errback: 提供一个回调函数，如果发生了指定异常，就调用该函数
        """
        self.errback = errback
        self.exception = exception
        self.func_name = func_name or _find_caller_name(is_func=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, self.exception):
            self.errback(self.func_name, exc_type, exc_val, exc_tb)
            return True
        else:
            return False


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
        self.start = start or time.time()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop = time.time()
        self.cost = self.stop - self.start
        return exc_type is None