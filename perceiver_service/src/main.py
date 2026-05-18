"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.exceptions.exception_handlers import register_exception_handlers
from database.core import engine
from middlewares import register_middlewares
from router import router as api_router

APP_TITLE = "Work Twin Perceiver"
APP_VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        lifespan=lifespan,
    )
    register_middlewares(app)
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()
