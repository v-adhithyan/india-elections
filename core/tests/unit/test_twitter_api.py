import mock
import pytest

from core.twitter.twitter_api import TwitterApi


@pytest.mark.usefixtures('tweets')
def test_get_and_save_tweets(tweets):
    with mock.patch(
        'core.twitter.twitter_api.TwitterApi.get_and_save_tweets'
    ) as get_and_save_tweets:
        get_and_save_tweets.return_value = len(tweets)
        api = TwitterApi()
        assert api.get_and_save_tweets(query="indiaelections") == len(tweets)


@pytest.mark.usefixtures('tweets')
def test_frame_tweets(tweets):
    api = TwitterApi()
    tweets = api.frame_tweets(tweets, "test")

    assert len(tweets) > 0
    keys = tweets[0].keys()
    assert 'q' in keys
    assert 'tweet' in keys
    assert 'cleaned_tweet' in keys
    assert 'tweet_sentiment' in keys
    assert 'user_name' in keys
