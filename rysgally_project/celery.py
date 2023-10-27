import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rysgally_project.settings")
app = Celery("rysgally_project")
app.config_from_object("django.conf:settings", namespace="CELERY")

# add tasks here

app.conf.beat_schedule = {
    "create_daily_commit": {
        "task": "apps.commits.tasks.create_daily_commit",
        "schedule": crontab(hour=0, minute=0),
    },
}

app.autodiscover_tasks()
