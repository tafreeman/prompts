---
title: Full-Stack Multi-Agent Development System Implementation
description: Comprehensive multi-agent system for full-stack software development workflows with evaluation framework integration
difficulty: expert
audience:
  - senior-engineer
  - machine-learning-engineer
platforms:
  - github-copilot
  - claude
  - gemini
tags:
  - multi-agent
  - full-stack
  - evaluation
  - workflow
  - agentic
---

## Description

This prompt guides the creation of a comprehensive multi-agent development tool that integrates with this repository's existing evaluation framework, model access patterns, and tooling infrastructure. The system implements multiple pre-built software development workflows with comprehensive logging, performance evaluation, and scoring rubrics.

## Variables

- `PROJECT_PATH`: Path to create the new project (default: `./multiagent-workflows/`)
- `WORKFLOW_FOCUS`: Which workflow(s) to prioritize (fullstack|refactoring|bugfix|architecture|all)

## Prompt

### System Prompt

You are an expert software architect specializing in multi-agent AI systems and software development automation. You will create production-ready multi-agent workflows that integrate seamlessly with an existing prompt evaluation repository.

### User Prompt

## Full-Stack Multi-Agent Development System Implementation

## Context

You are working within the `d:\source\prompts` repository. Create a **NEW standalone project** in its own folder. This repository contains reference implementations you can learn from:

- **Evaluation Framework**: `tools/prompteval/` - study for evaluation patterns
- **LLM Integration**: `tools/llm_client.py` (unified dispatcher), `tools/local_model.py` (ONNX), `tools/windows_ai.py` (NPU)
- **Model Access**: Local ONNX, Windows AI NPU, GitHub Models, Azure Foundry, OpenAI
- **Reference Implementation**: `multiagent-dev-system/` - existing partial implementation to learn from (do NOT modify)
- **Prompt Library**: `prompts/` with agents, techniques, frameworks, and system prompts

## Objective

Create a comprehensive multi-agent development tool that:

1. Integrates with existing repository model access patterns (`tools/llm_client.py`, `tools/local_model.py`)
2. Integrates with existing evaluation framework (`tools/prompteval/`)
3. Implements multiple pre-built software development workflows
4. Provides comprehensive logging and performance evaluation
5. Uses scoring guidelines with defined grading rubrics (see `tools/rubrics/`)
6. Provides easy integration points for the broader repository

## Repository Analysis Required

First, examine these existing components in the repository:

- **Evaluation Framework**: `tools/prompteval/` - study how it processes prompts, scores outputs, and logs results
- **Model Access**: `tools/llm_client.py`, `tools/local_model.py`, `tools/windows_ai.py`
- **Rubrics**: `tools/rubrics/` - existing scoring rubric definitions
- **Configuration**: `.env`, `pyproject.toml` for credential management
- **Logging Infrastructure**: Existing logging patterns in `tools/`
- **Agent Implementations**: `prompts/agents/`, `multiagent-dev-system/agents/`

## Available Model Ecosystem

The system has access to (via `tools/llm_client.py` prefixes):

- **Local ONNX (`local:`)**: phi4, phi4mini, phi3.5, phi3.5-vision, mistral-7b
- **Windows AI NPU (`windows-ai:`)**: phi-silica (Copilot+ PCs)
- **GitHub Models (`gh:`)**: gpt-4o, gpt-4o-mini, o3-mini, o4-mini, deepseek-r1, codestral-2501
- **Azure Foundry (`azure-foundry:`)**: phi4mini
- **OpenAI (`gpt-`)**: gpt-4o, gpt-4.1

## Project Structure

Create a **NEW** project folder: `./multiagent-workflows/`

This should be a completely standalone, self-contained project that can be extracted and used independently.

```text
multiagent-workflows/
├── README.md                    # Quick start guide
├── pyproject.toml               # Package configuration
├── requirements.txt             # Dependencies
├── src/
│   └── multiagent_workflows/    # Main Python package
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── model_manager.py     # Unified model access
│       │   ├── logger.py            # Hierarchical logging
│       │   ├── evaluator.py         # Workflow evaluation
│       │   └── scorer.py            # Scoring with rubrics
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py              # Base agent class
│       │   └── ... (workflow-specific agents)
│       ├── workflows/
│       │   ├── __init__.py
│       │   ├── base.py              # Base workflow class
│       │   ├── fullstack_generation.py
│       │   ├── legacy_refactoring.py
│       │   ├── bug_triage.py
│       │   └── architecture_evolution.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── configs/
│   ├── models.yaml              # Model configuration
│   ├── evaluation.yaml          # Evaluation settings
│   └── rubrics.yaml             # Scoring rubrics
├── datasets/                    # Evaluation datasets
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   └── workflows/
├── examples/
│   ├── fullstack_example.py
│   └── refactoring_example.py
└── tests/
    ├── conftest.py
    ├── test_model_manager.py
    ├── test_workflows.py
    └── test_agents.py
```

## Evaluation Framework Integration

### Critical Requirements

