from celery.utils.log import get_task_logger

from core.celery import app
from core.decorators import async_task
from database.core import get_db
from ingestion.schemas import UserIntegrationTaskPayload
from ingestion.services import IngestionService


logger = get_task_logger(__name__)


@app.task(
    name="ingestion.tasks.ingest_user_data",
    retry_backoff=True,
    retry_jitter=True,
    acks_late=True,
    time_limit=10,
    soft_time_limit=8,
)
@async_task
async def ingest_user_integration_data(payload):
    """Ingest user integration data task provided by
    third party service.
    """
    payload = UserIntegrationTaskPayload.model_validate_json(payload)
    async with get_db() as session:
        service = IngestionService(session)
        await service.pass_user_integration_data(payload)
