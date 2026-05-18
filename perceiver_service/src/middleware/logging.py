import logging
import time
import uuid
from contextvars import ContextVar
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger("perceiver.middleware")

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a correlation ID
    to the request context for tracing and logging purposes.
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        id_value = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        token = correlation_id.set(id_value)

        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = id_value
            return response
        finally:
            correlation_id.reset(token)


class EnhancedLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for classified logging and error handling."""

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        start_time = time.perf_counter()
        c_id = correlation_id.get()

        try:
            logger.info(
                f"[{c_id}] Request: {request.method} {request.url.path}"
            )
            response = await call_next(request)
            process_time = (time.perf_counter() - start_time) * 1000
            logger.info(
                f"[{c_id}] Response: {response.status_code} "
                f"| Time: {process_time:.2f}ms"
            )
            return response
        except Exception as exc:
            logger.error(
                f"[{c_id}] Critical Failure: {str(exc)} "
                f"| Time: {process_time:.2f}ms",
                exc_info=True,
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "corrlation_id": c_id,
                },
            )
