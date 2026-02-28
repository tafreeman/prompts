"""Unit tests for agentic_v2.server.auth — API key middleware."""

from __future__ import annotations

import sys
import types
from pathlib import Path

# ---------------------------------------------------------------------------
# Stub agentic_v2.server to avoid create_app() mounting ui/dist (doesn't
# exist in dev). We point __path__ to the real server directory so that
# sub-module imports (auth, websocket) still resolve correctly.
# ---------------------------------------------------------------------------
import agentic_v2

if "agentic_v2.server" not in sys.modules:
    _stub = types.ModuleType("agentic_v2.server")
    _pkg_dir = str(Path(agentic_v2.__file__).parent / "server")
    _stub.__path__ = [_pkg_dir]
    _stub.__package__ = "agentic_v2.server"
    sys.modules["agentic_v2.server"] = _stub

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from agentic_v2.server.auth import APIKeyMiddleware, _extract_token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_app(api_key: str | None = None) -> FastAPI:
    """Build a minimal FastAPI app with APIKeyMiddleware."""
    import agentic_v2.server.auth as auth_mod

    app = FastAPI()
    # Patch module-level _API_KEY for this test's app instance
    original = auth_mod._API_KEY
    auth_mod._API_KEY = api_key
    app.add_middleware(APIKeyMiddleware)

    @app.get("/api/data")
    def _data():
        return {"ok": True}

    @app.get("/api/health")
    def _health():
        return {"status": "ok"}

    @app.get("/ui/index.html")
    def _ui():
        return {"page": "ui"}

    # Restore after middleware is registered (captured by closure)
    auth_mod._API_KEY = original
    return app


# ---------------------------------------------------------------------------
# _extract_token tests
# ---------------------------------------------------------------------------

class TestExtractToken:
    def _req(self, headers: dict) -> object:
        """Create a mock Request-like object."""

        class _Headers:
            def __init__(self, h):
                self._h = {k.lower(): v for k, v in h.items()}

            def get(self, key, default=""):
                return self._h.get(key.lower(), default)

        class _Request:
            def __init__(self, h):
                self.headers = _Headers(h)

        return _Request(headers)

    def test_bearer_token_extracted(self):
        req = self._req({"Authorization": "Bearer my-secret"})
        assert _extract_token(req) == "my-secret"  # type: ignore[arg-type]

    def test_bearer_case_insensitive(self):
        req = self._req({"authorization": "bearer abc123"})
        assert _extract_token(req) == "abc123"  # type: ignore[arg-type]

    def test_x_api_key_extracted(self):
        req = self._req({"X-API-Key": "key-from-header"})
        assert _extract_token(req) == "key-from-header"  # type: ignore[arg-type]

    def test_bearer_takes_precedence_over_x_api_key(self):
        req = self._req({"Authorization": "Bearer bearer-wins", "X-API-Key": "ignored"})
        assert _extract_token(req) == "bearer-wins"  # type: ignore[arg-type]

    def test_no_headers_returns_none(self):
        req = self._req({})
        assert _extract_token(req) is None  # type: ignore[arg-type]

    def test_authorization_without_bearer_returns_none(self):
        req = self._req({"Authorization": "Basic dXNlcjpwYXNz"})
        assert _extract_token(req) is None  # type: ignore[arg-type]

    def test_whitespace_stripped_from_bearer(self):
        req = self._req({"Authorization": "Bearer   trimmed   "})
        assert _extract_token(req) == "trimmed"  # type: ignore[arg-type]

    def test_whitespace_stripped_from_x_api_key(self):
        req = self._req({"X-API-Key": "  spaced  "})
        assert _extract_token(req) == "spaced"  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Middleware integration tests (via TestClient)
# ---------------------------------------------------------------------------

class TestMiddlewareDisabled:
    """When no API key is configured, all requests pass through."""

    def setup_method(self):
        import agentic_v2.server.auth as auth_mod
        self._original = auth_mod._API_KEY
        auth_mod._API_KEY = None
        app = FastAPI()
        app.add_middleware(APIKeyMiddleware)

        @app.get("/api/data")
        def _data():
            return {"ok": True}

        self.client = TestClient(app, raise_server_exceptions=True)
        auth_mod._API_KEY = self._original

    def test_api_request_allowed_without_key(self):
        resp = self.client.get("/api/data")
        assert resp.status_code == 200


class TestMiddlewareEnabled:
    """When an API key is configured, unauthenticated requests are rejected."""

    SECRET = "super-secret-key"

    def setup_method(self):
        import agentic_v2.server.auth as auth_mod
        auth_mod._API_KEY = self.SECRET

        app = FastAPI()
        app.add_middleware(APIKeyMiddleware)

        @app.get("/api/data")
        def _data():
            return {"ok": True}

        @app.get("/api/health")
        def _health():
            return {"status": "ok"}

        @app.get("/static/app.js")
        def _static():
            return {}

        self.client = TestClient(app, raise_server_exceptions=False)

    def teardown_method(self):
        import agentic_v2.server.auth as auth_mod
        auth_mod._API_KEY = None

    def test_no_auth_returns_401(self):
        resp = self.client.get("/api/data")
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_wrong_key_returns_401(self):
        resp = self.client.get("/api/data", headers={"Authorization": "Bearer wrong"})
        assert resp.status_code == 401

    def test_correct_bearer_token_allowed(self):
        resp = self.client.get("/api/data", headers={"Authorization": f"Bearer {self.SECRET}"})
        assert resp.status_code == 200

    def test_correct_x_api_key_allowed(self):
        resp = self.client.get("/api/data", headers={"X-API-Key": self.SECRET})
        assert resp.status_code == 200

    def test_health_endpoint_bypasses_auth(self):
        resp = self.client.get("/api/health")
        assert resp.status_code == 200

    def test_non_api_route_bypasses_auth(self):
        resp = self.client.get("/static/app.js")
        assert resp.status_code == 200
