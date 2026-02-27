# Architecture Analysis — `tafreeman/prompts` Monorepo

> Generated 2026-02-27 via multi-agent codebase analysis (code-explorer + architect).

---

## High-Level Overview

```
                         ┌─────────────┐
                         │  React UI   │
                         │ React Flow  │
                         └──────┬──────┘
                                │ HTTP + WebSocket
                         ┌──────▼──────┐
                         │   FastAPI   │
                         │   Server    │
                         └──┬─────┬────┘
                            │     │
              ┌─────────────▼┐   ┌▼──────────────┐
              │  LangChain   │   │    Native      │
              │  Engine      │   │    Engine       │
              │  (PRIMARY)   │   │  (SECONDARY)   │
              │              │   │                 │
              │ StateGraph   │   │ DAG + Kahn's    │
              │ ReAct Agents │   │ StepExecutor    │
              └──────┬───────┘   └───────┬────────┘
                     │                   │
                     └────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  SmartModelRouter   │
                    │  circuit breaker    │
                    │  health scoring     │
                    │  fallback chains    │
                    └─────────┬──────────┘
                              │
         ┌────────┬───────┬───┴───┬────────┬────────┐
         │Gemini  │OpenAI │Claude │Ollama  │GitHub  │
         │        │       │       │        │Models  │
         └────────┴───────┴───────┴────────┴────────┘

    YAML Workflows ──► Both Engines
    Eval Framework ──► Server (scores runs via LLM judge)
    tools/ package  ──► LLMClient shared by all packages
```

## Package Structure

| Package | Purpose | Build | Python |
|---------|---------|-------|--------|
| `agentic-workflows-v2/` | Main runtime — workflow execution, agents, server, UI | hatchling | >=3.11 |
| `agentic-v2-eval/` | Evaluation framework — scorers, evaluators, runners, reporters | setuptools | >=3.10 |
| `tools/` | Shared utilities — LLMClient, benchmarks, config, errors | setuptools | >=3.10 |

### Module Layout (agentic-workflows-v2)

```
agentic_v2/
  cli/            Typer CLI entry point (agentic command)
  langchain/      PRIMARY execution engine (LangGraph state machines)
  engine/         SECONDARY native DAG executor (Kahn's algorithm)
  agents/         BaseAgent hierarchy + built-in roles (Coder, Architect, Reviewer)
  models/         LLM tier routing, provider dispatch, SmartModelRouter
  server/         FastAPI + WebSocket + SSE streaming
  workflows/      YAML loader, run logger, definitions/
  contracts/      Pydantic v2 I/O schemas
  tools/          In-process tool registry
  integrations/   OpenTelemetry, LangChain tracing adapters
  config/         YAML defaults (currently empty module)
  prompts/        Markdown persona files loaded by agent factory
```

---

## Execution Engines

### LangChain Engine (Primary)

**Entry:** `langchain/runner.py` → `WorkflowRunner`

The primary execution path used by both CLI and API.

**Flow:**
1. `load_workflow_config(name)` → `WorkflowConfig` from YAML
2. `compile_workflow(config)` → LangGraph `StateGraph`
   - `_add_step_nodes()` — one closure per step (tier0=deterministic, tier1+=LLM)
   - `_wire_dependency_edges()` — `depends_on` → LangGraph edges
   - `_add_conditional_edges()` — `when` expressions, `loop_until` bounds
3. `graph.compile()` → cached `CompiledGraph`
4. `graph.ainvoke(state)` → LangGraph handles parallel execution

**Per-node execution:**
- Resolve `${...}` input expressions into context
- Build task description prompt
- Iterate model candidates (ordered fallback chain)
- `create_react_agent(model, tools, prompt)` → multi-turn ReAct loop
- Extract response → parse outputs → update state immutably

**Key files:**
- `langchain/graph.py` — Heart of the system, compiles YAML to LangGraph
- `langchain/runner.py` — WorkflowRunner facade
- `langchain/config.py` — YAML loader → WorkflowConfig
- `langchain/state.py` — WorkflowState TypedDict with reducers
- `langchain/models.py` — Provider dispatch + tier resolution
- `langchain/agents.py` — ReAct agent factory

### Native Engine (Secondary)

**Entry:** `engine/executor.py` → `WorkflowExecutor`

Independent DAG executor not wired to CLI/API. Available as a library.

**Flow:**
1. `DAGExecutor.execute()` runs Kahn's algorithm with dynamic scheduling
2. `asyncio.wait(tasks, return_when=FIRST_COMPLETED)` for parallelism
3. Concurrency limiting, cascade skip on failure, deadlock detection
4. Runtime isolation via `SubprocessRuntime` or `DockerRuntime`

**Key differences from LangChain engine:**

| Dimension | LangChain | Native |
|-----------|-----------|--------|
| Graph | LangGraph StateGraph | Custom DAG dataclass |
| Parallelism | LangGraph internal | asyncio + deque |
| LLM integration | LangChain BaseChatModel | SmartModelRouter + LLMClientWrapper |
| State model | WorkflowState TypedDict (immutable merges) | ExecutionContext (mutable) |
| Checkpointing | LangGraph MemorySaver | Not built-in |
| CLI/API wired | Yes | No |

