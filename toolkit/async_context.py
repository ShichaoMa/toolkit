import sys
import asyncio
import inspect

from functools import wraps
from threading import Thread
from contextlib import _GeneratorContextManager

from . import _property_cache, global_cache_classproperty,\
    cache_classproperty, classproperty


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


def await_async_method(coroutine, *args, **kwargs):
    """
    如果event_loop已经开始，那么在异步方法中执行同步方法时又遇到了异步方法，
    使用run_until_complete会报错: `This event loop is already running`
    所以启用一个子线程来完成这件事。
    :param coroutine :可以直接传入一个coroutine对象，也可以传入一个异步方法，
                      如果传入的是异步方法，那么其调用所需参数也需要一并传入，
                      对于通过返回feature来将同步方法伪装成异步方法的情况，
                      只能使用第二种调用方式。
    :return:
    """
    container = dict()
    th = Thread(target=_coroutine_run_in_child_thread_loop,
                args=(container, coroutine, *args), kwargs=kwargs)
    th.start()
    th.join()
    if "rs" in container:
        return container["rs"]
    raise container["err"]


awt = await_async_method


def sync_run_async(func):
    """
    将异步方法通过该装饰器装饰后可以被同步方法同步调用，这个方法只是做用于容错，
    一般不要使用，同步方法会让该异步方法失去异步执行的能力，应该从设计上避免使用这个方法。
    :param func:
    :return: func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return await_async_method(func, *args, **kwargs)

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


def async_classproperty(func):
    """
    异步类属性
    :param func:
    :return:
    """
    return classproperty(sync_run_async(func))


def async_global_cache_classproperty(func):
    """
    异步全局类缓存属性
    :param func:
    :return:
    """
    return global_cache_classproperty(sync_run_async(func))


def async_cache_classproperty(func):
    """
    异步类缓存属性
    :param func:
    :return:
    """
    return cache_classproperty(sync_run_async(func))


def _coroutine_run_in_child_thread_loop(container, coroutine, *args, **kwargs):
    """
    使用一子线程事件循环来执行异步方法。
    :param container:
    :param coroutine:
    :return:
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        if not inspect.isawaitable(coroutine):
            coroutine = coroutine(*args, **kwargs)
        container["rs"] = loop.run_until_complete(coroutine)
    except Exception as e:
        container["err"] = e


class _AsyncGeneratorContextManager(_GeneratorContextManager):
    """
    异步上下文管理器
    """
    def __enter__(self):
        try:
            if inspect.isasyncgen(self.gen):
               return await_async_method(self.gen.asend, None)
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
                    await_async_method(self.gen.asend, None)
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
                    await_async_method(self.gen.athrow, type, value, traceback)

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
