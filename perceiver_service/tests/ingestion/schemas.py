"""Tests for ingestion Pydantic schemas."""

import json

import pytest
from pydantic import ValidationError
from uuid6 import uuid7

from src.database.enums import Integration, UserStatus
from src.ingestion.schemas import (
    IntegrationDataAnalysisTaskPayload,
    UserIntegrationTaskPayload,
)
from src.integrations.telegram.schemas import TelegramCredentials


@pytest.fixture
def uuid():
    """Generate a random UUID for testing."""
    return uuid7()


@pytest.fixture
def valid_user_integration_data(uuid, valid_tg_session_string):
    return {
        "user_id": uuid,
        "integration": Integration.TELEGRAM,
        "credentials": TelegramCredentials(
            session_string=valid_tg_session_string
        ),
    }


class TestUserIntegrationTaskPayload:
    def test_defaults_status_to_unpaid(self, valid_user_integration_data):
        """If status is not provided, it should default to UNPAID."""
        payload = UserIntegrationTaskPayload(**valid_user_integration_data)
        assert payload.status == UserStatus.UNPAID

    def test_accepts_explicit_status(self, valid_user_integration_data):
        """If status is provided, it should be set correctly."""
        valid_user_integration_data.update({"status": UserStatus.PAID})
        payload = UserIntegrationTaskPayload(**valid_user_integration_data)
        assert payload.status == UserStatus.PAID

    def test_invalid_user_id_raises(self, valid_tg_session_string):
        """If user_id is not a valid UUID, validation should fail."""
        with pytest.raises(ValidationError):
            UserIntegrationTaskPayload(
                user_id="not-a-uuid",
                integration=Integration.TELEGRAM,
                credentials=TelegramCredentials(
                    session_string=valid_tg_session_string
                ),
            )

    def test_required_fields_enforced(self):
        """If required fields are missing, validation should fail."""
        with pytest.raises(ValidationError):
            UserIntegrationTaskPayload()


class TestIntegrationDataAnalysisTaskPayload:
    def test_requires_integration_id(self, uuid):
        """
        Test that required field
        integration_id is enforced by validation.
        """
        integration_id = uuid
        payload = IntegrationDataAnalysisTaskPayload(
            integration_id=integration_id
        )
        assert payload.integration_id == integration_id

    def test_json_can_be_used_by_celery_tasks(self, uuid):
        """Test that the payload can be deserialized from JSON."""
        integration_id = uuid
        raw = json.dumps({"integration_id": str(integration_id)})
        payload = IntegrationDataAnalysisTaskPayload.model_validate_json(raw)
        assert payload.integration_id == integration_id
