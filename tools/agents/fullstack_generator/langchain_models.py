"""
LangChain Integration for Hybrid Full-Stack Generator
======================================================

Provides LangChain-compatible model wrappers that integrate with
our existing LLMClient for local, Ollama, and GitHub models.

LangChain is optional - if not installed, a simpler implementation is used.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Iterator
from dataclasses import dataclass

# Track LangChain availability
LANGCHAIN_AVAILABLE = False
BaseLLM = None  # Will be set if LangChain is available

def ensure_langchain() -> bool:
    """Ensure LangChain packages are installed. Returns True if available."""
    global LANGCHAIN_AVAILABLE, BaseLLM
    try:
        import langchain
        import langchain_core
        from langchain_core.language_models.llms import BaseLLM as _BaseLLM
        BaseLLM = _BaseLLM
        LANGCHAIN_AVAILABLE = True
        return True
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        return False


def install_langchain() -> bool:
    """Install LangChain packages."""
    print("[LangChain] Installing required packages...")
    import subprocess
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "langchain>=0.3.0", 
            "langchain-community>=0.3.0",
            "langchain-core>=0.3.0",
            "langgraph>=0.2.0",
            "-q"
        ])
        return ensure_langchain()
    except Exception as e:
        print(f"[LangChain] Installation failed: {e}")
        return False


# Check availability at import (don't auto-install)
ensure_langchain()

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parents[3]))
from tools.llm.llm_client import LLMClient


@dataclass
class ModelInfo:
    """Information about a model."""
    model_id: str
    provider: str  # local, ollama, gh, aitk
    is_local: bool
    is_free: bool
    supports_vision: bool = False
    
    @classmethod
    def from_model_string(cls, model: str) -> "ModelInfo":
        """Parse model string to ModelInfo."""
        if model.startswith("local:"):
            return cls(
                model_id=model,
                provider="local",
                is_local=True,
                is_free=True,
                supports_vision="vision" in model.lower()
            )
        elif model.startswith("ollama:"):
            return cls(
                model_id=model,
                provider="ollama", 
                is_local=True,
                is_free=True
            )
        elif model.startswith("gh:"):
            return cls(
                model_id=model,
                provider="github",
                is_local=False,
                is_free=False  # Rate limited but free tier available
            )
        elif model.startswith("aitk:"):
            return cls(
                model_id=model,
                provider="aitk",
                is_local=True,
                is_free=True
            )
        else:
            return cls(
                model_id=model,
                provider="unknown",
                is_local=False,
                is_free=False
            )


class HybridLLMBase:
    """
    Base class for hybrid LLM - works without LangChain.
    
    Supports:
    - local:* (ONNX NPU models)
    - ollama:* (Local Ollama models)
    - gh:* (GitHub Models API)
    - aitk:* (AI Toolkit models)
    """
    
    def __init__(
        self,
        model: str = "local:phi4mini",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        fallback_model: Optional[str] = None,
        **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.fallback_model = fallback_model
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        info = ModelInfo.from_model_string(self.model)
        return f"hybrid-{info.provider}"
    
    def invoke(self, prompt: str, system_instruction: str = None, **kwargs) -> str:
        """Execute the LLM call (LangChain-style interface)."""
        return self._call(prompt, system_instruction=system_instruction, **kwargs)
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> str:
        """Execute the LLM call."""
        system_instruction = kwargs.get("system_instruction")
        
        try:
            response = LLMClient.generate_text(
                model_name=self.model,
                prompt=prompt,
                system_instruction=system_instruction,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # Check for errors and try fallback
            if response.startswith("Error:") or response.startswith("gh models error:"):
                if self.fallback_model:
                    print(f"  [Fallback] {self.model} failed, trying {self.fallback_model}")
                    response = LLMClient.generate_text(
                        model_name=self.fallback_model,
                        prompt=prompt,
                        system_instruction=system_instruction,
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                    )
            
            return response
            
        except Exception as e:
            if self.fallback_model:
                print(f"  [Fallback] {self.model} error: {e}, trying {self.fallback_model}")
                return LLMClient.generate_text(
                    model_name=self.fallback_model,
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
            raise


# Create LangChain-compatible version if available
if LANGCHAIN_AVAILABLE:
    from langchain_core.language_models.llms import BaseLLM as LangChainBaseLLM
    from langchain_core.callbacks.manager import CallbackManagerForLLMRun
    from langchain_core.outputs import Generation, LLMResult
    
    class HybridLLM(LangChainBaseLLM, HybridLLMBase):
        """LangChain-compatible HybridLLM."""
        
        model: str = "local:phi4mini"
        temperature: float = 0.7
        max_tokens: int = 4096
        fallback_model: Optional[str] = None
        
        class Config:
            extra = "allow"
        
        @property
        def _llm_type(self) -> str:
            return HybridLLMBase._llm_type.fget(self)
        
        @property
        def _identifying_params(self) -> Dict[str, Any]:
            return {
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
        
        def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> str:
            return HybridLLMBase._call(self, prompt, stop, run_manager, **kwargs)
        
        def _generate(
            self,
            prompts: List[str],
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
        ) -> LLMResult:
            """Generate for multiple prompts."""
            generations = []
            for prompt in prompts:
                text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
                generations.append([Generation(text=text)])
            return LLMResult(generations=generations)
else:
    # Use base class without LangChain
    HybridLLM = HybridLLMBase


class LocalNPUModel(HybridLLM):
    """LangChain wrapper for local ONNX/NPU models."""
    
    def __init__(self, model_name: str = "phi4mini", **kwargs):
        if not model_name.startswith("local:"):
            model_name = f"local:{model_name}"
        super().__init__(model=model_name, **kwargs)


class OllamaModel(HybridLLM):
    """LangChain wrapper for Ollama models."""
    
    def __init__(self, model_name: str = "qwen2.5-coder:14b", **kwargs):
        if not model_name.startswith("ollama:"):
            model_name = f"ollama:{model_name}"
        super().__init__(model=model_name, **kwargs)


class GitHubModel(HybridLLM):
    """LangChain wrapper for GitHub Models API."""
    
    def __init__(self, model_name: str = "openai/gpt-4o-mini", **kwargs):
        if not model_name.startswith("gh:"):
            model_name = f"gh:{model_name}"
        super().__init__(model=model_name, **kwargs)


class AIToolkitModel(HybridLLM):
    """LangChain wrapper for AI Toolkit models."""
    
    def __init__(self, model_name: str = "phi-4-mini-instruct", **kwargs):
        if not model_name.startswith("aitk:"):
            model_name = f"aitk:{model_name}"
        super().__init__(model=model_name, **kwargs)


def create_llm_from_config(
    model: str,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    fallback_model: Optional[str] = None,
) -> HybridLLM:
    """
    Create appropriate LLM instance from model string.
    
    Args:
        model: Model identifier (e.g., "local:phi4", "gh:openai/gpt-5-mini")
        temperature: Sampling temperature
        max_tokens: Max tokens to generate
        fallback_model: Fallback model if primary fails
    
    Returns:
        HybridLLM instance
    """
    return HybridLLM(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        fallback_model=fallback_model,
    )


def get_model_for_tier(tier: str) -> str:
    """Get recommended model for a cost tier."""
    tier_models = {
        "local_npu": "local:phi4mini",
        "local_ollama": "ollama:qwen2.5-coder:14b",
        "cloud_fast": "gh:openai/gpt-4.1-mini",
        "cloud_std": "gh:openai/gpt-4.1",
        "cloud_premium": "gh:openai/gpt-5",
    }
    return tier_models.get(tier, "local:phi4mini")
