"""
Hybrid Full-Stack Code Generator (LangChain-based)
===================================================

A multi-agent workflow using LangChain/LangGraph that combines:
- Local NPU models (phi3.5-vision, phi4mini)
- Ollama models (qwen2.5-coder, deepseek-r1)
- GitHub cloud models (GPT-5, O3-mini, GPT-4.1)

Phases:
1. Requirements → Technical Specs
2. System Design  
3. Code Generation
4. Quality Assurance
"""

from .agents import (
    AGENT_REGISTRY,
    AgentConfig,
    AgentTier,
    Phase,
    get_agent_config,
    list_agents_by_phase,
    get_cost_summary,
)
from .workflow import HybridFullStackGenerator
from .runner import run_fullstack_workflow

__all__ = [
    "AGENT_REGISTRY",
    "AgentConfig", 
    "AgentTier",
    "Phase",
    "get_agent_config",
    "list_agents_by_phase",
    "get_cost_summary",
    "HybridFullStackGenerator",
    "run_fullstack_workflow",
]
