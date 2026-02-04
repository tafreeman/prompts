# Agentic Workflows v2 - Phased Implementation Plan

**Purpose:** Step-by-step implementation guide with model tier assignments  
**Date:** February 2, 2026  
**Goal:** Enable small models for simple tasks, reserve large models for reasoning  
**Status:** NEW INDEPENDENT MODULE (clean implementation)

> **📋 Ready-to-Use Prompts:** See companion file [`agentic-workflows-v2-prompts.md`](agentic-workflows-v2-prompts.md) for copy-paste prompts with full context for each phase.

---

## ⚠️ Implementation Decision: New Independent Module

**Decision**: Build `agentic-workflows-v2/` as a **completely independent package** - NOT integrated with existing `multiagent-workflows/`.

### Rationale

| Factor | Existing Code | New Module |
|--------|---------------|------------|
| **Coupling** | Tightly coupled to specific patterns | Clean separation of concerns |
| **Testing** | Hard to test in isolation | Unit testable from day 1 |
| **Model flexibility** | Hardcoded model assignments | Tier-based routing |
| **Incremental delivery** | All-or-nothing | Phase by phase |
| **Dependencies** | Heavy (LangChain, etc.) | Minimal (Pydantic, httpx) |

### Module Location

```
d:\source\prompts\
├── multiagent-workflows/     # EXISTING - do not modify
├── agentic-workflows-v2/     # NEW - independent package
│   ├── pyproject.toml
│   ├── README.md
│   └── src/
│       └── agentic_v2/
└── tools/llm/                # SHARED - can import from here
```

### Shared Dependencies (Import Only)

The new module MAY import from these existing utilities:

- `tools/llm/llm_client.py` - LLM abstraction (read-only import)
- `tools/core/tool_init.py` - CLI utilities (optional)

The new module MUST NOT:

- Modify existing `multiagent-workflows/` code
- Depend on `multiagent_workflows` package internals
- Share state with existing workflows

---

## Overview: Model Tiering Strategy

| Tier | Model Size | Cost | Tasks |
|------|------------|------|-------|
| **Tier 0** | Tiny (< 1B) | Free/Local | File copy, template fill, JSON transform |
| **Tier 1** | Small (1-3B) | Cheap | Code formatting, simple generation, validation |
| **Tier 2** | Medium (7-14B) | Moderate | Code generation, review, testing |
| **Tier 3** | Large (32B+/Cloud) | Expensive | Architecture, complex reasoning, evaluation |

### Model Assignments (Example)

```yaml
# config/model_routing.yaml
tier_0:  # No LLM needed - pure code
  - file_copy
  - directory_create
  - json_transform
  - template_render
  - config_merge

tier_1:  # Small models
  models: ["ollama:qwen2.5:1.5b", "ollama:phi3:mini", "local:phi-silica"]
  tasks:
    - simple_code_format
    - docstring_generation
    - variable_rename
    - json_schema_validate
    - markdown_cleanup

tier_2:  # Medium models  
  models: ["ollama:qwen2.5-coder:14b", "ollama:deepseek-coder-v2:16b"]
  tasks:
    - code_generation
    - code_review
    - test_generation
    - bug_fixing
    - refactoring

tier_3:  # Large models (cloud or local 32B+)
  models: ["gh:gpt-4o", "gh:gpt-4o-mini", "ollama:qwen2.5:32b"]
  premium_models:  # For critical tasks when standard models struggle
    - "gh:o3-mini"       # Reasoning specialist
    - "gh:o4-mini"       # Latest OpenAI
    - "gh:claude-3.5-sonnet"  # Anthropic via GitHub
  tasks:
    - architecture_design
    - complex_reasoning
    - evaluation_scoring
    - multi-step_planning
    - synthesis_combining
```

**Model Availability (from discovery):**

- **GitHub Models**: 24 available (gpt-4o, o3-mini, claude-3.5-sonnet, etc.)
- **Ollama Local**: 60+ models (qwen2.5-coder:14b, deepseek-coder-v2, etc.)
- **Azure OpenAI**: 4 deployments
- **OpenAI Direct**: Full API access

### Smart Model Router with Adaptive Learning

The module includes a **SmartModelRouter** that handles:

1. **Failure Tracking** - Counts errors per model/provider
2. **Adaptive Prioritization** - Demotes models that hit rate limits or fail
3. **Provider Health** - Tracks provider-level issues (e.g., GitHub API down)
4. **Automatic Fallback** - Falls back to local models when cloud is unavailable
5. **Learning Persistence** - Saves/loads model stats between runs

```python
# agentic_v2/models/smart_router.py
@dataclass
class ModelStats:
    """Tracks model performance for adaptive routing."""
    success_count: int = 0
    failure_count: int = 0
    rate_limit_count: int = 0
    total_latency_ms: float = 0
    last_failure: Optional[datetime] = None
    cooldown_until: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 1.0
    
    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.success_count if self.success_count else 0

class SmartModelRouter:
    """Routes requests with adaptive learning and fallback."""
    
    def record_success(self, model: str, latency_ms: float): ...
    def record_failure(self, model: str, error_type: str): ...
    def get_model_for_tier(self, tier: int) -> str:
        """Returns best available model, skipping those in cooldown."""
        ...
```

**Fallback Chain Example:**

```
Tier 2 request → gh:gpt-4o-mini (rate limited)
              → gh:gpt-4o (rate limited) 
              → ollama:qwen2.5-coder:14b (success!)
              → [learns: prefer ollama for next 5 min]
```

**Provider Cooldown Logic:**

