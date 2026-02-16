# Shared Tools

This directory contains shared utilities for the `agentic-workflows-v2` runtime and `agentic-v2-eval` evaluation framework.

## Modules

- **`agents/benchmarks`**: Standard benchmark definitions (HumanEval, MBPP, etc.).
- **`core/`**: Configuration, logging, and error handling primitives.
- **`llm/`**: Unified LLM client abstraction supporting multiple providers (OpenAI, Anthropic, etc.).
- **`windows_ai_bridge/`**: Integration for local Windows AI models (Phi Silica).

## Usage

These tools are installed as an editable package (`pip install -e .`) and imported by the main agentic packages.
