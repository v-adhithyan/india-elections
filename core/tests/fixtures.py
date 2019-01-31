import json
import pathlib
from collections import namedtuple

import pytest

from core.models import TweetStats
from core.twitter.twitter_api import TwitterApi
from core.twitter.utils import _generate_word_cloud_1

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


@pytest.fixture
@pytest.mark.django_db
def tweetstats(tweets):
    q = 'test'
    api = TwitterApi()
    framed_tweets = api.frame_tweets(tweets, q)
    _generate_word_cloud_1(q, framed_tweets)

    return TweetStats.objects.filter(q=q)
