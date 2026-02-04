"""Smart Model Router with Rate Limit Handling, Provider Fallback, and Adaptive
Learning.

Features:
- Automatic retry on rate limits (429)
- Provider fallback chain (cloud → local)
- Load balancing across providers
- Model tier awareness for task complexity
- Adaptive learning: tracks failures and adjusts priorities
- Premium model escalation when needed
- Persistence of learning across sessions
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ModelStats:
    """Track individual model performance."""

    model_id: str
    success_count: int = 0
    failure_count: int = 0
    total_latency_ms: float = 0.0
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    last_error: Optional[str] = None
    consecutive_failures: int = 0
    is_disabled: bool = False
    disabled_until: Optional[datetime] = None

    @property
    def failure_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.failure_count / total if total > 0 else 0.0

    @property
    def avg_latency_ms(self) -> float:
        return (
            self.total_latency_ms / self.success_count
            if self.success_count > 0
            else 0.0
        )

    def mark_success(self, latency_ms: float):
        self.success_count += 1
        self.total_latency_ms += latency_ms
        self.last_success = datetime.now()
        self.consecutive_failures = 0
        self.is_disabled = False
        self.disabled_until = None

    def mark_failure(self, error: str, disable_threshold: int = 3):
        self.failure_count += 1
        self.consecutive_failures += 1
        self.last_failure = datetime.now()
        self.last_error = error

        # Disable after consecutive failures with exponential backoff
        if self.consecutive_failures >= disable_threshold:
            backoff_minutes = min(
                2 ** (self.consecutive_failures - disable_threshold), 60
            )
            self.disabled_until = datetime.now() + timedelta(minutes=backoff_minutes)
            self.is_disabled = True
            logger.warning(
                f"Model {self.model_id} disabled for {backoff_minutes}m after {self.consecutive_failures} failures"
            )

    def is_available(self) -> bool:
        if not self.is_disabled:
            return True
        if self.disabled_until and datetime.now() > self.disabled_until:
            # Re-enable after backoff
            self.is_disabled = False
            self.disabled_until = None
            return True
        return False


@dataclass
class ProviderStatus:
    """Track provider health and rate limits."""

    name: str
    available: bool = True
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None
    rate_limit_until: Optional[datetime] = None
    request_count: int = 0
    error_count: int = 0
    avg_latency_ms: float = 0.0
    priority_penalty: int = 0  # Increases with failures, decreases priority

    def is_rate_limited(self) -> bool:
        if self.rate_limit_until is None:
            return False
        return datetime.now() < self.rate_limit_until

    def mark_rate_limited(self, retry_after: int = 60):
        """Mark provider as rate limited."""
        self.rate_limit_until = datetime.now() + timedelta(seconds=retry_after)
        self.priority_penalty += 1  # Penalize provider
        logger.warning(
            f"Provider {self.name} rate limited until {self.rate_limit_until}"
        )

    def mark_success(self, latency_ms: float):
        """Record successful request."""
        self.request_count += 1
        # Running average
        self.avg_latency_ms = (
            self.avg_latency_ms * (self.request_count - 1) + latency_ms
        ) / self.request_count
        self.available = True
        # Slowly reduce penalty on success
        if self.priority_penalty > 0:
            self.priority_penalty = max(0, self.priority_penalty - 0.1)

    def mark_error(self, error: str):
        """Record error."""
        self.error_count += 1
        self.last_error = error
        self.last_error_time = datetime.now()
        self.priority_penalty += 1
        # Disable after many consecutive errors
        if self.error_count >= 5:
            self.available = False
            logger.error(
                f"Provider {self.name} disabled after {self.error_count} errors"
            )


@dataclass
class ModelConfig:
    """Configuration for a model."""

    model_id: str
    provider: str
    tier: int  # 0=no-llm, 1=small, 2=medium, 3=large
    max_tokens: int = 4096
    supports_vision: bool = False
    supports_tools: bool = True
    cost_per_1k_tokens: float = 0.0  # 0 = free/local


# Model tier definitions with fallback chains.
#
# Repo expectation (2026-02): prefer free/cheap sources first.
# Desired high-level provider order:
#   GitHub Models (gh) -> Ollama (ollama) -> Gemini (gemini) -> Local ONNX (local)
#
# Note: actual selection is also filtered by discovery availability and provider health.
MODEL_TIERS = {
    0: {
        "name": "no_llm",
        "description": "Pure Python - no LLM needed",
        "models": [],  # No models needed
    },
    1: {
        "name": "small",
        "description": "Simple tasks (1-3B params)",
        "models": [
            # Cloud first - GitHub Models (free tier)
            "gh:microsoft/phi-4-mini-instruct",
            "gh:microsoft/phi-3.5-mini-instruct",
            "gh:openai/gpt-4.1-nano",
            # Local fallback
            "ollama:gemma3:4b",
            "ollama:gemma3:1b",
            # Remote fallback (optional)
            "gemini:gemini-1.5-flash",
            "local:phi4mini",
            "local:phi3.5",
        ],
    },
    2: {
        "name": "medium",
        "description": "Code generation (7-14B params)",
        "models": [
            # Cloud first - GitHub Models
            "gh:microsoft/phi-4",
            "gh:openai/gpt-4o-mini",
            "gh:openai/gpt-4.1-mini",
            "gh:cohere/command-r",
            # Local fallback
            "ollama:qwen2.5-coder:14b",
            "ollama:deepseek-r1:14b",
            "ollama:phi4-reasoning:latest",
            "ollama:qwen3:8b",
            "ollama:deepseek-r1:8b",
            # Remote fallback (optional)
            "gemini:gemini-1.5-pro",
            "local:phi4",
        ],
    },
    3: {
        "name": "large",
        "description": "Complex reasoning (32B+ or cloud)",
        "models": [
            # GitHub Models first (generous free tier)
            "gh:deepseek/deepseek-r1",
            "gh:meta/llama-3.3-70b-instruct",
            "gh:openai/gpt-4o",
            "gh:openai/o3-mini",
            "gh:openai/o4-mini",
            # Premium GitHub Models
            "gh:openai/gpt-4.1",
            "gh:openai/o1",
            "gh:anthropic/claude-sonnet-4",
            "gh:anthropic/claude-3.5-sonnet",
            # Ollama (local + cloud)
            "ollama:deepseek-v3.1:671b-cloud",
            "ollama:qwen3-coder:480b-cloud",
            "ollama:gpt-oss:120b-cloud",
            "ollama:deepseek-v3.2:cloud",
            "ollama:qwen3-vl:235b-cloud",
            "ollama:gpt-oss:20b-cloud",
            # Local large models (fallback)
            "ollama:qwen3-coder:30b",
            "ollama:gpt-oss:20b",
            "ollama:phi4-reasoning:latest",
            "ollama:qwen2.5-coder:14b",
            "ollama:deepseek-r1:14b",
            # Remote fallback (optional)
            "gemini:gemini-1.5-pro",
            # Local ONNX fallback (last in requested chain)
            "local:phi4",
            "local:mistral",
            "local:mistral-7b",
            "local:phi3-medium",
            # Paid cloud (last resort)
            "openai:gpt-4o",
            "openai:o3-mini",
            "anthropic:claude-3-5-sonnet",
        ],
    },
    # Premium tier for critical/complex tasks
    4: {
        "name": "premium",
        "description": "Highest quality (premium cloud models)",
        "models": [
            "gh:openai/o1",
            "gh:openai/o3",
            "gh:anthropic/claude-sonnet-4",
            "openai:o1",
            "openai:gpt-4-turbo",
            "anthropic:claude-3-opus",
        ],
    },
}

# Provider priority (global). Keep this aligned with LLMClient's safety gates.
# Requested default fallback order: gh -> ollama -> gemini -> local.
PROVIDER_PRIORITY = [
    "gh",  # GitHub Models (remote, but explicitly allowed by default)
    "ollama",  # Ollama (local + optional cloud)
    "gemini",  # Google Gemini (remote; requires PROMPTEVAL_ALLOW_REMOTE=1 + key)
    "local",  # Local ONNX models
    "windows_ai",  # Local Windows AI APIs (if available)
    "aitk",  # VS Code AI Toolkit local ONNX
    "azure",  # Azure (remote)
    "openai",  # OpenAI (remote)
    "anthropic",  # Anthropic (remote)
]


class SmartModelRouter:
    """Intelligent model router with rate limit handling, fallbacks, and
    adaptive learning.

    Features:
    - Tracks success/failure per model and provider
    - Adjusts priorities based on performance
    - Persists learning across sessions
    - Escalates to premium models when needed

    Usage:
        router = SmartModelRouter()
        model = router.get_model_for_tier(2)  # Get medium model

        # Or with automatic fallback on error
        result = await router.call_with_fallback(
            tier=2,
            prompt="Generate code...",
            on_rate_limit="wait"  # or "fallback" or "local"
        )
    """

    STATS_FILE = "model_router_stats.json"

    def __init__(
        self,
        discovery_path: Optional[str] = None,
        prefer_local: bool = True,
        rate_limit_strategy: str = "fallback",  # "wait", "fallback", "local"
        stats_path: Optional[str] = None,
        auto_escalate: bool = True,  # Auto-escalate to premium on repeated failures
    ):
        self.prefer_local = prefer_local
        self.rate_limit_strategy = rate_limit_strategy
        self.auto_escalate = auto_escalate
        self.provider_status: Dict[str, ProviderStatus] = {}
        self.model_stats: Dict[str, ModelStats] = {}
        self.available_models: Dict[str, List[str]] = {}
        self.stats_path = stats_path or self.STATS_FILE

        # Load discovery results
        self._load_discovery(discovery_path)

        # Initialize provider status
        for provider in PROVIDER_PRIORITY:
            self.provider_status[provider] = ProviderStatus(name=provider)

        # Load persisted stats
        self._load_stats()

    def _load_stats(self):
        """Load persisted model stats from file."""
        try:
            path = Path(self.stats_path)
            if path.exists():
                with open(path) as f:
                    data = json.load(f)

                for model_id, stats in data.get("models", {}).items():
                    self.model_stats[model_id] = ModelStats(
                        model_id=model_id,
                        success_count=stats.get("success_count", 0),
                        failure_count=stats.get("failure_count", 0),
                        total_latency_ms=stats.get("total_latency_ms", 0),
                        consecutive_failures=stats.get("consecutive_failures", 0),
                    )

                for provider, pstats in data.get("providers", {}).items():
                    if provider in self.provider_status:
                        self.provider_status[provider].priority_penalty = pstats.get(
                            "priority_penalty", 0
                        )
                        self.provider_status[provider].error_count = pstats.get(
                            "error_count", 0
                        )

                logger.info(f"Loaded stats for {len(self.model_stats)} models")
        except Exception as e:
            logger.warning(f"Could not load stats: {e}")

    def _save_stats(self):
        """Persist model stats to file."""
        try:
            data = {
                "updated": datetime.now().isoformat(),
                "models": {
                    model_id: {
                        "success_count": stats.success_count,
                        "failure_count": stats.failure_count,
                        "total_latency_ms": stats.total_latency_ms,
                        "consecutive_failures": stats.consecutive_failures,
                        "failure_rate": stats.failure_rate,
                    }
                    for model_id, stats in self.model_stats.items()
                },
                "providers": {
                    provider: {
                        "priority_penalty": status.priority_penalty,
                        "error_count": status.error_count,
                        "request_count": status.request_count,
                    }
                    for provider, status in self.provider_status.items()
                },
            }

            with open(self.stats_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save stats: {e}")

    def _get_model_stats(self, model_id: str) -> ModelStats:
        """Get or create stats for a model."""
        if model_id not in self.model_stats:
            self.model_stats[model_id] = ModelStats(model_id=model_id)
        return self.model_stats[model_id]

    def _load_discovery(self, path: Optional[str] = None):
        """Load model discovery results."""
        if path is None:
            # Try common locations
            candidates = [
                Path("discovery_results.json"),
                Path(__file__).parents[4] / "discovery_results.json",
            ]
            for p in candidates:
                if p.exists():
                    path = str(p)
                    break

        if path and Path(path).exists():
            with open(path) as f:
                data = json.load(f)

            for provider, info in data.get("providers", {}).items():
                if isinstance(info, dict):
                    models = info.get("available", [])
                    if isinstance(models, list):
                        self.available_models[provider] = models

            logger.info(
                f"Loaded {sum(len(m) for m in self.available_models.values())} models from discovery"
            )
        else:
            logger.warning("No discovery_results.json found - using default model list")

    def _get_provider(self, model_id: str) -> str:
        """Extract provider from model ID."""
        if ":" in model_id:
            return model_id.split(":")[0]
        return "unknown"

    def _is_model_available(self, model_id: str) -> bool:
        """Check if model is available."""
        provider = self._get_provider(model_id)

        # Fast config gating: if a provider clearly isn't configured, skip it.
        # This avoids spending many attempts on providers that cannot possibly work.
        if provider == "gh":
            # GitHub Models requires a token.
            if not (os.getenv("GITHUB_TOKEN") or "").strip():
                return False
        elif provider == "gemini":
            # Gemini requires remote enabled + API key.
            allow_remote = (
                os.getenv("PROMPTEVAL_ALLOW_REMOTE") or ""
            ).strip().lower() in {
                "1",
                "true",
                "yes",
                "y",
                "on",
            }
            if not allow_remote:
                return False
            if not (
                (
                    os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""
                ).strip()
            ):
                return False
        elif provider == "openai":
            if not ((os.getenv("OPENAI_API_KEY") or "").strip()):
                return False
        elif provider == "anthropic":
            if not (
                (
                    os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY") or ""
                ).strip()
            ):
                return False
        elif provider in {"azure-openai", "azure-foundry", "azure"}:
            # Azure providers require explicit configuration.
            if not (
                (
                    os.getenv("AZURE_OPENAI_API_KEY")
                    or os.getenv("AZURE_OPENAI_API_KEY_0")
                    or ""
                ).strip()
            ):
                return False

        # Check provider status
        status = self.provider_status.get(provider)
        if status and (not status.available or status.is_rate_limited()):
            return False

        # Check if model in discovery (provider keys vary across discovery implementations)
        for alias in [provider, f"{provider}_models", f"{provider}_onnx"]:
            if alias in self.available_models:
                if model_id in self.available_models[alias]:
                    return True

        # Fallback: assume available if not in discovery
        return True

    def get_models_for_tier(self, tier: int) -> List[str]:
        """Get available models for a tier, sorted by preference."""
        tier_config = MODEL_TIERS.get(tier, MODEL_TIERS[2])
        candidates = tier_config["models"]

        # Filter to available models
        available = [m for m in candidates if self._is_model_available(m)]

        # Sort by provider priority
        def sort_key(model_id: str) -> Tuple[int, float]:
            provider = self._get_provider(model_id)
            try:
                priority = PROVIDER_PRIORITY.index(provider)
            except ValueError:
                priority = 999

            # Also consider latency
            status = self.provider_status.get(provider)
            latency = status.avg_latency_ms if status else 0

            return (priority, latency)

        available.sort(key=sort_key)
        return available

    def get_model_for_tier(self, tier: int) -> Optional[str]:
        """Get the best available model for a tier."""
        models = self.get_models_for_tier(tier)
        return models[0] if models else None

    def get_fallback_chain(self, tier: int) -> List[str]:
        """Get ordered fallback chain for a tier."""
        models = self.get_models_for_tier(tier)

        # If no models at this tier, try adjacent tiers
        if not models:
            # Try one tier up
            if tier < 3:
                models = self.get_models_for_tier(tier + 1)
            # Try one tier down
            if not models and tier > 1:
                models = self.get_models_for_tier(tier - 1)

        return models

    async def call_with_fallback(
        self,
        tier: int,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        llm_client: Any = None,  # LLMClient instance
        max_retries: int = 3,
    ) -> Tuple[str, str]:  # Returns (result, model_used)
        """Call LLM with automatic fallback on rate limits or errors.

        Returns:
            Tuple of (response_text, model_id_used)
        """
        if llm_client is None:
            from tools.llm.llm_client import LLMClient

            llm_client = LLMClient

        fallback_chain = self.get_fallback_chain(tier)

        if not fallback_chain:
            raise RuntimeError(f"No models available for tier {tier}")

        last_error = None

        for model_id in fallback_chain:
            provider = self._get_provider(model_id)
            status = self.provider_status.get(provider, ProviderStatus(name=provider))

            # Skip rate-limited providers based on strategy
            if status.is_rate_limited():
                if self.rate_limit_strategy == "wait":
                    wait_seconds = (
                        status.rate_limit_until - datetime.now()
                    ).total_seconds()
                    if wait_seconds > 0 and wait_seconds < 120:  # Wait max 2 min
                        logger.info(
                            f"Waiting {wait_seconds:.0f}s for rate limit on {provider}"
                        )
                        await asyncio.sleep(wait_seconds)
                    else:
                        continue  # Skip if too long
                else:
                    continue  # Fallback strategy - try next

            # Attempt the call
            for attempt in range(max_retries):
                try:
                    start_time = time.time()

                    result = llm_client.generate_text(
                        model_id,
                        prompt,
                        system_instruction=system,
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )

                    # tools.llm.llm_client returns error strings instead of raising.
                    # Treat these as failures so we can fall back to the next model.
                    if isinstance(result, str):
                        low = result.strip().lower()
                        if (
                            low.startswith("error calling")
                            or low.startswith("error:")
                            or low.startswith("unknown model")
                            or low.startswith("gh models error")
                            or "remote provider disabled" in low
                            or "environment variable not set" in low
                        ):
                            raise RuntimeError(result.strip())

                    latency_ms = (time.time() - start_time) * 1000
                    status.mark_success(latency_ms)

                    return (result, model_id)

                except Exception as e:
                    error_str = str(e).lower()

                    def _is_permanent_error(err: str) -> bool:
                        # Errors that are unlikely to succeed on retry for the same model.
                        permanent_markers = (
                            "no access",
                            "no_access",
                            "unknown model",
                            "remote provider disabled",
                            "environment variable not set",
                            "not configured",
                            "gh cli not found",
                        )
                        if any(m in err for m in permanent_markers):
                            return True
                        # If the provider itself returns an error string (common for gh:),
                        # prefer switching models rather than hammering the same one.
                        if "gh models error" in err and not (
                            "rate limit" in err or "rate limited" in err or "429" in err
                        ):
                            return True
                        return False

                    # Check for rate limit
                    if (
                        "429" in error_str
                        or "rate limit" in error_str
                        or "rate limited" in error_str
                    ):
                        # Extract retry-after if present
                        retry_after = 60
                        if "retry-after" in error_str:
                            try:
                                retry_after = int(
                                    error_str.split("retry-after")[1].split()[0]
                                )
                            except:
                                pass

                        status.mark_rate_limited(retry_after)

                        if self.rate_limit_strategy == "wait" and retry_after < 120:
                            logger.info(
                                f"Rate limited on {model_id}, waiting {retry_after}s"
                            )
                            await asyncio.sleep(retry_after)
                            continue  # Retry same model
                        else:
                            break  # Try next model

                    # Other errors
                    status.mark_error(str(e))
                    last_error = e

                    if _is_permanent_error(error_str):
                        break  # Try next model immediately

                    if attempt < max_retries - 1:
                        await asyncio.sleep(1 * (attempt + 1))  # Backoff
                    else:
                        break  # Try next model

        # All models failed
        raise RuntimeError(
            f"All models failed for tier {tier}. Last error: {last_error}"
        )

    def get_status_report(self) -> Dict[str, Any]:
        """Get current status of all providers."""
        return {
            provider: {
                "available": status.available,
                "rate_limited": status.is_rate_limited(),
                "rate_limit_until": (
                    str(status.rate_limit_until) if status.rate_limit_until else None
                ),
                "requests": status.request_count,
                "errors": status.error_count,
                "avg_latency_ms": round(status.avg_latency_ms, 2),
            }
            for provider, status in self.provider_status.items()
        }


# Convenience function
def get_smart_router(**kwargs) -> SmartModelRouter:
    """Get a configured SmartModelRouter instance."""
    return SmartModelRouter(**kwargs)


if __name__ == "__main__":
    # Test the router
    router = SmartModelRouter()

    print("=== Smart Model Router ===\n")

    for tier in [1, 2, 3]:
        models = router.get_models_for_tier(tier)
        print(f"Tier {tier} ({MODEL_TIERS[tier]['name']}):")
        for m in models[:5]:
            print(f"  - {m}")
        print()

    print("Fallback chain for Tier 2:")
    for i, m in enumerate(router.get_fallback_chain(2)):
        print(f"  {i+1}. {m}")
