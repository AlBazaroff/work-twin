"""CRUD operations for PersonalityDNA model."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PersonalityDNA


async def get(
    *, db_session: AsyncSession, personality_id: int
) -> PersonalityDNA | None:
    """Return personality DNA based on the given id."""
    stmt = select(PersonalityDNA).where(PersonalityDNA.id == personality_id)
    return await db_session.scalar(stmt)


async def get_active_by_user_id(
    *, db_session: AsyncSession, user_id: UUID
) -> PersonalityDNA | None:
    """Return personality DNA based on the given user_id."""
    stmt = select(PersonalityDNA).where(
        PersonalityDNA.user_id == user_id,
        PersonalityDNA.is_active.is_(True),
    )
    return await db_session.scalar(stmt)
