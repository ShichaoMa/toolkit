import sys
import asyncio
import inspect

from functools import wraps
from threading import Thread
from contextlib import _GeneratorContextManager

from . import _property_cache


def contextmanager(func):
    """
    异步下上文管理器，其支持装饰同步生成器或异步生成器，并支持使用async with 或with。
    :param func:
    :return:
    """
    @wraps(func)
    def helper(*args, **kwds):
        return _AsyncGeneratorContextManager(func, args, kwds)

    return helper


def await_async_method(method, args: tuple=None, kwargs: dict=None):
    """
    如果event_loop已经开始，那么在异步方法中执行同步方法时又遇到了异步方法，
    使用run_until_complete会报错: `This event loop is already running`
    所以启用一个子线程来完成这件事。
    :param method:
    :param args:
    :param kwargs:
    :return:
    """
    container = dict()
    th = Thread(target=_async_run_in_child_thread_loop,
                args=(container, method, args, kwargs))
    th.start()
    th.join()
    if "rs" in container:
        return container["rs"]
    raise container["err"]


def sync_run_async(func):
    """
    同步执行异步
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return await_async_method(func, args=args, kwargs=kwargs)

    return wrapper


def async_property(func):
    """
    异步property，支持将异步方法转换成同步属性，但不支持后续的property.setter等方法。
    :return:
    """
    return property(sync_run_async(func))


def async_cached_property(func):
    """
    有缓存效果异步属性
    :param func:
    :return:
    """
    return property(_property_cache(sync_run_async(func)))


def _async_run_in_child_thread_loop(container, method, args, kwargs):
    """
    使用一子线程事件循环还执行异步方法。
    :param container:
    :param method:
    :param args:
    :param kwargs:
    :return:
    """
    loop = asyncio.new_event_loop()
    try:
        args = args or tuple()
        kwargs = kwargs or dict()
        container["rs"] = loop.run_until_complete(method(*args, **kwargs))
    except Exception as e:
        container["err"] = e


class _AsyncGeneratorContextManager(_GeneratorContextManager):
    """
    异步上下文管理器
    """
    def __enter__(self):
        try:
            if inspect.isasyncgen(self.gen):
               return await_async_method(self.gen.asend, args=(None, ))
            else:
                return self.gen.send(None)
        except StopIteration:
            raise RuntimeError("generator didn't yield") from None

    def __exit__(self, type, value, traceback):
        if type is None:
            try:
                if inspect.isgenerator(self.gen):
                    self.gen.send(None)
                elif inspect.isasyncgen(self.gen):
                    await_async_method(self.gen.asend, args=(None, ))
                else:
                    return False
            except (StopIteration, StopAsyncIteration):
                return False
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                # Need to force instantiation so we can reliably
                # tell if we get the same exception back
                value = type()
            try:
                if inspect.isgenerator(self.gen):
                    self.gen.throw(type, value, traceback)
                elif inspect.isasyncgen(self.gen):
                    await_async_method(
                        self.gen.athrow, args=(type, value, traceback))

                else:
                    raise value
            except (StopIteration, StopAsyncIteration) as exc:
                # Suppress StopIteration *unless* it's the same exception that
                # was passed to throw().  This prevents a StopIteration
                # raised inside the "with" statement from being suppressed.
                return exc is not value
            except RuntimeError as exc:
                # Don't re-raise the passed in exception. (issue27122)
                if exc is value:
                    return False
                # Likewise, avoid suppressing if a StopIteration exception
                # was passed to throw() and later wrapped into a RuntimeError
                # (see PEP 479).
                if type is StopIteration and exc.__cause__ is value:
                    return False
                raise
            except:
                # only re-raise if it's *not* the exception that was
                # passed to throw(), because __exit__() must not raise
                # an exception unless __exit__() itself failed.  But throw()
                # has to raise the exception to signal propagation, so this
                # fixes the impedance mismatch between the throw() protocol
                # and the __exit__() protocol.
                #
                if sys.exc_info()[1] is value:
                    return False
                raise
            raise RuntimeError("generator didn't stop after throw()")

    async def __aenter__(self):
        try:
            if inspect.isgenerator(self.gen):
                return self.gen.send(None)
            else:
                return await self.gen.asend(None)
        except (StopAsyncIteration, StopIteration):
            raise RuntimeError("generator didn't yield") from None

    async def __aexit__(self, type, value, traceback):
        if type is None:
            try:
                if inspect.isgenerator(self.gen):
                    self.gen.send(None)
                else:
                    await self.gen.asend(None)
            except (StopAsyncIteration, StopIteration):
                return False
            else:
                raise RuntimeError("generator didn't stop")
        else:
            if value is None:
                value = type()
            try:
                if inspect.isgenerator(self.gen):
                    await self.gen.throw(type, value, traceback)
                else:
                    await self.gen.athrow(type, value, traceback)
            except (StopAsyncIteration, StopIteration) as exc:
                return exc is not value
            except RuntimeError as exc:
                if exc is value:
                    return False
                if issubclass(type, (StopAsyncIteration, StopIteration))\
                        and exc.__cause__ is value:
                    return False
                raise
            except:
                if sys.exc_info()[1] is value:
                    return False
                raise
            raise RuntimeError("generator didn't stop after throw()")
