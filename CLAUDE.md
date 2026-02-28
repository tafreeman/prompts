# CLAUDE.md

## Environment Setup
Before doing anything else, run a full environment pre-flight check: 1) Detect the current OS and shell (PowerShell vs Bash vs Zsh), 2) Check if a Python venv exists and has all requirements installed — if not, create it and install dependencies, 3) Check if node_modules exists and matches package.json — if not, run install, 4) Scan for .env files and verify required environment variables are set (flag any missing ones), 5) Check if any required ports (3000, 8000, 8080) are already in use and report conflicts, 6) Verify git status is clean and report current branch. Output a concise status dashboard, then tell me we're ready to work.

## Shell Environment
- This project is developed on Windows/PowerShell. Do NOT use bash-specific syntax (e.g., `kill`, `lsof`). Use PowerShell equivalents (`Stop-Process`, `Get-NetTCPConnection`).

## Verification
- After making fixes, always verify they work by running the relevant code or tests. Do not wait for the user to ask 'did you even check it?'
- When user asks for a file path or simple answer, give the direct answer first before showing code.

---

## Repository Overview
**Repo:** `tafreeman/prompts` — A monorepo containing a multi-agent workflow runtime (`agentic-workflows-v2`), an evaluation framework (`agentic-v2-eval`), and shared utilities (`tools/`). Each subdirectory is an independent Python package.

**Mission:** Produce production-grade code, rigorous research, and reproducible evaluation artifacts that advance the state of the art in agentic AI.

---

## Code Quality Standards (Non-Negotiable)
1. **Immutability First:** Always create new objects. Never mutate existing ones. Use `@dataclass(frozen=True)`, `NamedTuple`, or `tuple`.
2. **Type Everything:** Full type annotations on all function signatures. No bare `Any` unless wrapping external untyped APIs. Use `Protocol` for duck-typed interfaces.
3. **Small Units:** Functions < 50 lines. Files < 800 lines (target 200–400). One class/module per file. Organize by feature/domain.
4. **Error Handling:** Never swallow exceptions. Use specific exception types with contextual messages. Validate at system boundaries. Fail fast.
5. **Formatting:** `black` (line-length 88) for code, `isort` (profile=black) for imports, `ruff` for linting.
6. **Testing:** At least one test per public function (happy path + error path). No test interdependencies. Target 80%+ coverage.

---

## Architecture

