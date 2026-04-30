"""
Contain models related to Personality DNA.
"""

from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from database.types import EncryptedJSON
from core.database.models.mixins import IDMixin, TimeStampMixin

if TYPE_CHECKING:
    from .user import User


class PersonalityDNA(Base, IDMixin, TimeStampMixin):
    """
    Personality DNA. Contain information about user behavior,
    his preferences, facts.
    Serve as user profile.
    """

    __tablename__ = "personality_dna"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        index=True,
        nullable=False,
    )
    style_markers: Mapped[dict] = mapped_column(EncryptedJSON, nullable=False)
    core_facts: Mapped[Optional[dict]] = mapped_column(EncryptedJSON)
    preferences: Mapped[Optional[dict]] = mapped_column(EncryptedJSON)
    version: Mapped[int] = mapped_column(
        Integer,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    user: Mapped["User"] = relationship(back_populates="personalities")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "version",
            name="ux_user_id_version",
        ),
    )
