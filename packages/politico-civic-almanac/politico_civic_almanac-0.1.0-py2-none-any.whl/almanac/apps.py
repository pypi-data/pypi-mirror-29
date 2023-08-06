from django.apps import AppConfig


class AlmanacConfig(AppConfig):
    name = 'almanac'

    def ready(self):
        from almanac import signals  # noqa
