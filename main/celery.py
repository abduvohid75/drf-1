from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

from celery.schedules import crontab

logger = logging.getLogger('celery')
logger.setLevel(logging.DEBUG)
log_file = 'logs/logging.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_inactive_users': {
        'task': 'your_app.tasks.check_and_block_inactive_users',
        'schedule': crontab(minute=0, hour=0),
    },
}
