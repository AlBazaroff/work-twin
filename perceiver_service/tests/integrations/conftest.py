"""Configuration for tests in integrations."""

import pytest
from datetime import datetime, timezone
from uuid import UUID

from uuid6 import uuid7

from perceiver_service.src.integrations.enums import (
    Integration,
    IntegrationStatus,
)


@pytest.fixture
def user_id() -> UUID:
    """Returns a random UUID for testing."""
    return uuid7()


@pytest.fixture
def valid_user_integration_create_data(user_id: UUID) -> dict:
    """Returns valid data for UserIntegrationCreate schema."""
    return {
        "user_id": user_id,
        "integration": Integration.TELEGRAM,
        "credentials": {"session_string": "123"},
        "status": IntegrationStatus.ACTIVE,
        "integration_user_id": "telegram_user_123",
        "last_synced_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def valid_user_integration_update_data(user_id: UUID) -> dict:
    """Returns valid data for UserIntegrationUpdate schema."""
    return {
        "id": uuid7(),
        "user_id": user_id,
        "integration": Integration.SLACK,
        "credentials": {"token": "xoxb-some-token"},
        "status": IntegrationStatus.INACTIVE,
    }
