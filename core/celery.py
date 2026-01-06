import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

from core import tasks  # noqa

app.conf.beat_schedule = {
    "add-every-monday-morning": {
        "task": "newsletter.tasks.send_newsletter",
        "schedule": crontab(hour=9, minute=00, day_of_week=1),
    }
}
