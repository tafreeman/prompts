# CLAUDE.md

## Environment Setup
Before doing anything else, run a full environment pre-flight check: 1) Detect the current OS and shell (PowerShell vs Bash vs Zsh), 2) Check if a Python venv exists and has all requirements installed — if not, create it and install dependencies, 3) Check if node_modules exists and matches package.json — if not, run install, 4) Scan for .env files and verify required environment variables are set (flag any missing ones), 5) Check if any required ports (3000, 8000, 8080) are already in use and report conflicts, 6) Verify git status is clean and report current branch. Output a concise status dashboard, then tell me we're ready to work.

## Shell Environment

- This project is developed on Windows/PowerShell. Do NOT use bash-specific syntax (e.g., `kill`, `lsof`). Use PowerShell equivalents (`Stop-Process`, `Get-NetTCPConnection`).

## Verification
- After making fixes, always verify they work by running the relevant code or tests. Do not wait for the user to ask 'did you even check it?'
- When user asks for a file path or simple answer, give the direct answer first before showing code.
Add under 

## Repository Overview

A monorepo containing a multi-agent workflow runtime (`agentic-workflows-v2`), an evaluation framework (`agentic-v2-eval`), and shared utilities (`tools/`). Each subdirectory is an independent Python package.

## Commands

### Backend (agentic-workflows-v2)

```bash
# Install (run from agentic-workflows-v2/)
pip install -e ".[dev,server,langchain]"

# Run full test suite
cd agentic-workflows-v2
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_dag.py -v

# Run specific evaluation tests
python -m pytest tests/test_server_evaluation.py tests/test_normalization.py tests/test_scoring_profiles.py -v

# Lint / format (pre-commit enforces black + isort + ruff + mypy + pydocstyle)
pre-commit run --all-files
```

### Frontend (agentic-workflows-v2/ui)

```bash
cd agentic-workflows-v2/ui
npm test          # Vitest unit tests
npm run build     # Production build → ui/dist/
```

### Port Management

- Before starting any server, check if the target port is already in use and handle it gracefully.
- Use the project's standard port (check existing configs) rather than assuming defaults.
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### Running the App

```bash
# Full-stack dev mode (backend + frontend hot-reload) — from agentic-workflows-v2/
bash dev.sh [backend_port] [frontend_port]   # defaults: 8010, 5173

# Production mode (serves built UI from ui/dist/)
cd agentic-workflows-v2
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010 --app-dir src
```

> **Windows note:** Port 8000 is often blocked by an elevated process. Use 8010 or higher. To kill a process by PID: `powershell -Command "Stop-Process -Id <n> -Force"`.


### CLI (after `pip install -e .`)

```bash
agentic list workflows|agents|tools
agentic run <workflow> --input <file.json>
agentic validate <workflow>
agentic serve
```

### Shared Tools (root)

```bash
pip install -e ".[dev]"   # from repo root
```

## Architecture

### Package Layout

```
agentic-workflows-v2/     # Main runtime (Python 3.11+, hatchling)
  agentic_v2/
    cli/                  # Typer CLI entry point (`agentic` command)
    langchain/            # PRIMARY execution engine (LangChain + LangGraph)
    engine/               # Native DAG executor (Kahn's algorithm, expressions)
    agents/               # Built-in agents: Coder, Architect, Reviewer, Orchestrator
    models/               # LLM tier routing (backends, router, smart_router)
    server/               # FastAPI app + WebSocket + routes
    workflows/            # YAML loader, runner, definitions/
    integrations/         # OpenTelemetry tracing (opt-in via AGENTIC_TRACING=1)
    contracts/            # Pydantic I/O models
    tools/                # In-process memory tools
    storage/              # Persistent run storage
  tests/                  # pytest-asyncio (asyncio_mode = "auto")
  ui/                     # React 19 + Vite 6 + React Flow 12 + TanStack Query 5
agentic-v2-eval/          # Evaluation framework (separate package, Python 3.10+)
  src/agentic_v2_eval/    # Datasets, scoring rubrics, runners
tools/                    # Shared utilities (installable as `prompts-tools`)
  llm/                    # LLMClient abstraction (multi-backend)
  agents/                 # Benchmark definitions
  core/                   # Config + error handling
```

### Key Architectural Points

**Execution engine:** The `langchain/` module is the primary runtime (wrapping LangGraph state machines). The `engine/` module contains an independent native DAG executor that uses Kahn's topological sort algorithm. Both are active; `langchain/` is used by the CLI and server.

**LLM routing:** `models/smart_router.py` dispatches to backends (GitHub Models, OpenAI, Azure OpenAI, Gemini, Anthropic, local Phi Silica) based on tier and capability. `LLMClient` in `tools/llm/llm_client.py` is a `@staticmethod`-based facade — call it as `LLMClient.generate_text(model_name, ...)`.

**Workflows:** Defined as YAML files under `agentic_v2/workflows/definitions/`. Each step **must** include an `agent:` field. Loaded via `agentic_v2/langchain/config.py` + `workflows/loader.py`.

**Server:** FastAPI serves `/api/*` routes and falls back to the built React SPA (`ui/dist/`) for all other routes. WebSocket endpoint handles real-time workflow events.

**Test split:** `agentic-workflows-v2/tests/` uses `pyproject.toml` `asyncio_mode = "auto"`. The root `tools/tests/` (if present) uses a root `pytest.ini` with `asyncio_mode = "strict"`.

### Environment Variables

Copy `.env.example` to `.env`. Required keys depend on which LLM backends you use:

| Variable | Provider |
|---|---|
| `GITHUB_TOKEN` | GitHub Models |
| `OPENAI_API_KEY` | OpenAI |
| `AZURE_OPENAI_API_KEY_0` + `AZURE_OPENAI_ENDPOINT_0` | Azure OpenAI |
| `GEMINI_API_KEY` | Google Gemini |
| `ANTHROPIC_API_KEY` | Anthropic |
| `AGENTIC_TRACING=1` | Enable OpenTelemetry tracing |
| `AGENTIC_MEMORY_PATH` | Path for persistent memory tools |

### Code Style

Enforced via pre-commit: **black** (88-char lines), **isort** (black profile), **ruff** (auto-fix), **mypy** (`--ignore-missing-imports`), **pydocstyle** (Google convention), **docformatter** (79-char wrap).
