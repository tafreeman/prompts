# Agentic Workflows v2 - Implementation Prompts

**Purpose:** Ready-to-use prompts with full context for each implementation phase  
**Companion to:** `agentic-workflows-v2-phased-implementation.md`  
**Date:** February 2, 2026

Each prompt below is self-contained with all context needed. Copy and use directly.

---

## How to Use These Prompts

1. **Select the phase** you're working on
2. **Copy the entire prompt** (including context blocks)
3. **Send to LLM** (gh:meta/llama-3.3-70b-instruct recommended for tier 3 tasks)
4. **Review output** and apply to codebase
5. **Run validation** before moving to next phase

**Model Recommendations:**
- Phase 0-1: Any model (tier 1-2)
- Phase 2-4: Medium model (tier 2) - `gh:phi-4` or `ollama:qwen2.5-coder:14b`
- Phase 5-6: Large model (tier 3) - `gh:meta/llama-3.3-70b-instruct`

---

## Phase 0: Foundation Setup

### Prompt 0.1: Create Package Structure

```
<TASK>
Create the initial package structure for agentic-workflows-v2, an independent Python module for tiered multi-model agentic workflows.
</TASK>

<CONTEXT>
Location: d:\source\prompts\agentic-workflows-v2\
This is a NEW independent package - do not modify existing multiagent-workflows/.
The package uses Pydantic v2, httpx, Jinja2, and jmespath.
Python version: 3.11+
</CONTEXT>

<REQUIRED_STRUCTURE>
agentic-workflows-v2/
├── pyproject.toml
├── README.md
├── src/
│   └── agentic_v2/
│       ├── __init__.py          # Version, exports
│       ├── contracts/
│       │   ├── __init__.py
│       │   ├── messages.py      # AgentMessage, StepResult
│       │   └── schemas.py       # Base schemas
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py          # BaseTool ABC
│       │   ├── registry.py      # Tool registry
│       │   └── builtin/
│       │       ├── __init__.py
│       │       ├── file_ops.py  # Tier 0 file operations
│       │       └── transform.py # Tier 0 transforms
│       ├── models/
│       │   ├── __init__.py
│       │   ├── router.py        # Basic tier routing
│       │   └── client.py        # LLM client wrapper
│       ├── engine/
│       │   ├── __init__.py
│       │   ├── executor.py
│       │   └── context.py
│       └── cli/
│           └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_tools.py
</REQUIRED_STRUCTURE>

<OUTPUT_FORMAT>
For each file, output:
### filename.py
```python
# Full implementation
```

Start with pyproject.toml, then __init__.py files, then implementation files.
</OUTPUT_FORMAT>
```

### Prompt 0.2: Implement Tier 0 Tools (No LLM)

```
<TASK>
Implement Tier 0 tools that require NO language model - pure Python operations.
These tools handle file operations, JSON transforms, and template rendering.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/tools/builtin/
These tools are deterministic and do not call any LLM.
</CONTEXT>

<BASE_TOOL_INTERFACE>
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ToolResult:
    success: bool
    output: Any
    error: Optional[str] = None

class BaseTool(ABC):
    """Base class for all tools."""
    name: str
    description: str
    tier: int = 0  # Model tier required (0 = no LLM)
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters."""
        pass
</BASE_TOOL_INTERFACE>

<REQUIRED_TOOLS>
file_ops.py:
- FileCopyTool: Copy file from source to destination
- FileMoveTool: Move/rename a file  
- FileDeleteTool: Delete a file
- DirectoryCreateTool: Create directory (mkdir -p)
- FileReadTool: Read file contents
- FileWriteTool: Write content to file

transform.py:
- JsonTransformTool: Apply jmespath query to JSON data
- TemplateRenderTool: Render Jinja2 template with variables
- ConfigMergeTool: Deep merge multiple config dicts
- YamlLoadTool: Load YAML file to dict
- YamlDumpTool: Dump dict to YAML string
</REQUIRED_TOOLS>

<OUTPUT_FORMAT>
### tools/base.py
```python
# BaseTool implementation
```

### tools/builtin/file_ops.py
```python
# All file operation tools
```

### tools/builtin/transform.py
```python
# All transform tools
```

### tools/registry.py
```python
# Tool registry with auto-discovery
```

Include docstrings, type hints, and error handling.
</OUTPUT_FORMAT>
```

