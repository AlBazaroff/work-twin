"""Setup celery to use in service."""

from celery import Celery

from config import settings

app = Celery(
    "perceiver",
    broker=str(settings.rabbitmq.connection_url),
    include=("ingestion.tasks",),
)

app.conf.update(
    task_routes={
        "ingestion.tasks.ingest_user_data": {"queue": "ingestion_high"}
    }
)

if __name__ == "__main__":
    app.start()
