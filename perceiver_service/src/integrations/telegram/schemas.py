"""Specific schemas for Telegram integration."""

from ingestion.schemas import BaseCredentials


class TelegramCredentials(BaseCredentials):
    """Credentials for Telegram Provider."""

    session_string: str
