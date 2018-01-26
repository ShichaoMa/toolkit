"""
function() {
    var n = 0, t, i, r;
    if (this.length === 0)
        return n;
    for (t = 0,
    r = this.length; t < r; t++)
        i = this.charCodeAt(t),
        n = (n << 5) - n + i | 0;
    return n
}
"""
import struct


def shift_left_for_js(num, count):
    rs = num << count
    if rs > 2147483647 or rs <= -2147483647:
        rs = struct.unpack("i", struct.pack("l", rs)[:4])[0]
    return rs


def hash_code(text):
    code = 0
    for i in text:
        i = ord(i)
        code = shift_left_for_js(code, 5) - code + i | 0
    return code


import requests

session = requests.Session()

headers = {
    #'origin': 'https://cn.bing.com',
    'accept-encoding': 'gzip, deflate, br',
    # 'cookie':
    #     'mtstkn=ylt9lqygf4d6xwjSxncfOcMX8VexOyMzprKU%2F8gaXe1zA1vPe%2FuLVXFOjulDsQ5t; '
    #     'MicrosoftApplicationsTelemetryDeviceId=1167bc09-a9a1-5df1-f0f8-e9a69d79c782; '
    #     'MicrosoftApplicationsTelemetryFirstLaunchTime=1516933299794; '
    #     'srcLang=-; '
    #     'destLang=en; '
    #     'smru_list=; '
    #     'dmru_list=en; '
    #     'destDia=en-US; '
    #     'sourceDia=en-US; '
    #     '_EDGE_S=F=1&SID=292F83786B416E1704D488FB6AF66FE4;'
    #     ' _EDGE_V=1; MUID=2AF83BF9F6EC6D223FBB307AF75B6C44; '
    #     'MUIDB=2AF83BF9F6EC6D223FBB307AF75B6C44; '
    #     'SRCHHPGUSR=WTS=63652530099; '
    #     'SRCHD=AF=NOFORM; '
    #     'SRCHUID=V=2&GUID=93C164FE09F84B84930B7A6AB73CB22C&dmnchg=1; '
    #     'SRCHUSR=DOB=20180126; '
    #     '_SS=SID=292F83786B416E1704D488FB6AF66FE4',
    #'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    #'content-type': 'application/json; charset=UTF-8',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    #'cache-control': 'no-cache',
    #'authority': 'cn.bing.com',
    #'referer': 'https://cn.bing.com/translator/?ref=TThis&IG=7A2F68129A754A71A90F7C015A199621&IID=SERP.5493&&text=&from=&to=en'
}
#
# session.get("https://cn.bing.com/translator/", headers=headers)
#
# resp = session.post("https://cn.bing.com/translator/api/Translate/TranslateArray?from=-&to=zh-CHS", headers=headers, json=[{"id": hash_code("my"), "text": "my"}])
#
# from toolkit import debugger
# debugger()
# print(resp.text)
# print(hash_code("name my"))
from translate import Translate

with Translate("bing") as t:
    t.set_logger()
    print(t.translate("my name is tom, i come from nanjing, I like eat shit, what about yours?"))