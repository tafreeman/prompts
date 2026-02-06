# ⚠️ DEPRECATED: Multi-Agent Workflows (Legacy)

**Status:** Deprecated (Superseded by `agentic-workflows-v2`)

This package is the legacy implementation of the multi-agent system. It is kept for reference but should not be used for new development. Please direct all new work to the `agentic-workflows-v2` package.

---

# Multi-Agent Workflows

A comprehensive, standalone multi-agent development system for software engineering workflows. This package provides pre-built workflows for common development tasks with full logging, evaluation, and scoring capabilities.

## Features

- **4 Pre-built Workflows**
  - Full-Stack Application Generation
  - Legacy Code Refactoring & Modernization
  - Intelligent Bug Triage & Automated Fixing
  - Architecture Evolution & Technical Debt Assessment

- **Unified Model Access**
  - Local ONNX models (Phi-4, Phi-3.5, Mistral)
  - Ollama integration
  - GitHub Models API
  - Azure OpenAI / Azure Foundry
  - OpenAI, Anthropic, Google AI

- **Comprehensive Logging**
  - Hierarchical 5-level logging (workflow → step → agent → model → tool)
  - JSON export for programmatic analysis
  - Markdown export for human review

- **Evaluation Framework**
  - Rubric-based scoring
  - Golden output comparison
  - Multi-run aggregation
  - Report generation

## Installation

```bash
# From source
pip install -e .

# With optional dependencies
pip install -e ".[all]"  # Everything
pip install -e ".[local]"  # Local ONNX models
pip install -e ".[ollama]"  # Ollama support
pip install -e ".[cloud]"  # Cloud providers
pip install -e ".[dev]"  # Development tools
```

## Quick Start

### Using the Workflow Engine

```python
import asyncio
from multiagent_workflows import ModelManager, WorkflowEngine, VerboseLogger

async def main():
    # Initialize components
    model_manager = ModelManager(allow_remote=True)
    engine = WorkflowEngine(model_manager)
    
    # Execute a workflow
    result = await engine.execute_workflow(
        workflow_name="fullstack_generation",
        inputs={
            "requirements": "Build a task management app with user auth..."
        }
    )
    
    print(f"Success: {result.success}")
    print(f"Outputs: {result.outputs.keys()}")

asyncio.run(main())
```

### Using Individual Agents

```python
from multiagent_workflows import ModelManager
from multiagent_workflows.agents import ArchitectAgent
from multiagent_workflows.core.agent_base import AgentConfig

async def design_architecture():
    model_manager = ModelManager()
    
    config = AgentConfig(
        name="Architect",
        role="System Designer",
        model_id="gh:gpt-4o",
        system_prompt="Design scalable architectures...",
    )
    
    agent = ArchitectAgent(config, model_manager)
    
    result = await agent.execute(
        task={"requirements": "Build a microservices platform..."},
        context={}
    )
    
    return result.output["architecture"]
```

### Running Examples

```bash
# Full workflow demo
python examples/fullstack_example.py

# Simple model manager test
python examples/fullstack_example.py --simple
```

## Project Structure

```
multiagent-workflows/
├── config/                    # Configuration files
│   ├── models.yaml           # Model definitions and routing
│   ├── workflows.yaml        # Workflow definitions
│   ├── agents.yaml           # Agent configurations
│   ├── rubrics.yaml          # Scoring rubrics
│   └── evaluation.yaml       # Evaluation settings
├── src/multiagent_workflows/
│   ├── core/                 # Core components
│   │   ├── model_manager.py  # Unified model access
│   │   ├── agent_base.py     # Base agent class
│   │   ├── workflow_engine.py # Workflow orchestration
│   │   ├── logger.py         # Verbose logging
│   │   ├── evaluator.py      # Evaluation framework
│   │   └── tool_registry.py  # Tool registration
│   ├── agents/               # Agent implementations
│   ├── workflows/            # Workflow implementations
│   └── evaluation/           # Evaluation components
├── examples/                 # Usage examples
├── tests/                    # Test suite
└── evaluation/               # Evaluation data and results
```

## Workflows

