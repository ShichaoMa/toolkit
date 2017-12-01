import re
import json
import requests
import warnings
import traceback

from googletrans.gtoken import TokenAcquirer

from . import retry_wrapper
from .monitors import ProxyPool
from .managers import ExceptContext


class Translate(ProxyPool):
    """
        翻译类
    """
    def __init__(self, settings):
        super(Translate, self).__init__(settings)
        self.web_site = self.settings.get("WEBSITE", "baidu,qq,google").split(",")
        self.site_count = 0
        self.session = requests.Session()
        self.acquirer = TokenAcquirer(session=self.session, host="translate.google.cn")

    def trans_error_handler(self, func_name, retry_time, e, *args, **kwargs):
        """
        error_handler实现参数
        :param func_name: 重试函数的名字
        :param retry_time: 重试到了第几次
        :param e: 需要重试的异常
        :param args: 重试参数的参数
        :param kwargs: 重试参数的参数
        :return: 当返回True时，该异常不会计入重试次数
        """
        self.logger.error("Error in %s for retry %s times: %s"%(func_name, retry_time, e))
        # 更新代理Ip
        args[1].update(self.proxy_choice())

    def site_choice(self):
        """
        顺序循环选择翻译网站
        :return: site
        """
        self.site_count += 1
        return self.web_site[self.site_count%len(self.web_site)]

    def translate(self, src):
        """
        翻译主函数
        :param src: 源
        :return: 结果
        """
        with ExceptContext(errback=lambda func_name, *args: self.logger.error(
                        "Error in translate, finally, we could not get the translate result. src: %s, Error:  %s"%(
                        src, "".join(traceback.format_exception(*args)))) is None):
            # 找出大于号和小于号之间的字符，使用换行符连接，进行翻译
            pattern = re.compile(r"(?:^|(?<=>))([\s\S]*?)(?:(?=<)|$)")
            ls = re.findall(pattern, src.replace("\n", ""))
            src_data = "\n".join(x.strip("\t ") for x in ls if x.strip())
            if src_data.strip():
                # 对源中的%号进行转义
                src_escape = src.replace("%", "%%")
                # 将源中被抽离进行翻译的部分替换成`%s`， 如果被抽离部分没有实质内容（为空），则省略
                src_template = re.sub(pattern, lambda x: "%s" if x.group(1).strip() else "", src_escape)
                return retry_wrapper(self.settings.get_int("TRANSLATE_RETRY_TIME", 10), error_handler=self.trans_error_handler)(
                    self._translate)(src_data, self.proxy or self.proxy_choice(), src_template)
        return src

    def _translate(self, src, proxies, src_template):
        return getattr(self, self.site_choice().strip())(
            src, proxies, src_template)

    def youdao(self, src_data, proxies, src_template):
        """
        有道翻译的实现,已过时
        :param src_data: 原生数据
        :param proxies: 代理
        :param src_template: 原生数据模板
        :return: 结果
        """
        warnings.warn("youdao is a deprecated alias, use other site instead.", DeprecationWarning, 2)
        url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"#"http://fanyi.youdao.com/translate"
        self.logger.debug("Process request %s with proxy: %s"%(url, proxies))
        resp = requests.post(url=url, data={
            'keyfrom': 'fanyi.web',
            'i': src_data,
            'doctype': 'json',
            'action': 'FY_BY_CLICKBUTTON',
            'ue': 'UTF-8',
            'xmlVersion': '1.8',
            'type': 'AUTO',
            'typoResult': 'true'}, headers=self.settings.get("HEADERS"),
                      timeout=self.settings.get_int("TRANSLATE_TIMEOUT", 5), proxies=proxies)
        return src_template % tuple(map(lambda y: "".join(
            map(lambda x: x["tgt"], y)), json.loads(resp.text)["translateResult"]))

    def qq(self, src_data, proxies, src_template, url='http://fanyi.qq.com/api/translate'):
        """
        腾讯翻译的实现, 腾讯翻译最长只能翻译2000个字符
        :param url: 翻译api
        :param src_data: 原生数据
        :param proxies: 代理
        :param src_template: 原生数据模板
        :return: 结果
        """
        self.logger.debug("Process request %s with proxy: %s" % (url, proxies))
        resp = requests.post(
            url, data={'source': 'auto', 'target': 'en', 'sourceText': src_data},
            headers=self.settings.get("HEADERS"), timeout=self.settings.get_int("TRANSLATE_TIMEOUT", 5), proxies=proxies)
        return src_template % tuple(
            record["targetText"] for record in json.loads(resp.text)["records"] if record.get("sourceText") != "\n")

    def baidu(self, src_data, proxies, src_template,
              url="http://fanyi.baidu.com/v2transapi",
              select_url="http://fanyi.baidu.com/langdetect"):
        """
        百度翻译的实现, 百度翻译最长只能翻译5000个字符
        :param src_data: 原生数据
        :param proxies: 代理
        :param src_template: 原生数据模板
        :param url: 翻译api
        :param select_url: 语言选择api
        :return: 结果
        """

        self.logger.debug("Select lang. ")
        resp = requests.post(url=select_url, data={
            "query": src_data[:50]
        })
        try:
            lan = json.loads(resp.text)["lan"]
        except Exception:
            lan = "en"

        self.logger.debug("Process request %s with proxy: %s" % (url, proxies))
        resp = requests.post(url=url, data={
            'from': lan,
            'to': 'zh',
            'transtype': 'realtime',
            'query': src_data,
            'simple_means_flag': 3
        }, headers=self.settings.get("HEADERS"), timeout=self.settings.get_int("TRANSLATE_TIMEOUT", 5), proxies=proxies)
        result = src_template % tuple(
            "".join(map(lambda x: x["src_str"], json.loads(resp.text)["trans_result"]['phonetic'])).split("\n"))
        return result

    def google(self, src_data,  proxies, src_template, url='https://translate.google.cn/translate_a/single'):
        """
        谷歌翻译的实现
        :param url: 翻译api
        :param src_data: 原生数据
        :param proxies: 代理
        :param src_template: 原生数据模板
        :return: 结果
        """
        self.logger.debug("Process request %s with proxy: %s" % (url, proxies))
        resp = self.session.get(url=url, params={
        'client': 't',
        'sl': "auto",
        'tl': "zh",
        'hl': "zh",
        'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'otf': 1,
        'ssel': 0,
        'tsel': 0,
        'tk': self.acquirer.do(src_data),
        'q': src_data,
        }, headers=self.settings.get("HEADERS"), timeout=self.settings.get_int("TRANSLATE_TIMEOUT", 5), proxies=proxies)
        return self.merge_conflict(src_template, [line[0] for line in json.loads(resp.text)[0]])

    @staticmethod
    def merge_conflict(src_template, returns):
        return src_template % tuple(returns[:src_template.count("%s")])