### Full Package Layout
```
prompts/                          # Monorepo root (prompts-tools, Python 3.10+, setuptools)
├── CLAUDE.md                     # This file — AI assistant instructions
├── pyproject.toml                # Root package: prompts-tools (shared utilities)
├── .pre-commit-config.yaml       # black, isort, ruff, docformatter, mypy, pydocstyle
├── .env.example                  # Template for all required environment variables
│
├── agentic-workflows-v2/         # Main runtime (Python 3.11+, hatchling)
│   ├── pyproject.toml            # Package: agentic-workflows-v2
│   ├── dev.sh                    # Hot-reload dev script (backend + frontend)
│   ├── agentic_v2/
│   │   ├── cli/                  # Typer CLI entry point (`agentic` command)
│   │   │   └── main.py           # CLI main: list, run, validate, serve
│   │   ├── agents/               # Agent definitions and implementations
│   │   │   ├── base.py           # Base agent ABC
│   │   │   ├── architect.py      # Architect agent
│   │   │   ├── coder.py          # Coder agent
│   │   │   ├── reviewer.py       # Reviewer agent
│   │   │   ├── orchestrator.py   # Multi-agent orchestrator
│   │   │   ├── capabilities.py   # Agent capability definitions
│   │   │   └── implementations/  # Backend-specific agent implementations
│   │   │       ├── agent_loader.py
│   │   │       ├── claude_agent.py
│   │   │       └── claude_sdk_agent.py
│   │   ├── config/               # Configuration management
│   │   │   └── defaults/         # Default YAML configs
│   │   │       ├── agents.yaml   # Agent tier assignments
│   │   │       ├── models.yaml   # Model registry (providers, endpoints, limits)
│   │   │       └── evaluation.yaml
│   │   ├── contracts/            # Pydantic I/O models (ADDITIVE-ONLY changes)
│   │   │   ├── messages.py       # Message contracts
│   │   │   └── schemas.py        # Workflow/step schemas
│   │   ├── engine/               # Native DAG executor (Kahn's algorithm)
│   │   │   ├── dag.py            # DAG construction
│   │   │   ├── dag_executor.py   # Async DAG execution engine
│   │   │   ├── executor.py       # Step executor
│   │   │   ├── runtime.py        # Workflow runtime
│   │   │   ├── pipeline.py       # Pipeline orchestration
│   │   │   ├── step.py           # Step definition
│   │   │   ├── step_state.py     # Step state tracking
│   │   │   ├── context.py        # Execution context
│   │   │   ├── expressions.py    # JMESPath expression evaluation
│   │   │   ├── agent_resolver.py # Agent resolution by tier
│   │   │   └── patterns/         # Execution patterns (extensible)
│   │   ├── evaluation/           # Inline evaluation helpers
│   │   │   └── normalization.py  # Score normalization utilities
│   │   ├── integrations/         # External system integrations
│   │   │   ├── base.py           # TraceAdapter ABC
│   │   │   ├── tracing.py        # NullTraceAdapter (no-op default)
│   │   │   ├── otel.py           # OpenTelemetry OTLP setup (opt-in)
│   │   │   └── langchain.py      # LangChain integration adapter
│   │   ├── langchain/            # PRIMARY execution engine (LangChain + LangGraph)
│   │   │   ├── graph.py          # LangGraph state machine builder
│   │   │   ├── runner.py         # LangGraph workflow runner
│   │   │   ├── state.py          # Graph state definitions
│   │   │   ├── agents.py         # LangChain agent wrappers
│   │   │   ├── models.py         # LLM provider probing + tier defaults
│   │   │   ├── config.py         # LangChain configuration
│   │   │   ├── expressions.py    # LangChain expression support
│   │   │   └── tools.py          # LangChain tool adapters
│   │   ├── models/               # LLM tier routing
│   │   │   ├── smart_router.py   # Smart model routing by tier + capability
│   │   │   ├── router.py         # Base router
│   │   │   ├── backends.py       # Provider backend registry
│   │   │   ├── client.py         # LLM client wrapper
│   │   │   ├── llm.py            # LLM abstractions
│   │   │   └── model_stats.py    # Model usage statistics
│   │   ├── prompts/              # Agent persona definitions (22 personas)
│   │   │   ├── analyst.md        ├── architect.md
│   │   │   ├── coder.md          ├── debugger.md
│   │   │   ├── developer.md      ├── generator.md
│   │   │   ├── judge.md          ├── linter.md
│   │   │   ├── orchestrator.md   ├── planner.md
│   │   │   ├── reasoner.md       ├── researcher.md
│   │   │   ├── reviewer.md       ├── summarizer.md
│   │   │   ├── task_planner.md   ├── tester.md
│   │   │   ├── validator.md      ├── vision.md
│   │   │   ├── writer.md         ├── analyzer.md
│   │   │   ├── assembler.md      └── containment_checker.md
│   │   ├── server/               # FastAPI app + WebSocket + SSE streaming
│   │   │   ├── app.py            # FastAPI factory, CORS, lifespan, SPA fallback
│   │   │   ├── auth.py           # API key middleware (opt-in via AGENTIC_API_KEY)
│   │   │   ├── websocket.py      # WebSocket streaming endpoint
│   │   │   ├── models.py         # Server-specific Pydantic models
│   │   │   ├── datasets.py       # Dataset management endpoints
│   │   │   ├── evaluation.py     # Evaluation endpoints
│   │   │   ├── evaluation_scoring.py
│   │   │   ├── judge.py          # LLM judge endpoints
│   │   │   ├── multidimensional_scoring.py
│   │   │   ├── normalization.py  # Server-side score normalization
│   │   │   ├── scoring_profiles.py
│   │   │   └── routes/           # API route modules
│   │   │       ├── health.py     # GET /api/health
│   │   │       ├── agents.py     # /api/agents endpoints
│   │   │       └── workflows.py  # /api/workflows endpoints
│   │   ├── tools/                # In-process tool system
│   │   │   ├── base.py           # Tool ABC
│   │   │   ├── registry.py       # Tool registry (allowlist enforcement)
│   │   │   └── builtin/          # 12 built-in tool categories
│   │   │       ├── build_ops.py      # Build/compile operations
│   │   │       ├── code_analysis.py  # Static code analysis
│   │   │       ├── code_execution.py # Code execution sandbox
│   │   │       ├── context_ops.py    # Context management
│   │   │       ├── file_ops.py       # File read/write
│   │   │       ├── git_ops.py        # Git operations
│   │   │       ├── http_ops.py       # HTTP requests
│   │   │       ├── memory_ops.py     # In-memory state
│   │   │       ├── search_ops.py     # Code/web search
│   │   │       ├── shell_ops.py      # Shell execution (HIGH-RISK)
│   │   │       └── transform.py      # Data transformation
│   │   ├── utils/
│   │   │   └── path_safety.py    # Path traversal prevention
│   │   └── workflows/            # YAML workflow system
│   │       ├── loader.py         # YAML workflow loader + validator
│   │       ├── runner.py         # Workflow execution runner
│   │       ├── run_logger.py     # JSON replay logging
│   │       ├── artifact_extractor.py
│   │       └── definitions/      # 10 declarative workflow YAMLs
│   │           ├── bug_resolution.yaml
│   │           ├── code_review.yaml
│   │           ├── deep_research.yaml
│   │           ├── fullstack_generation.yaml
│   │           ├── fullstack_generation_bounded_rereview.yaml
│   │           ├── multi_agent_codegen_e2e.yaml
│   │           ├── multi_agent_codegen_e2e_single_loop.yaml
│   │           ├── plan_implementation.yaml
│   │           ├── tdd_codegen_e2e.yaml
│   │           └── test_deterministic.yaml
│   ├── tests/                    # pytest-asyncio (asyncio_mode = "auto"), 37 test files
│   │   ├── conftest.py
│   │   ├── fixtures/             # Test data and datasets
│   │   ├── test_agents.py, test_agents_integration.py, test_agents_orchestrator.py
│   │   ├── test_cli.py, test_contracts.py
│   │   ├── test_dag.py, test_dag_executor.py, test_engine.py
│   │   ├── test_expressions.py, test_langchain_engine.py, test_langchain_integration.py
│   │   ├── test_model_router.py, test_provider_adapters.py
│   │   ├── test_evaluation_scoring.py, test_multidimensional_scoring.py
│   │   ├── test_normalization.py, test_scoring_profiles.py
│   │   ├── test_server_evaluation.py, test_server_judge.py, test_server_workflow_routes.py
│   │   ├── test_memory_context_tools.py, test_phase2d_tools.py, test_registry.py
│   │   ├── test_run_logger.py, test_runner_ui.py, test_runtime.py
│   │   ├── test_step_state.py, test_tier0.py
│   │   ├── test_workflow_loader.py, test_workflow_runner.py, test_workflow_tracing.py
│   │   └── test_dataset_workflows.py, test_new_agents.py
│   └── ui/                       # React 19 + Vite 6 + React Flow 12 + Tailwind CSS
│       ├── package.json          # TanStack Query, @xyflow/react, lucide-react, react-router-dom v7
│       ├── vite.config.ts
│       ├── vitest.config.ts      # Vitest + jsdom + @testing-library/react
│       └── src/
│           ├── App.tsx           # Main app with React Router
│           ├── main.tsx
│           ├── api/              # API client, types, WebSocket
│           ├── hooks/            # useRuns, useWorkflowStream, useWorkflows
│           ├── pages/            # Dashboard, Datasets, Evaluations, Live, RunDetail, Workflows
│           ├── components/       # Shared UI components
│           └── __tests__/        # 6 test files (Vitest)
│
├── agentic-v2-eval/              # Evaluation framework (Python 3.10+, setuptools)
│   ├── pyproject.toml            # Package: agentic-v2-eval v0.3.0
│   ├── src/agentic_v2_eval/
│   │   ├── interfaces.py         # LLMClientProtocol, Evaluator protocol
│   │   ├── scorer.py             # Rubric-based scoring engine
│   │   ├── datasets.py           # Benchmark dataset bridge
│   │   ├── evaluators/           # Pluggable evaluator implementations
│   │   │   ├── standard.py       # 5-dimension prompt scoring (clarity, effectiveness, structure, specificity, completeness)
│   │   │   ├── pattern.py        # Complex agentic pattern scoring (ReAct, CoVe, etc.)
│   │   │   ├── quality.py        # LLM-based quality metrics
│   │   │   └── llm.py            # LLM judge evaluator
│   │   ├── metrics/              # accuracy, quality, performance scoring
│   │   ├── runners/              # BatchRunner[T,R], StreamingRunner[T,R]
│   │   ├── reporters/            # JSON, Markdown, HTML report generation
│   │   ├── rubrics/              # YAML rubric definitions (8 rubrics)
│   │   │   ├── default.yaml, agent.yaml, code.yaml, pattern.yaml
│   │   │   ├── quality.yaml, coding_standards.yaml
│   │   │   └── prompt_pattern.yaml, prompt_standard.yaml
│   │   ├── sandbox/              # Code execution sandbox (local)
│   │   └── adapters/             # LLM client adapter layer
│   └── tests/                    # 10 test files (pytest + pytest-asyncio)
│
├── tools/                        # Shared utilities package (prompts-tools)
│   ├── __init__.py               # Package exports
│   ├── validate_subagents.py     # Subagent registry validator
│   ├── llm/                      # Multi-backend LLM client
│   │   ├── llm_client.py         # Unified LLMClient abstraction
│   │   ├── provider_adapters.py  # Provider-specific adapters
│   │   ├── langchain_adapter.py  # LangChain bridge
│   │   ├── smart_router.py → model_inventory.py  # Model catalog
│   │   ├── model_probe.py        # Runtime model availability probing
│   │   ├── model_bakeoff.py      # Model comparison benchmarks
│   │   ├── model_locks.py        # Rate limit management
│   │   ├── rank_models.py        # Model ranking algorithms
│   │   ├── local_model.py        # Local model integration (Ollama, etc.)
│   │   ├── local_models.py       # Local model discovery
│   │   ├── windows_ai.py         # Windows AI / Phi Silica integration
│   │   ├── check_provider_limits.py
│   │   ├── list_gemini.py
│   │   └── run_local_concurrency.py
│   ├── agents/                   # Agent benchmarks
│   │   └── benchmarks/           # Evaluation pipeline, LLM evaluator, datasets
│   │       ├── datasets.py, loader.py, registry.py
│   │       ├── runner.py, runner_ui.py
│   │       ├── llm_evaluator.py  # 0.0–10.0 rubric scoring
│   │       ├── evaluation_pipeline.py
│   │       └── workflow_pipeline.py
│   ├── core/                     # Config, errors, caching
│   │   ├── config.py             # Centralized configuration
│   │   ├── errors.py             # Custom exception hierarchy
│   │   ├── cache.py              # Caching utilities
│   │   ├── response_cache.py     # LLM response cache
│   │   ├── model_availability.py # Provider availability tracking
│   │   ├── prompt_db.py          # Prompt database
│   │   ├── local_media.py        # Local media handling
│   │   └── tool_init.py          # Tool initialization
│   └── research/
│       └── build_library.py      # Research library builder
│
├── .claude/                      # Claude Code configuration
│   ├── commands/                 # 11 slash commands
│   │   ├── build-fix.md, checkpoint.md, code-review.md
│   │   ├── eval.md, orchestrate.md, plan.md
│   │   ├── python-review.md, refactor-clean.md, tdd.md
│   │   ├── test-coverage.md, update-docs.md
│   ├── contexts/                 # Context profiles
│   │   ├── dev.md, research.md, review.md
│   ├── rules/                    # Coding rules (common/ + python/)
│   │   ├── common/               # agents, coding-style, git-workflow, ml-practices, patterns, security, testing
│   │   └── python/               # coding-style, hooks, patterns, security, testing
│   └── skills/                   # 9 Claude skills
│       ├── changelog-generator/, code-review/, context-engineering/
│       ├── debugging/, langsmith-fetch/, mcp-builder/
│       ├── problem-solving/, sequential-thinking/, webapp-testing/
│
├── .github/
│   ├── agents/                   # 16 GitHub Copilot agents (*.agent.md)
│   ├── workflows/                # 11 CI/CD workflows
│   │   ├── ci.yml                # Main CI: lint + test + coverage
│   │   ├── deploy.yml, dependency-review.yml
│   │   ├── eval-package-ci.yml, eval-poc.yml
│   │   ├── docs-verify.yml, validate-prompts.yml
│   │   ├── prompt-quality-gate.yml, prompt-validation.yml
│   │   ├── manifest-temperature-check.yml
│   │   └── performance-benchmark.yml
│   └── copilot-instructions.md
│
├── .agent/                       # Additional agent workflows
│   ├── rules/run.md
│   └── workflows/                # coderev, generate-prompt, improve-prompt, repo-documenter
│
├── docs/                         # Project documentation
│   ├── ARCHITECTURE.md           # Architecture deep-dive
│   ├── CODING_STANDARDS.md       # Coding standards reference
│   ├── subagents.yml             # Subagent registry
│   └── pr-checklists/            # PR review checklists
│
├── research/                     # Research artifacts
│   ├── library/                  # Approved domains, source registry, references
│   └── subagents/                # Research sub-agent reports (Scout, Librarian, Curator, Auditor)
│
├── reports/                      # Generated reports
│   ├── deep-research/            # Deep research workflow outputs (JSON, MD, PDF)
│   └── model-bakeoff/            # Model comparison results (JSON)
│
├── runs/                         # Workflow run logs (JSON replay)
│   └── _inputs/                  # Run input files
│
├── scripts/
│   └── setup_env_loading.ps1     # PowerShell env setup script
│
└── tests/                        # Root-level tests
    └── e2e/test_subagent_smoke.py
```

