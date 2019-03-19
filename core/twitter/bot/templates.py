from string import Template
from dataclasses import dataclass
from core.twitter.twitter_api import TwitterApi


@dataclass
class TweetTemplate:
    party1: str
    party1_count: int
    party2: str
    party2_count: str
    place: str

    def get_tweet(self):
        hashtags = TwitterApi().get_trends()

        return Template(
            """As per today's prediction $party1 will win $party1_count seats and $party2 will win $party2_count seats.
            Not satisfied with the prediction ???. Take part in the opinion poll and change $place fate.
            https://www.indiaelections.xyz/poll/opinion-poll/
            #bjp #inccongress #congress #india #admk #dmk $hashtags""").substitute(
            party1=self.party1, party1_count=self.party1_count, party2=self.party2, party2_count=self.party2_count,
            place=self.place, hashtags=" ".join(hashtags))