---

## Phase 1: Contracts & Model Router

### Prompt 1.1: Pydantic Contracts

```
<TASK>
Create Pydantic v2 contracts for the agentic workflow system.
These define the data structures for messages, results, and agent I/O.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/contracts/
Using Pydantic v2 (BaseModel, Field, model_validator)
</CONTEXT>

<REQUIRED_CONTRACTS>
messages.py:
- AgentMessage: Communication between agents
  - role: Literal["user", "assistant", "system", "tool"]
  - content: str
  - metadata: dict[str, Any]
  - timestamp: datetime
  
- StepResult: Result of executing a workflow step
  - step_id: str
  - status: Literal["success", "failure", "skipped"]
  - output: Any
  - error: Optional[str]
  - duration_ms: float
  - model_used: Optional[str]
  - tier: int
  
- WorkflowResult: Final workflow output
  - workflow_id: str
  - status: Literal["completed", "failed", "partial"]
  - steps: list[StepResult]
  - final_output: Any
  - total_duration_ms: float
  - models_used: dict[int, list[str]]  # tier -> models

schemas.py:
- TaskInput: Base input for any task
- TaskOutput: Base output for any task
- CodeGenerationInput/Output
- CodeReviewInput/Output
- TestGenerationInput/Output
- EvaluationInput/Output
</REQUIRED_CONTRACTS>

<OUTPUT_FORMAT>
### contracts/messages.py
```python
# Message and result contracts
```

### contracts/schemas.py
```python
# Task input/output schemas
```

### contracts/__init__.py
```python
# Exports
```

Use Pydantic v2 syntax with Field descriptions.
</OUTPUT_FORMAT>
```

### Prompt 1.2: Model Router with Adaptive Learning

```
<TASK>
Implement the model routing system with adaptive learning and fallback.
This routes tasks to appropriate model tiers and handles failures gracefully.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/models/
Uses tools/llm/llm_client.py from parent repo for actual LLM calls.

Model Tiers:
- Tier 0: No LLM (pure code)
- Tier 1: Small (1-3B) - ollama:phi3:mini, ollama:qwen2.5:1.5b
- Tier 2: Medium (7-14B) - ollama:qwen2.5-coder:14b, gh:phi-4
- Tier 3: Large (32B+/cloud) - gh:meta/llama-3.3-70b-instruct, gh:gpt-4o-mini
</CONTEXT>

<REQUIRED_COMPONENTS>
model_stats.py:
- ModelStats dataclass tracking:
  - success_count, failure_count, rate_limit_count
  - total_latency_ms
  - last_failure, cooldown_until
  - Properties: success_rate, avg_latency_ms

router.py:
- ModelRouter class with:
  - get_model_for_tier(tier: int) -> str
  - get_model_for_task(task: str) -> str
  - _first_available(models: list[str]) -> str

smart_router.py:
- SmartModelRouter extends ModelRouter:
  - record_success(model, latency_ms)
  - record_failure(model, error_type)
  - _apply_cooldown(model, duration_seconds)
  - _is_in_cooldown(model) -> bool
  - _get_fallback_model(tier) -> str
  - save_stats(path) / load_stats(path)

Fallback Logic:
- 3 failures in 1 min → 30 second cooldown
- 5 rate limits → 2 minute cooldown
- Provider outage → 5 minute cooldown, try local

client.py:
- LLMClientWrapper that imports from tools.llm.llm_client
- Handles tier-based model selection
</REQUIRED_COMPONENTS>

<OUTPUT_FORMAT>
### models/model_stats.py
```python
# ModelStats dataclass
```

### models/router.py
```python
# Basic ModelRouter
```

### models/smart_router.py
```python
# SmartModelRouter with adaptive learning
```

### models/client.py
```python
# LLM client wrapper
```
</OUTPUT_FORMAT>
```

---

