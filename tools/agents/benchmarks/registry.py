"""
Benchmark Registry and Configuration
=====================================

Manages benchmark configurations and user preferences.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .datasets import BENCHMARK_DEFINITIONS, BenchmarkDefinition, BenchmarkType


@dataclass
class BenchmarkConfig:
    """User configuration for running benchmarks.

    Can be saved/loaded from JSON for persistence.
    """

    # Selected benchmark
    benchmark_id: str = "custom-local"

    # Task filtering
    limit: Optional[int] = None  # Max tasks to load
    offset: int = 0  # Starting offset
    task_ids: List[str] = field(default_factory=list)  # Specific task IDs
    difficulty: Optional[str] = None  # Filter by difficulty
    tags: List[str] = field(default_factory=list)  # Filter by tags

    # Model configuration
    model: str = "gh:gpt-4o-mini"  # Default model
    fallback_models: List[str] = field(default_factory=list)  # Fallback chain

    # Agent workflow
    workflow: str = "multi-agent"  # Workflow type
    agents: List[str] = field(
        default_factory=lambda: ["analyst", "researcher", "strategist", "implementer"]
    )

    # Execution options
    parallel: bool = False  # Run tasks in parallel
    max_workers: int = 2  # Parallel workers
    timeout_seconds: int = 300  # Per-task timeout
    retry_count: int = 1  # Retries on failure

    # Output options
    output_dir: Optional[str] = None  # Where to save results
    verbose: bool = False  # Verbose logging
    save_intermediate: bool = False  # Save intermediate agent outputs

    # Cache options
    use_cache: bool = True  # Use cached benchmark data
    cache_ttl_hours: int = 24  # Cache expiry

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BenchmarkConfig":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def save(self, path: Path) -> None:
        """Save configuration to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "BenchmarkConfig":
        """Load configuration from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))


class BenchmarkRegistry:
    """Central registry for benchmark management.

    Provides methods to discover, configure, and load benchmarks.
    """

    _config_dir = Path(__file__).parent / ".config"
    _default_config_path = _config_dir / "default_config.json"

    @classmethod
    def list_benchmarks(
        cls,
        benchmark_type: Optional[BenchmarkType] = None,
        language: Optional[str] = None,
        verbose: bool = False,
    ) -> Dict[str, Dict[str, Any]]:
        """List all available benchmarks.

        Returns simplified dict for display (not full
        BenchmarkDefinition).
        """
        from .datasets import list_benchmarks

        benchmarks = list_benchmarks(benchmark_type, language)
        result = {}

        for bid, bdef in benchmarks.items():
            info = {
                "name": bdef.name,
                "description": bdef.description,
                "type": bdef.benchmark_type.value,
                "size": bdef.size,
                "source": bdef.source.value,
                "languages": bdef.languages,
            }
            if verbose:
                info.update(
                    {
                        "metrics": bdef.metrics,
                        "evaluation_method": bdef.evaluation_method,
                        "paper_url": bdef.paper_url,
                        "leaderboard_url": bdef.leaderboard_url,
                    }
                )
            result[bid] = info

        return result

    @classmethod
    def get_benchmark_info(cls, benchmark_id: str) -> Optional[BenchmarkDefinition]:
        """Get detailed info about a specific benchmark."""
        return BENCHMARK_DEFINITIONS.get(benchmark_id)

    @classmethod
    def get_config(cls) -> BenchmarkConfig:
        """Get current configuration (loads default if exists)."""
        if cls._default_config_path.exists():
            return BenchmarkConfig.load(cls._default_config_path)
        return BenchmarkConfig()

    @classmethod
    def save_config(cls, config: BenchmarkConfig) -> None:
        """Save configuration as default."""
        cls._config_dir.mkdir(parents=True, exist_ok=True)
        config.save(cls._default_config_path)

    @classmethod
    def create_config(
        cls,
        benchmark_id: str,
        model: str = "gh:gpt-4o-mini",
        limit: Optional[int] = None,
        **kwargs,
    ) -> BenchmarkConfig:
        """Create a new configuration."""
        return BenchmarkConfig(
            benchmark_id=benchmark_id, model=model, limit=limit, **kwargs
        )

    @classmethod
    def validate_config(cls, config: BenchmarkConfig) -> List[str]:
        """Validate a configuration.

        Returns list of error messages (empty if valid).
        """
        errors = []

        # Check benchmark exists
        if config.benchmark_id not in BENCHMARK_DEFINITIONS:
            errors.append(f"Unknown benchmark: {config.benchmark_id}")

        # Check model format
        valid_prefixes = ["gh:", "local:", "ollama:", "aitk:", "openai:", "anthropic:"]
        if not any(config.model.startswith(p) for p in valid_prefixes):
            errors.append(f"Model should start with one of: {valid_prefixes}")

        # Check workflow
        valid_workflows = ["multi-agent", "single-agent", "chain-of-thought", "react"]
        if config.workflow not in valid_workflows:
            errors.append(
                f"Unknown workflow: {config.workflow}. Valid: {valid_workflows}"
            )

        return errors


# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================

PRESET_CONFIGS: Dict[str, BenchmarkConfig] = {
    "quick-test": BenchmarkConfig(
        benchmark_id="humaneval",
        model="gh:gpt-4o-mini",
        limit=5,
        workflow="multi-agent",
        verbose=True,
    ),
    "swe-bench-eval": BenchmarkConfig(
        benchmark_id="swe-bench-lite",
        model="gh:gpt-4o",
        limit=50,
        workflow="multi-agent",
        timeout_seconds=600,
        save_intermediate=True,
    ),
    "local-dev": BenchmarkConfig(
        benchmark_id="custom-local",
        model="local:phi4",
        workflow="multi-agent",
        verbose=True,
    ),
    "full-eval": BenchmarkConfig(
        benchmark_id="swe-bench-verified",
        model="gh:gpt-4o",
        parallel=True,
        max_workers=4,
        timeout_seconds=900,
        save_intermediate=True,
    ),
}


def get_preset(name: str) -> Optional[BenchmarkConfig]:
    """Get a preset configuration by name."""
    return PRESET_CONFIGS.get(name)


def list_presets() -> Dict[str, str]:
    """List available preset configurations."""
    return {
        name: f"{cfg.benchmark_id} with {cfg.model}"
        for name, cfg in PRESET_CONFIGS.items()
    }
