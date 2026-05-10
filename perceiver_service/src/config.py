from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


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

    engine_pool_ping: bool = Field(default=False)
    engine_pool_recycle: int = Field(default=3600)
    engine_pool_size: int = Field(default=20)
    engine_pool_timeout: int = Field(default=30)
    engine_max_overflow: int = Field(default=10)

    @property
    def connection_url(self):
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.hostname}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    rabbitmq: RabbitMQSettings = Field(default=...)
    database: DBSettings = Field(default=...)


settings = Settings()
