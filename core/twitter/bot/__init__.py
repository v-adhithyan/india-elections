from collections import namedtuple

from core.constants import TODAY
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

    api = TwitterApi()
    api.update_status(status=template.get_tweet())


def tweet_prediction_for_india():
    return tweet_prediction(national_parties, remove=True)


def tweet_prediction_for_tamilnadu():
    return tweet_prediction(tn_parties)
