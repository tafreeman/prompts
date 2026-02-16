# LangChain Migration Plan & Feature Documentation

This document outlines the strategy to migrate the existing `agentic-workflows-v2` system to a **LangChain/LangGraph-based architecture**. The goal is to leverage LangChain's robust ecosystem (persistence, observability, established patterns) while maintaining the user-friendly **YAML-based workflow definition** system.

## 1. Migration Strategy

The migration will start in a new branch (e.g., `feature/langchain-migration`). The core approach is to replace the custom `DAG` and `BaseAgent` engine with **LangGraph**, using a "Bridge Module" to translate existing YAML configurations into LangGraph executables at runtime.

### Phase 1: Core Primitives (The "Bridge Module")

Develop the adapter layer that bridges existing YAMLs to LangGraph.

- **`State` Definition**: Define a typed state (e.g., `TypedDict` or Pydantic) that mirrors `ExecutionContext` and `ConversationMemory`.
- **`YamlGraphBuilder`**: A class that reads `WorkflowDefinition` objects (loaded by the existing `WorkflowLoader`) and programmatically constructs a `StateGraph`.

### Phase 2: Agent Isolation

Convert existing `BaseAgent` subclasses into LangGraph-compatible **Nodes**.

- Instead of managing their own loop, agents become functional nodes that receive `State`, call an LLM, and return `State` updates.
- Tools will be standardized to `langchain_core.tools.BaseTool`.

### Phase 3: Workflow Translation

Update the `runner.py` to execute the generated `StateGraph` instead of the custom `DAG`.

- Map `depends_on` → `graph.add_edge`.
- Map `when` expressions → `graph.add_conditional_edges`.
- Map `loop_until` → `graph.add_conditional_edges` (looping back to self).

### Phase 4: Persistence & Observability

- Replace `AGENTIC_MEMORY_PATH` with `langgraph.checkpoint.sqlite.SqliteSaver` or `MemorySaver`.
- Enable LangSmith tracing for free observability.

---

## 2. Feature Documentation (Proposed System)

The new system retains all high-level features but powers them with industry-standard infrastructure.

### 🌐 Declarative Workflows (YAML-Based)

**Feature**: Define complex multi-agent workflows in simple YAML files.
**How it works**:

- **Structure**: Continues to use `steps`, `inputs`, `outputs`, and `depends_on`.
- **Benefit**: No code required to wire agents together. The "Bridge Module" compiles YAML to a graph at runtime.

### 🧠 Unified State Management

**Feature**: Robust, typed state shared across all agents.
**Details**:

- Uses a central `AgentState` object containing:
  - `messages`: Full conversation history (replaces `ConversationMemory`).
  - `context`: Key-value store for workflow variables (replaces `ExecutionContext`).
  - `artifacts`: Generated files/code.

### 💾 Built-in Persistence (Time Travel)

**Feature**: Pause, resume, and "replay" workflows.
**Details**:

- Powered by **LangGraph Checkpointing**.
- Every step is saved. You can resume a failed workflow from the exact point of failure without re-running previous steps.

### 🔀 Dynamic conditional Logic

**Feature**: Logic gates and loops defined in YAML.
**Details**:

- **Conditions**: `when: "${context.score} < 5"` compiles to a conditional edge.
- **Loops**: `loop_until: "${context.is_valid}"` automatically creates a feedback loop in the graph.

### 🛠️ Adaptive Tooling

**Feature**: Agents receive tools dynamically based on their "Tier" or config.
**Details**:

- Tools are standard LangChain tools.
- The `Node` logic filters and binds usage-allowed tools to the LLM model just-in-time.

---

## 3. Implementation Blueprint: The "Bridge Module"

This module is the key "minor modification" that enables the migration without rewriting all YAMLs.

### `src/agentic_v2/langchain_bridge.py`

```python
import operator
from typing import Annotated, Any, TypedDict, Union, Sequence

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .workflows.loader import WorkflowDefinition, StepDefinition

# 1. Define the Global State
class WorkflowState(TypedDict):
    # Append-only message history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Shared context (overwrites keys)
    context: dict[str, Any]
    # Final outputs
    outputs: dict[str, Any]

class YamlGraphBuilder:
    """Compiles a YAML WorkflowDefinition into a specific LangGraph StateGraph."""
    
    def __init__(self, workflow_def: WorkflowDefinition):
        self.wf = workflow_def
        self.graph = StateGraph(WorkflowState)
        self.steps_map = {step.name: step for step in self.wf.dag.steps}

    def build(self):
        # 1. Add Nodes
        for step in self.wf.dag.steps:
            node_func = self._create_step_node(step)
            self.graph.add_node(step.name, node_func)

        # 2. Add Edges
        for step in self.wf.dag.steps:
            if not step.depends_on:
                # If no dependencies, it's a start node (or dependent on separate start logic)
                # In strict DAG, we might need a dummy start, but here we can rely on flow.
                # Simplification: If it's a root step, add edge from START? 
                # (Logic depends on specific topological sort or explicit entry)
                pass
            
            # Add standard edges
            # Note: LangGraph infers flow, but for explicit DAGs we draw edges.
            # If Step B depends on Step A, we add Edge A -> B
            for dep in step.depends_on:
                self.graph.add_edge(dep, step.name)

            # 3. Handle Conditional Edges (Loops & When)
            if step.loop_until:
                 self.graph.add_conditional_edges(
                    step.name,
                    self._make_condition(step.loop_until),
                    {True: "next_node", False: step.name} # Simplified logic
                 )

        self.graph.set_entry_point(self.wf.dag.steps[0].name) # Simplified entry
        return self.graph.compile()

    def _create_step_node(self, step: StepDefinition):
        """Factory to create a runnable node function from a step definition."""
        async def _node(state: WorkflowState):
            # Resolve Agent based on step.metadata['agent']
            # Execute Agent Logic (LLM Call)
            # Return State Update
            return {"context": {"last_step": step.name}}
        return _node

    def _make_condition(self, expr_str):
        """Converts string expression to callable."""
        def _cond(state):
            # Evaluate expr_str against state['context']
            return True
        return _cond
```

### Key Mapping Logic

| Concept | Current System | New LangGraph System |
| :--- | :--- | :--- |
| **Agent** | Class inheriting `BaseAgent` | `Annotated[Runnable, "agent"]` (Node) |
| **Memory** | `ConversationMemory` (Manual) | `state["messages"]` (Managed) |
| **DAG** | Custom `DAG` class | `StateGraph` |
| **Step** | `StepDefinition` | Graph Node |
| **Edge** | `depends_on` list | `graph.add_edge()` |
| **Loop** | Custom runner logic | Cyclic Graph Edge |

## 4. Next Steps for User

1. **Approval**: Confirm this plan aligns with your vision.
2. **Repo Setup**: Create the `feature/langchain-migration` branch.
3. **Dependency Install**: Add `langchain`, `langgraph`, `langchain-openai`.
4. **Prototype**: Implement the `YamlGraphBuilder` to validate one simple workflow.
