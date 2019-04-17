from collections.abc import MutableSequence, MutableMapping, MutableSet

__all__ = ["Frozen", "FrozenSettings"]


class Frozen(MutableSequence, MutableMapping):
    """
    替换json取数由[]变成.的形式
    """
    def __new__(cls, json):
        if isinstance(json, (MutableSequence, MutableSet)):
            instance = super().__new__(cls)
            object.__setattr__(instance, "_json",
                               json.__class__(cls(val) for val in json))
        elif isinstance(json, MutableMapping):
            instance = super().__new__(cls)
            object.__setattr__(instance, "_json", json)
        else:
            instance = json
        return instance

    def __getattr__(self, item):
        if hasattr(self._json, item):
            return getattr(self._json, item)
        else:
            prop_val = self._json.get(item)
            if prop_val is None:
                raise AttributeError(item)
            elif isinstance(prop_val, (list, dict)):
                return self.__class__(prop_val)
            else:
                return prop_val

    def __setattr__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, item):
        return self._json[item]

    def __iter__(self):
        return iter(self._json)

    def __bool__(self):
        return bool(self._json)

    def __len__(self):
        return len(self._json)

    def __delitem__(self, item):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def insert(self, index, value):
        raise NotImplementedError

    def __str__(self):
        return str(self._json)

    __repr__ = __str__

    def normalize(self):
        """
        使用Frozen对象获取列表或字典时，为了支持级联`.`操作，
        字典和列表对象被转换成了Frozen对象，如果直接使用，有时可能会引发错误。
        使用此方法得到真实的列表或字典。
        :return:
        """
        val = self._json
        if isinstance(val, (MutableSequence, MutableSet)):
            return val.__class__(
                i.normalize() if hasattr(i, "normalize") else i for i in val)
        else:
            return val


class FrozenSettings(Frozen):
    pass


if __name__ == "__main__":
    json = {"aa": [1, 2, 3, {"b": 3, "c": [4, 5, {"d": 33}]}]}
    f = Frozen(json)
    print(f.aa[3].c[2].d)
    print(f)
