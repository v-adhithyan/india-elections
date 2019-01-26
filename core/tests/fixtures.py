import json
import pathlib

import pytest
from collections import namedtuple


Tweet = namedtuple('Tweet', 'q text user')
User = namedtuple('User', 'screen_name')


@pytest.fixture
@pytest.mark.django_db
def tweets():
    tweet_file = pathlib.Path(__file__).resolve().parent / 'tweets.json'
    with open(tweet_file, 'r') as f:
        tweets_json = json.loads(f.read())

    tweets = []
    for t in tweets_json:
        tweets.append(Tweet(q=t['q'], text=t['tweet'], user=User(screen_name='test')))

    return tweets