## Phase 2: Engine & Executor

### Prompt 2.1: Execution Engine

```
<TASK>
Implement the core execution engine that runs workflow steps with tier-aware model routing.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/engine/
The engine executes steps, manages context, and routes to appropriate models.
</CONTEXT>

<DEPENDENCIES>
from agentic_v2.contracts.messages import StepResult, WorkflowResult
from agentic_v2.contracts.schemas import TaskInput, TaskOutput
from agentic_v2.models.smart_router import SmartModelRouter
from agentic_v2.tools.registry import ToolRegistry
</DEPENDENCIES>

<REQUIRED_COMPONENTS>
context.py:
- StepContext: Context for a single step
  - step_id: str
  - variables: dict[str, Any]
  - previous_results: dict[str, StepResult]
  - current_model: str
  - current_tier: int
  
- WorkflowContext: Context for entire workflow
  - workflow_id: str
  - steps: dict[str, StepContext]
  - global_variables: dict[str, Any]
  - start_time: datetime
  - add_result(step_id, result)
  - get_variable(name, default=None)
  - resolve_reference(ref: str) -> Any  # e.g., "${step1.output}"

executor.py:
- StepExecutor: Executes individual steps
  - execute_step(step, context) -> StepResult
  - _resolve_inputs(step, context) -> dict
  - _call_tool(tool_name, inputs) -> Any
  - _call_agent(agent_name, inputs, tier) -> Any

state.py:
- StateManager: Checkpoint and recovery
  - save_checkpoint(workflow_id, context)
  - load_checkpoint(workflow_id) -> WorkflowContext
  - list_checkpoints() -> list[str]
</REQUIRED_COMPONENTS>

<OUTPUT_FORMAT>
### engine/context.py
```python
# Context management
```

### engine/executor.py
```python
# Step execution
```

### engine/state.py
```python
# Checkpointing
```
</OUTPUT_FORMAT>
```

### Prompt 2.2: Base Agent System

```
<TASK>
Implement the base agent system that all specialized agents inherit from.
Agents are tier-aware and use the model router for LLM calls.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/agents/
Agents wrap LLM calls with specific prompts and output parsing.
</CONTEXT>

<REQUIRED_COMPONENTS>
base.py:
- AgentConfig (Pydantic model):
  - id: str
  - name: str
  - model_tier: int = 2
  - system_prompt: str
  - tools: list[str] = []
  - max_tokens: int = 4096
  - temperature: float = 0.7

- BaseAgent (ABC):
  - __init__(config, router, llm_client)
  - config: AgentConfig
  - router: SmartModelRouter
  - llm: LLMClientWrapper
  - @abstractmethod execute(input, context) -> output
  - _build_prompt(input) -> str
  - _parse_response(response) -> Any
  - _call_llm(prompt, tier=None) -> str

registry.py:
- AgentRegistry:
  - register(agent_class)
  - get(agent_id) -> BaseAgent
  - list_agents() -> list[str]
  - create_agent(agent_id, config) -> BaseAgent
</REQUIRED_COMPONENTS>

<OUTPUT_FORMAT>
### agents/base.py
```python
# BaseAgent and AgentConfig
```

### agents/registry.py
```python
# Agent registry
```

### agents/__init__.py
```python
# Exports
```
</OUTPUT_FORMAT>
```

---

## Phase 3: Specialized Agents

### Prompt 3.1: Tier 2 Agents (Code Generation)

