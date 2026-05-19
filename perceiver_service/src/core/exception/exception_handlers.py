"""Map domain exceptions to HTTP responses."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exception.base import BaseException
from core.exception.providers import (
    ProviderCredentialsNotFoundError,
    ProviderNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register handlers for service-level exceptions."""

    @app.exception_handler(ProviderNotFoundError)
    @app.exception_handler(ProviderCredentialsNotFoundError)
    async def provider_not_found_handler(
        request: Request,
        exc: ProviderNotFoundError | ProviderCredentialsNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )

    @app.exception_handler(BaseException)
    async def service_exception_handler(
        request: Request,
        exc: BaseException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )
