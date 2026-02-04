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

## Phase 4: Architects & Evaluators (Large Models)

**Duration:** 2-3 days  
**Models Required:** Tier 3 (large: 32B+ or cloud)

### 4.1 High-Reasoning Agents

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

## Quick Start: Stage 0 - Validate First!

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
