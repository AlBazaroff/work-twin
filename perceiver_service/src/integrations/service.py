"""CRUD operation to work with user integration models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import select, insert, update as q_update, delete as q_delete
from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserIntegration
from .schemas import UserIntegrationCreate, UserIntegrationUpdate


async def get(
    *, db_session: AsyncSession, integration_id: UUID
) -> UserIntegration | None:
    """Get user integration through integration_id."""
    stmt = select(UserIntegration).where(UserIntegration.id == integration_id)
    user_integration = await db_session.scalar(stmt)

    return user_integration


async def create(
    *, db_session: AsyncSession, integration_in: UserIntegrationCreate
) -> UserIntegration | None:
    """Create new user integration based on integration_in data."""
    stmt = (
        insert(UserIntegration)
        .values(**integration_in.model_dump(exclude_unset=True))
        .returning(UserIntegration)
    )
    user_integration = await db_session.scalar(stmt)
    await db_session.commit()

    return user_integration


async def create_or_update(
    *,
    db_session: AsyncSession,
    integration_in: UserIntegrationCreate,
    updated_at: datetime,
) -> UserIntegration | None:
    """
    Create or update new UserIntegration
    based on integration_in data and updated_at field.
    """
    data = integration_in.model_dump(exclude_unset=True)
    insert_stmt = psql_insert(UserIntegration).values(
        **data, updated_at=updated_at
    )

    update_columns = {
        col.name: insert_stmt.excluded[col.name]
        for col in UserIntegration.__table__.columns
        if col.name not in ["user_id", "integration"] and col.name in data
    }
    update_columns["updated_at"] = updated_at

    stmt = insert_stmt.on_conflict_do_update(
        index_elements=["user_id", "integration"],
        set_=update_columns,
        where=(UserIntegration.updated_at < updated_at)
        if updated_at
        else None,
    ).returning(UserIntegration)
    user_integration = await db_session.scalar(stmt)
    await db_session.commit()

    return user_integration


async def update(
    *, db_session: AsyncSession, integration_in: UserIntegrationUpdate
) -> UserIntegration | None:
    """Update user integration from integration_in data."""
    integration_data = integration_in.model_dump(exclude_unset=True)
    integration_id = integration_data.pop("id")

    stmt = (
        q_update(UserIntegration)
        .values(**integration_data)
        .where(UserIntegration.id == integration_id)
        .returning(UserIntegration)
    )
    user_integration = await db_session.scalar(stmt)

    if user_integration:
        await db_session.commit()

    return user_integration


async def delete(
    *, db_session, integration_id: UUID
) -> UserIntegration | None:
    """Delete user integration by integration_id."""
    stmt = (
        q_delete(UserIntegration)
        .where(UserIntegration.id == integration_id)
        .returning(UserIntegration)
    )
    user_integration = await db_session.scalar(stmt)

    if user_integration:
        await db_session.commit()

    return user_integration
