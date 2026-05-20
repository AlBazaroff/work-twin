"""Specific schemas for Telegram integration."""

from datetime import datetime

from pydantic import Field, BaseModel

from ingestion.schemas import BaseCredentials


class TelegramCredentials(BaseCredentials):
    """Credentials for Telegram Provider."""

    session_string: str = Field(..., min_length=1)


class TelegramMessage(BaseModel):
    """Telegram's necessary data about message."""

    message_id: int
    text: str
    date: datetime
    me: bool
    reply_to: int