```
<TASK>
Implement Tier 2 agents for code generation, review, and testing.
These use medium models (7-14B parameters).
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/agents/implementations/
Tier 2 models: ollama:qwen2.5-coder:14b, gh:phi-4
</CONTEXT>

<BASE_IMPORTS>
from agentic_v2.agents.base import BaseAgent, AgentConfig
from agentic_v2.contracts.schemas import (
    CodeGenerationInput, CodeGenerationOutput,
    CodeReviewInput, CodeReviewOutput,
    TestGenerationInput, TestGenerationOutput
)
from agentic_v2.engine.context import StepContext
</BASE_IMPORTS>

<REQUIRED_AGENTS>
coder.py - CoderAgent (tier=2):
- Input: CodeGenerationInput (task, language, context, constraints)
- Output: CodeGenerationOutput (files: list[CodeFile], explanation)
- System prompt: You are an expert programmer...
- Parse code blocks from response

reviewer.py - ReviewerAgent (tier=2):
- Input: CodeReviewInput (code, language, focus_areas)
- Output: CodeReviewOutput (issues: list[Issue], suggestions, score)
- System prompt: You are a code reviewer...
- Parse structured review from response

tester.py - TesterAgent (tier=2):
- Input: TestGenerationInput (code, language, framework)
- Output: TestGenerationOutput (tests: list[TestCase], coverage_estimate)
- System prompt: You are a test engineer...
- Generate pytest/unittest tests
</REQUIRED_AGENTS>

<OUTPUT_FORMAT>
### agents/implementations/coder.py
```python
# CoderAgent implementation with prompts
```

### agents/implementations/reviewer.py
```python
# ReviewerAgent implementation with prompts
```

### agents/implementations/tester.py
```python
# TesterAgent implementation with prompts
```

Include the full system prompts embedded in each agent.
</OUTPUT_FORMAT>
```

### Prompt 3.2: Tier 3 Agents (Reasoning)

```
<TASK>
Implement Tier 3 agents for architecture design and quality evaluation.
These REQUIRE large models (32B+ or cloud) for complex reasoning.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/agents/implementations/
Tier 3 models: gh:meta/llama-3.3-70b-instruct, gh:gpt-4o-mini
</CONTEXT>

<REQUIRED_AGENTS>
architect.py - ArchitectAgent (tier=3):
- Input: ArchitectInput (requirements, constraints, context)
- Output: ArchitectOutput (design, components, decisions, tradeoffs)
- Complex reasoning about system design
- Technology selection and trade-off analysis

evaluator.py - EvaluatorAgent (tier=3):
- Input: EvaluatorInput (artifact, criteria, rubric)
- Output: EvaluatorOutput (score, feedback, pass/fail, improvements)
- Quality scoring with detailed feedback
- Used in self-refinement loops

orchestrator_agent.py - OrchestratorAgent (tier=3):
- Input: OrchestratorInput (goal, available_agents, constraints)
- Output: OrchestratorOutput (plan: list[PlannedStep], reasoning)
- Breaks down complex tasks into agent assignments
- Determines execution order and dependencies

synthesizer.py - SynthesizerAgent (tier=3):
- Input: SynthesizerInput (artifacts: list, goal)
- Output: SynthesizerOutput (combined_result, integration_notes)
- Combines multiple outputs into coherent whole
</REQUIRED_AGENTS>

<OUTPUT_FORMAT>
### agents/implementations/architect.py
```python
# ArchitectAgent with full system prompt
```

### agents/implementations/evaluator.py
```python
# EvaluatorAgent with rubric-based evaluation
```

### agents/implementations/orchestrator_agent.py
```python
# OrchestratorAgent for task planning
```

### agents/implementations/synthesizer.py
```python
# SynthesizerAgent for combining outputs
```

Include detailed system prompts that leverage the model's reasoning capabilities.
</OUTPUT_FORMAT>
```

---

## Phase 4: DAG Workflows & Dependency Resolution

### Prompt 4.0: DAG Workflow Engine

