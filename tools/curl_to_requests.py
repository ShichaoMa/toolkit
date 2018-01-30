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
        f.write(tmpl.format(url, json.dumps(headers, indent=10), json.dumps(data, indent=10) if data else None, "post" if data else "get"))


cur_to_requests("curl 'https://www.ralphlauren.com/men-clothing-pants/sullivan-slim-cotton-pant/411909.html?cgid=men-clothing-pants&dwvar411909_colorname=Polo%20Black%2FTrade%20Blanket&webcat=direct' -H 'pragma: no-cache' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: www.ralphlauren.com' -H 'cookie: __cfduid=da006c81842bf7629916f135cce3e47371517304590; dwac_102c95db27e6f188d36d6303ba=plgz9erKvQ4WCtISsAt0LdFj1NgvIi0d3AU%3D|dw-only|||USD|false|US%2FEastern|true; cqcid=bcVRzEu9a9mYHKXXCSnFDhe99M; dwanonymous_55b6a3b329e729876c1d594e39f4ac4e=bcVRzEu9a9mYHKXXCSnFDhe99M; sid=plgz9erKvQ4WCtISsAt0LdFj1NgvIi0d3AU; dwsecuretoken_55b6a3b329e729876c1d594e39f4ac4e=KVVUOUiIRwPlI2msrkEPWGZmRedFzecrjA==; dwsid=rVPhH3Mr9WfIpJHo3D5DjtpoBjK2w2V0Aqvapa0dRlC7rMJ7B2tjhZGHtKm8mJASrVwObDuWp0_93BkBgBg9PA==; AMCVS_F18502BE5329FB670A490D4C%40AdobeOrg=1; mt.v=2.401312208.1517304764049; _ga=GA1.2.1171683572.1517304836; _gid=GA1.2.1087004090.1517304836; AMCV_F18502BE5329FB670A490D4C%40AdobeOrg=-1891778711%7CMCIDTS%7C17562%7CMCMID%7C26071746178851258062237771533638628948%7CMCAAMLH-1517909563%7C11%7CMCAAMB-1517909563%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1517311963s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17569%7CvVersion%7C2.4.0; stc111452=tsa:1517304836761.597364502.0387273.99016428752839.166:20180130100528|env:1%7C20180302093356%7C20180130100528%7C3%7C1012242:20190130093528|uid:1517304836761.1240346754.9168978.111452.1343997165:20190130093528|srchist:1012242%3A1%3A20180302093356:20190130093528' --compressed", "test.py")