from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health():
    """For checking service health."""
    return {
        "status": "ok",
    }


@router.get("/ready", tags=["health"])
async def ready():
    """For checking service health(alternative)."""
    return {
        "status": "ready",
    }
