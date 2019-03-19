from toolkit import _property_cache, cache_property, \
    cache_classproperty, classproperty, global_cache_classproperty


class A(object):

    c = 4
    b = 3

    @property
    @_property_cache
    def a(self):
        return self.b

    @cache_property
    def a_cache(self):
        return self.b

    @classproperty
    def d(cls):
        return cls.c

    @cache_classproperty
    def d_cache(cls):
        return cls.c

    @global_cache_classproperty
    def d_global_cache(cls):
        return cls.c


class B(A):
    pass


class TestCache(object):

    def test_cache_property(self):
        A.b = 3
        a = A()
        assert a.a == 3
        assert a.a_cache == 3
        global b
        A.b = 4
        assert a.a == 3
        assert a.a_cache == 3
        assert A.b == 4

    def test_classproperty(self):
        A.c = 4
        a = A()
        assert a.d == 4
        A.c = 5
        assert a.d == 5

    def test_cache_class_property(self):
        A.c = 4
        a = A()
        assert a.d_cache == 4
        A.c = 5
        assert a.d_cache == 4

    def test_global_cache_class_property(self):
        A.c = 4
        a = A()
        b = B()
        assert b.d_global_cache == 4
        A.c = 6
        assert b.d_global_cache == 4
        assert a.d_global_cache == 4