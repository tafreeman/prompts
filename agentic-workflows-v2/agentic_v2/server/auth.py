"""API key authentication middleware.

When ``AGENTIC_API_KEY`` is set, every request to ``/api/`` (except
``/api/health``) must include a matching ``Authorization: Bearer <key>``
or ``X-API-Key: <key>`` header.

When the env var is *not* set, authentication is disabled and all
requests are allowed (local development mode).
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
    """Reject unauthenticated API requests when an API key is configured."""

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
