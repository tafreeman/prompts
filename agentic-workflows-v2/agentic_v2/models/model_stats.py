"""Model statistics tracking with advanced metrics.

Aggressive design improvements:
- Exponential Moving Average (EMA) for latency smoothing
- Percentile tracking (p50, p95, p99) via sorted reservoir
- Sliding window for recent performance
- Circuit breaker state machine
- Time-decayed success rates
"""

import bisect
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional


class CircuitState(str, Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class LatencyPercentiles:
    """Percentile statistics for latency."""

    p50: float = 0.0
    p75: float = 0.0
    p90: float = 0.0
    p95: float = 0.0
    p99: float = 0.0

    def to_dict(self) -> dict[str, float]:
        """Convert to dictionary."""
        return {
            "p50": self.p50,
            "p75": self.p75,
            "p90": self.p90,
            "p95": self.p95,
            "p99": self.p99,
        }


@dataclass
class ModelStats:
    """Comprehensive statistics for a single model.

    Design improvements over original plan:
    - EMA for latency (smoother than simple average)
    - Percentile tracking via reservoir sampling
    - Circuit breaker pattern for automatic failure handling
    - Time-decayed metrics (recent performance weighted higher)
    - Serialization support for persistence
    """

    model_id: str

    # Counters
    success_count: int = 0
    failure_count: int = 0
    rate_limit_count: int = 0
    timeout_count: int = 0

    # Latency tracking (EMA)
    _ema_latency_ms: float = 0.0
    _ema_alpha: float = 0.2  # Smoothing factor

    # Percentile tracking (sorted reservoir)
    _latency_samples: list[float] = field(default_factory=list)
    _max_samples: int = 1000

    # Sliding window for recent performance
    _recent_results: list[tuple[datetime, bool]] = field(default_factory=list)
    _window_size: int = 50

    # Circuit breaker
    circuit_state: CircuitState = CircuitState.CLOSED
    _failure_threshold: int = 5
    _recovery_timeout_seconds: int = 60
    _last_failure_time: Optional[datetime] = None
    _consecutive_failures: int = 0
    _half_open_success_required: int = 2
    _half_open_successes: int = 0

    # Timestamps
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Cooldown tracking
    cooldown_until: Optional[datetime] = None

    @property
    def total_calls(self) -> int:
        """Total number of API calls."""
        return self.success_count + self.failure_count

    @property
    def success_rate(self) -> float:
        """Overall success rate (0-1)."""
        if self.total_calls == 0:
            return 1.0  # Assume good until proven otherwise
        return self.success_count / self.total_calls

    @property
    def recent_success_rate(self) -> float:
        """Success rate over recent window (0-1)."""
        if not self._recent_results:
            return 1.0
        successes = sum(1 for _, success in self._recent_results if success)
        return successes / len(self._recent_results)

    @property
    def avg_latency_ms(self) -> float:
        """Exponential moving average latency."""
        return self._ema_latency_ms

    @property
    def percentiles(self) -> LatencyPercentiles:
        """Calculate latency percentiles from samples."""
        if not self._latency_samples:
            return LatencyPercentiles()

        sorted_samples = sorted(self._latency_samples)
        n = len(sorted_samples)

        def get_percentile(p: float) -> float:
            idx = int(p * n)
            return sorted_samples[min(idx, n - 1)]

        return LatencyPercentiles(
            p50=get_percentile(0.50),
            p75=get_percentile(0.75),
            p90=get_percentile(0.90),
            p95=get_percentile(0.95),
            p99=get_percentile(0.99),
        )

    @property
    def is_healthy(self) -> bool:
        """Check if model is considered healthy."""
        if self.circuit_state == CircuitState.OPEN:
            return False
        if self.is_in_cooldown:
            return False
        # Consider unhealthy if recent success rate < 50%
        if len(self._recent_results) >= 5 and self.recent_success_rate < 0.5:
            return False
        return True

    @property
    def is_in_cooldown(self) -> bool:
        """Check if model is in cooldown period."""
        if self.cooldown_until is None:
            return False
        return datetime.now(timezone.utc) < self.cooldown_until

    @property
    def cooldown_remaining_seconds(self) -> float:
        """Seconds remaining in cooldown, or 0 if not in cooldown."""
        if not self.is_in_cooldown:
            return 0.0
        delta = self.cooldown_until - datetime.now(timezone.utc)
        return max(0.0, delta.total_seconds())

    def record_success(self, latency_ms: float) -> None:
        """Record a successful call.

        Args:
            latency_ms: Call latency in milliseconds
        """
        self.success_count += 1
        self.last_success = datetime.now(timezone.utc)

        # Update EMA latency
        if self._ema_latency_ms == 0:
            self._ema_latency_ms = latency_ms
        else:
            self._ema_latency_ms = (
                self._ema_alpha * latency_ms
                + (1 - self._ema_alpha) * self._ema_latency_ms
            )

        # Update latency samples (reservoir)
        if len(self._latency_samples) < self._max_samples:
            bisect.insort(self._latency_samples, latency_ms)
        else:
            # Replace random sample to maintain reservoir
            import random

            idx = random.randint(0, len(self._latency_samples) - 1)
            self._latency_samples[idx] = latency_ms
            self._latency_samples.sort()

        # Update recent window
        self._recent_results.append((datetime.now(timezone.utc), True))
        if len(self._recent_results) > self._window_size:
            self._recent_results.pop(0)

        # Circuit breaker handling
        self._consecutive_failures = 0
        if self.circuit_state == CircuitState.HALF_OPEN:
            self._half_open_successes += 1
            if self._half_open_successes >= self._half_open_success_required:
                self.circuit_state = CircuitState.CLOSED
                self._half_open_successes = 0

    def record_failure(self, error_type: str = "unknown") -> None:
        """Record a failed call.

        Args:
            error_type: Type of error encountered
        """
        self.failure_count += 1
        self.last_failure = datetime.now(timezone.utc)
        self._last_failure_time = self.last_failure

        # Update recent window
        self._recent_results.append((datetime.now(timezone.utc), False))
        if len(self._recent_results) > self._window_size:
            self._recent_results.pop(0)

        # Circuit breaker handling
        self._consecutive_failures += 1
        if self.circuit_state == CircuitState.HALF_OPEN:
            # Failed during recovery test - reopen circuit
            self.circuit_state = CircuitState.OPEN
            self._half_open_successes = 0
        elif self._consecutive_failures >= self._failure_threshold:
            self.circuit_state = CircuitState.OPEN

    def record_rate_limit(self) -> None:
        """Record a rate limit hit."""
        self.rate_limit_count += 1
        self.record_failure("rate_limit")
        # Apply longer cooldown for rate limits
        self.cooldown_until = datetime.now(timezone.utc) + timedelta(minutes=2)

    def record_timeout(self) -> None:
        """Record a timeout."""
        self.timeout_count += 1
        self.record_failure("timeout")

    def set_cooldown(self, seconds: int) -> None:
        """Set cooldown period.

        Args:
            seconds: Duration of cooldown in seconds
        """
        self.cooldown_until = datetime.now(timezone.utc) + timedelta(seconds=seconds)

    def clear_cooldown(self) -> None:
        """Clear any active cooldown."""
        self.cooldown_until = None

    def check_circuit(self) -> bool:
        """Check if circuit allows requests.

        Returns:
            True if requests should be allowed
        """
        if self.circuit_state == CircuitState.CLOSED:
            return True

        if self.circuit_state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self._last_failure_time is not None:
                elapsed = datetime.now(timezone.utc) - self._last_failure_time
                if elapsed.total_seconds() >= self._recovery_timeout_seconds:
                    self.circuit_state = CircuitState.HALF_OPEN
                    return True
            return False

        # HALF_OPEN: allow limited requests
        return True

    def to_dict(self) -> dict:
        """Serialize to dictionary for persistence."""
        return {
            "model_id": self.model_id,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "rate_limit_count": self.rate_limit_count,
            "timeout_count": self.timeout_count,
            "ema_latency_ms": self._ema_latency_ms,
            "circuit_state": self.circuit_state.value,
            "last_success": (
                self.last_success.isoformat() if self.last_success else None
            ),
            "last_failure": (
                self.last_failure.isoformat() if self.last_failure else None
            ),
            "first_seen": self.first_seen.isoformat(),
            "cooldown_until": (
                self.cooldown_until.isoformat() if self.cooldown_until else None
            ),
            "success_rate": self.success_rate,
            "recent_success_rate": self.recent_success_rate,
            "percentiles": self.percentiles.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelStats":
        """Deserialize from dictionary."""
        stats = cls(model_id=data["model_id"])
        stats.success_count = data.get("success_count", 0)
        stats.failure_count = data.get("failure_count", 0)
        stats.rate_limit_count = data.get("rate_limit_count", 0)
        stats.timeout_count = data.get("timeout_count", 0)
        stats._ema_latency_ms = data.get("ema_latency_ms", 0.0)
        stats.circuit_state = CircuitState(data.get("circuit_state", "closed"))

        if data.get("last_success"):
            stats.last_success = datetime.fromisoformat(data["last_success"])
        if data.get("last_failure"):
            stats.last_failure = datetime.fromisoformat(data["last_failure"])
        if data.get("first_seen"):
            stats.first_seen = datetime.fromisoformat(data["first_seen"])
        if data.get("cooldown_until"):
            stats.cooldown_until = datetime.fromisoformat(data["cooldown_until"])

        return stats

    def __repr__(self) -> str:
        """Rich representation."""
        return (
            f"ModelStats({self.model_id}: "
            f"success_rate={self.success_rate:.1%}, "
            f"calls={self.total_calls}, "
            f"latency={self.avg_latency_ms:.0f}ms, "
            f"circuit={self.circuit_state.value})"
        )
