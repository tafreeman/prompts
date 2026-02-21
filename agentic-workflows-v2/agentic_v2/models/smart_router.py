"""Smart model router with adaptive learning.

Aggressive design improvements:
- Health-weighted model selection (prefer reliable models)
- Adaptive cooldowns (scale with failure severity)
- Predictive availability (anticipate rate limits)
- Stats persistence with atomic writes
- Cost-aware routing (factor in token costs)
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from .model_stats import CircuitState, ModelStats
from .router import ModelRouter, ModelTier


@dataclass
class CooldownConfig:
    """Configuration for adaptive cooldowns."""

    # Base cooldown durations
    base_failure_cooldown_seconds: int = 30
    base_rate_limit_cooldown_seconds: int = 120
    base_timeout_cooldown_seconds: int = 60

    # Scaling factors
    consecutive_failure_multiplier: float = 1.5
    max_cooldown_seconds: int = 600  # 10 minutes

    # Recovery
    success_count_to_clear: int = 3


@dataclass
class SmartModelRouter(ModelRouter):
    """Intelligent router with learning and adaptive behavior.

    Aggressive improvements:
    - Records and persists model performance stats
    - Uses health scores for weighted selection
    - Applies adaptive cooldowns that scale with failures
    - Supports cost-aware routing
    - Provides predictive availability hints
    """

    # Stats for each model
    model_stats: dict[str, ModelStats] = field(default_factory=dict)

    # Configuration
    cooldown_config: CooldownConfig = field(default_factory=CooldownConfig)

    # Persistence
    stats_file: Optional[Path] = None
    _auto_save: bool = True

    # Cost weights (tokens per $0.001)
    model_costs: dict[str, float] = field(
        default_factory=lambda: {
            "ollama:phi4": 0.0,
            "ollama:llama3.2:latest": 0.0,
            "gh:gpt-4o-mini": 0.15,
            "gh:gpt-4o": 2.5,
        }
    )

    def __post_init__(self):
        if self.stats_file:
            self._load_stats()

    def _get_stats(self, model: str) -> ModelStats:
        """Get or create stats for a model."""
        if model not in self.model_stats:
            self.model_stats[model] = ModelStats(model_id=model)
        return self.model_stats[model]

    def record_success(self, model: str, latency_ms: float) -> None:
        """Record a successful call.

        Args:
            model: Model identifier
            latency_ms: Call latency in milliseconds
        """
        stats = self._get_stats(model)
        stats.record_success(latency_ms)
        self.mark_available(model)

        if self._auto_save and self.stats_file:
            self._save_stats()

    def record_failure(
        self, model: str, error_type: str = "unknown", is_permanent: bool = False
    ) -> None:
        """Record a failed call.

        Args:
            model: Model identifier
            error_type: Type of error
            is_permanent: Whether error is permanent (no retry)
        """
        stats = self._get_stats(model)
        stats.record_failure(error_type)

        # Apply adaptive cooldown
        cooldown = self._calculate_cooldown(stats, error_type)
        stats.set_cooldown(cooldown)

        # Mark permanently unavailable if permanent error
        if is_permanent:
            self.mark_unavailable(model)

        if self._auto_save and self.stats_file:
            self._save_stats()

    def record_rate_limit(self, model: str) -> None:
        """Record a rate limit hit.

        Args:
            model: Model identifier
        """
        stats = self._get_stats(model)
        stats.record_rate_limit()

        if self._auto_save and self.stats_file:
            self._save_stats()

    def record_timeout(self, model: str) -> None:
        """Record a timeout.

        Args:
            model: Model identifier
        """
        stats = self._get_stats(model)
        stats.record_timeout()

        cooldown = self._calculate_cooldown(stats, "timeout")
        stats.set_cooldown(cooldown)

        if self._auto_save and self.stats_file:
            self._save_stats()

    def _calculate_cooldown(self, stats: ModelStats, error_type: str) -> int:
        """Calculate adaptive cooldown duration."""
        cfg = self.cooldown_config

        # Base duration by error type
        if error_type == "rate_limit":
            base = cfg.base_rate_limit_cooldown_seconds
        elif error_type == "timeout":
            base = cfg.base_timeout_cooldown_seconds
        else:
            base = cfg.base_failure_cooldown_seconds

        # Scale by consecutive failures
        failures = stats._consecutive_failures
        multiplier = cfg.consecutive_failure_multiplier ** min(failures, 5)

        cooldown = int(base * multiplier)
        return min(cooldown, cfg.max_cooldown_seconds)

    def get_model_for_tier(
        self,
        tier: ModelTier,
        prefer_healthy: bool = True,
        max_cost: Optional[float] = None,
    ) -> Optional[str]:
        """Get best available model for a tier.

        Args:
            tier: Model tier
            prefer_healthy: Weight selection by health scores
            max_cost: Maximum cost per 1K tokens (None = no limit)

        Returns:
            Best model or None
        """
        chain = self.get_chain(tier)
        candidates = []

        for model in chain:
            # Check availability
            if not self.is_model_available(model):
                continue

            stats = self._get_stats(model)

            # Check circuit breaker
            if not stats.check_circuit():
                continue

            # Check cooldown
            if stats.is_in_cooldown:
                continue

            # Check cost
            if max_cost is not None:
                cost = self.model_costs.get(model, 0.0)
                if cost > max_cost:
                    continue

            candidates.append((model, stats))

        if not candidates:
            return None

        if not prefer_healthy or len(candidates) == 1:
            return candidates[0][0]

        # Score candidates by health
        def score(model_stats: tuple[str, ModelStats]) -> float:
            _, stats = model_stats
            # Weight: success_rate (60%) + low latency (20%) + recency (20%)
            success_score = stats.recent_success_rate * 0.6

            # Latency score (lower is better, normalize to 0-1)
            latency = stats.avg_latency_ms
            latency_score = max(0, 1 - (latency / 10000)) * 0.2 if latency > 0 else 0.2

            # Recency score (recent successes preferred)
            recency_score = 0.2
            if stats.last_success:
                age = (datetime.now(timezone.utc) - stats.last_success).total_seconds()
                recency_score = max(0, 1 - (age / 3600)) * 0.2  # Decay over 1 hour

            return success_score + latency_score + recency_score

        candidates.sort(key=score, reverse=True)
        return candidates[0][0]

    def get_fallback_chain_with_health(
        self, tier: ModelTier
    ) -> list[tuple[str, float]]:
        """Get fallback chain with health scores.

        Args:
            tier: Model tier

        Returns:
            List of (model, health_score) tuples, sorted by health
        """
        chain = self.get_chain(tier)
        scored = []

        for model in chain:
            stats = self._get_stats(model)
            if stats.check_circuit() and not stats.is_in_cooldown:
                scored.append((model, stats.recent_success_rate))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    def predict_availability(self, model: str) -> dict[str, Any]:
        """Predict model availability.

        Args:
            model: Model identifier

        Returns:
            Prediction dict with confidence and reason
        """
        stats = self._get_stats(model)

        # Check obvious blockers
        if not self.is_model_available(model):
            return {
                "available": False,
                "confidence": 1.0,
                "reason": "marked_unavailable",
            }

        if stats.circuit_state == CircuitState.OPEN:
            return {
                "available": False,
                "confidence": 0.9,
                "reason": "circuit_open",
                "recovery_in_seconds": stats._recovery_timeout_seconds,
            }

        if stats.is_in_cooldown:
            return {
                "available": False,
                "confidence": 0.95,
                "reason": "in_cooldown",
                "cooldown_remaining": stats.cooldown_remaining_seconds,
            }

        # Predict based on recent performance
        if stats.recent_success_rate < 0.3:
            return {
                "available": True,
                "confidence": 0.4,
                "reason": "poor_recent_performance",
                "success_rate": stats.recent_success_rate,
            }

        if stats.rate_limit_count > 5:
            # High rate limit history suggests future limits
            return {
                "available": True,
                "confidence": 0.6,
                "reason": "rate_limit_history",
                "rate_limit_count": stats.rate_limit_count,
            }

        return {
            "available": True,
            "confidence": min(0.9, stats.recent_success_rate + 0.1),
            "reason": "healthy",
            "success_rate": stats.recent_success_rate,
        }

    def get_stats_summary(self) -> dict[str, Any]:
        """Get summary of all model stats."""
        return {
            "total_models": len(self.model_stats),
            "healthy_models": sum(1 for s in self.model_stats.values() if s.is_healthy),
            "models": {
                model: stats.to_dict() for model, stats in self.model_stats.items()
            },
        }

    def _save_stats(self) -> None:
        """Save stats to file atomically."""
        if not self.stats_file:
            return

        data = {
            "version": "1.0",
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "stats": {
                model: stats.to_dict() for model, stats in self.model_stats.items()
            },
        }

        # Atomic write: write to temp file, then rename
        temp_file = self.stats_file.with_suffix(".tmp")
        temp_file.write_text(json.dumps(data, indent=2))
        temp_file.replace(self.stats_file)

    def _load_stats(self) -> None:
        """Load stats from file."""
        if not self.stats_file or not self.stats_file.exists():
            return

        try:
            data = json.loads(self.stats_file.read_text())
            for model, stats_dict in data.get("stats", {}).items():
                self.model_stats[model] = ModelStats.from_dict(stats_dict)
        except (json.JSONDecodeError, KeyError):
            # Log error but continue with empty stats
            pass

    async def call_with_fallback(
        self,
        caller: Callable[[str, str], Any],
        prompt: str,
        tier: ModelTier,
        max_retries: int = 3,
    ) -> tuple[str, Any]:
        """Call a model with automatic fallback.

        Args:
            caller: Async function(model, prompt) -> response
            prompt: Prompt to send
            tier: Model tier
            max_retries: Max models to try

        Returns:
            Tuple of (model_used, response)

        Raises:
            RuntimeError: If all models fail
        """
        tried = []
        last_error = None

        for _ in range(max_retries):
            model = self.get_model_for_tier(tier)
            if model is None or model in tried:
                break

            tried.append(model)
            start = datetime.now(timezone.utc)

            try:
                response = await caller(model, prompt)
                latency = (datetime.now(timezone.utc) - start).total_seconds() * 1000
                self.record_success(model, latency)
                return model, response

            except Exception as e:
                error_str = str(e).lower()

                # Classify error
                if "rate limit" in error_str or "429" in error_str:
                    self.record_rate_limit(model)
                elif "timeout" in error_str:
                    self.record_timeout(model)
                elif "not found" in error_str or "no access" in error_str:
                    self.record_failure(model, "permanent", is_permanent=True)
                else:
                    self.record_failure(model, type(e).__name__)

                last_error = e

        raise RuntimeError(
            f"All models failed. Tried: {tried}. Last error: {last_error}"
        )

    def __repr__(self) -> str:
        healthy = sum(1 for s in self.model_stats.values() if s.is_healthy)
        return (
            f"SmartModelRouter(models={len(self.model_stats)}, "
            f"healthy={healthy}, "
            f"stats_file={self.stats_file})"
        )


# Global smart router instance
_smart_router: Optional[SmartModelRouter] = None


def get_smart_router(stats_file: Optional[Path] = None) -> SmartModelRouter:
    """Get the global smart router."""
    global _smart_router
    if _smart_router is None:
        _smart_router = SmartModelRouter(stats_file=stats_file)
    return _smart_router


def reset_smart_router() -> None:
    """Reset the global smart router (for testing)."""
    global _smart_router
    _smart_router = None
