"""Tests for integration authorization exceptions."""

import pytest

from core.exception.base import BaseException
from integrations.exceptions import BaseUserNotAuthorized


@pytest.fixture
def msg():
    return "User is not authorized"


class TestBaseUserNotAuthorized:
    """Test BaseUserNotAuthorized formatting and inheritance."""

    def test_inherits_from_base_exception(self):
        """Test that auth errors inherit from service BaseException."""
        assert issubclass(BaseUserNotAuthorized, BaseException)

    def test_message_without_reason(self, msg):
        """Test that the base message is returned when no reason is set."""
        exc = BaseUserNotAuthorized()
        exc.message = msg
        exc.reason = None
        assert str(exc) == msg

    def test_message_with_reason(self, msg):
        """Test that reason is appended to the message in __str__."""
        reason = "session expired"
        exc = BaseUserNotAuthorized()
        exc.message = msg
        exc.reason = reason
        assert str(exc) == f"{msg} (Reason {reason})"
