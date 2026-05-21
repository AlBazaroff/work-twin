"""API for perceiver work twin microservice."""

from fastapi import APIRouter

from personality_dna.views import router as twins_router

router = APIRouter()
router.include_router(twins_router)


@router.get(
    "/health",
    tags=["health"],
    summary="Check health of service",
)
async def health():
    """For checking service health."""
    return {
        "status": "ok",
    }


@router.get(
    "/ready",
    tags=["health"],
    summary="Check readiness of service",
)
async def ready():
    """For checking service ready(alternative)."""
    return {
        "status": "ready",
    }
