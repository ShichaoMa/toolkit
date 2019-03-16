import sys
import asyncio
import inspect

from functools import wraps
from threading import Thread
from contextlib import _GeneratorContextManager


def contextmanager(func):
    @wraps(func)
    def helper(*args, **kwds):
        return _AsyncGeneratorContextManager(func, args, kwds)

    return helper


def await_async_gen(gen_method, gen_args=(None, )):
    """
    如果event_loop已经开始，那么在异步方法中执行同步方法时又遇到了异步方法，
    使用run_until_complete会报错: `This event loop is already running`
    所以启用一个子线程来完成这件事。
    :param gen_method:
    :param gen_args:
    :return:
    """
    container = dict()
    th = Thread(target=_child_thread, args=(container, gen_method, gen_args))
    th.start()
    th.join()
    if "rs" in container:
        return container["rs"]
    raise container["err"]


def _child_thread(container, gen_method, gen_args):
    loop = asyncio.new_event_loop()
    try:
        container["rs"] = loop.run_until_complete(gen_method(*gen_args))
    except Exception as e:
        container["err"] = e


class _AsyncGeneratorContextManager(_GeneratorContextManager):
    def __enter__(self):
        try:
            if inspect.isasyncgen(self.gen):
               return await_async_gen(self.gen.asend)
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
                    await_async_gen(self.gen.asend)
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
                    await_async_gen(self.gen.athrow, (type, value, traceback))

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
