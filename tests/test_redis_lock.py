import sys
import time
from toolkit.redis_tools import DistributedLock


def test_lock_sync():
    from redis import Redis
    redis_conn = Redis(host="127.0.0.1", port=7777)
    lock = DistributedLock(redis_conn, "test_key", 10)
    #import ipdb;ipdb.set_trace()
    with lock:
        time.sleep(int(sys.argv[1]))
        print(11111111111, sys.argv[1])


def test_lock_async():
    async def lock():
        from aredis import StrictRedis
        redis_conn = StrictRedis(host="127.0.0.1", port=7777)
        lock = DistributedLock(redis_conn, "test_key", 10)
        #import ipdb;ipdb.set_trace()
        async with lock:
            time.sleep(int(sys.argv[1]))
            print(11111111111, sys.argv[1])
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(lock())

test_lock_async()