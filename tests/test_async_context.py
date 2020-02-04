import pytest
import asyncio

from toolkit.async_context import contextmanager, \
    async_cached_property, async_property, awt, Context, CURRENCY_TYPE_COROUTINE, create_task


class TestError(RuntimeError):
    pass


@contextmanager
def sync_method():
    yield 1


@contextmanager
def sync_method_error_before():
    raise TestError()
    yield 1


@contextmanager
def sync_method_error_after():
    yield 1
    raise TestError()


@contextmanager
async def async_method():
    yield 2


@contextmanager
async def async_method_error_before():
    raise TestError()
    yield 2


@contextmanager
async def async_method_error_after():
    yield 2
    raise TestError()


class TestContextManager(object):

    def test_sync_method_with_sync(self):
        with sync_method() as rs:
            assert rs == 1

    def test_sync_method_with_sync_with_error(self):
        with pytest.raises(TestError):
            with sync_method() as rs:
                assert rs == 1
                raise TestError()

    def test_sync_method_with_sync_with_inner_error_before(self):
        with pytest.raises(TestError):
            with sync_method_error_before() as rs:
                pass

    def test_sync_method_with_sync_with_inner_error_after(self):
        with pytest.raises(TestError):
            with sync_method_error_after() as rs:
                assert rs == 1

    @pytest.mark.asyncio
    async def test_sync_method_with_async(self):
        async with sync_method() as rs:
            assert rs == 1

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_error(self):
        with pytest.raises(TestError):
            async with sync_method() as rs:
                assert rs == 1
                raise TestError()

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_inner_error_before(self):
        with pytest.raises(TestError):
            async with sync_method_error_before() as rs:
                pass

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_inner_error_after(self):
        with pytest.raises(TestError):
            async with sync_method_error_after() as rs:
                assert rs == 1

    @pytest.mark.asyncio
    async def test_async_method_with_async(self):
        async with async_method() as rs:
            assert rs == 2

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_error(self):
        with pytest.raises(TestError):
            async with async_method() as rs:
                assert rs == 2
                raise TestError("111")

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_inner_error_before(self):
        with pytest.raises(TestError):
            async with async_method_error_before() as rs:
                pass

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_inner_error_after(self):
        with pytest.raises(TestError):
            async with async_method_error_after() as rs:
                assert rs == 2

    @pytest.mark.asyncio
    async def test_async_method_with_sync(self):
        with async_method() as rs:
            assert rs == 2

    @pytest.mark.asyncio
    async def test_async_method_with_sync_with_error(self):
        with pytest.raises(TestError):
            with async_method() as rs:
                assert rs == 2
                raise TestError("111")

    @pytest.mark.asyncio
    async def test_async_method_with_sync_with_inner_error_before(self):
        with pytest.raises(TestError):
            with async_method_error_before() as rs:
                pass

    @pytest.mark.asyncio
    async def test_async_method_with_sync_with_inner_error_after(self):
        with pytest.raises(TestError):
            with async_method_error_after() as rs:
                assert rs == 2


class AsyncPropertyClass(object):

    @async_property
    async def name(self):
        print("name")
        return "tom"

    @async_cached_property
    async def age(self):
        print("age")
        return 18


class TestAsyncProperty(object):
    def test_async_property(self, capsys):
        obj = AsyncPropertyClass()
        assert obj.name == "tom"
        obj.name
        captured = capsys.readouterr()
        assert captured.out.count("name") == 2

    @pytest.mark.asyncio
    async def test_async_property_in_async(self, capsys):
        obj = AsyncPropertyClass()
        assert obj.name == "tom"
        obj.name
        captured = capsys.readouterr()
        assert captured.out.count("name") == 2

    def test_async_cached_property(self, capsys):
        obj = AsyncPropertyClass()
        assert obj.age == 18
        obj.age
        captured = capsys.readouterr()
        assert captured.out.count("age") == 1

    @pytest.mark.asyncio
    async def test_async_cached_property_in_async(self, capsys):
        obj = AsyncPropertyClass()
        assert obj.age == 18
        obj.age
        captured = capsys.readouterr()
        assert captured.out.count("age") == 1


class TestAsyncRun(object):

    def test_run_async(self):
        async def fun(a):
            return a
        assert awt(fun(1)) == 1

    def test_run_future(self):
        import asyncio

        def fun(a):
            loop = asyncio.get_event_loop()
            future = loop.create_future()
            def bar():
                future.set_result(a*2)
            loop.run_in_executor(None, bar)
            return future

        assert awt(fun, 3) == 6


@pytest.mark.asyncio
class TestContext(object):

    async def test_context(self):
        coroutinelocal = Context(currency_type=CURRENCY_TYPE_COROUTINE)
        coroutinelocal["a"] = 11

        async def fun():
            return coroutinelocal["a"]

        async def bar():
            coroutinelocal["a"] = 33
            return coroutinelocal["a"]

        task2 = create_task(bar())
        await asyncio.gather(task2)
        task1 = create_task(fun())

        await asyncio.gather(task1)
        assert task1.result() == 11
        assert task2.result() == 33

    async def test_context_inherit(self):
        coroutinelocal = Context(currency_type=CURRENCY_TYPE_COROUTINE)
        coroutinelocal["a"] = 11

        async def bar():
            task = create_task(fun())
            await asyncio.sleep(1)
            coroutinelocal["a"] = 33
            return task

        async def fun():
            assert coroutinelocal["a"] == 11
            await asyncio.sleep(2)
            assert coroutinelocal["a"] == 33

        task2 = create_task(bar())
        await asyncio.gather(task2)
        task1 = task2.result()
        await asyncio.gather(task1)

    async def test_context_clear_coroutine(self):
        coroutinelocal = Context(currency_type=CURRENCY_TYPE_COROUTINE)
        coroutinelocal["a"] = 11
        coroutinelocal.clear()
        assert coroutinelocal["a"] is None

    async def test_context_clear_thread(self):
        coroutinelocal = Context()
        coroutinelocal["a"] = 11
        coroutinelocal.clear()
        assert coroutinelocal["a"] is None