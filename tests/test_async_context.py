import pytest

from toolkit.async_context import contextmanager


@contextmanager
def sync_method():
    yield 1


@contextmanager
async def async_method():
    yield 2


class TestContextManager(object):

    def test_sync_method_with_sync(self):
        with sync_method() as rs:
            assert rs == 1

    @pytest.mark.asyncio
    async def test_sync_method_with_async(self):
        async with sync_method() as rs:
            assert rs == 1

    @pytest.mark.asyncio
    async def test_async_method_with_async(self):
        async with async_method() as rs:
            assert rs == 2

    def test_async_method_with_sync(self):
        with async_method() as rs:
            assert rs == 2
