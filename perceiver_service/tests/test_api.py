"""Tests for health endpoints."""

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Test base health endpoints."""

    def test_health_returns_ok(self, client: TestClient):
        """Test '/health' endpoint returns status 'ok'"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ok"

    def test_ready_returns_ready(self, client: TestClient):
        """Test '/ready' endpoint return status 'ready'"""
        response = client.get("/ready")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "ready"
