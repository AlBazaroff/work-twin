"""Providers implementation for Telegram"""

import asyncio
import logging
from contextlib import asynccontextmanager
from uuid import UUID

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    AuthKeyUnregisteredError,
    AuthKeyNotFound,
    UserDeactivatedError,
)

from config import Settings
from core.providers.exceptions import ProviderCredentialsNotFoundError
from core.providers.base import SocialProvider
from database.enums import Integration
from core.exception import BaseException
from .exceptions import TelegramUserNotAuthorized
from .schemas import TelegramCredentials, TelegramMessage

logger = logging.getLogger(__name__)


class TelegramProvider(SocialProvider):
    """Provider for Telegram service."""

    provider: Integration = Integration.TELEGRAM

    def __init__(self, api_id: int, api_hash: str, **kwargs):
        """Initialize telegram provider instance.

        Args:
            api_id: telegram app api_id
            api_hash: telegram app api_hash
            **kwargs: additional args for TelegramClient
        """
        self._api_id: int = api_id
        self._api_hash: str = api_hash
        self._client_config: dict = kwargs

    @classmethod
    def from_settings(cls, settings: Settings) -> "TelegramProvider":
        """Create TelegramProvider instance from app settings."""
        return cls(
            api_id=settings.telegram.api_id,
            api_hash=settings.telegram.api_hash,
            timeout=settings.telegram.timeout,
            request_retries=settings.telegram.request_retries,
            connection_retries=settings.telegram.connection_retries,
            retry_delay=settings.telegram.retry_delay,
        )

    @asynccontextmanager
    async def _get_client(
        self, user_id: UUID, credentials: TelegramCredentials
    ):
        """Return Telegram client."""
        session_string = credentials.session_string
        if not session_string:
            raise ProviderCredentialsNotFoundError(self.provider.value)

        client = TelegramClient(
            StringSession(session_string),
            self._api_id,
            self._api_hash,
            **self._client_config,
        )

        try:
            await asyncio.wait_for(client.connect(), timeout=10)
            if not await client.is_user_authorized():
                logger.warning(
                    f"[Telegram][AuthWarn] User {user_id} is connected, "
                    "but not authorized"
                )
                raise TelegramUserNotAuthorized(str(user_id))

            yield client

        except asyncio.TimeoutError as exc:
            logger.info(
                f"[Telegram][TimeoutError] Connection for user"
                f"{user_id} timed out"
            )
            raise exc

        except (
            AuthKeyUnregisteredError,
            AuthKeyNotFound,
            UserDeactivatedError,
        ):
            logger.warning(
                f"[Telegram][AuthWarn] User {user_id} not authorized"
            )
            raise TelegramUserNotAuthorized(str(user_id))

        except BaseException as exc:
            logger.error(
                f"[Telegram] Unexpected error while connecting "
                f"{user_id}: {exc}"
            )

        finally:
            await client.disconnect()

    async def fetch_chat_history(
        self,
        user_id: UUID,
        credentials: TelegramCredentials,
        limit: int | None = None,
        dialog: int | str = "me",
        *args,
        **kwargs,
    ) -> list[TelegramMessage]:
        """Fetch chat history from Telegram.

        Args:
            credentials: TelegramCredentials to auth in Telegram
            limit: limit of messages, if None - unlimited
            dialog: id of dialog
        """
        # can use deque instead list
        messages = []

        async with self._get_client(user_id, credentials) as client:
            async for message in client.iter_messages(
                dialog,
                limit=limit,
            ):
                messages.append(
                    TelegramMessage(
                        message_id=message.id,
                        text=message.text,
                        date=message.date,
                        me=message.me,
                        reply_to=message.reply_to,
                    )
                )

        # reverse to change order from first to latest
        messages.reverse()

        return messages

    async def analyze_profile(
        self, user_id: UUID, credentials: TelegramCredentials
    ):
        """Analyze user profile in Telegram.

        Args:
            credentials: TelegramCredentials to auth in Telegram
        """
        pass

    async def get_identity(
        self, user_id: UUID, credentials: TelegramCredentials
    ) -> str:
        """Get the identity of the Telegram user account."""
        async with self._get_client(user_id, credentials) as client:
            me = await client.get_me()

            identity = str(me.id)
            return identity
