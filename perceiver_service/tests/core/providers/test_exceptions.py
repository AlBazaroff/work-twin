"""Test provider's exceptions."""

import pytest

from core.factory.exceptions import EntityNotFoundError
from core.providers.exceptions import (
    ProviderCredentialsNotFoundError,
    ProviderNotFoundError,
)


@pytest.fixture
def provider():
    return "test-provider"


class TestProviderExceptions:
    """Test provider exception classes and their behavior."""

    def test_provider_not_found_uses_provider_name_as_message(self, provider):
        """
        Test that ProviderNotFoundError formats the message
        with the provider name.
        """
        exc = ProviderNotFoundError(provider)
        assert isinstance(exc, EntityNotFoundError)
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
        with pytest.raises(EntityNotFoundError):
            raise ProviderNotFoundError("unknown")
