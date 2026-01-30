"""
Unified Model Manager

Provides a consistent interface for all model providers with:
- Automatic fallback strategies
- Comprehensive logging
- Async/parallel execution support
- Model health checking
- Instance caching

Integrates with existing repository patterns from tools/llm/llm_client.py.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional, Union

import yaml

from multiagent_workflows.core.logger import VerboseLogger

# Add repository tools to path for imports
REPO_ROOT = Path(__file__).parent.parent.parent.parent.parent
TOOLS_PATH = REPO_ROOT / "tools"
if TOOLS_PATH.exists() and str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

# Try to import existing repository tools
try:
    from llm.llm_client import LLMClient
    HAS_LLM_CLIENT = True
except ImportError:
    HAS_LLM_CLIENT = False
    LLMClient = None

try:
    from llm.model_probe import discover_all_models, get_probe
    HAS_MODEL_PROBE = True
except ImportError:
    HAS_MODEL_PROBE = False
    discover_all_models = None
    get_probe = None


@dataclass
class ModelInfo:
    """Information about a model."""
    id: str
    name: str
    provider: str
    capabilities: List[str]
    cost_tier: str
    available: bool = False
    context_length: int = 4096


@dataclass 
class GenerationResult:
    """Result from a model generation call."""
    text: str
    model_id: str
    tokens_used: int = 0
    timing_ms: float = 0.0
    cost_estimate: float = 0.0


class ModelManager:
    """
    Unified interface for all model providers with comprehensive logging.
    
    Wraps tools/llm_client.py patterns for consistency while adding:
    - Automatic fallback strategies (premium → mid-tier → local)
    - All calls logged with full context
    - Async execution support
    - Model availability checking
    
    Example:
        manager = ModelManager(config, logger)
        result = await manager.generate("gh:gpt-4o", "Hello, world!")
        print(result.text)
    """
    
    # Default routing for task types
    TASK_ROUTING = {
        "vision": ["gh:openai/gpt-4o", "local:phi3.5-vision"],
        "reasoning": ["gh:openai/gpt-4o", "gh:openai/o3-mini", "gh:openai/gpt-4o-mini"],
        "code_gen": ["gh:openai/gpt-4o", "gh:openai/gpt-4o-mini", "local:phi4"],
        "code_review": ["gh:openai/gpt-4o", "gh:openai/gpt-4o-mini", "local:phi4"],
        "coordination": ["gh:openai/gpt-4o-mini", "gh:openai/gpt-4o", "local:phi4"],
        "documentation": ["gh:openai/gpt-4o-mini", "gh:openai/gpt-4o", "local:phi4"],
    }
    
    # Cost estimates per 1M tokens (input + output average)
    COST_PER_MILLION = {
        "gh:openai/gpt-4o": 15.0,
        "gh:openai/gpt-4o-mini": 0.6,
        "gh:openai/o3-mini": 25.0,
        "gh:openai/o4-mini": 25.0,
        "gh:deepseek/deepseek-r1": 5.0,
        "local:phi4": 0.0,
        "local:phi4mini": 0.0,
        "local:phi3.5-vision": 0.0,
        "ollama:qwen2.5-coder:14b": 0.0,
        "ollama:deepseek-r1:14b": 0.0,
    }
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        logger: Optional[VerboseLogger] = None,
        allow_remote: bool = True,
    ):
        """
        Initialize ModelManager.
        
        Args:
            config: Model configuration dict (or loaded from config/models.yaml)
            logger: VerboseLogger instance for logging
            allow_remote: Whether to allow cloud model calls
        """
        self.config = config or self._load_default_config()
        self.logger = logger
        self.allow_remote = allow_remote
        
        # Initialize LLM client if available
        self._llm_client = LLMClient() if HAS_LLM_CLIENT else None
        
        # Model availability cache
        self._availability_cache: Dict[str, bool] = {}
        self._cache_ttl = 300  # 5 minutes
        self._cache_time: Dict[str, float] = {}
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration from config/models.yaml."""
        config_path = Path(__file__).parent.parent.parent.parent / "config" / "models.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {"providers": {}, "routing": {}, "fallback": {"chain": []}}
    
    async def generate(
        self,
        model_id: str,
        prompt: str,
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
    ) -> Union[GenerationResult, AsyncIterator[str]]:
        """
        Generate response from a model with full logging.
        
        Args:
            model_id: Model identifier (e.g., "gh:gpt-4o", "local:phi4")
            prompt: User prompt
            context: Optional context to prepend
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0 = deterministic)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream response
            
        Returns:
            GenerationResult with text, timing, and token info
        """
        start_time = time.perf_counter()
        
        # Combine context and prompt
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        params = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        
        # Log the call
        call_id = None
        if self.logger:
            call_id = self.logger.log_model_call(
                agent_id="model_manager",
                model_id=model_id,
                prompt=full_prompt,
                params=params,
            )
        
        try:
            # Check if remote calls allowed
            if not self.allow_remote and self._is_remote_model(model_id):
                raise ValueError(f"Remote model {model_id} not allowed (allow_remote=False)")
            
            # Try to generate
            response_text = await self._call_model(
                model_id=model_id,
                prompt=full_prompt,
                system_instruction=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            tokens = self._estimate_tokens(full_prompt, response_text)
            cost = self._estimate_cost(model_id, tokens)
            
            # Log response
            if self.logger and call_id:
                self.logger.log_model_response(
                    call_id=call_id,
                    response=response_text,
                    timing_ms=elapsed_ms,
                    tokens=tokens,
                    cost=cost,
                )
            
            return GenerationResult(
                text=response_text,
                model_id=model_id,
                tokens_used=tokens,
                timing_ms=elapsed_ms,
                cost_estimate=cost,
            )
            
        except Exception as e:
            if self.logger and call_id:
                self.logger.log_model_error(call_id, e)
            
            # Try fallback
            fallback_model = await self._get_fallback(model_id)
            if fallback_model:
                return await self.generate(
                    model_id=fallback_model,
                    prompt=prompt,
                    context=context,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                )
            raise
    
    async def _call_model(
        self,
        model_id: str,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Call the appropriate model provider."""
        if self._llm_client:
            # Use existing LLMClient from repository
            return await asyncio.to_thread(
                self._llm_client.generate_text,
                model_name=model_id,
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            # Fallback implementation
            return await self._fallback_call(
                model_id, prompt, system_instruction, temperature, max_tokens
            )
    
    async def _fallback_call(
        self,
        model_id: str,
        prompt: str,
        system_instruction: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Fallback implementation when LLMClient is not available."""
        # This is a basic implementation - in practice, would implement
        # direct API calls to providers
        
        if model_id.startswith("local:"):
            # Try local ONNX model
            try:
                from llm.local_model import LocalModel
                model = LocalModel(model_key=model_id.replace("local:", ""))
                return model.generate(
                    prompt=prompt,
                    system_prompt=system_instruction,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
            except ImportError:
                pass
        
        elif model_id.startswith("ollama:"):
            # Call Ollama API directly
            return await self._call_ollama(
                model_id.replace("ollama:", ""),
                prompt,
                system_instruction,
            )
        
        elif model_id.startswith("gh:"):
            # Call GitHub Models API
            return await self._call_github_models(
                model_id.replace("gh:", ""),
                prompt,
                system_instruction,
            )
        
        raise ValueError(f"No implementation available for model: {model_id}")
    
    async def _call_ollama(
        self,
        model_name: str,
        prompt: str,
        system_instruction: Optional[str],
    ) -> str:
        """Call Ollama API directly."""
        import httpx
        
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    
        headers = {
            "Content-Type": "application/json",
        }
        
        # Add auth if available
        api_key = os.environ.get("OLLAMA_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{host}/api/chat",
                json={
                    "model": model_name,
                    "messages": messages,
                    "stream": False,
                },
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("message", {}).get("content", "")
    
    async def _call_github_models(
        self,
        model_name: str,
        prompt: str,
        system_instruction: Optional[str],
    ) -> str:
        """Call GitHub Models API directly."""
        import httpx
        
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable required for GitHub Models")
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://models.github.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model_name,
                    "messages": messages,
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def check_availability(self, model_id: str) -> bool:
        """Check if a model is available and healthy."""
        # Check cache first
        now = time.time()
        if model_id in self._availability_cache:
            if now - self._cache_time.get(model_id, 0) < self._cache_ttl:
                return self._availability_cache[model_id]
        
        # Check availability
        available = False
        try:
            if HAS_MODEL_PROBE:
                probe = get_probe()
                result = await asyncio.to_thread(probe.check_model, model_id)
                available = result.usable if hasattr(result, "usable") else bool(result)
            else:
                # Simple availability check
                if model_id.startswith("local:"):
                    available = self._check_local_model(model_id)
                elif model_id.startswith("ollama:"):
                    available = await self._check_ollama()
                else:
                    # Assume cloud models available if we have credentials
                    available = self._has_credentials(model_id)
        except Exception:
            available = False
        
        # Update cache
        self._availability_cache[model_id] = available
        self._cache_time[model_id] = now
        
        return available
    
    def _check_local_model(self, model_id: str) -> bool:
        """Check if a local ONNX model is available."""
        try:
            from llm.local_model import check_model_available
            return check_model_available()
        except ImportError:
            return False
    
    async def _check_ollama(self) -> bool:
        """Check if Ollama server is running."""
        import httpx
        
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        
        headers = {}
        api_key = os.environ.get("OLLAMA_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{host}/api/tags", headers=headers)
                return response.status_code == 200
        except Exception:
            return False
    
    def _has_credentials(self, model_id: str) -> bool:
        """Check if credentials are available for a model."""
        if model_id.startswith("gh:"):
            return bool(os.environ.get("GITHUB_TOKEN"))
        elif model_id.startswith("azure"):
            return bool(os.environ.get("AZURE_OPENAI_API_KEY"))
        elif "gpt" in model_id or "openai" in model_id.lower():
            return bool(os.environ.get("OPENAI_API_KEY"))
        return True
    
    async def list_models(
        self,
        provider: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> List[ModelInfo]:
        """List available models, optionally filtered."""
        models: List[ModelInfo] = []
        
        if HAS_MODEL_PROBE:
            try:
                discovered = await asyncio.to_thread(discover_all_models, False)
                providers = discovered.get("providers", {})
                for name, info in providers.items():
                    if provider and provider != name:
                        continue
                    for m in info.get("available", []) or []:
                        models.append(ModelInfo(
                            id=f"{name}:{m}" if ":" not in m else m,
                            name=m,
                            provider=name,
                            capabilities=[],
                            cost_tier="unknown",
                            available=True,
                        ))
            except Exception:
                pass
        
        # Add models from config
        for prov_name, prov_info in self.config.get("providers", {}).items():
            if provider and provider != prov_name:
                continue
            for model in prov_info.get("available", []):
                model_id = model.get("id", "")
                caps = model.get("capabilities", [])
                if capability and capability not in caps:
                    continue
                models.append(ModelInfo(
                    id=model_id,
                    name=model.get("name", model_id),
                    provider=prov_name,
                    capabilities=caps,
                    cost_tier=model.get("cost_tier", "unknown"),
                    context_length=model.get("context_length", 4096),
                ))
        
        return models
    
    def get_optimal_model(
        self,
        task_type: str,
        complexity: int = 5,
        prefer_local: bool = True,
    ) -> str:
        """
        Get optimal model for a task based on availability and requirements.
        
        Args:
            task_type: Type of task (vision, reasoning, code_gen, etc.)
            complexity: Complexity level 1-10 (higher = need better model)
            prefer_local: Whether to prefer local models
            
        Returns:
            Best available model ID for the task
        """
        # Get routing from config or defaults
        routing = self.config.get("routing", {}).get(task_type) or self.TASK_ROUTING.get(task_type)
        
        if not routing:
            routing = self.TASK_ROUTING.get("code_gen", ["gh:openai/gpt-4o-mini"])
        
        candidates = routing.get("preferred", routing) if isinstance(routing, dict) else routing
        
        # For high complexity, prioritize cloud models
        if complexity >= 8 and not prefer_local:
            candidates = [m for m in candidates if not m.startswith("local:")]
        
        # For prefer_local, prioritize local models
        if prefer_local:
            local_first = [m for m in candidates if m.startswith("local:") or m.startswith("ollama:")]
            local_first.extend([m for m in candidates if m not in local_first])
            candidates = local_first
        
        # Return first available (synchronous check for immediate use)
        for model in candidates:
            if model in self._availability_cache and self._availability_cache[model]:
                return model
        
        # Return first candidate if no cache
        return candidates[0] if candidates else "gh:openai/gpt-4o-mini"
    
    async def _get_fallback(self, failed_model: str) -> Optional[str]:
        """Get fallback model when one fails."""
        fallback_chain = self.config.get("fallback", {}).get("chain", [])
        
        if not fallback_chain:
            fallback_chain = ["gh:openai/gpt-4o-mini", "gh:openai/gpt-4o", "local:phi4"]
        
        for model in fallback_chain:
            if model != failed_model and await self.check_availability(model):
                return model
        
        return None
    
    def _is_remote_model(self, model_id: str) -> bool:
        """Check if a model requires remote API calls."""
        return not (model_id.startswith("local:") or model_id.startswith("ollama:"))
    
    def _estimate_tokens(self, prompt: str, response: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: ~4 chars per token
        return (len(prompt) + len(response)) // 4
    
    def _estimate_cost(self, model_id: str, tokens: int) -> float:
        """Estimate cost in USD based on model and tokens."""
        cost_per_million = self.COST_PER_MILLION.get(model_id, 0.0)
        return (tokens / 1_000_000) * cost_per_million
