# CLAUDE.md

## Environment Setup
Before doing anything else, run a full environment pre-flight check: 1) Detect the current OS and shell (PowerShell vs Bash vs Zsh), 2) Check if a Python venv exists and has all requirements installed — if not, create it and install dependencies, 3) Check if node_modules exists and matches package.json — if not, run install, 4) Scan for .env files and verify required environment variables are set (flag any missing ones), 5) Check if any required ports (3000, 8000, 8080) are already in use and report conflicts, 6) Verify git status is clean and report current branch. Output a concise status dashboard, then tell me we're ready to work.

## Shell Environment
- This project is developed on Windows/PowerShell. Do NOT use bash-specific syntax (e.g., `kill`, `lsof`). Use PowerShell equivalents (`Stop-Process`, `Get-NetTCPConnection`).

## Verification
- After making fixes, always verify they work by running the relevant code or tests. Do not wait for the user to ask 'did you even check it?'
- When user asks for a file path or simple answer, give the direct answer first before showing code.

## Repository Overview
**Repo:** `tafreeman/prompts` — A monorepo containing a multi-agent workflow runtime (`agentic-workflows-v2`), an evaluation framework (`agentic-v2-eval`), and shared utilities (`tools/`). Each subdirectory is an independent Python package.

**Mission:** Produce production-grade code, rigorous research, and reproducible evaluation artifacts that advance the state of the art in agentic AI.

## Code Quality Standards (Non-Negotiable)
1. **Immutability First:** Always create new objects. Never mutate existing ones. Use `@dataclass(frozen=True)`, `NamedTuple`, or `tuple`.
2. **Type Everything:** Full type annotations on all function signatures. No bare `Any` unless wrapping external untyped APIs. Use `Protocol` for duck-typed interfaces.
3. **Small Units:** Functions < 50 lines. Files < 800 lines (target 200–400). One class/module per file. Organize by feature/domain.
4. **Error Handling:** Never swallow exceptions. Use specific exception types with contextual messages. Validate at system boundaries. Fail fast.
5. **Formatting:** `black` for code, `isort` for imports, `ruff` for linting.
6. **Testing:** At least one test per public function (happy path + error path). No test interdependencies.

## Architecture

### Package Layout
```
agentic-workflows-v2/     # Main runtime (Python 3.11+, hatchling)
  agentic_v2/
    cli/                  # Typer CLI entry point (`agentic` command)
    langchain/            # PRIMARY execution engine (LangChain + LangGraph)
    engine/               # Native DAG executor (Kahn's algorithm)
    agents/               # Built-in agents: Coder, Architect, Reviewer
    models/               # LLM tier routing (smart_router.py)
    server/               # FastAPI app + WebSocket + SSE streaming
    workflows/            # YAML loader, runner, definitions/
    contracts/            # Pydantic I/O models
    tools/                # In-process memory tools
    storage/              # Persistent run logs (JSON replay)
  tests/                  # pytest-asyncio (asyncio_mode = "auto")
  ui/                     # React 19 + Vite 6 + React Flow 12
agentic-v2-eval/          # Evaluation framework (Python 3.10+)
  src/agentic_v2_eval/    # Scorer, rubrics, runners, reporters
tools/                    # Shared utilities (prompts-tools)
  llm/                    # LLMClient abstraction (multi-backend)
  agents/                 # Benchmark definitions
  core/                   # Config + error handling
```

### Key Architectural Points
- **Execution engine:** `langchain/` wraps LangGraph state machines. `engine/` is an independent native DAG executor. Both are active.
- **LLM routing:** `models/smart_router.py` dispatches to backends based on tier and capability.
- **Workflows:** Declarative YAML under `workflows/definitions/`. Steps reference agents by tier name.
- **Contracts:** Pydantic models in `contracts/` define all I/O. **Additive-only changes** — never break existing schemas.

## Research Standards
- **Source Governance:** 
  - **Tier A (Always allowed):** Official vendor docs, Peer-reviewed papers (NeurIPS, ICML, etc.), arXiv (known groups).
  - **Tier B (Conditional):** High-quality engineering blogs, Stack Overflow (high votes).
  - **Tier C (Blocked):** Unverified blogs, marketing materials.
- **Citations:** Every research claim must include inline citations with valid URLs: `[Claim text] (Source: Title, Publisher, Date — URL)`.
- **Critical-claim rule:** Architectural decisions require >= 2 independent Tier A sources.

## Evaluation Framework
- **Scorer:** YAML rubrics → weighted scores across dimensions (Completeness, Correctness, Quality, Specificity, Alignment).
- **Runners:** BatchRunner, StreamingRunner, AsyncStreamingRunner.
- **LLM Judge:** `tools/agents/benchmarks/llm_evaluator.py` — 0.0–10.0 rubric scoring.
- **Confidence Interval Gating:** For research workflows, require `coverage_score >= 0.80`, `source_quality_score >= 0.80`, etc.

## Workflow & Agent Authoring
- **YAML Rules:** Every step MUST have `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`.
- **Tools:** Allowlisted per step. Default DENY for high-risk tools (shell, git, file_delete).
- **Personas:** Defined in `agentic_v2/prompts/*.md`. Must define Expertise, Boundaries, Critical rules, Output format.

## Commands

### Backend (agentic-workflows-v2)
```bash
# Install
pip install -e ".[dev,server,langchain]"
# Run full test suite
python -m pytest tests/ -v
# Lint / format
pre-commit run --all-files
# Hot-reload dev (backend + frontend)
bash dev.sh [backend_port] [frontend_port]
# Production serve
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010 --app-dir src
```

### CLI
```bash
agentic list workflows|agents|tools
agentic run <workflow> --input <file.json>
agentic validate <workflow>
agentic serve
```

### Evaluation
```bash
cd agentic-v2-eval && pip install -e ".[dev]"
python -m agentic_v2_eval evaluate results.json
python -m agentic_v2_eval report results.json --format html
```

## Anti-Patterns — Never Do These
- **Never mutate state in place.** Always return new objects.
- **Never use bare `except:`.** Catch specific exceptions.
- **Never hardcode secrets.** Use `.env`.
- **Never produce TODOs in generated code.** All files must be complete.
- **Never add web servers or scaffolding unless explicitly requested.**
- **Never use sys.path hacks.** Use `from tools...` imports.
- **Never break existing contracts/schemas.** Additive-only.
- **Never skip the eval flywheel.** Define rubrics before building, run evals after.
