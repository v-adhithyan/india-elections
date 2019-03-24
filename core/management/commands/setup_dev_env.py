from django.core.management.base import BaseCommand
from django.core.management import call_command

from core.models import Alliance


class Command(BaseCommand):
    help = "Bootstrap/Setup development environment with data."

    def handle(self, *args, **options):
        self.stdout.write("Running DB migrations ...")
        call_command("migrate")

        self.stdout.write("Populating alliance table ...")
        call_command("populate_alliance")

        self.stdout.write("Downloading textblob corpora ...")
        call_command("textblob_download_corpora")

        self.stdout.write("Populating tweets in DB ...")
        queries = Alliance.objects.all().values_list('q', flat=True)
        for q in queries:
            self.stdout.write("Fetching tweets for {} ...".format(q))
            call_command("fetch_and_save_tweets", q)

        self.stdout.write("Collecting static files ...")
        call_command("collectstatic")
