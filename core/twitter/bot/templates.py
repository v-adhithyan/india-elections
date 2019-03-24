from collections import namedtuple
from dataclasses import dataclass
from string import Template

from core.twitter.twitter_api import TwitterApi

tweettemplate = namedtuple("tweettemplate", "text link hashtags")

TWEET_LENGTH = 280

@dataclass
class TweetTemplate:
    party1: str
    party1_count: int
    party2: str
    party2_count: str
    place: str
    timerange: str

    def get_tweet(self):
        hashtags = filter(lambda hashtag: hashtag.startswith("#"), TwitterApi().get_trends())

        text = Template("""
            As per $timerange 's prediction, in the upcoming loksabha election 2019:\n
            - $party1 may win $party1_count seats and\n
            - $party2 may win $party2_count seats.\n
            Not satisfied with the prediction ???. Take part in the opinion poll and change $place fate.\n
            Opinion poll link in tweet. Voice your opinion now.""")\
            .substitute(party1=self.party1.upper(), party1_count=self.party1_count, party2=self.party2.upper(),
                        party2_count=self.party2_count, place=self.place, timerange=self.timerange)

        link = "https://www.indiaelections.xyz/poll/opinion-poll/ "

        current_tweet_hashtag = ""
        _hashtags = []
        for hashtag in hashtags:
            if len(link + current_tweet_hashtag + hashtag + " ") < TWEET_LENGTH:
                current_tweet_hashtag += hashtag + " "
            else:
                _hashtags.append(current_tweet_hashtag.strip().lstrip().rstrip())
                current_tweet_hashtag = hashtag

        return tweettemplate(text=text, link=link, hashtags=_hashtags)
