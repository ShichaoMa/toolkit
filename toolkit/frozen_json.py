class FrozenJSON(object):
    """
    替换json取数由[]变成.的形式
    """
    def __new__(cls, json):
        if isinstance(json, list):
            instance = super(FrozenJSON, cls).__new__(cls)
            instance.json = [cls(val) for val in json]
        elif isinstance(json, dict):
            instance = super(FrozenJSON, cls).__new__(cls)
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
                raise KeyError(item)
            elif isinstance(prop_val, (list, dict)):
                return self.__class__(prop_val)
            else:
                return prop_val

    def __getitem__(self, item):
        return self.json[item]

    def __str__(self):
        return str(self.json)

    __repr__ = __str__


if __name__ == "__main__":
    json = {"aa": [1, 2, 3,{"b": 3, "c": [4, 5, {"d": 33}]} ]}
    f = FrozenJSON(json)
    print(f.aa[3].c[2].d)