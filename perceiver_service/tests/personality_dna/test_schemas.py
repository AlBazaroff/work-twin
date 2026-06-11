"""Test schemas for personality DNA."""

import pytest
from pydantic import ValidationError
from uuid6 import uuid7

from personality_dna.schemas import (
    BasePersonalityDNA,
    PersonalityDNAResponse,
    PersonalityDNACreate,
    PersonalityDNAUpdate,
    ActivePersonalityDNAUpdate,
)


class TestBasePersonalityDNA:
    """Test BasePersonalityDNA schema"""

    def test_validate_from_attributes(self, active_personality_dna):
        """Test successful validation from valid attributes."""
        result = BasePersonalityDNA.model_validate(active_personality_dna)

        assert result.style_markers == active_personality_dna["style_markers"]

    def test_failed_with_empty_data(self):
        """Test failing validation without necessary fields."""
        with pytest.raises(ValidationError):
            BasePersonalityDNA()


class TestPersonalityDNAResponse:
    """Test Personality DNA schemas."""

    def test_validate_from_attributes(self, active_personality_dna):
        """Test successful validation from correct attributes."""
        result = PersonalityDNAResponse.model_validate(active_personality_dna)

        assert result.model_dump() == {
            "style_markers": active_personality_dna["style_markers"],
            "core_facts": active_personality_dna["core_facts"],
            "preferences": active_personality_dna["preferences"],
            "version": 1,
        }

    def test_failed_without_attributes(self):
        """Test failing validation without attributes."""
        with pytest.raises(ValidationError):
            PersonalityDNAResponse()

    def test_creation_with_default_values(
        self,
        active_personality_dna,
    ):
        """
        Test successful create model with default values,
        if they're missed.
        """
        result = PersonalityDNAResponse(
            style_markers=active_personality_dna["style_markers"]
        )

        assert result.core_facts is None
        assert result.preferences is None


class TestPersonalityDNACreate:
    """Test PersonalityDNACreate schema."""

    def test_validation_success(self, active_personality_dna):
        """Test successful validation."""
        result = PersonalityDNACreate.model_validate(active_personality_dna)
        assert result.user_id == active_personality_dna["user_id"]
        assert result.is_active is True

    def test_validation_failure(self):
        """Test failure without required fields."""
        with pytest.raises(ValidationError):
            PersonalityDNACreate(version=1)

    def test_default_values_with_minimal_data(self):
        """Test that default values are set correctly."""
        version = 1
        user_id = uuid7()
        data = {
            "user_id": user_id,
            "version": version,
        }
        result = PersonalityDNACreate(**data)

        assert result.user_id == user_id
        assert result.version == version
        assert result.is_active is True


class TestPersonalityDNAUpdate:
    """Test PersonalityDNAUpdate schema."""

    def test_validation_success(self, active_personality_dna):
        """Test successful validation."""
        data = {"id": active_personality_dna["id"], "is_active": False}
        result = PersonalityDNAUpdate.model_validate(data)
        assert result.id == active_personality_dna["id"]
        assert result.is_active is False

    def test_validation_failure(self):
        """Test failure without required fields."""
        with pytest.raises(ValidationError):
            PersonalityDNAUpdate()

    def test_default_values_with_minimal_data(self):
        """Test that default values are set correctly."""
        p_id = uuid7()
        data = {
            "id": p_id,
        }
        result = PersonalityDNAUpdate(**data)

        assert result.id == p_id


class TestActivePersonalityDNAUpdate:
    """Test ActivePersonalityDNAUpdate schema."""

    def test_validation_success(self, active_personality_dna):
        """Test successful validation."""
        data = {
            "user_id": active_personality_dna["user_id"],
            "is_active": False,
        }
        result = ActivePersonalityDNAUpdate.model_validate(data)
        assert result.user_id == active_personality_dna["user_id"]
        assert result.is_active is False

    def test_validation_failure(self):
        """Test failure without required fields."""
        with pytest.raises(ValidationError):
            ActivePersonalityDNAUpdate()

    def test_default_values_with_minimal_data(self):
        """Test that default values are set correctly."""
        user_id = uuid7()
        data = {
            "user_id": user_id,
        }
        result = ActivePersonalityDNAUpdate(**data)

        assert result.user_id == user_id
