#!/usr/bin/env python3
"""Model Probe & Cache -- slim facade.

Provides runtime probing of model availability with persistent caching.
This prevents wasted evaluation runs on models that are known to be unavailable.

Implementation is split across:
    - ``probe_config``     : Constants, ProbeResult, cache helpers, retry decorator
    - ``probe_providers``  : Per-provider probe functions
    - ``probe_discovery``  : Multi-provider discovery

Usage:
    from tools.llm.model_probe import ModelProbe

    probe = ModelProbe()

    # Check if a model is usable
    status = probe.check_model("gh:gpt-4o-mini")
    if status.usable:
        # Safe to evaluate
        ...

    # Filter a list of models to only runnable ones
    runnable = probe.filter_runnable(["gh:gpt-4o-mini", "gh:o1", "local:phi4"])

    # Get cached probe results
    probe.get_cache_summary()
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Add parent directory to path for imports when run as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[2]))


# ---------------------------------------------------------------------------
# Load .env so provider API keys are available via os.getenv().
# We search upward from this file to find the nearest .env, which covers both
# the repo root (d:\source\prompts\.env) and any nested package roots.
# ---------------------------------------------------------------------------
def _load_dotenv() -> None:
    """Load the nearest .env file into os.environ (idempotent)."""
    try:
        from dotenv import load_dotenv  # type: ignore[import-untyped]
    except ImportError:
        # python-dotenv not installed — fall back to manual parse
        _load_dotenv_manual()
        return

    # Walk up from this file's directory to find .env
    search = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = search / ".env"
        if candidate.is_file():
            load_dotenv(candidate, override=False)
            return
        if search.parent == search:
            break
        search = search.parent


def _load_dotenv_manual() -> None:
    """Minimal .env loader when python-dotenv is not installed."""
    search = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = search / ".env"
        if candidate.is_file():
            for line in candidate.read_text(
                encoding="utf-8", errors="replace"
            ).splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip()
                if not key or key.startswith(" "):
                    continue
                # Only set if not already present (don't override real env)
                if key not in os.environ:
                    # Strip surrounding quotes (python-dotenv does this automatically)
                    if (
                        len(value) >= 2
                        and value[0] == value[-1]
                        and value[0] in ('"', "'")
                    ):
                        value = value[1:-1]
                    os.environ[key] = value
            return
        if search.parent == search:
            break
        search = search.parent


_load_dotenv()


# =============================================================================
# ERROR CLASSIFICATION - Import from canonical source
# =============================================================================

from tools.core.errors import ErrorCode, classify_error

# =============================================================================
# CONSTANTS - Path, Provider, Environment, URL, and Timeout Configuration
# =============================================================================

# Cache paths and configuration
_CACHE_BASE_DIR = ".cache"
_CACHE_APP_DIR = "prompts-eval"
_CACHE_PROBES_DIR = "model-probes"
_CACHE_FILE_NAME = "probe_cache.json"
_CACHE_VERSION = "1.0.0"

# AI Gallery and AI Toolkit paths
_AI_GALLERY_CACHE_DIR = "aigallery"
_AITK_HOME_DIR = ".aitk"
_AITK_MODELS_DIR = "models"
_AITK_MODELINFO_FILE = "foundry.modelinfo.json"
_AITK_MODELS_TASK_TYPE = "chat-completion"

# Model provider prefixes
_PREFIX_LOCAL = "local:"
_PREFIX_GITHUB = "gh:"
_PREFIX_GITHUB_ALT = "github:"
_PREFIX_OLLAMA = "ollama:"
_PREFIX_OPENAI = "openai:"
_PREFIX_GPT = "gpt"
_PREFIX_AZURE_FOUNDRY = "azure-foundry:"
_PREFIX_AZURE_OPENAI = "azure-openai:"
_PREFIX_WINDOWS_AI = "windows-ai:"
_PREFIX_AITK = "aitk:"
_PREFIX_AITK_ALT = "ai-toolkit:"
_PREFIX_GEMINI = "gemini:"
_PREFIX_CLAUDE = "claude:"
_PREFIX_LMSTUDIO = "lmstudio:"
_PREFIX_LMSTUDIO_ALT = "lm-studio:"
_PREFIX_LOCAL_API = "local-api:"

# Environment variable names
_ENV_GITHUB_TOKEN = "GITHUB_TOKEN"
_ENV_GH_TOKEN = "GH_TOKEN"
_ENV_OLLAMA_HOST = "OLLAMA_HOST"
_ENV_OLLAMA_API_KEY = "OLLAMA_API_KEY"
_ENV_OPENAI_API_KEY = "OPENAI_API_KEY"
_ENV_OPENAI_BASE_URL = "OPENAI_BASE_URL"
_ENV_OPENAI_API_BASE = "OPENAI_API_BASE"
_ENV_AZURE_FOUNDRY_API_KEY = "AZURE_FOUNDRY_API_KEY"
_ENV_AZURE_FOUNDRY_ENDPOINT_PREFIX = "AZURE_FOUNDRY_ENDPOINT"
_ENV_AZURE_OPENAI_ENDPOINT = "AZURE_OPENAI_ENDPOINT"
_ENV_AZURE_OPENAI_API_KEY = "AZURE_OPENAI_API_KEY"
_ENV_AZURE_OPENAI_DEPLOYMENT = "AZURE_OPENAI_DEPLOYMENT"
_ENV_GEMINI_API_KEY = "GEMINI_API_KEY"
_ENV_GOOGLE_API_KEY = "GOOGLE_API_KEY"
_ENV_ANTHROPIC_API_KEY = "ANTHROPIC_API_KEY"
_ENV_LMSTUDIO_HOST = "LMSTUDIO_HOST"
_ENV_LOCAL_AI_API_BASE_URL = "LOCAL_AI_API_BASE_URL"
_ENV_LOCAL_OPENAI_BASE_URL = "LOCAL_OPENAI_BASE_URL"

# URLs and API endpoints
_OLLAMA_DEFAULT_HOST = "http://localhost:11434"
_OLLAMA_API_TAGS_ENDPOINT = "/api/tags"
_LMSTUDIO_DEFAULT_HOST = "http://127.0.0.1:12340"
_LOCAL_SERVER_COMMON_PORTS = [12340, 1234, 5000, 5001, 8080, 8081]

# Windows AI bridge
_WINDOWS_AI_BRIDGE_DIR = "windows_ai_bridge"
_WINDOWS_AI_BRIDGE_PROJECT = "PhiSilicaBridge.csproj"

# AI Toolkit model directories
_AITK_MS_SUBDIR = "Microsoft"

# Timeout values (seconds)
_TIMEOUT_GH_AUTH = 10
_TIMEOUT_GH_MODELS_LIST = 30
_TIMEOUT_GH_MODELS_RUN = 30
_TIMEOUT_WINDOWS_AI_BRIDGE = 60
_TIMEOUT_OLLAMA_HTTP = 3
_TIMEOUT_CLOUD_HTTP = 10  # Remote cloud APIs (Gemini, Anthropic) — higher latency

# Cache key and string truncation lengths
_CACHE_KEY_MD5_LENGTH = 12
_GH_CLI_OUTPUT_MODELS_LIMIT = 5
_ENDPOINT_TRUNCATION_LENGTH = 50
_ERROR_BRIEF_LENGTH = 200
_ERROR_STANDARD_LENGTH = 500
_ERROR_DISPLAY_LENGTH = 60

# GitHub CLI and model probing
_GH_CLI_PROBE_TEST_MESSAGE = "Hi"
_GH_CLI_PROBE_MAX_TOKENS = "1"
_GH_CLI_ARG_MAX_TOKENS = "--max-tokens"

# Windows AI and dotnet
_DOTNET_CLI_ARG_PROJECT = "--project"
_WINDOWS_AI_CLI_ARG_INFO = "--info"

# Path separators and delimiters
_PATH_SEPARATOR = "/"
_TAB_SEPARATOR = "\t"
_OLLAMA_MODEL_TAG_SUFFIX = ":latest"

# AI Toolkit model name cleanup suffixes
_AITK_SUFFIX_GENERIC_CPU = "-generic-cpu"
_AITK_SUFFIX_GENERIC_GPU = "-generic-gpu"
_AITK_SUFFIX_CPU = "-cpu"
_AITK_SUFFIX_GPU = "-gpu"
_AITK_TRAILING_CHARS = "0123456789-"

# Azure deployment slot range
_AZURE_SLOT_RANGE = 10

# Exponential backoff configuration
_BACKOFF_BASE = 2
_JITTER_LOWER = 0.8
_JITTER_RANGE = 0.4

# Windows AI specific constants
_WINDOWS_AI_MODEL_ID = "windows-ai:phi-silica"

# Platform check
_PLATFORM_WINDOWS = "win32"

# =============================================================================
# PROBE RESULT
# =============================================================================


@dataclass
class ProbeResult:
    """Result of probing a model's availability."""

    model: str
    provider: str
    usable: bool
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    should_retry: bool = False
    probe_time: str = ""
    duration_ms: int = 0
    cached: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# =============================================================================