### Key Architectural Points
- **Dual execution engines:** `langchain/` wraps LangGraph state machines (primary). `engine/` is an independent native DAG executor using Kahn's algorithm. Both are active and share contracts.
- **LLM routing:** `models/smart_router.py` dispatches to backends (OpenAI, Anthropic, Google Gemini, Azure, Ollama, local models, Windows AI/Phi Silica) based on tier and capability.
- **Workflows:** Declarative YAML under `workflows/definitions/`. Steps reference agents by tier name. 10 pre-built workflows covering codegen, research, review, TDD, and bug resolution.
- **Contracts:** Pydantic models in `contracts/` define all I/O. **Additive-only changes** — never break existing schemas.
- **Tool system:** 12 built-in tool categories with allowlist enforcement. Default DENY for high-risk tools (shell, git, file_delete).
- **Agent personas:** 22 markdown persona files in `prompts/` defining expertise, boundaries, critical rules, and output format.
- **Tracing:** Opt-in OpenTelemetry integration via `AGENTIC_TRACING=1`. OTLP export to AI Toolkit or custom collectors.
- **Server:** FastAPI with CORS, optional API key auth, WebSocket streaming, and SPA fallback serving the React UI in production.

---

## Environment Variables

Copy `.env.example` to `.env` and configure. Key variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | For GitHub Models | GitHub PAT for GitHub Models API |
| `OPENAI_API_KEY` | For OpenAI | OpenAI API key |
| `AZURE_OPENAI_API_KEY_0` | For Azure | Azure OpenAI key (supports _0 through _n for failover) |
| `AZURE_OPENAI_ENDPOINT_0` | For Azure | Azure OpenAI endpoint |
| `GEMINI_API_KEY` | For Gemini | Google Gemini API key |
| `ANTHROPIC_API_KEY` | For Claude | Anthropic API key |
| `LOCAL_MODEL_PATH` | Optional | Path to local models (auto-detected from ~/.cache/aigallery) |
| `PHI_SILICA_LAF_TOKEN` | Optional | Windows AI Phi Silica LAF token |
| `AGENTIC_TRACING` | Optional | Set to `1` to enable OpenTelemetry tracing |
| `AGENTIC_TRACE_SENSITIVE` | Optional | Set to `1` to include prompts/responses in traces |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | Optional | OTLP endpoint (default: `http://localhost:4317`) |
| `AGENTIC_API_KEY` | Optional | API key for server authentication |
| `AGENTIC_CORS_ORIGINS` | Optional | Comma-separated CORS origins |

