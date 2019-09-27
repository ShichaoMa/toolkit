import random

from redis import Redis
from itertools import repeat

from .translate_adapter import TranslateAdapter

__all__ = ["Translator"]


class Translator(TranslateAdapter):
    """
        基于代理池的翻译类
    """
    name = "translator"
    web_site = None
    translate_timeout = None
    retry_times = None

    def __init__(self, settings):
        super(Translator, self).__init__()
        self.web_site = settings.get(
            "WEBSITE", "baidu,qq,google").split(",")
        self.retry_times = settings.get("TRANSLATE_RETRY_TIMES", 10)
        self.translate_timeout = settings.get("TRANSLATE_TIMEOUT", 10)
        self.headers = settings.get("HEADERS") or self.headers
        self.protocols = settings.get("PROTOCOLS", "http,https").split(
            ",")
        self.redis_conn = Redis(
            settings.get("REDIS_HOST", "0.0.0.0"),
            settings.get_int("REDIS_PORT", 6379))
        self.proxy_sets = settings.get("PROXY_SETS", "proxy_set").split(",")
        self.account_password = settings.get("PROXY_ACCOUNT_PASSWORD", "")

    def proxy_choice(self):
        """
        随机选取代理
        :return: 代理
        """
        proxy = self.redis_conn.srandmember(random.choice(self.proxy_sets))
        if proxy:
            proxy_str = "http://%s%s" % (
                self.account_password+"@" if self.account_password else "",
                proxy.decode())
            self.proxy = dict(zip(self.protocols, repeat(proxy_str)))
        return self.proxy