import time
import unittest
from toolkit import test_prepare
test_prepare()
from toolkit.translator import Translator


class TranslateTest(unittest.TestCase):

    def assertContainEqual(self, first, second, msg=None):
        if not first.count(second):
            msg = self._formatMessage(msg, "%s is not contain %s" % (first, second))
            self.fail(msg)

    def trans_thread(self, site):
        with Translator({"WEBSITE": site}) as translator:
            for i in range(5):
                result = translator.translate("what %s fuck day it is!" % i)
                translator.logger.info(result)
                self.assertContainEqual(result, "天")
                time.sleep(0.1)

    # def test_baidu(self):
    #     threads = list()
    #     for i in range(10):
    #         th = Thread(target=self.trans_thread, args=("baidu", ))
    #         th.start()
    #         threads.append(th)
    #     for th in threads:
    #         th.join()

    # def test_google(self):
    #     threads = list()
    #     for i in range(10):
    #         th = Thread(target=self.trans_thread, args=("google", ))
    #         th.start()
    #         threads.append(th)
    #     for th in threads:
    #         th.join()

    # def test_bing(self):
    #     threads = list()
    #     for i in range(10):
    #         th = Thread(target=self.trans_thread, args=("bing", ))
    #         th.start()
    #         threads.append(th)
    #     for th in threads:
    #         th.join()

    def test_qq(self):
        with Translator({"WEBSITE": "qq"}) as t:
            rs = t.translate("what a fuck day it is!")
            t.logger.info(rs)
            self.assertContainEqual(rs, "天")


if __name__ == "__main__":
    unittest.main()
