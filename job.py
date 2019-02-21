#!/usr/local/bin/python3
import os
from collections import OrderedDict
from urllib.parse import urljoin
import time
import argparse

import requests


def run(queries):
    host = "https://www.indiaelections.xyz"

    token_url = urljoin(host, 'api/token/')
    job_url = urljoin(host, 'job/')

    print(token_url)
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

    print(response)
    print(response.content)

    if access_token:
        headers = {'Authorization': "Bearer {}".format(access_token)}
        for q in queries:
            params = OrderedDict()
            params['q'] = q
            response = requests.get(job_url, params=params, headers=headers)
            print("q: {}".format(q))
            print("status: {}".format(response.status_code))
            print("response content: {}".format(response.content))
    else:
        print("Unable to get access_token")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queries",
        dest='queries',
        help="comma seperated list of words to fetch and save tweets",
        required=True)
    parser.add_argument(
        "--interval",
        dest='interval',
        help="time interval in minutes to fetch the queries repeatedly",
        type=int,
        required=True)
    parser.add_argument(
        "--quit",
        dest='quit',
        help="hours after which the script should quit.",
        type=int,
        required=True)
    args = parser.parse_args()

    quit = args.quit * 60 * 60
    time_taken = 0
    sleep_time = 60*args.interval
    while True:
        queries = args.queries.split(",")
        run(queries)
        print("sleeping")
        time.sleep(sleep_time)
        time_taken += sleep_time
        if time_taken == quit:
            break
