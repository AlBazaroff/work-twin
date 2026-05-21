"""Configuration for tests with Personality DNA."""

import pytest
from uuid6 import uuid7


@pytest.fixture
def active_personality_dna() -> dict:
    """Return data for personality DNA."""
    return {
        "id": uuid7(),
        "user_id": uuid7(),
        "style_markers": {"openness": 0.8, "conscientiousness": 0.6},
        "core_facts": {"age": 30, "location": "New York"},
        "preferences": {"likes_coffee": True, "uses_swearing": True},
        "version": 1,
        "is_active": True,
    }
