"""HTTP middleware registration."""

from fastapi import FastAPI

from middleware.logging import (
    CorrelationIdMiddleware,
    EnhancedLoggingMiddleware,
)


def register_middlewares(app: FastAPI) -> None:
    """Attach base middleware stack (last added runs first)."""
    app.add_middleware(EnhancedLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)
