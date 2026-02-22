# Active vs Legacy Tooling Map

> **Purpose:** Authoritative reference for which modules are active, deprecated, or superseded in `agentic-workflows-v2`.
>
> **Last updated:** 2026-02-20 (refactor alignment)

---

## Active Modules (agentic-workflows-v2/agentic_v2/)

### Server

| Module | Purpose | Status |
|--------|---------|--------|
| `server/app.py` | FastAPI app factory, CORS, route registration, SPA fallback | **Active** |
| `server/evaluation.py` | Backward-compatible orchestration surface for workflow scoring | **Active** |
| `server/evaluation_scoring.py` | Scoring engine internals: hard gates, rubric resolution, criterion floors, grading | **Active** |
| `server/datasets.py` | Dataset loading, adaptation, and compatibility matching | **Active** |
| `evaluation/normalization.py` | Canonical formula registry (binary, likert, lower-is-better, etc.) + reliability adjustment | **Active** (Phase 0) |
| `server/normalization.py` | Backward-compatible re-export of normalization functions | **Active** (compatibility shim) |
| `server/scoring_profiles.py` | Workflow-family scoring profiles A-D with default weights and extra gates | **Active** (Phase 0) |
| `server/models.py` | Pydantic request/response models for API | **Active** |
| `server/websocket.py` | WebSocket connection manager with replay buffer and SSE listener | **Active** |
| `server/routes/workflows.py` | Workflow API routes: run, evaluate, list datasets, SSE streaming | **Active** |
| `server/routes/agents.py` | Agent listing and info routes | **Active** |
| `server/routes/health.py` | Health check endpoint | **Active** |

### Engine

| Module | Purpose | Status |
|--------|---------|--------|
| `engine/dag_executor.py` | DAG-based step execution with dependency resolution | **Active** |
| `engine/expressions.py` | `${...}` expression evaluator for step I/O wiring | **Active** |
| `engine/executor.py` | Step executor (single step lifecycle) | **Active** |
| `engine/step.py` | Step definition and metadata | **Active** |
| `engine/step_state.py` | Step state management during execution | **Active** |
| `engine/context.py` | Execution context shared across steps | **Active** |
| `engine/dag.py` | DAG construction and validation | **Active** |
| `engine/pipeline.py` | Pipeline orchestration | **Active** |
| `engine/agent_resolver.py` | Agent resolution for steps | **Active** |
| `engine/patterns/` | Execution patterns (empty — future Phase 2 strategies) | **Placeholder** |

### Workflows

| Module | Purpose | Status |
|--------|---------|--------|
| `workflows/loader.py` | YAML workflow parsing: `WorkflowDefinition`, capabilities, evaluation, rubric criteria | **Active** |
| `workflows/runner.py` | Workflow runner: load → validate → execute → resolve outputs | **Active** |
| `workflows/run_logger.py` | Run log persistence (JSON per run) | **Active** |
| `workflows/definitions/code_review.yaml` | Code review DAG workflow (Profile B) | **Active** |
| `workflows/definitions/fullstack_generation.yaml` | Fullstack generation workflow (Profile A) | **Active** |
| `workflows/definitions/plan_implementation.yaml` | Iterative plan implementation | **Experimental** (hidden by default) |

### Integrations

| Module | Purpose | Status |
|--------|---------|--------|
| `integrations/langchain.py` | LangChain adapters (AgenticChatModel, AgenticTool, AgenticAgent) | **Active** (pre-contract; Phase 1 will normalize to base interfaces) |
| `integrations/__init__.py` | Integration package exports and registration | **Active** |

### Contracts

| Module | Purpose | Status |
|--------|---------|--------|
| `contracts/messages.py` | Core data models: `StepResult`, `WorkflowResult`, `StepStatus`, `AgentMessage` | **Active** |
| `contracts/schemas.py` | Schema utilities | **Active** |

### Other Active

| Module | Purpose | Status |
|--------|---------|--------|
| `agents/` | Built-in agent implementations (Coder, Reviewer, etc.) | **Active** |
| `cli/` | CLI entry point (`agentic` command) | **Active** |
| `config/` | Configuration management | **Active** |
| `models/` | Model routing and tier-based selection | **Active** |
| `tools/` | Built-in tools (memory, file ops, etc.) | **Active** |
| `prompts/` | Agent prompt templates | **Active** |

---

## Legacy / Deprecated / Superseded

### In this project

| Path | Status | Superseded By | Notes |
|------|--------|---------------|-------|
| Historical evaluation migration docs (removed) | **Historical** | — | Prior migration planning records were removed during cleanup |
| Historical implementation plan v1 docs (removed) | **Historical** | — | Prior phase 1 implementation records were removed during cleanup |
| Historical implementation plan v2 docs (removed) | **Historical** | — | Prior phase 2 implementation records were removed during cleanup |
| scripts/add_module_docstrings.py | **Removed** | — | No longer present in repository |

### In the parent repo (d:\source\prompts\)

| Path | Status | Superseded By | Notes |
|------|--------|---------------|-------|
| `tools/prompteval/` | **Active (separate concern)** | — | Prompt library evaluation; distinct from workflow evaluation |
| `agentic-v2-eval/` | **Active (separate package)** | — | Evaluation framework with sandbox, evaluators, and benchmark bridge; complements but does not replace `server/evaluation.py` |

---

## Modules Not Yet Created (Planned)

| Planned Module | Ticket | Phase |
|----------------|--------|-------|
| `engine/strategy.py` | P2-T001 | 2 |
| `engine/iterative.py` | P2-T002 | 2 |

---

## Test Files

| Test File | Covers | Status |
|-----------|--------|--------|
| `test_server_evaluation.py` | Scoring, hard gates, floors, rubrics, profiles, compatibility | **Active** (27 tests) |
| `test_normalization.py` | Formula registry, reliability adjustment | **Active** (9 tests) |
| `test_scoring_profiles.py` | Profile definitions and selection | **Active** (4 tests) |
| `test_server_workflow_routes.py` | SSE payloads, gate fields, 422 rejection, input validation | **Active** |
| `test_workflow_runner.py` | Runner execution, output resolution, metadata flags | **Active** |
| `test_workflow_loader.py` | YAML parsing, experimental filtering, capabilities | **Active** |
| `test_expressions.py` | Expression resolution, deep nesting, context merge | **Active** |
| `test_dag_executor.py` | DAG execution ordering and error handling | **Active** |
| `test_step_state.py` | Step state transitions | **Active** |
| `test_contracts.py` | Message/schema contracts | **Active** |
| `test_agents.py` | Agent implementations | **Active** |
| `test_cli.py` | CLI commands | **Active** |
| `test_dataset_workflows.py` | Dataset-workflow integration | **Active** |
| `test_engine.py` | Engine core | **Active** |
| `test_model_router.py` | Model routing | **Active** |
| `test_tier0.py` | Tier 0 structural checks | **Active** |
