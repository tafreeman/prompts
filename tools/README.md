# Shared Tools

This directory contains shared utilities for the `agentic-workflows-v2` runtime and `agentic-v2-eval` evaluation framework.

## Modules

- **`agents/benchmarks/`**: Standard benchmark definitions, task loader, evaluator, and registry (HumanEval, MBPP, SWE-bench, etc.).
- **`core/`**: Configuration (`ModelConfig`, `PathConfig`), error codes, and shared error handling primitives.
- **`llm/`**: Unified `LLMClient` static facade supporting multiple providers:
  - Local: ONNX models, Ollama, Windows AI (Phi Silica via `llm/windows_ai_bridge/`)
  - Remote: OpenAI, Anthropic Claude, Google Gemini, GitHub Models, Azure OpenAI, Azure Foundry
- **`research/`**: Research utilities and helpers.
- **`validate_subagents.py`**: Subagent definition validator.
- **`windows_ai_bridge/`**: C# build output for the Phi Silica NPU bridge (source code is in `llm/windows_ai_bridge/`).

## Usage

These tools are installed as an editable package (`pip install -e .`) and imported by the main agentic packages.
