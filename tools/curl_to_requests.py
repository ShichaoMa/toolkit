import re
import json
from toolkit import re_search


def cur_to_requests(curl_cmd, filename):
    tmpl = """import requests


def main():
    url = "{}"
    headers = {}
    form = {}
    json = {}
    resp = requests.{}(url, headers=headers, json=json, data=form)
    print(resp.text)


main()
"""
    url = re.search(r"'(http.*?)'", curl_cmd).group(1)
    headers = json.dumps(
        dict(tuple(v.strip() for v in header.split(":", 1)) for header in re.findall(r"-H '(.*?)'", curl_cmd)), indent=10)
    form = re_search(r"--data '(.*?)'", curl_cmd, default=None)

    json_data = re_search(r"--data-binary '(.*?)'", curl_cmd, default=None)
    if form:
        form = json.dumps(dict(tuple(param.split("=", 1)) for param in form.replace("+", " ").split("&")), indent=10)
    if json_data:
        json_data = json.dumps(json.loads(json_data), indent=10)

    with open(filename, "w") as f:
        f.write(tmpl.format(
            url,
            headers,
            form,
            json_data,
            "post" if form or json_data else "get"))


cur_to_requests(
    """curl 'https://www.ssense.com/en-ca/men' -H 'pragma: no-cache' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: www.ssense.com' -H 'cookie: visitorId=30b6cf149dff5c4e9842dd625564a04d55054a16308b978492929b37a8aba10c; forcedCountry=ca; visid_incap_1637567=5W5N3zwSTtKvNLpM0/VuhqGPp1oAAAAAQUIPAAAAAAAI3+oJCChBGwChrDMlOVq1; lang=en_CA; shopping_bag=9144B81BB3844BDE93F64F1102B85F30; _ga=GA1.2.1067427706.1520930829; _gid=GA1.2.967977577.1520930829; __zlcmid=lPhBgPN4OuJVkp; exp_helloWorld=B-cbIuunSUu_Pxz6SzGfoA.helloWorld.0.control; sync_exp_helloWorld=B-cbIuunSUu_Pxz6SzGfoA.helloWorld.0.control; incap_ses_426_1637567=54IgImaS1i9pXLuZOXXpBdLKqVoAAAAAJGFJxjO2jLbwRV4wMW9KuQ==; nlbi_1637567=wANhSqy4v2aWsFEEjefZEAAAAABoqOo9dOpo8Pq0HfPyle7u; incap_ses_982_1637567=bTeIQgftTyW0eKSj+sOgDT/cqVoAAAAAfCRH7yuMXGQFo4XvSkUNCQ==; NavigationSessions:token=fa2ff03aa3ff70e7e08bd65c1ac187e7; country=ca; _uetsid=_uetc7e6fdc1' --compressed""",
    "test.py")