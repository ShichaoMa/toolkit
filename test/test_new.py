"""
实例创建时，调用顺序
元类的__call__
类的__new__
类的__init__
子类的元类(除type以外)必须是父类元类的子类
"""
import unittest

from toolkit.monitors import Singleton


class SingletonTest(unittest.TestCase):

    class A(metaclass=Singleton):
        pass

    def test_single(self):

        self.assertIs(SingletonTest.A(), SingletonTest.A())


if __name__ == "__main__":
    unittest.main()