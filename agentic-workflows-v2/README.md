# agentic-workflows-v2

Tier-based multi-model AI workflow orchestration.

[![Tests](https://img.shields.io/badge/tests-305%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Status](https://img.shields.io/badge/status-Phase%202-yellow)]()

## 📋 Implementation Status

| Phase | Status | Details |
|-------|--------|---------|
| **Phase 1** | ✅ Complete | [IMPLEMENTATION_PLAN_V1_COMPLETE.md](docs/IMPLEMENTATION_PLAN_V1_COMPLETE.md) |
| **Phase 2** | 🚧 In Progress | [IMPLEMENTATION_PLAN_V2.md](docs/IMPLEMENTATION_PLAN_V2.md) |

**Current:** 305 tests passing, 4 agents, 2 workflows, 13 tools

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from agentic_v2 import Orchestrator, Task

# Create orchestrator
orch = Orchestrator()

# Define a task
task = Task(
    name="analyze_code",
    tier=2,  # Medium complexity
    input={"code": "def hello(): pass"}
)

# Run
result = await orch.run(task)
```

## Features

- **Tier-based routing**: Route tasks to appropriate model sizes
- **Smart fallback**: Automatic retry with different models
- **Pydantic contracts**: Type-safe inputs/outputs
- **Async-first**: Built for concurrent execution

## Documentation

- API Reference: `docs/API_REFERENCE.md`
- Tutorials: `docs/tutorials/`
- Architecture decisions (ADRs): `docs/adr/`
- Examples: `examples/`

To build the API docs locally see `docs/API_REFERENCE.md` for Sphinx/MkDocs instructions.

## Developer tooling

We enforce formatting and linting via `pre-commit`.

Install and enable locally:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Recommended VS Code extensions: `ms-python.python`, `ms-python.vscode-pylance`, and `njpwerner.autodocstring`.
