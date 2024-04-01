# rssapp/apps.py
from django.apps import AppConfig
from django.conf import settings

class RssappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rssapp'

    def ready(self):
        if settings.USE_CELERY and not self.running_unit_tests():
            from .tasks import update_articles_command
            update_articles_command.delay()

    def running_unit_tests(self):
        # Implement a check to see if unit tests are running
        # This is a simple check, you might want to improve it based on your setup
        import sys
        return 'test' in sys.argv