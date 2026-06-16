import logging

from core.factory.provider_factory import ProviderFactory
from database.core import AsyncSession
from ingestion.schemas import (
    UserIntegrationResponse,
    UserIntegrationTaskPayload,
)
from integrations.schemas import UserIntegrationCreate
from integrations.service import (
    create_or_update as create_or_update_integration,
)
from user.service import get_or_create as get_or_create_user

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingest user data from third party service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def pass_user_integration_data(
        self, payload: UserIntegrationTaskPayload
    ) -> UserIntegrationResponse:
        """Pass user integration data from payload."""
        user_id = payload.user_id
        integration = payload.integration

        user = await get_or_create_user(
            db_session=self.session, user_id=user_id
        )

        provider = ProviderFactory.get_entity(integration)
        integration_user_id = await provider.get_identity(
            user.id, payload.credentials
        )

        integration_create = UserIntegrationCreate(
            user_id=user_id,
            integration=integration,
            integration_user_id=integration_user_id,
            credentials=payload.credentials.model_dump(exclude_unset=True),
        )
        new_integration = await create_or_update_integration(
            db_session=self.session,
            integration_in=integration_create,
            updated_at=payload.updated_at,
        )

        logger.info(
            f"Added new integration: {integration} for user: {user_id}"
        )

        return UserIntegrationResponse(user=user, integration=new_integration)