- 3 failures in 1 minute → 30 second cooldown
- 5 rate limits → 2 minute cooldown
- Provider-wide outage → 5 minute cooldown, try local

**🔮 Future Enhancement: ML-Based Routing**

> The current rule-based router could be enhanced with a small ML model that learns:
>
> - Optimal model selection based on task characteristics
> - Predicted latency and success rate per model
> - Cost optimization (prefer cheaper models when quality is sufficient)
>
> A simple approach: train a small classifier on (task_type, prompt_length, time_of_day) → best_model.
> Could use scikit-learn or a tiny neural net. The learning data is already collected via `ModelStats`.

---

## Phase 0: Foundation (No LLM Required)

**Duration:** 1-2 days  
**Model Required:** None (pure Python)

### 0.1 Create Package Structure

```
d:\source\prompts\agentic-workflows-v2\
├── pyproject.toml            # Package definition
├── README.md                 # Quick start guide
├── src/
│   └── agentic_v2/
│       ├── __init__.py
│       ├── contracts/
│       │   ├── __init__.py
│       │   ├── messages.py   # AgentMessage, StepResult
│       │   └── schemas.py    # Input/output schemas
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py       # BaseTool ABC, ToolResult
│       │   ├── registry.py   # Simple dict-based registry
│       │   └── builtin/
│       │       ├── __init__.py
│       │       ├── file_ops.py
│       │       └── transform.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── router.py     # Tier-based model selection
│       │   ├── smart_router.py  # Adaptive learning + fallback
│       │   ├── model_stats.py   # Success/failure tracking
│       │   └── client.py     # Thin wrapper or import from tools/llm
│       ├── engine/
│       │   ├── __init__.py
│       │   ├── executor.py   # Step execution
│       │   └── orchestrator.py
│       └── cli/
│           └── __init__.py
└── tests/
    ├── test_tools.py         # Tier 0 tests (no LLM needed)
    ├── test_contracts.py
    └── conftest.py
```

### 0.2 pyproject.toml

```toml
[project]
name = "agentic-workflows-v2"
version = "0.1.0"
description = "Tiered multi-model agentic workflows"
requires-python = ">=3.11"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.25",
    "jinja2>=3.0",
    "jmespath>=1.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-asyncio>=0.21"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/agentic_v2"]
```

### 0.3 Implement Zero-LLM Tools (Tier 0)

These tools require NO language model - pure Python operations:

```python
# tools/builtin/file_ops.py - NO LLM NEEDED
class FileCopyTool(BaseTool):
    """Copy file from source to destination."""
    async def execute(self, source: str, dest: str) -> ToolResult:
        shutil.copy2(source, dest)
        return ToolResult(success=True, output=dest)

class DirectoryCreateTool(BaseTool):
    """Create directory (mkdir -p)."""
    async def execute(self, path: str) -> ToolResult:
        Path(path).mkdir(parents=True, exist_ok=True)
        return ToolResult(success=True, output=path)

class FileMoveTool(BaseTool):
    """Move/rename a file."""
    async def execute(self, source: str, dest: str) -> ToolResult:
        shutil.move(source, dest)
        return ToolResult(success=True, output=dest)

class FileDeleteTool(BaseTool):
    """Delete a file."""
    async def execute(self, path: str) -> ToolResult:
        Path(path).unlink()
        return ToolResult(success=True, output=True)

class JsonTransformTool(BaseTool):
    """Apply jmespath query to JSON."""
    async def execute(self, data: dict, query: str) -> ToolResult:
        import jmespath
        result = jmespath.search(query, data)
        return ToolResult(success=True, output=result)

class TemplateRenderTool(BaseTool):
    """Render Jinja2 template with variables."""
    async def execute(self, template: str, variables: dict) -> ToolResult:
        from jinja2 import Template
        result = Template(template).render(**variables)
        return ToolResult(success=True, output=result)

class ConfigMergeTool(BaseTool):
    """Deep merge multiple config dicts."""
    async def execute(self, configs: list[dict]) -> ToolResult:
        from functools import reduce
        result = reduce(deep_merge, configs, {})
        return ToolResult(success=True, output=result)
```

**Deliverables:**

- [ ] `agentic_v2/tools/builtin/file_ops.py` - File operations (copy, move, delete, mkdir)
- [ ] `agentic_v2/tools/builtin/transform.py` - JSON/YAML transform, template render
- [ ] `agentic_v2/tools/builtin/validation.py` - Schema validation (no LLM)
- [ ] `agentic_v2/tools/registry.py` - Tool registry with auto-discovery

---

## Phase 1: Contracts & Small Model Tasks

**Duration:** 2-3 days  
**Models Required:** Tier 1 (small: 1-3B params)

### 1.1 Pydantic Contracts

Copy from implementation patterns doc:

- [ ] `agentic_v2/contracts/base.py` - BaseModel utilities
- [ ] `agentic_v2/contracts/messages.py` - AgentMessage, StepResult, WorkflowResult
- [ ] `agentic_v2/contracts/agent_contracts.py` - Per-agent input/output schemas
- [ ] `agentic_v2/contracts/validation.py` - Runtime validation helpers

### 1.2 Simple LLM Tools (Tier 1 - Small Models)

These tasks are simple enough for tiny models:

