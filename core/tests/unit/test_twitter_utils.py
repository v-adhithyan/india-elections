import json
import tempfile
from pathlib import Path

import mock
import pytest
from dateutil.parser import parse as dateparser

from core.models import TweetStats, Wordcloud
from core.twitter import utils
from core.twitter.utils import TIMESERIES, SENTIMENT_TIMESERIES


def test_get_tweet_sentiment():
    text = "I am good."
    assert utils.get_tweet_sentiment(text) == "positive"

    text = "I am bad."
    assert utils.get_tweet_sentiment(text) == "negative"

    text = "Hello."
    assert utils.get_tweet_sentiment(text) == "neutral"


def test_clean_tweet():
    # Check whether the link is cleaned from text.
    text = "Here is the link https://www.google.co.in"
    assert utils.clean_tweet(text) == "Here is the link"


@pytest.mark.usefixtures("tweets")
@pytest.mark.django_db
def test_get_wordcloud(tweets):
    with mock.patch('core.twitter.utils._generate_word_cloud_1') as generate_word_cloud:
        q = "test"
        with tempfile.NamedTemporaryFile() as f:
            mocked_filename = f.name + ".png"
            generate_word_cloud.return_value = mocked_filename
            with mock.patch('core.twitter.utils.get_word_cloud') as get_word_cloud:
                get_word_cloud.return_value = mocked_filename
                wordcloud = get_word_cloud(q=q)

            assert wordcloud == mocked_filename


@pytest.mark.django_db
def test_generate_view_dict():
    data = utils.generate_view_data(party_1="upa", party_2="nda", remove=True)

    assert isinstance(data, dict)

    data_keys = data.keys()
    keys = [
        "positive",
        "negative",
        "neutral",
        "male",
        "female",
        "tags",
        "post_count",
        "time_series",
        "sentiment_time_series",
        "color",
        "seats"
    ]
    for key in data_keys:
        key = key.split("_")[1:]
        key = "_".join(key)
        if key:
            assert key in keys


@pytest.mark.django_db
@pytest.mark.usefixtures("tweetstats")
def test_get_timeseries_data(tweetstats):
    timeseries_data = utils.get_timeseries_data(TIMESERIES, "upa", "nda")
    keys = timeseries_data.keys()
    assert "upa_time_series" in keys
    assert "nda_time_series" in keys

    sentiment_timeseries = utils.get_timeseries_data(SENTIMENT_TIMESERIES, "upa", "nda")
    keys = sentiment_timeseries.keys()
    assert "upa_sentiment_time_series" in keys
    assert "nda_sentiment_time_series" in keys


@pytest.mark.django_db
@pytest.mark.usefixtures("tweetstats")
def test_convert_timedata_to_2d(tweetstats):
    data = TweetStats.get_tweet_count_of_party_by_date(party='u')
    if not data:
        data = TweetStats.get_tweet_count_of_party_by_date(party='n')

    twod_data = json.loads(utils.convert_timedata_to_2d(data))
    assert isinstance(twod_data, list)
    assert sorted(['x', 'y']) == sorted(twod_data[0].keys())

    data = twod_data[0]
    date = data['x']
    count = data['y']
    try:
        dateparser(date)
        assert True
    except ValueError:
        pass
    assert isinstance(count, int)


@pytest.mark.django_db()
def test_old_wordcloud_files_removal():
    q = "test"
    file_1 = tempfile.NamedTemporaryFile("w", delete=False)
    Wordcloud.objects.create(q=q, file_path=file_1.name)

    file_2 = tempfile.NamedTemporaryFile("w", delete=False)
    utils.put_word_cloud(q=q, file_path=file_2.name)

    assert not Path(file_1.name).exists()

    # delete new file to save space
    Path(file_2.name).unlink()


@pytest.mark.usefixtures("positive", "negative", "neutral")
def test_calculate_percentage(positive, negative, neutral):
    pos = positive
    neg = negative
    neu = neutral
    total = pos + neg + neu
    positive_percentage, negative_percentage, neutral_percentage = utils.calculate_percentage(pos, neg, neu)
    assert positive_percentage == float(pos/total)*100
    assert negative_percentage == float(neg/total)*100
    assert neutral_percentage == float(neu/total)*100


@pytest.mark.usefixtures('sentiment_data')
def test_convert_sentiment_to_percentage(sentiment_data):
    keys = sentiment_data.keys()
    parties = list({key.split("_")[0] for key in keys})
    data = utils.sentiment_to_percentage(sentiment_data, party_1=parties[0], party_2=parties[1])

    for k in keys:
        assert isinstance(data[k], float)
