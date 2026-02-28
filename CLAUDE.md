# CLAUDE.md

## Environment Setup

Before doing anything else, run a full environment pre-flight check:
1. Detect the current OS and shell (PowerShell vs Bash vs Zsh)
2. Check if a Python venv exists and has all requirements installed — if not, create it and install dependencies
3. Check if `node_modules` exists under `agentic-workflows-v2/ui/` and matches `package.json` — if not, run install
4. Scan for `.env` files and verify required environment variables are set (flag any missing ones; see `.env.example`)
5. Check if any required ports (3000, 8000, 8010) are already in use and report conflicts
6. Verify git status is clean and report current branch

Output a concise status dashboard, then confirm readiness.

## Shell Environment

- This project is developed on Windows/PowerShell. Do NOT use bash-specific syntax (e.g., `kill`, `lsof`). Use PowerShell equivalents (`Stop-Process`, `Get-NetTCPConnection`).

## Verification

- After making fixes, always verify they work by running the relevant code or tests. Do not wait for the user to ask.
- When user asks for a file path or simple answer, give the direct answer first before showing code.

---

## Repository Overview

**Repo:** `tafreeman/prompts`
**Default branch:** `main` (local has `master`)
**Python:** 3.11+ for `agentic-workflows-v2`, 3.10+ for `agentic-v2-eval` and `tools`
**Build systems:** hatchling (agentic-workflows-v2), setuptools (agentic-v2-eval, tools)

A monorepo containing three independent Python packages plus a React frontend:

| Package | Description | Python | Build |
|---------|-------------|--------|-------|
| `agentic-workflows-v2/` | Multi-agent workflow runtime | 3.11+ | hatchling |
| `agentic-v2-eval/` | Evaluation framework | 3.10+ | setuptools |
| `tools/` (prompts-tools) | Shared LLM client, benchmarks, utilities | 3.10+ | setuptools |
| `agentic-workflows-v2/ui/` | React dashboard | Node/TS | Vite 6 |

**Mission:** Produce production-grade code, rigorous research, and reproducible evaluation artifacts that advance the state of the art in agentic AI.

---

## Architecture

### Full Repository Layout