---

## LLM Routing

### Two-Layer Architecture

**Layer 1: `langchain/models.py`** — Provider dispatch for LangChain engine
- Tier defaults (1=flash-lite, 2=flash, 3-5=flash-2.5)
- Model candidate resolution: step override → env var → probed default → fallback chain → GitHub backup
- Provider dispatch by prefix: `gemini:`, `openai:`, `claude:`, `gh:`, `ollama:`, `local:`, `lmstudio:`

**Layer 2: `models/smart_router.py`** — Adaptive routing for native engine + cross-engine health
- Circuit breaker: CLOSED → OPEN → HALF_OPEN per model
- Health-weighted selection: `success_rate * 0.6 + latency * 0.2 + recency * 0.2`
- Adaptive cooldown: `base * 1.5^consecutive_failures`, capped at 600s
- EMA-smoothed latency tracking + reservoir sampling for percentiles
- Atomic JSON persistence (temp-file-rename pattern)

### Model Tiers

| Tier | Purpose | Default |
|------|---------|---------|
| 0 | Deterministic (no LLM) | N/A |
| 1 | Fast/cheap | gemini-2.0-flash-lite |
| 2 | Balanced | gemini-2.0-flash |
| 3-5 | Strong reasoning | gemini-2.5-flash |

---

## Workflow System

### YAML Definition Language

10 workflow definitions under `workflows/definitions/`:
- `bug_resolution.yaml`
- `code_review.yaml`
- `deep_research.yaml`
- `fullstack_generation.yaml`
- `fullstack_generation_bounded_rereview.yaml`
- `multi_agent_codegen_e2e.yaml`
- `multi_agent_codegen_e2e_single_loop.yaml`
- `plan_implementation.yaml`
- `tdd_codegen_e2e.yaml`
- `test_deterministic.yaml`

Each step declares: `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`, `when`, `loop_until`, `loop_max`, `tools`, `model_override`.

### Expression Language

`${...}` expressions resolve data flow between steps:
- `${inputs.code_file}` — workflow input
- `${steps.parse_code.outputs.ast}` — step output reference
- `${context.some_key}` — context variable
- `${steps.review.outputs.review} != 'quick'` — conditional

### Agent Naming Convention

Agents follow `tier{N}_{role}` — e.g., `tier0_parser`, `tier1_linter`, `tier2_reviewer`. The role maps to a persona file under `prompts/{role}.md`.

---

## Server Layer

**Entry:** `server/app.py` → `create_app()`

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/run` | Execute workflow (background task) |
| GET | `/api/workflows` | List available workflows |
| GET | `/api/workflows/{name}/dag` | DAG for visualization |
| GET | `/api/runs` | List past runs |
| GET | `/api/runs/{run_id}/stream` | SSE event stream |
| WS | `/ws/execution/{run_id}` | WebSocket live events |

**Execution flow:**
1. POST `/api/run` → validate, generate `run_id`, launch background task
2. Background task streams via `ConnectionManager` (WebSocket + SSE)
3. Replay buffer (500 events) for late-connecting clients
4. If evaluation enabled: scores result, emits `evaluation_complete` event

---

## Evaluation Framework

### Scorer (`agentic-v2-eval/scorer.py`)

YAML rubrics → weighted scoring. Each criterion has `weight`, `min_value`, `max_value`. Score = weighted average of normalized criterion values.

### Evaluators

| Evaluator | Registered As | Scale | Purpose |
|-----------|---------------|-------|---------|
| LLMEvaluator | `"llm"` | 0.0–1.0 | LLM-as-judge with configurable prompts |
| PatternEvaluator | `"pattern"` | 0–30 | Agentic reasoning patterns (ReAct, CoVe) |
| StandardEvaluator | `"standard"` | 0–10 | 5-dimension prompt quality (clarity, effectiveness, structure, specificity, completeness) |
| QualityEvaluator | `"quality"` | 0.0–1.0 | Coherence, Fluency, Relevance, Groundedness, Similarity |

### Runners

| Runner | Execution | Concurrency |
|--------|-----------|-------------|
| BatchRunner | Synchronous | Sequential |
| StreamingRunner | Synchronous | Callback-based, no accumulation |
| AsyncStreamingRunner | Async | Bounded via `asyncio.Semaphore` |

### Reporters

JSON, Markdown (pipe-delimited tables), HTML (self-contained with color-coded scores).

---

## Shared Utilities (`tools/`)

### LLMClient

Static method `generate_text()` — all invocations are stateless. Dispatch by model name prefix:

| Prefix | Backend |
|--------|---------|
| `local:` | Local ONNX via onnxruntime-genai |
| `ollama:` | Ollama REST API |
| `windows-ai:` | Windows Copilot Runtime (NPU) |
| `azure-foundry:` | Azure Foundry REST |
| `azure-openai:` | Azure OpenAI SDK |
| `gh:` | GitHub Models via `gh` CLI |
| `openai:` | OpenAI SDK |
| `gemini:` | Google Generative AI SDK |
| `claude:` | Anthropic SDK |

Security gate: Remote providers disabled by default. Only `local:`, `gh:`, `windows-ai:`, `ollama:` allowed without `PROMPTEVAL_ALLOW_REMOTE=1`.

### Benchmark Definitions

8 benchmarks: SWE-Bench (2294), SWE-Bench Verified (500), SWE-Bench Lite (300), HumanEval (164), HumanEval+ (164), MBPP (974), MBPP Sanitized (427), CodeClash (100).

---

## UI (`agentic-workflows-v2/ui/`)

**Stack:** React 19 + Vite 6 + TypeScript 5.7 + @xyflow/react 12 + TanStack Query 5 + Tailwind CSS 3

**Routes:**
- `/` — Dashboard
- `/workflows` — Workflow list
- `/workflows/:name` — Detail + run trigger
- `/live/:runId` — Live execution with DAG visualization
- `/runs/:filename` — Run detail
- `/datasets` — Evaluation datasets
- `/evaluations` — Evaluated runs

**Dual update channels:**
- WebSocket for live in-progress runs (sub-second)
- Polling (5s) for completed run discovery

**DAG visualization features:**
- Optimistic running status (shows steps as running before backend confirms)
- Auto-pan to running step with user-interaction detection
- Edge coloring by traversal state
- Live elapsed timer per step (250ms refresh)

---

## Cross-Package Dependencies

```
ui/ (TypeScript)
    → agentic-workflows-v2 backend (HTTP + WebSocket)
        → tools.llm.LLMClient (via smart_router / langchain_adapter)
        → agentic-v2-eval (optional, for evaluation during runs)
            → tools.agents.benchmarks (lazy import for datasets)
            → tools.llm.LLMClient (via LLMClientAdapter)
