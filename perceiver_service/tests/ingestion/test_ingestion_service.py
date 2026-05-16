"""Tests for IngestionService user integration flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from uuid6 import uuid7

from src.database.enums import Integration, UserStatus
from src.database.models.user import User
from src.ingestion.schemas import UserIntegrationTaskPayload
from src.ingestion.services import IngestionService
from src.integrations.telegram.schemas import TelegramCredentials


@pytest.fixture
def user_id():
    return uuid7()


@pytest.fixture
def mock_session(user_id):
    """Create a mock AsyncSession with a user already in the db."""
    session = AsyncMock()
    user = User(id=user_id, status=UserStatus.UNPAID)
    result = MagicMock()
    result.scalar_one.return_value = user
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()
    return session, user


@pytest.fixture
def payload(user_id):
    """Provide a sample UserIntegrationTaskPayload for testing."""
    return UserIntegrationTaskPayload(
        user_id=user_id,
        integration=Integration.TELEGRAM,
        status=UserStatus.PAID,
        credentials=TelegramCredentials(session_string="sess"),
    )


class TestIngestionService:
    @pytest.mark.asyncio
    async def test_get_or_create_user_executes_upsert(self, mock_session):
        """
        Test that get_or_create_user executes upsert
        and returns user.
        """
        session, user = mock_session
        service = IngestionService(session)

        result = await service._get_or_create_user(
            user.id, UserStatus.DEACTIVATED
        )

        session.execute.assert_awaited_once()
        assert result is user

    @pytest.mark.asyncio
    @patch("src.ingestion.services.ProviderFactory.get_provider")
    async def test_pass_user_integration_data_creates_integration(
        self, mock_get_provider, mock_session, payload
    ):
        """
        Test that pass_user_integration_data creates a new integration
        and commits the session.
        """
        session, user = mock_session
        mock_provider = AsyncMock()
        mock_provider.get_identity = AsyncMock(return_value="12345")
        mock_get_provider.return_value = mock_provider

        service = IngestionService(session)
        response = await service.pass_user_integration_data(payload)

        mock_get_provider.assert_called_once_with(Integration.TELEGRAM)
        mock_provider.get_identity.assert_awaited_once_with(
            payload.credentials
        )
        session.execute.assert_awaited_once()
        session.commit.assert_awaited_once()

        assert response.user is user
        assert len(user.integrations) == 1
        integration = response.integration
        assert integration.integration == Integration.TELEGRAM
        assert integration.integration_user_id == "12345"
        assert integration.credentials == payload.credentials

    @pytest.mark.asyncio
    @patch("src.ingestion.services.ProviderFactory.get_provider")
    async def test_propagates_provider_not_found(
        self, mock_get_provider, mock_session, payload
    ):
        """
        Test pass_user_integration_data propagates
        ProviderNotFoundError.
        """
        from src.core.exceptions.providers import ProviderNotFoundError

        session, _user = mock_session
        mock_get_provider.side_effect = ProviderNotFoundError("slack")

        service = IngestionService(session)
        with pytest.raises(ProviderNotFoundError):
            await service.pass_user_integration_data(payload)

        session.commit.assert_not_awaited()
