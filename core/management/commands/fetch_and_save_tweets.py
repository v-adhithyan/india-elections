from django.core.management.base import CommandError, LabelCommand

from core.twitter.twitter_api import TwitterApi


class Command(LabelCommand):

    def handle_label(self, label, **options):
        try:
            twitter_api = TwitterApi()
            count = twitter_api.get_and_save_tweets(query=label)

            self.stdout.write(self.style.SUCCESS
                              ('Downloaded {} tweets relating to {} and saved in db')
                              .format(count, label))
        except CommandError as e:
            self.stderr.write(str(e))
            raise
