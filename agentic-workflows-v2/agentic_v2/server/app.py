"""FastAPI application for agentic workflows v2."""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import websocket
from .routes import agents, health, workflows

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Built frontend assets directory
UI_DIST_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ui" / "dist"


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

    # Serve built frontend in production (after API routes so they take priority)
    if UI_DIST_DIR.exists():
        # Serve static assets (JS, CSS, etc.)
        app.mount("/assets", StaticFiles(directory=str(UI_DIST_DIR / "assets")), name="assets")

        # SPA fallback: serve index.html for all non-API, non-asset routes
        index_html = UI_DIST_DIR / "index.html"

        @app.get("/{path:path}")
        async def spa_fallback(request: Request, path: str):
            # Serve actual files if they exist in dist/
            file_path = UI_DIST_DIR / path
            if path and file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(index_html)

        logger.info("Serving UI from %s", UI_DIST_DIR)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting Agentic Workflows V2 Server")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down Agentic Workflows V2 Server")

    return app


# Create global app instance
app = create_app()
