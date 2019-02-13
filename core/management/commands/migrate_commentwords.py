from django.core.management.base import BaseCommand

from core.models import TweetStats, CommentWords


# Actually this is a wrong way to migrate.
# I will be removing commentwords from Tweetstats table in next commit.
# I do not want to lose the production data of commentwords.
# I should have written this as a migration script instead of command.
# I had less time, so I am writing this as a command.
# Removal process:
# Commit 1: add a new table to store commentwords and migration script to move
# data from TweetStats table to new table.
# Push to production and perform migration.
# Commit 2: remove commentwords column from Tweetstats table and migrate.

class Command(BaseCommand):
    help = "Utility to migrate existing comment words from Tweetstats table to CommentWords table,"

    def handle(self, *args, **options):
        tweetstats = TweetStats.objects.all()

        for ts in tweetstats:
            if hasattr(ts, "comment_words"): # this
                self.stdout.write(".")
                CommentWords.objects.create(q=ts.q, comment_words=ts.comment_words)
            else:
                self.stdout.write("comment_words column not in Tweetstats table.")
