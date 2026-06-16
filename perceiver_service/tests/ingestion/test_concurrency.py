import asyncio
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from sqlalchemy import select

from ingestion.ingestion import IngestionService
from ingestion.schemas import UserIntegrationTaskPayload
from integrations.enums import Integration
from integrations.telegram.schemas import TelegramCredentials
from integrations.models import UserIntegration
from tests.conftest import TestSessionLocal
from user.models import User


@pytest.mark.asyncio
async def test_race_condition_create_or_update_integration(
    db_session, user_id
):
    """
    Test that concurrent calls to pass_user_integration_data
    for the same integration do not result in corrupted
    state or errors, and that the latest timestamp wins.
    """
    async with TestSessionLocal() as session:
        user = User(id=user_id)
        session.add(user)
        await session.commit()

    now = datetime.now()
    payload1 = UserIntegrationTaskPayload(
        user_id=user_id,
        integration=Integration.TELEGRAM,
        credentials=TelegramCredentials(session_string="key1"),
        updated_at=now,
    )
    payload2 = UserIntegrationTaskPayload(
        user_id=user_id,
        integration=Integration.TELEGRAM,
        credentials=TelegramCredentials(session_string="key2"),
        updated_at=now + timedelta(seconds=1),
    )

    async def run_ingestion(payload):
        async with TestSessionLocal() as session:
            service = IngestionService(session)
            with patch(
                "ingestion.ingestion.ProviderFactory.get_entity"
            ) as mock_get_provider:
                mock_provider = AsyncMock()
                mock_provider.get_identity = AsyncMock(return_value="12345")
                mock_get_provider.return_value = mock_provider
                return await service.pass_user_integration_data(payload)

    results = await asyncio.gather(
        run_ingestion(payload1),
        run_ingestion(payload2),
        return_exceptions=True,
    )

    for res in results:
        assert not isinstance(res, Exception), f"Ingestion failed with: {res}"

    # Verify final state in DB using a new session
    async with TestSessionLocal() as session:
        final_integration = await session.scalar(
            select(UserIntegration).where(
                UserIntegration.user_id == user_id,
                UserIntegration.integration == Integration.TELEGRAM,
            )
        )

    # The newer payload should have won
    assert final_integration is not None, "Integration record not found"
    assert final_integration.credentials["session_string"] == "key2"


@pytest.mark.asyncio
async def test_race_condition_user_creation(db_engine, user_id):
    """
    Test that concurrent calls to pass_user_integration_data
    for a user that doesn't exist yet do not result in corrupted
    state or errors, and that the user is correctly created.
    """
    integration = Integration.TELEGRAM
    now = datetime.now()

    payload = UserIntegrationTaskPayload(
        user_id=user_id,
        integration=integration,
        credentials=TelegramCredentials(session_string="key1"),
        updated_at=now,
    )

    async def run_ingestion(payload):
        async with TestSessionLocal() as session:
            service = IngestionService(session)
            with patch(
                "ingestion.ingestion.ProviderFactory.get_entity"
            ) as mock_get_provider:
                mock_provider = AsyncMock()
                mock_provider.get_identity = AsyncMock(return_value="12345")
                mock_get_provider.return_value = mock_provider
                return await service.pass_user_integration_data(payload)

    results = await asyncio.gather(
        run_ingestion(payload),
        run_ingestion(payload),
        return_exceptions=True,
    )

    for res in results:
        assert not isinstance(res, Exception), f"Ingestion failed with: {res}"

    # Verify user exists and only one was created
    async with TestSessionLocal() as session:
        stmt = select(User).where(User.id == user_id)
        users = await session.scalars(stmt)
        user_list = users.all()
        assert len(user_list) == 1, f"Expected 1 user, found {len(user_list)}"
