"""Setup celery to use in service."""

from celery import Celery
from kombu import Queue

from config import settings

app = Celery(
    "perceiver",
    broker=str(settings.rabbitmq.connection_url),
    include=("ingestion.tasks",),
)

app.conf.update(
    task_default_delivery_mode="persistent",
    # Queues
    task_queues=(
        Queue(
            "ingestion_high",
            durable=True,
        ),
    ),
    # Routes
    task_routes={
        "ingestion.tasks.ingest_user_data": {"queue": "ingestion_high"}
    },
    # RabbitMQ publish confirmation
    broker_transport_options={
        "confirm_publish": True,
    },
    # Celery 6 behavior
    worker_cancel_long_running_tasks_on_connection_loss=True,
)

if __name__ == "__main__":
    app.start()
