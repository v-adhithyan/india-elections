import requests

params = [
    'modi',
    'rahulgandhi'
]
url = "https://indiaelections.pythonanywhere.com/job/?q={}"

for q in params:
    response = requests.get(url.format(q))
    print(response)
