import pathlib
import tempfile

from django.core.management.base import BaseCommand

from core.models import Wordcloud


class Command(BaseCommand):
    help = "Clear tmp directory used to store wordclouds."

    def handle(self, *args, **options):
        tmpdir = pathlib.Path(tempfile.gettempdir())
        existing_wordclouds = Wordcloud.objects.all().values_list('file_path', flat=True)

        for t in tmpdir.iterdir():
            if t not in existing_wordclouds and t.is_file():
                print(t)
                t.unlink()
