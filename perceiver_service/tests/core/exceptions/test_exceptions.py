"""Tests for service exception hierarchy."""

import pytest

from core.exception.base import BaseException
from core.exception.providers import (
    ProviderCredentialsNotFoundError,
    ProviderError,
    ProviderNotFoundError,
)


@pytest.fixture
def default_message():
    return "An unexpected error occurred"


@pytest.fixture
def provider():
    return "test-provider"


class TestBaseException:
    def test_default_message(self, default_message):
        """
        Test default message is used
        when no custom message is provided.
        """
        exc = BaseException()
        assert str(exc) == default_message

    def test_custom_message_overrides_default(self):
        """
        Test that providing a custom message overrides the default
        message.
        """
        exc = BaseException("custom failure")
        assert str(exc) == "custom failure"


class TestProviderExceptions:
    """Test provider exception classes and their behavior."""

    def test_provider_not_found_uses_provider_name_as_message(self, provider):
        """
        Test that ProviderNotFoundError formats the message
        with the provider name.
        """
        exc = ProviderNotFoundError(provider)
        assert isinstance(exc, ProviderError)
        assert provider in str(exc)
        assert "not found" in str(exc)

    def test_credentials_not_found(self, provider):
        """
        Test that ProviderCredentialsNotFoundError formats the message
        with the provider name.
        """
        exc = ProviderCredentialsNotFoundError(provider)
        assert provider in str(exc)
        assert "not found" in str(exc)

    def test_provider_errors_inherit_from_base(self):
        """
        Test that provider exceptions inherit from BaseException
        """
        with pytest.raises(ProviderError):
            raise ProviderNotFoundError("unknown")
