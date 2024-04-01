from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import logging.config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djrssproj.settings')

app = Celery('djrssproj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    worker_prefetch_multiplier=1,
    # Other Celery configurations can be added here
)

# Apply the logging configuration from the Django settings
logging.config.dictConfig(settings.LOGGING)