```python
# tools/builtin/formatting.py - TIER 1 (small model)
class CodeFormatTool(BaseTool):
    """Format code using small model for style fixes."""
    tier = 1
    
    async def execute(self, code: str, language: str) -> ToolResult:
        prompt = f"Format this {language} code. Return ONLY the formatted code:\n```{language}\n{code}\n```"
        result = await self.llm.generate(prompt, max_tokens=len(code) * 2)
        return ToolResult(success=True, output=result)

class DocstringGeneratorTool(BaseTool):
    """Generate docstring for a function."""
    tier = 1
    
    async def execute(self, code: str) -> ToolResult:
        prompt = f"Write a one-line docstring for this function:\n{code}"
        result = await self.llm.generate(prompt, max_tokens=100)
        return ToolResult(success=True, output=result)

class MarkdownCleanupTool(BaseTool):
    """Clean up markdown formatting."""
    tier = 1
    
    async def execute(self, markdown: str) -> ToolResult:
        prompt = f"Fix formatting issues in this markdown. Return cleaned markdown only:\n{markdown}"
        result = await self.llm.generate(prompt, max_tokens=len(markdown) * 2)
        return ToolResult(success=True, output=result)
```

### 1.3 Model Router (Basic)

```python
# models/router.py
class ModelRouter:
    """Route tasks to appropriate model tier."""
    
    def __init__(self, config: dict):
        self.tier_models = config.get("tier_models", {})
        self.task_tiers = config.get("task_tiers", {})
    
    def get_model_for_task(self, task: str) -> str:
        """Get the appropriate model for a task."""
        tier = self.task_tiers.get(task, 2)  # Default to medium
        models = self.tier_models.get(tier, [])
        # Return first available model in tier
        return self._first_available(models)
    
    def get_model_for_tier(self, tier: int) -> str:
        """Get any model from a specific tier."""
        models = self.tier_models.get(tier, [])
        return self._first_available(models)
```

**Deliverables:**

- [ ] All contract files from patterns doc (in `agentic_v2/contracts/`)
- [ ] `agentic_v2/tools/builtin/formatting.py` - Tier 1 formatting tools
- [ ] `agentic_v2/models/router.py` - Basic model routing
- [ ] `agentic_v2/models/smart_router.py` - Adaptive learning router with:
  - Failure tracking per model/provider
  - Automatic cooldown on rate limits
  - Provider health monitoring
  - Fallback chain (cloud → local)
  - Stats persistence between runs
- [ ] `agentic_v2/models/model_stats.py` - ModelStats dataclass for learning

---

## Phase 2: Core Engine & Medium Model Tasks

**Duration:** 3-4 days  
**Models Required:** Tier 2 (medium: 7-14B params)

### 2.1 Engine Components

- [ ] `agentic_v2/engine/context.py` - WorkflowContext, StepContext
- [ ] `agentic_v2/engine/executor.py` - Step execution with model routing
- [ ] `agentic_v2/engine/state.py` - State management + checkpointing

### 2.2 Base Agent System

```python
# agents/base.py
class AgentConfig(BaseModel):
    """Configuration for an agent."""
    id: str
    name: str
    model_tier: int = 2  # Default to medium
    system_prompt: str
    tools: list[str] = []
    max_tokens: int = 4096

class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, config: AgentConfig, router: ModelRouter):
        self.config = config
        self.router = router
        self.model = router.get_model_for_tier(config.model_tier)
    
    @abstractmethod
    async def execute(self, input: BaseModel, context: StepContext) -> BaseModel:
        """Execute the agent's task."""
        pass
```

### 2.3 Code Generation Agents (Tier 2)

```python
# agents/implementations/coder.py - TIER 2
class CoderAgent(BaseAgent):
    """Code generation agent - uses medium model."""
    
    default_tier = 2
    
    async def execute(self, input: CoderInput, context: StepContext) -> CoderOutput:
        prompt = self._build_prompt(input)
        result = await self.llm.generate(prompt)
        files = self._parse_code_blocks(result)
        return CoderOutput(files=files)

# agents/implementations/tester.py - TIER 2  
class TesterAgent(BaseAgent):
    """Test generation agent - uses medium model."""
    
    default_tier = 2
    
    async def execute(self, input: TesterInput, context: StepContext) -> TesterOutput:
        prompt = f"Write unit tests for:\n{input.code}"
        result = await self.llm.generate(prompt)
        return TesterOutput(tests=self._parse_tests(result))
```

### 2.4 Tier 2 Tools

```python
# tools/builtin/code_tools.py - TIER 2
class CodeGeneratorTool(BaseTool):
    """Generate code from specification."""
    tier = 2
    
class RefactoringTool(BaseTool):
    """Refactor code while preserving behavior."""
    tier = 2

class TestGeneratorTool(BaseTool):
    """Generate unit tests for code."""
    tier = 2
```

**Deliverables:**

- [ ] `agentic_v2/engine/context.py`
- [ ] `agentic_v2/engine/executor.py`
- [ ] `agentic_v2/engine/state.py`
- [ ] `agentic_v2/agents/base.py`
- [ ] `agentic_v2/agents/registry.py`
- [ ] `agentic_v2/agents/implementations/coder.py`
- [ ] `agentic_v2/agents/implementations/reviewer.py`
- [ ] `agentic_v2/agents/implementations/tester.py`

---

## Phase 3: Orchestration & Patterns

**Duration:** 3-4 days  
**Models Required:** Tier 2-3 (medium to large)

### 3.1 Execution Patterns

- [ ] `agentic_v2/engine/patterns/sequential.py` - Linear execution
- [ ] `agentic_v2/engine/patterns/parallel.py` - Concurrent execution
- [ ] `agentic_v2/engine/patterns/iterative.py` - Retry with feedback
- [ ] `agentic_v2/engine/patterns/conditional.py` - Branching logic

### 3.2 Orchestrator with Tier Awareness

