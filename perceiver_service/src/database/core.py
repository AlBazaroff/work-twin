from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from config import settings


def create_async_db_engine(connection_string: str) -> AsyncEngine:
    """Create a database engine with proper timeout settings.

    Args:
        connection_string: Database connection string
    """
    timeout_kwargs = {
        # Connection timeout - how long to wait for a connection from the pool
        "pool_timeout": settings.database.engine_pool_timeout,
        # Recycle connections after this many seconds
        "pool_recycle": settings.database.engine_pool_recycle,
        # Maximum number of connections to keep in the pool
        "pool_size": settings.database.engine_pool_size,
        # Maximum overflow connections allowed beyond pool_size
        "max_overflow": settings.database.engine_max_overflow,
        # Connection pre-ping to verify connection is still alive
        "pool_pre_ping": settings.database.engine_pool_ping,
    }
    return create_async_engine(connection_string, **timeout_kwargs)


engine = create_async_db_engine(settings.database.connection_url)

AsyncSessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    def __repr__(self):
        cols = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({cols})"


@asynccontextmanager
async def get_db():
    """Get database session from request state."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


DbSession = Annotated[AsyncSession, Depends(get_db)]
