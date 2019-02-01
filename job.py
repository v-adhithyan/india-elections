import os
from collections import OrderedDict
from urllib.parse import urljoin

import requests

QUERIES = [
    'modi',
    'rahulgandhi'
]

dev = os.environ.get('IE_DEBUG', False)
host = "http://localhost:8000" if dev else "https://indiaelections.pythonanywhere.com"

token_url = urljoin(host, 'api/token/')
job_url = urljoin(host, 'job/')

username = os.environ['IE_USERNAME']
password = os.environ['IE_PASSWORD']
data = {
    'username': username,
    'password': password
}
response = requests.post(token_url, data=data)
access_token = ""
if response.status_code == 200:
    access_token = response.json()['access']
    print(access_token)


if access_token:
    headers = {'Authorization': "Bearer {}".format(access_token)}
    for q in QUERIES:
        params = OrderedDict()
        params['q'] = q
        response = requests.get(job_url, params=params, headers=headers)
        print("q: {}".format(q))
        print("status: {}".format(response.status_code))
        print("response content: {}".format(response.content))
else:
    print("Unable to get access_token")
