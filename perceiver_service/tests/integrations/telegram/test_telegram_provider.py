"""Tests for TelegramProvider identity and credentials handling."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from config import settings
from core.exceptions.providers import ProviderCredentialsNotFoundError
from database.enums import Integration
from integrations.telegram.providers import TelegramProvider
from integrations.telegram.schemas import TelegramCredentials


@pytest.fixture
def provider():
    return TelegramProvider(api_id=1, api_hash="test_hash")


class TestTelegramProviderFromSettings:
    """Test the from_settings classmethod of TelegramProvider."""

    def test_from_settings_maps_telegram_config(self):
        """
        Test telegram provider is correctly created from settings
        from environment variables.
        """
        instance = TelegramProvider.from_settings(settings)
        assert instance._api_id == settings.telegram.api_id
        assert instance._api_hash == settings.telegram.api_hash
        assert isinstance(instance, TelegramProvider)


class TestTelegramProviderGetIdentity:
    """Test the get_identity method of TelegramProvider."""

    @pytest.mark.asyncio
    async def test_raises_when_session_string_empty(self, provider):
        """
        Test that NotFound error is raised
        when session string is empty.
        """
        credentials = TelegramCredentials.model_construct(session_string="")
        with pytest.raises(ProviderCredentialsNotFoundError):
            await provider.get_identity(credentials)

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_returns_telegram_user_id_as_string(
        self, mock_session_cls, mock_client_cls, provider
    ):
        """
        Test that get_identity find user's Telegram ID.
        """
        mock_me = MagicMock()
        mock_me.id = 123456
        mock_client = AsyncMock()
        mock_client.get_me = AsyncMock(return_value=mock_me)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_cls.return_value = mock_client
        identity = await provider.get_identity(
            TelegramCredentials(session_string="valid_session")
        )

        assert identity == "123456"
        mock_session_cls.assert_called_once_with("valid_session")
        mock_client_cls.assert_called_once()
        mock_client.get_me.assert_awaited_once()

    def test_provider_enum_is_telegram(self, provider):
        """Test that provider is correct."""
        assert provider.provider == Integration.TELEGRAM