```
prompts/                          # Monorepo root
├── CLAUDE.md                     # This file
├── README.md                     # Project overview
├── pyproject.toml                # Root package (prompts-tools)
├── .env.example                  # Required env vars template
├── .pre-commit-config.yaml       # black, isort, ruff, mypy, pydocstyle
├── .gitignore
│
├── .claude/                      # Claude Code configuration
│   ├── commands/                 # 11 slash commands (plan, tdd, build-fix, etc.)
│   ├── contexts/                 # 3 modes (dev, research, review)
│   ├── rules/                    # Coding style, git, security, testing, ML
│   │   ├── common/              # Language-agnostic rules (7 files)
│   │   └── python/              # Python-specific rules (5 files)
│   └── skills/                   # 8 specialized skills
│
├── .github/
│   ├── agents/                   # 19 GitHub Copilot agent definitions
│   ├── instructions/             # copilot-instructions.md
│   └── workflows/                # 11 CI/CD workflows
│
├── agentic-workflows-v2/         # ── Main Runtime ──────────────────
│   ├── pyproject.toml            # hatchling, Python 3.11+
│   ├── dev.sh                    # Hot-reload dev server
│   ├── manifest.json             # Package manifest
│   ├── agentic_v2/               # Source package (~20,900 lines)
│   │   ├── __init__.py           # Public API exports
│   │   ├── agents/               # Built-in agents + implementations
│   │   │   ├── base.py           # BaseAgent, AgentConfig, AgentState
│   │   │   ├── coder.py          # CoderAgent
│   │   │   ├── architect.py      # ArchitectAgent
│   │   │   ├── reviewer.py       # ReviewerAgent
│   │   │   ├── orchestrator.py   # OrchestratorAgent
│   │   │   ├── capabilities.py   # Capability system (mixins)
│   │   │   └── implementations/  # Claude SDK agent, agent loader
│   │   ├── cli/                  # Typer CLI (`agentic` command)
│   │   ├── config/               # Runtime config + defaults (YAML)
│   │   │   └── defaults/         # agents.yaml, evaluation.yaml, models.yaml
│   │   ├── contracts/            # Pydantic I/O models (messages, schemas)
│   │   ├── engine/               # Native DAG executor
│   │   │   ├── dag.py            # DAG data structure
│   │   │   ├── dag_executor.py   # Kahn's algorithm executor
│   │   │   ├── executor.py       # Step executor
│   │   │   ├── runtime.py        # Execution runtime
│   │   │   ├── expressions.py    # Template expressions
│   │   │   ├── pipeline.py       # Pipeline orchestration
│   │   │   ├── context.py        # Execution context
│   │   │   ├── step.py / step_state.py
│   │   │   └── patterns/         # Execution patterns
│   │   ├── evaluation/           # Normalization utilities
│   │   ├── integrations/         # LangChain, OTEL, tracing adapters
│   │   ├── langchain/            # LangGraph execution engine
│   │   │   ├── graph.py          # LangGraph state machine
│   │   │   ├── runner.py         # LangChain workflow runner
│   │   │   ├── state.py          # Graph state management
│   │   │   ├── agents.py         # LangChain agent wrappers
│   │   │   ├── config.py         # LangChain configuration
│   │   │   ├── expressions.py    # Expression evaluation
│   │   │   ├── models.py         # LangChain model adapters
│   │   │   └── tools.py          # Tool bindings
│   │   ├── models/               # LLM tier routing
│   │   │   ├── smart_router.py   # Tier-based model dispatch
│   │   │   ├── router.py         # Router logic
│   │   │   ├── client.py         # Model client
│   │   │   ├── backends.py       # Backend configurations
│   │   │   ├── llm.py            # LLM abstraction
│   │   │   └── model_stats.py    # Usage statistics
│   │   ├── prompts/              # 23 agent persona definitions (.md)
│   │   ├── server/               # FastAPI app
│   │   │   ├── app.py            # Main FastAPI application
│   │   │   ├── websocket.py      # WebSocket streaming
│   │   │   ├── auth.py           # Authentication
│   │   │   ├── routes/           # API routes (agents, health, workflows)
│   │   │   ├── evaluation.py     # Evaluation endpoints
│   │   │   ├── evaluation_scoring.py
│   │   │   ├── multidimensional_scoring.py
│   │   │   ├── scoring_profiles.py
│   │   │   ├── normalization.py
│   │   │   ├── judge.py          # LLM judge endpoint
│   │   │   ├── datasets.py       # Dataset management
│   │   │   └── models.py         # API models
│   │   ├── tools/                # In-process tool system
│   │   │   ├── registry.py       # Tool registry
│   │   │   └── builtin/          # 12 built-in tools
│   │   │       ├── file_ops.py, git_ops.py, shell_ops.py
│   │   │       ├── code_analysis.py, code_execution.py
│   │   │       ├── search_ops.py, http_ops.py
│   │   │       ├── memory_ops.py, context_ops.py
│   │   │       ├── build_ops.py, transform.py
│   │   │       └── ...
│   │   ├── utils/                # Path safety utilities
│   │   └── workflows/            # Workflow system
│   │       ├── loader.py         # YAML workflow loader
│   │       ├── runner.py         # Workflow runner
│   │       ├── run_logger.py     # JSON replay logs
│   │       ├── artifact_extractor.py
│   │       └── definitions/      # 10 YAML workflow definitions
│   ├── tests/                    # 37 test files (pytest-asyncio)
│   ├── ui/                       # React 19 dashboard
│   │   ├── package.json          # React 19, Vite 6, React Flow 12
│   │   └── src/
│   │       ├── components/       # UI components (dag, layout, live, runs)
│   │       ├── pages/            # 7 pages (Dashboard, Workflows, Runs, etc.)
│   │       ├── hooks/            # React hooks (useRuns, useWorkflows, etc.)
│   │       ├── api/              # API client, types, WebSocket
│   │       └── styles/
│   ├── docs/
│   ├── examples/
│   ├── fixtures/
│   └── scripts/
│
├── agentic-v2-eval/              # ── Evaluation Framework ──────────
│   ├── pyproject.toml            # setuptools, Python 3.10+
│   └── src/agentic_v2_eval/
│       ├── __main__.py           # CLI entry point
│       ├── scorer.py             # Weighted rubric scorer
│       ├── interfaces.py         # Core interfaces
│       ├── datasets.py           # Dataset bridge
│       ├── adapters/             # LLM client adapter
│       ├── evaluators/           # 5 evaluators (base, llm, pattern, quality, standard)
│       ├── metrics/              # Accuracy, performance, quality metrics
│       ├── reporters/            # HTML, JSON, Markdown reporters
│       ├── rubrics/              # 8 YAML rubric definitions
│       ├── runners/              # Batch + streaming runners
│       └── sandbox/              # Execution sandboxing
│
├── tools/                        # ── Shared Utilities ──────────────
│   ├── __init__.py               # Package exports + backwards-compat aliases
│   ├── validate_subagents.py     # YAML schema validator
│   ├── agents/benchmarks/        # Benchmark system (~4,100 lines)
│   │   ├── datasets.py           # 10+ benchmark definitions (SWE-bench, HumanEval, etc.)
│   │   ├── registry.py           # Configuration presets
│   │   ├── loader.py             # On-demand data fetching
│   │   ├── runner.py             # Interactive CLI
│   │   ├── evaluation_pipeline.py
│   │   ├── workflow_pipeline.py
│   │   └── llm_evaluator.py      # LLM rubric scoring (0.0–10.0)
│   ├── core/                     # Configuration, errors, caching (~1,600 lines)
│   │   ├── config.py             # Model tier config
│   │   ├── errors.py             # Error classification + codes
│   │   ├── cache.py / response_cache.py  # LLM response caching
│   │   ├── tool_init.py          # Tool initialization framework
│   │   └── ...
│   ├── llm/                      # Multi-provider LLM client (~5,300 lines)
│   │   ├── llm_client.py         # Unified LLM abstraction
│   │   ├── provider_adapters.py  # 8+ provider implementations
│   │   ├── model_probe.py        # Model discovery + capability detection
│   │   ├── local_model.py        # ONNX Runtime inference
│   │   ├── model_bakeoff.py      # Model comparison framework
│   │   ├── model_inventory.py    # Availability + limits tracking
│   │   ├── rank_models.py        # Tier-based ranking
│   │   └── windows_ai_bridge/    # C# bridge for Phi Silica
│   └── research/
│       └── build_library.py      # Research artifact consolidation
│
├── research/                     # Research docs + ADRs
│   ├── SYSTEM_INSTRUCTIONS.md
│   ├── adr07.md
│   ├── library/                  # Consolidated research artifacts
│   └── subagents/                # Subagent research
│
├── reports/                      # Generated reports
│   ├── deep-research/
│   └── model-bakeoff/
│
├── runs/                         # Workflow run logs (JSON replay)
│   └── _inputs/                  # Input fixtures
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   ├── CODING_STANDARDS.md
│   ├── Architecture-Analysis.pdf
│   ├── subagents.yml
│   └── pr-checklists/
│
├── scripts/
│   └── setup_env_loading.ps1     # PowerShell env setup
│
├── tests/e2e/                    # Root-level E2E tests
│   └── test_subagent_smoke.py
│
└── .vscode/                      # VS Code configuration
    ├── settings.json
    ├── launch.json
    ├── tasks.json
    ├── mcp.json
    └── extensions.json
```

