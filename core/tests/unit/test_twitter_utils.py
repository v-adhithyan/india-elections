import json
import tempfile
from itertools import product
from pathlib import Path

import mock
import pytest
from dateutil.parser import parse as dateparser

from core.models import TweetStats, Wordcloud
from core.twitter import utils


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
    data = utils.generate_view_data("upa", "nda")

    assert isinstance(data, dict)

    data_keys = data.keys()
    parties = ["upa", "nda"]
    keys = ["positive", "negative", "neutral", "male", "female", "tags", "post_count"]
    for p in product(parties, keys):
        expected_key = "_".join(p)
        assert expected_key in data_keys


@pytest.mark.django_db
@pytest.mark.usefixtures("tweetstats")
def test_get_timeseries_data(tweetstats):
    timeseries_data = utils.get_timeseries_data("upa", "nda")
    keys = timeseries_data.keys()
    assert "upa_time_series" in keys
    assert "nda_time_series" in keys


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
    data = utils.convert_sentiment_to_percentage(sentiment_data)
    keys = sentiment_data.keys()
    for k in keys:
        assert isinstance(data[k], float)
