import mock
import pytest

from core.twitter.bot import tweet_prediction_for_tamilnadu, tweet_prediction_for_india
from core.twitter.bot.templates import TWEET_LENGTH


@mock.patch('core.twitter.twitter_api.TwitterApi.get_trends')
def test_tweet_template(mock_trends, tweet_template, twitter_trends):
    mock_trends.return_value = twitter_trends
    tweet = tweet_template.get_tweet()

    assert isinstance(tweet.hashtags, list)
    assert "poll" in tweet.link
    assert "win" in tweet.text
    for h in tweet.hashtags:
        assert len(tweet.link + h + " ") < TWEET_LENGTH


@pytest.mark.django_db
@mock.patch('core.image.helpers.generate_tweet_image')
@mock.patch('core.twitter.bot.TweetTemplate')
@mock.patch('core.twitter.utils.generate_view_data')
@mock.patch('tweepy.API.update_with_media')
@mock.patch('core.models.TweetStats.get_all_time_sentiment_difference')
def test_tweet_prediction(mock_all_time_sentiment, twitter_api, generate_view_data,
                          mock_tweet_template, generate_tweet_image, tweet_template):
    mock_all_time_sentiment.return_value = {"_wincount_performance": "No change."}
    twitter_api.return_value = []
    generate_view_data.return_value = dict()
    mock_tweet_template.return_value = tweet_template
    generate_tweet_image.return_value = None
    tweet_prediction_for_tamilnadu()
    tweet_prediction_for_india()
