"""Base factory classes."""

from abc import ABC, abstractmethod
from typing import Type


class BaseFactory(ABC):
    pass


class RegistryFactory(BaseFactory, ABC):
    """Factory with register pattern."""

    _registry: dict[str, Type]

    @classmethod
    @abstractmethod
    def register(cls, entity_cls: Type, entity_key, *args, **kwargs):
        """Method for register new entities."""
        pass

    @classmethod
    @abstractmethod
    def get_entity(cls, entity, *args, **kwargs):
        pass