---

## Commands

### Backend (agentic-workflows-v2)
```bash
# Install (from agentic-workflows-v2/)
pip install -e ".[dev,server,langchain]"

# Install with tracing support
pip install -e ".[dev,server,langchain,tracing]"

# Install with Claude Agent SDK
pip install -e ".[dev,server,langchain,claude]"

# Run full test suite
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ -v --cov=agentic_v2 --cov-report=term-missing

# Lint / format (from repo root)
pre-commit run --all-files

# Hot-reload dev (backend port 8010 + frontend port 5173)
bash dev.sh [backend_port] [frontend_port]

# Production serve
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010 --app-dir src
```

### CLI (`agentic` command)
```bash
agentic list workflows|agents|tools
agentic run <workflow> --input <file.json>
agentic validate <workflow>
agentic serve
```

### Frontend (agentic-workflows-v2/ui/)
```bash
cd agentic-workflows-v2/ui

# Install dependencies
npm install

# Dev server (Vite, port 5173)
npm run dev

# Build for production
npm run build

# Run tests (Vitest)
npm run test

# Tests with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Evaluation (agentic-v2-eval/)
```bash
cd agentic-v2-eval && pip install -e ".[dev]"

# Score results against a rubric
python -m agentic_v2_eval evaluate results.json [--rubric custom.yaml] [-o scored.json]

