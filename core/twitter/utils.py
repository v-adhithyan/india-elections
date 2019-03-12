import itertools
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

from core.models import Alliance, CommentWords, TweetStats, Wordcloud
from core.constants import (PARTIES_COLOR, TOTAL_LOKSABHA_SEATS_INDIA, TOTAL_LOKSABHA_SEATS_TN,
                            ALL_TIME,
                            TIMERANGE_DICT)

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
]
SET_KEYS = [
    "tags"
]
SENTIMENT_KEYS = [
    "positive",
    "negative",
    "neutral"
]

TIMESERIES = "time_series"
SENTIMENT_TIMESERIES = "sentiment_time_series"

TIMESERIES_DICT = {
    TIMESERIES: TweetStats.get_tweet_count_of_party_by_date,
    SENTIMENT_TIMESERIES: TweetStats.get_sentiment_data_party_by_date
}

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

        try:
            # delete old file to save memory in prodution :)
            old_file = Path(wc.file_path)
            old_file.unlink()
        except Exception:
            pass

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

    # put_word_cloud(q, file_path=temp_file.name + ".png")

    plot.cla()
    plot.close('all')

    TweetStats.objects.create(q=q, count=len(tweets_dict),
                              positive=pos, negative=neg, neutral=neg,
                              male=male, female=female, party=party)

    CommentWords.objects.create(q=q, comment_words=comment_words)

    return temp_file.name + ".png"


def get_candidate_and_party_dict() -> dict:
    candidate_party_dict = {}
    alliances = Alliance.objects.all()
    for a in alliances:
        candidate_party_dict[a.q] = a.get_party_display()
    candidate_party_dict["test"] = random.choice(['upa', 'nda'])  # for pytest
    return candidate_party_dict


def calculate_percentage(positive, negative, neutral):
    total = positive + negative + neutral
    try:
        return float(positive / total) * 100, float(negative / total) * 100, float(neutral / total) * 100
    except ZeroDivisionError:
        return 0, 0, 0


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


def _frame_keys(parties, keys):
    return list(map("_".join, itertools.product(parties, keys, repeat=1)))


def _frame_initial_dict(keys, value) -> dict:
    return {key: value for key in keys}


def _add_set_data_to_initial_dict(keys):
    return {key: set(["#" + key.split("_")[0]]) for key in keys}


def _add_int_data(data, party, tweet_stats):
    for key in INT_KEYS:
        if hasattr(tweet_stats, key):
            party_key = "{}_{}".format(party, key)
            data[party_key] = data[party_key] + getattr(tweet_stats, key)
    return data


def generate_view_data(party_1, party_2, remove=False, timerange=ALL_TIME):
    candidate_n_party_dict = get_candidate_and_party_dict()
    parties = [
        party_1,
        party_2
    ]

    int_keys = _frame_keys(parties, INT_KEYS)
    set_keys = _frame_keys(parties, SET_KEYS)

    data = _frame_initial_dict(int_keys, 0)
    data.update(_add_set_data_to_initial_dict(set_keys))
    _parties = [party_1[0], party_2[0]]
    if TIMERANGE_DICT.get(timerange, None) is None:
        tweets = TweetStats.objects.filter(party__in=_parties)
    else:
        tweets = TweetStats.filter_by_date_range(parties=_parties, range=TIMERANGE_DICT[timerange])

    for tweet in tweets:
        tag = "#" + tweet.q
        party = candidate_n_party_dict.get(tweet.q, '')
        if party not in parties:
            continue

        data.update(_add_int_data(data, party, tweet))

        tags_key = "{}_{}".format(party, "tags")
        tags = data[tags_key]
        tags.add(tag)
        data[tags_key] = tags

        party_post_count = "{}_{}".format(party, "post_count")
        data[party_post_count] = data[party_post_count] + tweet.count

    party1_tags = "{}_{}".format(party_1, "tags")
    party2_tags = "{}_{}".format(party_2, "tags")

    if remove:
        data[party1_tags].remove("#" + party_1)
        data[party2_tags].remove("#" + party_2)

    data[party1_tags] = " ".join(list(data[party1_tags]))
    data[party2_tags] = " ".join(list(data[party2_tags]))

    data = sentiment_to_percentage(data, party_1, party_2)
    # data.update(get_timeseries_data(TIMESERIES, party_1, party_2, queryset=tweets))
    # data.update(get_timeseries_data(SENTIMENT_TIMESERIES, party_1, party_2, queryset=tweets))

    return replace_parties_from_data(data, party_1, party_2, queryset=tweets)


