import pytest

from toolkit.async_context import contextmanager


@contextmanager
def sync_method():
    yield 1


@contextmanager
def sync_method_error_before():
    raise RuntimeError()
    yield 1


@contextmanager
def sync_method_error_after():
    yield 1
    raise RuntimeError()


@contextmanager
async def async_method():
    yield 2


@contextmanager
async def async_method_error_before():
    raise RuntimeError()
    yield 2


@contextmanager
async def async_method_error_after():
    yield 2
    raise RuntimeError()


class TestContextManager(object):

    def test_sync_method_with_sync(self):
        with sync_method() as rs:
            assert rs == 1

    def test_sync_method_with_sync_with_error(self):
        with pytest.raises(RuntimeError):
            with sync_method() as rs:
                assert rs == 1
                raise RuntimeError()

    def test_sync_method_with_sync_with_inner_error_before(self):
        with pytest.raises(RuntimeError):
            with sync_method_error_before() as rs:
                pass

    def test_sync_method_with_sync_with_inner_error_after(self):
        with pytest.raises(RuntimeError):
            with sync_method_error_after() as rs:
                assert rs == 1

    @pytest.mark.asyncio
    async def test_sync_method_with_async(self):
        async with sync_method() as rs:
            assert rs == 1

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_error(self):
        with pytest.raises(RuntimeError):
            async with sync_method() as rs:
                assert rs == 1
                raise RuntimeError()

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_inner_error_before(self):
        with pytest.raises(RuntimeError):
            async with sync_method_error_before() as rs:
                pass

    @pytest.mark.asyncio
    async def test_sync_method_with_async_with_inner_error_after(self):
        with pytest.raises(RuntimeError):
            async with sync_method_error_after() as rs:
                assert rs == 1

    @pytest.mark.asyncio
    async def test_async_method_with_async(self):
        async with async_method() as rs:
            assert rs == 2

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_error(self):
        with pytest.raises(RuntimeError):
            async with async_method() as rs:
                assert rs == 2
                raise RuntimeError("111")

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_inner_error_before(self):
        with pytest.raises(RuntimeError):
            async with async_method_error_before() as rs:
                pass

    @pytest.mark.asyncio
    async def test_async_method_with_async_with_inner_error_after(self):
        with pytest.raises(RuntimeError):
            async with async_method_error_after() as rs:
                assert rs == 2

    def test_async_method_with_sync(self):
        with async_method() as rs:
            assert rs == 2

    def test_async_method_with_sync_with_error(self):
        with pytest.raises(RuntimeError):
            with async_method() as rs:
                assert rs == 2
                raise RuntimeError("111")

    def test_async_method_with_sync_with_inner_error_before(self):
        with pytest.raises(RuntimeError):
            with async_method_error_before() as rs:
                pass

    def test_async_method_with_sync_with_inner_error_after(self):
        with pytest.raises(RuntimeError):
            with async_method_error_after() as rs:
                assert rs == 2