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
    form = re_search(r"--data '(.*?)'", curl_cmd)
    json_data = re_search(r"--data-binary '(.*?)'", curl_cmd, None)
    if form:
        data = json.dumps(dict(tuple(param.split("=", 1)) for param in form.replace("+", " ").split("&")), indent=10)
    else:
        data = None
    if json_data:
        json_data = json.dumps(json.loads(json_data), indent=10)
    with open(filename, "w") as f:
        f.write(tmpl.format(
            url,
            headers,
            data,
            json_data,
            "post" if data or json_data else "get"))


cur_to_requests(
    """curl 'https://www.bluefly.com/api/commerce/catalog/storefront/products/445603101/configure?includeOptionDetails=true&quantity=1' -H 'x-vol-master-catalog: 1' -H 'Origin: https://www.bluefly.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'x-vol-app-claims: K0Fb51pK4PRPjSvd71NmAxApUcfJTo3Zc0DksIJ/r5XfmFLECSp5lYkNL6s+ucpJFG37VKMz6dwphqJfmuyVk8hMM3SUEI19IARlIDeloynkdFjCQOp/NFN37zOwXxyd85Hbhb5TLfRusTpDYvUfg7dnHvpa+PvqJjfB1U2gEDidDdX+RVE6cT/XSonv+4YnENVyUGfIxUCJgFb2JNG3lTGKmkTQVpB721kE+EDxlBo5HdQRkmMCbsUxtk5p+/wIY5iHKHNPEOAvwnXwzQiWvA==' -H 'x-vol-currency: USD' -H 'x-vol-locale: en-US' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: _mzvr=JVZWJqp2mkWKgicJTkyw7Q; sb-sf-at-prod-s=pt=&at=wlrsZeKprdHXhPGEW7VW8ASj/NKHbGChBtKDzESTUvVq5XBuxtqh3ic9OgC3RM7URec4+UUUrh6W/cc01hzjDgj1FhI/2v/O6W6+7PgM4lwGv60JmqpK/jz22LYqL0J5X/0iRQJgwBGfevGv/sQZbK/u4qpGvz2hLlOVskADrp9ZhCPWI27LwWFouW3YHZ+838+S4iOIeHHDyXQyq7N6NLh4lAmJeEwiFe1uzP1raEkUCoy5WUSEGzYj1zMvn2FD0iO2inqGagC5iK51DfymJGQC/7I9mVQh3brGUc5t6rrMJyCYb0IZCrg3F92V7BER&dt=2018-01-31T03:10:50.9992158Z; sb-sf-at-prod=pt=&at=wlrsZeKprdHXhPGEW7VW8ASj/NKHbGChBtKDzESTUvVq5XBuxtqh3ic9OgC3RM7URec4+UUUrh6W/cc01hzjDgj1FhI/2v/O6W6+7PgM4lwGv60JmqpK/jz22LYqL0J5X/0iRQJgwBGfevGv/sQZbK/u4qpGvz2hLlOVskADrp9ZhCPWI27LwWFouW3YHZ+838+S4iOIeHHDyXQyq7N6NLh4lAmJeEwiFe1uzP1raEkUCoy5WUSEGzYj1zMvn2FD0iO2inqGagC5iK51DfymJGQC/7I9mVQh3brGUc5t6rrMJyCYb0IZCrg3F92V7BER; _ga=GA1.2.48673652.1517368254; _gid=GA1.2.856416581.1517368254; _mzvs=yn; MOZU_AFFILIATE_IDS=%5B%5D; INTLCOUNTRYCODE=CN; mozucartcount=%7B%2254a7acec48cb4fb6bf5ea6fb62a5c008%22%3A0%7D; cto_lwid=6df1067b-3e90-4186-8977-a4a76f2eccba; bounceClientVisit1447v=N4IgNgDiBcIBYBcEQM4FIDMBBNAmAYnvgO6kB0ARmAK4CmAZmAJ5kDGA9gLZEgA0IAJxghiASwDWosgCtRAOwCGcsOzkBzWnLZdMWABwAGPXpABfIA; __ibxl=1; 3060738.3440491=24197705-6005-4cb4-b273-1d8887fdcd83; tracker_device=24197705-6005-4cb4-b273-1d8887fdcd83; _mzvt=E0k_cJBqLESxyxoLnffjjQ; _gat_UA-1028946-1=1; viewedProducts=474042701,475422601,378660602,378660601,445603101; _gat=1' -H 'Connection: keep-alive' -H 'x-vol-tenant: 12106' -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'x-vol-site: 16829' -H 'Content-type: application/json' -H 'Accept: application/json' -H 'x-vol-user-claims: FqxqO45gXF9FCxLMRFO5HUYkf+MqIOn3vk7gznnLnHRqTjRQTFTsx6MeF7hiCCssgebRXQAxntqLefMQsu+DkB1pzFt4s1vu6ljoffDWtB26suugajU2texMPKsWqcGotIPcQi46IfRYngbd6rjXO8EGacgKnz48xwqW/gO4tvcQZC4DNBcPpSr9gkG2Cj+2w59qYAVKECD/F3Z3psFLtXkCua82MGw0RJ/HYY2ck9l3oS+MZuePlVA1rrMrUbY9laRFg1RzNzUmN/CDuqD0Vhi9CmVnkzvgrgdYGcfk6OmaPsfdxC9or+1Y10RpAil2G0Ll6lEod9eTP4LFjp46oGMfi7zv+dzKmKFbcMsAVx/A+wvbqCgMoMV3RVSX/gYo' -H 'Referer: https://www.bluefly.com/bailarinas-emma-oro-gold-shimmer-ballerina-flat/p/445603101' -H 'x-vol-catalog: 1' --data-binary '{"options":[{"attributeFQN":"tenant~shoes-size","value":43740}]}' --compressed""",
    "test.py")