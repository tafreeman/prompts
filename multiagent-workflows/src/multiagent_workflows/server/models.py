from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ModelRecord:
    """A UI/API-friendly model record."""

    id: str
    provider_group: str
    selectable: bool
    usable: Optional[bool] = None
    error: Optional[str] = None


def _now_ms() -> int:
    return int(time.time() * 1000)


class ModelRegistry:
    """Keeps a cached snapshot of model discovery + probe results.

    Design goals:
    - Server starts fast: discovery runs in the background.
    - UI can list models immediately (maybe empty or stale).
    - Selecting a model triggers a lightweight probe check.

    Note: We intentionally avoid probing every model at startup.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._discovery: Optional[Dict[str, Any]] = None
        self._discover_status: str = "idle"  # idle|running|done|error
        self._discover_error: Optional[str] = None
        self._discover_started_at_ms: Optional[int] = None
        self._discover_finished_at_ms: Optional[int] = None
        self._discover_task: Optional[asyncio.Task] = None

        # Probe is cache-backed, so instantiating it is cheap.
        self._probe = None

    def snapshot(self) -> Dict[str, Any]:
        providers = (self._discovery or {}).get("providers") or {}
        models = self._flatten_discovery(providers)
        return {
            "status": self._discover_status,
            "error": self._discover_error,
            "started_at_ms": self._discover_started_at_ms,
            "finished_at_ms": self._discover_finished_at_ms,
            "models": [m.__dict__ for m in models],
            "providers": providers,
        }

    async def start_background_discovery(self) -> None:
        async with self._lock:
            if self._discover_task and not self._discover_task.done():
                return
            self._discover_task = asyncio.create_task(self.refresh())

    async def refresh(self) -> None:
        async with self._lock:
            self._discover_status = "running"
            self._discover_error = None
            self._discover_started_at_ms = _now_ms()
            self._discover_finished_at_ms = None

        try:
            # Import lazily so the server can still start even if tools/ isn't importable.
            from tools.llm.model_probe import discover_all_models  # type: ignore

            # Discovery can touch subprocesses + network. Run it off the event loop.
            data = await asyncio.to_thread(discover_all_models, verbose=False)

            async with self._lock:
                self._discovery = data
                self._discover_status = "done"
                self._discover_finished_at_ms = _now_ms()
        except Exception as e:
            async with self._lock:
                self._discover_status = "error"
                self._discover_error = str(e)
                self._discover_finished_at_ms = _now_ms()

    def _get_probe(self):
        if self._probe is None:
            from tools.llm.model_probe import ModelProbe  # type: ignore

            self._probe = ModelProbe(use_cache=True, verbose=False)
        return self._probe

    def check_model(self, model_id: str) -> Dict[str, Any]:
        """Return a probe result dict for a model."""
        probe = self._get_probe()
        res = probe.check_model(model_id)
        # ProbeResult has to_dict().
        return (
            res.to_dict()
            if hasattr(res, "to_dict")
            else {
                "model": model_id,
                "usable": bool(getattr(res, "usable", False)),
                "error_message": getattr(res, "error_message", None),
            }
        )

    @staticmethod
    def _flatten_discovery(providers: Dict[str, Any]) -> List[ModelRecord]:
        out: List[ModelRecord] = []

        # Mirror tools.llm.llm_client.LLMClient's safe-by-default policy.
        allow_remote = (os.getenv("PROMPTEVAL_ALLOW_REMOTE") or "").strip().lower() in {
            "1",
            "true",
            "yes",
            "y",
            "on",
        }
        default_allowed_prefixes = (
            "local:",
            "gh:",
            "windows-ai:",
            "ollama:",
            "aitk:",
            "ai-toolkit:",
        )

        for provider_group, info in providers.items():
            available = info.get("available") or []
            missing = info.get("missing") or []
            error = info.get("error")

            for mid in available:
                mid_s = str(mid)
                if (not allow_remote) and (
                    not mid_s.lower().startswith(default_allowed_prefixes)
                ):
                    out.append(
                        ModelRecord(
                            id=mid_s,
                            provider_group=str(provider_group),
                            selectable=False,
                            usable=False,
                            error="remote providers disabled (set PROMPTEVAL_ALLOW_REMOTE=1)",
                        )
                    )
                    continue
                out.append(
                    ModelRecord(
                        id=mid_s,
                        provider_group=str(provider_group),
                        selectable=True,
                        usable=None,
                        error=None,
                    )
                )

            for mid in missing:
                out.append(
                    ModelRecord(
                        id=str(mid),
                        provider_group=str(provider_group),
                        selectable=False,
                        usable=False,
                        error=error or "not installed / not available",
                    )
                )

        # Stable ordering: selectable first, then by provider group, then id.
        out.sort(key=lambda m: (not m.selectable, m.provider_group, m.id))
        return out
