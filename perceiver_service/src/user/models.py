"""Contain user and his related models."""

from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from database.mixins import IDMixin, TimeStampMixin
from .enums import UserStatus

if TYPE_CHECKING:
    from personality_dna.models import PersonalityDNA
    from integrations.models import UserIntegration
    from knowledge.models import KnowledgeSpace


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
        "UserIntegration",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    personalities: Mapped[list["PersonalityDNA"]] = relationship(
        "PersonalityDNA",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    knowledge_namespaces: Mapped[list["KnowledgeSpace"]] = relationship(
        "KnowledgeSpace",
        back_populates="user",
        cascade="all, delete-orphan",
    )
