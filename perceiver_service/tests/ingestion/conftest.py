"""Specific configs for ingestion."""

from datetime import datetime, timezone

import pytest
from uuid6 import uuid7

from integrations.enums import Integration
from ingestion.schemas import UserIntegrationTaskPayload
from integrations.telegram.schemas import TelegramCredentials


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
        credentials=TelegramCredentials(session_string=session_string),
        updated_at=datetime.now(timezone.utc),
    )