```
<TASK>
Implement DAG-based workflow execution that achieves maximum parallelism from dependency graphs.
This replaces/subsumes the simpler Pipeline execution with true dynamic scheduling.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/engine/
Current Pipeline uses sync barriers (ParallelGroup). DAG execution has no artificial barriers.
Existing StepDefinition already has depends_on, when, unless fields.
</CONTEXT>

<REQUIRED_COMPONENTS>
dag.py:
- DAG class:
  - __init__(name: str)
  - add(step: StepDefinition) -> DAG  # Fluent API
  - validate() -> None  # Raises on cycle or missing dependency
  - _detect_cycles() -> bool  # DFS with coloring (WHITE/GRAY/BLACK)
  - _build_adjacency_list() -> dict[str, list[str]]
  - get_execution_order() -> list[str]  # Topological sort (Kahn's algorithm)
  - get_ready_steps(completed: set[str]) -> list[str]  # Steps with met dependencies

- Exceptions:
  - CycleDetectedError(cycle_path: list[str])
  - MissingDependencyError(step: str, missing_dep: str)

dag_executor.py:
- DAGExecutor:
  - execute(dag: DAG, ctx: ExecutionContext, max_concurrency: int = 10) -> WorkflowResult
  - Uses asyncio.Queue for ready steps
  - Uses asyncio.Semaphore for concurrency limiting
  - Tracks in_degree (pending dependency count) per step
  - When step completes, decrements dependents' in_degree
  - Schedules steps immediately when in_degree reaches 0
  - No sync barriers - pure BFS-style dynamic scheduling

expressions.py:
- ExpressionEvaluator:
  - evaluate(expr: str, ctx: ExecutionContext) -> bool
  - resolve_variable(path: str, ctx: ExecutionContext) -> Any
  - Supports: ${ctx.var}, ${ctx.count > 5}, ${steps.step1.status == 'success'}
  - Uses safe_eval (no exec, limited builtins)

step_state.py:
- StepState enum: PENDING, READY, RUNNING, RETRYING, SUCCESS, FAILED, SKIPPED, CANCELLED
- StepStateManager:
  - get_state(step_name: str) -> StepState
  - transition(step_name: str, new_state: StepState) -> None
  - can_transition(from_state, to_state) -> bool
  - Enforces valid transitions per state machine diagram
</REQUIRED_COMPONENTS>

<DESIGN_NOTES>
DAG vs Pipeline:
- Pipeline: [step1] -> [step2, step3 parallel] -> [step4]
  - Has implicit sync barrier after parallel group
- DAG: step1 -> step2, step1 -> step3, step2 -> step4, step3 -> step4
  - step4 starts as soon as BOTH step2 and step3 complete
  - If step2 finishes before step3, no waiting

Cycle Detection:
- DFS with three colors: WHITE (unvisited), GRAY (in current path), BLACK (done)
- If we visit a GRAY node, cycle detected
- Track path for error message

Dynamic Scheduling:
- Initialize: in_degree[step] = len(step.depends_on)
- Ready: all steps with in_degree == 0
- On completion: for each dependent, in_degree[dep] -= 1
- If in_degree reaches 0, add to ready queue
</DESIGN_NOTES>

<OUTPUT_FORMAT>
### engine/dag.py
```python
# DAG class with cycle detection and topological sort
```

### engine/dag_executor.py
```python
# Dynamic parallel execution with no sync barriers
```

### engine/expressions.py
```python
# Safe expression evaluation for conditions
```

### engine/step_state.py
```python
# Step state machine with valid transitions
```

### tests/test_dag.py
```python
# Test cases:
# - test_simple_dag_execution
# - test_parallel_dag_execution (diamond pattern)
# - test_cycle_detection
# - test_missing_dependency_error
# - test_max_concurrency_respected
# - test_conditional_execution_in_dag
# - test_step_failure_stops_dependents
```
</OUTPUT_FORMAT>
```

---

## Phase 4b: Execution Patterns

### Prompt 4.1: Execution Patterns

