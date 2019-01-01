import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Download textblob corpora.'

    def handle(self, *args, **options):
        proc = subprocess.Popen(["python",
                                 "-m",
                                 "textblob.download_corpora"],
                                stdout=subprocess.PIPE
                                )
        out = proc.stdout.read().decode("utf-8")
        self.stdout.write(out)
