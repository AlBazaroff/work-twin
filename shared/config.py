from pydantic import BaseModel
from starlette.config import Config


class BaseConfigurationModel(BaseModel):
    pass


config = Config(".env")

# Secret keys
CRYPTO_SECRET_KEY = config("CRYPTO_SECRET_KEY", default=None)

# Database credentials
DATABASE_USER = config("DATABASE_USER", default="admin")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", default="admin")
DATABASE_NAME = config("DATABASE_NAME", default="work-twin")
DATABASE_HOSTNAME = config("DATABASE_HOSTNAME", default="127.0.0.1")
DATABASE_PORT = config("DATABASE_PORT", default="5432")
SQLALCHEMY_DATABASE_CONNECTION = (
    f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
)

# DB Timeout settings:
DATABASE_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)
DATABASE_ENGINE_POOL_RECYCLE = config(
    "DATABASE_ENGINE_POOL_RECYCLE",
    cast=int,
    default=3600,
)
DATABASE_ENGINE_POOL_SIZE = config(
    "DATABASE_ENGINE_POOL_SIZE",
    cast=int,
    default=20,
)
DATABASE_ENGINE_POOL_TIMEOUT = config(
    "DATABASE_ENGINE_POOL_TIMEOUT",
    cast=int,
    default=30,
)
DATABASE_ENGINE_MAX_OVERFLOW = config(
    "DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=10
)
