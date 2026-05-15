"""Tests for application settings and connection URL builders."""

import pytest
from typing import TypedDict

from src.config import DBSettings, RabbitMQSettings, TelegramSettings


class AuthSettings(TypedDict):
    user: str
    password: str
    hostname: str


class TelegramAPISettings(TypedDict):
    api_id: int
    api_hash: str


@pytest.fixture
def infr_auth():
    """Fixture for infrastructure authentication settings."""
    user = "testuser"
    password = "password123"
    hostname = "localhost"
    return AuthSettings(user=user, password=password, hostname=hostname)


@pytest.fixture
def telegram_settings():
    """Fixture for Telegram API credentials."""
    api_id = 123456
    api_hash = "abcdef1234567890"
    return TelegramAPISettings(api_id=api_id, api_hash=api_hash)


class TestRabbitMQSettings:
    def test_connection_url_formats_amqp_uri(self, infr_auth):
        """Test connection URL is correctly formatted for RabbitMQ."""
        settings = RabbitMQSettings(
            user=infr_auth.user,
            password=infr_auth.password,
            hostname=infr_auth.hostname,
            port="5672",
        )
        assert settings.connection_url == (
            f"amqp://{infr_auth.user}:{infr_auth.password}"
            f"@{infr_auth.hostname}:5672/"
        )


class TestDBSettings:
    def test_connection_url_uses_asyncpg_driver(self, infr_auth):
        """
        Test that connection URL is correctly formatted
        for asyncpg and includes all components.
        """
        settings = DBSettings(
            user=infr_auth.user,
            password=infr_auth.password,
            hostname=infr_auth.hostname,
            port="5433",
            name="mydb",
        )
        url = settings.connection_url
        assert url.startswith("postgresql+asyncpg://")
        assert (
            f"{infr_auth.user}:{infr_auth.password}@"
            f"{infr_auth.hostname}:5433/mydb"
        ) in url

    def test_defaults_for_pool_settings(self):
        """
        Test default DB values for connections.
        """
        settings = DBSettings()
        assert settings.engine_pool_size == 20
        assert settings.engine_pool_recycle == 3600
        assert settings.engine_pool_ping is False


class TestTelegramSettings:
    def test_requires_api_credentials(self, telegram_settings):
        """Test that TelegramSettings requires api_id and api_hash."""
        settings = TelegramSettings(
            api_id=telegram_settings.api_id,
            api_hash=telegram_settings.api_hash,
        )
        assert settings.api_id == telegram_settings.api_id
        assert settings.api_hash == telegram_settings.api_hash
