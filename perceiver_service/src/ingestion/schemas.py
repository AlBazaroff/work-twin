from uuid import UUID

from pydantic import BaseModel, Field

from database.enums import Integration, UserStatus


class BaseCredentials(BaseModel):
    """Base credentials for all providers."""

    pass


class UserIntegrationTaskPayload(BaseModel):
    """Schema for user integrations data.

    Args:
        user_id: user's id from another service
        integration: service for integration

    """

    user_id: UUID
    integration: Integration
    status: UserStatus = Field(default=UserStatus.UNPAID)
    credentials: BaseCredentials


class IntegrationDataAnalysisTaskPayload(BaseModel):
    """Schema for user integrations data analysis task."""

    integration_id: UUID
