"""Tests for IngestionService user integration flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from database.enums import Integration, UserStatus
from database.models.user import User
from ingestion.services import IngestionService


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
    @patch("ingestion.services.ProviderFactory.get_entity")
    async def test_pass_user_integration_data_creates_integration(
        self, mock_get_provider, mock_session, user_integration_payload
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
        response = await service.pass_user_integration_data(
            user_integration_payload
        )

        mock_get_provider.assert_called_once_with(Integration.TELEGRAM)
        mock_provider.get_identity.assert_awaited_once_with(
            user_integration_payload.credentials
        )
        session.execute.assert_awaited_once()
        session.commit.assert_awaited_once()

        assert response.user is user
        assert len(user.integrations) == 1
        integration = response.integration
        assert integration.integration == Integration.TELEGRAM
        assert integration.integration_user_id == "12345"
        assert integration.credentials == user_integration_payload.credentials

    @pytest.mark.asyncio
    @patch("ingestion.services.ProviderFactory.get_entity")
    async def test_propagates_provider_not_found(
        self, mock_get_provider, mock_session, user_integration_payload
    ):
        """
        Test pass_user_integration_data propagates
        ProviderNotFoundError.
        """
        from core.exception.providers import ProviderNotFoundError

        session, _user = mock_session
        mock_get_provider.side_effect = ProviderNotFoundError("slack")

        service = IngestionService(session)
        with pytest.raises(ProviderNotFoundError):
            await service.pass_user_integration_data(user_integration_payload)

        session.commit.assert_not_awaited()
