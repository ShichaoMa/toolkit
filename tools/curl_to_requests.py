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
    """curl 'https://www.bluefly.com/api/commerce/catalog/storefront/products/484094401/configure?includeOptionDetails=true&quantity=1' -H 'x-vol-master-catalog: 1' -H 'Origin: https://www.bluefly.com' -H 'Accept-Encoding: gzip, deflate, br' -H 'x-vol-app-claims: dT4DuhD38QDBERWJshp5PG15jYPOI+Xv7nolBWHm7jjNNztHGrbdSDIVlegPb/9DBXLKUvb62OhvqkeFondrNRt3pgFx6ToC/JbDKoPDE3jvPBZyHlaPU/35eaUpV/7BVPuITwFcGAucenoN5Kh6O7y4Hs7WUrZ5Rbm+D47ybBQkFHvDzPYwlkAfhZwJOZrpqS6/qduDoIqHIKIwjG9NxfhB/3VO82Qj9nCz8mn8EDIWadIntgqAuig4DOEOEwp4KsMBiKr4X1Q0cd4tWSC57g==' -H 'x-vol-currency: USD' -H 'x-vol-locale: en-US' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'Cookie: _mzvr=PKZEI77Ah0WOCJpFf8RzgQ; _mzvt=QeZxWaPEX0O-Krg7LwWvQA; _svsid=a0c62cde9ae043e8f65e77ca1c484ed8; cX_S=jef2qbldo50eyw5f; cX_P=jef2qblggyxlibpj; _sp_ses.0fdf=*; _ga=GA1.2.621378539.1520305652; _gid=GA1.2.718496842.1520305652; MOZU_AFFILIATE_IDS=%5B%5D; INTLCOUNTRYCODE=CA; cX_G=cx%3A18yp6g4sy0zb1x0m1d95t6xsh%3A23af7rqf29sfm; cto_lwid=e88c1a3c-f568-4244-a472-f86edee905c2; sb-sf-at-Prod-s=pt=&at=A1beQsym7TKnIntMVAckW2kzlutf0D4iIXv0VLZUELN2rW7IfxCvy9H/ZpsFMBafzcPlSm+FQuwid9roeuNQrYIHdSeGF3vRhCof8IuP/S2IH9CYFfUFNnKkF9E8aK4t67vdpuTDRjwLurSCDbW7e9Gar4S/bb97IDpm4kU1MylTdD56xBUyW/41ugYtJ+nLES9t6jlpmtaqZvcrvvE8QlTkilpwV2oFWhXAfZFH2gvpsAPsnYdcVRV57cuGebrZHBgvVoakYUxgYVR4IrNijXlfHmgyIV4HCVimJbTRW10V1Gvz110F42I7AEytU4mD&dt=2018-03-06T03:07:26.4495383Z; sb-sf-at-Prod=pt=&at=A1beQsym7TKnIntMVAckW2kzlutf0D4iIXv0VLZUELN2rW7IfxCvy9H/ZpsFMBafzcPlSm+FQuwid9roeuNQrYIHdSeGF3vRhCof8IuP/S2IH9CYFfUFNnKkF9E8aK4t67vdpuTDRjwLurSCDbW7e9Gar4S/bb97IDpm4kU1MylTdD56xBUyW/41ugYtJ+nLES9t6jlpmtaqZvcrvvE8QlTkilpwV2oFWhXAfZFH2gvpsAPsnYdcVRV57cuGebrZHBgvVoakYUxgYVR4IrNijXlfHmgyIV4HCVimJbTRW10V1Gvz110F42I7AEytU4mD; mozucartcount=%7B%2211f39b15f0d24263b8ab16c9a17bff1d%22%3A0%2C%22cbe3ab65593a4a81a9a80c646695d1b7%22%3A0%7D; _mzvs=yn; tracker_device=408677c1-de52-467f-be5c-c0f731f7ae99; viewedProducts=487868601,484094401; _sp_id.0fdf=5e409de1-f303-40ac-a468-d69ed3d34ff1.1520305652.1.1520307071.1520305652.ec375653-4764-401b-b466-f27f588f049d' -H 'Connection: keep-alive' -H 'x-vol-tenant: 12106' -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36' -H 'x-vol-site: 16829' -H 'Content-type: application/json' -H 'Accept: application/json' -H 'x-vol-user-claims: Iezaopzbqk2oFKXwHqwg2XuOm8QNjzvpmN66iow8XIJBtd5AioArgV3WKy48TKkFPs30fHnI+q1X4/kNTha9cY8rVvfqIwVNnOsc1aeYn9mZhX4JJejzLc9FgoDz4Sj7KWFRv1JTzLFZX1xe/nB0kHfAgkdWQgzP7qvnMkR59tYfr9K8XWT9M6lnbZ5CMzlOyUO1p/8miDbOd9Rv/HZ7VwumOYol60C6fplbzN0a/2NxR/14AJuzloPvGLksbVZXEu/zchxKgNI6ghghtxZpwMXBaLajjcOrjdyku+jgyjWKPw3W4twkTgExezvI2xhbuqVFFxNKqZpXvZpxjYlEdrsFrJA1Sd+yyaMHtUHPkVO502OtvMEnUYcsvHen3u6z' -H 'Referer: https://www.bluefly.com/adidas-adidas-mens-eqt-basketball-adv-originals-basketball-shoe/p/484094401' -H 'x-vol-catalog: 1' --data-binary '{"options":[{"attributeFQN":"tenant~mens-shoes-size","value":43987}]}' --compressed""",
    "test.py")