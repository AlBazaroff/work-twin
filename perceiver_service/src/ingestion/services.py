import logging
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert

from database.core import AsyncSession
from database.enums import UserStatus
from database.models.user import User, UserIntegration
from core.factory.provider_factory import ProviderFactory
from ingestion.schemas import (
    UserIntegrationTaskPayload,
    UserIntegrationResponse,
)

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingest user data from third party service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_create_user(
        self, user_id: UUID, status: UserStatus
    ) -> User:
        stmt = (
            insert(User)
            .values(id=user_id, status=status)
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(status=status),
                where=(User.status != status),
            )
            .returning(User)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one()
        return user

    async def pass_user_integration_data(
        self, payload: UserIntegrationTaskPayload
    ) -> UserIntegrationResponse:
        """Pass user integration data from payload."""
        user_id = payload.user_id
        integration = payload.integration
        status = payload.status

        user: User = await self._get_or_create_user(user_id, status)

        provider = ProviderFactory.get_entity(integration)
        integration_user_id = await provider.get_identity(
            user.id, payload.credentials
        )

        new_integration = UserIntegration(
            integration=integration,
            credentials=payload.credentials,
            integration_user_id=integration_user_id,
        )
        user.integrations.append(new_integration)

        await self.session.commit()
        logger.info(
            f"Added new integration: {integration} for user: {user_id}"
        )

        return UserIntegrationResponse(user=user, integration=new_integration)
