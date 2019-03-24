from collections import namedtuple

from core.constants import TODAY
from core.image.constants import TWEET_IMAGE
from core.image.helpers import generate_tweet_image
from core.twitter.bot.templates import TweetTemplate
from core.twitter.twitter_api import TwitterApi
from core.twitter.utils import generate_view_data

party_tuple = namedtuple("party_tuple", "party1 party2 place alliance1 alliance2")
national_parties = party_tuple(party1="BJP", party2="Congress", place="India's", alliance1='nda', alliance2='upa')
tn_parties = party_tuple(party1="Admk", party2="Dmk", place="Tamilnadu's", alliance1='admk', alliance2='dmk')


def tweet_prediction(parties, remove=False, timerange=TODAY):
    data = generate_view_data(parties.alliance1, parties.alliance2, remove=remove, timerange=timerange)
    template = TweetTemplate(party1=parties.party1, party2=parties.party2, party1_count=data['party1_seats'],
                             party2_count=data['party2_seats'], place=parties.place, timerange=timerange)

    tweet = template.get_tweet()
    # put prediction text in image
    generate_tweet_image(tweet.text, TWEET_IMAGE)

    # upload to twitter
    twitter = TwitterApi()

    for hashtag in tweet.hashtags:
        status = tweet.link + hashtag
        twitter.api.update_with_media(str(TWEET_IMAGE), status=status)


def tweet_prediction_for_india():
    tweet_prediction(national_parties, remove=True)


def tweet_prediction_for_tamilnadu():
    tweet_prediction(tn_parties)


def tweet_all():
    tweet_prediction_for_india()
    tweet_prediction_for_tamilnadu()
