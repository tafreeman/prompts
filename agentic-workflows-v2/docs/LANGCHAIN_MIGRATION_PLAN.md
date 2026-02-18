# LangChain Migration — Implementation Status

## Overview

Clean LangChain/LangGraph reimplementation of the agentic workflow engine.
The old custom `DAG`, `BaseAgent`, `StepExecutor`, and `ExecutionContext`
are replaced entirely with standard LangChain primitives.

**Branch:** `feature/langchain-migration`

---

## Architecture

```text
agentic_v2/langchain/
├── __init__.py          # Package exports (WorkflowRunner, WorkflowConfig)
├── state.py             # WorkflowState TypedDict (LangGraph state schema)
├── config.py            # YAML config loader → pure dataclasses
├── tools.py             # @tool decorated functions (file, code, shell, etc.)
├── agents.py            # create_react_agent factory (tier-based model selection)
├── expressions.py       # ${...} expression evaluator (conditions / variable refs)
├── graph.py             # StateGraph compiler (YAML config → runnable graph)
└── runner.py            # WorkflowRunner (top-level API: load → validate → run)
```

### What's Standard LangChain

| Component     | LangChain Primitive Used                          |
|:--------------|:--------------------------------------------------|
| State         | `TypedDict` with `Annotated` reducers             |
| Tools         | `@tool` decorator from `langchain_core`           |
| Agents        | `create_react_agent` from `langgraph.prebuilt`    |
| Models        | `ChatOpenAI` from `langchain_openai`              |
| Graph         | `StateGraph` from `langgraph.graph`               |
| Edges         | `add_edge`, `add_conditional_edges`               |
| Checkpointing | `MemorySaver` / `SqliteSaver` (ready)             |

### What's Custom (Thin Layers)

| Component        | Purpose                                           |
|:-----------------|:--------------------------------------------------|
| `config.py`      | YAML parsing → dataclasses (no execution logic)   |
| `expressions.py` | `${...}` expression evaluation on state dict      |
| `graph.py`       | Compiles YAML config into `StateGraph`            |
| `runner.py`      | Orchestrates load/validate/compile/run            |

---

## Module Details

### `state.py` — WorkflowState

```python
class WorkflowState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]  # append-only
    context: dict[str, Any]      # overwrite merge
    inputs: dict[str, Any]       # immutable after init
    outputs: dict[str, Any]      # resolved at end
    steps: dict[str, dict]       # per-step status + outputs
    current_step: str
    errors: Annotated[list[str], operator.add]  # append-only
```

### `config.py` — YAML Loader

Pure-data parsing:

- `WorkflowConfig` → `StepConfig`, `InputConfig`, `OutputConfig`
- `EvaluationConfig` → `CriterionConfig`
- Uses existing YAML files unchanged

### `tools.py` — LangChain Tools

Standard `@tool` decorated functions:

- `file_read`, `file_write`, `file_list`
- `code_analyze`
- `shell_run`
- `search_files`
- `context_store`
- `http_get`
- Tier-based tool sets: `get_tools_for_tier(tier)`

### `agents.py` — Agent Factory

- Parses `tier{N}_{role}` agent names
- Maps tiers to models (`gpt-4o-mini`, `gpt-4o`, etc.)
- Loads system prompts from `prompts/{role}.md`
- Creates `create_react_agent(model, tools, prompt)`
- Env var overrides: `AGENTIC_MODEL_TIER_{N}`

### `graph.py` — Graph Compiler

Transforms `WorkflowConfig` → compiled `StateGraph`:

- **Tier 0 nodes**: Deterministic functions (no LLM)
- **Tier 1+ nodes**: ReAct agent wrappers
- **Edges**: `depends_on` → `add_edge`
- **Conditional edges**: `when` → `add_conditional_edges`
- **Loop edges**: `loop_until` → self-edge with iteration counter
- **Auto-wiring**: `START → root steps`, `terminal steps → END`

### `runner.py` — WorkflowRunner API

```python
runner = WorkflowRunner()
result = runner.invoke("code_review", code_file="main.py")
result = await runner.run("code_review", code_file="main.py")
```

- Input validation with defaults and enum checks
- Graph caching (compile once, run many)
- Output resolution from final state
- `WorkflowResult` with status, outputs, steps, errors, timing

---

## Test Coverage

**54 tests** (50 passed, 4 skipped in focused LangChain suite):