# CACHE MANAGEMENT
# =============================================================================


def get_cache_dir() -> Path:
    """Get the directory for probe cache files."""
    cache_dir = Path.home() / _CACHE_BASE_DIR / _CACHE_APP_DIR / _CACHE_PROBES_DIR
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_file() -> Path:
    """Get the main probe cache file."""
    return get_cache_dir() / _CACHE_FILE_NAME


def load_cache() -> dict[str, Any]:
    """Load the probe cache from disk."""
    cache_file = get_cache_file()
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": _CACHE_VERSION, "probes": {}, "last_updated": None}


def save_cache(cache: dict[str, Any]) -> None:
    """Save the probe cache to disk."""
    cache["last_updated"] = datetime.now().isoformat()
    cache_file = get_cache_file()
    cache_file.write_text(json.dumps(cache, indent=2), encoding="utf-8")


# Re-export everything callers used to import from this module
from tools.llm.probe_config import (
    CACHE_VERSION,
    ProbeResult,
    cache_key,
    get_cache_file,
    load_cache,
    save_cache,
    with_retry,
)
from tools.llm.probe_discovery import discover_all_models
from tools.llm.probe_providers import get_provider, probe_model

# Backward-compat: re-export public names so ``from tools.llm.model_probe import X`` still works
__all__ = [
    "ModelProbe",
    "ProbeResult",
    "discover_all_models",
    "filter_usable_models",
    "get_model_error",
    "get_probe",
    "is_model_usable",
    "main",
    "with_retry",
]


