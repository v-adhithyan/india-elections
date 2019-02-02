import json
import tempfile
from pathlib import Path

import mock
import pytest
from dateutil.parser import parse as dateparser
from itertools import product

from core.models import TweetStats, Wordcloud
from core.twitter.utils import (clean_tweet, convert_timedata_to_2d,
                                generate_view_dict, get_timeseries_tweet_data,
                                get_tweet_sentiment, put_word_cloud)


def test_get_tweet_sentiment():
    text = "I am good."
    assert get_tweet_sentiment(text) == "positive"

    text = "I am bad."
    assert get_tweet_sentiment(text) == "negative"

    text = "Hello."
    assert get_tweet_sentiment(text) == "neutral"


def test_clean_tweet():
    # Check whether the link is cleaned from text.
    text = "Here is the link https://www.google.co.in"
    assert clean_tweet(text) == "Here is the link"


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
    data = generate_view_dict()

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
    timeseries_data = get_timeseries_tweet_data()
    keys = timeseries_data.keys()
    assert "upa_time_series" in keys
    assert "nda_time_series" in keys


@pytest.mark.django_db
@pytest.mark.usefixtures("tweetstats")
def test_convert_timedata_to_2d(tweetstats):
    data = TweetStats.get_tweet_count_of_party_by_date(party='u')
    if not data:
        data = TweetStats.get_tweet_count_of_party_by_date(party='n')

    twod_data = json.loads(convert_timedata_to_2d(data))
    assert isinstance(twod_data, list)
    assert sorted(['x', 'y']) == sorted(twod_data[0].keys())

    data = twod_data[0]
    date = data['x']
    count = data['y']
    try:
        dateparser(date)
        assert True
    except ValueError:
        raise
    assert isinstance(count, int)


@pytest.mark.django_db()
def test_old_wordcloud_files_removal():
    q = "test"
    file_1 = tempfile.NamedTemporaryFile("w", delete=False)
    Wordcloud.objects.create(q=q, file_path=file_1.name)

    file_2 = tempfile.NamedTemporaryFile("w", delete=False)
    put_word_cloud(q=q, file_path=file_2.name)

    assert not Path(file_1.name).exists()

    # delete new file to save space
    Path(file_2.name).unlink()