### 1. Full-Stack Application Generation

Transforms business requirements into a complete, deployable application.

**Agents**: Requirements Analyst → Technical Architect → Database Designer → API Designer → Code Generator → Code Reviewer → Test Generator → Documentation Agent

**Inputs**: Business requirements, optional UI mockups
**Outputs**: Backend code, frontend code, tests, documentation

### 2. Legacy Code Refactoring

Analyzes legacy codebases and systematically modernizes them.

**Agents**: Code Archaeologist → Dependency Mapper → Pattern Detector → Test Analyst → Code Transformer → Migration Agent → Validator

**Inputs**: Legacy codebase path, target framework
**Outputs**: Refactored code, migration plan, test suite

### 3. Bug Triage & Automated Fixing

Analyzes bug reports, identifies root causes, and generates fixes.

**Agents**: Bug Analyst → Reproduction Agent → Tracer → Root Cause Analyzer → Fix Generator → Test Generator → Validator → PR Creator

**Inputs**: Bug report, codebase path
**Outputs**: Fix patch, regression tests, PR content

### 4. Architecture Evolution

Assesses technical debt and creates evolution roadmaps.

**Agents**: Architecture Scanner → Debt Assessor → Pattern Matcher → Scalability Analyzer → Security Auditor → Modernization Planner → ADR Generator

**Inputs**: Codebase path, business context
**Outputs**: Assessment report, evolution roadmap, ADRs

## Configuration

### Model Routing

```yaml
# config/models.yaml
routing:
  code_gen:
    preferred: ["gh:gpt-4o", "ollama:qwen2.5-coder:14b"]
    fallback: ["local:phi4mini"]
  reasoning:
    preferred: ["gh:o3-mini", "gh:deepseek-r1"]
    fallback: ["ollama:deepseek-r1:14b"]
```

### Scoring Rubrics

```yaml
# config/rubrics.yaml
rubrics:
  fullstack_generation:
    total_points: 100
    pass_threshold: 70
    categories:
      functional_correctness:
        weight: 40
      code_quality:
        weight: 25
      completeness:
        weight: 20
      documentation:
        weight: 10
      efficiency:
        weight: 5
```

## Evaluation

### Running Evaluations

```python
from multiagent_workflows.core.evaluator import WorkflowEvaluator

evaluator = WorkflowEvaluator()
result = await evaluator.evaluate_workflow(
    workflow_name="fullstack_generation",
    output=workflow_output,
    golden=golden_output,
)

print(f"Score: {result.total_score}/{result.max_score}")
print(f"Grade: {result.grade}")
print(f"Passed: {result.passed}")
```

### Generating Reports

```python
results = [result1, result2, result3]
report = await evaluator.generate_report(
    results,
    output_path=Path("evaluation/reports/summary.md"),
)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/multiagent_workflows --cov-report=html

# Run specific test file
pytest tests/test_model_manager.py -v
```

## Integration with Repository

This package integrates with existing repository patterns:

- **Model Access**: Wraps `tools/llm/llm_client.py` for consistent model access
- **Evaluation**: Compatible with `tools/prompteval/` scoring patterns
- **Rubrics**: Uses similar structure to `tools/rubrics/unified-scoring.yaml`

## Architecture review & findings

I performed a focused review of the key files and folders that implement the workflow engine, agents, evaluation, scoring, and logging. Below are concise findings, concrete issues observed, and recommended actions to improve correctness, maintainability, and alignment with canonical benchmarks (e.g., SWE-Bench).

Files reviewed (representative):

- `src/multiagent_workflows/core/agent_base.py`
- `src/multiagent_workflows/core/evaluator.py`
- `src/multiagent_workflows/core/logger.py`
- `src/multiagent_workflows/server/run_manager.py`
- `src/multiagent_workflows/server/benchmarks.py`
- `src/multiagent_workflows/server/dataset_loader.py`
- `src/multiagent_workflows/evaluation/scorer.py`
- `src/multiagent_workflows/agents/*.py`

High-level findings

