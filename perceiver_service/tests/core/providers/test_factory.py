"""Tests for ProviderFactory registration and resolution."""

from unittest.mock import MagicMock, patch

import pytest

from core.providers.base import BaseProvider
from core.providers.exceptions import ProviderNotFoundError
from core.factory.provider_factory import ProviderFactory
from integrations.enums import Integration
from ingestion.schemas import BaseCredentials
from integrations.telegram.providers import TelegramProvider


class TestProviderFactory:
    def test_get_entity_returns_telegram_instance(self):
        """Test for getting existing provider from factory."""
        provider = ProviderFactory.get_entity(Integration.TELEGRAM)
        assert isinstance(provider, TelegramProvider)

    def test_get_entity_raises_for_unregistered_integration(self):
        """
        Raise ProviderNotFoundError
        if provider unregistered in factory.
        Works if we have unregistered integrations in
        our Enum Integration.
        """
        with pytest.raises(ProviderNotFoundError) as exc_info:
            ProviderFactory.get_entity(Integration.SLACK)
        assert (
            str(exc_info.value)
            == f"Provider '{Integration.SLACK.value}' not found"
        )

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

        ProviderFactory.register(StubProvider, StubProvider.provider)
        try:
            provider = ProviderFactory.get_entity(Integration.SLACK)
            assert isinstance(provider, StubProvider)
        finally:
            ProviderFactory._registry.pop(Integration.SLACK.value, None)

    @patch.object(TelegramProvider, "from_settings")
    def test_get_entity_uses_from_settings(self, mock_from_settings):
        """
        Test that ProviderFactory.get_entity calls the from_settings
        method of the provider class to create an instance.
        """
        mock_instance = MagicMock(spec=TelegramProvider)
        mock_from_settings.return_value = mock_instance

        result = ProviderFactory.get_entity(Integration.TELEGRAM)

        mock_from_settings.assert_called_once()
        assert result is mock_instance