def replace_parties_from_data(data, party_1, party_2, queryset=None):
    parties = {
        party_1: "party1",
        party_2: "party2"
    }

    return_data = {
        k.replace(party_1, parties[party_1]): v for k, v in data.items() if party_1 in k
    }
    return_data.update({
        k.replace(party_2, parties[party_2]): v for k, v in data.items() if party_2 in k
    })

    return_data.update({
        "party1": party_1,
        "party2": party_2
    })

    return_data.update(get_new_timeseries_data(TIMESERIES, party_1, party_2, queryset=queryset))
    return_data.update(get_new_timeseries_data(SENTIMENT_TIMESERIES, party_1, party_2, queryset=queryset))

    return_data.update({
        "party1_color": PARTIES_COLOR[party_1],
        "party2_color": PARTIES_COLOR[party_2]
    })

    return_data.update(TweetStats.get_all_time_sentiment_difference(party=party_1[0], alias="party1", data=return_data))
    return_data.update(TweetStats.get_all_time_sentiment_difference(party=party_2[0], alias="party2", data=return_data))

    return update_winning_seats(return_data, parties)


def update_winning_seats(data, parties):
    if "upa" in parties and "nda" in parties:
        seats = TOTAL_LOKSABHA_SEATS_INDIA
    else:  # should be tn since we dont have any other parties
        seats = TOTAL_LOKSABHA_SEATS_TN

    data["party1_seats"] = int((data["party1_positive"] / 100) * seats)
    data["party2_seats"] = int((data["party2_positive"] / 100) * seats)
    data["total_seats"] = seats

    return data

def convert_timedata_to_2d(data):
    data_2d = []
    for x, y in data.items():
        data_2d.append({
            'x': x,
            'y': y
        })

    return mark_safe(json.dumps(data_2d))


def convert_timedata_to_2d_new(data1, data2, party1, party2):
    data_2d = []

    for k in data1.keys():
        p1_val = data1.get(k)
        p2_val = data2.get(k)

        if p1_val is None or p2_val is None:
            continue

        data_2d.append({
            'date': k,
            party1: p1_val,
            party2: p2_val
        })

    return mark_safe(json.dumps(data_2d))


def get_timeseries_data(key, party_1, party_2):
    get_timeseries = TIMESERIES_DICT[key]
    party1_data = get_timeseries(party=party_1[0])
    party2_data = get_timeseries(party=party_2[0])

    return {
        "{}_{}".format(party_1, key): convert_timedata_to_2d(party1_data),
        "{}_{}".format(party_2, key): convert_timedata_to_2d(party2_data)
    }


def get_new_timeseries_data(key, party_1, party_2, queryset=None):
    get_timeseries = TIMESERIES_DICT[key]

    p1_queryset = None
    p2_queryset = None
    if queryset:
        p1_queryset = queryset.filter(party=party_1[0])
        p2_queryset = queryset.filter(party=party_2[0])

    party1_data = get_timeseries(party=party_1[0], queryset=p1_queryset)
    party2_data = get_timeseries(party=party_2[0], queryset=p2_queryset)

    return {
        "new_" + key: convert_timedata_to_2d_new(party1_data, party2_data, party_1, party_2)
    }
