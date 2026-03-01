"""WebSocket and SSE streaming for real-time workflow execution updates.

Provides :class:`ConnectionManager`, a pub/sub hub that fans out execution
events (``step_start``, ``step_end``, ``workflow_end``, etc.) to:

* **WebSocket clients** -- connected via ``/ws/execution/{run_id}``.
  Each client is associated with exactly one ``run_id``.  Late-connecting
  clients receive a replay of buffered events so they can reconstruct
  current workflow state.
* **SSE listeners** -- registered via :meth:`ConnectionManager.register_sse_listener`
  using an ``asyncio.Queue``.  The ``GET /runs/{run_id}/stream`` endpoint
  in the workflows router consumes this queue.

Architecture:
    ``broadcast(run_id, event)`` is the single write path.  It appends
    the event to a per-run circular buffer (default 500 events), then
    pushes to all WebSocket connections *and* all SSE queues for that
    ``run_id``.  Disconnection cleanup is handled per-client; the buffer
    persists until :meth:`ConnectionManager.clear_buffer` is called.

A module-level singleton ``manager`` is used by both the WebSocket
endpoint and the workflow execution background task.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter(tags=["streaming"])


class ConnectionManager:
    """Pub/sub hub for WebSocket connections and SSE listeners, keyed by run ID.

    Maintains three per-run data structures:

    * ``connections`` -- list of accepted ``WebSocket`` instances.
    * ``event_buffers`` -- circular list of JSON-serializable event dicts
      (capped at ``max_buffer_size``) used to replay history to
      late-connecting clients.
    * ``_sse_listeners`` -- list of ``asyncio.Queue`` instances that
      receive the same events for Server-Sent Event streaming.

    Attributes:
        connections: Mapping of ``run_id`` to active WebSocket list.
        event_buffers: Mapping of ``run_id`` to buffered event list.
        _max_buffer_size: Maximum events retained per run (default 500).
        _sse_listeners: Mapping of ``run_id`` to SSE queue list.
    """

    def __init__(self, max_buffer_size: int = 500):
        """Initialize the connection manager.

        Args:
            max_buffer_size: Maximum number of events to retain in the
                per-run replay buffer.  Oldest events are evicted when
                the limit is exceeded.
        """
        # map run_id -> list of websockets
        self.connections: dict[str, list[WebSocket]] = {}
        # Replay buffer: run_id -> list of events (for late-connecting clients)
        self.event_buffers: dict[str, list[dict[str, Any]]] = {}
        self._max_buffer_size = max_buffer_size
        # SSE listeners: run_id -> list of asyncio.Queue
        self._sse_listeners: dict[str, list[asyncio.Queue[dict[str, Any]]]] = {}

    async def connect(self, websocket: WebSocket, run_id: str):
        """Accept a WebSocket connection and associate it with a run.

        Args:
            websocket: The incoming WebSocket to accept.
            run_id: Workflow run identifier to subscribe to.
        """
        await websocket.accept()
        if run_id not in self.connections:
            self.connections[run_id] = []
        self.connections[run_id].append(websocket)

    def disconnect(self, websocket: WebSocket, run_id: str):
        """Remove a WebSocket from the run's connection list.

        Args:
            websocket: The disconnected WebSocket instance.
            run_id: The run identifier the socket was subscribed to.
        """
        if run_id in self.connections:
            if websocket in self.connections[run_id]:
                self.connections[run_id].remove(websocket)
            if not self.connections[run_id]:
                del self.connections[run_id]

    async def replay(self, websocket: WebSocket, run_id: str):
        """Send all buffered events to a newly connected client.

        Args:
            websocket: The freshly accepted WebSocket.
            run_id: Run whose event history should be replayed.
        """
        for event in self.event_buffers.get(run_id, []):
            try:
                await websocket.send_json(event)
            except Exception:
                break

    async def broadcast(self, run_id: str, message: dict[str, Any]):
        """Broadcast an event to all WebSocket clients and SSE listeners for a run.

        The event is first appended to the run's replay buffer (evicting
        the oldest entry if the buffer exceeds ``_max_buffer_size``), then
        pushed to every WebSocket connection and every SSE queue registered
        for the given ``run_id``.

        Args:
            run_id: Target workflow run identifier.
            message: JSON-serializable event dict to broadcast.
        """
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
        """Register an asyncio queue to receive broadcast events via SSE.

        Args:
            run_id: Run identifier to subscribe to.
            queue: Bounded asyncio queue that will receive event dicts.
        """
        if run_id not in self._sse_listeners:
            self._sse_listeners[run_id] = []
        self._sse_listeners[run_id].append(queue)

    def unregister_sse_listener(
        self, run_id: str, queue: asyncio.Queue[dict[str, Any]]
    ) -> None:
        """Remove a previously registered SSE listener queue.

        Args:
            run_id: Run identifier the queue was subscribed to.
            queue: The queue instance to remove.
        """
        if run_id in self._sse_listeners:
            if queue in self._sse_listeners[run_id]:
                self._sse_listeners[run_id].remove(queue)
            if not self._sse_listeners[run_id]:
                del self._sse_listeners[run_id]

    def clear_buffer(self, run_id: str) -> None:
        """Clear the replay event buffer for a completed run.

        Args:
            run_id: Run identifier whose buffer should be freed.
        """
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
