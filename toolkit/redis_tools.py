import uuid
import time


class DistributedLock(object):
    """
    Redis分布式锁
    """
    SCRIPT = "if redis.call('get', KEYS[1]) == ARGV[1] then " \
             "return redis.call('del', KEYS[1]) else return 0 end"

    def __init__(self, redis_conn, lock_key, expire, roll_interval=0.1):
        self.lock_key = lock_key
        self.redis_conn = redis_conn
        self.req_id = uuid.uuid4()
        self.expire = expire
        self.roll_interval = roll_interval

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unlock()

    async def __aenter__(self):
        return await self.alock()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aunlock()

    def _lock(self):
        return self.redis_conn.set(
            self.lock_key, self.req_id, ex=self.expire, nx=True)

    def lock(self):
        while not self._lock():
            time.sleep(self.roll_interval)

    def unlock(self):
        script = self.redis_conn.register_script(self.SCRIPT)
        return script(keys=[self.lock_key], args=[self.req_id])

    async def _alock(self):
        return await self.redis_conn.set(
            self.lock_key, self.req_id, ex=self.expire, nx=True)

    async def alock(self):
        while not await self._alock():
            time.sleep(self.roll_interval)

    async def aunlock(self):
        script = self.redis_conn.register_script(self.SCRIPT)
        return await script.execute(keys=[self.lock_key], args=[self.req_id])
