"""CRUD operation to work with user integration models."""

from uuid import UUID

from sqlalchemy import select, insert, update as q_update, delete as q_delete
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
        .values(**integration_in.model_dump())
        .returning(UserIntegration)
    )
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
