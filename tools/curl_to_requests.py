import re
import json
from toolkit import re_search


def repl(mth):
   return mth.group().encode('utf-8').decode('unicode_escape')


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
        dict(tuple(v.strip() for v in header.split(":", 1)) for header in re.findall(r"-H '(.*?)'", curl_cmd)), indent=4)
    form = re_search(r"--data ?'(.*?)'", curl_cmd, default=None)

    json_data = re_search(r"--data-binary \$'(.*?)'", curl_cmd, default=None)
    if form:
        form = json.dumps(dict(tuple(param.split("=", 1)) for param in form.replace("+", " ").split("&")), indent=4)
    if json_data:
        json_data = re.sub(r"\\u\w{4}", repl, json.dumps(json.loads(json_data), indent=4).replace("false", "False").replace("true", "True").replace("null", "None"))

    with open(filename, "w") as f:
        f.write(tmpl.format(
            url,
            headers,
            form,
            json_data,
            "post" if form or json_data else "get"))

import sys
cur_to_requests(sys.argv[1], sys.argv[2])