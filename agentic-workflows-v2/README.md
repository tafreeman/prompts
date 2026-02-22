# Agentic Workflows v2

Tier-based, multi-model workflow orchestration for coding and research tasks.

This package combines:
- A typed Python workflow runtime (`agentic_v2`)
- YAML-defined multi-step workflows (`agentic_v2/workflows/definitions`)
- A CLI (`agentic`)
- A FastAPI backend and React UI for live runs and evaluation

## What You Can Do

- Run workflows from YAML with dependency-aware DAG execution.
- Route steps to different model tiers (`tier0` to `tier3`).
- Execute deterministic tool steps and model-backed agent steps in one graph.
- Stream workflow events over SSE and WebSocket.
- Run workflow-level evaluation with scoring profiles and rubric criteria.

## Repository Map

| Path | Purpose |
| --- | --- |
| `agentic_v2/` | Core runtime package (agents, engine, models, tools, workflows, server) |
| `agentic_v2/workflows/definitions/` | Built-in workflow definitions |
| `docs/` | Tutorials, architecture, API, and operations documentation |
| `examples/` | Minimal runnable examples |
| `tests/` | Backend test suite |
| `ui/` | React + Vite frontend |
| `scripts/` | Dev, evaluation, and docs helper scripts |
| `feature_package/` | Example generated package + handoff artifacts |

For a deeper map, see `docs/REPO_MAP.md`.

## Quick Start

### 1) Install

From this directory:

```bash
pip install -e ".[dev,server,langchain]"
```

Optional extras:

```bash
# OpenTelemetry tracing support
pip install -e ".[tracing]"

# Claude SDK adapters
pip install -e ".[claude]"
```

### 2) Explore CLI

```bash
agentic list workflows
agentic list agents
agentic list tools
agentic validate code_review
agentic run code_review --dry-run
agentic version
```

### 3) Run API + UI (single server path)

```bash
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010
```

Open:
- UI: `http://127.0.0.1:8010`
- Health: `http://127.0.0.1:8010/api/health`
- OpenAPI docs: `http://127.0.0.1:8010/docs`

### 4) Frontend Hot Reload (optional)

```bash
# terminal 1
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8000

# terminal 2
cd ui
npm install
npm run dev
```

Vite serves `http://127.0.0.1:5173` and proxies `/api` and `/ws` to backend.

## Built-In Workflows

Current built-in definitions include:
- `code_review`
- `bug_resolution`
- `deep_research`
- `fullstack_generation`
- `fullstack_generation_bounded_rereview`
- `multi_agent_codegen_e2e`
- `multi_agent_codegen_e2e_single_loop`
- `tdd_codegen_e2e`
- `test_deterministic`
- `plan_implementation` (experimental and legacy-structured)

See `docs/WORKFLOWS.md` for inputs/outputs and guidance.

## API Surfaces

Primary routes:
- `GET /api/health`
- `GET /api/agents`
- `GET /api/workflows`
- `GET /api/workflows/{name}/dag`
- `GET /api/workflows/{name}/capabilities`
- `POST /api/run`
- `GET /api/runs`
- `GET /api/runs/{filename}`
- `GET /api/runs/{run_id}/stream` (SSE)
- `GET /api/eval/datasets`
- `GET /api/workflows/{workflow_name}/preview-dataset-inputs`
- `WS /ws/execution/{run_id}`

## Sub-Agents

This project supports two related sub-agent patterns:
- Workflow-tier agents in YAML (`tier0_parser`, `tier2_reviewer`, etc.).
- Claude SDK sub-agents loaded from Markdown frontmatter definitions.

See `docs/SUBAGENTS.md` for setup and examples.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `AGENTIC_API_KEY` | unset | Enables API key auth for `/api/*` (except health/docs) |
| `AGENTIC_CORS_ORIGINS` | local dev origins | Comma-separated CORS allowlist |
| `AGENTIC_MEMORY_PATH` | unset | File path for persistent memory tools |
| `AGENTIC_TRACING` | unset | Set `1/true/yes` to enable tracing |
| `AGENTIC_TRACE_SENSITIVE` | unset | Include prompts/outputs in spans |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4317` | OTLP collector endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` | `grpc` or `http/protobuf` |
| `OTEL_SERVICE_NAME` | `agentic-workflows-v2` | Service name used in traces |
| `AGENTIC_MODEL_TIER_1` | unset | Force tier 1 model |
| `AGENTIC_MODEL_TIER_2` | unset | Force tier 2 model |
| `AGENTIC_MODEL_TIER_3` | unset | Force tier 3 model |
| `AGENTIC_EXTERNAL_AGENTS_DIR` | unset | Directory of external Markdown agent definitions |

## Development

Quality checks:

```bash
pre-commit run --all-files
python scripts/check_docs_refs.py
```

Backend tests:

```bash
python -m pytest tests -v
python -m pytest --cov=agentic_v2 --cov-report=term-missing --cov-report=xml
```

UI tests:

```bash
cd ui
npm test
npm run test:coverage
```

More details: `docs/DEVELOPMENT.md`.

## Documentation Index

Start here:
- `docs/README.md`
- `docs/ARCHITECTURE.md`
- `docs/WORKFLOWS.md`
- `docs/API_REFERENCE.md`
- `docs/tutorials/getting_started.md`
- `docs/DOCS_BEST_PRACTICES.md`

## Community Health Files

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`
- `.github/ISSUE_TEMPLATE/`
- `.github/PULL_REQUEST_TEMPLATE.md`

## License

MIT. See `LICENSE`.
