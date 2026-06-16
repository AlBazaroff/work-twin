from uuid import UUID
from typing import Union
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from integrations.enums import Integration
from integrations.models import UserIntegration
from integrations.telegram.schemas import TelegramCredentials
from user.models import User

CredentialsUnion = Union[TelegramCredentials]


class UserIntegrationTaskPayload(BaseModel):
    """Schema for user integrations data.

    Args:
        user_id: user's id from another service
        integration: service for integration

    """

    user_id: UUID
    integration: Integration
    credentials: CredentialsUnion = Field(..., discriminator="provider")
    updated_at: datetime


class IntegrationDataAnalysisTaskPayload(BaseModel):
    """Schema for user integrations data analysis task."""

    integration_id: UUID


class UserIntegrationResponse(BaseModel):
    """Schema for user integration response."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: User
    integration: UserIntegration | None
