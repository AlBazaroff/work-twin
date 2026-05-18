"""Exceptions for working with providers."""

from .base import BaseException


class ProviderError(BaseException):
    """Base exception for all provider-related errors."""

    pass


class ProviderNotFoundError(ProviderError):
    """Raised when a provider is not found."""

    _template = "Provider '{0}' not found"

    def __init__(self, provider_name: str):
        self.message = self._template.format(provider_name)
        super().__init__(self.message)


class ProviderCredentialsNotFoundError(ProviderError):
    """Raised when provider credentials are not found."""

    _template = "Credentials for provider '{0}' not found"

    def __init__(self, provider_name: str):
        self.message = self._template.format(provider_name)
        super().__init__(self.message)
