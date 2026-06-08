"""Setup celery to use in service."""

from celery import Celery
from celery.signals import worker_process_init
from kombu import Queue

from database.core import engine
from config import get_settings


@worker_process_init.connect
def dispose_sqlalchemy_engine(**kwargs):
    """Reset connection pool, when worker start."""
    engine.sync_engine.dispose()


high_queue = Queue("ingestion_high", durable=True)
heavy_queue = Queue("ingestion_heavy", durable=True)

settings = get_settings()

app = Celery(
    "perceiver",
    broker=str(settings.rabbitmq.connection_url),
    include=("ingestion.tasks",),
)

app.conf.update(
    task_default_delivery_mode="persistent",
    # Queues
    task_queues=(
        high_queue,
        heavy_queue,
    ),
    # Routes
    task_routes={
        "ingestion.tasks.ingest_user_data": {
            "queue": high_queue.name,
        },
        "ingestion.tasks.analyze_integration_data": {
            "queue": heavy_queue.name,
        },
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
