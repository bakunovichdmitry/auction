import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')

app = Celery('auction')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# TODO: set 10 minutes
# app.conf.beat_schedule = {
#     'start-auctions-every-10-minutes': {
#         'task': 'auctions.tasks.start_auctions',
#         'schedule': crontab(minute=2),
#     },
# }
