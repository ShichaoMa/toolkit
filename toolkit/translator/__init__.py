from ..monitors import ProxyPool
from .translate_adapter import TranslateAdapter

__all__ = ["Translator"]


class Translator(ProxyPool, TranslateAdapter):
    """
        基于代理池的翻译类
    """
    name = "translator"
    web_site = None
    translate_timeout = None
    retry_times = None

    def __init__(self, settings):
        super(Translator, self).__init__(settings=settings)
        self.web_site = self.settings.get(
            "WEBSITE", "baidu,qq,google").split(",")
        self.retry_times = self.settings.get("TRANSLATE_RETRY_TIMES", 10)
        self.translate_timeout = self.settings.get("TRANSLATE_TIMEOUT", 10)
        self.headers = self.settings.get("HEADERS") or self.headers
