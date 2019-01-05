import tempfile

import mock
import pytest

from core.models import Wordcloud
from core.twitter.utils import get_tweet_sentiment, clean_tweet, get_word_cloud


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
    with mock.patch('core.twitter.utils._generate_word_cloud') as generate_word_cloud:
        q = "test"
        with tempfile.NamedTemporaryFile() as f:
            mocked_filename = f.name + ".png"
            generate_word_cloud.return_value = mocked_filename
            wordcloud = get_word_cloud(q=q)

            assert wordcloud == mocked_filename

            wordcloud_from_db = Wordcloud.objects.get(q=q)
            assert wordcloud_from_db
            assert wordcloud_from_db.file_path == mocked_filename
            assert wordcloud_from_db.q == q