- Clear, modular architecture: core components (agents, model manager, workflows, logger, evaluator) are separated and easy to reason about.
- Robust hierarchical logging (`VerboseLogger`) with JSON/Markdown export—this is a strength.
- `AgentBase` provides rich functionality (retries, timeouts, tool invocation hooks, structured logging) and is a solid foundation for agents.

Key issues and pitfalls

- Scoring mismatch for SWE-Bench: `benchmarks.py` declares `evaluation_method="execution"` and `metrics=["resolved_rate"]`, but `server/run_manager.py` scores SWE-bench tasks using text similarity (`difflib.SequenceMatcher`). This yields misleading results for patch-bug benchmarks where execution (apply patch + run tests) is the ground truth.
- `run_manager` currently treats patch matching as the canonical metric. Recommendation: either implement an execution harness (Docker + repo clone + apply patch + test run) for SWE-Bench tasks or explicitly label the current scores as `text_similarity` (proxy) and add a separate `execution` scorer later.
- Overreliance on SequenceMatcher: `core/evaluator.py` uses SequenceMatcher-based similarity for many rubric categories. Similarity is a weak signal for correctness for code/patches; where possible prefer execution-based checks, AST-level diffs, or semantic equivalence checks.
- Minimal package-level exports: several `__init__.py` files are intentionally minimal/blank (fine), but consider exporting common symbols (e.g., agent classes) to simplify imports and improve discoverability.
- Agent base vs concrete agents: concrete agents implement similar prompt-building and post-processing logic. Consider moving common helpers (prompt template composition, parse helpers) into `AgentBase` or a shared mixin to reduce duplication.
- Autosave & persistence: `run_manager` autosaves JSON to `evaluations/results/` which is good, but there are places with `print()` debug outputs—prefer routing all messages through `VerboseLogger` for consistent structured logs.
- Test coverage assumptions: tests exercise dataset loader and model routing, but there are no integration tests for execution-based evaluation (understandable given infra requirements). If you plan to add execution scoring, add sandboxed integration tests that run in containers.

Concrete recommendations (priority order)

1. Fix SWE-Bench scoring mismatch

- Implement an optional execution harness (containerized) that: clones repo at `base_commit`, applies generated patch, runs `test_patch` tests, and returns `resolved` boolean.
- Add an `ExecutionScorer` class under `evaluation/` and wire it to `run_manager` when `benchmark.evaluation_method == 'execution'`.

2. Label current similarity scorer as a proxy

- Rename `total_score` → `text_similarity_score` in `run_manager` outputs for patch tasks, and document this clearly in the README.

3. Consolidate prompt utilities

- Move `_build_prompt`, parsing, and formatting helpers into `AgentBase` (or a PromptMixin) so concrete agents remain focused on role-specific logic.

4. Standardize logging usage

- Replace ad-hoc `print()` statements in server components with calls to `VerboseLogger` to keep structured logs complete.

5. Add explicit exports for agents

- Populate `src/multiagent_workflows/agents/__init__.py` to export available agent classes for easier imports.

6. Add integration tests for execution scoring (optional)

- Create a small, sandboxed integration test that verifies `ExecutionScorer` behavior using a tiny Git repo fixture and pytest + Docker.

Potential technical risks and mitigations

- Running tests inside containers is resource-heavy and introduces security considerations. Mitigate by using ephemeral Docker containers with constrained resources, and fail gracefully if Docker is not available (fall back to proxy scoring).
- AST/semantic comparison can be complex; prefer simpler heuristics first (unit tests pass) and add semantic diffing as a secondary improvement.

Next steps I can take for you

- Implement the `ExecutionScorer` skeleton and wire it into `run_manager` behind a feature flag.
- Rename and document the current similarity metric to avoid confusion.
- Refactor common prompt-building helpers into `AgentBase`.

If you'd like, I can proceed to implement any of the recommended fixes (starting with the SWE-Bench scoring alignment). Tell me which item to start with and I will create an implementation plan and patches.

## Contributing

1. Install development dependencies: `pip install -e ".[dev]"`
2. Run tests: `pytest`
3. Format code: `black src/ tests/`
4. Lint: `ruff check src/ tests/`

## License

MIT License - See LICENSE file for details.
