"""Schemas for integrations."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import Integration, IntegrationStatus


class BaseCredentials(BaseModel):
    """Base credentials for all providers."""

    pass


class BaseUserIntegration(BaseModel):
    """Base schema for UserIntegration."""

    user_id: UUID
    integration: Integration
    credentials: dict
    status: IntegrationStatus | None = Field(default=None)


class DefaultFieldsMixin(BaseModel):
    """Mixin with default fields in UserIntegration."""

    integration_user_id: str | None = Field(default=None)
    last_synced_at: datetime | None = Field(default=None)


class UserIntegrationCreate(BaseUserIntegration, DefaultFieldsMixin):
    """Schema for create new UserIntegration."""

    pass


class UserIntegrationUpdate(BaseUserIntegration, DefaultFieldsMixin):
    """Schema for update UserIntegration."""

    id: UUID
    integration: Integration | None = Field(None)
    credentials: dict | None = Field(None)
    status: IntegrationStatus | None = Field(None)
