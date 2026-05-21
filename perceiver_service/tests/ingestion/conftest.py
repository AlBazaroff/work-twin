"""Specific configs for ingestion."""

import pytest
from uuid6 import uuid7

from integrations.enums import Integration
from ingestion.schemas import UserIntegrationTaskPayload
from integrations.telegram.schemas import TelegramCredentials
from user.enums import UserStatus


@pytest.fixture
def user_id():
    return uuid7()


@pytest.fixture
def session_string():
    return "test_session_string"


@pytest.fixture
def user_integration_payload(user_id, session_string):
    """Provide a sample UserIntegrationTaskPayload for testing."""
    return UserIntegrationTaskPayload(
        user_id=user_id,
        integration=Integration.TELEGRAM,
        status=UserStatus.PAID,
        credentials=TelegramCredentials(session_string=session_string),
    )
