"""HTTP middleware registration."""

from fastapi import FastAPI
from asgi_correlation_id import CorrelationIdMiddleware

from middleware.logging import (
    EnhancedLoggingMiddleware,
)


def register_middlewares(app: FastAPI) -> None:
    """Attach base middleware stack (last added runs first)."""
    app.add_middleware(EnhancedLoggingMiddleware)
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Correlation-ID",
        update_request_header=True,
    )
