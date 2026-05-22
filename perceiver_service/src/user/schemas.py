"""Schemas to work with user."""

from uuid import UUID

from pydantic import BaseModel, Field

from .enums import UserStatus


class BaseUser(BaseModel):
    """Base User schema."""

    id: UUID
    status: UserStatus


class DefaultFieldsMixin(BaseModel):
    """Default fields for User."""

    status: UserStatus | None = Field(None)


class UserCreate(BaseUser, DefaultFieldsMixin):
    """Schema for creating User."""

    pass


class UserUpdate(BaseUser, DefaultFieldsMixin):
    """Schema for updating User."""

    pass
