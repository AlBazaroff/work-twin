"""Tests for Telegram integration exceptions."""

import pytest
from uuid6 import uuid7

from integrations.exceptions import BaseUserNotAuthorized
from integrations.telegram.exceptions import TelegramUserNotAuthorized


@pytest.fixture
def user_id():
    return str(uuid7())


class TestTelegramUserNotAuthorized:
    """Test TelegramUserNotAuthorized message formatting."""

    def test_inherits_from_base_user_not_authorized(self):
        """Test telegram auth error uses shared integrations base."""
        assert issubclass(TelegramUserNotAuthorized, BaseUserNotAuthorized)

    def test_default_message_without_user(self):
        """Test default template is used when user is omitted."""
        exc = TelegramUserNotAuthorized()
        assert str(exc) == "[Telegram] User {user} is not authorized"

    def test_message_with_user(self, user_id):
        """Test user_id is formatted into the default template."""
        exc = TelegramUserNotAuthorized(user=user_id)
        assert str(exc) == f"[Telegram] User {user_id} is not authorized"

    def test_custom_message_overrides_template(self, user_id):
        """Test explicit message bypasses user_id formatting."""
        msg = "Custom auth failure"
        exc = TelegramUserNotAuthorized(
            user=user_id,
            message=msg,
        )
        assert str(exc) == msg

    def test_reason_appended_to_message(self, user_id):
        """Test reason is included via BaseUserNotAuthorized.__str__."""
        reason = "revoked"
        exc = TelegramUserNotAuthorized(user=user_id, reason=reason)
        assert str(exc) == (
            f"[Telegram] User {user_id} is not authorized (Reason {reason})"
        )

    def test_raises_as_exception(self, user_id):
        """Test exception can be raised and caught by base type."""
        with pytest.raises(BaseUserNotAuthorized):
            raise TelegramUserNotAuthorized(user=user_id)
