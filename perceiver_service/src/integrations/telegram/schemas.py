"""Specific schemas for Telegram integration."""

from pydantic import Field

from ingestion.schemas import BaseCredentials


class TelegramCredentials(BaseCredentials):
    """Credentials for Telegram Provider."""

    session_string: str = Field(..., min_length=1)
