# Multi-Agent Workflow Repository

Monorepo for agentic workflow runtime, evaluation tooling, and shared LLM utilities.

## Components

### `agentic-workflows-v2/`
Core runtime for multi-agent orchestration:
- Typed workflow engine and DAG execution
- Workflow definitions and model-tier routing
- FastAPI backend and React UI
- Evaluation-aware run APIs and live streaming

Primary docs:
- `agentic-workflows-v2/README.md`
- `agentic-workflows-v2/docs/README.md`

### `agentic-v2-eval/`
Evaluation framework package for benchmark and rubric scoring:
- Dataset adapters and evaluators
- Batch/stream runners
- Reporters and scoring utilities

Primary docs:
- `agentic-v2-eval/README.md`

### `tools/`
Shared utilities used by runtime and eval packages:
- `tools/llm/`: provider adapters, probes, ranking, model tooling
- `tools/core/`: config, errors, caching, helpers
- `tools/agents/benchmarks/`: benchmark pipelines and dataset loading

## Documentation Coverage

This repo follows docs-as-code patterns with:
- README and setup docs per major package
- Contributor guidance and community health files
- Architecture/workflow/development references in package docs
- Checkable path references via docs validation scripts

## Quick Start

For runtime development:

```bash
cd agentic-workflows-v2
pip install -e ".[dev,server,langchain]"
agentic list workflows
```

For evaluation package development:

```bash
cd agentic-v2-eval
pip install -e ".[dev]"
```

## Contributing

- Runtime/package changes: `agentic-workflows-v2/CONTRIBUTING.md`
- Root docs and subagent registry: `docs/README.md`, `docs/subagents.yml`
