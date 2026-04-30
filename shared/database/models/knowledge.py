"""
Contain database related models with knowledge.
"""

from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Enum,
    JSON,
    String,
    Integer,
    Boolean,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import VECTOR

from database.core import Base
from database.types import EncryptedJSON, EncryptedString
from core.database.models.mixins import IDMixin, TimeStampMixin
from core.constants.knowledge import KnowledgeScope, KnowledgeSourceType
from core.constants.user import Integrity

if TYPE_CHECKING:
    from .user import User


class KnowledgeSpace(Base, IDMixin):
    __tablename__ = "knowledge_space"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        index=True,
        nullable=False,
    )
    integrity: Mapped[Integrity] = mapped_column(
        Enum(Integrity, native_enum=False),
        nullable=False,
    )
    extra_info: Mapped[Optional[dict]] = mapped_column(JSON)

    user: Mapped["User"] = relationship(back_populates="knowledge_namespaces")
    knowledge_item: Mapped["Knowledge"] = relationship(
        back_populates="knowledge_space",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "integrity",
            name="ux_user_id_integrity",
        ),
    )


class Knowledge(Base, IDMixin, TimeStampMixin):
    __tablename__ = "knowledge"

    knowledge_space_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_space.id"),
        index=True,
    )
    content: Mapped[str] = mapped_column(
        EncryptedString,
        nullable=False,
    )
    embedding: Mapped[list] = mapped_column(
        VECTOR(1536),
        nullable=False,
    )
    embedding_model: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    scope: Mapped[KnowledgeScope] = mapped_column(
        Enum(KnowledgeScope, native_enum=False),
        default=KnowledgeScope.PRIVATE,
        nullable=False,
    )
    source_type: Mapped[KnowledgeSourceType] = mapped_column(
        Enum(KnowledgeSourceType, native_enum=False),
        nullable=True,
    )
    source_id: Mapped[str] = mapped_column(
        EncryptedString(64),
        nullable=True,
        index=True,
    )
    interceptor_id: Mapped[str] = mapped_column(
        EncryptedString(64),
        nullable=True,
        index=True,
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    extra_info: Mapped[Optional[dict]] = mapped_column(EncryptedJSON)

    knowledge_space: Mapped["KnowledgeSpace"] = relationship(
        back_populates="knowledge_items",
    )

    __table_args__ = (
        UniqueConstraint(
            "knowledge_space_id",
            "source_id",
            "interceptor_id",
            "version",
            name="ux_space_source_interceptor_version",
        ),
        Index("ix_source_id_interceptor_id", "source_id", "interceptor_id"),
    )
