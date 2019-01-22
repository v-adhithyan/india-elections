from django.db import models


class TweetStats(models.Model):
    q = models.CharField(max_length=50)
    count = models.PositiveIntegerField()
    comment_words = models.TextField()
    added_time = models.DateTimeField(auto_now_add=True)
    positive = models.PositiveIntegerField(default=0)
    negative = models.PositiveIntegerField(default=0)
    neutral = models.PositiveIntegerField(default=0)
    male = models.PositiveIntegerField(default=0)
    female = models.PositiveIntegerField(default=0)

    @classmethod
    def get_comment_words(cls, q) -> str:
        words = ""
        tweet_stats = cls.objects.filter(q=q)
        for tweet_stat in tweet_stats:
            words += tweet_stat.comment_words + " "

        return words.strip()


class Wordcloud(models.Model):
    q = models.CharField(max_length=100)
    file_path = models.CharField(max_length=200)

    def __str__(self):
        return "{} wordcloud path :: {}".format(self.q, self.file_path)

    def __unicode__(self):
        return "{} wordcloud path :: {}".format(self.q, self.file_path)
