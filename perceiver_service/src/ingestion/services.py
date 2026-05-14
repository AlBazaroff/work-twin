import logging
from uuid import UUID

from database.core import AsyncSession
from database.models.user import User, UserIntegration
from ingestion.schemas import UserIntegrationTaskPayload

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for ingest user data from third party service."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_create_user(self, user_id: UUID) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            user = User(id=user_id)
            self.session.add(user)
            logger.info(f"Created new User: {user_id}")
        return user

    async def pass_user_integration_data(
        self, payload: UserIntegrationTaskPayload
    ):
        """Pass user integration data from payload."""
        user_id = payload.user_id
        user: User = await self._get_or_create_user(user_id)

        # get integration_user_id

        new_integration = UserIntegration(
            integration=payload.integration,
            credentials=payload.credentials,
        )
        user.integrations.append(new_integration)
        logger.info(
            f"Added new integration: {payload.integration} for user: {user_id}"
        )

        # celery tasks for analyze

        await self.session.commit()
