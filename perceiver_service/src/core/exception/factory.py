"""Exceptions for basic factory errors."""

from .base import BaseException


class EntityError(BaseException):
    """Base exception for entity-related errors in
    registry factories.
    """

    pass


class EntityNotFoundError(EntityError):
    """Raise, when an entity not found in registry."""

    entity_name: str
    _template: str = "{entity_name} '{name}' not found"

    def __init__(self, name: str):
        self.message = self._template.format(
            entity_name=self.entity_name,
            name=name,
        )
        super().__init__(self.message)
