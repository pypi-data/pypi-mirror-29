from django.core.management.base import BaseCommand

from almanac.celery import publish_all_state_data


class Command(BaseCommand):
    help = 'Bakes JavaScript and CSS for calendar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--production',
            default=False,
            action='store_true',
            help="Publish to production"
        )

        parser.add_argument(
            '--cycle',
            default='2018',
            action='store',
            help="Specify election cycle"
        )

    def handle(self, *args, **options):
        publish_all_state_data.delay(options['cycle'])
