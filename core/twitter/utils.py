import os
import re
import tempfile

import matplotlib.pyplot as plot
import textblob
from django.utils.encoding import smart_text
from wordcloud import WordCloud, STOPWORDS

from core.models import TweetStats, Wordcloud

_STOPWORDS = set(STOPWORDS)


def clean_tweet(tweet):
    tweet = ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", smart_text(tweet)).split())
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
        wordcloud = Wordcloud.objects.get(q=q)
        if not os.path.exists(wordcloud.file_path):
            file_path = _generate_word_cloud_1(q=q)
            wordcloud.file_path = file_path
            wordcloud.save()
            return file_path

        return wordcloud.file_path
    except Wordcloud.DoesNotExist:
        file_path = _generate_word_cloud_1(q=q)
        Wordcloud.objects.create(q=q, file_path=file_path)
        return file_path


def put_word_cloud(q, file_path):
    try:
        wc = Wordcloud.objects.get(q=q)
        wc.file_path = file_path
        wc.save()
    except Wordcloud.DoesNotExist:
        Wordcloud.objects.create(q=q, file_path=file_path)


def _generate_word_cloud_1(q, tweets_dict):
    tweet_texts = (tweet['cleaned_tweet'] for tweet in tweets_dict)
    comment_words = ' '

    for tweet in tweet_texts:
        tweet = smart_text(tweet).lower()
        tokens = tweet.split(" ")

        for word in tokens:
            comment_words = comment_words + word + ' '

    comment_words += TweetStats.get_comment_words(q=q)

    wordcloud = WordCloud(width=800,
                          height=800,
                          background_color='white',
                          stopwords=_STOPWORDS,
                          min_font_size=10).generate(comment_words)

    plot.figure(figsize=(8, 8), facecolor=None)
    plot.imshow(wordcloud)
    plot.axis("off")
    plot.tight_layout(pad=0)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    plot.savefig(temp_file.name)

    put_word_cloud(q, file_path=temp_file.name + ".png")
    TweetStats.objects.create(q=q, count=len(tweets_dict), comment_words=comment_words)

    return temp_file.name + ".png"


def generate_view_dict() -> dict:
    candidate_n_party_dict = dict()
    candidate_n_party_dict['modi'] = "upa"
    candidate_n_party_dict["bjp"] = "upa"
    candidate_n_party_dict["#Modi2019Interview"] = "upa"
    candidate_n_party_dict["congress"] = "nda"
    candidate_n_party_dict["rahulgandhi"] = "nda"
    candidate_n_party_dict["soniagandhi"] = "nda"

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
        "nda_post_count": 0
    }

    upa_post_count = 0
    nda_post_count = 0

    for tweet in tweets:
        tag = "#" + tweet.q
        party = candidate_n_party_dict.get(tweet.q, '')

        if party == "nda":
            nda_tags = data["nda_tags"]
            nda_tags.add(tag)

            data["nda_" + tweet.sentiment] += 1
            data["nda_tags"] = nda_tags
            nda_post_count += tweet.count
            continue

        if party == "upa":
            upa_tags = data["upa_tags"]
            upa_tags.add(tag)

            data["upa_" + tweet.sentiment] += 1
            data["upa_tags"] = upa_tags
            upa_post_count += tweet.count
            continue

    data["upa_tags"] = " ".join(list(data["upa_tags"]))
    data["nda_tags"] = " ".join(list(data["nda_tags"]))
    data["upa_post_count"] = upa_post_count
    data["nda_post_count"] = nda_post_count
    return data
