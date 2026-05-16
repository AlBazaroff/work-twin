"""Tests for ProviderFactory registration and resolution."""

from unittest.mock import MagicMock, patch

import pytest

from src.core.exceptions.providers import ProviderNotFoundError
from src.core.providers.base import BaseProvider
from src.core.providers.factory import ProviderFactory
from src.database.enums import Integration
from src.ingestion.schemas import BaseCredentials
from src.integrations.telegram.providers import TelegramProvider


class TestProviderFactory:
    def test_get_provider_returns_telegram_instance(self):
        """Test for getting existing provider from factory."""
        provider = ProviderFactory.get_provider(Integration.TELEGRAM)
        assert isinstance(provider, TelegramProvider)

    def test_get_provider_raises_for_unregistered_integration(self):
        """
        Raise ProviderNotFoundError
        if provider unregistered in factory.
        Works if we have unregistered integrations in
        our Enum Integration.
        """
        with pytest.raises(ProviderNotFoundError) as exc_info:
            ProviderFactory.get_provider(Integration.SLACK)
        assert str(exc_info.value) == Integration.SLACK.value

    def test_register_adds_custom_provider(self):
        """
        Test register new providers internally in the ProviderFactory.
        """

        class StubProvider(BaseProvider):
            provider = Integration.SLACK

            @classmethod
            def from_settings(cls, settings):
                return cls()

            async def get_identity(self, credentials: BaseCredentials):
                return "stub-id"

        ProviderFactory.register(StubProvider)
        try:
            provider = ProviderFactory.get_provider(Integration.SLACK)
            assert isinstance(provider, StubProvider)
        finally:
            ProviderFactory._providers.pop(Integration.SLACK.value, None)

    @patch.object(TelegramProvider, "from_settings")
    def test_get_provider_uses_from_settings(self, mock_from_settings):
        """
        Test that ProviderFactory.get_provider calls the from_settings
        method of the provider class to create an instance.
        """
        mock_instance = MagicMock(spec=TelegramProvider)
        mock_from_settings.return_value = mock_instance

        result = ProviderFactory.get_provider(Integration.TELEGRAM)

        mock_from_settings.assert_called_once()
        assert result is mock_instance
