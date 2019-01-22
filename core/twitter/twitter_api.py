from collections import OrderedDict

import tweepy
from guess_indian_gender import IndianGenderPredictor

from core.constants import (
    TW_ACCESS_TOKEN,
    TW_ACCESS_TOKEN_SECRET,
    TW_CONSUMER_KEY,
    TW_CONSUMER_SECRET,
)
from core.twitter.utils import clean_tweet, get_tweet_sentiment, generate_word_cloud_1

predictor = IndianGenderPredictor()

class TwitterApi(object):

    def __init__(self):
        auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def get_and_save_tweets(self, query, max_count=200) -> int:
        fetched_tweets = self.api.search(q=query, count=max_count)
        tweets = []

        for tweet in fetched_tweets:
            parsed_tweet = OrderedDict()
            cleaned_tweet = clean_tweet(tweet.text)

            parsed_tweet['q'] = query
            parsed_tweet['tweet'] = tweet.text
            parsed_tweet['cleaned_tweet'] = cleaned_tweet
            parsed_tweet['tweet_sentiment'] = get_tweet_sentiment(cleaned_tweet)
            parsed_tweet['user_name'] = tweet.user.screen_name

            if not hasattr(tweet, 'retweeted_status'):
                tweets.append(parsed_tweet)

        generate_word_cloud_1(query, tweets)

        return len(tweets)