### Key Architectural Points

- **Dual execution engine:** `langchain/` wraps LangGraph state machines; `engine/` is an independent native DAG executor (Kahn's algorithm). Both are active and maintained.
- **LLM routing:** `models/smart_router.py` dispatches to backends based on tier and capability. Supports 8+ providers (OpenAI, Anthropic, Google Gemini, Azure OpenAI, Azure Foundry, GitHub Models, Ollama, local ONNX).
- **Workflows:** Declarative YAML under `workflows/definitions/` (10 workflows). Steps reference agents by tier name.
- **Contracts:** Pydantic models in `contracts/` define all I/O. **Additive-only changes** — never break existing schemas.
- **Agent personas:** 23 markdown persona definitions in `prompts/` (coder, architect, reviewer, researcher, planner, etc.).
- **Built-in tools:** 12 tool modules in `tools/builtin/` (file ops, git, shell, code analysis, memory, HTTP, etc.). Default DENY for high-risk tools.
- **Server:** FastAPI with WebSocket/SSE streaming, evaluation endpoints, and LLM judge.
- **UI:** React 19 + Vite 6 + React Flow 12 + TanStack Query + Tailwind CSS. 7 pages (Dashboard, Workflows, Runs, Live, Datasets, Evaluations, Workflow Detail).

### Workflow Definitions

Located in `agentic-workflows-v2/agentic_v2/workflows/definitions/`:
- `bug_resolution.yaml` — Bug investigation and fix
- `code_review.yaml` — Multi-agent code review
- `deep_research.yaml` — Deep research pipeline
- `fullstack_generation.yaml` — Full-stack code generation
- `fullstack_generation_bounded_rereview.yaml` — Bounded re-review variant
- `multi_agent_codegen_e2e.yaml` — End-to-end multi-agent codegen
- `multi_agent_codegen_e2e_single_loop.yaml` — Single-loop variant
- `plan_implementation.yaml` — Plan + implement workflow
- `tdd_codegen_e2e.yaml` — TDD-driven code generation
- `test_deterministic.yaml` — Deterministic test workflow

---

## Code Quality Standards (Non-Negotiable)

1. **Immutability First:** Always create new objects. Never mutate existing ones. Use `@dataclass(frozen=True)`, `NamedTuple`, or `tuple`.
2. **Type Everything:** Full type annotations on all function signatures. No bare `Any` unless wrapping external untyped APIs. Use `Protocol` for duck-typed interfaces.
3. **Small Units:** Functions < 50 lines. Files < 800 lines (target 200–400). One class/module per file. Organize by feature/domain.
4. **Error Handling:** Never swallow exceptions. Use specific exception types with contextual messages. Validate at system boundaries. Fail fast.
5. **Formatting:** `black` (line-length 88) for code, `isort` (profile=black) for imports, `ruff` for linting, `mypy --strict` for types, `pydocstyle` (google convention) for docstrings.
6. **Testing:** At least one test per public function (happy path + error path). No test interdependencies. Minimum 80% coverage.

---

## Commands

### Backend — agentic-workflows-v2

```bash
# Install (from agentic-workflows-v2/)
pip install -e ".[dev,server,langchain]"

# Run full test suite
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ -q --cov=agentic_v2 --cov-report=term-missing

# Lint / format (from repo root)
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

### Frontend — UI (from agentic-workflows-v2/ui/)

```bash
npm install
npm run dev          # Vite dev server
npm run build        # TypeScript check + Vite build
npm run test         # Vitest
npm run test:coverage
```

### Evaluation Framework (from agentic-v2-eval/)

```bash
pip install -e ".[dev]"
python -m agentic_v2_eval evaluate results.json
python -m agentic_v2_eval report results.json --format html
```

### Shared Tools (from repo root)

```bash
pip install -e ".[dev]"
# Used as: from tools.llm import LLMClient
# Used as: from tools.core.errors import ErrorCode
```

---

## CI/CD Workflows

Located in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | push/PR to main, agenticv2 | Lint (pre-commit) + test (pytest + coverage) + docs check |
| `eval-package-ci.yml` | — | Eval package CI |
| `deploy.yml` | — | Deployment |
| `docs-verify.yml` | — | Documentation verification |
| `prompt-validation.yml` | — | Prompt YAML validation |
| `prompt-quality-gate.yml` | — | Prompt quality checks |
| `validate-prompts.yml` | — | Prompt schema validation |
| `manifest-temperature-check.yml` | — | Manifest validation |
| `performance-benchmark.yml` | — | Performance benchmarks |
| `dependency-review.yml` | — | Dependency security review |
| `eval-poc.yml` | — | Eval proof-of-concept |

---

## Environment Variables

See `.env.example` for the full template. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Optional | GitHub Models API |
| `OPENAI_API_KEY` | Optional | OpenAI API |
| `ANTHROPIC_API_KEY` | Optional | Anthropic Claude API |
| `GEMINI_API_KEY` | Optional | Google Gemini API |
| `AZURE_OPENAI_API_KEY_0` | Optional | Azure OpenAI (supports _0 through _n for failover) |
| `AZURE_OPENAI_ENDPOINT_0` | Optional | Azure OpenAI endpoint |
| `LOCAL_MODEL_PATH` | Optional | Local ONNX models (auto-detected from `~/.cache/aigallery`) |
| `AGENTIC_TRACING` | Optional | Enable OpenTelemetry tracing (set to 1) |
| `AGENTIC_TRACE_SENSITIVE` | Optional | Include prompts/outputs in traces |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Optional | OTLP endpoint (default: localhost:4317) |

At least one LLM provider key is needed for runtime operation.

---

## Testing Infrastructure

### Test Organization

| Location | Count | Framework | Scope |
|----------|-------|-----------|-------|
| `agentic-workflows-v2/tests/` | 37 files | pytest-asyncio (auto mode) | Unit + integration |
| `agentic-v2-eval/tests/` | 10 files | pytest + pytest-asyncio | Evaluator tests |
| `tests/e2e/` | 1 file | pytest | E2E smoke tests |
| `agentic-workflows-v2/ui/src/__tests__/` | — | Vitest + React Testing Library | Frontend |

### Running Tests

```bash
# All backend tests
cd agentic-workflows-v2 && python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_dag_executor.py -v

# With coverage
python -m pytest tests/ --cov=agentic_v2 --cov-report=term-missing --cov-fail-under=80

# Eval tests
cd agentic-v2-eval && python -m pytest tests/ -v

# Frontend tests
cd agentic-workflows-v2/ui && npm run test
```

---

## Pre-commit Hooks

Configured in `.pre-commit-config.yaml`:
1. **black** (v26.1.0) — Code formatting, line-length 88
2. **isort** (v7.0.0) — Import sorting, profile=black
3. **ruff** (v0.15.0) — Linting with auto-fix
4. **docformatter** (v1.7.7) — Docstring formatting, wrap-summaries 79
5. **mypy** (v1.19.1) — Type checking, ignore-missing-imports
6. **pydocstyle** (v6.3.0) — Docstring convention (google)

Run manually: `pre-commit run --all-files`

---

## Evaluation Framework

- **Scorer:** YAML rubrics with weighted scores across dimensions: Completeness, Correctness, Quality, Specificity, Alignment.
- **Evaluators:** 5 types — base, LLM, pattern, quality, standard.
- **Rubrics:** 8 YAML definitions — `default.yaml`, `agent.yaml`, `code.yaml`, `coding_standards.yaml`, `pattern.yaml`, `prompt_pattern.yaml`, `prompt_standard.yaml`, `quality.yaml`.
- **Runners:** BatchRunner, StreamingRunner.
- **Reporters:** HTML, JSON, Markdown output formats.
- **Sandbox:** Local execution sandboxing for safe evaluation.
- **LLM Judge:** `tools/agents/benchmarks/llm_evaluator.py` — 0.0–10.0 rubric scoring.
- **Confidence Interval Gating:** For research workflows, require `coverage_score >= 0.80`, `source_quality_score >= 0.80`, etc.

---

## Research Standards

- **Source Governance:**
  - **Tier A (Always allowed):** Official vendor docs, peer-reviewed papers (NeurIPS, ICML, etc.), arXiv (known groups).
  - **Tier B (Conditional):** High-quality engineering blogs, Stack Overflow (high votes).
  - **Tier C (Blocked):** Unverified blogs, marketing materials.
- **Citations:** Every research claim must include inline citations with valid URLs: `[Claim text] (Source: Title, Publisher, Date — URL)`.
- **Critical-claim rule:** Architectural decisions require >= 2 independent Tier A sources.

---

## Workflow & Agent Authoring

- **YAML Rules:** Every step MUST have `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`.
- **Tools:** Allowlisted per step. Default DENY for high-risk tools (shell, git, file_delete).
- **Personas:** Defined in `agentic_v2/prompts/*.md` (23 personas). Must define Expertise, Boundaries, Critical rules, Output format.
- **Agent implementations:** `agents/implementations/` contains Claude SDK agent and dynamic agent loader.

---

## Claude Code Configuration

### Commands (`.claude/commands/`)

11 slash commands for development workflows:

| Command | Purpose |
|---------|---------|
| `/plan` | Create implementation plan using planner agent |
| `/tdd` | Enforce TDD workflow (RED → GREEN → REFACTOR) |
| `/build-fix` | Incrementally fix build errors |
| `/code-review` | Security and quality review |
| `/python-review` | Python-specific code review (ruff, mypy, bandit) |
| `/test-coverage` | Analyze coverage and generate missing tests |
| `/refactor-clean` | Safely remove dead code |
| `/orchestrate` | Sequential multi-agent workflow |
| `/eval` | Eval-driven development |
| `/checkpoint` | Create/verify workflow checkpoints |
| `/update-docs` | Sync documentation with source code |

### Contexts (`.claude/contexts/`)

3 execution modes: `dev` (implementation), `research` (exploration), `review` (code review/QA).

### Rules (`.claude/rules/`)

7 common rules (agents, coding-style, git-workflow, ml-practices, patterns, security, testing) + 5 Python-specific rules (coding-style, hooks, patterns, security, testing).

### Skills (`.claude/skills/`)

8 specialized skills: code-review, debugging, context-engineering, problem-solving, sequential-thinking, langsmith-fetch, mcp-builder, webapp-testing.

---

## Anti-Patterns — Never Do These

- **Never mutate state in place.** Always return new objects.
- **Never use bare `except:`.** Catch specific exceptions.
- **Never hardcode secrets.** Use `.env`.
- **Never produce TODOs in generated code.** All files must be complete.
- **Never add web servers or scaffolding unless explicitly requested.**
- **Never use `sys.path` hacks.** Use `from tools...` imports.
- **Never break existing contracts/schemas.** Additive-only.
- **Never skip the eval flywheel.** Define rubrics before building, run evals after.
- **Never use `print()` for logging.** Use `structlog` or `loguru`.
- **Never log secrets, PII, or raw model weights.**
- **Never commit `.env` files or API keys.**
