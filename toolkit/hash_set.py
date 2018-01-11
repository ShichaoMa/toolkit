import copy

from collections.abc import MutableSet

__all__ = ["HashSet"]


class HashSet(MutableSet):
    """
    自实现hashset，采用多维数组的方式进行存储数据，读写的性能比set差，但内存使用量比set少
    """
    data_tmp = [None] * 10

    def __init__(self):
        self.data = copy.copy(self.data_tmp)
        self.size = 0

    def add(self, value):
        self.dive(hash(value), self.data, value)

    def dive(self, hash_val, current_list, value, remove=False, contains=False):
        div, mod = divmod(hash_val, 10)
        if current_list[mod] is None:
            current_list[mod] = copy.copy(self.data_tmp)
        elif not isinstance(current_list[mod], list):
            val = current_list[mod]
            current_list[mod] = copy.copy(self.data_tmp)
            current_list[mod][0] = val
        if div > 9:
            result = self.dive(div, current_list[mod], value, remove, contains)
            if result:
                if not filter(None, current_list[mod]):
                    current_list[mod] = None
                    return True
            return result
        elif remove:
            cur_li, index, current_node = self._first(current_list[mod][div])
            cur_li = cur_li or current_list[mod]
            index = index if index is not None else div
            if current_node is not None:
                if not contains:
                    cur_li[index] = None
                    self.size -= 1
                return True
            else:
                if not contains:
                    raise KeyError(value)
                return False
        else:
            if current_list[mod][div] is None:
                current_list[mod][div] = value
                self.size += 1
            else:
                return False

    def _first(self, ls):
        if isinstance(ls, list):
            return ls, 0, self._first(ls[0])[2]
        else:
            return None, None, ls

    def __iter__(self):
        return self.next(self.data)

    def next(self, ls):
        for i in ls:
            if isinstance(i, list):
                yield from self.next(i)
            else:
                if i is not None:
                    yield i

    def __len__(self):
        return self.size

    def __contains__(self, value):
        return self.dive(hash(value), self.data, value, True, True)

    def remove(self, value):
        return self.dive(hash(value), self.data, value, True)

    discard = remove

    def join_str(self, li):
        if isinstance(li, list):
            total = ""
            for l in li:
                total += self.join_str(l)
            return total
        else:
            if li is not None:
                return str(li) + ","
            else:
                return ""

    def __str__(self):
        return "{%s}"%self.join_str(self.data).strip(",")

    __repr__ = __str__
