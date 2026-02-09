"""FastAPI application for agentic workflows v2."""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import websocket
from .routes import agents, health, workflows

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Agentic Workflows V2 API",
        description="REST API for multi-model AI workflow orchestration",
        version="0.1.0",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(health.router, prefix="/api")
    app.include_router(agents.router, prefix="/api")
    app.include_router(workflows.router, prefix="/api")
    app.include_router(websocket.router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Agentic Workflows V2 Server")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Agentic Workflows V2 Server")

    return app


# Create global app instance
app = create_app()
