"""Tests for API key authentication middleware."""

from __future__ import annotations

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient

import agentic_v2.server.auth as auth_module
from agentic_v2.server.auth import APIKeyMiddleware, _extract_token


def _make_app(api_key: str | None) -> FastAPI:
    """Create a minimal FastAPI app with auth middleware for testing."""
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware)

    @app.get("/api/run")
    async def protected_route():
        return {"data": "secret"}

    @app.get("/api/health")
    async def health_route():
        return {"status": "ok"}

    @app.get("/docs")
    async def docs_route():
        return {"docs": True}

    @app.get("/openapi.json")
    async def openapi_route():
        return {"openapi": "3.0"}

    @app.get("/static/app.js")
    async def static_route():
        return {"js": True}

    return app


class TestExtractToken:
    """Unit tests for _extract_token helper."""

    def _make_request(self, headers: dict[str, str]) -> Request:
        """Create a minimal ASGI scope for testing."""
        scope = {
            "type": "http",
            "method": "GET",
            "path": "/api/run",
            "headers": [
                (k.lower().encode(), v.encode()) for k, v in headers.items()
            ],
        }
        return Request(scope)

    def test_bearer_token_extracted(self) -> None:
        """Authorization: Bearer <key> returns the key."""
        request = self._make_request({"authorization": "Bearer test-key-123"})
        assert _extract_token(request) == "test-key-123"

    def test_bearer_case_insensitive(self) -> None:
        """'bearer' prefix is case-insensitive."""
        request = self._make_request({"authorization": "BEARER my-key"})
        assert _extract_token(request) == "my-key"

    def test_x_api_key_header_extracted(self) -> None:
        """X-API-Key header is extracted."""
        request = self._make_request({"x-api-key": "xkey-456"})
        assert _extract_token(request) == "xkey-456"

    def test_bearer_takes_precedence_over_x_api_key(self) -> None:
        """Bearer token is checked before X-API-Key."""
        request = self._make_request({
            "authorization": "Bearer bearer-key",
            "x-api-key": "x-key",
        })
        assert _extract_token(request) == "bearer-key"

    def test_no_token_returns_none(self) -> None:
        """Missing headers returns None."""
        request = self._make_request({})
        assert _extract_token(request) is None

    def test_bearer_with_extra_whitespace(self) -> None:
        """Bearer token with surrounding whitespace is stripped."""
        request = self._make_request({"authorization": "Bearer   padded-key  "})
        assert _extract_token(request) == "padded-key"

    def test_non_bearer_auth_returns_none(self) -> None:
        """Non-Bearer Authorization (e.g. Basic) returns None."""
        request = self._make_request({"authorization": "Basic dXNlcjpwYXNz"})
        assert _extract_token(request) is None


class TestAPIKeyMiddlewareNoKey:
    """Tests when AGENTIC_API_KEY is not set (auth disabled)."""

    def test_no_api_key_env_allows_all_requests(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When AGENTIC_API_KEY is unset, all requests pass through."""
        monkeypatch.setattr(auth_module, "_API_KEY", None)
        app = _make_app(api_key=None)
        client = TestClient(app)

        response = client.get("/api/run")
        assert response.status_code == 200
        assert response.json() == {"data": "secret"}


class TestAPIKeyMiddlewareWithKey:
    """Tests when AGENTIC_API_KEY is set (auth enabled)."""

    @pytest.fixture(autouse=True)
    def _set_api_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Configure a test API key for all tests in this class."""
        monkeypatch.setattr(auth_module, "_API_KEY", "test-secret-key")

    def test_valid_bearer_token_passes(self) -> None:
        """Valid Bearer token returns 200 for /api/run."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get(
            "/api/run",
            headers={"Authorization": "Bearer test-secret-key"},
        )
        assert response.status_code == 200
        assert response.json() == {"data": "secret"}

    def test_valid_x_api_key_header_passes(self) -> None:
        """Valid X-API-Key header returns 200."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get(
            "/api/run",
            headers={"X-API-Key": "test-secret-key"},
        )
        assert response.status_code == 200

    def test_invalid_token_returns_401(self) -> None:
        """Wrong token returns 401 with expected error body."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get(
            "/api/run",
            headers={"Authorization": "Bearer wrong-key"},
        )
        assert response.status_code == 401
        assert "Invalid or missing API key" in response.json()["detail"]

    def test_missing_token_returns_401(self) -> None:
        """No auth header on protected route returns 401."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get("/api/run")
        assert response.status_code == 401

    def test_health_endpoint_bypasses_auth(self) -> None:
        """GET /api/health does not require authentication."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get("/api/health")
        assert response.status_code == 200

    def test_docs_endpoint_bypasses_auth(self) -> None:
        """GET /docs bypasses auth check."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get("/docs")
        assert response.status_code == 200

    def test_non_api_routes_bypass_auth(self) -> None:
        """Non-/api/ paths (static files) are not gated."""
        app = _make_app(api_key="test-secret-key")
        client = TestClient(app)

        response = client.get("/static/app.js")
        assert response.status_code == 200
