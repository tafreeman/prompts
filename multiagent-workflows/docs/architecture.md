# Architecture Overview

This document describes the high-level architecture of the multi-agent workflow system.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLI / Python API                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Workflow Engine                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Step        │  │ Context     │  │ Evaluation  │              │
│  │ Orchestrator│  │ Manager     │  │ Integration │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    Agents     │    │    Logger     │    │   Evaluator   │
│ ┌───────────┐ │    │ ┌───────────┐ │    │ ┌───────────┐ │
│ │ Architect │ │    │ │ Workflow  │ │    │ │ Scorer    │ │
│ │ Coder     │ │    │ │ Step      │ │    │ │ Comparator│ │
│ │ Reviewer  │ │    │ │ Agent     │ │    │ │ Reporter  │ │
│ │ Tester    │ │    │ │ Model     │ │    │ └───────────┘ │
│ └───────────┘ │    │ │ Tool      │ │    └───────────────┘
└───────────────┘    │ └───────────┘ │
        │            └───────────────┘
        ▼                    │
┌───────────────────────────────────────────────────────────────┐
│                      Model Manager                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Model       │  │ Fallback    │  │ Cost        │            │
│  │ Routing     │  │ Strategy    │  │ Tracking    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└───────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Local ONNX   │    │    Ollama     │    │  Cloud APIs   │
│  (NPU/CPU)    │    │   (Local)     │    │  (GitHub,etc) │
└───────────────┘    └───────────────┘    └───────────────┘
```

## Core Components

### Workflow Engine

The central orchestrator that:

- Loads workflow definitions from YAML
- Manages step-by-step execution
- Passes context between steps
- Handles parallel execution where possible
- Integrates with evaluation framework

```python
class WorkflowEngine:
    async def execute_workflow(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
    ) -> WorkflowResult:
        ...
```

### Model Manager

Unified interface for all model providers:

- Automatic fallback (premium → mid-tier → local)
- Task-based routing
- Comprehensive logging
- Cost tracking

```python
class ModelManager:
    async def generate(
        self,
        model_id: str,
        prompt: str,
        **params
    ) -> GenerationResult:
        ...
```

### Agent Base

Foundation for all agents with:

- Built-in logging hooks
- Tool invocation support
- Retry logic with fallback
- Structured output handling

```python
class AgentBase:
    async def execute(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> AgentResult:
        ...
```

### Verbose Logger

Hierarchical logging system:

- 5 levels: Workflow → Step → Agent → Model → Tool
- JSON export for analysis
- Markdown export for review
- Metric aggregation

### Evaluator

Rubric-based evaluation:

- Category-weighted scoring
- Golden output comparison
- Report generation
- Baseline comparison

## Data Flow

### Execution Flow

1. **Input Processing**: Workflow engine receives inputs
2. **Step Scheduling**: Steps are scheduled based on dependencies
3. **Agent Execution**: Each step creates and runs an agent
4. **Context Propagation**: Agent outputs are added to context
5. **Evaluation**: Final output is scored against rubrics
6. **Logging**: All events are captured hierarchically

### Context Structure

```python
context = {
    "inputs": {  # Original workflow inputs
        "requirements": "...",
    },
    "artifacts": {  # Outputs from completed steps
        "architecture_design": {...},
        "api_spec": {...},
    },
    "config": {...},  # Runtime configuration
    "workflow_id": "wf-abc123",
}
```

## Configuration

### YAML Configuration Files

- `config/models.yaml`: Model providers and routing
- `config/workflows.yaml`: Workflow definitions
- `config/agents.yaml`: Agent configurations
- `config/rubrics.yaml`: Scoring rubrics
- `config/evaluation.yaml`: Evaluation settings

### Model Routing Strategy

```yaml
routing:
  code_gen:
    preferred: ["gh:gpt-4o", "ollama:qwen2.5-coder:14b"]
    fallback: ["local:phi4mini"]
```

## Integration Points

### Repository Tools Integration

- Imports from `tools/llm/llm_client.py` when available
- Falls back to direct API calls if not available
- Compatible with `tools/prompteval/` patterns

### Extensibility

1. **Custom Agents**: Extend `AgentBase`
2. **Custom Workflows**: Extend `BaseWorkflow` or define in YAML
3. **Custom Tools**: Register with `ToolRegistry`
4. **Custom Evaluators**: Extend `WorkflowEvaluator`
