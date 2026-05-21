"""Test personality dna views."""

import pytest
from fastapi import status
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
class TestPersonalityDNARoutes:
    """Test personality_dna routes."""

    @patch(
        "personality_dna.views.get_active_by_user_id",
        new_callable=AsyncMock,
    )
    async def test_personality_dna_returns_personality(
        self, mock_get_active, active_personality_dna, client
    ):
        """
        Test that personality_dna returns personality.
        And data prevented leaks.
        """
        mock_get_active.return_value = active_personality_dna

        response = client.get(
            f"/twin/personality_dna/{active_personality_dna['id']}"
        )
        mock_get_active.assert_awaited_once()
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert data["style_markers"] == active_personality_dna["style_markers"]
        assert data["core_facts"] == active_personality_dna["core_facts"]
        assert data["preferences"] == active_personality_dna["preferences"]
        assert "id" not in data
        assert "user_id" not in data

    @patch(
        "personality_dna.views.get_active_by_user_id",
        new_callable=AsyncMock,
    )
    async def test_personality_dna_returns_not_found(
        self, mock_get_active, active_personality_dna, client
    ):
        """Test that personality_dna returns HttpException."""
        mock_get_active.return_value = None

        response = client.get(
            f"/twin/personality_dna/{active_personality_dna['id']}"
        )
        mock_get_active.assert_awaited_once()
        assert response.status_code == status.HTTP_404_NOT_FOUND

        data = response.json()

        assert "detail" in data
        assert "msg" in data["detail"]
