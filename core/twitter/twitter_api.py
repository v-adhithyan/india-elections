from collections import OrderedDict

import tweepy

from core.constants import (TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET,
                            TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
from core.twitter.utils import (clean_tweet, get_candidate_and_party_dict,
                                get_tweet_sentiment, generate_word_cloud_1)


class TwitterApi(object):

    def __init__(self):
        auth = tweepy.OAuthHandler(TW_CONSUMER_KEY, TW_CONSUMER_SECRET)
        auth.set_access_token(TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def frame_tweets(self, fetched_tweets, query):
        tweets = []
        candidate_party_dict = get_candidate_and_party_dict()

        for tweet in fetched_tweets:
            parsed_tweet = OrderedDict()
            cleaned_tweet = clean_tweet(tweet.text)

            parsed_tweet['q'] = query
            parsed_tweet['tweet'] = tweet.text
            parsed_tweet['cleaned_tweet'] = cleaned_tweet
            parsed_tweet['tweet_sentiment'] = get_tweet_sentiment(cleaned_tweet)
            parsed_tweet['user_name'] = tweet.user.screen_name
            try:
                parsed_tweet['party'] = candidate_party_dict[query][0]
            except KeyError:
                raise

            if not hasattr(tweet, 'retweeted_status'):
                tweets.append(parsed_tweet)

        return tweets

    def get_and_save_tweets(self, query, max_count=200) -> int:
        fetched_tweets = self.api.search(q=query, count=max_count)
        tweets = self.frame_tweets(fetched_tweets, query)
        generate_word_cloud_1(query, tweets)
        return len(tweets)
