from translate import TranslateAdapter

from .monitors import ProxyPool


class Translator(ProxyPool, TranslateAdapter):
    """
        翻译类
    """
    name = "translator"

    def __init__(self, settings):
        super(Translator, self).__init__(settings=settings)
        self._web_site = self.settings.get("WEBSITE", "baidu,qq,google").split(",")
        self._retry_times = self.settings.get("TRANSLATE_RETRY_TIMES", 10)
        self._translate_timeout = self.settings.get("TRANSLATE_TIMEOUT", 10)

    @property
    def web_site(self):
        return self._web_site

    @property
    def translate_timeout(self):
        return self._translate_timeout

    @property
    def retry_times(self):
        return self._retry_times
