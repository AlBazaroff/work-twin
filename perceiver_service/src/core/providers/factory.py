from typing import Type

from config import settings
from core.exceptions.providers import ProviderNotFoundError
from database.enums import Integration
from integrations.telegram.providers import TelegramProvider
from .base import BaseProvider


class ProviderFactory:
    """Factory for creating provider instances based on provider name."""

    _providers: dict[str, Type[BaseProvider]] = {
        Integration.TELEGRAM.value: TelegramProvider,
    }

    @classmethod
    def register(cls, provider_cls: Type[BaseProvider]):
        cls._providers[provider_cls.provider.value] = provider_cls

    @classmethod
    def get_provider(cls, provider: Integration) -> BaseProvider:
        if provider.value not in cls._providers:
            raise ProviderNotFoundError(provider.value)
        provider = cls._providers[provider.value].from_settings(settings)
        return provider
