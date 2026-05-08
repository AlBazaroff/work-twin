"""Setup celery to use in service."""

from celery import Celery

from src.config import settings

app = Celery(
    "perceiver",
    broker=str(settings.broker_url),
)

app.autodiscover_tasks()