# =============================================================================
# MODEL PROBE CLASS
# =============================================================================


class ModelProbe:
    """Probes model availability and caches results.

    Cache TTL:
    - Permanent errors (403, unavailable): 24 hours
    - Transient errors (rate limit, timeout): 5 minutes
    - Success: 1 hour
    """

    # Cache TTLs
    TTL_SUCCESS = timedelta(hours=1)
    TTL_PERMANENT_ERROR = timedelta(hours=24)
    TTL_TRANSIENT_ERROR = timedelta(minutes=5)

    def __init__(self, use_cache: bool = True, verbose: bool = False):
        self.use_cache = use_cache
        self.verbose = verbose
        self._cache = (
            load_cache() if use_cache else {"version": CACHE_VERSION, "probes": {}}
        )
        self._session_probes: dict[str, ProbeResult] = {}

    def _log(self, msg: str) -> None:
        if self.verbose:
            logger.debug(msg)

    def _get_provider(self, model: str) -> str:
        """Extract provider from model string."""
        return get_provider(model)

    def _cache_key(self, model: str) -> str:
        """Generate cache key for a model."""
        return cache_key(model)

    def _is_cache_valid(self, cached: dict[str, Any]) -> bool:
        """Check if a cached probe result is still valid."""
        if not cached.get("probe_time"):
            return False

        try:
            probe_time = datetime.fromisoformat(cached["probe_time"])
        except Exception:
            return False

        now = datetime.now()
        error_code = cached.get("error_code")

        if error_code is None or error_code == ErrorCode.SUCCESS.value:
            ttl = self.TTL_SUCCESS
        elif error_code in [
            ErrorCode.PERMISSION_DENIED.value,
            ErrorCode.UNAVAILABLE_MODEL.value,
        ]:
            ttl = self.TTL_PERMANENT_ERROR
        else:
            ttl = self.TTL_TRANSIENT_ERROR

        return (now - probe_time) < ttl

    def _probe_model(self, model: str) -> ProbeResult:
        """Probe a model based on its provider."""
        return probe_model(model, log=self._log)

    def check_model(self, model: str, force_probe: bool = False) -> ProbeResult:
        """Check if a model is usable.

        Args:
            model: Model identifier (e.g., "gh:gpt-4o-mini", "local:phi4")
            force_probe: Skip cache and probe fresh

        Returns:
            ProbeResult with usability status
        """
        ck = self._cache_key(model)

        # Check session cache first (fastest)
        if not force_probe and ck in self._session_probes:
            result = self._session_probes[ck]
            result.cached = True
            return result

        # Check persistent cache
        if not force_probe and self.use_cache:
            cached = self._cache.get("probes", {}).get(ck)
            if cached and self._is_cache_valid(cached):
                result = ProbeResult(**cached)
                result.cached = True
                self._session_probes[ck] = result
                self._log(f"Cache hit: {model} -> usable={result.usable}")
                return result

        # Probe the model
        self._log(f"Probing: {model}")
        result = self._probe_model(model)

        # Cache the result
        self._session_probes[ck] = result
        if self.use_cache:
            self._cache.setdefault("probes", {})[ck] = result.to_dict()
            save_cache(self._cache)

        self._log(
            f"Probe complete: {model} -> usable={result.usable}, error={result.error_code}"
        )
        return result

    def filter_runnable(
        self, models: list[str], force_probe: bool = False
    ) -> list[str]:
        """Filter a list of models to only those that are runnable.

        Args:
            models: List of model identifiers
            force_probe: Skip cache and probe fresh

        Returns:
            List of runnable model identifiers
        """
        runnable = []
        for model in models:
            result = self.check_model(model, force_probe=force_probe)
            if result.usable:
                runnable.append(model)
        return runnable

    def get_probe_report(self, models: list[str]) -> dict[str, Any]:
        """Get a detailed probe report for a list of models.

        Returns:
            Dict with probe results and summary
        """
        results = {}
        usable = []
        unusable = []

        for model in models:
            result = self.check_model(model)
            results[model] = result.to_dict()
            if result.usable:
                usable.append(model)
            else:
                unusable.append((model, result.error_code, result.error_message))

        return {
            "timestamp": datetime.now().isoformat(),
            "total": len(models),
            "usable_count": len(usable),
            "unusable_count": len(unusable),
            "usable": usable,
            "unusable": [
                {"model": m, "error_code": c, "error": e} for m, c, e in unusable
            ],
            "details": results,
        }

    def clear_cache(self, model: str = None) -> None:
        """Clear probe cache.

        Args:
            model: If provided, clear only this model. Otherwise clear all.
        """
        if model:
            ck = self._cache_key(model)
            self._session_probes.pop(ck, None)
            self._cache.get("probes", {}).pop(ck, None)
        else:
            self._session_probes.clear()
            self._cache["probes"] = {}

        if self.use_cache:
            save_cache(self._cache)

    def get_cache_summary(self) -> dict[str, Any]:
        """Get a summary of the current cache state."""
        probes = self._cache.get("probes", {})

        valid = 0
        expired = 0
        usable = 0
        unusable = 0

        for cached in probes.values():
            if self._is_cache_valid(cached):
                valid += 1
                if cached.get("usable"):
                    usable += 1
                else:
                    unusable += 1
            else:
                expired += 1

        return {
            "cache_file": str(get_cache_file()),
            "total_entries": len(probes),
            "valid_entries": valid,
            "expired_entries": expired,
            "usable_models": usable,
            "unusable_models": unusable,
            "last_updated": self._cache.get("last_updated"),
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def is_model_usable(model: str) -> bool:
    """Quick check if a model is usable."""
    return get_probe().check_model(model).usable


def filter_usable_models(models: list[str]) -> list[str]:
    """Filter a list to only usable models."""
    return get_probe().filter_runnable(models)


def get_model_error(model: str) -> str | None:
    """Get the error message for an unusable model."""
    result = get_probe().check_model(model)
    return result.error_message if not result.usable else None


# =============================================================================
# CANONICAL SINGLETON ACCESS
# =============================================================================

_DEFAULT_PROBE: ModelProbe | None = None


def get_probe(*, verbose: bool = False, use_cache: bool = True) -> ModelProbe:
    """Return a process-wide ModelProbe instance.

    Many scripts (and tool_init) want a quick probe without managing lifetime.
    We provide a singleton so callers share cache and avoid repeated disk I/O.

    Args:
        verbose: Enable probe logging.
        use_cache: Enable persistent cache.
    """
    global _DEFAULT_PROBE
    if _DEFAULT_PROBE is None:
        _DEFAULT_PROBE = ModelProbe(use_cache=use_cache, verbose=verbose)
    return _DEFAULT_PROBE


# =============================================================================
# CLI
# =============================================================================


def main(argv: list[str]) -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Probe model availability")
    parser.add_argument("models", nargs="*", help="Models to probe")
    parser.add_argument(
        "--all-github", action="store_true", help="Probe common GitHub models"
    )
    parser.add_argument(
        "--all-local", action="store_true", help="Probe all local ONNX models"
    )
    parser.add_argument(
        "--all-azure", action="store_true", help="Check Azure Foundry/OpenAI"
    )
    parser.add_argument("--all-ollama", action="store_true", help="Probe Ollama models")
    parser.add_argument(
        "--all-aitk", action="store_true", help="Probe AI Toolkit local models (free)"
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover all available models from all providers",
    )
    parser.add_argument(
        "--force", action="store_true", help="Force fresh probe (ignore cache)"
    )
    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear the probe cache"
    )
    parser.add_argument(
        "--cache-info", action="store_true", help="Show cache information"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", help="Output file (JSON)")

    args = parser.parse_args(argv)

    probe = ModelProbe(verbose=args.verbose)

    if args.clear_cache:
        probe.clear_cache()
        print("Cache cleared.")
        return 0

    if args.cache_info:
        info = probe.get_cache_summary()
        print(json.dumps(info, indent=2))
        return 0

    # Discovery mode - find all available models
    if args.discover:
        discovered = discover_all_models(verbose=args.verbose)

        if args.output:
            Path(args.output).write_text(json.dumps(discovered, indent=2))
            print(f"Discovery saved to: {args.output}")
        else:
            print("\n" + "=" * 60)
            print("MODEL DISCOVERY REPORT")
            print("=" * 60)
            print(f"Total available: {discovered['summary']['total_available']}")
            print(
                f"Providers configured: {discovered['summary']['providers_configured']}"
            )
            print()

            for name, info in discovered["providers"].items():
                print(f"\n{name.upper().replace('_', ' ')}")
                if info.get("available"):
                    print(f"   [OK] {len(info['available'])} model(s) available:")
                    for m in info["available"][:10]:
                        print(f"      - {m}")
                    if len(info.get("available", [])) > 10:
                        print(f"      ... and {len(info['available']) - 10} more")
                elif info.get("configured"):
                    print("   [OK] Configured (use explicit model IDs)")
                else:
                    print(f"   [FAIL] {info.get('error', 'Not configured')}")

        return 0

    # Build model list
    models = list(args.models)

    if args.all_github:
        # Use full publisher/model format for GitHub models
        models.extend(
            [
                "gh:openai/gpt-4o-mini",
                "gh:openai/gpt-4o",
                "gh:openai/gpt-4.1",
                "gh:openai/gpt-4.1-nano",
                "gh:meta/llama-3.3-70b-instruct",
                "gh:mistralai/mistral-small-2503",
                "gh:openai/o1",
                "gh:openai/o3",
                "gh:deepseek/deepseek-r1",
                "gh:microsoft/phi-4",
            ]
        )

    if args.all_local:
        models.extend(
            [
                "local:phi4",
                "local:phi3.5",
                "local:phi3",
                "local:mistral",
                "local:phi3-medium",
            ]
        )

    if args.all_azure:
        models.extend(
            [
                "azure-foundry:default",
                "azure-openai:default",
            ]
        )

    if args.all_ollama:
        # Discover Ollama models dynamically
        try:
            discovered = discover_all_models(verbose=False)
            ollama_models = (
                discovered.get("providers", {}).get("ollama", {}).get("available", [])
            )
            models.extend(ollama_models)
        except Exception:
            pass

    if args.all_aitk:
        # Discover AI Toolkit local models dynamically
        try:
            discovered = discover_all_models(verbose=False)
            aitk_models = (
                discovered.get("providers", {})
                .get("ai_toolkit", {})
                .get("available", [])
            )
            models.extend(aitk_models)
        except Exception:
            pass

    if not models:
        selected_provider_group = any(
            [
                args.all_github,
                args.all_local,
                args.all_azure,
                args.all_ollama,
                args.all_aitk,
            ]
        )
        if selected_provider_group:
            print("No models discovered for the selected provider flags.")
            print(
                "Check provider connectivity/configuration (e.g., OLLAMA_HOST, "
                "gh auth, local model installation)."
            )
            return 1

        parser.print_help()
        return 1

    # Remove duplicates while preserving order
    seen: set[str] = set()
    unique_models = []
    for m in models:
        if m not in seen:
            seen.add(m)
            unique_models.append(m)

    # Get report
    report = probe.get_probe_report(unique_models)

    # Output
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"Report saved to: {args.output}")
    else:
        print("\n" + "=" * 60)
        print("Model Probe Report")
        print("=" * 60)
        print(
            f"Total: {report['total']} | Usable: {report['usable_count']} | Unusable: {report['unusable_count']}"
        )
        print()

        if report["usable"]:
            print("[OK] Usable models:")
            for m in report["usable"]:
                print(f"   {m}")

        if report["unusable"]:
            print("\n[FAIL] Unusable models:")
            for item in report["unusable"]:
                print(
                    f"   {item['model']}: {item['error_code']} - {item['error'][:60]}"
                )

        print()

    return 0 if report["unusable_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
