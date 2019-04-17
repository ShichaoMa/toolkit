from toolkit.singleton import Singleton


class A(metaclass=Singleton):
    pass


class TestSingleton:

    def test_singleton(self):
        assert A() is A()
