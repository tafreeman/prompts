# agentic-workflows-v2

Tier-based multi-model AI workflow orchestration.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)]()
[![Status](https://img.shields.io/badge/status-Eval%20Phase%200%20Complete-blue)]()

## 📋 Implementation Status

| Phase | Status | Details |
|-------|--------|--------|
| **Eval Phase 0** | ✅ Complete | Scoring, hard gates, normalization, profiles, rubrics |

**Current:** Evaluation Phase 0 is complete — hard gates, normalization framework, scoring profiles, workflow-level rubrics.

For active vs legacy module mapping, see [ACTIVE_VS_LEGACY_TOOLING_MAP.md](docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md).

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

## Run The App (API + UI)

Run the full app (FastAPI backend serving the built UI):

```bash
cd agentic-workflows-v2
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010 --app-dir src
```

Open:

- App UI: `http://127.0.0.1:8010`
- Health: `http://127.0.0.1:8010/api/health`

Notes:

- Port `8000` may already be used on some machines. `8010` is a safe default.
- The app serves `ui/dist` via SPA fallback from the backend.

### Frontend dev mode (optional)

For hot-reload UI development:

```bash
# terminal 1
cd agentic-workflows-v2
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8000 --app-dir src

# terminal 2
cd agentic-workflows-v2/ui
npm run dev
```

Vite runs on `http://127.0.0.1:5173` and proxies `/api` + `/ws` to `http://localhost:8000`.

## Workflow Evaluation UI

The UI supports running and scoring workflows in one pass:

1. Select a workflow.
2. Enable evaluation.
3. Choose dataset source (`repository` or `local`).
4. Pick dataset + sample index.
5. Run and monitor live workflow + evaluation events.

API endpoints used by this flow:

- `GET /api/eval/datasets`
- `POST /api/run` (with optional `evaluation` payload)
- `GET /api/runs`, `GET /api/runs/{filename}`
- `GET /api/runs/{run_id}/stream` (SSE)

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

## Tracing (OpenTelemetry / AI Toolkit)

Agentic workflows supports OpenTelemetry tracing for workflow execution, LLM calls, and step-level events. Tracing is **opt-in** and sends spans to an OTLP collector (e.g., AI Toolkit).

### Enable tracing

```bash
# Enable tracing (required)
export AGENTIC_TRACING=1

# Include sensitive content (prompts, outputs, tool args) in spans (optional, off by default)
export AGENTIC_TRACE_SENSITIVE=1
```

### Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `AGENTIC_TRACING` | (unset) | Set to `1` to enable tracing |
| `AGENTIC_TRACE_SENSITIVE` | (unset) | Set to `1` to include prompts/outputs in spans |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP collector endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` | Protocol: `grpc` or `http/protobuf` |

### Install tracing dependencies

Tracing requires the `tracing` optional extra:

```bash
pip install -e ".[tracing]"
```

### What gets traced

- **Workflow-level span**: `workflow.run` with `workflow_name`, `workflow_id`, `run_id`
- **Step-level spans**: `workflow.step` for each step with `step_name`, `step_status`
- **LLM call spans**: Model ID, token counts (`tokens.prompt`, `tokens.completion`)
- **Tool calls**: Tool name, success/failure (args excluded by default)
- **Errors**: Exception type and message on failed spans

### Using with AI Toolkit

AI Toolkit listens on `http://localhost:4317` by default. With tracing enabled, workflow runs will appear in the AI Toolkit trace viewer automatically.

## Documentation

- API Reference: `docs/API_REFERENCE.md`
- Tutorials: `docs/tutorials/`
- Architecture decisions (ADRs): `docs/adr/`
- Active vs Legacy Tooling: `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`
- Examples: `examples/`

## Developer tooling

We enforce formatting and linting via `pre-commit`.

Install and enable locally:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Recommended VS Code extensions: `ms-python.python`, `ms-python.vscode-pylance`, and `njpwerner.autodocstring`.

## Testing

Backend (full suite):

```bash
cd agentic-workflows-v2
python -m pytest tests/ -v
```

Backend (evaluation-specific):

```bash
python -m pytest tests/test_server_evaluation.py tests/test_normalization.py tests/test_scoring_profiles.py tests/test_server_workflow_routes.py -v
```

UI:

```bash
cd agentic-workflows-v2/ui
npm test
npm run build
```
