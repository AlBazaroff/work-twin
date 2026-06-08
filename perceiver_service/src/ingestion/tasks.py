from celery.utils.log import get_task_logger

from core.celery import app
from core.decorators import async_task
from database.core import AsyncSessionLocal
from ingestion.schemas import (
    UserIntegrationTaskPayload,
    IntegrationDataAnalysisTaskPayload,
)
from ingestion.ingestion import IngestionService
from user.enums import UserStatus


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
    async with AsyncSessionLocal() as session:
        service = IngestionService(session)
        response = await service.pass_user_integration_data(payload)

        user = response.user
        integration = response.integration

        logger.info(
            f"Added new integration: {integration.integration}"
            f" for user: {user.id}"
        )

        if user.status == UserStatus.PAID:
            logger.info(f"User {user.id} is paid, add analysis task.")
            analyze_user_integration_data.delay(
                IntegrationDataAnalysisTaskPayload(
                    integration_id=integration.id
                ).model_dump_json()
            )


@app.task(
    name="ingestion.tasks.analyze_integration_data",
    retry_backoff=True,
    retry_jitter=True,
    acks_late=True,
)
@async_task
async def analyze_user_integration_data(payload):
    """Analyze user integration data task."""
    payload = IntegrationDataAnalysisTaskPayload.model_validate_json(payload)
    # TODO: implement analysis logic
