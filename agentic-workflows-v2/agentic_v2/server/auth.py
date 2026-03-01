"""API key authentication middleware for the Agentic server.

Implements a single-key bearer-token gate using Starlette's
``BaseHTTPMiddleware``.

Authentication behavior:
    * When ``AGENTIC_API_KEY`` is set in the environment, every HTTP
      request whose path starts with ``/api/`` (except public prefixes
      like ``/api/health``, ``/docs``, ``/openapi.json``, ``/redoc``)
      must supply the key via ``Authorization: Bearer <key>`` or the
      ``X-API-Key: <key>`` header.  Token comparison uses
      :func:`secrets.compare_digest` to prevent timing side-channels.
    * When the env var is **not** set, the middleware is a no-op and all
      requests are allowed (local development mode).
    * Non-API routes (UI static files, WebSocket upgrade) bypass
      authentication entirely so the React frontend can load without
      credentials.
"""

from __future__ import annotations

import os
import secrets

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

_API_KEY: str | None = os.environ.get("AGENTIC_API_KEY") or None

# Paths that bypass authentication
_PUBLIC_PREFIXES = ("/api/health", "/docs", "/openapi.json", "/redoc")


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Starlette middleware that enforces bearer-token authentication on ``/api/`` routes.

    When ``AGENTIC_API_KEY`` is not set, all requests pass through unchanged.
    Otherwise, requests to protected paths must include a valid token via
    ``Authorization: Bearer <key>`` or ``X-API-Key: <key>``.  Invalid or
    missing tokens receive a ``401`` JSON response.

    Attributes:
        Inherits from ``BaseHTTPMiddleware``; no additional instance state.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        if _API_KEY is None:
            return await call_next(request)

        path = request.url.path

        # Allow public endpoints and non-API routes (UI static files)
        if not path.startswith("/api/"):
            return await call_next(request)
        for prefix in _PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        # Check for API key in headers
        token = _extract_token(request)
        if token is None or not secrets.compare_digest(token, _API_KEY):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API key"},
            )

        return await call_next(request)


def _extract_token(request: Request) -> str | None:
    """Extract API key from Authorization or X-API-Key header."""
    # Try Authorization: Bearer <key>
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()

    # Try X-API-Key header
    api_key_header = request.headers.get("x-api-key")
    if api_key_header:
        return api_key_header.strip()

    return None
