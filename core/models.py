from collections import Counter

from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncDate

from core.constants import PARTIES
from core.twitter.helpers import lower_bound, upper_bound


class TweetStats(models.Model):
    q = models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    added_time = models.DateTimeField(auto_now_add=True)
    positive = models.PositiveIntegerField(default=0)
    negative = models.PositiveIntegerField(default=0)
    neutral = models.PositiveIntegerField(default=0)
    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)
    party = models.CharField(max_length=1, default='', choices=PARTIES)

    @classmethod
    def get_comment_words(cls, q) -> str:
        words = ""
        tweet_stats = cls.objects.filter(q=q)
        for tweet_stat in tweet_stats:
            words += tweet_stat.comment_words + " "

        return words.strip()

    @classmethod
    def filter_by_date_range(cls, range, parties):
        yesterday = True if range == -1 else False
        return TweetStats.objects.filter(
            party__in=parties, added_time__range=(
                lower_bound(range), upper_bound(
                    yesterday=yesterday)))

    @classmethod
    def get_tweet_count_of_party_by_date(cls, party, queryset=None):
        if not queryset:
            queryset = cls.objects.filter(
                party=party).annotate(
                total_count=Sum('count'),
                date=TruncDate('added_time')).values(
                'date',
                'total_count').order_by('date')
        else:
            queryset = queryset.annotate(
                total_count=Sum('count'),
                date=TruncDate('added_time')).values(
                'date',
                'total_count').order_by('date')

        party_count = Counter()
        for q in queryset:
            if hasattr(q, "date") and hasattr(q, "total_count"):
                date = getattr(q, "date")
                total_count = getattr(q, "total_count")
                party_count[str(date)] += total_count
                continue
            party_count[str(q['date'])] += q['total_count']

        return party_count

    @classmethod
    def get_sentiment_data_party_by_date(cls, party, queryset=None):
        if not queryset:
            queryset = cls.objects.filter(
                party=party).annotate(
                pos=Sum('positive'),
                neg=Sum('negative'),
                neu=Sum('neutral'),
                date=TruncDate('added_time')).values(
                'date',
                'pos', 'neg', 'neu').order_by('date')
        else:
            queryset = queryset.annotate(
                pos=Sum('positive'),
                neg=Sum('negative'),
                neu=Sum('neutral'),
                date=TruncDate('added_time')).values(
                'date',
                'pos', 'neg', 'neu').order_by('date')

        sentiment_timeseries = dict()
        pos_data = Counter()
        neg_data = Counter()
        neu_data = Counter()
        for q in queryset:
            if hasattr(q, "date"):
                date = str(getattr(q, "date"))
                pos_data[date] += getattr(q, "pos")
                neg_data[date] += getattr(q, "neg")
                neu_data[date] += getattr(q, "neu")
            else:
                date = str(q['date'])
                pos_data[date] += q['pos']
                neg_data[date] += q['neg']
                neu_data[date] += q['neu']

        for date in pos_data.keys():
            total = sum([pos_data[date], neg_data[date], neu_data[date]])
            positive_percent = ((pos_data[date] / total) * 100)
            positive_percent = round(positive_percent, 2)
            sentiment_timeseries[date] = positive_percent

        return sentiment_timeseries

    def __str__(self):
        q_and_count = "q -> {}\n count {}\n".format(self.q, self.count)
        sentiment = "positive:negative:neutral::{},{},{}\n".format(self.positive,
                                                                   self.negative,
                                                                   self.neutral)
        gender = "male:female::{},{}\n".format(self.male, self.female)
        party = 'party:{}\n'.format(self.get_party_display())
        return q_and_count + sentiment + gender + party


class Wordcloud(models.Model):
    q = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return "{} wordcloud path :: {}".format(self.q, self.file_path)

    def __unicode__(self):
        return "{} wordcloud path :: {}".format(self.q, self.file_path)


class Alliance(models.Model):
    q = models.CharField(max_length=100, unique=True)
    party = models.CharField(max_length=1, default='', choices=PARTIES)

    def __str__(self):
        return "{} : {}".format(self.q, self.party)


class CommentWords(models.Model):
    q = models.CharField(max_length=100)
    comment_words = models.TextField()

    @classmethod
    def get_comment_words(cls, q) -> str:
        words = ""
        commentwords = cls.objects.filter(q=q)
        for commentword in commentwords:
            words += commentword.comment_words + " "

        return words.strip()
