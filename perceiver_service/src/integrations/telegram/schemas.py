"""Specific schemas for Telegram integration."""

from datetime import datetime
from typing import Literal

from pydantic import Field, BaseModel

from integrations.schemas import BaseCredentials


class TelegramCredentials(BaseCredentials):
    """Credentials for Telegram Provider."""

    provider: Literal["telegram"] = Field(default="telegram")
    session_string: str = Field(..., min_length=1)


class TelegramMessage(BaseModel):
    """Telegram's necessary data about message."""

    message_id: int
    text: str
    date: datetime
    me: bool
    reply_to: int
