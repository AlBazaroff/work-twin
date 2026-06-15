"""CRUD operations for user models."""

from uuid import UUID

from sqlalchemy import select, insert, update as q_update, delete as q_delete
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.dialects.postgresql import insert as pg_insert
from .models import User
from .schemas import UserCreate, UserUpdate


async def get_or_create(*, db_session: AsyncSession, user_id: UUID) -> User:
    """Get user by id or create if it doesn't exist."""
    stmt = (
        pg_insert(User)
        .values(id=user_id)
        .on_conflict_do_nothing(index_elements=[User.id])
        .returning(User)
    )
    user = await db_session.scalar(stmt)

    if not user:
        user = await get(db_session=db_session, user_id=user_id)
    else:
        await db_session.commit()

    return user


async def get(*, db_session: AsyncSession, user_id: UUID) -> User | None:
    """Get user by user_id"""
    stmt = select(User).where(User.id == user_id)
    user = await db_session.scalar(stmt)

    return user


async def create(*, db_session: AsyncSession, user_in: UserCreate) -> User:
    """Create new user from user_in."""
    stmt = insert(User).values(**user_in.model_dump()).returning(User)
    user = await db_session.scalar(stmt)
    await db_session.commit()

    return user


async def update(
    *, db_session: AsyncSession, user_in: UserUpdate
) -> User | None:
    """Update user from user_in."""
    user_data = user_in.model_dump(exclude_unset=True)
    user_id = user_data.pop("id")

    stmt = (
        q_update(User)
        .values(**user_data)
        .where(User.id == user_id)
        .returning(User)
    )
    user = await db_session.scalar(stmt)

    if user:
        await db_session.commit()

    return user


async def delete(*, db_session: AsyncSession, user_id: UUID) -> User | None:
    stmt = q_delete(User).where(User.id == user_id).returning(User)
    user = await db_session.scalar(stmt)

    if user:
        await db_session.commit()

    return user
