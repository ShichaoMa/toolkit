# -*- coding:utf-8 -*-
import os
import time
import glob
import json
import struct

from threading import RLock

from . import thread_safe_for_method_in_class, call_later


class RedisQueue(object):
    """
    redis队列
    """
    def __init__(self, redis_conn, key):
        self.redis_conn = redis_conn
        self.lock = RLock()
        self.key = key

    @thread_safe_for_method_in_class
    def push(self, *strings):
        self.redis_conn.lpush(self.key, *strings)

    @thread_safe_for_method_in_class
    def pop(self):
        return self.redis_conn.rpop(self.key)

    def __len__(self):
        return self.redis_conn.llen(self.key)

    @thread_safe_for_method_in_class
    def rid_all(self):
        pipe = self.redis_conn.pipeline()
        pipe.watch(self.key)
        pipe.multi()
        pipe.lrange(self.key, 0, -1).ltrim(self.key, 1, 0)
        results, count = pipe.execute()
        return results


class RedisHashSet(object):
    """
    使用hash和zset管理数据
    """
    def __init__(self, redis_conn, key):
        self.redis_conn = redis_conn
        self.hash_key = "%s_hash"%key
        self.set_key = "%s_set"%key
        self.lock = RLock()

    @thread_safe_for_method_in_class
    def push(self, message, id, delay):
        self.redis_conn.zadd(self.set_key, id, delay)
        self.redis_conn.hset(self.hash_key, id, message)

    @thread_safe_for_method_in_class
    def rid_all(self):
        pipe = self.redis_conn.pipeline()
        pipe.watch(self.set_key)
        pipe.multi()
        pipe.zrangebyscore(self.set_key, 0, time.time() * 1000).zremrangebyscore(
            self.set_key, 0, time.time() * 1000)
        result, count = pipe.execute()
        return result and [message for message in self.redis_conn.hmget(self.hash_key, result) if message]

    def hash_len(self):
        return self.redis_conn.hlen(self.hash_key)

    def set_len(self):
        return self.redis_conn.zcard(self.set_key)

    def __delitem__(self, key):
        self.redis_conn.hdel(self.hash_key, key)
        self.redis_conn.zrem(self.set_key, key)


class FifoDiskQueue(object):
    """持久化 FIFO 队列."""

    szhdr_format = ">L"
    szhdr_size = struct.calcsize(szhdr_format)

    def __init__(self, path, chunksize=100000):
        self.lock = RLock()
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.info = self._loadinfo(chunksize)
        self.chunksize = self.info['chunksize']
        self.headf = self._openchunk(self.info['head'][0], 'ab+')
        self.tailf = self._openchunk(self.info['tail'][0])
        os.lseek(self.tailf.fileno(), self.info['tail'][2], os.SEEK_SET)

    @thread_safe_for_method_in_class
    @call_later(callback="_saveinfo")
    def push(self, *strings):
        for string in strings:
            self._push(string)

    def _push(self, string):
        if not isinstance(string, bytes):
            raise TypeError('Unsupported type: {}'.format(type(string).__name__))
        hnum, hpos = self.info['head']
        hpos += 1
        szhdr = struct.pack(self.szhdr_format, len(string))
        os.write(self.headf.fileno(), szhdr + string)
        if hpos == self.chunksize:
            hpos = 0
            hnum += 1
            self.headf.close()
            self.headf = self._openchunk(hnum, 'ab+')
        self.info['size'] += 1
        self.info['head'] = [hnum, hpos]

    def _openchunk(self, number, mode='rb'):
        return open(os.path.join(self.path, 'q%05d' % number), mode)

    @call_later(callback="_saveinfo")
    def rid(self, count):
        messages = []
        message = self.pop()
        while message and len(messages) < count:
            messages.append(message)
            message = self.pop()
        return messages

    @thread_safe_for_method_in_class
    @call_later(callback="_saveinfo", immediately=False)
    def pop(self):
        tnum, tcnt, toffset = self.info['tail']
        if [tnum, tcnt] >= self.info['head']:
            return
        tfd = self.tailf.fileno()
        szhdr = os.read(tfd, self.szhdr_size)
        if not szhdr:
            return
        size, = struct.unpack(self.szhdr_format, szhdr)
        data = os.read(tfd, size)
        tcnt += 1
        toffset += self.szhdr_size + size
        if tcnt == self.chunksize and tnum <= self.info['head'][0]:
            tcnt = toffset = 0
            tnum += 1
            self.tailf.close()
            os.remove(self.tailf.name)
            self.tailf = self._openchunk(tnum)
        self.info['size'] -= 1
        self.info['tail'] = [tnum, tcnt, toffset]
        return data

    def close(self):
        self.headf.close()
        self.tailf.close()
        self._saveinfo()
        if len(self) == 0:
            self._cleanup()

    def __len__(self):
        return self.info['size']

    def _loadinfo(self, chunksize):
        infopath = self._infopath()
        if os.path.exists(infopath):
            try:
                with open(infopath) as f:
                    return json.load(f)
            except json.decoder.JSONDecodeError:
                import traceback
                traceback.print_exc()
                os.unlink(infopath)
        return {
                'chunksize': chunksize,
                'size': 0,
                'tail': [0, 0, 0],
                'head': [0, 0],
            }

    def _saveinfo(self):
        with open(self._infopath(), 'w') as f:
            json.dump(self.info, f)

    def _infopath(self):
        return os.path.join(self.path, 'info.json')

    def _cleanup(self):
        for x in glob.glob(os.path.join(self.path, 'q*')):
            os.remove(x)
        os.remove(os.path.join(self.path, 'info.json'))
        if not os.listdir(self.path):
            os.rmdir(self.path)