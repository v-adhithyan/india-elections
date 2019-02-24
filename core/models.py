from collections import Counter

from core.constants import PARTIES
from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncDate


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
    def get_tweet_count_of_party_by_date(cls, party):
        queryset = cls.objects.filter(
            party=party).annotate(
            total_count=Sum('count'),
            date=TruncDate('added_time')).values(
            'date',
            'total_count').order_by('date')

        party_count = Counter()
        for q in queryset:
            party_count[str(q['date'])] += q['total_count']

        return party_count

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
