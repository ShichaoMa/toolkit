from toolkit.translator import Translator
from toolkit import test_prepare
test_prepare()
with Translator({"WEBSITE": "baidu"}) as translator:
    for i in range(10):
        result = translator.translate("what a fuck day it is!")
        translator.logger.info(result)
