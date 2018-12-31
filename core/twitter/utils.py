import re
import tempfile

import matplotlib.pyplot as plot
import textblob
from django.utils.encoding import smart_text
from wordcloud import WordCloud, STOPWORDS

from core.models import Tweet


def clean_tweet(tweet):
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", smart_text(tweet)).split())


def get_tweet_sentiment(tweet) -> str:
    analysis = textblob.TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity == 0:
        return "neutral"
    else:
        return "negative"


def generate_word_cloud(q='bjp'):
    tweets = Tweet.objects.filter(q=q)
    tweet_texts = (tweet.tweet for tweet in tweets)
    comment_words = ' '
    stopwords = set(STOPWORDS)

    for tweet in tweet_texts:
        tweet = smart_text(tweet).lower()
        tokens = tweet.split(" ")

        for word in tokens:
            comment_words = comment_words + word + ' '

    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    plot.figure(figsize=(8, 8), facecolor=None)
    plot.imshow(wordcloud)
    plot.axis("off")
    plot.tight_layout(pad=0)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    plot.savefig(temp_file.name)
    return temp_file.name + ".png"
