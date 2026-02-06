# agentic-workflows-v2

Tier-based multi-model AI workflow orchestration.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Status](https://img.shields.io/badge/status-Phase%202-yellow)]()

## 📋 Implementation Status

| Phase | Status | Details |
|-------|--------|---------|
| **Phase 1** | ✅ Complete | [IMPLEMENTATION_PLAN_V1_COMPLETE.md](docs/IMPLEMENTATION_PLAN_V1_COMPLETE.md) |
| **Phase 2** | ✅ Complete (2D) / 🚧 Polish | [IMPLEMENTATION_PLAN_V2.md](docs/IMPLEMENTATION_PLAN_V2.md) |

**Current:** Phase 2D tools + memory/context improvements are implemented. See `docs/` for details.

## Installation

```bash
pip install -e .
```

## Quick Start

### CLI

After installation, you can use the `agentic` CLI:

```bash
agentic list agents
agentic list tools
agentic orchestrate "Review the code in src/main.py" --verbose
```

### Python

Run a built-in agent directly:

```python
import asyncio

from agentic_v2 import CodeGenerationInput, CoderAgent


async def main() -> None:
    agent = CoderAgent()
    out = await agent.run(
        CodeGenerationInput(
            description="Write a small Python function that returns the string 'hello'.",
            language="python",
        )
    )
    print(out.code)


asyncio.run(main())
```

## Features

- **Tier-based routing**: Route tasks to appropriate model sizes
- **Smart fallback**: Automatic retry with different models
- **Pydantic contracts**: Type-safe inputs/outputs
- **Async-first**: Built for concurrent execution
- **Token-aware memory**: `ConversationMemory` trims to a message + token budget
- **Persistent memory tools**: File-backed CRUD via `AGENTIC_MEMORY_PATH`

### Persistent memory location

If you want the built-in persistent memory tools to write to a specific file, set:

- `AGENTIC_MEMORY_PATH` (e.g., `C:\\temp\\agentic_memory.json`)

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
