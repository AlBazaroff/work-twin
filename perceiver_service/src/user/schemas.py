"""Schemas to work with user."""

from uuid import UUID

from pydantic import BaseModel, Field

from .enums import UserStatus


class BaseUser(BaseModel):
    """Base User schema."""

    id: UUID


class DefaultUserFieldsMixin(BaseModel):
    """Default fields for User."""

    status: UserStatus | None = Field(default=None)


class UserCreate(BaseUser, DefaultUserFieldsMixin):
    """Schema for creating User."""

    pass


class UserUpdate(BaseUser, DefaultUserFieldsMixin):
    """Schema for updating User."""

    pass
