"""Database integration models."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

import uuid6
from sqlalchemy import ForeignKey, Enum, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from database.mixins import IDMixin, TimeStampMixin
from database.types import EncryptedJSON
from .enums import Integration, IntegrationStatus

if TYPE_CHECKING:
    from user.models import User


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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="integrations",
    )

    __table_args__ = (
        UniqueConstraint(
            "integration_user_id",
            "integration",
            name="uq_integration_uid_integration",
        ),
    )
