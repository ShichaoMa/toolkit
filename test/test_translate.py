import unittest
from toolkit.translator import Translator


class TranslateTest(unittest.TestCase):

    def assertContainEqual(self, first, second, msg=None):
        if not first.count(second):
            msg = self._formatMessage(msg, "%s is not contain %s"%(first, second))
            self.fail(msg)

    def test_translate(self):
        with Translator("settings") as t:
            t.set_logger()
            self.assertContainEqual(t.translate("my name is tom, what about yours?"), "我")

if __name__ == "__main__":
    unittest.main()
