import sys
import time
import pytest

from toolkit.tools.redis_tools import DistributedLock


@pytest.mark.skip(reason="May not have redis server. ")
class TestRedisLock(object):

    def test_lock_sync(self):
        from redis import Redis
        redis_conn = Redis(host="127.0.0.1", port=7777)
        lock = DistributedLock(redis_conn, "test_key", 10)
        with lock:
            time.sleep(int(sys.argv[1]))
            print(11111111111, sys.argv[1])

    @pytest.mark.asyncio
    def test_lock_async(self):
        async def lock():
            from aredis import StrictRedis
            redis_conn = StrictRedis(host="127.0.0.1", port=7777)
            lock = DistributedLock(redis_conn, "test_key", 10)
            async with lock:
                time.sleep(int(sys.argv[1]))
                print(11111111111, sys.argv[1])
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(lock())