```
<TASK>
Implement workflow execution patterns: sequential, parallel, iterative, and conditional.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/engine/patterns/
Patterns define HOW steps are executed (order, concurrency, conditions).
</CONTEXT>

<REQUIRED_PATTERNS>
base.py:
- ExecutionPattern (ABC):
  - execute(steps, context, executor) -> list[StepResult]

sequential.py:
- SequentialPattern: Execute steps one after another
- Stops on first failure (configurable)

parallel.py:
- ParallelPattern: Execute independent steps concurrently
- Uses asyncio.gather with max_concurrency limit
- Collects all results before continuing

iterative.py:
- IterativePattern: Retry with feedback loop
- max_iterations, exit_condition
- Passes previous result as feedback to next iteration

conditional.py:
- ConditionalPattern: Branch based on condition
- if_true_steps, if_false_steps
- condition is a callable or expression

self_refine.py:
- SelfRefinePattern: Generator → Evaluator → Refiner loop
- Generator: Tier 2 (produces output)
- Evaluator: Tier 3 (scores and critiques)
- Refiner: Tier 2 (fixes based on feedback)
- Continues until score >= threshold or max_iterations
</REQUIRED_PATTERNS>

<OUTPUT_FORMAT>
### engine/patterns/base.py
```python
# ExecutionPattern ABC
```

### engine/patterns/sequential.py
```python
# SequentialPattern
```

### engine/patterns/parallel.py
```python
# ParallelPattern with asyncio
```

### engine/patterns/iterative.py
```python
# IterativePattern with feedback
```

### engine/patterns/conditional.py
```python
# ConditionalPattern with branching
```

### engine/patterns/self_refine.py
```python
# SelfRefinePattern with mixed tiers
```
</OUTPUT_FORMAT>
```

### Prompt 4.2: Main Orchestrator

```
<TASK>
Implement the main WorkflowOrchestrator that executes workflows with tier-aware routing.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/engine/orchestrator.py
The orchestrator is the main entry point for running workflows.
</CONTEXT>

<REQUIRED_FUNCTIONALITY>
WorkflowOrchestrator:
- __init__(router, executor, agent_registry, tool_registry)
- execute_workflow(workflow, context) -> WorkflowResult
- _get_step_tier(step) -> int  # Determine tier from step type
- _execute_step(step, context) -> StepResult
- _handle_failure(step, error, context) -> StepResult
- _should_retry(step, error) -> bool

Tier Assignment Logic:
- Tier 0: file_copy, mkdir, template_render, json_transform
- Tier 1: format, docstring, validate_schema, markdown_cleanup
- Tier 2: generate_code, review, test, refactor
- Tier 3: architect, evaluate, synthesize, plan, orchestrate

WorkflowLoader:
- load_from_yaml(path) -> Workflow
- load_from_dict(data) -> Workflow
- validate_workflow(workflow) -> list[ValidationError]
</REQUIRED_FUNCTIONALITY>

<WORKFLOW_DEFINITION>
@dataclass
class WorkflowStep:
    id: str
    type: str
    tier: Optional[int] = None  # Override auto-detection
    agent: Optional[str] = None
    tool: Optional[str] = None
    inputs: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)

@dataclass  
class Workflow:
    name: str
    version: str
    description: str
    steps: list[WorkflowStep]
    config: dict[str, Any] = field(default_factory=dict)
</WORKFLOW_DEFINITION>

<OUTPUT_FORMAT>
### engine/orchestrator.py
```python
# Full WorkflowOrchestrator implementation
```

### workflows/base.py
```python
# Workflow and WorkflowStep definitions
```

### workflows/loader.py
```python
# YAML workflow loading
```
</OUTPUT_FORMAT>
```

---

## Phase 5: CLI & Workflows

### Prompt 5.1: CLI Implementation

```
<TASK>
Implement the CLI for running and managing agentic workflows.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/cli/
Use Typer for CLI framework.
</CONTEXT>

<REQUIRED_COMMANDS>
main.py:
- run: Execute a workflow
  --workflow: Path to workflow YAML
  --input: Path to input JSON
  --tier-override: Force all steps to specific tier
  --dry-run: Show what would be executed
  --verbose: Detailed output
  --output: Path for results JSON

- list: List available resources
  --workflows: List workflow definitions
  --agents: List registered agents
  --tools: List available tools
  --models: List available models by tier

- validate: Validate workflow definition
  --workflow: Path to workflow YAML
  --strict: Fail on warnings

- status: Check system status
  --models: Test model connectivity
  --providers: Check provider health

- stats: Show model statistics
  --model: Filter by model
  --provider: Filter by provider
  --reset: Reset statistics
</REQUIRED_COMMANDS>

<OUTPUT_FORMAT>
### cli/main.py
```python
# Main CLI app with Typer
```

### cli/commands/run.py
```python
# Run command implementation
```

### cli/commands/list_cmd.py
```python
# List command (list is reserved keyword)
```

### cli/commands/validate.py
```python
# Validate command
```

Add console output formatting with rich or simple print.
</OUTPUT_FORMAT>
```

