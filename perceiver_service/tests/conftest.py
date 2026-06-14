"""Shared pytest fixtures and test environment setup."""

import os

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import StaticPool

import knowledge.models  # noqa: F401
import user.models  # noqa: F401
import personality_dna.models  # noqa: F401
import integrations.models  # noqa: F401
from database.core import Base, create_async_db_engine
from main import app

# Settings and encrypted column types load at import time; set env first.
os.environ.setdefault("SECRET_KEY", Fernet.generate_key().decode())
os.environ.setdefault("RABBITMQ__USER", "guest")
os.environ.setdefault("RABBITMQ__PASSWORD", "guest")
os.environ.setdefault("RABBITMQ__HOSTNAME", "localhost")
os.environ.setdefault("RABBITMQ__PORT", "5672")
os.environ.setdefault("TELEGRAM__API_ID", "12345")
os.environ.setdefault("TELEGRAM__API_HASH", "test_api_hash")
os.environ.setdefault(
    "DATABASE__CONNECTION_URL", "sqlite+aiosqlite:///:memory:"
)

#  Test DB setup
test_engine = create_async_db_engine(
    os.getenv("DATABASE__CONNECTION_URL"),
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest.fixture
def valid_tg_session_string():
    return "valid_session_string"


@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def db_session():
    """Fixture for work with test DB."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
