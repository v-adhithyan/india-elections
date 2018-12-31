import mock

from core.twitter.twitter_api import TwitterApi


def test_get_and_save_tweets(tweets):
    with mock.patch(
        'core.twitter.twitter_api.TwitterApi.get_and_save_tweets'
    ) as get_and_save_tweets:
        get_and_save_tweets.return_value = len(tweets)
        api = TwitterApi()
        assert api.get_and_save_tweets(query="indiaelections") == len(tweets)
