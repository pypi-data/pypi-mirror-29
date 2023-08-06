from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'Bootstrap development for almanac'
    )

    def handle(self, *args, **options):
        call_command('bootstrap_geography')
        call_command('bootstrap_jurisdictions')
        call_command('bootstrap_fed')
        call_command('bootstrap_offices')
        call_command('bootstrap_parties')
