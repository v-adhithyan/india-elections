from core.twitter.utils import get_tweet_sentiment, clean_tweet


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
