def post():

    import requests

    resp = requests.post("http://127.0.0.1:8000/a/1", json={
        "title": "aaaa", "tags": ["python"],
        "description": "111"})

    print(resp.json())

post()
