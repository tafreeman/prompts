"""Memory MCP Client.

Provides a simple, local, persistent memory store exposed via MCP-style tools.

Why this exists
- VS Code MCP servers (configured in `.vscode/mcp.json`) are available to the editor,
  but Python workflows run as standalone processes and do not automatically inherit
  those servers.
- This client provides an always-available, dependency-free memory backend that
  LangChain agents (or any ToolRegistry consumer) can use.

Storage
- Persists to a JSON file (default: `.mcp_memory.json` in the current working dir)
- Values are stored as JSON-serializable objects when possible, otherwise `str(value)`.

Tools
- upsert: Store a value under a key (optionally with tags)
- get: Retrieve a value by key
- search: Naive substring search across keys/values
- list: List keys (optionally by prefix)
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from multiagent_workflows.mcp.base import (
    MCPClient,
    MCPResponse,
    MCPServerConfig,
    MCPToolSchema,
)


def _now_ms() -> int:
    return int(time.time() * 1000)


class MemoryMCPClient(MCPClient):
    """Local memory store exposed as MCP tools."""

    TOOLS: List[MCPToolSchema] = [
        MCPToolSchema(
            name="upsert",
            description="Create or update a memory entry (key -> value).",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Memory key"},
                    "value": {"description": "JSON-serializable value to store"},
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags",
                    },
                },
                "required": ["key", "value"],
            },
        ),
        MCPToolSchema(
            name="get",
            description="Get a memory entry by key.",
            input_schema={
                "type": "object",
                "properties": {
                    "key": {"type": "string", "description": "Memory key"},
                },
                "required": ["key"],
            },
        ),
        MCPToolSchema(
            name="list",
            description="List memory keys (optionally filter by prefix).",
            input_schema={
                "type": "object",
                "properties": {
                    "prefix": {
                        "type": "string",
                        "description": "Optional key prefix filter",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max keys to return (default 100)",
                    },
                },
            },
        ),
        MCPToolSchema(
            name="search",
            description="Search memory by substring match over keys/values.",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return (default 10)",
                    },
                },
                "required": ["query"],
            },
        ),
    ]

    def __init__(
        self,
        storage_path: Optional[str] = None,
        config: Optional[MCPServerConfig] = None,
    ):
        if config is None:
            config = MCPServerConfig(
                name="memory",
                server_type="memory",
                capabilities=["store", "search"],
            )
        super().__init__(config)

        env_path = os.environ.get("MCP_MEMORY_PATH")
        self._storage_path = Path(
            storage_path or env_path or ".mcp_memory.json"
        ).resolve()
        self._lock = threading.Lock()
        self._tools = self.TOOLS.copy()

    async def connect(self) -> bool:
        # Ensure storage file exists.
        with self._lock:
            if not self._storage_path.exists():
                self._storage_path.parent.mkdir(parents=True, exist_ok=True)
                self._storage_path.write_text("{}", encoding="utf-8")
        self.connected = True
        return True

    async def disconnect(self) -> None:
        self.connected = False

    async def list_tools(self) -> List[MCPToolSchema]:
        return self._tools

    async def invoke_tool(
        self, tool_name: str, arguments: Dict[str, Any]
    ) -> MCPResponse:
        try:
            if tool_name == "upsert":
                result = self._upsert(arguments)
            elif tool_name == "get":
                result = self._get(arguments)
            elif tool_name == "list":
                result = self._list(arguments)
            elif tool_name == "search":
                result = self._search(arguments)
            else:
                return MCPResponse(
                    success=False, result=None, error=f"Unknown tool: {tool_name}"
                )

            return MCPResponse(success=True, result=result)
        except Exception as e:
            return MCPResponse(success=False, result=None, error=str(e))

    # ---------------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------------

    def _load(self) -> Dict[str, Any]:
        if not self._storage_path.exists():
            return {}
        raw = self._storage_path.read_text(encoding="utf-8").strip()
        if not raw:
            return {}
        return json.loads(raw)

    def _save(self, data: Dict[str, Any]) -> None:
        self._storage_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._storage_path.with_suffix(self._storage_path.suffix + ".tmp")
        tmp_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        tmp_path.replace(self._storage_path)

    def _normalize_value(self, value: Any) -> Any:
        # Ensure JSON serializability.
        try:
            json.dumps(value)
            return value
        except TypeError:
            return str(value)

    def _upsert(self, args: Dict[str, Any]) -> Dict[str, Any]:
        key = str(args["key"]).strip()
        if not key:
            raise ValueError("key must be non-empty")

        value = self._normalize_value(args.get("value"))
        tags = args.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]

        with self._lock:
            data = self._load()
            data[key] = {
                "value": value,
                "tags": [str(t) for t in tags],
                "updated_at_ms": _now_ms(),
            }
            self._save(data)

        return {"key": key, "stored": True}

    def _get(self, args: Dict[str, Any]) -> Dict[str, Any]:
        key = str(args["key"]).strip()
        with self._lock:
            data = self._load()
            entry = data.get(key)

        return {"key": key, "found": entry is not None, "entry": entry}

    def _list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        prefix = (args.get("prefix") or "").strip()
        limit = int(args.get("limit") or 100)

        with self._lock:
            data = self._load()

        keys = sorted(data.keys())
        if prefix:
            keys = [k for k in keys if k.startswith(prefix)]
        keys = keys[: max(0, limit)]

        return {"keys": keys, "count": len(keys)}

    def _search(self, args: Dict[str, Any]) -> Dict[str, Any]:
        query = str(args["query"]).strip().lower()
        limit = int(args.get("limit") or 10)

        with self._lock:
            data = self._load()

        hits = []
        for key, entry in data.items():
            haystacks = [key]
            if isinstance(entry, dict) and "value" in entry:
                try:
                    haystacks.append(json.dumps(entry["value"], ensure_ascii=False))
                except TypeError:
                    haystacks.append(str(entry["value"]))
            else:
                haystacks.append(str(entry))

            if any(query in h.lower() for h in haystacks):
                hits.append({"key": key, "entry": entry})
                if len(hits) >= limit:
                    break

        return {"query": query, "results": hits, "count": len(hits)}
