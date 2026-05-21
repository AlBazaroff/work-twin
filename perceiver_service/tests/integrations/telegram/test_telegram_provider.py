"""Tests for TelegramProvider."""

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telethon.errors import AuthKeyUnregisteredError

from config import get_settings
from core.providers.exceptions import ProviderCredentialsNotFoundError
from integrations.enums import Integration
from integrations.telegram.exceptions import TelegramUserNotAuthorized
from integrations.telegram.providers import TelegramProvider
from integrations.telegram.schemas import TelegramCredentials, TelegramMessage

settings = get_settings()


@pytest.fixture
def telegram_client(*, authorized=True, connect_side_effect=None):
    """Build a Telethon client mock matching _get_client lifecycle."""

    def _builder(*, authorized=True, connect_side_effect=None):
        client = AsyncMock()
        if connect_side_effect is not None:
            client.connect = AsyncMock(side_effect=connect_side_effect)
        else:
            client.connect = AsyncMock()
        client.disconnect = AsyncMock()
        client.is_user_authorized = AsyncMock(return_value=authorized)
        return client

    return _builder


class TestTelegramProviderFromSettings:
    """Test the from_settings classmethod of TelegramProvider."""

    def test_from_settings_maps_telegram_config(self):
        """
        Test telegram provider is correctly created from settings
        from environment variables.
        """
        instance = TelegramProvider.from_settings(settings)
        assert instance._api_id == settings.telegram.api_id
        assert instance._api_hash == settings.telegram.api_hash
        assert isinstance(instance, TelegramProvider)

    def test_from_settings_passes_telethon_client_options(self):
        """Test optional Telethon client kwargs are taken from settings."""
        instance = TelegramProvider.from_settings(settings)
        assert instance._client_config == {
            "timeout": settings.telegram.timeout,
            "request_retries": settings.telegram.request_retries,
            "connection_retries": settings.telegram.connection_retries,
            "retry_delay": settings.telegram.retry_delay,
        }


