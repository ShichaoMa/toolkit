import sys
import asyncio
import inspect
import contextvars

from threading import RLock
from functools import wraps
from threading import Thread
from contextlib import _GeneratorContextManager

from . import _property_cache, global_cache_classproperty,\
    cache_classproperty, classproperty


CURRENCY_TYPE_THREAD = 1
CURRENCY_TYPE_COROUTINE = 2


from weakref import WeakKeyDictionary, finalize, WeakSet, ref


NOT_FOUND = object()


class Compact36ContextVar(object):

    def __init__(self, key):
        self.task_val_mapping = WeakKeyDictionary()

    def set(self, val):
        self.task_val_mapping[asyncio.Task.current_task()] = val

    def get(self):
        task = asyncio.Task.current_task()
        while True:
            val = self.task_val_mapping.get(task, NOT_FOUND)
            if val == NOT_FOUND and hasattr(task, "parent_task"):
                task = task.parent_task()
            else:
                break

        if val != NOT_FOUND:
            return val


def coro_finalize(task):
    """
    回收task时，将该task的child和其parent双向绑定到一起
    :param task:
    :return:
    """
    children = getattr(task, "children", WeakSet())
    if hasattr(task, "parent_task") and task.parent_task() is not None:
        parent_task = task.parent_task()
        parent_task.children.update(children)
        for child in children:
            child.parent_task = ref(parent_task)


def create_task(coro):
    task = asyncio.get_event_loop().create_task(coro)
    current_task = asyncio.Task.current_task()
    if current_task is not None:
        task.parent_task = ref(current_task)
        if not hasattr(current_task, "children"):
            current_task.children = WeakSet()
        current_task.children.add(task)
        finalize(task, coro_finalize, task)
    return task


class Context(object):
    contextvar_mappings = dict()
    lock = RLock()

    def __init__(self, currency_type=None):
        """
        并发环境下的上下文变量，兼容python3.7, 3.6，threading 和coroutine
        对于coroutine，在3.6环境下，需要传入currency_type = CURRENCY_TYPE_COROUTINE,
        同时创建子协程需要使用当前包下的create_task才会有继承效果
        :param currency_type: CURRENCY_TYPE_COROUTINE/CURRENCY_TYPE_THREAD/None
        """
        if currency_type == CURRENCY_TYPE_COROUTINE:
            object.__setattr__(self, "contextvar", Compact36ContextVar)
        else:
            object.__setattr__(self, "contextvar", contextvars.ContextVar)

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as e:
            raise AttributeError(e)

    def __getitem__(self, item):
        key = self.contextvar_mappings.get(item)
        if key is None:
            raise KeyError(f"{item} not found!")
        return key.get()

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        with self.lock:
            if key not in self.contextvar_mappings:
                self.contextvar_mappings[key] = self.contextvar(key)
        self.contextvar_mappings[key].set(value)

    def __setattr__(self, key, value):
        self[key] = value

    def set(self, key, value):
        self[key] = value

    def clear(self):
        ctx = contextvars.copy_context()
        for var in ctx.keys():
            var.set(None)


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
