"""Exceptions for working with providers."""

from .base import BaseException


class ProviderError(BaseException):
    """Base exception for all provider-related errors."""

    pass


class ProviderNotFoundError(ProviderError):
    """Raised when a provider is not found."""

    message = "Provider '{0}' not found"

    def __init__(self, provider_name: str):
        super().__init__(self.message.format(provider_name))


class ProviderCredentialsNotFoundError(ProviderError):
    """Raised when provider credentials are not found."""

    message = "Credentials for provider '{0}' not found"

    def __init__(self, provider_name: str):
        super().__init__(self.message.format(provider_name))
