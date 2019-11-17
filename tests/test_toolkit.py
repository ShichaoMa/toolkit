import time

from toolkit import cache_classproperty, cache_property, clear_cache, global_cache_classproperty


class A(object):

    @cache_classproperty
    def fun(self):
        return time.time()

    @global_cache_classproperty
    def zoo(self):
        return time.time()

    @cache_property
    def bar(self):
        return time.time()


class B(A):
    pass


def test_clear_cache():
    a = A()
    fun = a.fun
    bar = a.bar
    zoo = a.zoo
    time.sleep(1)
    assert a.fun == fun
    assert a.bar == bar
    assert a.zoo == zoo
    clear_cache(A, "fun")
    clear_cache(A, "zoo")
    clear_cache(a, "bar")
    assert a.fun != fun
    assert a.bar != bar
    assert a.zoo != zoo
    assert A.fun != B.fun
    assert A.zoo == B.zoo
