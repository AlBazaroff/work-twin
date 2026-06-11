"""Tests for telegram integrations schemas."""

import pytest
from pydantic import ValidationError

from integrations.enums import Integration
from integrations.telegram.schemas import TelegramCredentials, TelegramMessage


@pytest.fixture
def valid_user_integration_data(uuid, valid_tg_session_string):
    return {
        "user_id": uuid,
        "integration": Integration.TELEGRAM,
        "credentials": TelegramCredentials(
            session_string=valid_tg_session_string
        ),
    }


class TestTelegramCredentials:
    def test_requires_session_string(self, valid_tg_session_string):
        """
        Test that required field session_string is enforced by validation.
        """
        credentials = TelegramCredentials(
            session_string=valid_tg_session_string
        )
        assert credentials.session_string == valid_tg_session_string

    def test_type_validation(self):
        """Test that session_string must be a string."""
        with pytest.raises(ValidationError):
            TelegramCredentials(session_string=123)  # type: ignore

    def test_empty_session_string_raises(self):
        """If session string is empty, validation should fail."""
        with pytest.raises(ValidationError):
            TelegramCredentials(session_string="")

    def test_missing_session_string_raises(self):
        """
        If credentials are missing required fields,
        validation should fail.
        """
        with pytest.raises(ValidationError):
            TelegramCredentials()  # type: ignore


class TestTelegramMessage:
    def test_validation_success(self):
        """Test successful instantiation with valid data."""
        data = {
            "message_id": 1,
            "text": "Hello",
            "date": "2026-06-11T12:00:00",
            "me": True,
            "reply_to": 0,
        }
        message = TelegramMessage(**data)
        assert message.message_id == 1
        assert message.text == "Hello"

    def test_validation_failure(self):
        """Test validation failure with missing necessary fields."""
        with pytest.raises(ValidationError):
            TelegramMessage(message_id=1, text="Hello")
