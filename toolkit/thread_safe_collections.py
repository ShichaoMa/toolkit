from threading import RLock
from collections import UserDict
from collections.abc import MutableSet

from . import thread_safe_for_method


class ThreadSafeSet(MutableSet):
    def __init__(self, *args, **kwargs):
        self._data = set(*args, **kwargs)
        self.lock = RLock()

    @thread_safe_for_method
    def add(self, value):
        return self._data.add(value)

    @thread_safe_for_method
    def discard(self, value):
        return self._data.discard(value)

    @thread_safe_for_method
    def pop_all(self):
        while len(self._data):
            yield self.pop()

    @thread_safe_for_method
    def update(self, seq):
        self._data.update(seq)

    @thread_safe_for_method
    def __contains__(self, item):
        return item in self._data

    @thread_safe_for_method
    def __iter__(self):
        return iter(self._data)

    @thread_safe_for_method
    def __len__(self):
        return len(self._data)


class TreadSafeDict(UserDict):
    def __init__(self, *args, **kwargs):
        super(TreadSafeDict, self).__init__(*args, **kwargs)
        self.lock = RLock()

    @thread_safe_for_method
    def update(*args, **kwds):
        super(TreadSafeDict, args[0]).update(*args[1:], **kwds)

    @thread_safe_for_method
    def pop_all(self):
        while len(self):
            yield self.popitem()
