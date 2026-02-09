"""WebSocket streaming for real-time execution updates."""

from __future__ import annotations

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter(tags=["streaming"])


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/execution/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    """WebSocket endpoint for real-time execution streaming.

    In a full implementation, this should:
    1. Subscribe to events for the specific run_id
    2. Stream step updates, logs, and results
    """
    await manager.connect(websocket)
    try:
        # Send initial status
        await websocket.send_json(
            {
                "type": "connection_established",
                "run_id": run_id,
                "message": f"Connected to execution stream for {run_id}",
            }
        )

        while True:
            # Just keep the connection alive for now
            # Real implementation would push events here
            data = await websocket.receive_text()
            await websocket.send_json({"type": "echo", "data": data})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Client disconnected from execution stream: {run_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {run_id}: {e}")
        manager.disconnect(websocket)
