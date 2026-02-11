"""Health check routes."""

from __future__ import annotations

from fastapi import APIRouter

from ..models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if server is alive."""
    return HealthResponse()
