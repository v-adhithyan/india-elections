import json
import random
import re
import tempfile
from collections import namedtuple
from pathlib import Path
import itertools

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
INT_KEYS = [
    "positive",
    "negative",
    "neutral",
    "post_count",
    "male",
    "female",
    "tags"
]
SET_KEYS = [
    "tags"
]
SENTIMENT_KEYS = [
    "positive",
    "negative",
    "neutral"
]

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
    candidate_party_dict = {}
    alliances = Alliance.objects.all()
    for a in alliances:
        candidate_party_dict[a.q] = a.get_party_display()
    candidate_party_dict["test"] = random.choice(['upa', 'nda'])  # for pytest
    return candidate_party_dict


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

    """if not CANDIDATE_PARTY_DICT:
        _frame_candidate_party_dict()
    if len(CANDIDATE_PARTY_DICT) != Alliance.objects.count():
        _frame_candidate_party_dict()"""

    return _frame_candidate_party_dict()


def calculate_percentage(positive, negative, neutral):
    total = positive + negative + neutral
    try:
        return float(positive/total)*100, float(negative/total)*100, float(neutral/total)*100
    except ZeroDivisionError:
        return 0, 0, 0


def convert_sentiment_to_percentage(data):
    upa_positive, upa_negative, upa_neutral = calculate_percentage(
        data["upa_positive"], data["upa_negative"], data["upa_neutral"])
    nda_positive, nda_negative, nda_neutral = calculate_percentage(
        data["nda_positive"], data["nda_negative"], data["nda_neutral"])
    data["upa_positive"] = round(upa_positive, 2)
    data["upa_negative"] = round(upa_negative, 2)
    data["upa_neutral"] = round(upa_neutral, 2)
    data["nda_positive"] = round(nda_positive, 2)
    data["nda_negative"] = round(nda_negative, 2)
    data["nda_neutral"] = round(nda_neutral, 2)
    return data


def convert_tn_sentiment_to_percentage(data):
    dmk_positive, dmk_negative, dmk_neutral = calculate_percentage(
        data["dmk_positive"], data["dmk_negative"], data["dmk_neutral"])
    admk_positive, admk_negative, admk_neutral = calculate_percentage(
        data["admk_positive"], data["admk_negative"], data["admk_neutral"])
    data["dmk_positive"] = round(dmk_positive, 2)
    data["dmk_negative"] = round(dmk_negative, 2)
    data["dmk_neutral"] = round(dmk_neutral, 2)
    data["admk_positive"] = round(admk_positive, 2)
    data["admk_negative"] = round(admk_negative, 2)
    data["admk_neutral"] = round(admk_neutral, 2)
    return data


def sentiment_to_percentage(data, party_1, party_2):
    p1_positive, p1_negative, p1_neutral = calculate_percentage(
        data[party_1 + "_positive"], data[party_1 + "_negative"], data[party_1 + "_neutral"])
    p2_positive, p2_negative, p2_neutral = calculate_percentage(
        data[party_2 + "_positive"], data[party_2 + "_negative"], data[party_2 + "_neutral"])
    data[party_1 + "_positive"] = round(p1_positive, 2)
    data[party_1 + "_negative"] = round(p1_negative, 2)
    data[party_1 + "_neutral"] = round(p1_neutral, 2)
    data[party_2 + "_positive"] = round(p2_positive, 2)
    data[party_2 + "_negative"] = round(p2_negative, 2)
    data[party_2 + "_neutral"] = round(p2_neutral, 2)
    return data


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

    data = convert_sentiment_to_percentage(data)
    data.update(get_timeseries_tweet_data())
    return data