### Prompt 5.2: Example Workflow Definitions

```
<TASK>
Create example YAML workflow definitions demonstrating tiered execution.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: src/agentic_v2/workflows/definitions/
Workflows define steps, tiers, and execution patterns.
</CONTEXT>

<REQUIRED_WORKFLOWS>
code_review.yaml:
- Collect files (tier 0)
- Format check (tier 1)
- Code review (tier 2)
- Synthesis (tier 3)

code_generation.yaml:
- Parse requirements (tier 2)
- Generate code (tier 2)
- Generate tests (tier 2)
- Review (tier 2)
- Evaluate quality (tier 3)

self_refine_code.yaml:
- Initial generation (tier 2)
- Loop: evaluate (tier 3) → refine (tier 2)
- Final validation (tier 3)

architecture_design.yaml:
- Analyze requirements (tier 3)
- Design components (tier 3)
- Generate scaffolding (tier 2)
- Create documentation (tier 1)
</REQUIRED_WORKFLOWS>

<YAML_SCHEMA>
name: string
version: string
description: string
config:
  max_iterations: int
  fail_fast: bool
  checkpoint_interval: int

steps:
  - id: string
    type: string  # file_list, format, review, generate_code, etc.
    tier: int     # 0-3, optional (auto-detected)
    agent: string # Agent to use (if type requires agent)
    tool: string  # Tool to use (if type requires tool)
    inputs:
      key: value or ${previous_step.output}
    config:
      key: value
    depends_on:
      - step_id
</YAML_SCHEMA>

<OUTPUT_FORMAT>
### workflows/definitions/code_review.yaml
```yaml
# Full workflow
```

### workflows/definitions/code_generation.yaml
```yaml
# Full workflow
```

### workflows/definitions/self_refine_code.yaml
```yaml
# Full workflow with loop
```

### workflows/definitions/architecture_design.yaml
```yaml
# Full workflow
```
</OUTPUT_FORMAT>
```

---

## Phase 6: Testing & Validation

### Prompt 6.1: Unit Tests (Tier 0 - No LLM)

```
<TASK>
Create unit tests for Tier 0 components that require no LLM.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: tests/
Use pytest with pytest-asyncio for async tests.
</CONTEXT>

<REQUIRED_TESTS>
test_tools.py:
- test_file_copy_tool
- test_file_move_tool
- test_directory_create_tool
- test_json_transform_tool
- test_template_render_tool
- test_config_merge_tool

test_contracts.py:
- test_agent_message_creation
- test_step_result_validation
- test_workflow_result_aggregation
- test_schema_serialization

test_router.py:
- test_tier_model_selection
- test_fallback_on_unavailable
- test_model_stats_tracking
- test_cooldown_logic

test_context.py:
- test_variable_resolution
- test_reference_resolution  # ${step.output}
- test_context_inheritance
</REQUIRED_TESTS>

<OUTPUT_FORMAT>
### tests/conftest.py
```python
# Fixtures
```

### tests/test_tools.py
```python
# Tool tests
```

### tests/test_contracts.py
```python
# Contract tests
```

### tests/test_router.py
```python
# Router tests (mocked LLM)
```

### tests/test_context.py
```python
# Context tests
```

All tests should be runnable without LLM (mock where needed).
</OUTPUT_FORMAT>
```

### Prompt 6.2: Integration Tests (Tiered)

