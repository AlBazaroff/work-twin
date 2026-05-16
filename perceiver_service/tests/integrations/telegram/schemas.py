"""Tests for telegram integrations schemas."""

import pytest
from pydantic import ValidationError

from src.integrations.telegram.schemas import TelegramCredentials
from src.database.enums import Integration


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
