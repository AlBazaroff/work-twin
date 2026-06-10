"""Tests  exceptions hierarchy."""

import pytest

from core.exception.base import BaseException


@pytest.fixture
def default_message():
    return "An unexpected error occurred"


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