```python
# engine/orchestrator.py
class WorkflowOrchestrator:
    """
    Orchestrates workflow execution with model tier awareness.
    
    Key principle: Use smallest model that can do the job.
    """
    
    def __init__(self, router: ModelRouter, executor: StepExecutor):
        self.router = router
        self.executor = executor
    
    async def execute_workflow(self, workflow: Workflow, context: WorkflowContext):
        """Execute a workflow, routing each step to appropriate model tier."""
        
        for step in workflow.steps:
            # Determine tier based on step type
            tier = self._get_step_tier(step)
            
            # Get model for tier
            model = self.router.get_model_for_tier(tier)
            context.set_model(model)
            
            # Execute step
            result = await self.executor.execute_step(step, context)
            
            # Store result
            context.add_result(step.id, result)
        
        return WorkflowResult(...)
    
    def _get_step_tier(self, step: WorkflowStep) -> int:
        """Determine the appropriate tier for a step."""
        # Tier 0: No LLM needed
        if step.type in ["file_copy", "mkdir", "template_render"]:
            return 0
        
        # Tier 1: Simple tasks
        if step.type in ["format", "docstring", "validate_schema"]:
            return 1
        
        # Tier 2: Code generation/review
        if step.type in ["generate_code", "review", "test", "refactor"]:
            return 2
        
        # Tier 3: Complex reasoning
        if step.type in ["architect", "evaluate", "synthesize", "plan"]:
            return 3
        
        return 2  # Default to medium
```

### 3.3 Self-Refinement Pattern (Uses Mixed Tiers)

```python
# engine/patterns/self_refine.py
class SelfRefinePattern:
    """
    Self-refinement loop with tiered models.
    
    - Generator: Tier 2 (medium) - produces output
    - Evaluator: Tier 3 (large) - scores and critiques  
    - Refiner: Tier 2 (medium) - fixes based on feedback
    
    This optimizes cost: expensive model only used for judging.
    """
    
    async def execute(self, ...):
        # Step 1: Generate with medium model (Tier 2)
        context.set_tier(2)
        gen_result = await self.executor.execute_step(generator_step, context)
        
        # Step 2: Evaluate with large model (Tier 3)
        context.set_tier(3)
        eval_result = await self.executor.execute_step(evaluator_step, context)
        
        # Step 3: Refine with medium model (Tier 2)
        if eval_result.score < threshold:
            context.set_tier(2)
            gen_result = await self.executor.execute_step(refiner_step, context)
```

**Deliverables:**

- [ ] All pattern implementations (in `agentic_v2/engine/patterns/`)
- [ ] `agentic_v2/engine/orchestrator.py` with tier routing
- [ ] `agentic_v2/workflows/base.py` - Workflow definition class
- [ ] `agentic_v2/workflows/registry.py` - Workflow registry

---

## Phase 4: DAG Workflows & Dependency Resolution

**Duration:** 2-3 days  
**Models Required:** Tier 0-2 (testing engine logic)

> **Note:** This phase builds true DAG-based execution that subsumes both sequential and parallel patterns. The existing `Pipeline` and `ParallelGroup` work but have sync barriers. DAG execution achieves maximum parallelism from dependency graphs with no artificial barriers.

### 4.1 DAG Workflow Definition

```python
# engine/dag.py - True DAG with validation
class DAG:
    """
    Directed Acyclic Graph for workflow execution.
    
    Key advantages over Pipeline:
    - No sync barriers between "layers"
    - Maximum parallelism from dependency graph
    - Automatic topological ordering
    - Cycle detection at definition time
    """
    
    def __init__(self, name: str):
        self.name = name
        self.steps: dict[str, StepDefinition] = {}
        self._adjacency: dict[str, list[str]] = {}  # step -> dependents
    
    def add(self, step: StepDefinition) -> "DAG":
        """Add step to DAG. Validates dependencies exist."""
        self.steps[step.name] = step
        return self  # Fluent API
    
    def validate(self) -> None:
        """
        Validate DAG structure.
        
        Raises:
            CycleDetectedError: If circular dependency found
            MissingDependencyError: If step depends on unknown step
        """
        self._check_missing_dependencies()
        self._detect_cycles()
    
    def _detect_cycles(self) -> bool:
        """Detect cycles using DFS with coloring."""
        ...
    
    def _build_adjacency_list(self) -> dict[str, list[str]]:
        """Build adjacency list from depends_on fields."""
        ...
    
    def get_execution_order(self) -> list[str]:
        """Return topologically sorted step names."""
        ...
    
    def get_ready_steps(self, completed: set[str]) -> list[str]:
        """Get steps whose dependencies are all met."""
        ...
```

### 4.2 DAG Executor (Dynamic Parallel Execution)

```python
# engine/dag_executor.py - BFS-style dynamic execution
class DAGExecutor:
    """
    Execute DAG with maximum parallelism.
    
    Uses Kahn's algorithm variant:
    - Track in-degree (# pending dependencies) per step
    - Steps with in_degree=0 are ready to run
    - When step completes, decrement dependents' in_degree
    - No artificial barriers - steps run ASAP
    """
    
    async def execute(
        self,
        dag: DAG,
        ctx: ExecutionContext,
        max_concurrency: int = 10
    ) -> WorkflowResult:
        """
        Execute DAG with dynamic scheduling.
        
        Steps run as soon as their dependencies complete.
        Maximum parallelism bounded by max_concurrency.
        """
        # Initialize in-degree for each step
        in_degree = {name: len(step.depends_on) for name, step in dag.steps.items()}
        
        # Queue of ready steps
        ready = asyncio.Queue()
        for name, deg in in_degree.items():
            if deg == 0:
                await ready.put(name)
        
        # Track running and completed
        running: set[str] = set()
        completed: set[str] = set()
        results: dict[str, StepResult] = {}
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def run_step(name: str):
            async with semaphore:
                result = await self._execute_single(dag.steps[name], ctx)
                results[name] = result
                completed.add(name)
                running.discard(name)
                
                # Schedule dependents whose in_degree is now 0
                for dependent in self._get_dependents(dag, name):
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        await ready.put(dependent)
        
        # Process until all complete
        tasks = []
        while len(completed) < len(dag.steps):
            while not ready.empty():
                name = await ready.get()
                running.add(name)
                tasks.append(asyncio.create_task(run_step(name)))
            
            if tasks:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                tasks = list(pending)
        
        return WorkflowResult(...)
```

