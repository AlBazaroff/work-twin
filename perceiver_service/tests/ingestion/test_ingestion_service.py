"""Tests for IngestionService user integration flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from user.models import User
from integrations.enums import Integration
from integrations.models import UserIntegration
from ingestion.ingestion import IngestionService
from user.enums import UserStatus


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
    @patch("ingestion.ingestion.create_or_update_integration")
    @patch("ingestion.ingestion.ProviderFactory.get_entity")
    @patch("ingestion.ingestion.get_user")
    async def test_pass_user_integration_data_creates_integration(
        self,
        mock_get_user,
        mock_get_provider,
        mock_create_or_update,
        mock_session,
        user_integration_payload,
    ):
        """
        Test that pass_user_integration_data creates a new integration
        and commits the session.
        """
        session, user = mock_session
        # integration = UserIntegration
        mock_provider = AsyncMock()
        mock_provider.get_identity = AsyncMock(return_value="12345")
        mock_get_provider.return_value = mock_provider
        mock_get_user.return_value = user

        async def fake_create_or_update(*, db_session, integration_in):
            await db_session.commit()
            integration = UserIntegration(
                user_id=user_integration_payload.user_id,
                integration=user_integration_payload.integration,
                integration_user_id="12345",
                credentials=user_integration_payload.credentials.model_dump(
                    exclude_unset=True
                ),
            )
            user.integrations.append(integration)
            return integration

        mock_create_or_update.side_effect = fake_create_or_update

        service = IngestionService(session)
        response = await service.pass_user_integration_data(
            user_integration_payload
        )

        mock_get_provider.assert_called_once_with(Integration.TELEGRAM)
        mock_provider.get_identity.assert_awaited_once_with(
            user_integration_payload.user_id,
            user_integration_payload.credentials,
        )
        session.commit.assert_awaited_once()

        assert response.user is user
        assert len(user.integrations) == 1
        integration = response.integration
        assert integration.integration == Integration.TELEGRAM
        assert integration.integration_user_id == "12345"
        assert (
            integration.credentials
            == user_integration_payload.credentials.model_dump(
                exclude_unset=True
            )
        )

    @pytest.mark.asyncio
    @patch("ingestion.ingestion.ProviderFactory.get_entity")
    async def test_propagates_provider_not_found(
        self, mock_get_provider, mock_session, user_integration_payload
    ):
        """
        Test pass_user_integration_data propagates
        ProviderNotFoundError.
        """
        from core.providers.exceptions import ProviderNotFoundError

        session, _user = mock_session
        mock_get_provider.side_effect = ProviderNotFoundError("slack")

        service = IngestionService(session)
        with pytest.raises(ProviderNotFoundError):
            await service.pass_user_integration_data(user_integration_payload)

        session.commit.assert_not_awaited()
