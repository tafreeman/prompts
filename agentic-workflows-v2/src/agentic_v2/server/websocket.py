"""WebSocket streaming for real-time execution updates."""

from __future__ import annotations

import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter(tags=["streaming"])


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        # map run_id -> list of websockets
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        if run_id not in self.connections:
            self.connections[run_id] = []
        self.connections[run_id].append(websocket)

    def disconnect(self, websocket: WebSocket, run_id: str):
        if run_id in self.connections:
            if websocket in self.connections[run_id]:
                self.connections[run_id].remove(websocket)
            if not self.connections[run_id]:
                del self.connections[run_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, run_id: str, message: dict):
        if run_id in self.connections:
            for connection in self.connections[run_id]:
                # Handle disconnected clients gracefully
                try:
                    await connection.send_json(message)
                except Exception:
                    # Let disconnect handler clean this up
                    pass


manager = ConnectionManager()


@router.websocket("/ws/execution/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    """WebSocket endpoint for real-time execution streaming.

    In a full implementation, this should:
    1. Subscribe to events for the specific run_id
    2. Stream step updates, logs, and results
    """
    await manager.connect(websocket, run_id)
    try:
        # Send initial status
        await manager.broadcast(run_id, 
            {
                "type": "connection_established",
                "run_id": run_id,
                "message": f"Connected to execution stream for {run_id}",
            }
        )

        while True:
            # Just keep the connection alive defined
            # Real implementation would push events here
            data = await websocket.receive_text()
            await websocket.send_json({"type": "echo", "data": data})

    except WebSocketDisconnect:
        manager.disconnect(websocket, run_id)
        logger.info(f"Client disconnected from execution stream: {run_id}")
    except Exception as e:
        logger.error(f"WebSocket error for {run_id}: {e}")
        manager.disconnect(websocket, run_id)