### 4.3 Step State Machine

```
Step Lifecycle States:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  [*] ───► PENDING ───► READY ───► RUNNING ──┬─► SUCCESS    │
│               │                     │        │              │
│               │                     │        ├─► FAILED     │
│               │                     │        │              │
│               │                     ▼        └─► CANCELLED  │
│               │                 RETRYING ────────►          │
│               │                                             │
│               └──────────────────────────────► SKIPPED      │
│                     (condition false)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Transitions:
- PENDING → READY: All dependencies completed successfully
- PENDING → SKIPPED: when=False or unless=True
- READY → RUNNING: Executor schedules step
- RUNNING → SUCCESS: Step completes without error
- RUNNING → FAILED: Error and no retries left
- RUNNING → RETRYING: Error but retries available
- RETRYING → RUNNING: Retry attempt starts
- RUNNING → CANCELLED: Workflow cancelled or timeout
```

### 4.4 Conditional Execution & Expression Evaluation

```python
# engine/expressions.py - Expression evaluator for conditions
class ExpressionEvaluator:
    """
    Evaluate condition expressions against context.
    
    Supports:
    - Variable access: ${ctx.var_name}
    - Comparisons: ${ctx.count > 5}
    - Boolean ops: ${ctx.enabled and ctx.ready}
    - Step results: ${steps.step1.status == 'success'}
    """
    
    def evaluate(self, expr: str, ctx: ExecutionContext) -> bool:
        """Safely evaluate expression."""
        ...
    
    def resolve_variable(self, path: str, ctx: ExecutionContext) -> Any:
        """Resolve ${step1.output.field} style paths."""
        ...
```

### 4.5 Inter-Step Data Flow

Document existing I/O mapping capabilities:

```python
# How input_mapping/output_mapping work at runtime
step = StepDefinition(
    name="process",
    func=process_func,
    # Map context vars to step inputs
    input_mapping={
        "data": "previous_step.result",      # ${previous_step.result}
        "config": "workflow.config.settings"  # ${workflow.config.settings}
    },
    # Map step outputs to context vars  
    output_mapping={
        "processed": "process.result",       # Store in ctx as process.result
        "count": "metrics.item_count"        # Store in ctx as metrics.item_count
    }
)
```

**Deliverables:**

- [ ] `agentic_v2/engine/dag.py` - DAG class with cycle detection, topological sort
- [ ] `agentic_v2/engine/dag_executor.py` - Dynamic parallel DAG execution
- [ ] `agentic_v2/engine/expressions.py` - Condition expression evaluator
- [ ] `agentic_v2/engine/step_state.py` - Step state machine (formalize existing)
- [ ] `tests/test_dag.py` - DAG validation, execution, cycle detection tests

---

## Phase 4b: Architects & Evaluators (Large Models)

**Duration:** 2-3 days  
**Models Required:** Tier 3 (large: 32B+ or cloud)

> **Note:** This phase implements specialized Tier 3 agents. These require large models for complex reasoning tasks. The agents integrate with the DAG executor from Phase 4.

```python
# agents/implementations/architect.py - TIER 3
class ArchitectAgent(BaseAgent):
    """
    Architecture design agent - REQUIRES large model.
    
    This agent handles complex reasoning:
    - System design decisions
    - Trade-off analysis
    - Technology selection
    """
    
    default_tier = 3
    
    async def execute(self, input: ArchitectInput, ctx: StepContext) -> ArchitectOutput:
        # Use large model for complex reasoning
        prompt = self._build_architecture_prompt(input)
        result = await self.llm.generate(prompt, model_tier=3)
        return self._parse_architecture(result)

# agents/implementations/evaluator.py - TIER 3
class EvaluatorAgent(BaseAgent):
    """
    Quality evaluation agent - REQUIRES large model.
    
    Judges output quality, provides scores and feedback.
    Critical for self-refinement loops.
    """
    
    default_tier = 3
    
    async def execute(self, input: EvaluatorInput, ctx: StepContext) -> EvaluatorOutput:
        prompt = self._build_evaluation_prompt(input)
        result = await self.llm.generate(prompt, model_tier=3)
        return self._parse_evaluation(result)
```

### 4.2 Evaluation Framework

- [ ] `agentic_v2/evaluation/evaluator.py` - WorkflowEvaluator
- [ ] `agentic_v2/evaluation/rubrics/` - YAML scoring rubrics
- [ ] `agentic_v2/evaluation/reporters/` - JSON/Markdown output

**Deliverables:**

- [ ] `agentic_v2/agents/implementations/architect.py`
- [ ] `agentic_v2/agents/implementations/evaluator.py`
- [ ] `agentic_v2/agents/implementations/synthesizer.py`
- [ ] Complete evaluation framework (in `agentic_v2/evaluation/`)

---

## Phase 5: Workflow Definitions & CLI

**Duration:** 2-3 days  
**Models Required:** All tiers

### 5.1 YAML Workflow Definitions

