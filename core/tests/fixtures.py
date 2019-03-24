import json
import pathlib
import random
from collections import namedtuple

import mock
import pytest

from core.constants import YESTERDAY
from core.models import TweetStats
from core.twitter.bot.templates import TweetTemplate
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


@pytest.fixture
def positive():
    return random.randint(50, 100)


@pytest.fixture
def negative():
    return random.randint(50, 100)


@pytest.fixture
def neutral():
    return random.randint(50, 100)


@pytest.fixture
def sentiment_data(positive, negative, neutral):
    data = {
        "upa_positive": positive,
        "upa_negative": negative,
        "upa_neutral": neutral,
        "nda_positive": positive,
        "nda_negative": negative,
        "nda_neutral": neutral
    }
    return data


@pytest.fixture
def twitter_trends():
    return ['#KKRvSRH',
            '#RememberMeWhenYouVote',
            'David Warner',
            '#CashTheGame',
            'Sapna',
            '#KKRHaiTaiyaar',
            'Dinesh Karthik',
            'Prasidh Krishna',
            'Bairstow',
            'Shaan New Track',
            'Piyush Chawla',
            'Bhuvneshwar Kumar',
            '21 MP',
            'Match 2',
            'Eden Gardens',
            'Kolkata Knight Riders',
            'Travel Cash Fest',
            'Pakistin',
            'Andre Russell',
            'Williamson',
            'Ram Madhav',
            'Mulayam Singh Yadav',
            '#ProtinexWithPrithvi',
            '#OrangeArmy',
            '#kejriwalhateshindu',
            '#RadhaRavi',
            '#SRHvsKKR',
            '#21ru21Sankha',
            '#SundayMotivation',
            '#TuMeraRabHai',
            '#SundayThoughts',
            '#WorldTBDay',
            '#TeamModi',
            '#CricbuzzLIVE',
            '#MIvDC',
            '#PatiPatniAurWoh',
            '#Warner',
            '#MainBhiChowkidarAtCP',
            '#ChowkidarDebate',
            '#KorboLorboJeetbo',
            '#ChowkidarSeMahilaKoBachao',
            '#GreenplyPlywood',
            '#EndTB',
            '#Taanaji',
            '#StopForcedConversions',
            '#RiseWithUs',
            '#StopDestroyingStartUps',
            '#WorldTuberculosisDay']


@pytest.fixture
def tweet_template():
    return TweetTemplate(
        party1="admk",
        party1_count=20,
        party2="dmk",
        party2_count=20,
        place="Tamilnadu",
        timerange=YESTERDAY)


@pytest.fixture
@mock.patch('core.image.helpers.generate_tweet_image')
@mock.patch('core.twitter.bot.TweetTemplate')
@mock.patch('core.twitter.utils.generate_view_data')
@mock.patch('tweepy.API.update_with_media')
def mock_tweet_prediction(twitter_api, generate_view_data, mock_tweet_template, generate_tweet_image, tweet_template):
    twitter_api.return_value = []
    generate_view_data.return_value = dict()
    mock_tweet_template.return_value = tweet_template
    generate_tweet_image.return_value = None