1. **Dataset Integration**: Support HumanEval, MBPP, SWE-bench, custom datasets
2. **Verbose Logging**: Log every agent I/O, model call, tool invocation with hierarchical structure
3. **Scoring**: Use defined rubrics, compare to golden outputs, multiple metrics
4. **Performance**: Track latency, tokens, costs, success rates

**IMPORTANT**: Reuse existing `tools/prompteval/` patterns. Study its scoring and logging implementation before creating new code.

## Workflow Implementations

### Workflow 1: Full-Stack Application Generation

**Agents**: Vision (gh:openai/gpt-4o), Requirements (gh:gpt-4o-mini), Architect (gh:gpt-4o), DB Designer (gh:gpt-4o), API Designer (gh:gpt-4o-mini), Frontend (gh:gpt-4o), Backend (gh:gpt-4o-mini), Integration (local:phi4mini), Reviewer (gh:o4-mini), Tests (gh:gpt-4o), Docs (gh:gpt-4o-mini)

**Dataset**: Custom fullstack with requirements, mockups, golden application code

**Reference Resources**:

- Martin Fowler - Domain-Driven Design: <https://martinfowler.com/bliki/DomainDrivenDesign.html>
- Martin Fowler - Bounded Context: <https://martinfowler.com/bliki/BoundedContext.html>

### Workflow 2: Legacy Code Refactoring

**Agents**: Archaeologist (gh:deepseek-r1), Dependency Mapper (local:phi4), Pattern Detector (gh:o3-mini), Test Analyst (local:phi4), Safety Net (gh:gpt-4o), Planner (gh:gpt-4o), Transformer (gh:gpt-4o), Migrator (local:phi4), Validator (gh:o4-mini), Docs (local:phi4)

**Dataset**: Legacy code with documented issues, golden refactored version

**Reference Resources**:

- Martin Fowler - Strangler Fig Application: <https://martinfowler.com/bliki/StranglerFigApplication.html>
- Refactoring Guru - Catalog: <https://refactoring.guru/refactoring/catalog>

### Workflow 3: Bug Triage & Fixing

**Agents**: Bug Analyst (gh:gpt-4o-mini), Reproduction (local:phi4), Tracer (gh:deepseek-r1), Root Cause (gh:o3-mini), Fix Generator (gh:gpt-4o), Tests (gh:gpt-4o), Validator (local:phi4), Side Effects (gh:o4-mini), Docs (local:phi4), PR Creator (local:phi4mini)

**Dataset**: SWE-bench - real GitHub issues with golden patches

**Reference Resources**:

- SWE-bench Official: <https://www.swebench.com/>
- SWE-bench GitHub: <https://github.com/princeton-nlp/SWE-bench>

### Workflow 4: Architecture Evolution

**Agents**: Scanner (gh:deepseek-r1), Debt Assessor (gh:o3-mini), Pattern Matcher (local:phi4), Scalability (gh:gpt-4o), Security (gh:o4-mini), Planner (gh:gpt-4o-mini), Cost Estimator (local:phi4), ADR Generator (gh:gpt-4o-mini), Roadmap (local:phi4), Reporter (local:phi4)

**Dataset**: Architecture case studies with golden evolution plans

**Reference Resources**:

- ThoughtWorks - Building Evolutionary Architectures: <https://www.thoughtworks.com/insights/books/building-evolutionary-architectures>
- ADR GitHub: <https://adr.github.io/>

## Implementation Details

### Model Manager

```python
class ModelManager:
    """Wraps tools/llm_client.py for unified model access"""
    async def generate(model_id, prompt, context, **params) -> str
    async def check_availability(model_id) -> bool
    async def list_models(provider=None) -> List[dict]
    def get_optimal_model(task_type, complexity, prefer_local) -> str
```

### Verbose Logger

```python
class VerboseLogger:
    """Hierarchical logging for all agent interactions"""
    def log_workflow_start/complete(...)
    def log_step_start/complete(...)
    def log_agent_start/output(...)
    def log_model_call/response(...)
    def log_tool_invocation(...)
    def get_structured_log() -> dict
    def export_to_json/markdown(...)
```

### Evaluator

```python
class WorkflowEvaluator:
    """Integrates with tools/prompteval for workflow evaluation"""
    async def evaluate_workflow(workflow_name, dataset_name, num_samples) -> dict
    async def load_dataset(dataset_name) -> List[dict]
    async def run_sample(workflow, sample) -> dict
    def score_output(output, golden, rubric) -> dict
    def generate_report(results) -> dict
```

### Scorer with Rubrics

```python
class Scorer:
    """Uses rubrics from tools/rubrics/ or configs/rubrics.yaml"""
    def score(output, golden, rubric_name) -> dict
    def score_functional_correctness(...)
    def score_code_quality(...)
    def score_completeness(...)
    def score_documentation(...)
    def score_efficiency(...)
```

## Configuration Files

### configs/evaluation.yaml