```yaml
# workflows/definitions/code_review.yaml
name: code_review
description: Review code with tiered models
version: "1.0"

steps:
  # Tier 0 - No LLM
  - id: collect_files
    type: file_list
    tier: 0
    config:
      pattern: "**/*.py"
  
  # Tier 1 - Small model
  - id: format_check
    type: format_validate
    tier: 1
    agent: formatter
    input:
      files: ${collect_files.output}
  
  # Tier 2 - Medium model
  - id: code_review
    type: review
    tier: 2
    agent: reviewer
    input:
      files: ${collect_files.output}
      context: ${format_check.output}
  
  # Tier 3 - Large model
  - id: synthesis
    type: synthesize
    tier: 3
    agent: evaluator
    input:
      reviews: ${code_review.output}
```

### 5.2 CLI

```python
# cli/main.py
import typer
app = typer.Typer()

@app.command()
def run(
    workflow: str,
    input_file: Path = None,
    tier_override: int = None,  # Force all steps to use specific tier
    dry_run: bool = False,
):
    """Run a workflow with tier-aware model routing."""
    ...

@app.command()
def list_tiers():
    """Show model assignments per tier."""
    ...

@app.command()
def validate(workflow: str):
    """Validate workflow definition."""
    ...
```

**Deliverables:**

- [ ] YAML workflow definitions (in `agentic_v2/workflows/definitions/`)
- [ ] `agentic_v2/cli/main.py` with Typer
- [ ] `agentic_v2/cli/commands/run.py`
- [ ] `agentic_v2/cli/commands/list.py`
- [ ] `agentic_v2/cli/commands/validate.py`

---

## Phase 6: Integration & Testing

**Duration:** 2-3 days  
**Models Required:** All tiers for integration tests

### 6.1 Unit Tests (No LLM)

```python
# tests/test_tools.py - NO LLM NEEDED
def test_file_copy_tool():
    tool = FileCopyTool()
    result = asyncio.run(tool.execute("src.txt", "dst.txt"))
    assert result.success

def test_template_render():
    tool = TemplateRenderTool()
    result = asyncio.run(tool.execute(
        template="Hello {{ name }}!",
        variables={"name": "World"}
    ))
    assert result.output == "Hello World!"
```

### 6.2 Integration Tests (Tiered)

```python
# tests/test_integration.py
@pytest.mark.tier0  # No LLM
def test_file_workflow():
    ...

@pytest.mark.tier1  # Small model
def test_formatting_workflow():
    ...

@pytest.mark.tier2  # Medium model
@pytest.mark.slow
def test_code_generation():
    ...

@pytest.mark.tier3  # Large model
@pytest.mark.expensive
def test_architecture_workflow():
    ...
```

**Deliverables:**

- [ ] Unit tests for Tier 0 tools (in `agentic-workflows-v2/tests/`)
- [ ] Integration tests per tier
- [ ] CI configuration with tier-based test selection
- [ ] Documentation (in `agentic-workflows-v2/docs/`)

---

## Current Implementation Status (February 3, 2026)

| Phase | Component | Status | Tests | Notes |
|-------|-----------|--------|-------|-------|
| **Phase 0** | Tools & Registry | ✅ Complete | 27 pass | File ops, transforms, auto-discovery |
| **Phase 1** | Contracts | ✅ Complete | 35 pass | Pydantic v2 messages, schemas |
| **Phase 2** | Model Router | ✅ Complete | 40 pass | Smart routing, circuit breakers, stats |
| **Phase 3a** | Engine Core | ✅ Complete | — | Context, Step, StepExecutor, Pipeline |
| **Phase 3b** | DAG Engine | ✅ Complete | — | DAG, DAGExecutor, StepState |
| **Phase 3c** | Expressions | ✅ Complete | — | `${ctx.var}` syntax, safe eval |
| **Phase 4** | Agents | ⚠️ Partial | 0 tests | Base, Coder, Reviewer exist (mocked LLM) |
| **Phase 5** | CLI | ❌ Not Started | — | Empty `cli/__init__.py` |
| **Phase 6** | Workflows | ❌ Not Started | — | Empty `workflows/definitions/` |

**Total Tests: 176 passing**

---

## Parallel Execution Plan (Next Stages)

The remaining work can be executed in two parallel lanes after completing the foundation stage:

```
                    ┌─────────────────────────────────────────┐
                    │        Stage A: Engine Tests            │
                    │   (DAG, Executor, Expressions, State)   │
                    │          Effort: 1-2 days               │
                    └─────────────────────────────────────────┘
                                       │
              ┌────────────────────────┴────────────────────────┐
              ↓                                                 ↓
┌─────────────────────────────────┐            ┌─────────────────────────────────┐
│     Stage B: LLM Integration    │            │   Stage C: Workflow Definitions │
│   (Wire agents to SmartRouter)  │            │     (YAML definitions + loader) │
│       Effort: 2-3 days          │            │        Effort: 1-2 days         │
└─────────────────────────────────┘            └─────────────────────────────────┘
              │                                                 │
              └────────────────────────┬────────────────────────┘
                                       ↓
                    ┌─────────────────────────────────────────┐
                    │          Stage D: CLI                   │
                    │   (Typer commands: run, list, validate) │
                    │          Effort: 1-2 days               │
                    └─────────────────────────────────────────┘
                                       │
                                       ↓
                    ┌─────────────────────────────────────────┐
                    │    Stage E: Cleanup & Documentation     │
                    │  (Remove duplicates, update TEST_SUMMARY)│
                    │          Effort: 30 min                 │
                    └─────────────────────────────────────────┘
```

