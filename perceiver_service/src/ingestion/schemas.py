from uuid import UUID

from pydantic import BaseModel

from database.enums import Integration


class UserIntegrationTaskPayload(BaseModel):
    """Schema for user integrations data.

    Args:
        user_id: user's id from another service
        integration: service for integration

    """

    user_id: UUID
    integration: Integration
    credentials: dict
