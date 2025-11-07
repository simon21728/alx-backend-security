# ip_tracking/celery.py

import os
import django
from celery import Celery

# 1. Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ip_tracking.settings")  # <-- change if your settings module is different

# 2. Initialize Django
django.setup()

# 3. Create Celery app
app = Celery("ip_tracking")

# 4. Configure Celery to use Django settings with CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# 5. Auto-discover tasks from all installed apps
app.autodiscover_tasks()