### Stage A: Engine Tests (Priority: HIGH)

The DAG engine is implemented but has zero test coverage.

**Deliverables:**

- [x] `tests/test_dag.py` — DAG validation, cycle detection, topological ordering
- [x] `tests/test_dag_executor.py` — Parallel execution, failure cascade/skipping
- [x] `tests/test_expressions.py` — Variable resolution, safe eval, comparison operators
- [x] `tests/test_step_state.py` — State machine transitions

**Implementation Notes (Completed 2026-02-03):**

- Created `tests/test_step_state.py` with 18 tests for StepState enum and StepStateManager
- Extended `tests/test_dag.py` with comprehensive validation, cycle detection, and topological ordering tests
- Created `tests/test_dag_executor.py` with parallel execution, concurrency limits, and failure cascade tests
- Created `tests/test_expressions.py` with variable resolution, comparisons, boolean operators, and safety tests
- All 89 Stage A/C tests passing

### Stage B: Agents & Orchestration (Parallel with C)

Wire agents to SmartModelRouter and refactor Orchestrator to use the new DAG engine.

**Tasks:**

- [x] Update `agents/base.py` to inject `SmartModelRouter` + `LLMClientWrapper`
- [x] Implement `_call_model()` in `CoderAgent` using real router
- [x] **Refactor `OrchestratorAgent` to use `DAG` engine** (replace `PipelineBuilder`)
- [x] Update `OrchestratorAgent` to execute using `DAGExecutor`
- [x] Add `tests/test_agents_integration.py` (mocked HTTP)
- [x] Add `tests/test_agents_orchestrator.py` (DAG generation & execution)

**Implementation Notes (Completed 2026-02-04):**

- Created `models/backends.py` with `GitHubModelsBackend`, `OllamaBackend`, `MockBackend`
- Updated `BaseAgent.__init__` to accept `llm_client` parameter
- `CoderAgent._call_model()` now uses real LLM when backend is configured
- Added `OrchestratorAgent.execute_as_dag()` method (preferred over legacy `execute_as_pipeline()`)
- All 77 agent/DAG tests passing (18 orchestrator tests + 8 integration tests + 51 others)

### Stage C: Workflow Definitions (Parallel with B)

Create concrete workflow YAML definitions and loader.

**Tasks:**

- [x] Create `workflows/definitions/code_review.yaml`
- [x] Create `workflows/definitions/fullstack_generation.yaml`
- [x] Implement `workflows/loader.py` (YAML → DAG)
- [x] Add `tests/test_workflow_loader.py`

**Implementation Notes (Completed 2026-02-03):**

- Created `code_review.yaml` workflow with 5-step DAG (parse → style/complexity → review → summary)
- Created `fullstack_generation.yaml` workflow with 7-step diamond pattern (arch → api/frontend/migrations → e2e → review → assemble)
- Implemented `WorkflowLoader` with YAML parsing, input/output schemas, caching, and convenience functions
- Created `tests/test_workflow_loader.py` with 20 tests for loading, DAG construction, inputs/outputs, caching, and error handling
- Exported `load_workflow()`, `get_dag()`, and classes from `workflows/__init__.py`

### Stage D: CLI Implementation

Add Typer-based CLI after B & C complete.

**Commands:**

- [x] `agentic run <workflow> --input <file.json>` (Static DAG)
- [x] `agentic orchestrate "task description"` (Dynamic DAG via Orchestrator)
- [x] `agentic list workflows|agents|tools`
- [x] `agentic validate <workflow.yaml>`

**Implementation Notes (Completed 2026-02-03):**

- Created `cli/main.py` (484 lines) with full Typer-based CLI
- Rich console output with tables, trees, and progress spinners
- Commands implemented:
  - `run` - Execute workflows with input JSON, dry-run mode, verbose output, JSON output file
  - `orchestrate` - Dynamic workflow generation (requires LLM backend)
  - `list` - Show workflows/agents/tools in formatted tables
  - `validate` - Validate YAML workflow with detailed DAG visualization
  - `version` - Show version info
- Entry point: `python -m agentic_v2.cli.main` or via exported `app`
- Added `tests/test_cli.py` with 22 tests covering all commands
- Added `pyproject.toml` entry point `agentic = "agentic_v2.cli:main"`

### Stage E: File Cleanup

Move/remove misplaced files.

| Current Location | Action |
|------------------|--------|
| `agentic_v2/agentmessage.py` | **Deleted** (duplicate of `contracts/messages.py`) |
| `agentic_v2/basetool.py` | **Deleted** (duplicate of `tools/base.py` + `builtin/`) |
| `agentic_v2/agenticworkflowsv2config.py` | **Deleted** (legacy scaffolding) |

**Implementation Notes (Completed 2026-02-03):**

- Verified strict redundancy of all 3 files before deletion
- Confirmed no import references existed in checking `src/` and `tests/`
- Validated that `contracts/messages.py`, `tools/base.py`, `tools/builtin/file_ops.py`, and `tools/builtin/transform.py` provide superior supersets of functionality

---

## 🏁 Project Completion Summary

**Status**: 100% Complete
**Completion Date**: 2026-02-03

All 5 stages of the Agentic Workflows V2 Refactoring Plan are complete:

1. **Stage A (Engine)**: Built `DAG`, `DAGExecutor`, `ExecutionContext`, `StepDefinition`. (44 tests)
2. **Stage B (Agents)**: Refactored `OrchestratorAgent`, injected `SmartModelRouter`, wired `CoderAgent` to real LLMs. (77 tests total)
3. **Stage C (Workflows)**: Implemented YAML-based workflows (`code_review`, `fullstack_generation`) and `WorkflowLoader`. (97 tests total)
4. **Stage D (CLI)**: Created comprehensive Typer CLI (`agentic run`, `orchestrate`, `validate`).
5. **Stage E (Cleanup)**: Removed legacy technical debt.

