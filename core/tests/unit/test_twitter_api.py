import mock

from core.twitter.twitter_api import TwitterApi


@mock.patch('core.constants.TW_CONSUMER_KEY', 'test')
@mock.patch('core.constants.TW_CONSUMER_SECRET', 'test')
@mock.patch('core.constants.TW_ACCESS_TOKEN', 'test')
@mock.patch('core.constants.TW_ACCESS_TOKEN_SECRET', 'test')
def test_get_and_save_tweets(tweets):
    with mock.patch(
        'core.twitter.twitter_api.TwitterApi.get_and_save_tweets'
    ) as get_and_save_tweets:
        get_and_save_tweets.return_value = len(tweets)
        api = TwitterApi()
        assert api.get_and_save_tweets(query="indiaelections") == len(tweets)
