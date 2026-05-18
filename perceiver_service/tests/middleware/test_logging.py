"""Test for logging middlewares."""

import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.const.errors.base import INTERNAL_ERROR_MESSAGE
from middlewares.logging import (
    CorrelationIdMiddleware,
    EnhancedLoggingMiddleware,
)

ROOT_PATH = "/"
ERROR_PATH = "/error"


@pytest.fixture
def fake_app():
    """Create a fake FastAPI app with the logging middlewares"""
    app = FastAPI()
    app.add_middleware(EnhancedLoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)

    @app.get(ROOT_PATH)
    async def root():
        return {"message": "Hello World"}

    @app.get(ERROR_PATH)
    async def error():
        raise ValueError("Test error")

    return app


class TestCorrelationIdMiddleware:
    """Tests cases for CorrelationIdMiddleware."""

    def test_adds_correlation_id_header(self, client: TestClient):
        """
        Test that the middleware add a correlation ID header
        to the response.
        """
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers.get("X-Correlation-ID")

    def test_get_correlation_id_from_request(self, client: TestClient):
        """
        Test that the middleware uses the correlation ID from
        the request header if provided. And return the same ID
        """
        correlation_id = str(uuid.uuid4())
        response = client.get(
            "/health", headers={"X-Correlation-ID": correlation_id}
        )
        assert response.status_code == 200
        assert response.headers.get("X-Correlation-ID") == correlation_id


class TestEnhancedLoggingMiddleware:
    """Test cases for EnhancedLoggingMiddleware"""

    def test_internal_error_handling(self, fake_app: FastAPI):
        """
        Test correctness of internal error message,
        must raise INTERNAL_ERROR_MESSAGE.
        """
        with TestClient(fake_app) as client:
            response = client.get(ERROR_PATH)
            assert response.status_code == 500

            data = response.json()
            assert data["error"] == INTERNAL_ERROR_MESSAGE