**Key Features Delivered:**

- **True Parallel Execution**: DAG engine supports concurrent step execution
- **Model Routing**: Router selects models (Tier 0-3) based on task complexity
- **Dynamic Orchestration**: `OrchestratorAgent` can plan and execute workflows on the fly
- **Developer DX**: Strong typing, Pydantic v2 validation, CLI tooling, and YAML definitions

**Next Steps:**

- User Acceptance Testing (UAT) with real workloads
- Creating more workflow definitions
- Documentation expansion (`docs/`)

### Why B & C Can Run Concurrently

| Stage B (Agents & Orchestration) | Stage C (Workflow Definitions) |
|---------------------------|-------------------------------|
| Modifies `agents/` package | Modifies `workflows/` package |
| Tests agent → LLM communication | Tests YAML → DAG parsing |
| Refactors `Orchestrator` to DAG | Defines static DAG structure |

### Timeline Estimate

| Day | Lane 1 | Lane 2 |
|-----|--------|--------|
| **1-2** | Stage A: Engine Tests | Stage A: Engine Tests |
| **3-4** | Stage B: LLM Integration | Stage C: Workflow Definitions |
| **5** | Stage D: CLI | Stage D: CLI |
| **5+** | Stage E: Cleanup | — |

**Total: ~5 days** (vs 7-9 days sequential)

---

## Summary: Task → Tier Mapping

| Task Category | Tier | Model Size | Example Models |
|---------------|------|------------|----------------|
| **File Operations** | 0 | None | Pure Python |
| **Template Rendering** | 0 | None | Jinja2 |
| **Config Merge/Transform** | 0 | None | Python dict ops |
| **Code Formatting** | 1 | 1-3B | phi3:mini, qwen2.5:1.5b |
| **Docstring Generation** | 1 | 1-3B | phi3:mini |
| **Simple Validation** | 1 | 1-3B | phi3:mini |
| **Code Generation** | 2 | 7-14B | qwen2.5-coder:14b, deepseek-coder:16b |
| **Code Review** | 2 | 7-14B | qwen2.5-coder:14b |
| **Test Generation** | 2 | 7-14B | deepseek-coder:16b |
| **Refactoring** | 2 | 7-14B | qwen2.5-coder:14b |
| **Architecture Design** | 3 | 32B+ | gpt-4o, qwen2.5:32b |
| **Quality Evaluation** | 3 | 32B+ | gpt-4o |
| **Multi-Step Planning** | 3 | 32B+ | gpt-4o |
| **Synthesis/Combining** | 3 | 32B+ | gpt-4o-mini, claude |

---

## Quick Start: Stage 0 - Validate First

**STOP! Before writing any code:**

```powershell
# Step 1: Run the ReAct validator against plans
cd d:\source\prompts

# Use the Architecture Plan Validator prompt with your preferred LLM
# Input: This plan + architecture docs
# Output: Validation report with GO/NO-GO
```

Only after validation passes, create the structure:

```powershell
# Step 2: Create the independent package structure
cd d:\source\prompts
mkdir agentic-workflows-v2\src\agentic_v2\contracts
mkdir agentic-workflows-v2\src\agentic_v2\tools\builtin
mkdir agentic-workflows-v2\src\agentic_v2\engine\patterns
mkdir agentic-workflows-v2\src\agentic_v2\agents\implementations
mkdir agentic-workflows-v2\src\agentic_v2\models
mkdir agentic-workflows-v2\src\agentic_v2\workflows\definitions
mkdir agentic-workflows-v2\src\agentic_v2\cli\commands
mkdir agentic-workflows-v2\src\agentic_v2\evaluation\rubrics
mkdir agentic-workflows-v2\tests
mkdir agentic-workflows-v2\docs

# Create __init__.py files
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\contracts\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\tools\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\tools\builtin\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\engine\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\engine\patterns\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\agents\__init__.py
"" | Out-File -Encoding utf8 agentic-workflows-v2\src\agentic_v2\agents\implementations\__init__.py
```

Then proceed to Phase 1 - implement Tier 0 tools which need no LLM at all!

---

## Companion Files

| File | Purpose |
|------|---------|
| [`agentic-workflows-v2-prompts.md`](agentic-workflows-v2-prompts.md) | **Ready-to-use prompts** with full context for each phase |
| `agentic-workflows-v2/README.md` | Quick start guide (created in Phase 0) |
| `agentic-workflows-v2/docs/` | Package documentation (created in Phase 6) |

## Prompt Usage Quick Start

1. Open [`agentic-workflows-v2-prompts.md`](agentic-workflows-v2-prompts.md)
2. Find the phase you're implementing (e.g., "Prompt 0.1: Create Package Structure")
3. Copy the entire prompt block (including `<TASK>`, `<CONTEXT>`, etc.)
4. Send to your LLM (recommend `gh:meta/llama-3.3-70b-instruct` for tier 3 tasks)
5. Apply the generated code to your codebase
6. Run the validation prompt before moving to next phase

**Model Recommendations by Phase:**

| Phase | Tier | Recommended Model |
|-------|------|-------------------|
| 0-1 | 1-2 | `gh:phi-4` or any |
| 2-3 | 2 | `gh:phi-4`, `ollama:qwen2.5-coder:14b` |
| 4-6 | 3 | `gh:meta/llama-3.3-70b-instruct` |