class TestTelegramProviderGetClient:
    """Test the _get_client context manager of TelegramProvider."""

    @pytest.mark.asyncio
    async def test_raises_when_session_string_empty(self, provider, user_id):
        """Test missing session string raises credentials not found."""
        credentials = TelegramCredentials.model_construct(session_string="")
        with pytest.raises(ProviderCredentialsNotFoundError):
            async with provider._get_client(user_id, credentials):
                pass

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_raises_when_user_not_authorized(
        self,
        mock_session_cls,
        mock_client_cls,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """Test unauthorized session raises TelegramUserNotAuthorized."""
        mock_client = telegram_client(authorized=False)
        mock_client_cls.return_value = mock_client

        with pytest.raises(TelegramUserNotAuthorized) as exc_info:
            async with provider._get_client(user_id, credentials):
                pass

        assert str(user_id) in str(exc_info.value)
        mock_session_cls.assert_called_once_with(credentials.session_string)
        mock_client.connect.assert_awaited_once()
        mock_client.disconnect.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_raises_on_auth_key_unregistered(
        self,
        mock_session_cls,
        mock_client_cls,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """
        Test Telethon auth errors are mapped
        to TelegramUserNotAuthorized.
        """
        auth_error = AuthKeyUnregisteredError(MagicMock())
        mock_client = telegram_client(
            connect_side_effect=auth_error,
        )
        mock_client_cls.return_value = mock_client

        with pytest.raises(TelegramUserNotAuthorized):
            async with provider._get_client(user_id, credentials):
                pass

        mock_client.disconnect.assert_awaited_once()

    @pytest.mark.asyncio
    @patch(
        "integrations.telegram.providers.asyncio.wait_for",
        new_callable=AsyncMock,
    )
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_raises_on_connection_timeout(
        self,
        mock_session_cls,
        mock_client_cls,
        mock_wait_for,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """Test connection timeout is propagated to the caller."""

        async def wait_for(coro, timeout):
            coro.close()
            raise asyncio.TimeoutError()

        mock_wait_for.side_effect = wait_for

        mock_client = telegram_client()
        mock_client_cls.return_value = mock_client

        with pytest.raises(asyncio.TimeoutError):
            async with provider._get_client(user_id, credentials):
                pass

        mock_client.disconnect.assert_awaited_once()

    @pytest.mark.asyncio
    @patch(
        "integrations.telegram.providers.asyncio.wait_for",
        new_callable=AsyncMock,
    )
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_yields_connected_client_when_authorized(
        self,
        mock_session_cls,
        mock_client_cls,
        mock_wait_for,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """
        Test authorized user receives a connected
        client from the context.
        """

        async def wait_for(coro, timeout):
            return await coro

        mock_wait_for.side_effect = wait_for

        mock_client = telegram_client(authorized=True)
        mock_client_cls.return_value = mock_client

        async with provider._get_client(user_id, credentials) as client:
            assert client is mock_client

        mock_client_cls.assert_called_once_with(
            mock_session_cls.return_value,
            provider._api_id,
            provider._api_hash,
            **provider._client_config,
        )
        mock_client.connect.assert_awaited_once()
        mock_client.is_user_authorized.assert_awaited_once()
        mock_client.disconnect.assert_awaited_once()


class TestTelegramProviderFetchChatHistory:
    """Test the fetch_chat_history method of TelegramProvider."""

    @staticmethod
    def _raw_message(msg_id, text, *, me=False, reply_to=0):
        message = MagicMock()
        message.id = msg_id
        message.text = text
        message.date = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
        message.me = me
        message.reply_to = reply_to
        return message

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_returns_messages_in_chronological_order(
        self,
        mock_session_cls,
        mock_client_cls,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """Test iter_messages order is reversed to oldest-first."""
        mock_client = telegram_client(authorized=True)

        async def iter_messages(dialog, limit=None):
            yield self._raw_message(2, "newer")
            yield self._raw_message(1, "older")

        print([msg async for msg in iter_messages("someone")])

        mock_client.iter_messages = iter_messages
        mock_client_cls.return_value = mock_client

        msgs = [
            TelegramMessage(
                message_id=msg.id,
                text=msg.text,
                date=msg.date,
                me=msg.me,
                reply_to=msg.reply_to,
            )
            async for msg in iter_messages("someone")
        ]
        msgs.reverse()

        messages = await provider.fetch_chat_history(user_id, credentials)

        assert messages == msgs

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_passes_dialog_and_limit_to_iter_messages(
        self,
        mock_session_cls,
        mock_client_cls,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """Test dialog and limit arguments are forwarded to Telethon."""
        limit = 50
        dialog = 12345
        mock_client = telegram_client(authorized=True)
        iter_calls = []

        async def iter_messages(dialog, limit=None):
            iter_calls.append((dialog, limit))
            return
            yield  # pragma: no cover

        mock_client.iter_messages = iter_messages
        mock_client_cls.return_value = mock_client

        await provider.fetch_chat_history(
            user_id,
            credentials,
            limit=limit,
            dialog=dialog,
        )

        assert iter_calls == [(dialog, limit)]

    @pytest.mark.asyncio
    async def test_raises_when_session_string_empty(self, provider, user_id):
        """Test missing credentials prevent history fetch."""
        credentials = TelegramCredentials.model_construct(session_string="")
        with pytest.raises(ProviderCredentialsNotFoundError):
            await provider.fetch_chat_history(user_id, credentials)


class TestTelegramProviderGetIdentity:
    """Test the get_identity method of TelegramProvider."""

    @pytest.mark.asyncio
    async def test_raises_when_session_string_empty(self, provider, user_id):
        """
        Test that NotFound error is raised
        when session string is empty.
        """
        credentials = TelegramCredentials.model_construct(session_string="")
        with pytest.raises(ProviderCredentialsNotFoundError):
            await provider.get_identity(user_id, credentials)

    @pytest.mark.asyncio
    @patch("integrations.telegram.providers.TelegramClient")
    @patch("integrations.telegram.providers.StringSession")
    async def test_returns_telegram_user_id_as_string(
        self,
        mock_session_cls,
        mock_client_cls,
        provider,
        user_id,
        credentials,
        telegram_client,
    ):
        """Test that get_identity returns the Telegram user id as a string."""
        mock_me = MagicMock()
        mock_me.id = 123456
        mock_client = telegram_client(authorized=True)
        mock_client.get_me = AsyncMock(return_value=mock_me)
        mock_client_cls.return_value = mock_client

        identity = await provider.get_identity(user_id, credentials)

        assert identity == "123456"
        mock_session_cls.assert_called_once_with(credentials.session_string)
        mock_client_cls.assert_called_once()
        mock_client.get_me.assert_awaited_once()
        mock_client.disconnect.assert_awaited_once()

    def test_provider_enum_is_telegram(self, provider):
        """Test that provider is correct."""
        assert provider.provider == Integration.TELEGRAM
