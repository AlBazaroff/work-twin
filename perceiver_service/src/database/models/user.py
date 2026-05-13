"""Contain user and his related models."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

import uuid6
from sqlalchemy import (
    ForeignKey,
    Enum,
    String,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from database.types import EncryptedJSON
from database.mixins import IDMixin, TimeStampMixin
from database.enums import UserStatus, Integration, IntegrationStatus

if TYPE_CHECKING:
    from .dna import PersonalityDNA
    from .knowledge import KnowledgeSpace


class User(Base, IDMixin, TimeStampMixin):
    """
    User model. Used for store main data about user
    from third-party service for connectivity between them.
    """

    __tablename__ = "perceiver_user"

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, native_enum=False),
        default=UserStatus.UNPAID,
        nullable=False,
    )

    integrations: Mapped[list["UserIntegration"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    personalities: Mapped[list["PersonalityDNA"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    knowledge_namespaces: Mapped[list["KnowledgeSpace"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class UserIntegration(Base, IDMixin, TimeStampMixin):
    """
    User's integration model.
    Show social and another integrations,
    which user provided.
    """

    __tablename__ = "user_integration"

    user_id: Mapped[uuid6.UUID] = mapped_column(
        ForeignKey("perceiver_user.id"),
        index=True,
        nullable=False,
    )
    integration: Mapped[Integration] = mapped_column(
        Enum(Integration, native_enum=False),
        nullable=False,
    )
    integration_user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        index=True,
    )
    credentials: Mapped[dict] = mapped_column(EncryptedJSON)
    status: Mapped[IntegrationStatus] = mapped_column(
        Enum(IntegrationStatus, native_enum=False),
        default=IntegrationStatus.PENDING,
        nullable=False,
    )
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
    )

    user: Mapped["User"] = relationship(back_populates="integrations")

    __table_args__ = (
        UniqueConstraint(
            "integration_user_id",
            "integration",
            name="uq_integration_uid_integration",
        ),
    )
