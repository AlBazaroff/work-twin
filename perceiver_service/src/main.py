"""FastAPI application entrypoint."""

import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router as api_router
from core.exception.exception_handlers import register_exception_handlers
from core.settings import LOGGING_CONFIG
from database.core import engine
from middleware import register_middlewares

APP_TITLE = "Work Twin Perceiver"
APP_VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        logger.info("Connections pool is closing...")
        await engine.dispose()
        logger.info("Connection pool is successfully closed.")


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


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

app = create_app()
