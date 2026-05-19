"""Exceptions for working with providers."""

from core.exception.base import BaseException
from core.exception.factory import EntityNotFoundError


class ProviderNotFoundError(EntityNotFoundError):
    """Raised when a provider is not found."""

    entity_name = "Provider"


class ProviderCredentialsNotFoundError(BaseException):
    """Raised when provider credentials are not found."""

    _template = "Credentials for provider '{0}' not found"

    def __init__(self, provider_name: str):
        self.message = self._template.format(provider_name)
        super().__init__(self.message)
