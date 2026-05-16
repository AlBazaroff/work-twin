from pydantic import Field, BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseModel):
    """Settings for telegram APP."""

    api_id: int = Field(default=...)
    api_hash: str = Field(default=...)


class RabbitMQSettings(BaseModel):
    user: str = Field(default=...)
    password: str = Field(default=...)
    hostname: str = Field(default=...)
    port: str = Field(default=...)

    @property
    def connection_url(self) -> str:
        """Form and return broker URL."""
        return (
            f"amqp://{self.user}:{self.password}@{self.hostname}:{self.port}/"
        )


class DBSettings(BaseModel):
    user: str = Field(default="admin")
    password: str = Field(default="admin")
    hostname: str = Field(default="127.0.0.1")
    port: str = Field(default="5432")
    name: str = Field(default="perceiver_work_twin")
    provider: str = Field(default="postgresql+asyncpg")
    connection_url: str | None = Field(default=None)

    engine_pool_ping: bool = Field(default=False)
    engine_pool_recycle: int = Field(default=3600)
    engine_pool_size: int = Field(default=20)
    engine_pool_timeout: int = Field(default=30)
    engine_max_overflow: int = Field(default=10)

    @model_validator(mode="before")
    @classmethod
    def compute_connection_url(cls, data: dict) -> dict:
        """Compute connection URL from components."""
        if data.get("connection_url") is None:
            data["connection_url"] = (
                f"{data['provider']}://{data['user']}:{data['password']}@"
                f"{data['hostname']}:{data['port']}/{data['name']}"
            )
        return data


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    rabbitmq: RabbitMQSettings = Field(default=...)
    database: DBSettings = Field(default=...)
    telegram: TelegramSettings = Field(default=...)

    secret_key: str = Field(default=...)


settings = Settings()
