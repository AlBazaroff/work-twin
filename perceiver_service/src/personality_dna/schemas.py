"""Schemas for twin-related operations."""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class BasePersonalityDNA(BaseModel):
    """Schema for Personality DNA."""

    style_markers: Optional[dict] = Field(...)


class PersonalityDNAResponse(BasePersonalityDNA):
    """Schema for Personality DNA for common responses."""

    core_facts: Optional[dict] = Field(default=None)
    preferences: Optional[dict] = Field(default=None)
    version: Optional[int] = Field(default=None)

    model_config = {"from_attributes": True, "extra": "ignore"}


class PersonalityDNACreate(BasePersonalityDNA):
    """Schema for creating Personality DNA."""

    user_id: UUID
    style_markers: Optional[dict] = Field(default=None)
    core_facts: Optional[dict] = Field(default=None)
    preferences: Optional[dict] = Field(default=None)
    version: int
    is_active: bool = True


class BasePersonalityDNAUpdate(BaseModel):
    """Base schema for updating Personality DNA."""

    style_markers: Optional[dict] = Field(default=None)
    core_facts: Optional[dict] = Field(default=None)
    preferences: Optional[dict] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)


class PersonalityDNAUpdate(BasePersonalityDNAUpdate):
    """Schema for updating Personality DNA."""

    id: UUID


class ActivePersonalityDNAUpdate(BasePersonalityDNAUpdate):
    """Schema for updating active Personality DNA by user ID."""

    user_id: UUID
