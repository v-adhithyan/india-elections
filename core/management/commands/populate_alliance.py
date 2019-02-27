from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Run this command to populate initial data for Alliance table."

    def handle(self, *args, **kwargs):
        data = {
            'bjp': 'nda',
            'congress': 'upa',
            'modi': 'nda',
            'rahulgandhi': 'upa',
            'admk': 'admk',
            'dmk': 'dmk'
        }
        bulk_data = []
        for q, party in data.items():
            bulk_data.append(Alliance(q=q, party=party[0]))

        Alliance.objects.bulk_create(bulk_data)
