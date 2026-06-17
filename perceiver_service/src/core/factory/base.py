"""Base factory classes."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Type, TypeVar, Generic

K = TypeVar("K", bound=Enum)
V = TypeVar("V")


class BaseFactory(ABC):
    pass


class RegistryFactory(BaseFactory, ABC, Generic[K, V]):
    """Factory with register pattern."""

    _registry: dict[K, V]

    @classmethod
    @abstractmethod
    def register(cls, entity_cls: Type, entity_key, *args, **kwargs):
        """Method for register new entities."""
        pass

    @classmethod
    @abstractmethod
    def get_entity(cls, entity, *args, **kwargs):
        pass
