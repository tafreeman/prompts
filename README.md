# Multi-Agent Workflow Repository

This repository contains the `agentic-workflows-v2` runtime and `agentic-v2-eval` evaluation framework for building and testing multi-agent systems.

## Components

### `agentic-workflows-v2/`
The core multi-agent workflow runtime, providing:
- **Server:** FastAPI-based orchestration server.
- **Engine:** DAG-based execution engine.
- **Workflows:** YAML-defined workflow definitions.
- **Agents:** Built-in agent implementations.

### `agentic-v2-eval/`
The evaluation framework for agentic workflows, providing:
- **Datasets:** Benchmark dataset integration.
- **Scoring:** Rubric-based evaluation logic.
- **Runners:** Evaluation runners.

### `tools/`
Shared utilities required by the runtime and evaluation framework:
- **`tools/llm/`**: LLM client abstraction.
- **`tools/core/`**: Core configuration and error handling.
- **`tools/agents/benchmarks/`**: Benchmark dataset definitions.

## Getting Started

Refer to `agentic-workflows-v2/README.md` for installation and usage instructions.
