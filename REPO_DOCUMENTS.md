# 📚 Repository Documents — Master Catalog

> **Repository:** `d:\source\prompts` (branch: `main`)
> **Generated:** 2026-02-19
> **Purpose:** Definitive guide to the repository's contents, structure, and key files.

---

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Top-Level Structure](#top-level-structure)
3. [Domain Catalog](#domain-catalog)
   - [agentic-workflows-v2 (Core Runtime)](#agentic-workflows-v2-core-runtime)
   - [agentic-v2-eval (Evaluation Framework)](#agentic-v2-eval-evaluation-framework)
   - [tools (Shared Utilities)](#tools-shared-utilities)
   - [.github (CI/CD & Agents)](#github-cicd--agents)
   - [reports & runs (Artifacts)](#reports--runs-artifacts)
4. [Deep Dive: agentic-workflows-v2](#deep-dive-agentic-workflows-v2)
   - [Engine](#engine)
   - [Server](#server)
   - [Workflows & Definitions](#workflows--definitions)
   - [Agents](#agents)
   - [Models & Routing](#models--routing)
   - [Tools (Built-in)](#tools-built-in)
   - [Integrations](#integrations)
   - [Contracts](#contracts)
   - [Configuration](#configuration)
   - [Prompts](#prompts)
   - [LangChain Sub-Module](#langchain-sub-module)
   - [UI (Frontend Dashboard)](#ui-frontend-dashboard)
   - [Scripts](#scripts)
   - [Tests](#tests)
   - [Documentation](#documentation)
5. [Deep Dive: agentic-v2-eval](#deep-dive-agentic-v2-eval)
6. [Deep Dive: tools](#deep-dive-tools)
7. [Project Health & Observations](#project-health--observations)
8. [Recommendations](#recommendations)

---

## Repository Overview

This is a **mono-repo** for building, running, and evaluating multi-agent AI workflows. It is organized around three primary packages:

| Package | Purpose | Install |
|---------|---------|---------|
| **`agentic-workflows-v2/`** | Core runtime — agent orchestration, DAG engine, workflow runner, FastAPI server with React UI | `pip install -e .` |
| **`agentic-v2-eval/`** | Evaluation framework — rubric scoring, metrics, batch runners, HTML/MD/JSON reporting | `pip install -e .` |
| **`tools/`** | Shared utilities — LLM client abstraction, benchmark datasets, config primitives | `pip install -e .` (root `pyproject.toml`) |

All packages target **Python 3.11+** and follow an async-first architecture.

---

## Top-Level Structure

```
d:\source\prompts\
├── .agent/                    # Agent workflow definitions (slash commands)
├── .claude/                   # Claude agent settings
├── .github/                   # CI/CD workflows + GitHub Copilot agents (19 agents)
│   ├── agents/                # GitHub Agent definitions (.agent.md files)
│   ├── instructions/          # Copilot instructions
│   └── workflows/             # 10 CI/CD workflow YAML files
├── agentic-v2-eval/           # Evaluation framework package
├── agentic-workflows-v2/      # Core runtime package (primary)
├── reports/                   # Output reports (deep-research, model-bakeoff)
├── runs/                      # Archived workflow run outputs
├── tools/                     # Shared utilities package
├── .aider.conf.yml            # Aider AI assistant config
├── .env / .env.example        # Environment variables
├── .gitignore                 # Git ignore rules
├── .pre-commit-config.yaml    # Pre-commit hooks
├── follow.txt                 # Scratch/notes file
├── output.txt                 # Scratch/notes file
├── prompts.sln                # Visual Studio solution
├── pyproject.toml             # Root package (prompts-tools)
└── README.md                  # Root README
```

---

## Domain Catalog

### agentic-workflows-v2 (Core Runtime)

The **primary package**. Contains the full-stack application: Python backend (agents, engine, server) and React/TypeScript frontend (dashboard UI).

**Key entry points:**

- `agentic_v2/__init__.py` — Public API surface (219 lines, ~100 exports)
- `agentic_v2/server/app.py` — FastAPI app factory
- `agentic_v2/cli/__init__.py` — CLI entry point (`agentic` command)
- `pyproject.toml` — Package definition, dependencies, optional extras

### agentic-v2-eval (Evaluation Framework)

A **separate, standalone package** for evaluating agentic workflow outputs. Provides scoring, metrics, rubrics, and report generation.

**Key entry points:**

- `src/agentic_v2_eval/__init__.py` — Package API
- `src/agentic_v2_eval/__main__.py` — CLI entry point
- `README.md` — Usage documentation

### tools (Shared Utilities)

The **shared foundation layer** installed from the root `pyproject.toml`. Provides:

- LLM client abstraction (multi-provider)
- Benchmark dataset loaders (HumanEval, MBPP, SWE-bench)
- Configuration, caching, and error handling primitives

### .github (CI/CD & Agents)

Contains **10 GitHub Actions workflows** and **19 GitHub Copilot agent definitions**:

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Core CI pipeline |
| `deploy.yml` | Deployment pipeline |
| `eval-package-ci.yml` | Eval package CI |
| `dependency-review.yml` | Dependency security review |
| `performance-benchmark.yml` | Performance benchmarks |
| `prompt-quality-gate.yml` | Prompt quality gate checks |
| `prompt-validation.yml` | Prompt validation pipeline |

### reports & runs (Artifacts)

- **`reports/`** — Contains sub-folders for `deep-research` and `model-bakeoff` results.
- **`runs/`** — Archived workflow execution outputs (JSON format). Currently contains only `_inputs/` folder with 5 sample input files. Historic run JSON files were recently reorganized.

---

## Deep Dive: agentic-workflows-v2

### Engine

**Path:** `agentic_v2/engine/`
**Purpose:** The workflow execution infrastructure — step lifecycle, DAG resolution, pipeline orchestration, and isolated runtime execution.

| File | Size | Purpose |
|------|------|---------|
| `__init__.py` | 2.4 KB | Module exports (~50 symbols) |
| `agent_resolver.py` | 33.4 KB | Agent resolution for workflow steps — maps step `agent:` to live agent instances |
| `context.py` | 15.2 KB | `ExecutionContext` and `ServiceContainer` — shared state across steps |
| `dag.py` | 5.2 KB | DAG construction, topological sorting, cycle detection |
| `dag_executor.py` | 7.4 KB | DAG-based step execution with dependency resolution |
| `executor.py` | 13.8 KB | `WorkflowExecutor` — top-level orchestrator for running workflows |
| `expressions.py` | 13.4 KB | `${...}` expression evaluator for step I/O wiring |
| `pipeline.py` | 13.9 KB | `Pipeline`, `PipelineBuilder`, `PipelineExecutor` — sequential/parallel grouping |
| `runtime.py` | 12.2 KB | `IsolatedTaskRuntime`, `SubprocessRuntime`, `DockerRuntime` — sandboxed execution |
| `step.py` | 18.5 KB | `StepDefinition`, `StepExecutor`, retry logic |
| `step_state.py` | 2.4 KB | `StepState`, `StepStateManager` — step lifecycle state machine |
| `patterns/` | (empty) | **Placeholder** — future execution patterns (Phase 2) |

### Server

**Path:** `agentic_v2/server/`
**Purpose:** FastAPI-based REST API serving the workflow runtime and built frontend UI.

| File | Size | Purpose |
|------|------|---------|
| `app.py` | 2.9 KB | FastAPI app factory with CORS, route registration, SPA fallback |
| `evaluation.py` | 51.3 KB | **Largest module** — Scoring engine: hard gates, normalization, rubric resolution, criterion floors, grading |
| `judge.py` | 15.3 KB | LLM-as-a-judge evaluation logic |
| `models.py` | 4.7 KB | Pydantic request/response models |
| `normalization.py` | 4.0 KB | Formula registry (binary, likert, lower-is-better, etc.) + Bayesian reliability |
| `scoring_profiles.py` | 2.1 KB | Workflow-family scoring profiles A–D |
| `websocket.py` | 4.7 KB | WebSocket connection manager + SSE listener |
| `routes/workflows.py` | 20.7 KB | Workflow API routes: run, evaluate, list datasets, SSE streaming |
| `routes/agents.py` | 1.2 KB | Agent listing and info routes |
| `routes/health.py` | 329 B | Health check endpoint |

### Workflows & Definitions

**Path:** `agentic_v2/workflows/`
**Purpose:** YAML-defined workflow parsing, execution, and logging.

| File | Size | Purpose |
|------|------|---------|
| `loader.py` | 21.6 KB | YAML workflow parsing → `WorkflowDefinition` objects |
| `runner.py` | 17.6 KB | Workflow runner: load → validate → execute → resolve outputs |
| `run_logger.py` | 7.5 KB | Run log persistence (JSON per run) |
| `artifact_extractor.py` | 4.6 KB | Extract artifacts from step outputs |

**Workflow Definitions** (`definitions/`):

| Definition | Size | Purpose |
|------------|------|---------|
| `code_review.yaml` | 3.8 KB | Code review DAG workflow (Profile B) |
| `fullstack_generation.yaml` | 6.4 KB | Fullstack generation workflow (Profile A) |
| `fullstack_generation_bounded_rereview.yaml` | 8.3 KB | Bounded re-review fullstack generation |
| `bug_resolution.yaml` | 4.8 KB | Bug resolution workflow |
| `deep_research.yaml` | 28.0 KB | Deep research multi-step workflow |
| `multi_agent_codegen_e2e.yaml` | 20.5 KB | End-to-end multi-agent code generation |
| `plan_implementation.yaml` | 22.6 KB | Iterative plan implementation (experimental) |
| `test_deterministic.yaml` | 763 B | Deterministic test workflow fixture |

### Agents

**Path:** `agentic_v2/agents/`
**Purpose:** Built-in agent implementations with capability mixins.

| File | Size | Purpose |
|------|------|---------|
| `__init__.py` | 2.1 KB | Public re-exports |
| `base.py` | 24.3 KB | `BaseAgent` — abstract base with memory, event hooks, conversation management |
| `architect.py` | 12.2 KB | `ArchitectAgent` — system design and architecture |
| `coder.py` | 11.4 KB | `CoderAgent` — code generation with Pydantic contracts |
| `reviewer.py` | 12.2 KB | `ReviewerAgent` — code review and security analysis |
| `orchestrator.py` | 19.0 KB | `OrchestratorAgent` — multi-agent task delegation |
| `test_agent.py` | 16.6 KB | `TestAgent` — test generation agent |
| `capabilities.py` | 8.9 KB | `Capability`, `CapabilityMixin`, `CapabilitySet` |
| `implementations/` | — | Additional agent implementations |
| `implementations/agent_loader.py` | 3.6 KB | Dynamic agent loading from config |
| `implementations/claude_agent.py` | 6.3 KB | Claude (Anthropic) agent adapter |
| `implementations/claude_sdk_agent.py` | 4.6 KB | Claude SDK–based agent |

### Models & Routing

**Path:** `agentic_v2/models/`
**Purpose:** Model routing, LLM client, circuit breaker, token budgets.

| File | Size | Purpose |
|------|------|---------|
| `__init__.py` | 1.9 KB | Module exports |
| `router.py` | 11.8 KB | `ModelRouter` — tier-based model selection and fallback |
| `smart_router.py` | 14.0 KB | `SmartModelRouter` — adaptive routing with circuit breakers |
| `client.py` | 13.8 KB | `LLMClientWrapper` — unified async LLM client |
| `backends.py` | 26.3 KB | Provider-specific backends (OpenAI, Anthropic, Ollama, ONNX, etc.) |
| `model_stats.py` | 11.8 KB | `ModelStats` — latency, token, cost tracking per model |
| `llm.py` | 1.2 KB | Lightweight LLM abstraction |

### Tools (Built-in)

**Path:** `agentic_v2/tools/`
**Purpose:** Agent-callable tool implementations.

| File | Size | Purpose |
|------|------|---------|
| `base.py` | 5.1 KB | `BaseTool`, `ToolResult`, `ToolSchema` — abstract tool interface |
| `registry.py` | 4.9 KB | `ToolRegistry` — discover and register tools |
| **`builtin/`** | | |
| `code_analysis.py` | 7.7 KB | AST analysis, complexity scoring |
| `code_execution.py` | 8.1 KB | Sandboxed code execution |
| `context_ops.py` | 5.8 KB | Context management operations |
| `file_ops.py` | 10.8 KB | File read/write/list operations |
| `git_ops.py` | 6.6 KB | Git operations (diff, log, blame) |
| `http_ops.py` | 7.7 KB | HTTP requests |
| `memory_ops.py` | 12.5 KB | Persistent memory CRUD (file-backed) |
| `search_ops.py` | 9.6 KB | Search operations (grep, find) |
| `shell_ops.py` | 8.0 KB | Shell command execution |
| `transform.py` | 11.7 KB | Data transformation utilities |

### Integrations

**Path:** `agentic_v2/integrations/`
**Purpose:** External system integrations.

| File | Size | Purpose |
|------|------|---------|
| `base.py` | 5.4 KB | Base integration interface (Phase 1: P1-T001) |
| `langchain.py` | 9.0 KB | LangChain adapters (`AgenticChatModel`, `AgenticTool`, `AgenticAgent`) |
| `otel.py` | 6.7 KB | OpenTelemetry setup and configuration |
| `tracing.py` | 10.7 KB | Workflow tracing — span creation for steps, LLM calls, tools |

### Contracts

**Path:** `agentic_v2/contracts/`
**Purpose:** Pydantic data models shared across the entire runtime.

| File | Size | Purpose |
|------|------|---------|
| `messages.py` | 17.0 KB | `StepResult`, `WorkflowResult`, `AgentMessage`, `StepStatus` |
| `schemas.py` | 15.6 KB | `CodeGenerationInput/Output`, `CodeReviewInput/Output`, `TestCase`, etc. |

### Configuration

**Path:** `agentic_v2/config/`
**Purpose:** YAML-based default configurations.

| File | Size | Purpose |
|------|------|---------|
| `defaults/models.yaml` | 6.7 KB | Model definitions, providers, routing rules, fallback strategy |
| `defaults/agents.yaml` | 8.0 KB | 18 agent definitions with roles, tools, and model assignments |
| `defaults/evaluation.yaml` | 7.6 KB | Evaluation datasets, metrics, scoring weights, reporting config |

### Prompts

**Path:** `agentic_v2/prompts/`
**Purpose:** Markdown-formatted agent prompt templates (22 files).

Agents with dedicated prompts: `analyst`, `analyzer`, `architect`, `assembler`, `coder`, `containment_checker`, `debugger`, `developer`, `generator`, `judge`, `linter`, `orchestrator`, `planner`, `reasoner`, `researcher`, `reviewer`, `summarizer`, `task_planner`, `tester`, `validator`, `vision`, `writer`.

### LangChain Sub-Module

**Path:** `agentic_v2/langchain/`
**Purpose:** Full LangChain/LangGraph integration layer.

| File | Size | Purpose |
|------|------|---------|
| `config.py` | 9.5 KB | LangChain configuration management |
| `graph.py` | 18.5 KB | LangGraph-based workflow graph builder |
| `runner.py` | 21.0 KB | LangChain workflow runner |
| `agents.py` | 3.9 KB | LangChain agent wrappers |
| `models.py` | 15.5 KB | LangChain model wrappers |
| `expressions.py` | 4.5 KB | LangChain expression adapters |
| `state.py` | 2.3 KB | LangGraph state management |
| `tools.py` | 13.1 KB | LangChain tool adapters |

### UI (Frontend Dashboard)

**Path:** `agentic-workflows-v2/ui/`
**Stack:** React + TypeScript + Vite + TailwindCSS
**Purpose:** Workflow management dashboard with live monitoring.

**Pages:**

| File | Purpose |
|------|---------|
| `DashboardPage.tsx` | Main dashboard overview |
| `WorkflowsPage.tsx` | List all available workflows |
| `WorkflowDetailPage.tsx` | Workflow detail view with DAG visualization |
| `RunDetailPage.tsx` | Individual run results and scoring |
| `LivePage.tsx` | Live execution monitoring via SSE/WebSocket |

**Components:**

| Directory | Purpose |
|-----------|---------|
| `components/common/` | Shared UI components |
| `components/dag/` | DAG visualization (`StepNode.tsx`, `WorkflowDAG.tsx`) |
| `components/layout/` | Page layout components |
| `components/live/` | Live event feed components |
| `components/runs/` | Run configuration and results (`RunConfigForm.tsx`) |

**API Layer:**

| File | Purpose |
|------|---------|
| `api/client.ts` | REST API client |
| `api/types.ts` | TypeScript type definitions |

### Scripts

**Path:** `agentic-workflows-v2/scripts/`
**Purpose:** Development utilities and operational tools.

| File | Purpose |
|------|---------|
| `start-dev.ps1` | Start development server (API + UI) |
| `stop-dev.ps1` | Stop development server |
| `restart-dev.ps1` | Restart development server |
| `status-dev.ps1` | Check development server status |
| `run-bounded-rereview.ps1` | Run bounded re-review workflow |
| `run-deep-research.ps1` | Run deep research workflow |
| `run_deep_research.py` | Python deep research runner |
| `test_sentinel_e2e.py` | End-to-end sentinel test |

### Tests

**Path:** `agentic-workflows-v2/tests/`
**Total test files:** 32
**Coverage areas:** Agents, CLI, contracts, DAG, engine, expressions, integrations, LangChain, memory, model routing, normalization, scoring profiles, server evaluation, workflow tracing, and more.

**Key test files by coverage:**

| Test File | Size | Covers |
|-----------|------|--------|
| `test_langchain_engine.py` | 41.7 KB | LangChain engine integration (largest test file) |
| `test_engine.py` | 28.7 KB | Core engine execution |
| `test_server_evaluation.py` | 26.7 KB | Scoring, hard gates, floors, rubrics, profiles |
| `test_expressions.py` | 22.8 KB | Expression resolution and context merge |
| `test_model_router.py` | 20.1 KB | Model routing and fallback |
| `test_contracts.py` | 18.8 KB | Message/schema contracts |
| `test_workflow_runner.py` | 16.9 KB | Runner execution and output resolution |
| `test_agents.py` | 15.7 KB | Agent implementations |
| `test_agents_orchestrator.py` | 14.9 KB | Orchestrator agent |
| `test_new_agents.py` | 14.9 KB | New agent implementations |
| `test_phase2d_tools.py` | 14.5 KB | Phase 2D tool implementations |
| `test_workflow_loader.py` | 12.6 KB | YAML parsing and filtering |

### Documentation

**Path:** `agentic-workflows-v2/docs/`

| File | Purpose |
|------|---------|
| `API_REFERENCE.md` | API reference documentation |
| `EVALUATION_MIGRATION_PLAN.md` | **Superseded** — Original evaluation migration plan |
| `IMPLEMENTATION_PLAN_V1_COMPLETE.md` | **Historical** — Phase 1 implementation record |
| `IMPLEMENTATION_PLAN_V2.md` | **Historical** — Phase 2 implementation record |
| `LANGCHAIN_MIGRATION_PLAN.md` | LangChain migration strategy |
| `PHASE2D_SUMMARY.md` | Phase 2D summary and outcomes |
| `adr/0001-package-structure.md` | ADR: Package structure decision |
| `adr/0002-evaluation-package.md` | ADR: Evaluation as separate package |
| `adr/0003-server-optional.md` | ADR: Server as optional dependency |
| `reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md` | Authoritative active vs deprecated module map |
| `tutorials/getting_started.md` | Getting started tutorial |
| `tutorials/creating_agent.md` | How to create a custom agent |
| `tutorials/building_workflow.md` | How to build a workflow |

---

## Deep Dive: agentic-v2-eval

**Path:** `agentic-v2-eval/`
**Purpose:** Standalone evaluation framework for scoring agentic workflow outputs.

```
agentic-v2-eval/
├── src/agentic_v2_eval/
│   ├── __init__.py            # Package exports (Scorer, etc.)
│   ├── __main__.py            # CLI entry point (6.1 KB)
│   ├── scorer.py              # Core scoring engine (5.0 KB)
│   ├── interfaces.py          # Abstract interfaces
│   ├── datasets.py            # Dataset loaders (7.1 KB)
│   ├── adapters/              # External system adapters
│   ├── evaluators/            # Evaluation implementations (6 files)
│   ├── metrics/               # Metric calculations (accuracy, quality, performance)
│   ├── reporters/             # Report generators (JSON, Markdown, HTML)
│   ├── rubrics/               # YAML rubric definitions (8 files)
│   ├── runners/               # Batch and streaming runners
│   └── sandbox/               # Sandboxed execution environment
├── tests/                     # Test suite (10 files)
├── docs/                      # Documentation (7 files)
├── pyproject.toml             # Package definition
├── LICENSE                    # MIT License
├── README.md                  # Usage documentation
└── chatlg.md                  # ⚠️ Large scratch file (54 KB) — candidate for cleanup
```

---

## Deep Dive: tools

**Path:** `tools/`
**Purpose:** Shared foundation utilities used by both `agentic-workflows-v2` and `agentic-v2-eval`.

```
tools/
├── __init__.py                # Package init
├── README.md                  # Module documentation
├── agents/
│   ├── __init__.py
│   └── benchmarks/            # Benchmark loaders (HumanEval, MBPP, SWE-bench)
├── core/
│   ├── __init__.py
│   ├── _encoding.py           # Encoding utilities
│   ├── cache.py               # Multi-layer cache (6.8 KB)
│   ├── config.py              # Configuration management
│   ├── errors.py              # Error hierarchy (5.5 KB)
│   ├── local_media.py         # Local media handling (14.9 KB)
│   ├── prompt_db.py           # Prompt database (5.7 KB)
│   ├── response_cache.py      # Response caching (14.5 KB)
│   └── tool_init.py           # Tool initialization (16.2 KB)
├── llm/
│   ├── __init__.py
│   ├── llm_client.py          # Unified LLM client (41.1 KB — largest file)
│   ├── local_model.py         # Local ONNX model runner (30.4 KB)
│   ├── model_probe.py         # Model capability probing (63.3 KB — very large)
│   ├── model_bakeoff.py       # Model comparison tool (21.4 KB)
│   ├── model_inventory.py     # Model inventory management (18.3 KB)
│   ├── model_locks.py         # Concurrency management
│   ├── langchain_adapter.py   # LangChain adapter
│   ├── windows_ai.py          # Windows AI integration (8.6 KB)
│   └── windows_ai_bridge/     # Windows AI bridge (C#/native)
└── windows_ai_bridge/         # Windows AI bridge utilities
```

---

## Project Health & Observations

### ✅ Strengths

1. **Clean working tree** — `main` is fully committed, no untracked or modified files.
2. **Comprehensive test suite** — 32 test files covering all major modules.
3. **Well-structured configs** — YAML-based agents, models, and evaluation configs are cleanly organized.
4. **Rich prompt library** — 22 dedicated agent prompt templates.
5. **Multi-provider model routing** — Supports OpenAI, Anthropic, Ollama, ONNX, Windows AI, GitHub Models, Azure Foundry.
6. **OpenTelemetry tracing** — Production-ready observability.
7. **Evaluation framework** — Separate, well-structured package with scoring, rubrics, and reporting.
8. **Frontend dashboard** — React/TypeScript UI with DAG visualization and live monitoring.
9. **CI/CD pipeline** — 10 GitHub Actions workflows covering CI, deployment, eval, security, and prompt validation.
10. **ADR documentation** — Architecture Decision Records for key design choices.

### ⚠️ Areas of Concern

1. **`server/evaluation.py` is 51 KB** — This is the largest Python source file in the project. Consider splitting into sub-modules (gates, normalization, rubrics, grading).
2. **`tools/llm/model_probe.py` is 63 KB** — Extremely large utility file. May benefit from decomposition.
3. **`tools/llm/llm_client.py` is 41 KB** — Large LLM client. The agentic-workflows-v2 has its own `models/client.py` — verify there's no duplicated logic.
4. **`agentic-v2-eval/chatlg.md` is 54 KB** — Appears to be a scratch/conversation log. Candidate for cleanup or `.gitignore`.
5. **Duplicate model IDs in `models.yaml`** — `gh:openai/gpt-4o` appears twice under `github_models`, and `gpt-4o` appears twice under `openai` provider (lines 96–109, 144–152).
6. **`engine/patterns/` is empty** — Placeholder directory for future Phase 2 strategies.
7. **Root-level scratch files** — `follow.txt` and `output.txt` at project root are likely temporary.
8. **`agents.yaml` references non-existent prompts** — Some agents reference prompt files (e.g., `prompts/explorer.md`, `prompts/cleanup.md`, `prompts/librarian.md`, `prompts/engineering_expert.md`, `prompts/lats_quality_controller.md`) that may not exist in the prompts directory.
9. **`.github/agents/` has a duplicate** — `prompt-agent.agent copy.md` should be cleaned up.

### 📊 Module Size Summary

| Module | Files | Largest File |
|--------|-------|-------------|
| Engine | 11 | `agent_resolver.py` (33.4 KB) |
| Server | 8 + 4 routes | `evaluation.py` (51.3 KB) |
| Workflows | 5 + 8 defs | `deep_research.yaml` (28.0 KB) |
| Agents | 8 + 4 impls | `base.py` (24.3 KB) |
| Models | 7 | `backends.py` (26.3 KB) |
| Tools (built-in) | 12 | `memory_ops.py` (12.5 KB) |
| LangChain | 9 | `runner.py` (21.0 KB) |
| Tests | 32 | `test_langchain_engine.py` (41.7 KB) |

---

## Recommendations

1. **Split `server/evaluation.py`** into `evaluation/gates.py`, `evaluation/normalization.py`, `evaluation/rubrics.py`, `evaluation/grading.py` — the 51 KB single-file is a maintenance risk.
2. **De-duplicate `models.yaml`** — Remove the duplicate `gpt-4o` entries under both `github_models` and `openai` providers.
3. **Clean up scratch files** — Remove or `.gitignore` `follow.txt`, `output.txt`, `chatlg.md`, and `prompt-agent.agent copy.md`.
4. **Verify prompt coverage** — Ensure every agent in `agents.yaml` has a corresponding prompt file in `prompts/`.
5. **Phase 1 integration readiness** — `integrations/base.py` exists but needs full implementation per P1-T001.
6. **Populate `engine/patterns/`** — Start implementing execution strategy patterns for Phase 2.
7. **Consider `tools/llm/` consolidation** — Evaluate whether `tools/llm/llm_client.py` and `agentic_v2/models/client.py` have overlapping responsibilities.

---

*Generated by the repo-documenter workflow on 2026-02-19.*
