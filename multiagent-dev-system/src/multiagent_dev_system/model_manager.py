"""Model manager integrating repository model access patterns."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from tools.llm.llm_client import LLMClient
from tools.llm.model_probe import discover_all_models, get_probe


@dataclass
class ModelChoice:
    model_id: str
    provider: str
    available: bool


class ModelManager:
    """Unified model manager for local and cloud providers."""

    def __init__(self, allow_remote: bool = False):
        self.allow_remote = allow_remote
        self._probe = get_probe()

    async def generate(self, model_id: str, prompt: str, context: Optional[str] = None, **params: Any) -> str:
        full_prompt = prompt if context is None else f"{context}\n\n{prompt}"
        return await asyncio.to_thread(
            LLMClient.generate_text,
            model_name=model_id,
            prompt=full_prompt,
            system_instruction=params.get("system_instruction"),
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 2048),
        )

    async def check_availability(self, model_id: str) -> bool:
        return await asyncio.to_thread(self._probe.check_model, model_id)

    async def list_models(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        discovered = await asyncio.to_thread(discover_all_models, False)
        models: List[Dict[str, Any]] = []
        providers = discovered.get("providers", {})
        for name, info in providers.items():
            if provider and provider != name:
                continue
            for m in info.get("available", []) or []:
                models.append({"provider": name, "model": m})
        return models

    def get_optimal_model(self, task_type: str, complexity: str, prefer_local: bool) -> str:
        task_type = task_type.lower()
        complexity = complexity.lower()

        local_fallbacks = [
            "local:phi4mini",
            "local:phi3.5",
            "local:mistral",
        ]
        cloud_map = {
            "analysis": "gh:gpt-5",
            "refactor": "gh:gpt-4.1",
            "bugfix": "gh:gpt-4.1",
            "architecture": "gh:gpt-5-mini",
            "docs": "gh:gpt-4.1-mini",
            "tests": "gh:gpt-4.1",
        }
        preferred_cloud = cloud_map.get(task_type, "gh:gpt-4.1-mini")

        if prefer_local:
            for model in local_fallbacks:
                if self._probe.check_model(model).usable:
                    return model
            return preferred_cloud

        if complexity in {"high", "critical"}:
            return preferred_cloud
        if complexity in {"medium", "normal"}:
            return cloud_map.get(task_type, "gh:gpt-4.1-mini")
        return local_fallbacks[0]
