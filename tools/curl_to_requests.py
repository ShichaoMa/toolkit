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
    """curl 'https://shop.diesel.com/on/demandware.store/Sites-DieselUS-Site/default/OnRequest-ShipToRedirect?IsShipTo=true&locale=en_CA&origin=NOUS' -H 'pragma: no-cache' -H 'cookie: __cfduid=d1a529ada34d015141cc52db40046d1671520643871; check=true; gvsC=New; adms_channel=Typed/Bookmarked; fb_test=B; AMCVS_982E985B591252110A495C70%40AdobeOrg=1; _ga=GA1.2.2064890246.1520643874; _gid=GA1.2.683740139.1520643874; s_cc=true; __cq_uuid=0267f480-23ff-11e8-bedc-5fc866bd8e58; __cq_seg=; s_dfa=diesel.prod; aa_dslv_s=Less%20than%201%20day; AMCV_982E985B591252110A495C70%40AdobeOrg=1406116232%7CMCIDTS%7C17601%7CMCMID%7C63592494528222457541512736415179606139%7CMCAAMLH-1521273014%7C11%7CMCAAMB-1521273014%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1520675414s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17608%7CvVersion%7C2.5.0; sid=DMRP9DXnHFRde9W8iDOB0SNmxG_tHZ8eIcE; dwanonymous_06fd9c6d4fc17274b498b31014b05f19=bdxxbj2LPNEVaBcQjr9YvJdp9j; dwsid=MJvC8VdwVmIV0ceCkspclh85SWqPitUoaWuYXWswL9-lIs-L1Q16Rx77oqxWXc1a6JuyoQnSHyQ6Wl7eRZrHIg==; _uetsid=_uetab0cafd0; dwac_cgjKkiaagRliAaaaebGcbjdViA=DMRP9DXnHFRde9W8iDOB0SNmxG_tHZ8eIcE%3D|dw-only|||USD|false|US%2FEastern|true; cqcid=bdxxbj2LPNEVaBcQjr9YvJdp9j; dwsecuretoken_06fd9c6d4fc17274b498b31014b05f19=ww0KkZiDZ4CY0bEC63sdGq54DZ5iLvqbog==; _ga=GA1.3.2064890246.1520643874; _gid=GA1.3.683740139.1520643874; aam_uuid=63785932000181125231457924750885550346; cto_lwid=bb27be6a-047e-4975-a88e-b39f1222252f; LPVID=A3Yzc1NzAxZGM4ZTU0MWQ1; LPSID-1843710=VQhpfphkRcC_kDR-WhEg3Q; pdpbacklabel=Jackets%20Man%20%7C%20Diesel%20Online%20Store%20USA; pdpbackurl=https://shop.diesel.com/mens/jackets/?lang=default&elementsLoaded=60; locale=default; dw=1; __atuvc=5%7C10; __atuvs=5aa38e5cffa5bec1004; utag_main=v_id:01620d701d9f0007035a5a6a067204079002e07100bd0$_sn:2$_ss:0$_st:1520670472344$vapi_domain:diesel.com$ses_id:1520668210901%3Bexp-session$_pn:8%3Bexp-session; aa_dslv=1520668673080; aa_newrep=1520668673083-Repeat; aa_prev_page=us%3Aman%3Adenimandclothing%3Ajackets; mbox=session#9e2530a5bda345f1ad449968a9ca0a0a#1520670534|PC#9e2530a5bda345f1ad449968a9ca0a0a.24_11#1583913380; s_ppv=5; aa_cvpmc_n=%5B%5B%27Typed%2FBookmarked%27%2C%271520643877632%27%5D%2C%5B%27Referring%2520Domains%27%2C%271520668651937%27%5D%2C%5B%27Typed%2FBookmarked%27%2C%271520668667494%27%5D%2C%5B%27Referring%2520Domains%27%2C%271520668763167%27%5D%5D; s_sq=diesel.prod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dus%25253Aman%25253Adenimandclothing%25253Ajackets%2526link%253DCanada%252520%252528English%252529%2526region%253Dwrapper-ship%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dus%25253Aman%25253Adenimandclothing%25253Ajackets%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fshop.diesel.com%25252Fon%25252Fdemandware.store%25252FSites-DieselUS-Site%25252Fdefault%25252FOnRequest-ShipToRedirect%25253FIsS%2526ot%253DA' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'cache-control: no-cache' -H 'authority: shop.diesel.com' -H 'referer: https://shop.diesel.com/mens/jackets/?lang=default&elementsLoaded=60' --compressed""",
    "test.py")