# Generate reports
python -m agentic_v2_eval report results.json -f {json|markdown|html} -o output.ext

# Run tests
python -m pytest tests/ -v

# Run with coverage
./scripts/run_coverage.sh
```

### Shared Tools (from repo root)
```bash
# Install root package
pip install -e ".[dev]"

# Validate subagent registry
python tools/validate_subagents.py
```

### Pre-commit Hooks
The `.pre-commit-config.yaml` runs in order:
1. **black** (line-length 88)
2. **isort** (profile=black)
3. **ruff** (--fix)
4. **docformatter** (google convention, wrap-summaries 79)
5. **mypy** (--ignore-missing-imports)
6. **pydocstyle** (google convention)

---

## Research Standards
- **Source Governance:**
  - **Tier A (Always allowed):** Official vendor docs, Peer-reviewed papers (NeurIPS, ICML, etc.), arXiv (known groups).
  - **Tier B (Conditional):** High-quality engineering blogs, Stack Overflow (high votes).
  - **Tier C (Blocked):** Unverified blogs, marketing materials.
- **Citations:** Every research claim must include inline citations with valid URLs: `[Claim text] (Source: Title, Publisher, Date — URL)`.
- **Critical-claim rule:** Architectural decisions require >= 2 independent Tier A sources.
- **Research library:** Maintained in `research/library/` with approved domains, source registry, and material manifests.

---

## Evaluation Framework
- **Scorer:** YAML rubrics → weighted scores across dimensions (Completeness, Correctness, Quality, Specificity, Alignment).
- **Evaluators:** Standard (5-dimension), Pattern (7 universal + pattern-specific), Quality (LLM-based), LLM Judge.
- **Runners:** BatchRunner[T,R], StreamingRunner[T,R] with progress/error callbacks.
- **Reporters:** JSON, Markdown, HTML with shared summary utilities.
- **LLM Judge:** `tools/agents/benchmarks/llm_evaluator.py` — 0.0–10.0 rubric scoring.
- **Confidence Interval Gating:** For research workflows, require `coverage_score >= 0.80`, `source_quality_score >= 0.80`, etc.
- **Rubrics:** 8 pre-built YAML rubrics: default, agent, code, pattern, quality, coding_standards, prompt_pattern, prompt_standard.

---

## Workflow & Agent Authoring
- **YAML Rules:** Every step MUST have `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`.
- **Tools:** Allowlisted per step. Default DENY for high-risk tools (shell, git, file_delete).
- **Personas:** Defined in `agentic_v2/prompts/*.md`. Must define Expertise, Boundaries, Critical rules, Output format. 22 personas available.
- **Available Workflows:** bug_resolution, code_review, deep_research, fullstack_generation, fullstack_generation_bounded_rereview, multi_agent_codegen_e2e, multi_agent_codegen_e2e_single_loop, plan_implementation, tdd_codegen_e2e, test_deterministic.

---

## CI/CD

### Main CI Pipeline (`.github/workflows/ci.yml`)
Triggers on push/PR to `main` and `agenticv2` branches:
1. Pre-commit hooks (black, isort, ruff, mypy, pydocstyle)
2. pytest with coverage (`--cov=agentic_v2 --cov-report=term-missing`)
3. Documentation reference check
4. Optional Sphinx docs build

### Additional Workflows
- **eval-package-ci.yml** — Eval framework CI
- **prompt-quality-gate.yml** / **prompt-validation.yml** — Prompt quality gates
- **dependency-review.yml** — Dependency security review
- **performance-benchmark.yml** — Performance benchmarks
- **deploy.yml** — Deployment pipeline
- **docs-verify.yml** — Documentation verification

---

## Anti-Patterns — Never Do These
- **Never mutate state in place.** Always return new objects.
- **Never use bare `except:`.** Catch specific exceptions.
- **Never hardcode secrets.** Use `.env`.
- **Never produce TODOs in generated code.** All files must be complete.
- **Never add web servers or scaffolding unless explicitly requested.**
- **Never use sys.path hacks.** Use `from tools...` imports.
- **Never break existing contracts/schemas.** Additive-only.
- **Never skip the eval flywheel.** Define rubrics before building, run evals after.
- **Never log secrets, PII, or raw model weights.** GDPR/CCPA compliance.
- **Never use `print()` for logging.** Use `structlog` or `loguru`.
- **Never commit `.env` files.** They are gitignored.
