"""Providers implementation for Telegram"""

from telethon import TelegramClient
from telethon.sessions import StringSession

from config import Settings
from core.exceptions.providers import ProviderCredentialsNotFoundError
from core.providers.base import SocialProvider
from database.enums import Integration
from ingestion.schemas import BaseCredentials
from .schemas import TelegramCredentials


class TelegramProvider(SocialProvider):
    """Provider for Telegram service."""

    provider: Integration = Integration.TELEGRAM

    def __init__(self, api_id: int, api_hash: str):
        self._api_id: int = api_id
        self._api_hash: str = api_hash

    @classmethod
    def from_settings(cls, settings: Settings) -> "TelegramProvider":
        """Create TelegramProvider instance from settings."""
        return cls(
            api_id=settings.telegram.api_id,
            api_hash=settings.telegram.api_hash,
        )

    async def fetch_chat_history(
        self, credentials: TelegramCredentials, limit: int | None = None
    ):
        """Fetch chat history from Telegram.

        Args:
            credentials: TelegramCredentials to auth in Telegram
            limit: limit of messages, if None - unlimited
        """
        pass

    async def analyze_profile(self, credentials: BaseCredentials):
        """Analyze user profile in Telegram.

        Args:
            credentials: TelegramCredentials to auth in Telegram
        """
        pass

    async def get_identity(self, credentials: TelegramCredentials) -> str:
        """Get the identity of the Telegram user account."""
        session_string = credentials.session_string

        if not session_string:
            raise ProviderCredentialsNotFoundError(self.provider.value)

        async with TelegramClient(
            StringSession(session_string), self._api_id, self._api_hash
        ) as client:
            # TODO: try-except-finally
            me = await client.get_me()

            identity = str(me.id)
            return identity
