import json
import random
import re
import tempfile
from collections import namedtuple
from pathlib import Path

import matplotlib.pyplot as plot
import textblob
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from guess_indian_gender import IndianGenderPredictor
from wordcloud import STOPWORDS, WordCloud

from core.models import TweetStats, Wordcloud, Alliance, CommentWords

_STOPWORDS = set(STOPWORDS)
# loading gender predictor as global constant, so that training happens
# only once.
GENDER_PREDICTOR = IndianGenderPredictor()
CANDIDATE_PARTY_DICT = {}

def clean_tweet(tweet):
    tweet = ' '.join(
        re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", smart_text(tweet)).split())
    tweet = tweet.replace("RT ", "").strip()
    return tweet


def get_tweet_sentiment(tweet) -> str:
    analysis = textblob.TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def get_word_cloud(q):
    try:
        # While fetching tweets itself we generate word cloud
        # so if a cloud doesnot exists, we havent fetched tweets for that q
        # so raise error
        wordcloud = Wordcloud.objects.get(q=q)
        return wordcloud.file_path
    except Wordcloud.DoesNotExist:
        raise


def put_word_cloud(q, file_path):
    try:
        wc = Wordcloud.objects.get(q=q)

        # delete old file to save memory in prodution :)
        old_file = Path(wc.file_path)
        old_file.unlink()

        wc.file_path = file_path
        wc.save()
    except Wordcloud.DoesNotExist:
        Wordcloud.objects.create(q=q, file_path=file_path)


def _generate_word_cloud_1(q, tweets_dict):
    return generate_word_cloud_1(q, tweets_dict)


def generate_word_cloud_1(q, tweets_dict):
    Tweet = namedtuple("Tweet", "tweet sentiment user_name")
    party = tweets_dict[0]['party']
    tweets = (Tweet(tweet["cleaned_tweet"], tweet['tweet_sentiment'],
                    tweet['user_name']) for tweet in tweets_dict)
    comment_words = ' '

    pos = 0
    neg = 0
    neu = 0
    male = 0
    female = 0

    for _tweet in tweets:
        tweet = smart_text(_tweet.tweet).lower()
        tokens = tweet.split(" ")

        for word in tokens:
            comment_words = comment_words + word + ' '

        if _tweet.sentiment == "positive":
            pos += 1
        elif _tweet.sentiment == "negative":
            neg += 1
        else:
            neu += 1

        gender = GENDER_PREDICTOR.predict(name=_tweet.user_name)
        if gender == 'male':
            male += 1
        if gender == 'female':
            female += 1

    wordcloud = WordCloud(width=800,
                          height=800,
                          background_color='white',
                          stopwords=_STOPWORDS,
                          min_font_size=10).generate(comment_words + CommentWords.get_comment_words(q=q))

    plot.figure(figsize=(8, 8), facecolor=None)
    plot.imshow(wordcloud)
    plot.axis("off")
    plot.tight_layout(pad=0)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    plot.savefig(temp_file.name)

    put_word_cloud(q, file_path=temp_file.name + ".png")

    plot.cla()
    plot.close('all')

    TweetStats.objects.create(q=q, count=len(tweets_dict),
                              positive=pos, negative=neg, neutral=neg,
                              male=male, female=female, party=party)

    CommentWords.objects.create(q=q, comment_words=comment_words)

    return temp_file.name + ".png"

def _frame_candidate_party_dict():
    global CANDIDATE_PARTY_DICT
    CANDIDATE_PARTY_DICT = {}
    alliances = Alliance.objects.all()
    for a in alliances:
        CANDIDATE_PARTY_DICT[a.q] = a.get_party_display()
    CANDIDATE_PARTY_DICT["test"] = random.choice(['upa', 'nda'])

def get_candidate_and_party_dict() -> dict:
    """
    candidate_n_party_dict = dict()
    candidate_n_party_dict['modi'] = "nda"
    candidate_n_party_dict["bjp"] = "nda"
    candidate_n_party_dict["#Modi2019Interview"] = "nda"
    candidate_n_party_dict["#GoBackSadistModi"] = "nda"
    candidate_n_party_dict["#GoBackModi"] = "nda"
    candidate_n_party_dict["#TNWelcomesModi"] = "nda"
    candidate_n_party_dict["#MaduraiWelcomesModi"] = "nda"
    candidate_n_party_dict["#TNThanksModi"] = "nda"

    candidate_n_party_dict["congress"] = "upa"
    candidate_n_party_dict["rahulgandhi"] = "upa"
    candidate_n_party_dict["soniagandhi"] = "upa"
    candidate_n_party_dict["Priyanka"] = "upa"
    candidate_n_party_dict['priyanka'] = "upa"
    candidate_n_party_dict['test'] = random.choice(['upa', 'nda'])  # for pytest
    """

    if not CANDIDATE_PARTY_DICT:
        _frame_candidate_party_dict()
    if len(CANDIDATE_PARTY_DICT) != Alliance.objects.count():
        _frame_candidate_party_dict()

    return CANDIDATE_PARTY_DICT


def generate_view_dict() -> dict:
    candidate_n_party_dict = get_candidate_and_party_dict()

    tweets = TweetStats.objects.all()
    data = {
        "upa_positive": 0,
        "upa_negative": 0,
        "upa_neutral": 0,
        "nda_positive": 0,
        "nda_negative": 0,
        "nda_neutral": 0,
        "upa_tags": set(),
        "nda_tags": set(),
        "upa_post_count": 0,
        "nda_post_count": 0,
        "upa_male": 0,
        "upa_female": 0,
        "nda_male": 0,
        "nda_female": 0
    }

    upa_post_count = 0
    nda_post_count = 0

    for tweet in tweets:
        tag = "#" + tweet.q
        party = candidate_n_party_dict.get(tweet.q, '')

        if party == "nda":
            nda_tags = data["nda_tags"]
            nda_tags.add(tag)

            data["nda_positive"] += tweet.positive
            data["nda_negative"] += tweet.negative
            data["nda_neutral"] += tweet.neutral
            data["nda_tags"] = nda_tags
            data["nda_male"] += tweet.male
            data["nda_female"] += tweet.female
            nda_post_count += tweet.count
            continue

        if party == "upa":
            upa_tags = data["upa_tags"]
            upa_tags.add(tag)

            data["upa_positive"] += tweet.positive
            data["upa_negative"] += tweet.negative
            data["upa_neutral"] += tweet.neutral
            data["upa_tags"] = upa_tags
            data["upa_male"] += tweet.male
            data["upa_female"] += tweet.female
            upa_post_count += tweet.count
            continue

    data["upa_tags"] = " ".join(list(data["upa_tags"]))
    data["nda_tags"] = " ".join(list(data["nda_tags"]))
    data["upa_post_count"] = upa_post_count
    data["nda_post_count"] = nda_post_count
    data.update(get_timeseries_tweet_data())
    return data


def convert_timedata_to_2d(data):
    data_2d = []
    for x, y in data.items():
        data_2d.append({
            'x': x,
            'y': y
        })

    return mark_safe(json.dumps(data_2d))


def get_timeseries_tweet_data() -> dict:
    upa = TweetStats.get_tweet_count_of_party_by_date(party='u')
    nda = TweetStats.get_tweet_count_of_party_by_date(party='n')

    return {
        'upa_time_series': convert_timedata_to_2d(upa),
        'nda_time_series': convert_timedata_to_2d(nda)
    }
