from toolkit import property_cache, cache_property


b = 3


class A(object):

    @property
    @property_cache
    def env_a(self):
        return b

    @cache_property
    def env_a_act(self):
        return b


class TestCache(object):

    def test_a(self):
        a = A()
        assert a.env_a == 3
        assert a.env_a_act == 3
        global b
        b = 4
        assert a.env_a == 3
        assert a.env_a_act == 3
        assert b == 4
