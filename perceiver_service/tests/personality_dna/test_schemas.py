"""Test schemas for personality DNA."""

import pytest
from pydantic import ValidationError

from personality_dna.schemas import BasePersonalityDNA, PersonalityDNAResponse


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
