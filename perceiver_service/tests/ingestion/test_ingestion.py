"""Tests for IngestionService user integration flow."""

from unittest.mock import AsyncMock, patch

import pytest

from core.providers.exceptions import ProviderNotFoundError
from integrations.enums import Integration
from integrations.models import UserIntegration
from ingestion.ingestion import IngestionService


class TestIngestionService:
    @pytest.mark.asyncio
    @pytest.mark.asyncio
    @patch("ingestion.ingestion.get_or_create_user")
    @patch("ingestion.ingestion.create_or_update_integration")
    @patch("ingestion.ingestion.ProviderFactory.get_entity")
    async def test_pass_user_integration_data_with_none_identity(
        self,
        mock_get_provider,
        mock_create_or_update,
        mock_get_or_create_user,
        mock_session,
        user_integration_payload,
    ):
        """
        Test that pass_user_integration_data creates an integration
        even if get_identity returns None.
        """
        session, user = mock_session
        mock_provider = AsyncMock()
        mock_provider.get_identity = AsyncMock(return_value=None)
        mock_get_provider.return_value = mock_provider
        mock_get_or_create_user.return_value = user

        async def fake_create_or_update(
            *, db_session, integration_in, updated_at=None
        ):
            integration = UserIntegration(
                user_id=user_integration_payload.user_id,
                integration=user_integration_payload.integration,
                integration_user_id=None,
                credentials=user_integration_payload.credentials.model_dump(
                    exclude_unset=True
                ),
            )
            return integration

        mock_create_or_update.side_effect = fake_create_or_update

        service = IngestionService(session)
        response = await service.pass_user_integration_data(
            user_integration_payload
        )

        assert response.integration.integration_user_id is None

    @pytest.mark.asyncio
    @patch("ingestion.ingestion.get_or_create_user")
    @patch("ingestion.ingestion.create_or_update_integration")
    @patch("ingestion.ingestion.ProviderFactory.get_entity")
    async def test_pass_user_integration_data_creates_integration(
        self,
        mock_get_provider,
        mock_create_or_update,
        mock_get_or_create_user,
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
        mock_get_or_create_user.return_value = user

        async def fake_create_or_update(
            *, db_session, integration_in, updated_at=None
        ):
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

    @patch("ingestion.ingestion.get_or_create_user")
    @patch("ingestion.ingestion.ProviderFactory.get_entity")
    async def test_propagates_provider_not_found(
        self,
        mock_get_provider,
        mock_get_or_create_user,
        mock_session,
        user_integration_payload,
    ):
        """
        Test pass_user_integration_data propagates
        ProviderNotFoundError.
        """
        session, user = mock_session
        mock_get_or_create_user.return_value = user
        mock_get_provider.side_effect = ProviderNotFoundError("slack")

        service = IngestionService(session)
        with pytest.raises(ProviderNotFoundError):
            await service.pass_user_integration_data(user_integration_payload)

        session.commit.assert_not_awaited()