```yaml
evaluation:
  enabled: true
  datasets:
    humaneval: {type: "code_generation", cache_path: "./datasets/humaneval"}
    swe_bench: {type: "bug_fixing", cache_path: "./datasets/swe_bench"}
  logging:
    level: "DEBUG"
    capture: {agent_inputs: true, model_calls: true, timing: true, tokens: true}
  metrics:
    - {name: "functional_correctness", type: "pass_at_k", k_values: [1, 5, 10]}
    - {name: "generation_time", type: "duration"}
  scoring:
    normalize: true
    weights: {correctness: 0.5, code_quality: 0.25, efficiency: 0.15}
```

### configs/rubrics.yaml

```yaml
rubrics:
  fullstack_generation:
    total_points: 100
    categories:
      functional_correctness:
        weight: 40
        criteria:
          - {name: "Requirements Coverage", points: 15}
          - {name: "Working Application", points: 15}
          - {name: "Test Pass Rate", points: 10}
      code_quality:
        weight: 25
        criteria:
          - {name: "Architecture Quality", points: 8}
          - {name: "Code Standards", points: 7}
          - {name: "Documentation", points: 5}
          - {name: "Error Handling", points: 5}
      efficiency:
        weight: 15
        criteria:
          - {name: "Performance", points: 8}
          - {name: "Resource Usage", points: 7}
      completeness:
        weight: 20
        criteria:
          - {name: "All Features Implemented", points: 10}
          - {name: "Edge Cases Handled", points: 10}
```

## Testing & Quality Requirements

- Unit tests for all core components (>80% coverage)
- Integration tests for workflow execution
- Mock model responses for testing
- Performance benchmarks
- Example workflows with sample data
- Tests should extend patterns in `multiagent-dev-system/tests/`

## Documentation Requirements

- README with quick start guide
- Architecture documentation with diagrams
- API reference for all public interfaces
- Workflow documentation with examples
- Configuration guide
- Integration guide showing how to use with existing `tools/`

## Research References

### Agent Frameworks

- AutoGen: <https://microsoft.github.io/autogen/stable/>
- CrewAI: <https://docs.crewai.com/>
- LangGraph: <https://docs.langchain.com/oss/python/langgraph/overview>

### Software Engineering Automation

- SWE-agent: <https://swe-agent.com/latest/>
- Cognition Labs (Devin): <https://www.cognition-labs.com/blog>

### Code Generation & Patterns

- GitHub Copilot Prompting Guide: <https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/>
- Patterns.dev: <https://www.patterns.dev/>

### Multi-Agent Systems

- AutoGen Paper (arXiv): <https://arxiv.org/abs/2308.08155>
- LLM Powered Autonomous Agents (Lilian Weng): <https://lilianweng.github.io/posts/2023-06-23-agent/>

## Success Criteria

1. ✅ All 4 workflows fully implemented with working code
2. ✅ Model manager integrates all available model types via `tools/llm_client.py`
3. ✅ At least 2 example workflows execute successfully end-to-end
4. ✅ Tests pass with >80% coverage
5. ✅ Documentation is comprehensive with examples
6. ✅ Integration points with existing `tools/` are clear
7. ✅ Code follows repository patterns and conventions
8. ✅ Evaluation framework integration with verbose logging
9. ✅ Scoring rubrics implemented and validated

## Execution Instructions

1. Create the new project folder `multiagent-workflows/` with complete structure
2. Study reference implementations in `tools/llm_client.py`, `tools/local_model.py`, and `multiagent-dev-system/`
3. Implement core components in `src/multiagent_workflows/core/` (model_manager.py, logger.py, evaluator.py, scorer.py)
4. Implement base classes for agents and workflows
5. Implement all 4 workflows with their agent chains
6. Create configuration files in `configs/`
7. Add comprehensive tests in `tests/`
8. Write documentation in `docs/`
9. Create working examples in `examples/`
10. Add `pyproject.toml` and `requirements.txt` for standalone installation

## Important Notes

- **Reuse existing repository code** - import from `tools/` instead of duplicating
- **Study existing patterns** before implementing new components
- **Prefer composition over inheritance**
- **Make it modular** - each workflow independently usable
- **Include error handling** - graceful degradation when models unavailable
- **Add comprehensive logging** - every agent interaction logged
- **Make it configurable** - YAML configs for all parameters
- **Document everything** - inline and external docs
- **Integrate evaluation framework** - study and reuse `tools/prompteval/` patterns

## Example

### Input

```yaml
workflow: fullstack_generation
requirements: |
  Build a task management web app with:
  - User authentication
  - CRUD operations for tasks
  - Due date reminders
  - Mobile-responsive UI
mockup_path: ./examples/taskapp_mockup.png
```

### Expected Output

```text
Workflow: fullstack_generation
Status: COMPLETED
Duration: 45.2s
Agents Executed: 11/11

Generated Artifacts:
- database/schema.sql (PostgreSQL schema)
- backend/api/routes.py (FastAPI endpoints)
- backend/models/task.py (SQLAlchemy models)
- frontend/src/App.tsx (React app)
- frontend/src/components/TaskList.tsx
- tests/test_api.py (pytest tests)
- docs/API.md (API documentation)

Evaluation Scores:
- Functional Correctness: 85/100
- Code Quality: 92/100
- Completeness: 88/100
- Overall: 88.3/100

Logs: ./logs/workflow_20260124_021500.json
```