```

**Key integration points:**
1. `LLMClientProtocol` — 6-line Protocol interface bridging eval to any LLM backend
2. `ExecutionEvent` — 11-variant discriminated union (WebSocket contract between backend and UI)
3. `DAGNode/DAGEdge` — Shared between backend serialization and frontend layout
4. `EvaluationResult` — Flows from scorer → WebSocket → UI run detail

---

## Architectural Scorecard

| Area | Rating | Notes |
|------|--------|-------|
| LLM Routing | Excellent | Circuit breaker, health scoring, adaptive cooldowns, fallback chains |
| DAG Execution | Strong | Kahn's algorithm, cycle detection, cascade skip, deadlock detection |
| Workflow DSL | Excellent | Declarative YAML, expression language, conditional execution |
| Defensive LLM Handling | Strong | Robust normalization of freeform LLM outputs |
| Observability | Good | Pluggable TraceAdapter (OTel, console, file, composite) |
| Contract Design | Good | Pydantic v2, computed fields — some immutability gaps |
| Test Coverage | Good | 37 test files, autouse fixtures, async support |
| Eval Integration | Strong | End-to-end from config → WebSocket → UI |

---

## Known Issues and Technical Debt

### 1. Dual Engine Maintenance Burden (HIGH)
Two parallel implementations of workflow compilation, expression evaluation, step execution, and output mapping. Bug fixes must be applied in two places. The native engine isn't wired to CLI/API. Two separate `WorkflowResult` classes exist in different modules.

**Recommendation:** Either deprecate one engine or extract shared core (expression eval, output mapping, state tracking).

### 2. Immutability Violations (HIGH)
Despite "Immutability First" being a non-negotiable rule:
- `TaskInput.with_context()` mutates in place
- `StepResult.mark_complete()` mutates
- `WorkflowResult.add_step()` mutates
- `ExecutionContext.set()` mutates
- `ConversationMemory.add()` mutates

**Recommendation:** Redesign with copy-on-write semantics or relax the principle for stateful execution objects.

### 3. Empty Configuration Module (MEDIUM)
`config/__init__.py` exports nothing. Configuration scattered across env vars, dataclass defaults, and hardcoded constants.

**Recommendation:** Introduce Pydantic `BaseSettings` class, validate at startup, inject via ServiceContainer.

### 4. Global Singleton Proliferation (MEDIUM)
6+ module-level singletons with `get_*()` / `reset_*()` patterns. The DI `ServiceContainer` exists but is underutilized.

**Recommendation:** Route all dependencies through `ServiceContainer`.

### 5. Silent Exception Swallowing (MEDIUM)
Multiple bare `except: pass` blocks in base.py, step.py, smart_router.py, client.py, context.py.

**Recommendation:** At minimum log at WARNING/DEBUG level.

### 6. Evaluation Logic in Server Layer (LOW)
Domain-heavy modules (`evaluation.py`, `judge.py`, `scoring_profiles.py`) live under `server/` when they should be in a dedicated `evaluation/` package.

### 7. Duplicated Tier Fallback Data (LOW)
`langchain/models.py` and `models/router.py` both define fallback chains that can diverge silently.

**Recommendation:** Single source of truth for fallback chains.

### 8. No Schema Versioning (LOW)
Despite the additive-only rule for contracts, no mechanism exists to version schemas, detect breaking changes, or migrate data.
