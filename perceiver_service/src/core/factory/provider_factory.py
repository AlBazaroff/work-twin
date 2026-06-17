from typing import Type

from config import get_settings
from core.providers.exceptions import ProviderNotFoundError
from core.providers.base import BaseProvider
from integrations.enums import Integration
from integrations.telegram.providers import TelegramProvider
from .base import RegistryFactory

settings = get_settings()


class ProviderFactory(RegistryFactory):
    """Factory for creating provider instances based on provider name."""

    _registry: dict[Integration, Type[BaseProvider]] = {
        Integration.TELEGRAM: TelegramProvider,
    }

    @classmethod
    def register(
        cls,
        entity_cls: Type[BaseProvider],
        entity_key: Integration,
        *args,
        **kwargs,
    ):
        """Register new provider class in registry.

        Args:
            entity_cls: class of provider
            entity_key: registered Integration
        """
        cls._registry[entity_key] = entity_cls

    @classmethod
    def get_entity(cls, entity: Integration, *args, **kwargs) -> BaseProvider:
        """Return provider by integration from registry.

        Args:
            entity: existing provider in Integration
        """
        if entity not in cls._registry:
            raise ProviderNotFoundError(entity.value)
        result = cls._registry[entity].from_settings(settings)
        return result
