"""Specific configs for ingestion."""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from uuid6 import uuid7

from integrations.enums import Integration
from ingestion.schemas import UserIntegrationTaskPayload
from integrations.telegram.schemas import TelegramCredentials
from user.models import User
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
        credentials=TelegramCredentials(session_string=session_string),
        updated_at=datetime.now(timezone.utc),
    )


@pytest.fixture
def mock_session(user_id):
    """Create a mock AsyncSession with a user already in the db."""
    session = AsyncMock()
    user = User(id=user_id, status=UserStatus.UNPAID)
    result = MagicMock()
    result.scalar_one.return_value = user
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()
    return session, user
