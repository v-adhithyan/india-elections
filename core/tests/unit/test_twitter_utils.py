import tempfile

import mock
import pytest
from itertools import product

from core.twitter.utils import (get_tweet_sentiment,
                                clean_tweet,
                                generate_view_dict)


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
                get_word_cloud.return_value  = mocked_filename
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
