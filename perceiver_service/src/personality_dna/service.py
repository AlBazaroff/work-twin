"""CRUD operations for PersonalityDNA model."""

from uuid import UUID

from sqlalchemy import select, insert, update as q_update, delete as q_delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PersonalityDNA
from .schemas import (
    PersonalityDNACreate,
    PersonalityDNAUpdate,
    ActivePersonalityDNAUpdate,
)


async def get(
    *, db_session: AsyncSession, personality_id: UUID
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


async def create(
    *, db_session: AsyncSession, personality_in: PersonalityDNACreate
) -> PersonalityDNA:
    """Create new personality DNA from personality_in."""
    stmt = (
        insert(PersonalityDNA)
        .values(**personality_in.model_dump())
        .returning(PersonalityDNA)
    )
    personality = await db_session.scalar(stmt)
    await db_session.commit()

    return personality  # type: ignore


async def update(
    *, db_session: AsyncSession, personality_in: PersonalityDNAUpdate
) -> PersonalityDNA | None:
    """Update personality DNA from personality_in."""
    personality_data = personality_in.model_dump(exclude_unset=True)
    personality_id = personality_data.pop("id")

    stmt = (
        q_update(PersonalityDNA)
        .values(**personality_data)
        .where(PersonalityDNA.id == personality_id)
        .returning(PersonalityDNA)
    )
    personality = await db_session.scalar(stmt)

    if personality:
        await db_session.commit()

    return personality


async def update_active_by_user_id(
    *,
    db_session: AsyncSession,
    personality_in: ActivePersonalityDNAUpdate,
) -> PersonalityDNA | None:
    """Update active personality DNA for user by user_id."""
    personality_data = personality_in.model_dump(exclude_unset=True)
    user_id = personality_data.pop("user_id")

    stmt = (
        q_update(PersonalityDNA)
        .values(**personality_data)
        .where(
            PersonalityDNA.user_id == user_id,
            PersonalityDNA.is_active.is_(True),
        )
        .returning(PersonalityDNA)
    )

    personality = await db_session.scalar(stmt)

    if personality:
        await db_session.commit()

    return personality


async def delete(
    *, db_session: AsyncSession, personality_id: UUID
) -> PersonalityDNA | None:
    """Delete personality DNA by id."""
    stmt = (
        q_delete(PersonalityDNA)
        .where(PersonalityDNA.id == personality_id)
        .returning(PersonalityDNA)
    )
    personality = await db_session.scalar(stmt)

    if personality:
        await db_session.commit()

    return personality
