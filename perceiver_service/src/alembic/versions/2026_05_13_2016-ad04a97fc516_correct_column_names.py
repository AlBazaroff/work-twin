"""correct column names

Revision ID: ad04a97fc516
Revises: c1f51803b156
Create Date: 2026-05-13 20:16:11.653134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import database.types

revision: str = "ad04a97fc516"
down_revision: Union[str, Sequence[str], None] = "c1f51803b156"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "perceiver_user",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "PAID",
                "UNPAID",
                "DEACTIVATED",
                name="userstatus",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_integration",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column(
            "integration",
            sa.Enum(
                "TELEGRAM", "SLACK", name="integration", native_enum=False
            ),
            nullable=False,
        ),
        sa.Column("integration_user_id", sa.String(length=64), nullable=True),
        sa.Column(
            "credentials", database.types.EncryptedJSON(), nullable=False
        ),
        sa.Column(
            "status",
            sa.Enum(
                "PENDING",
                "ACTIVE",
                "INACTIVE",
                "EXPIRED",
                "REVOKED",
                name="integrationstatus",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["perceiver_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "integration_user_id",
            "integration",
            name="uq_integration_uid_integration",
        ),
    )
    op.create_index(
        op.f("ix_user_integration_integration_user_id"),
        "user_integration",
        ["integration_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_integration_user_id"),
        "user_integration",
        ["user_id"],
        unique=False,
    )
    op.drop_constraint(
        op.f("knowledge_space_user_id_fkey"),
        "knowledge_space",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("personality_dna_user_id_fkey"),
        "personality_dna",
        type_="foreignkey",
    )
    op.drop_index(
        op.f("ix_user_integrity_integrity_user_id"),
        table_name="user_integrity",
    )
    op.drop_index(
        op.f("ix_user_integrity_user_id"), table_name="user_integrity"
    )
    op.drop_table("user_integrity")
    op.drop_table("user")
    op.create_foreign_key(
        None, "knowledge_space", "perceiver_user", ["user_id"], ["id"]
    )
    op.create_foreign_key(
        None, "personality_dna", "perceiver_user", ["user_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "personality_dna", type_="foreignkey")  # type: ignore
    op.create_foreign_key(
        op.f("personality_dna_user_id_fkey"),
        "personality_dna",
        "user",
        ["user_id"],
        ["id"],
    )
    op.drop_constraint(None, "knowledge_space", type_="foreignkey")  # type: ignore
    op.create_foreign_key(
        op.f("knowledge_space_user_id_fkey"),
        "knowledge_space",
        "user",
        ["user_id"],
        ["id"],
    )
    op.create_table(
        "user",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "status",
            sa.VARCHAR(length=11),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
    )
    op.create_table(
        "user_integrity",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "integrity",
            sa.VARCHAR(length=8),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "integrity_user_id",
            sa.VARCHAR(length=64),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "credentials", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "status", sa.VARCHAR(length=8), autoincrement=False, nullable=False
        ),
        sa.Column(
            "last_synced_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["user.id"], name=op.f("user_integrity_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_integrity_pkey")),
        sa.UniqueConstraint(
            "integrity_user_id",
            "integrity",
            name=op.f("uq_integrity_uid_integrity"),
            postgresql_include=[],
            postgresql_nulls_not_distinct=False,
        ),
    )
    op.create_index(
        op.f("ix_user_integrity_user_id"),
        "user_integrity",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_integrity_integrity_user_id"),
        "user_integrity",
        ["integrity_user_id"],
        unique=False,
    )
    op.drop_index(
        op.f("ix_user_integration_user_id"), table_name="user_integration"
    )
    op.drop_index(
        op.f("ix_user_integration_integration_user_id"),
        table_name="user_integration",
    )
    op.drop_table("user_integration")
    op.drop_table("perceiver_user")