def generate_tn_dict() -> dict:
    candidate_n_party_dict = get_candidate_and_party_dict()

    tweets = TweetStats.objects.all()
    data = {
        "admk_positive": 0,
        "admk_negative": 0,
        "admk_neutral": 0,
        "dmk_positive": 0,
        "dmk_negative": 0,
        "dmk_neutral": 0,
        "admk_tags": set(),
        "dmk_tags": set(),
        "admk_post_count": 0,
        "dmk_post_count": 0,
        "admk_male": 0,
        "admk_female": 0,
        "dmk_male": 0,
        "dmk_female": 0
    }

    admk_post_count = 0
    dmk_post_count = 0

    for tweet in tweets:
        tag = "#" + tweet.q
        party = candidate_n_party_dict.get(tweet.q, '')

        if party == "dmk":
            dmk_tags = data["dmk_tags"]
            dmk_tags.add(tag)

            data["dmk_positive"] += tweet.positive
            data["dmk_negative"] += tweet.negative
            data["dmk_neutral"] += tweet.neutral
            data["dmk_tags"] = dmk_tags
            data["dmk_male"] += tweet.male
            data["dmk_female"] += tweet.female
            dmk_post_count += tweet.count
            continue

        if party == "admk":
            admk_tags = data["admk_tags"]
            admk_tags.add(tag)

            data["admk_positive"] += tweet.positive
            data["admk_negative"] += tweet.negative
            data["admk_neutral"] += tweet.neutral
            data["admk_tags"] = admk_tags
            data["admk_male"] += tweet.male
            data["admk_female"] += tweet.female
            admk_post_count += tweet.count
            continue

    data["admk_tags"] = " ".join(list(data["admk_tags"]))
    data["dmk_tags"] = " ".join(list(data["dmk_tags"]))
    data["admk_post_count"] = admk_post_count
    data["dmk_post_count"] = dmk_post_count

    data = convert_tn_sentiment_to_percentage(data)
    data.update(get_timeseries_tweet_tn_data())
    return data


def _frame_keys(parties, keys):
    return list(map("_".join, itertools.product(parties, keys, repeat=1)))


def _frame_initial_dict(keys, value) -> dict:
    return {key: value for key in keys}


def _add_int_data(data, party, tweet_stats):
    for key in INT_KEYS:
        if hasattr(tweet_stats, key):
            data["{}_{}".format(party, key)] = getattr(tweet_stats, key)
    return data


def generate_view_data(party_1, party_2):
    candidate_n_party_dict = get_candidate_and_party_dict()
    parties = [
        party_1,
        party_2
    ]

    int_keys = _frame_keys(parties, INT_KEYS)
    set_keys = _frame_keys(parties, SET_KEYS)

    data = _frame_initial_dict(int_keys, 0)
    data.update(_frame_initial_dict(set_keys, set()))
    print(data)
    tweets = TweetStats.objects.all()
    for tweet in tweets:
        tag = "#" + tweet.q
        party = candidate_n_party_dict.get(tweet.q, '')
        if party not in parties:
            continue

        data = _add_int_data(data, party, tweet)

        tags_key = "{}_{}".format(party, "tags")
        tags = data[tags_key]
        tags.add(tag)
        data[tags_key] = tags

        party_post_count = "{}_{}".format(party, "post_count")
        data[party_post_count] = data[party_post_count] + tweet.count

    party1_tags = "{}_{}".format(party_1, "tags")
    party2_tags = "{}_{}".format(party_2, "tags")
    data[party1_tags] = " ".join(list(data[party1_tags]))
    data[party2_tags] = " ".join(list(data[party2_tags]))

    data = sentiment_to_percentage(data, party_1, party_2)
    data.update(get_timeseries_data(party_1, party_2))
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


def get_timeseries_tweet_tn_data() -> dict:
    admk = TweetStats.get_tweet_count_of_party_by_date(party='a')
    dmk = TweetStats.get_tweet_count_of_party_by_date(party='d')

    return {
        'admk_time_series': convert_timedata_to_2d(admk),
        'dmk_time_series': convert_timedata_to_2d(dmk)
    }


def get_timeseries_data(party_1, party_2):
    timeseries = "time_series"

    party1_data = TweetStats.get_tweet_count_of_party_by_date(party=party_1[0])
    party2_data = TweetStats.get_tweet_count_of_party_by_date(party=party_2[1])

    return {
        "{}_{}".format(party_1, timeseries): convert_timedata_to_2d(party1_data),
        "{}_{}".format(party_2, timeseries): convert_timedata_to_2d(party2_data)
    }
