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
from core.database.models.mixins import IDMixin, TimeStampMixin
from core.constants.user import UserStatus, Integrity, IntegrityStatus

if TYPE_CHECKING:
    from .dna import PersonalityDNA
    from .knowledge import KnowledgeSpace


class User(Base, IDMixin, TimeStampMixin):
    """
    User model. Used for store main data about user
    from third-party service for connectivity between them.
    """

    __tablename__ = "user"

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, native_enum=False),
        default=UserStatus.UNPAID,
        nullable=False,
    )

    integrities: Mapped[list["UserIntegrity"]] = relationship(
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


class UserIntegrity(Base, IDMixin, TimeStampMixin):
    """
    User's integrity model.
    Show social and another integrities,
    which user provided.
    """

    __tablename__ = "user_integrity"

    user_id: Mapped[uuid6.UUID] = mapped_column(
        ForeignKey("user.id"),
        index=True,
        nullable=False,
    )
    integrity: Mapped[Integrity] = mapped_column(
        Enum(Integrity, native_enum=False),
        nullable=False,
    )
    integrity_user_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        index=True,
    )
    credentials: Mapped[dict] = mapped_column(EncryptedJSON)
    status: Mapped[IntegrityStatus] = mapped_column(
        Enum(IntegrityStatus, native_enum=False),
        default=IntegrityStatus.PENDING,
        nullable=False,
    )
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
    )

    user: Mapped["User"] = relationship(back_populates="integrities")

    __table_args__ = (
        UniqueConstraint(
            "integrity_user_id", "integrity", name="uq_integrity_uid_integrity"
        ),
    )
