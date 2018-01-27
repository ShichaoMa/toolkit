from toolkit.translator import Translator

with Translator({"WEBSITE": "bing"}) as translator:

    result = translator.translate("what a fuck day it is!")
    translator.logger.info(result)
