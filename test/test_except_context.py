import unittest
from toolkit.managers import ExceptContext


class ExceptContextTest(unittest.TestCase):

    def test_raise(self):
        with self.assertRaises(Exception):
            with ExceptContext(Exception, errback=lambda name, *args: print(name)):
                raise Exception("test. ..")

    @staticmethod
    def fun():
        with ExceptContext(Exception, errback=lambda name, *args: print(name) is None):
            raise Exception("test. ..")

    def test_no_raise(self):
        self.assertIsNone(self.fun())


if __name__ == "__main__":
    unittest.main()