from typing import Type

from config import settings
from core.exception.providers import ProviderNotFoundError
from core.providers.base import BaseProvider
from database.enums import Integration
from integrations.telegram.providers import TelegramProvider
from .base import RegistryFactory


class ProviderFactory(RegistryFactory):
    """Factory for creating provider instances based on provider name."""

    _registry: dict[Integration, Type[BaseProvider]] = {
        Integration.TELEGRAM: TelegramProvider,
    }

    @classmethod
    def register(
        cls, provider_cls: Type[BaseProvider], integration: Integration
    ):
        """Register new provider class in registry.

        Args:
            provider_cls: class of provider
        """
        cls._registry[integration] = provider_cls

    @classmethod
    def get_entity(
        cls, provider: Integration, *args, **kwargs
    ) -> BaseProvider:
        """Return provider by integration from registry.

        Args:
            provider: existing provider in Integration
        """
        if provider not in cls._registry:
            raise ProviderNotFoundError(provider.value)
        result = cls._registry[provider].from_settings(settings)
        return result
