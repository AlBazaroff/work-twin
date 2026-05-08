from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    rabbitmq_user: str = Field(default=...)
    rabbitmq_password: str = Field(default=...)
    rabbitmq_hostname: str = Field(default=...)
    rabbitmq_port: str = Field(default=...)

    @property
    def broker_url(self) -> str:
        """Form and return broker URL."""
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@"
            f"{self.rabbitmq_hostname}:{self.rabbitmq_password}/"
        )


settings = Settings()
