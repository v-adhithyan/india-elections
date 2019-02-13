from django.core.management.base import BaseCommand

from core.models import TweetStats, CommentWords


class Command(BaseCommand):
    help = "Utility to migrate existing comment words from Tweetstats table to CommentWords table,"

    def handle(self, *args, **options):
        tweetstats = TweetStats.objects.all()

        for ts in tweetstats:
            if hasattr(ts, "comment_words"):
                self.stdout.write(".")
                CommentWords.objects.create(q=ts.q, comment_words=ts.comment_words)
            else:
                self.stdout.write("comment_words column not in Tweetstats table.")
