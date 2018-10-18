import json
import time


def merge_conflict(src_template, returns):
    return src_template % tuple(returns[:src_template.count("%s")]) + \
           "。".join(returns[src_template.count("%s"):])


def youdao(self, src_data, proxies, src_template):
    """
    有道翻译的实现(废弃)
    :param src_data: 原生数据
    :param proxies: 代理
    :param src_template: 原生数据模板
    :return: 结果
    """
    url = "http://fanyi.youdao.com/translate"
    resp = self.session.post(url=url, data={
        'keyfrom': 'fanyi.web',
        'i': src_data,
        'doctype': 'json',
        'action': 'FY_BY_CLICKBUTTON',
        'ue': 'UTF-8',
        'xmlVersion': '1.8',
        'type': 'AUTO',
        'typoResult': 'true'}, headers=self.headers,
                         timeout=self.translate_timeout, proxies=proxies)
    return src_template % tuple(map(lambda y: "".join(
        map(lambda x: x["tgt"], y)), json.loads(resp.text)["translateResult"]))


def bing(self, src_data, proxies, src_template, acquirer):
    """
    必应翻译的实现
    :param src_data: 原生数据
    :param proxies: 代理
    :param src_template: 原生数据模板
    :return: 结果
    """
    with acquirer:
        url = "https://cn.bing.com/translator/api/Translate/TranslateArray?" \
              "from=-&to=zh-CHS"
        data_mapping = dict(
            (d, acquirer.acquire(d)) for d in src_data.split("\n"))
        resp = self.session.post(
            url=url,
            json=[{"id": acquirer.acquire(d), "text": d}
                  for d in src_data.split("\n")],
            headers=self.headers,
            timeout=self.translate_timeout, proxies=proxies)
        trans_rs = dict((item["id"], item["text"])
                        for item in json.loads(resp.text)["items"])
        finish_data = [trans_rs[str(data_mapping.get(d))]
                       for d in src_data.split("\n")]
        return src_template % tuple(finish_data)


def baidu(self, src_data, proxies, src_template, acquirer):
    """
    百度翻译的实现, 百度翻译最长只能翻译5000个字符
    :param src_data: 原生数据
    :param proxies: 代理
    :param src_template: 原生数据模板
    :param acquirer: token获取器
    :return: 结果
    """
    with acquirer:
        url = "http://fanyi.baidu.com/v2transapi"
        resp = self.session.post(url=url, data={
            'from': 'en',
            'to': 'zh',
            'transtype': 'realtime',
            'query': src_data,
            'simple_means_flag': 3,
            'token': acquirer.token,
            "sign": acquirer.acquire(src_data)}, headers=self.headers,
                             timeout=self.translate_timeout, proxies=proxies)
        return src_template % tuple("".join(
            map(lambda x: x["src_str"],
                json.loads(resp.text)["trans_result"]['phonetic'])).split("\n"))


def qq(self, src_data, proxies, src_template, acquirer):
    """
    腾讯翻译的实现, 腾讯翻译最长只能翻译2000个字符
    :param src_data: 原生数据
    :param proxies: 代理
    :param src_template: 原生数据模板
    :param acquirer: cookie获取器
    :return: 结果
    """
    url = 'http://fanyi.qq.com/api/translate'
    with acquirer:
        acquirer.headers.update(self.headers)
        resp = self.session.post(
            url, data={'source': 'auto',
                       'target': 'en',
                       'sourceText': src_data,
                       'sessionUuid': 'translate_uuid%d' % (time.time()*1000)},
            headers=acquirer.headers, timeout=self.translate_timeout, proxies=proxies)
        return merge_conflict(
            src_template,
            [record["targetText"] for record in json.loads(
                resp.text)["translate"]["records"]
             if record.get("sourceText") != "\n"])


def google(self, src_data, proxies, src_template, acquirer):
    url = 'https://translate.google.cn/translate_a/single'
    with acquirer:
        data = {
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
            'tk': acquirer.acquire(src_data),
            'q': src_data,
        }
        resp = self.session.get(
            url, params=data, headers=self.headers,
            timeout=self.translate_timeout, proxies=proxies)
        return merge_conflict(
            src_template,
            [line[0] for line in json.loads(resp.text)[0] if line[0]])
