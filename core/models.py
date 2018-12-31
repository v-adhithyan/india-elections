from datetime import datetime

from django.db import models

from core.constants import SENTIMENTS


class Tweet(models.Model):
    q = models.CharField(max_length=50)
    tweet = models.TextField()
    cleaned_text = models.TextField()
    sentiment = models.CharField(choices=SENTIMENTS, max_length=1)
    added_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def save_to_db(cls, tweet_dict):
        tweet = Tweet()
        tweet.tweet = tweet_dict['dict']
        tweet.cleaned_text = tweet_dict['cleaned_tweet']
        tweet.sentiment = tweet_dict['tweet_sentiment']
        tweet.save()

    @classmethod
    def bulk_save(cls, tweet_dicts):
        for tweet_dict in tweet_dicts:
            Tweet(
                q=tweet_dict['q'],
                tweet=tweet_dict['tweet'],
                cleaned_text=tweet_dict['cleaned_tweet'],
                sentiment=tweet_dict['tweet_sentiment'],
                added_time=datetime.now()).save()

    def __str__(self):
        return "{} :: {}".format(self.sentiment, self.tweet)

    def __unicode__(self):
        return "{} :: {}".format(self.sentiment, self.tweet)
