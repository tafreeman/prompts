# LangChain Migration — Implementation Status

## Overview

Clean LangChain/LangGraph reimplementation of the agentic workflow engine.
The old custom `DAG`, `BaseAgent`, `StepExecutor`, and `ExecutionContext`
are replaced entirely with standard LangChain primitives.

**Branch:** `feature/langchain-migration`

---

## Architecture

```
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

| Component           | LangChain Primitive Used                     |
|---------------------|----------------------------------------------|
| State               | `TypedDict` with `Annotated` reducers        |
| Tools               | `@tool` decorator from `langchain_core`      |
| Agents              | `create_react_agent` from `langgraph.prebuilt`|
| Models              | `ChatOpenAI` from `langchain_openai`         |
| Graph               | `StateGraph` from `langgraph.graph`          |
| Edges               | `add_edge`, `add_conditional_edges`          |
| Checkpointing       | `MemorySaver` / `SqliteSaver` (ready)        |

### What's Custom (Thin Layers)

| Component           | Purpose                                      |
|---------------------|----------------------------------------------|
| `config.py`         | YAML parsing → dataclasses (no execution logic) |
| `expressions.py`    | `${...}` expression evaluation on state dict |
| `graph.py`          | Compiles YAML config into `StateGraph`       |
| `runner.py`         | Orchestrates load/validate/compile/run       |

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

**21 tests** (20 passed, 1 skipped without API key):

| Suite               | Tests | Notes                          |
|---------------------|-------|--------------------------------|
| Config Loader       | 8     | YAML parsing, inputs, steps    |
| Expressions         | 7     | Variables, conditions, `in`    |
| State               | 2     | Initial state creation         |
| Graph Compilation   | 4     | Compile, edge validation, run  |

---

## Phase 2: Remaining Work

### 2a. Run with Real LLM (requires API key)

- [ ] End-to-end `code_review` workflow execution
- [ ] Multi-step agent orchestration test
- [ ] Tool usage verification

### 2b. Persistence & Memory

- [ ] Wire `MemorySaver` / `SqliteSaver` checkpointer
- [ ] Resume interrupted workflows
- [ ] Cross-session memory

### 2c. UI Rearchitecture

- [ ] Update dashboard to work with new `WorkflowResult`
- [ ] Stream graph events to UI in real-time
- [ ] Graph visualization (LangGraph natively supports this)

### 2d. Evaluation Rearchitecture

- [ ] Port evaluation criteria resolution
- [ ] LangSmith integration for tracing
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
