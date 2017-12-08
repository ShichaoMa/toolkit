import unittest
from toolkit.monitors import Service


class SingletonTest(unittest.TestCase):

    def test(self):
      self.assertIs(Service(), Service())


if __name__ == "__main__":
    unittest.main()