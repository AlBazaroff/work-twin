"""Tests for integrations schemas."""

import pytest
from uuid import UUID

from pydantic import ValidationError
from uuid6 import uuid7

from perceiver_service.src.integrations.enums import (
    Integration,
)
from perceiver_service.src.integrations.schemas import (
    UserIntegrationCreate,
    UserIntegrationUpdate,
)


class TestUserIntegrationCreate:
    """Tests for UserIntegrationCreate schema."""

    def test_creation_success(self, valid_user_integration_create_data: dict):
        """Test successful creation with valid data."""
        schema = UserIntegrationCreate(**valid_user_integration_create_data)

        assert schema.user_id == valid_user_integration_create_data["user_id"]
        assert (
            schema.integration
            == valid_user_integration_create_data["integration"]
        )

    def test_creation_with_minimal_data(
        self, valid_user_integration_create_data: dict
    ):
        """Test successful creation with only required fields."""
        minimal_data = {
            "user_id": valid_user_integration_create_data["user_id"],
            "integration": valid_user_integration_create_data["integration"],
            "credentials": valid_user_integration_create_data["credentials"],
        }
        schema = UserIntegrationCreate(**minimal_data)

        assert schema.status is None  # Default value
        assert schema.integration_user_id is None
        assert schema.last_synced_at is None

    def test_missing_required_fields(self):
        """Test failure when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            UserIntegrationCreate(
                integration=Integration.TELEGRAM,
                credentials={"api_id": 123, "api_hash": "some_hash"},
            )
        assert "user_id" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            UserIntegrationCreate(
                user_id=uuid7(),
                credentials={"api_id": 123, "api_hash": "some_hash"},
            )
        assert "integration" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            UserIntegrationCreate(
                user_id=uuid7(), integration=Integration.TELEGRAM
            )
        assert "credentials" in str(exc_info.value)

    def test_invalid_field_types(self, user_id: UUID):
        """Test failure with incorrect data types for fields."""
        with pytest.raises(ValidationError):
            UserIntegrationCreate(
                user_id="not-a-uuid",  # type: ignore
                integration=Integration.TELEGRAM,
                credentials={"api_id": 123, "api_hash": "some_hash"},
            )

        with pytest.raises(ValidationError):
            UserIntegrationCreate(
                user_id=user_id,
                integration="NOT_AN_INTEGRATION",  # type: ignore
                credentials={"api_id": 123, "api_hash": "some_hash"},
            )

        with pytest.raises(ValidationError):
            UserIntegrationCreate(
                user_id=user_id,
                integration=Integration.TELEGRAM,
                credentials="not-a-dict",  # type: ignore
            )


class TestUserIntegrationUpdate:
    """Tests for UserIntegrationUpdate schema."""

    def test_successful_update(self, valid_user_integration_update_data: dict):
        """Test successful update with valid data."""
        schema = UserIntegrationUpdate(**valid_user_integration_update_data)

        assert schema.user_id == valid_user_integration_update_data["user_id"]
        assert (
            schema.integration
            == valid_user_integration_update_data["integration"]
        )
        assert (
            schema.credentials
            == valid_user_integration_update_data["credentials"]
        )
        assert schema.status == valid_user_integration_update_data["status"]

    def test_update_partial_success(
        self, user_id: UUID, valid_user_integration_update_data: dict
    ):
        """Test successful update with only a subset of optional fields."""
        minimal_update_data = {
            "id": valid_user_integration_update_data["id"],
            "user_id": user_id,
            "integration": Integration.SLACK,
        }
        schema = UserIntegrationUpdate(**minimal_update_data)

        assert schema.user_id == minimal_update_data["user_id"]
        assert schema.integration == minimal_update_data["integration"]
        assert schema.credentials is None
        assert schema.status is None

        # Test with just credentials
        credentials_only_data = {
            "id": valid_user_integration_update_data["id"],
            "user_id": user_id,
            "credentials": {"token": "another-token"},
        }
        schema = UserIntegrationUpdate(**credentials_only_data)
        assert schema.user_id == credentials_only_data["user_id"]
        assert schema.credentials == credentials_only_data["credentials"]
        assert schema.integration is None
        assert schema.status is None

    def test_invalid_field_types(self, user_id: UUID):
        """Test failure with incorrect data types for optional fields."""
        with pytest.raises(ValidationError):
            UserIntegrationUpdate(
                user_id=user_id,
                integration="NOT_AN_INTEGRATION",  # type: ignore
            )

        with pytest.raises(ValidationError):
            UserIntegrationUpdate(
                user_id=user_id,
                credentials="not-a-dict",  # type: ignore
            )

        with pytest.raises(ValidationError):
            UserIntegrationUpdate(
                user_id="not-a-uuid",  # type: ignore
                integration=Integration.TELEGRAM,
            )
