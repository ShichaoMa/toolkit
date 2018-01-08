from threading import RLock
from collections import UserDict
from collections.abc import MutableSet

from . import thread_safe_for_method_in_class


class ThreadSafeSet(MutableSet):
    def __init__(self, *args, **kwargs):
        self._data = set(*args, **kwargs)
        self.lock = RLock()

    @thread_safe_for_method_in_class
    def add(self, value):
        return self._data.add(value)

    @thread_safe_for_method_in_class
    def discard(self, value):
        return self._data.discard(value)

    @thread_safe_for_method_in_class
    def pop_all(self):
        while len(self._data):
            yield self.pop()

    @thread_safe_for_method_in_class
    def update(self, seq):
        self._data.update(seq)

    @thread_safe_for_method_in_class
    def __contains__(self, item):
        return item in self._data

    @thread_safe_for_method_in_class
    def __iter__(self):
        return iter(self._data)

    @thread_safe_for_method_in_class
    def __len__(self):
        return len(self._data)


class TreadSafeDict(UserDict):
    def __init__(self, *args, **kwargs):
        super(TreadSafeDict, self).__init__(*args, **kwargs)
        self.lock = RLock()

    @thread_safe_for_method_in_class
    def update(*args, **kwds):
        super(TreadSafeDict, args[0]).update(*args[1:], **kwds)

    @thread_safe_for_method_in_class
    def pop_all(self):
        while len(self):
            yield self.popitem()
