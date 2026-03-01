"""Unit tests for agentic_v2.server.websocket — ConnectionManager."""

from __future__ import annotations

import asyncio
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Stub agentic_v2.server package to avoid create_app() static-file mount.
# ---------------------------------------------------------------------------
import agentic_v2

if "agentic_v2.server" not in sys.modules:
    _stub = types.ModuleType("agentic_v2.server")
    _pkg_dir = str(Path(agentic_v2.__file__).parent / "server")
    _stub.__path__ = [_pkg_dir]
    _stub.__package__ = "agentic_v2.server"
    sys.modules["agentic_v2.server"] = _stub

from agentic_v2.server.websocket import ConnectionManager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_ws() -> MagicMock:
    ws = MagicMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestConnectDisconnect:
    async def test_connect_accepts_websocket(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        await mgr.connect(ws, "run-1")
        ws.accept.assert_awaited_once()

    async def test_connect_registers_under_run_id(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        await mgr.connect(ws, "run-1")
        assert ws in mgr.connections["run-1"]

    async def test_multiple_clients_same_run(self):
        mgr = ConnectionManager()
        ws1, ws2 = _mock_ws(), _mock_ws()
        await mgr.connect(ws1, "run-1")
        await mgr.connect(ws2, "run-1")
        assert len(mgr.connections["run-1"]) == 2

    async def test_disconnect_removes_client(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        await mgr.connect(ws, "run-1")
        mgr.disconnect(ws, "run-1")
        assert "run-1" not in mgr.connections

    async def test_disconnect_cleans_empty_run(self):
        mgr = ConnectionManager()
        ws1, ws2 = _mock_ws(), _mock_ws()
        await mgr.connect(ws1, "run-1")
        await mgr.connect(ws2, "run-1")
        mgr.disconnect(ws1, "run-1")
        assert ws1 not in mgr.connections["run-1"]
        assert ws2 in mgr.connections["run-1"]

    def test_disconnect_unknown_run_is_safe(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        mgr.disconnect(ws, "no-such-run")  # must not raise


class TestBroadcast:
    async def test_broadcast_sends_to_connected_ws(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        await mgr.connect(ws, "run-1")
        await mgr.broadcast("run-1", {"type": "step_complete"})
        ws.send_json.assert_awaited_once_with({"type": "step_complete"})

    async def test_broadcast_buffers_event(self):
        mgr = ConnectionManager()
        await mgr.broadcast("run-1", {"type": "start"})
        assert mgr.event_buffers["run-1"] == [{"type": "start"}]

    async def test_broadcast_to_sse_listener(self):
        mgr = ConnectionManager()
        q: asyncio.Queue = asyncio.Queue()
        mgr.register_sse_listener("run-1", q)
        await mgr.broadcast("run-1", {"type": "progress"})
        assert q.qsize() == 1
        assert q.get_nowait() == {"type": "progress"}

    async def test_broadcast_tolerates_failed_ws(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        ws.send_json = AsyncMock(side_effect=Exception("disconnected"))
        await mgr.connect(ws, "run-1")
        # Must not raise
        await mgr.broadcast("run-1", {"type": "event"})

    async def test_broadcast_no_listeners_is_safe(self):
        mgr = ConnectionManager()
        await mgr.broadcast("run-with-no-clients", {"type": "done"})


class TestReplayBuffer:
    async def test_replay_sends_buffered_events(self):
        mgr = ConnectionManager()
        await mgr.broadcast("run-1", {"seq": 1})
        await mgr.broadcast("run-1", {"seq": 2})

        late_ws = _mock_ws()
        await mgr.connect(late_ws, "run-1")
        await mgr.replay(late_ws, "run-1")

        assert late_ws.send_json.await_count == 2

    async def test_replay_empty_buffer_sends_nothing(self):
        mgr = ConnectionManager()
        ws = _mock_ws()
        await mgr.connect(ws, "run-1")
        await mgr.replay(ws, "run-1")
        ws.send_json.assert_not_awaited()

    async def test_buffer_enforces_max_size(self):
        mgr = ConnectionManager(max_buffer_size=3)
        for i in range(5):
            await mgr.broadcast("run-1", {"seq": i})
        assert len(mgr.event_buffers["run-1"]) == 3
        # Oldest events evicted; last 3 remain
        assert mgr.event_buffers["run-1"][-1] == {"seq": 4}

    async def test_clear_buffer_removes_events(self):
        mgr = ConnectionManager()
        await mgr.broadcast("run-1", {"type": "event"})
        mgr.clear_buffer("run-1")
        assert "run-1" not in mgr.event_buffers

    async def test_clear_buffer_unknown_run_is_safe(self):
        mgr = ConnectionManager()
        mgr.clear_buffer("ghost-run")


class TestSSEListeners:
    def test_register_sse_listener(self):
        mgr = ConnectionManager()
        q: asyncio.Queue = asyncio.Queue()
        mgr.register_sse_listener("run-1", q)
        assert q in mgr._sse_listeners["run-1"]

    def test_unregister_sse_listener(self):
        mgr = ConnectionManager()
        q: asyncio.Queue = asyncio.Queue()
        mgr.register_sse_listener("run-1", q)
        mgr.unregister_sse_listener("run-1", q)
        assert "run-1" not in mgr._sse_listeners

    def test_unregister_unknown_run_is_safe(self):
        mgr = ConnectionManager()
        q: asyncio.Queue = asyncio.Queue()
        mgr.unregister_sse_listener("no-such-run", q)

    async def test_full_sse_queue_does_not_raise(self):
        mgr = ConnectionManager()
        q: asyncio.Queue = asyncio.Queue(maxsize=1)
        q.put_nowait({"already": "full"})
        mgr.register_sse_listener("run-1", q)
        # Should log a warning but not raise
        await mgr.broadcast("run-1", {"overflow": True})
