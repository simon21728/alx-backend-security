
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_security.settings')

app = Celery('alx_backend_security')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule your task
app.conf.beat_schedule = {
    'detect-suspicious-ips-hourly': {
        'task': 'ip_tracking.tasks.detect_suspicious_ips',
        'schedule': crontab(minute=0, hour='*'),  # Runs every hour
    },
}
