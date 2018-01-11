# -*- coding:utf-8 -*-
import os
import glob
import json
import struct

from threading import RLock
from abc import ABC, abstractmethod

from . import thread_safe_for_method, call_later
from .managers import ExceptContext

__all__ = ["Queue", "RedisQueue", "FifoDiskQueue"]


class Queue(ABC):

    def __init__(self):
        self.lock = RLock()

    @abstractmethod
    def push(self, *strings):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def rid(self, count):
        pass

    @abstractmethod
    def clear(self):
        pass


class RedisQueue(Queue):
    """
    redis队列
    """
    def __init__(self, redis_conn, key):
        super(RedisQueue, self).__init__()
        self.redis_conn = redis_conn
        self.key = key

    @thread_safe_for_method
    def push(self, *strings):
        self.redis_conn.rpush(self.key, *strings)

    @thread_safe_for_method
    def pop(self):
        return self.redis_conn.lpop(self.key)

    def __len__(self):
        return self.redis_conn.llen(self.key)

    @thread_safe_for_method
    def rid(self, count):
        pipe = self.redis_conn.pipeline()
        pipe.multi()
        pipe.lrange(self.key, 0, count-1).ltrim(self.key, count, -1)
        results, count = pipe.execute()
        return results

    def clear(self):
        self.redis_conn.delete(self.key)

    def close(self):
        pass


class FifoDiskQueue(Queue):
    """持久化 FIFO 队列."""

    szhdr_format = ">L"
    szhdr_size = struct.calcsize(szhdr_format)

    def __init__(self, path, chunk_size=100000):
        super(FifoDiskQueue, self).__init__()
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.info = self._load_info(chunk_size)
        self.chunk_size = self.info['chunk_size']
        self.headf = self._open_chunk(self.info['head'][0], 'ab+')
        self.tailf = self._open_chunk(self.info['tail'][0])
        os.lseek(self.tailf.fileno(), self.info['tail'][2], os.SEEK_SET)

    @thread_safe_for_method
    @call_later(callback="_save_info")
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
        if hpos == self.chunk_size:
            hpos = 0
            hnum += 1
            self.headf.close()
            self.headf = self._open_chunk(hnum, 'ab+')
        self.info['size'] += 1
        self.info['head'] = [hnum, hpos]

    def _open_chunk(self, number, mode='rb'):
        return open(os.path.join(self.path, 'q%05d' % number), mode)

    @call_later(callback="_save_info")
    def rid(self, count):
        messages = []
        while len(messages) < count:
            message = self.pop()
            if message:
                messages.append(message)
            else:
                break
        return messages

    @thread_safe_for_method
    @call_later(callback="_save_info", immediately=False)
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
        if tcnt == self.chunk_size and tnum <= self.info['head'][0]:
            tcnt = toffset = 0
            tnum += 1
            self.tailf.close()
            os.remove(self.tailf.name)
            self.tailf = self._open_chunk(tnum)
        self.info['size'] -= 1
        self.info['tail'] = [tnum, tcnt, toffset]
        return data

    def clear(self):
        self._cleanup()
        self._load_info(self.chunk_size)

    def close(self):
        self.headf.close()
        self.tailf.close()
        self._save_info()
        if len(self) == 0:
            self._cleanup()

    def __len__(self):
        return self.info['size']

    def _load_info(self, chunk_size):
        infopath = self._info_path()
        if os.path.exists(infopath):
            with ExceptContext(json.decoder.JSONDecodeError):
                with open(infopath) as f:
                    return json.load(f)
            os.unlink(infopath)
        return {
                'chunk_size': chunk_size,
                'size': 0,
                'tail': [0, 0, 0],
                'head': [0, 0],
            }

    def _save_info(self):
        with open(self._info_path(), 'w') as f:
            json.dump(self.info, f)

    def _info_path(self):
        return os.path.join(self.path, 'info.json')

    def _cleanup(self):
        for x in glob.glob(os.path.join(self.path, 'q*')):
            os.remove(x)
        os.remove(os.path.join(self.path, 'info.json'))
        if not os.listdir(self.path):
            os.rmdir(self.path)