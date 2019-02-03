import pytest

from toolkit.frozen import Frozen


class TestFrozen(object):

    def test_dict_get(self):
        a = Frozen({"a": 1})
        assert a["a"] == 1
        assert a.a == 1

    def test_list_dict_get(self):
        a = Frozen([{"b": 3}])
        assert a[0].b == 3

    def test_readonly(self):
        a = Frozen({"a": 1})
        with pytest.raises(NotImplementedError):
            a.a = 3

        with pytest.raises(NotImplementedError):
            a["a"] = 3

        with pytest.raises(NotImplementedError):
            del a["a"]

        b = Frozen([])
        with pytest.raises(NotImplementedError):
            b.insert(0, "1")