```
<TASK>
Create integration tests organized by model tier required.
</TASK>

<CONTEXT>
Package: agentic-workflows-v2
Location: tests/
Tests are marked with pytest markers for selective running.
</CONTEXT>

<TEST_MARKERS>
@pytest.mark.tier0  # No LLM needed
@pytest.mark.tier1  # Small model (fast)
@pytest.mark.tier2  # Medium model (moderate)
@pytest.mark.tier3  # Large model (slow, expensive)
@pytest.mark.slow   # Takes > 10 seconds
@pytest.mark.expensive  # Uses paid API
</TEST_MARKERS>

<REQUIRED_TESTS>
test_integration_tier0.py:
- test_file_workflow_execution
- test_template_workflow
- test_json_transform_workflow

test_integration_tier1.py:
- test_formatting_workflow
- test_docstring_generation
- test_markdown_cleanup

test_integration_tier2.py:
- test_code_generation_workflow
- test_code_review_workflow
- test_test_generation_workflow

test_integration_tier3.py:
- test_architecture_workflow
- test_evaluation_workflow
- test_self_refine_workflow
</REQUIRED_TESTS>

<OUTPUT_FORMAT>
### tests/test_integration_tier0.py
```python
# Tier 0 integration tests
```

### tests/test_integration_tier1.py
```python
# Tier 1 integration tests
```

### tests/test_integration_tier2.py
```python
# Tier 2 integration tests
```

### tests/test_integration_tier3.py
```python
# Tier 3 integration tests
```

### pytest.ini (updates)
```ini
[pytest]
markers =
    tier0: No LLM required
    tier1: Small model required
    tier2: Medium model required
    tier3: Large model required
    slow: Takes more than 10 seconds
    expensive: Uses paid API
```
</OUTPUT_FORMAT>
```

---

## Validation Prompt (Run After Each Phase)

### Prompt: Phase Validation

```
<TASK>
Validate the implementation of Phase [N] of agentic-workflows-v2.
</TASK>

<CONTEXT>
Phase: [0-6]
Package location: d:\source\prompts\agentic-workflows-v2\
Expected deliverables: [list from implementation plan]
</CONTEXT>

<VALIDATION_CHECKLIST>
1. File Structure:
   - [ ] All required files exist
   - [ ] __init__.py exports are correct
   - [ ] No circular imports

2. Code Quality:
   - [ ] Type hints on all public functions
   - [ ] Docstrings on all classes and public methods
   - [ ] Error handling for edge cases
   - [ ] Async where appropriate

3. Contracts:
   - [ ] Pydantic models validate correctly
   - [ ] Schemas match expected structure
   - [ ] Serialization/deserialization works

4. Tests:
   - [ ] All tests pass: pytest tests/ -v
   - [ ] No warnings in test output
   - [ ] Coverage > 80% for new code

5. Integration:
   - [ ] Imports from tools/llm work
   - [ ] No dependencies on multiagent-workflows
   - [ ] CLI commands functional (if applicable)
</VALIDATION_CHECKLIST>

<OUTPUT_FORMAT>
Provide:
1. Pass/Fail status for each checklist item
2. List of issues found (if any)
3. Suggested fixes for issues
4. GO/NO-GO decision for next phase
</OUTPUT_FORMAT>
```

---

## Quick Reference: Task → Tier → Model

| Task | Tier | Recommended Model |
|------|------|-------------------|
| File operations | 0 | None (Python) |
| JSON transform | 0 | None (Python) |
| Template render | 0 | None (Jinja2) |
| Code formatting | 1 | ollama:phi3:mini |
| Docstring gen | 1 | ollama:qwen2.5:1.5b |
| Code generation | 2 | gh:phi-4 |
| Code review | 2 | ollama:qwen2.5-coder:14b |
| Test generation | 2 | ollama:qwen2.5-coder:14b |
| Architecture | 3 | gh:meta/llama-3.3-70b-instruct |
| Evaluation | 3 | gh:gpt-4o-mini |
| Planning | 3 | gh:meta/llama-3.3-70b-instruct |

---

## Execution Commands

```powershell
# Run a phase prompt
$prompt = Get-Content "docs/planning/agentic-workflows-v2-prompts.md" -Raw
# Extract specific prompt section, send to LLM

# Validate phase
cd d:\source\prompts\agentic-workflows-v2
python -m pytest tests/ -v --tb=short

# Run specific tier tests
python -m pytest tests/ -v -m "tier0"
python -m pytest tests/ -v -m "tier1" 
python -m pytest tests/ -v -m "tier2"

# Run CLI
python -m agentic_v2.cli run --workflow workflows/definitions/code_review.yaml
```
