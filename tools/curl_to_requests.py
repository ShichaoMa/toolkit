import re
import json

from toolkit import re_search


def cur_to_requests(curl_cmd, filename):
    tmpl = """import requests


def main():
    url = "{}"
    headers = {}
    form = {}
    resp = requests.{}(url, headers=headers, data=form)
    print(resp.text)


main()
"""
    url = re.search(r"'(http.*?)'", curl_cmd).group(1)
    headers = dict(tuple(v.strip() for v in header.split(":", 1)) for header in re.findall(r"-H '(.*?)'", curl_cmd))
    form = re_search(r"--data '(.*?)'", curl_cmd)
    if form:
        data = dict(tuple(param.split("=", 1)) for param in form.replace("+", " ").split("&"))
    else:
        data = None
    with open(filename, "w") as f:
        f.write(tmpl.format(url, json.dumps(headers, indent=10), json.dumps(data, indent=10), "post" if data else "get"))


cur_to_requests("curl 'http://fanyi.baidu.com/v2transapi' -H 'Pragma: no-cache' -H 'Origin: http://fanyi.baidu.com' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: locale=zh; BAIDUID=C4165D8852A9C27A66016416B27DB24F:FG=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1517035809; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1517035810' -H 'Connection: keep-alive' -H 'Referer: http://fanyi.baidu.com/?aldtype=16047' --data 'from=en&to=zh&query=what+a+fuck+day+it+is!&simple_means_flag=3&sign=58161.262144&token=4fb8af2446a026608f95bd3a27b4b67d' --compressed", "test2.py")