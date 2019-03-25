#!/usr/local/bin/python3
import argparse
import logging
import os
import sys
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
import functools
import time

load_dotenv()
prefix = "job/"
host = urljoin(os.environ["PC_HOST"], prefix)
SAVE_TWEETS = "save-tweets"
TWEET_PREDICTION = "tweet-prediction"
jobs = {
    SAVE_TWEETS: host + "save-tweets/",
    TWEET_PREDICTION: host + "tweet-prediction/"
}
INTERVAL = 10
HOURS = 9
ONETIMEJOB = False
MINUTES_IN_HOUR = 60
SECONDS = 60
logging.basicConfig(level=logging.INFO)


def run(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if ONETIMEJOB:
            func(*args, **kwargs)
        else:
            total_execution_time = int((MINUTES_IN_HOUR / INTERVAL) * HOURS)
            current_elapsed_time = 0
            while current_elapsed_time < total_execution_time:
                func(*args, **kwargs)
                time.sleep(INTERVAL * SECONDS)
                current_elapsed_time += 1
                logging.info("Total execution time: {}, Current elapsed time: {}".format(
                    total_execution_time, current_elapsed_time))
    return wrapper


@run
def make_get_request(job, params):
    url = jobs.get(job)
    if not params:
        response = requests.get(url=url)
    else:
        response = requests.get(url=url, params=params)

    if response.ok:
        logging.info("{} success.".format(job))
    else:
        logging.warning("{} failed.".format(job))


def save_tweets(queries):
    if not queries:
        logging.error("No queries supplied. Exiting..")
        sys.exit(0)

    params = {
        'q': queries
    }
    make_get_request(SAVE_TWEETS, params=params)


def tweet_prediction():
    make_get_request(TWEET_PREDICTION, params={})


def main():
    global INTERVAL, HOURS, ONETIMEJOB

    parser = argparse.ArgumentParser(description="Run Jobs ...")
    parser.add_argument("--savetweets", action='store_true', help="Extract, Transform and Save tweets.")
    parser.add_argument("--tweetprediction", action="store_true", help="Tweet prediction stats.")
    parser.add_argument('--queries', type=str, help='Comma seperated search terms for which ETL should be performed.',
                        default="bjp, incindia, modi, rahulgandhi", required=False)
    parser.add_argument("--interval", type=int,
                        help="Time interval to sleep between each request in minutes", default=INTERVAL, required=False)
    parser.add_argument("-runfor", type=int,
                        help="Time in hours for which the script should run before quitting.",
                        default=HOURS, required=False)
    parser.add_argument("--onetimejob", type=bool, help="Enable this flag to run this job only once",
                        default=ONETIMEJOB, required=False)
    args = parser.parse_args()
    if not (args.savetweets or args.tweetprediction):
        parser.print_help()
    else:
        INTERVAL = args.interval
        HOURS = args.runfor
        ONETIMEJOB = args.onetimejob

        if ONETIMEJOB:
            logging.info("Job is onetime job.")
        else:
            logging.info("Job will run in intervals of {} minutes for {} hour(s).".format(INTERVAL, HOURS))

        if args.savetweets:
            save_tweets(queries=args.queries)
        elif args.tweetprediction:
            tweet_prediction()


if __name__ == "__main__":
    main()
