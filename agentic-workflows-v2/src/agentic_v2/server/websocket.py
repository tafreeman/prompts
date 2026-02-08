"""WebSocket streaming for real-time execution updates."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter(tags=["streaming"])


class ConnectionManager:
    """Manages active WebSocket connections with replay buffer and SSE support."""

    def __init__(self, max_buffer_size: int = 500):
        # map run_id -> list of websockets
        self.connections: dict[str, list[WebSocket]] = {}
        # Replay buffer: run_id -> list of events (for late-connecting clients)
        self.event_buffers: dict[str, list[dict[str, Any]]] = {}
        self._max_buffer_size = max_buffer_size
        # SSE listeners: run_id -> list of asyncio.Queue
        self._sse_listeners: dict[str, list[asyncio.Queue[dict[str, Any]]]] = {}

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

    async def replay(self, websocket: WebSocket, run_id: str):
        """Send buffered events to a newly connected client."""
        for event in self.event_buffers.get(run_id, []):
            try:
                await websocket.send_json(event)
            except Exception:
                break

    async def broadcast(self, run_id: str, message: dict[str, Any]):
        """Broadcast an event to all WS clients and SSE listeners for a run."""
        # Buffer the event for late-connecting clients
        if run_id not in self.event_buffers:
            self.event_buffers[run_id] = []
        buf = self.event_buffers[run_id]
        buf.append(message)
        if len(buf) > self._max_buffer_size:
            buf.pop(0)

        # Push to WebSocket clients
        if run_id in self.connections:
            for connection in self.connections[run_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass  # disconnect handler will clean up

        # Push to SSE listeners
        for queue in self._sse_listeners.get(run_id, []):
            try:
                queue.put_nowait(message)
            except asyncio.QueueFull:
                logger.warning("SSE listener queue full for run %s, dropping event", run_id)

    def register_sse_listener(
        self, run_id: str, queue: asyncio.Queue[dict[str, Any]]
    ) -> None:
        """Register an SSE listener queue for a run."""
        if run_id not in self._sse_listeners:
            self._sse_listeners[run_id] = []
        self._sse_listeners[run_id].append(queue)

    def unregister_sse_listener(
        self, run_id: str, queue: asyncio.Queue[dict[str, Any]]
    ) -> None:
        """Remove an SSE listener queue."""
        if run_id in self._sse_listeners:
            if queue in self._sse_listeners[run_id]:
                self._sse_listeners[run_id].remove(queue)
            if not self._sse_listeners[run_id]:
                del self._sse_listeners[run_id]

    def clear_buffer(self, run_id: str) -> None:
        """Clear the event buffer for a completed run."""
        self.event_buffers.pop(run_id, None)


manager = ConnectionManager()


@router.websocket("/ws/execution/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    """WebSocket endpoint for real-time execution streaming.

    On connect:
    1. Accept the connection and replay buffered events
    2. Keep alive — execution events are pushed via broadcast()
    3. Client can send ping/commands; server ignores content
    """
    await manager.connect(websocket, run_id)
    try:
        # Replay buffered events for late joiners
        await manager.replay(websocket, run_id)

        # Keep alive — events are pushed via broadcast()
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket, run_id)
        logger.info("Client disconnected from execution stream: %s", run_id)
    except Exception as e:
        logger.error("WebSocket error for %s: %s", run_id, e)
        manager.disconnect(websocket, run_id)
