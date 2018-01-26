import unittest
from toolkit.translator import Translator


class TranslateTest(unittest.TestCase):

    def assertContainEqual(self, first, second, msg=None):
        if not first.count(second):
            msg = self._formatMessage(msg, "%s is not contain %s"%(first, second))
            self.fail(msg)

    # def test_translate(self):
    #     with Translator({"WEB_SITE": "baidu"}) as t:
    #         t.set_logger()
    #         src = t.translate("my name is tom, what about yours?")
    #         print(111111111, t.settings.WEB_SITE, src)
    #         self.assertContainEqual(src, "我")

    # def test_google(self):
    #     with Translator({"WEB_SITE": "google"}) as t:
    #         t.set_logger()
    #         src = t.translate("my name is tom, what about yours?")
    #         print(111111111, t.settings.WEB_SITE, src)
    #         self.assertContainEqual(src, "我")

    # def test_qq(self):
    #     with Translator({"WEB_SITE": "qq"}) as t:
    #         t.set_logger()
    #         src = t.translate("my name is tom, what about yours?")
    #         print(111111111, t.settings.WEB_SITE, src)
    #         self.assertContainEqual(src, "我")

    def test_bing(self):
        with Translator({"WEB_SITE": "bing"}) as t:
            t.set_logger()
            src = t.translate("my name is tom, what about yours?")
            print(111111111, t.settings.WEB_SITE, src)
            self.assertContainEqual(src, "我")

if __name__ == "__main__":
    unittest.main()
