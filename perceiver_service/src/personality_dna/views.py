"""Endpoints for actions with twins."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Path, HTTPException, status

from database.core import DBSession

from .service import get_active_by_user_id
from .schemas import PersonalityDNAResponse

router = APIRouter(prefix="/twin", tags=["User"])


@router.get("/personality_dna/{user_id}")
async def personality_dna(
    db_session: DBSession,
    user_id: Annotated[
        UUID, Path(description="The ID of user to get his personality DNA")
    ],
) -> PersonalityDNAResponse:
    """Get active personality DNA for user."""
    profile_dna = await get_active_by_user_id(
        db_session=db_session, user_id=user_id
    )
    if not profile_dna:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "Active Personality DNA not found for user"},
        )
    return PersonalityDNAResponse.model_validate(profile_dna)
