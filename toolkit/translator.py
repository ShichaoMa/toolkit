from translate import Translate, sites

from .monitors import ProxyPool


class Translator(ProxyPool, Translate):
    """
        翻译类
    """
    name = "translator"

    def __init__(self, settings):
        super(Translator, self).__init__(settings=settings)
        self.web_site = self.settings.get("WEBSITE", "baidu,qq,google").split(",")
        self.retry_times = self.settings.get("TRANSLATE_RETRY_TIMES", 10)
        self.translate_timeout = self.settings.get("TRANSLATE_TIMEOUT", 10)
        self.load(sites)
