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

    def test_normalize(self):
        a = Frozen([{"b": 3}, {"a", "b"}, ["c", ["b", "d"]]])
        assert isinstance(a.normalize(), list)
        assert isinstance(a[0], Frozen)
        assert isinstance(a.normalize()[0], dict)
        assert isinstance(a[1], Frozen)
        assert any(isinstance(i, Frozen) for i in a[2])
        assert any(isinstance(i, list) for i in a[2].normalize())

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
