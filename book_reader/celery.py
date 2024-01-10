from celery.schedules import crontab
from django.conf import settings
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_reader.settings')
app = Celery('book_reader')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    app.conf.timezone = 'UTC'
    app.conf.beat_schedule = {
        'make-analytics-every-day': {
            'task': 'apps.analytics.tasks.collect_analytics',
            # run at 1:01 AM PT (9:01 AM UTC)
            'schedule': crontab(hour=7, minute=56),
        },
    }
