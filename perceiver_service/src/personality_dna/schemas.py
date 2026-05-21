"""Schemas for twin-related operations."""

from pydantic import BaseModel, Field


class BasePersonalityDNA(BaseModel):
    """Schema for Personality DNA."""

    style_markers: dict = Field(...)


class PersonalityDNAResponse(BasePersonalityDNA):
    """Schema for Personality DNA for common responses."""

    core_facts: dict | None = Field(default=None)
    preferences: dict | None = Field(default=None)

    model_config = {"from_attributes": True, "extra": "ignore"}
