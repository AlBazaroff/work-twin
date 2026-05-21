"""Configuration for telegram integration tests."""

import pytest
from uuid6 import uuid7

from integrations.telegram.providers import TelegramProvider
from integrations.telegram.schemas import TelegramCredentials


@pytest.fixture
def provider():
    return TelegramProvider(api_id=1, api_hash="test_hash")


@pytest.fixture
def user_id():
    return uuid7()


@pytest.fixture
def credentials(valid_tg_session_string):
    return TelegramCredentials(session_string=valid_tg_session_string)
