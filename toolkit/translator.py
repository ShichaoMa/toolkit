from translate import TranslateAdapter

from .monitors import ProxyPool


class Translator(ProxyPool, TranslateAdapter):
    """
        翻译类
    """
    name = "translator"
    web_site = None
    translate_timeout = None
    retry_times = None

    def __init__(self, settings):
        super(Translator, self).__init__(settings=settings)
        self.web_site = self.settings.get("WEBSITE", "baidu,qq,google").split(",")
        self.retry_times = self.settings.get("TRANSLATE_RETRY_TIMES", 10)
        self.translate_timeout = self.settings.get("TRANSLATE_TIMEOUT", 10)