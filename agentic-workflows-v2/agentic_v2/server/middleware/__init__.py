"""ASGI middleware wrappers for the Agentic Workflows V2 server."""

from __future__ import annotations

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class SanitizationASGIMiddleware(BaseHTTPMiddleware):
    """Starlette BaseHTTPMiddleware that applies prompt sanitization to JSON request bodies.

    Reads ``app.state.sanitization`` (a :class:`~agentic_v2.middleware.sanitization.SanitizationMiddleware`
    instance) to process incoming request bodies.  Only JSON payloads are
    inspected; all other content types pass through unchanged.

    Classifications:
        * ``clean`` / ``requires_approval`` — pass through unmodified.
        * ``redacted`` — replace the request body with the sanitized text.
        * ``blocked`` — return HTTP 422 immediately.
    """

    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        sanitizer = getattr(request.app.state, "sanitization", None)
        if sanitizer is None:
            return await call_next(request)

        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            return await call_next(request)

        try:
            body_bytes = await request.body()
            body_text = body_bytes.decode("utf-8", errors="replace")
            result = await sanitizer.process(body_text, {"source": "api_request"})

            if result.classification == "blocked":
                return JSONResponse(
                    status_code=422,
                    content={"detail": "Request blocked by sanitization policy"},
                )

            if result.classification == "redacted":
                # Rebuild request with sanitized body
                sanitized = result.sanitized_text.encode("utf-8")

                async def receive():
                    return {"type": "http.request", "body": sanitized, "more_body": False}

                request = Request(request.scope, receive)
        except Exception:
            logger.exception("Sanitization middleware error — passing request through")

        return await call_next(request)