- Config Loader (8): YAML parsing, inputs, steps
- Expressions (7): variables, conditions, `in`
- State (2): initial state creation
- Graph Compilation (4): compile, edge validation, run
- Runner Integration (10+): checkpointer + thread config + stream + resume + tracing hooks

---

## Phase 2: Execution Plan (Detailed)

This section is the concrete migration backlog and acceptance contract.

### Phase 2a. Real LLM Execution Parity

**Goal:** prove end-to-end production behavior with real model calls.

- [ ] Add deterministic smoke harness for `code_review` with golden fixtures.
- [ ] Add multi-step orchestration test with at least one tool call in each tier.
- [ ] Add output-schema validation for each step output payload.

#### Acceptance criteria (2a)

- Tiered workflow runs complete on a real model without manual patching.
- Step outputs parse as valid JSON for declared output keys.
- Failures are captured in `errors` and surfaced in `WorkflowResult.status`.

### Phase 2b. Persistence & Resume

**Goal:** make checkpointing operational, not just declared in docs.

- [x] Compile LangGraph with optional `checkpointer` when provided.
- [x] Support `thread_id` via LangGraph `configurable.thread_id` in `invoke` / `run`.
- [x] Add `stream` / `astream` APIs with the same thread-aware runtime config path.
- [x] Add checkpoint state read/inspect helper methods (debug + recovery).
- [x] Add `resume(...)` API for thread-based continuation.
- [ ] Add interrupted-run resume tests using `MemorySaver` and `SqliteSaver`.

#### Acceptance criteria (2b)

- Same `thread_id` preserves execution thread state across invocations.
- Streaming and non-streaming execution paths use identical checkpoint keys.
- Persistence tests pass for in-memory and SQLite checkpointers.

### Phase 2c. UI Rearchitecture

**Goal:** bind dashboard/live views to `WorkflowResult` + graph events.

- [ ] Define stable UI event contract for step start/complete/error.
- [ ] Stream graph events into UI timeline.
- [ ] Add graph visualization view backed by LangGraph topology.

#### Acceptance criteria (2c)

- UI can render full step timeline without old DAG runtime adapters.
- Real-time run view works for both success and failure paths.

### Phase 2d. Evaluation Rearchitecture

**Goal:** move eval/tracing to the LangChain-native runner.

- [ ] Port evaluation criteria resolution to consume new step output shape.
- [x] Integrate LangSmith tracing adapter.
- [ ] Add benchmark harness entrypoints using `WorkflowRunner`.

#### Acceptance criteria (2d)

- Existing rubric criteria can score LangChain runs without compatibility shims.
- Traces are queryable per workflow + run/thread id.

### Phase 2e. Custom/Multi-Agent Extensions

**Goal:** keep flexibility where `create_react_agent` is insufficient.

- [ ] Inventory agents needing custom wrappers.
- [ ] Add supervisor/swarm reference patterns.
- [ ] Add human-in-the-loop interrupt/resume examples.

#### Acceptance criteria (2e)

- Non-ReAct agents run through the same state + output contracts.
- HITL flow can pause and resume in a persistent thread.

---

## Phase 2: Remaining Work (Legacy Checklist)

### 2a. Run with Real LLM (requires API key)

- [ ] End-to-end `code_review` workflow execution
- [ ] Multi-step agent orchestration test
- [ ] Tool usage verification

### 2b. Persistence & Memory

- [x] Wire `MemorySaver` / `SqliteSaver` checkpointer (compile + thread config plumbing)
- [x] Add resume/checkpoint-inspection APIs on `WorkflowRunner`
- [ ] Validate interrupted-run resume behavior with concrete `MemorySaver`/`SqliteSaver` integration tests
- [ ] Cross-session memory

### 2c. UI Rearchitecture

- [ ] Update dashboard to work with new `WorkflowResult`
- [ ] Stream graph events to UI in real-time
- [ ] Graph visualization (LangGraph natively supports this)

### 2d. Evaluation Rearchitecture

- [ ] Port evaluation criteria resolution
- [x] LangSmith integration for tracing
- [ ] Benchmark harness using new runner

### 2e. Custom Agents

- [ ] Port any agents that don't fit `create_react_agent`
- [ ] Multi-agent collaboration patterns (supervisor, swarm)
- [ ] Human-in-the-loop (LangGraph interrupts)

---

## Dependencies Added

```toml
# Core (required)
"langchain-core>=0.3"
"langgraph>=0.2"

# Optional [langchain] extra
"langchain>=0.3"
"langchain-openai>=0.2"
"langgraph-checkpoint-sqlite>=2.0"
```
