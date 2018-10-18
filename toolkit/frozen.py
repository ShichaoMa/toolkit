from collections.abc import MutableSequence, MutableMapping, MutableSet

__all__ = ["Frozen", "FrozenSettings"]


class Frozen(MutableSequence, MutableMapping):
    """
    替换json取数由[]变成.的形式
    """
    def __new__(cls, json):
        if isinstance(json, (MutableSequence, MutableSet)):
            instance = super().__new__(cls)
            instance.json = [cls(val) for val in json]
        elif isinstance(json, MutableMapping):
            instance = super().__new__(cls)
            instance.json = json
        else:
            instance = json
        return instance

    def __getattr__(self, item):
        if hasattr(self.json, item):
            return getattr(self.json, item)
        else:
            prop_val = self.json.get(item)
            if prop_val is None:
                raise AttributeError(item)
            elif isinstance(prop_val, (list, dict)):
                return self.__class__(prop_val)
            else:
                return prop_val

    def __getitem__(self, item):
        return self.json[item]

    def __iter__(self):
        return iter(self.json)

    def __bool__(self):
        return bool(self.json)

    def __len__(self):
        return len(self.json)

    def __delitem__(self, item):
        return NotImplemented

    def __setitem__(self, key, value):
        return NotImplemented

    def insert(self, index, value):
        return NotImplemented

    def __str__(self):
        return str(self.json)

    __repr__ = __str__


class FrozenSettings(Frozen):
    pass


if __name__ == "__main__":
    json = {"aa": [1, 2, 3, {"b": 3, "c": [4, 5, {"d": 33}]} ]}
    f = Frozen(json)
    print(f.aa[3].c[2].d)
