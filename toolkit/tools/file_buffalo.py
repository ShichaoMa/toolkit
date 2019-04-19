import time
import asyncio

from threading import RLock


class FileBuffalo(object):
    """
    文件流管道， 同步写，异步读
    """
    def __init__(self, max_size=1024*1024):
        self._max_size = max_size
        self._datas = list()
        self._size = 0
        self._finished = False
        self.name = "tmp"
        self.lock = RLock()

    @property
    def finished(self):
        return not self._finished and not self._datas

    def finish(self):
        self._finished = True

    def write(self, data):
        """
        同步写接口
        :param data:
        :return:
        """
        while not self._finished:
            with self.lock:
                if self._size < self._max_size:
                    self._datas.append(data)
                    self._size += len(data)
                    break
            time.sleep(0.1)

    async def read(self, size=1024000):
        """
        异步读接口
        :param size:
        :return:
        """
        buffer = b""
        while not self.finished and len(buffer) < size:
            if self._datas:
                with self.lock:
                    data = self._datas.pop(0)
                    buffer += data
                    self._size -= len(data)
            else:
                await asyncio.sleep(0.1)
        return buffer
