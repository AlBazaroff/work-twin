"""Tests for exception handlers mapping."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.exception.base import BaseException
from core.exception.exception_handlers import register_exception_handlers
from core.providers.exceptions import (
    ProviderCredentialsNotFoundError,
    ProviderNotFoundError,
)


@pytest.fixture
def app():
    """FastAPI app instance with registered exception handlers."""
    app = FastAPI()
    register_exception_handlers(app)
    return app


@pytest.fixture
def client(app):
    """Test client for the FastAPI app."""
    return TestClient(app)


class TestExceptionHandlers:
    """Tests for mapping domain exceptions to HTTP responses."""

    def test_provider_not_found_handler(self, client, app):
        """Test ProviderNotFoundError maps to 404."""

        @app.get("/test-provider-not-found")
        async def route():
            raise ProviderNotFoundError("TestProvider")

        response = client.get("/test-provider-not-found")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Provider 'TestProvider' not found"
        }

    def test_provider_credentials_not_found_handler(self, client, app):
        """Test ProviderCredentialsNotFoundError maps to 404."""

        @app.get("/test-provider-creds-not-found")
        async def route():
            raise ProviderCredentialsNotFoundError("TestProvider")

        response = client.get("/test-provider-creds-not-found")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Credentials for provider 'TestProvider' not found"
        }

    def test_base_exception_handler(self, client, app):
        """Test BaseException maps to 400."""

        @app.get("/test-base-exception")
        async def route():
            raise BaseException("General error")

        response = client.get("/test-base-exception")
        assert response.status_code == 400
        assert response.json() == {"detail": "General error"}

    def test_entity_error_handler(self, client, app):
        """Test EntityError (inherits from BaseException) maps to 400."""
        from core.factory.exceptions import EntityError

        @app.get("/test-entity-error")
        async def route():
            raise EntityError("Factory error")

        response = client.get("/test-entity-error")
        assert response.status_code == 400
        assert response.json() == {"detail": "Factory error"}
