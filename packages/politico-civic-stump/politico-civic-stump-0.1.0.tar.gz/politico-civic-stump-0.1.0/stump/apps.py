from django.apps import AppConfig


class StumpConfig(AppConfig):
    name = 'stump'

    def ready(self):
        from stump import signals  # noqa
