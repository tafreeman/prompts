#!/usr/bin/env python3
"""
Model Probe & Cache
===================

Provides runtime probing of model availability with persistent caching.
This prevents wasted evaluation runs on models that are known to be unavailable.

Features:
- Probe models once and cache results (per-session or persistent)
- Classify errors as transient vs permanent
- Filter model lists to runnable intersection
- Retry logic with exponential backoff for transient errors

Usage:
    from model_probe import ModelProbe
    
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
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib


# =============================================================================
# ERROR CLASSIFICATION - Import from canonical source
# =============================================================================

from tools.errors import ErrorCode, classify_error, TRANSIENT_ERRORS, PERMANENT_ERRORS


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
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# CACHE MANAGEMENT
# =============================================================================

def get_cache_dir() -> Path:
    """Get the directory for probe cache files."""
    cache_dir = Path.home() / ".cache" / "prompts-eval" / "model-probes"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_file() -> Path:
    """Get the main probe cache file."""
    return get_cache_dir() / "probe_cache.json"


def load_cache() -> Dict[str, Any]:
    """Load the probe cache from disk."""
    cache_file = get_cache_file()
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"version": "1.0.0", "probes": {}, "last_updated": None}


def save_cache(cache: Dict[str, Any]) -> None:
    """Save the probe cache to disk."""
    cache["last_updated"] = datetime.now().isoformat()
    cache_file = get_cache_file()
    cache_file.write_text(json.dumps(cache, indent=2), encoding="utf-8")


# =============================================================================
# MODEL PROBE CLASS
# =============================================================================

class ModelProbe:
    """
    Probes model availability and caches results.
    
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
        self._cache = load_cache() if use_cache else {"version": "1.0.0", "probes": {}}
        self._session_probes: Dict[str, ProbeResult] = {}
    
    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[ModelProbe] {msg}")
    
    def _get_provider(self, model: str) -> str:
        """Extract provider from model string."""
        if model.startswith("local:"):
            return "local"
        if model.startswith("windows-ai:"):
            return "windows_ai"
        if model.startswith("gh:") or model.startswith("github:"):
            return "github"
        if model.startswith("openai:") or model.startswith("gpt"):
            return "openai"
        if model.startswith("azure-foundry:"):
            return "azure_foundry"
        if model.startswith("azure-openai:"):
            return "azure_openai"
        if model.startswith("ollama:"):
            return "ollama"
        if model.startswith("gemini:"):
            return "gemini"
        if model.startswith("aitk:") or model.startswith("ai-toolkit:"):
            return "ai_toolkit"
        if model.startswith("claude:"):
            return "claude"
        return "unknown"
    
    def _cache_key(self, model: str) -> str:
        """Generate cache key for a model."""
        return hashlib.md5(model.encode()).hexdigest()[:12]
    
    def _is_cache_valid(self, cached: Dict[str, Any]) -> bool:
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
        elif error_code in [e.value for e in PERMANENT_ERRORS]:
            ttl = self.TTL_PERMANENT_ERROR
        else:
            ttl = self.TTL_TRANSIENT_ERROR
        
        return (now - probe_time) < ttl
    
    def _probe_local(self, model: str) -> ProbeResult:
        """Probe a local ONNX model."""
        start = time.time()
        model_key = model.replace("local:", "")
        
        try:
            # Check if model exists in AI Gallery cache
            ai_gallery = Path.home() / ".cache" / "aigallery"
            
            # Import LLMClient to get model paths
            sys.path.insert(0, str(Path(__file__).parent))
            from llm_client import LLMClient
            
            model_path = LLMClient.LOCAL_MODELS.get(model_key)
            if not model_path:
                return ProbeResult(
                    model=model,
                    provider="local",
                    usable=False,
                    error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                    error_message=f"Unknown local model key: {model_key}",
                    probe_time=datetime.now().isoformat(),
                    duration_ms=int((time.time() - start) * 1000),
                )
            
            # Check if the model directory exists
            top_dir = str(model_path).split("/")[0]
            if not (ai_gallery / top_dir).exists():
                return ProbeResult(
                    model=model,
                    provider="local",
                    usable=False,
                    error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                    error_message=f"Model not installed: {top_dir}",
                    probe_time=datetime.now().isoformat(),
                    duration_ms=int((time.time() - start) * 1000),
                )
            
            return ProbeResult(
                model=model,
                provider="local",
                usable=True,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        except Exception as e:
            code, retry = classify_error(str(e))
            return ProbeResult(
                model=model,
                provider="local",
                usable=False,
                error_code=code.value,
                error_message=str(e),
                should_retry=retry,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
    
    def _probe_github(self, model: str) -> ProbeResult:
        """Probe a GitHub Models model with a lightweight test."""
        start = time.time()
        model_id = model.replace("gh:", "").replace("github:", "")
        
        # Check if gh CLI is available
        import shutil
        if not shutil.which("gh"):
            return ProbeResult(
                model=model,
                provider="github",
                usable=False,
                error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                error_message="GitHub CLI (gh) not found on PATH",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # Check for authentication (env var OR gh auth)
        gh_authenticated = bool(os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"))
        
        if not gh_authenticated:
            # Check if logged in via gh auth
            try:
                auth_check = subprocess.run(
                    ["gh", "auth", "status"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                gh_authenticated = auth_check.returncode == 0
            except Exception:
                pass
        
        if not gh_authenticated:
            return ProbeResult(
                model=model,
                provider="github",
                usable=False,
                error_code=ErrorCode.PERMISSION_DENIED.value,
                error_message="Not authenticated (run: gh auth login or set GITHUB_TOKEN)",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # If model_id doesn't have a slash, we need to resolve it from gh models list
        if "/" not in model_id:
            try:
                result = subprocess.run(
                    ["gh", "models", "list"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    for line in result.stdout.strip().split("\n"):
                        if line.strip():
                            parts = line.split("\t")
                            if parts:
                                full_id = parts[0].strip()
                                # Check if model_id matches the short name
                                if full_id.endswith(f"/{model_id}") or full_id == model_id:
                                    model_id = full_id
                                    break
            except Exception:
                pass  # Continue with original model_id
        
        try:
            # Do a minimal probe - just ask for a single token response
            result = subprocess.run(
                ["gh", "models", "run", model_id, "Hi", "--max-tokens", "1"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            duration_ms = int((time.time() - start) * 1000)
            
            if result.returncode == 0:
                return ProbeResult(
                    model=model,
                    provider="github",
                    usable=True,
                    probe_time=datetime.now().isoformat(),
                    duration_ms=duration_ms,
                )
            else:
                error_text = result.stderr or result.stdout
                code, retry = classify_error(error_text, result.returncode)
                return ProbeResult(
                    model=model,
                    provider="github",
                    usable=False,
                    error_code=code.value,
                    error_message=error_text[:500],
                    should_retry=retry,
                    probe_time=datetime.now().isoformat(),
                    duration_ms=duration_ms,
                )
        
        except subprocess.TimeoutExpired:
            return ProbeResult(
                model=model,
                provider="github",
                usable=False,
                error_code=ErrorCode.TIMEOUT.value,
                error_message="Probe timed out after 30s",
                should_retry=True,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            code, retry = classify_error(str(e))
            return ProbeResult(
                model=model,
                provider="github",
                usable=False,
                error_code=code.value,
                error_message=str(e),
                should_retry=retry,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
    
    def _probe_model(self, model: str) -> ProbeResult:
        """Probe a model based on its provider."""
        provider = self._get_provider(model)
        
        if provider == "local":
            return self._probe_local(model)
        elif provider == "windows_ai":
            return self._probe_windows_ai(model)
        elif provider == "github":
            return self._probe_github(model)
        elif provider == "azure_foundry":
            return self._probe_azure_foundry(model)
        elif provider == "azure_openai":
            return self._probe_azure_openai(model)
        elif provider == "ollama":
            return self._probe_ollama(model)
        elif provider == "openai":
            return self._probe_openai(model)
        elif provider == "ai_toolkit":
            return self._probe_ai_toolkit(model)
        else:
            # For other providers, assume usable if configured
            # (full probing would require actual API calls)
            return ProbeResult(
                model=model,
                provider=provider,
                usable=True,  # Optimistic - will fail at runtime if not
                probe_time=datetime.now().isoformat(),
                duration_ms=0,
            )

    def _probe_windows_ai(self, model: str) -> ProbeResult:
        """Probe Windows AI (Phi Silica) via the .NET bridge --info."""
        start = time.time()

        if sys.platform != "win32":
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                error_message="Windows AI is only available on Windows",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )

        import shutil
        if not shutil.which("dotnet"):
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                error_message="dotnet not found on PATH (install .NET SDK)",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )

        bridge_proj = Path(__file__).parent / "windows_ai_bridge" / "PhiSilicaBridge.csproj"
        if not bridge_proj.exists():
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=ErrorCode.FILE_NOT_FOUND.value,
                error_message="Bridge project not found (tools/windows_ai_bridge/PhiSilicaBridge.csproj)",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )

        try:
            r = subprocess.run(
                ["dotnet", "run", "--project", str(bridge_proj), "--", "--info"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(bridge_proj.parent),
            )

            stdout = (r.stdout or "").strip()
            stderr = (r.stderr or "").strip()
            duration_ms = int((time.time() - start) * 1000)

            info: Dict[str, Any] = {}
            if stdout:
                try:
                    info = json.loads(stdout)
                except Exception:
                    info = {}

            available = bool(info.get("available")) if info else False
            if available:
                return ProbeResult(
                    model=model,
                    provider="windows_ai",
                    usable=True,
                    probe_time=datetime.now().isoformat(),
                    duration_ms=duration_ms,
                )

            err_msg = None
            if info:
                err_msg = info.get("error")
            err_msg = err_msg or stderr or stdout or "Windows AI not available"

            # Add a little extra context for common Phi Silica failures.
            msg_lower = str(err_msg).lower()
            if "limited access feature" in msg_lower or "unauthorized" in msg_lower:
                err_msg = (
                    f"{err_msg} | Phi Silica may require a Limited Access Feature (LAF) token "
                    f"and/or package identity + systemAIModels capability. "
                    f"See: https://learn.microsoft.com/windows/ai/apis/troubleshooting "
                    f"(unlock: https://aka.ms/phi-silica-unlock)"
                )
            code, retry = classify_error(str(err_msg), r.returncode)
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=code.value,
                error_message=str(err_msg)[:500],
                should_retry=retry,
                probe_time=datetime.now().isoformat(),
                duration_ms=duration_ms,
            )

        except subprocess.TimeoutExpired:
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=ErrorCode.TIMEOUT.value,
                error_message="Bridge probe timed out after 60s",
                should_retry=True,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            code, retry = classify_error(str(e))
            return ProbeResult(
                model=model,
                provider="windows_ai",
                usable=False,
                error_code=code.value,
                error_message=str(e),
                should_retry=retry,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
    
    def _probe_azure_foundry(self, model: str) -> ProbeResult:
        """Probe an Azure Foundry model."""
        start = time.time()
        _ = model.replace("azure-foundry:", "")
        
        # Check for API key
        api_key = os.getenv("AZURE_FOUNDRY_API_KEY")
        if not api_key:
            return ProbeResult(
                model=model,
                provider="azure_foundry",
                usable=False,
                error_code=ErrorCode.PERMISSION_DENIED.value,
                error_message="No AZURE_FOUNDRY_API_KEY environment variable",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # Check for endpoint
        endpoint = None
        for k, v in os.environ.items():
            if k.startswith("AZURE_FOUNDRY_ENDPOINT") and v:
                endpoint = v
                break
        
        if not endpoint:
            return ProbeResult(
                model=model,
                provider="azure_foundry",
                usable=False,
                error_code=ErrorCode.INVALID_INPUT.value,
                error_message="No AZURE_FOUNDRY_ENDPOINT_* environment variable",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # Assume configured = usable (actual probe would require API call)
        return ProbeResult(
            model=model,
            provider="azure_foundry",
            usable=True,
            probe_time=datetime.now().isoformat(),
            duration_ms=int((time.time() - start) * 1000),
        )
    
    def _probe_azure_openai(self, model: str) -> ProbeResult:
        """Probe an Azure OpenAI model."""
        start = time.time()
        model_id = model.replace("azure-openai:", "")
        
        # Check for endpoint and key (check slots 0-9)
        configured = False
        for i in range(10):
            ep = os.getenv(f"AZURE_OPENAI_ENDPOINT_{i}")
            key = os.getenv(f"AZURE_OPENAI_API_KEY_{i}")
            if ep and key:
                configured = True
                break
        
        if not configured:
            # Also check default (non-numbered) env vars
            if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
                configured = True
        
        if not configured:
            return ProbeResult(
                model=model,
                provider="azure_openai",
                usable=False,
                error_code=ErrorCode.PERMISSION_DENIED.value,
                error_message="No AZURE_OPENAI_ENDPOINT/API_KEY environment variables",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        return ProbeResult(
            model=model,
            provider="azure_openai",
            usable=True,
            probe_time=datetime.now().isoformat(),
            duration_ms=int((time.time() - start) * 1000),
        )
    
    def _probe_ollama(self, model: str) -> ProbeResult:
        """Probe an Ollama model."""
        import urllib.request
        import urllib.error
        
        start = time.time()
        model_id = model.replace("ollama:", "")
        
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        
        try:
            # Check if Ollama is running
            req = urllib.request.Request(
                f"{ollama_host}/api/tags",
                headers={"Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                
                # Check if specific model is available
                if model_id and model_id not in models and f"{model_id}:latest" not in models:
                    return ProbeResult(
                        model=model,
                        provider="ollama",
                        usable=False,
                        error_code=ErrorCode.UNAVAILABLE_MODEL.value,
                        error_message=f"Model '{model_id}' not found. Available: {', '.join(models[:5])}",
                        probe_time=datetime.now().isoformat(),
                        duration_ms=int((time.time() - start) * 1000),
                    )
                
                return ProbeResult(
                    model=model,
                    provider="ollama",
                    usable=True,
                    probe_time=datetime.now().isoformat(),
                    duration_ms=int((time.time() - start) * 1000),
                )
        
        except urllib.error.URLError as e:
            return ProbeResult(
                model=model,
                provider="ollama",
                usable=False,
                error_code=ErrorCode.NETWORK_ERROR.value,
                error_message=f"Ollama not reachable at {ollama_host}: {e}",
                should_retry=True,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            code, retry = classify_error(str(e))
            return ProbeResult(
                model=model,
                provider="ollama",
                usable=False,
                error_code=code.value,
                error_message=str(e),
                should_retry=retry,
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
    
    def _probe_openai(self, model: str) -> ProbeResult:
        """Probe an OpenAI model."""
        start = time.time()
        model_id = model.replace("openai:", "")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return ProbeResult(
                model=model,
                provider="openai",
                usable=False,
                error_code=ErrorCode.PERMISSION_DENIED.value,
                error_message="No OPENAI_API_KEY environment variable",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        return ProbeResult(
            model=model,
            provider="openai",
            usable=True,
            probe_time=datetime.now().isoformat(),
            duration_ms=int((time.time() - start) * 1000),
        )
    
    def _probe_ai_toolkit(self, model: str) -> ProbeResult:
        """
        Probe an AI Toolkit local model.
        
        AI Toolkit stores downloaded models in ~/.aitk/models/ with metadata
        in ~/.aitk/models/foundry.modelinfo.json (these are FREE local ONNX models,
        NOT paid cloud Foundry models).
        
        Model format: aitk:<model-alias> or aitk:<full-model-name>
        Examples: aitk:phi-4-mini, aitk:qwen2.5-coder-7b
        """
        start = time.time()
        model_id = model.replace("aitk:", "").replace("ai-toolkit:", "")
        
        aitk_base = Path.home() / ".aitk"
        models_dir = aitk_base / "models"
        modelinfo_file = models_dir / "foundry.modelinfo.json"
        
        # Check if AI Toolkit is installed
        if not aitk_base.exists():
            return ProbeResult(
                model=model,
                provider="ai_toolkit",
                usable=False,
                error_code=ErrorCode.FILE_NOT_FOUND.value,
                error_message="AI Toolkit not installed (~/.aitk not found)",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # Check if models directory exists
        if not models_dir.exists():
            return ProbeResult(
                model=model,
                provider="ai_toolkit",
                usable=False,
                error_code=ErrorCode.FILE_NOT_FOUND.value,
                error_message="No AI Toolkit models downloaded (~/.aitk/models not found)",
                probe_time=datetime.now().isoformat(),
                duration_ms=int((time.time() - start) * 1000),
            )
        
        # Load model info to check available models
        available_aliases = []
        available_names = []
        
        if modelinfo_file.exists():
            try:
                info = json.loads(modelinfo_file.read_text(encoding="utf-8"))
                for m in info.get("models", []):
                    if m.get("task") == "chat-completion":  # Only chat models
                        alias = m.get("alias", "")
                        name = m.get("name", "")
                        if alias:
                            available_aliases.append(alias)
                        if name:
                            available_names.append(name)
            except Exception:
                pass
        
        # Check downloaded models in the models directory
        downloaded = []
        if models_dir.exists():
            for subdir in models_dir.iterdir():
                if subdir.is_dir() and subdir.name != "Microsoft":
                    downloaded.append(subdir.name)
            # Also check Microsoft subdir
            ms_dir = models_dir / "Microsoft"
            if ms_dir.exists():
                for subdir in ms_dir.iterdir():
                    if subdir.is_dir():
                        downloaded.append(subdir.name)
        
        # Match model_id against available aliases, names, and downloaded folders
        model_lower = model_id.lower()
        
        # Direct match against aliases
        if model_lower in [a.lower() for a in available_aliases]:
            # Check if it's actually downloaded
            # Find the corresponding model name
            for d in downloaded:
                if model_lower in d.lower():
                    return ProbeResult(
                        model=model,
                        provider="ai_toolkit",
                        usable=True,
                        probe_time=datetime.now().isoformat(),
                        duration_ms=int((time.time() - start) * 1000),
                    )
        
        # Fuzzy match against downloaded models
        for d in downloaded:
            d_lower = d.lower()
            if model_lower in d_lower or d_lower.startswith(model_lower.replace("-", "")):
                return ProbeResult(
                    model=model,
                    provider="ai_toolkit",
                    usable=True,
                    probe_time=datetime.now().isoformat(),
                    duration_ms=int((time.time() - start) * 1000),
                )
        
        # Model not found
        return ProbeResult(
            model=model,
            provider="ai_toolkit",
            usable=False,
            error_code=ErrorCode.UNAVAILABLE_MODEL.value,
            error_message=f"Model '{model_id}' not downloaded. Available: {', '.join(downloaded[:5])}",
            probe_time=datetime.now().isoformat(),
            duration_ms=int((time.time() - start) * 1000),
        )
    
    def check_model(self, model: str, force_probe: bool = False) -> ProbeResult:
        """
        Check if a model is usable.
        
        Args:
            model: Model identifier (e.g., "gh:gpt-4o-mini", "local:phi4")
            force_probe: Skip cache and probe fresh
            
        Returns:
            ProbeResult with usability status
        """
        cache_key = self._cache_key(model)
        
        # Check session cache first (fastest)
        if not force_probe and cache_key in self._session_probes:
            result = self._session_probes[cache_key]
            result.cached = True
            return result
        
        # Check persistent cache
        if not force_probe and self.use_cache:
            cached = self._cache.get("probes", {}).get(cache_key)
            if cached and self._is_cache_valid(cached):
                result = ProbeResult(**cached)
                result.cached = True
                self._session_probes[cache_key] = result
                self._log(f"Cache hit: {model} -> usable={result.usable}")
                return result
        
        # Probe the model
        self._log(f"Probing: {model}")
        result = self._probe_model(model)
        
        # Cache the result
        self._session_probes[cache_key] = result
        if self.use_cache:
            self._cache.setdefault("probes", {})[cache_key] = result.to_dict()
            save_cache(self._cache)
        
        self._log(f"Probe complete: {model} -> usable={result.usable}, error={result.error_code}")
        return result
    
    def filter_runnable(self, models: List[str], force_probe: bool = False) -> List[str]:
        """
        Filter a list of models to only those that are runnable.
        
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
    
    def get_probe_report(self, models: List[str]) -> Dict[str, Any]:
        """
        Get a detailed probe report for a list of models.
        
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
                {"model": m, "error_code": c, "error": e}
                for m, c, e in unusable
            ],
            "details": results,
        }
    
    def clear_cache(self, model: str = None) -> None:
        """
        Clear probe cache.
        
        Args:
            model: If provided, clear only this model. Otherwise clear all.
        """
        if model:
            cache_key = self._cache_key(model)
            self._session_probes.pop(cache_key, None)
            self._cache.get("probes", {}).pop(cache_key, None)
        else:
            self._session_probes.clear()
            self._cache["probes"] = {}
        
        if self.use_cache:
            save_cache(self._cache)
    
    def get_cache_summary(self) -> Dict[str, Any]:
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
# RETRY DECORATOR
# =============================================================================

def with_retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential: bool = True,
):
    """
    Decorator for retrying functions with exponential backoff.
    
    Only retries on transient errors (rate limit, timeout, network).
    
    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap
        exponential: Use exponential backoff
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            last_code = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e)
                    code, should_retry = classify_error(error_str)
                    last_error = error_str
                    last_code = code
                    
                    if not should_retry or attempt >= max_retries:
                        # Don't retry permanent errors or if we've exhausted retries
                        raise
                    
                    # Calculate delay
                    if exponential:
                        delay = min(base_delay * (2 ** attempt), max_delay)
                    else:
                        delay = base_delay
                    
                    # Add jitter (±20%)
                    import random
                    delay = delay * (0.8 + random.random() * 0.4)
                    
                    print(f"[Retry] {code.value}: attempt {attempt + 1}/{max_retries}, waiting {delay:.1f}s")
                    time.sleep(delay)
            
            # Should not reach here, but just in case
            raise RuntimeError(f"Exhausted retries: {last_code} - {last_error}")
        
        return wrapper
    return decorator


# =============================================================================
# DISCOVERY FUNCTIONS
# =============================================================================

def discover_all_models(verbose: bool = False) -> Dict[str, Any]:
    """
    Discover all available models from all configured providers.
    
    Returns a dict with models grouped by provider.
    """
    import urllib.request
    import urllib.error
    import shutil
    
    discovered = {
        "timestamp": datetime.now().isoformat(),
        "providers": {},
    }
    
    # 1. Local ONNX (AI Gallery)
    if verbose:
        print("[Discovery] Checking local ONNX models...")
    
    ai_gallery = Path.home() / ".cache" / "aigallery"
    local_models = []
    local_missing = []
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from llm_client import LLMClient
        
        for key, model_path in LLMClient.LOCAL_MODELS.items():
            top_dir = str(model_path).split("/")[0]
            if ai_gallery.exists() and (ai_gallery / top_dir).exists():
                local_models.append(f"local:{key}")
            else:
                local_missing.append(f"local:{key}")
    except Exception as e:
        if verbose:
            print(f"  Error: {e}")
    
    discovered["providers"]["local_onnx"] = {
        "available": local_models,
        "missing": local_missing,
        "count": len(local_models),
        "path": str(ai_gallery),
    }
    
    # 2. GitHub Models
    if verbose:
        print("[Discovery] Checking GitHub Models...")
    
    gh_models = []
    gh_error = None
    gh_authenticated = False
    
    # Check for gh CLI and authentication (either via env var or gh auth)
    if shutil.which("gh"):
        # Check if logged in via gh auth
        try:
            auth_check = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            gh_authenticated = auth_check.returncode == 0
        except Exception:
            pass
        
        # Also accept env var token
        if not gh_authenticated:
            gh_authenticated = bool(os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"))
    
    if gh_authenticated:
        try:
            # List models via gh CLI (plain text format: "model-id<tab>Description")
            result = subprocess.run(
                ["gh", "models", "list"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                # Parse tab-separated output: "publisher/model<tab>Display Name"
                for line in result.stdout.strip().split("\n"):
                    if line.strip():
                        # First column is the model ID (full format: publisher/model)
                        parts = line.split("\t")
                        if parts:
                            model_id = parts[0].strip()
                            if model_id:
                                gh_models.append(f"gh:{model_id}")
            else:
                gh_error = result.stderr[:200] if result.stderr else "Unknown error"
        except Exception as e:
            gh_error = str(e)
    else:
        gh_error = "gh CLI not available or not authenticated (run: gh auth login)"
    
    discovered["providers"]["github_models"] = {
        "available": gh_models,
        "count": len(gh_models),
        "error": gh_error,
    }
    
    # 3. Ollama
    if verbose:
        print("[Discovery] Checking Ollama models...")
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_models = []
    ollama_error = None
    
    try:
        req = urllib.request.Request(
            f"{ollama_host}/api/tags",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ollama_models = [f"ollama:{m.get('name', '')}" for m in data.get("models", [])]
    except Exception as e:
        ollama_error = f"Ollama not reachable at {ollama_host}"
    
    discovered["providers"]["ollama"] = {
        "available": ollama_models,
        "count": len(ollama_models),
        "host": ollama_host,
        "error": ollama_error,
    }
    
    # 4. Azure Foundry
    if verbose:
        print("[Discovery] Checking Azure Foundry...")
    
    foundry_configured = bool(os.getenv("AZURE_FOUNDRY_API_KEY"))
    foundry_endpoints = []
    for k, v in os.environ.items():
        if k.startswith("AZURE_FOUNDRY_ENDPOINT") and v:
            foundry_endpoints.append(v)
    
    discovered["providers"]["azure_foundry"] = {
        "configured": foundry_configured and bool(foundry_endpoints),
        "endpoints": foundry_endpoints,
        "notes": "Azure Foundry models require explicit model IDs (azure-foundry:model-name)",
    }
    
    # 5. Azure OpenAI
    if verbose:
        print("[Discovery] Checking Azure OpenAI...")
    
    azure_slots = []
    for i in range(10):
        ep = os.getenv(f"AZURE_OPENAI_ENDPOINT_{i}")
        key = os.getenv(f"AZURE_OPENAI_API_KEY_{i}")
        deployment = os.getenv(f"AZURE_OPENAI_DEPLOYMENT_{i}")
        if ep and key:
            azure_slots.append({
                "slot": i,
                "endpoint": ep[:50] + "..." if len(ep) > 50 else ep,
                "deployment": deployment,
            })
    
    # Also check default env vars
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        azure_slots.append({
            "slot": "default",
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "")[:50],
            "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        })
    
    discovered["providers"]["azure_openai"] = {
        "configured": bool(azure_slots),
        "slots": azure_slots,
        "notes": "Use azure-openai:deployment-name to specify model",
    }
    
    # 6. OpenAI (direct)
    if verbose:
        print("[Discovery] Checking OpenAI API...")
    
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    openai_models = []
    
    if openai_configured:
        try:
            from llm_client import LLMClient
            openai_models = [f"openai:{m}" for m in LLMClient.list_openai_models()[:20]]
        except Exception:
            openai_models = ["openai:gpt-4o", "openai:gpt-4o-mini", "openai:gpt-4-turbo"]
    
    discovered["providers"]["openai"] = {
        "configured": openai_configured,
        "available": openai_models,
        "count": len(openai_models),
    }
    
    # 7. Windows AI (Phi Silica)
    if verbose:
        print("[Discovery] Checking Windows AI / Phi Silica...")
    
    windows_ai_available = False
    windows_ai_error = None
    windows_ai_ready_state = None
    
    if sys.platform == "win32" and shutil.which("dotnet"):
        bridge_proj = Path(__file__).parent / "windows_ai_bridge" / "PhiSilicaBridge.csproj"
        if bridge_proj.exists():
            try:
                result = subprocess.run(
                    ["dotnet", "run", "--project", str(bridge_proj), "--", "--info"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=str(bridge_proj.parent),
                )
                stdout = (result.stdout or "").strip()
                stderr = (result.stderr or "").strip()

                info = None
                if stdout:
                    try:
                        info = json.loads(stdout)
                    except Exception:
                        info = None

                if isinstance(info, dict):
                    windows_ai_available = bool(info.get("available", False))
                    windows_ai_ready_state = info.get("readyState")
                    if not windows_ai_available:
                        windows_ai_error = info.get("error") or stderr or "Unknown"
                else:
                    windows_ai_error = stderr or stdout or "Bridge did not return JSON"
            except Exception as e:
                windows_ai_error = str(e)
        else:
            windows_ai_error = "Bridge project not found"
    else:
        windows_ai_error = "Windows only / dotnet not available"
    
    discovered["providers"]["windows_ai"] = {
        "available": windows_ai_available,
        "readyState": windows_ai_ready_state,
        "models": ["windows-ai:phi-silica"] if windows_ai_available else [],
        "error": windows_ai_error,
    }
    
    # 8. AI Toolkit Local Models (FREE - local ONNX models from VS Code AI Toolkit)
    if verbose:
        print("[Discovery] Checking AI Toolkit local models...")
    
    aitk_base = Path.home() / ".aitk"
    aitk_models_dir = aitk_base / "models"
    aitk_modelinfo = aitk_models_dir / "foundry.modelinfo.json"
    
    aitk_models = []
    aitk_catalog = []  # Available but not downloaded
    aitk_error = None
    
    if not aitk_base.exists():
        aitk_error = "AI Toolkit not installed (run: code --install-extension ms-windows-ai-studio.windows-ai-studio)"
    elif not aitk_models_dir.exists():
        aitk_error = "No AI Toolkit models downloaded"
    else:
        # Get downloaded models
        downloaded = []
        for subdir in aitk_models_dir.iterdir():
            if subdir.is_dir() and subdir.name not in ("Microsoft",):
                downloaded.append(subdir.name)
        # Also check Microsoft subdir
        ms_dir = aitk_models_dir / "Microsoft"
        if ms_dir.exists():
            for subdir in ms_dir.iterdir():
                if subdir.is_dir():
                    downloaded.append(subdir.name)
        
        # Map downloaded folders to aitk: model IDs
        for d in downloaded:
            # Simplify name for model ID
            simple_name = d.lower()
            # Remove version suffixes like "-generic-cpu-5"
            for suffix in ["-generic-cpu", "-generic-gpu", "-cpu", "-gpu"]:
                if suffix in simple_name:
                    simple_name = simple_name.split(suffix)[0]
            # Remove trailing version numbers like -1, -2, -3
            while simple_name and simple_name[-1].isdigit():
                simple_name = simple_name.rstrip("0123456789-")
            aitk_models.append(f"aitk:{simple_name}")
        
        # Deduplicate
        aitk_models = list(dict.fromkeys(aitk_models))
        
        # Load catalog to show available but not downloaded
        if aitk_modelinfo.exists():
            try:
                info = json.loads(aitk_modelinfo.read_text(encoding="utf-8"))
                for m in info.get("models", []):
                    if m.get("task") == "chat-completion":
                        alias = m.get("alias", "")
                        if alias:
                            catalog_id = f"aitk:{alias}"
                            if catalog_id not in aitk_models:
                                aitk_catalog.append(catalog_id)
            except Exception:
                pass
    
    discovered["providers"]["ai_toolkit"] = {
        "available": aitk_models,
        "count": len(aitk_models),
        "catalog": aitk_catalog[:10],  # First 10 not-downloaded models
        "path": str(aitk_models_dir) if aitk_models_dir.exists() else None,
        "error": aitk_error,
        "notes": "FREE local ONNX models via VS Code AI Toolkit (NOT cloud/paid)",
    }
    
    # Summary
    total_available = sum(
        len(p.get("available", []))
        for p in discovered["providers"].values()
        if isinstance(p.get("available"), list)
    )
    discovered["summary"] = {
        "total_available": total_available,
        "providers_configured": sum(
            1 for p in discovered["providers"].values()
            if p.get("configured", False) or p.get("available")
        ),
    }
    
    return discovered


def is_model_usable(model: str) -> bool:
    """Quick check if a model is usable."""
    return get_probe().check_model(model).usable


def filter_usable_models(models: List[str]) -> List[str]:
    """Filter a list to only usable models."""
    return get_probe().filter_runnable(models)


def get_model_error(model: str) -> Optional[str]:
    """Get the error message for an unusable model."""
    result = get_probe().check_model(model)
    return result.error_message if not result.usable else None


# =============================================================================
# CANONICAL SINGLETON ACCESS
# =============================================================================

_DEFAULT_PROBE: Optional[ModelProbe] = None


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

def main(argv: List[str]) -> int:
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Probe model availability")
    parser.add_argument("models", nargs="*", help="Models to probe")
    parser.add_argument("--all-github", action="store_true", help="Probe common GitHub models")
    parser.add_argument("--all-local", action="store_true", help="Probe all local ONNX models")
    parser.add_argument("--all-azure", action="store_true", help="Check Azure Foundry/OpenAI")
    parser.add_argument("--all-ollama", action="store_true", help="Probe Ollama models")
    parser.add_argument("--all-aitk", action="store_true", help="Probe AI Toolkit local models (free)")
    parser.add_argument("--discover", action="store_true", help="Discover all available models from all providers")
    parser.add_argument("--force", action="store_true", help="Force fresh probe (ignore cache)")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the probe cache")
    parser.add_argument("--cache-info", action="store_true", help="Show cache information")
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
            print(f"\n{'='*60}")
            print("MODEL DISCOVERY REPORT")
            print(f"{'='*60}")
            print(f"Total available: {discovered['summary']['total_available']}")
            print(f"Providers configured: {discovered['summary']['providers_configured']}")
            print()
            
            for name, info in discovered["providers"].items():
                print(f"\n📦 {name.upper().replace('_', ' ')}")
                if info.get("available"):
                    print(f"   ✅ {len(info['available'])} model(s) available:")
                    for m in info["available"][:10]:
                        print(f"      - {m}")
                    if len(info.get("available", [])) > 10:
                        print(f"      ... and {len(info['available']) - 10} more")
                elif info.get("configured"):
                    print(f"   ✅ Configured (use explicit model IDs)")
                else:
                    print(f"   ❌ {info.get('error', 'Not configured')}")
        
        return 0
    
    # Build model list
    models = list(args.models)
    
    if args.all_github:
        # Use full publisher/model format for GitHub models
        models.extend([
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
        ])
    
    if args.all_local:
        models.extend([
            "local:phi4",
            "local:phi3.5",
            "local:phi3",
            "local:mistral",
            "local:phi3-medium",
        ])
    
    if args.all_azure:
        models.extend([
            "azure-foundry:default",
            "azure-openai:default",
        ])
    
    if args.all_ollama:
        # Discover Ollama models dynamically
        try:
            discovered = discover_all_models(verbose=False)
            ollama_models = discovered.get("providers", {}).get("ollama", {}).get("available", [])
            models.extend(ollama_models)
        except Exception:
            pass
    
    if args.all_aitk:
        # Discover AI Toolkit local models dynamically
        try:
            discovered = discover_all_models(verbose=False)
            aitk_models = discovered.get("providers", {}).get("ai_toolkit", {}).get("available", [])
            models.extend(aitk_models)
        except Exception:
            pass
    
    if not models:
        parser.print_help()
        return 1
    
    # Remove duplicates while preserving order
    seen = set()
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
        print(f"\n{'='*60}")
        print(f"Model Probe Report")
        print(f"{'='*60}")
        print(f"Total: {report['total']} | Usable: {report['usable_count']} | Unusable: {report['unusable_count']}")
        print()
        
        if report["usable"]:
            print("[OK] Usable models:")
            for m in report["usable"]:
                print(f"   {m}")
        
        if report["unusable"]:
            print("\n[FAIL] Unusable models:")
            for item in report["unusable"]:
                print(f"   {item['model']}: {item['error_code']} - {item['error'][:60]}")
        
        print()
    
    return 0 if report["unusable_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
