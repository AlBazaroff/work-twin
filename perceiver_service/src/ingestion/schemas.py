from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from database.enums import Integration, UserStatus
from database.models.user import User, UserIntegration


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


class UserIntegrationResponse(BaseModel):
    """Schema for user integration response."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: User
    integration: UserIntegration
