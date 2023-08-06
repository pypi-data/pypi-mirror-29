import os
import uuid

from datetime import date
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from glob import glob

from almanac.models import ElectionEvent
from almanac.utils.aws import defaults, get_bucket
from geography.models import Division, DivisionLevel
from government.models import Body


class Command(BaseCommand):
    help = 'Bakes JavaScript and CSS for calendar'

    def add_arguments(self, parser):
        parser.add_argument(
            '--production',
            default=False,
            action='store_true',
            help="Publish to production"
        )

    def upload_assets(self, base_key):
        for file in glob('../almanac/static/almanac/js/*'):
            filename, ext = os.path.splitext(file.split('/')[-1])
            key = os.path.join(
                base_key,
                'schedule',
                '{}-{}{}'.format(filename, self.hash, ext)
            )
            self.upload_file(file, key, 'text/javascript')

        for file in glob('../almanac/static/almanac/css/*'):
            filename, ext = os.path.splitext(file.split('/')[-1])
            key = os.path.join(
                base_key,
                'schedule',
                '{}-{}{}'.format(filename, self.hash, ext)
            )
            self.upload_file(file, key, 'text/css')

        for file in glob('../almanac/static/almanac/images/*'):
            filename = file.split('/')[-1]
            key = os.path.join(
                base_key,
                'schedule',
                'images',
                filename
            )
            self.upload_file(file, key, 'image/svg+xml')

    def build_national_page(self, base_key):
        placeholder_template_string = render_to_string(
            'almanac/home.export.html', {
                'statics_path': './schedule',
                'data': './schedule/data.json',
                'link_path': './',
                'ad_tag': '',
                'hash': self.hash
            }
        )
        placeholder_html_key = os.path.join(
            base_key,
            'index.html'
        )
        self.upload_html_string(
            placeholder_template_string, placeholder_html_key
        )

        archive_template_string = render_to_string(
            'almanac/home.export.html', {
                'statics_path': '.',
                'data': './data.json',
                'link_path': '../',
                'ad_tag': ':Schedule',
                'hash': self.hash
            }
        )
        archive_html_key = os.path.join(
            base_key,
            'schedule',
            'index.html'
        )

        self.upload_html_string(archive_template_string, archive_html_key)

    def build_state_pages(self, base_key):
        states = Division.objects.filter(
            level__name=DivisionLevel.STATE
        )

        for state in states:
            # if state.label == 'Texas':
            #     continue

            context = {
                'state': state,
                'statics_path': '../../schedule',
                'data': './data.json',
                'ad_tag': ':Schedule',
                'hash': self.hash
            }
            archive_template_string = render_to_string(
                'almanac/state.export.html', context
            )
            archive_html_key = os.path.join(
                base_key,
                state.slug,
                'schedule',
                'index.html'
            )
            self.upload_html_string(archive_template_string, archive_html_key)

            # decide whether to publish the placeholder
            events = ElectionEvent.objects.filter(
                division=state
            )
            event_passed = False
            now = date.today()
            for event in events:
                if event.election_day.date <= now:
                    event_passed = True

            if event_passed:
                print('Skipping placeholder for {0}'.format(state.label))
                continue

            context['statics_path'] = '../schedule'
            context['data'] = './schedule/data.json'
            context['ad_tag'] = ''
            placeholder_template_string = render_to_string(
                'almanac/state.export.html', context
            )
            placeholder_html_key = os.path.join(
                base_key,
                state.slug,
                'index.html'
            )
            self.upload_html_string(
                placeholder_template_string, placeholder_html_key
            )

    def build_body_pages(self, base_key):
        bodies = Body.objects.all()

        for body in bodies:
            context = {
                'body': body,
                'statics_path': '../../schedule',
                'data': './data.json',
                'link_path': '../',
                'ad_tag': ':Schedule',
                'hash': self.hash
            }
            archive_template_string = render_to_string(
                'almanac/body.export.html', context
            )
            archive_html_key = os.path.join(
                base_key,
                body.slug,
                'schedule',
                'index.html'
            )
            self.upload_html_string(archive_template_string, archive_html_key)

            context['statics_path'] = '../schedule'
            context['data'] = './schedule/data.json'
            context['link_path'] = '../'
            context['ad_tag'] = ''

            placeholder_template_string = render_to_string(
                'almanac/body.export.html', context
            )
            placeholder_html_key = os.path.join(
                base_key,
                body.slug,
                'index.html',
            )
            self.upload_html_string(
                placeholder_template_string, placeholder_html_key
            )

    def upload_file(self, file, key, content_type):
        print(key)
        with open(file, 'rb') as f:
            self.bucket.upload_fileobj(f, key, {
                'CacheControl': defaults.CACHE_HEADER,
                'ACL': defaults.ACL,
                'ContentType': content_type
            })

    def upload_html_string(self, string, key):
        print(key)
        self.bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=string,
            CacheControl=defaults.CACHE_HEADER,
            ContentType='text/html'
        )

    def handle(self, *args, **options):
        print('> Publishing statics')
        self.hash = uuid.uuid4().hex[:10]
        self.bucket = get_bucket()

        base_key = 'election-results/2018/'

        self.upload_assets(base_key)
        self.build_national_page(base_key)
        self.build_state_pages(base_key)
        self.build_body_pages(base_key)
