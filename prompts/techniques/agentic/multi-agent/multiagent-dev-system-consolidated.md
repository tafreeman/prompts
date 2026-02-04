---
title: Full-Stack Multi-Agent Development System - Consolidated Implementation Prompt
description: Unified prompt for creating a comprehensive multi-agent system for full-stack software development workflows with evaluation framework integration, logging, and scoring rubrics
difficulty: expert
audience:
  - senior-engineer
  - machine-learning-engineer
  - ai-engineer
platforms:
  - github-copilot
  - claude
  - gemini
  - antigravity
tags:
  - multi-agent
  - full-stack
  - evaluation
  - workflow
  - agentic
  - logging
  - scoring
---

## Description

This consolidated prompt combines three source prompts into a single executable specification for creating a comprehensive multi-agent development tool. The system integrates with existing repository evaluation frameworks, model access patterns, and tooling infrastructure to implement multiple pre-built software development workflows with comprehensive logging, performance evaluation, and scoring rubrics.

## Variables

- `PROJECT_PATH`: Path to create the new project (default: `./multiagent/langchain//`)
- `WORKFLOW_FOCUS`: Which workflow(s) to prioritize (fullstack|refactoring|bugfix|architecture|all)
- `EVALUATION_ENABLED`: Enable evaluation framework integration (true|false, default: true)
- `LOGGING_LEVEL`: Verbosity level (DEBUG|INFO|WARN|ERROR, default: DEBUG)

## Prompt

### System Prompt

You are an expert software architect specializing in multi-agent AI systems and software development automation. You have deep expertise in:

1. Multi-agent orchestration patterns (AutoGen, CrewAI, LangGraph)
2. Software development lifecycle automation
3. LLM integration across local and cloud providers
4. Evaluation frameworks and scoring methodologies
5. Production-grade logging and observability

Your task is to create a production-ready multi-agent workflow system that integrates seamlessly with an existing prompt evaluation repository. You will produce modular, well-documented, thoroughly tested code that follows established patterns.

### User Prompt

# Full-Stack Multi-Agent Development System Implementation

## Context

You are working within a repository that contains tools for accessing local and cloud AI models AND an existing evaluation framework that analyzes multi-agent workflows using online code datasets with prompts, existing code, and golden output examples.

Your task is to create a NEW standalone, modular multi-agent development tool in its own folder.

### Repository Analysis Required

First, examine these existing tools and frameworks in the repository:

| Component | Location | Purpose |
|-----------|----------|---------|
| **Evaluation Framework** | `tools/prompteval/` | Study how it fetches datasets, processes prompts, compares outputs to golden examples, implements scoring rubrics, and performs verbose logging |
| **LLM Integration** | `tools/llm_client.py` | Unified dispatcher for all model providers |
| **Local Models** | `tools/local_model.py` | ONNX runtime integration |
| **NPU Models** | `tools/windows_ai.py` | Windows AI NPU access |
| **Rubrics** | `tools/rubrics/` | Existing scoring rubric definitions |
| **Configuration** | `.env`, `pyproject.toml` | Credential management and config patterns |
| **Logging Infrastructure** | `tools/` | Existing logging patterns |
| **Agent Implementations** | `prompts/agents/`, `multiagent-dev-system/` | Reference agent implementations |
| **Prompt Library** | `prompts/` | Agents, techniques, frameworks, and system prompts |

## Objective

Create a comprehensive multi-agent development tool that:

1. **Integrates with existing repository model access patterns** (`tools/llm_client.py`, `tools/local_model.py`)
2. **Integrates with existing evaluation framework** (`tools/prompteval/`) for workflow analysis
3. **Implements multiple pre-built software development workflows** (4 workflows)
4. **Provides comprehensive logging and performance evaluation** (hierarchical, verbose logging)
5. **Uses scoring guidelines with defined grading rubrics** (per-workflow rubrics)
6. **Provides easy integration points** for the broader repository
7. **Uses native model access code** when LangChain lacks equivalent capabilities

---

## Available Model Ecosystem

The system has access to these model providers (using `tools/llm_client.py` prefix conventions):

### Local ONNX (NPU-optimized)

| Model ID | Capabilities | Device |
|----------|--------------|--------|
| `local:phi4` | text, reasoning | NPU |
| `local:phi4mini` | text, fast | NPU |
| `local:phi3.5` | text, reasoning | NPU |
| `gh:openai/gpt-4o` | vision, text | NPU |
| `local:mistral-7b` | text, code | CPU/GPU |

### Windows AI NPU

| Model ID | Capabilities | Device |
|----------|--------------|--------|
| `windows-ai:phi-silica` | text | NPU (Copilot+ PCs) |

### Ollama (Local)

| Model ID | Capabilities | Context Length |
|----------|--------------|----------------|
| `ollama:qwen2.5-coder:14b` | code, text | 32768 |
| `ollama:qwen3-coder:30b` | code, text | 32768 |
| `ollama:deepseek-r1:8b` | reasoning, code | 16384 |
| `ollama:deepseek-r1:14b` | reasoning, code | 16384 |
| `ollama:phi4-reasoning` | reasoning | 16384 |

### GitHub Models (Cloud)

| Model ID | Capabilities | Cost Tier |
|----------|--------------|-----------|
| `gh:gpt-4o` | text, reasoning, code | premium |
| `gh:gpt-4o-mini` | text, code | standard |
| `gh:o3-mini` | reasoning, math | premium |
| `gh:o4-mini` | reasoning, review | premium |
| `gh:deepseek-r1` | reasoning, code | premium |
| `gh:codestral-2501` | code | standard |
| `gh:llama-4-scout` | text, code | standard |
| `gh:llama-4-maverick` | text, reasoning | standard |

### Azure Foundry

| Model ID | Capabilities | Device |
|----------|--------------|--------|
| `azure-foundry:phi4mini` | text | cloud |

### OpenAI Direct

| Model ID | Capabilities | Cost Tier |
|----------|--------------|-----------|
| `gpt-4o` | text, reasoning, code | premium |
| `gpt-4.1` | text, reasoning, code | premium |

---

## Project Structure

Create a **NEW** project folder: `./multiagent-workflows/`

This should be a completely standalone, self-contained project that can be extracted and used independently.

```text
multiagent-workflows/
├── README.md                          # Quick start guide + comprehensive documentation
├── pyproject.toml                     # Package configuration (PEP 621)
├── requirements.txt                   # Dependencies for pip install
├── config/
│   ├── models.yaml                    # Model configurations and routing
│   ├── workflows.yaml                 # Workflow definitions
│   ├── agents.yaml                    # Agent role definitions
│   ├── evaluation.yaml                # Evaluation and scoring config
│   └── rubrics.yaml                   # Grading rubrics for each workflow
├── src/
│   └── multiagent_workflows/          # Main Python package
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── model_manager.py       # Unified model access layer
│       │   ├── agent_base.py          # Base agent class with logging
│       │   ├── workflow_engine.py     # Workflow orchestration with eval
│       │   ├── tool_registry.py       # Tool/MCP registration
│       │   ├── logger.py              # Verbose hierarchical logging system
│       │   └── evaluator.py           # Integration with eval framework
│       ├── models/
│       │   ├── __init__.py
│       │   ├── local_onnx.py          # NPU model integration
│       │   ├── ollama_client.py       # Ollama integration
│       │   ├── github_models.py       # GitHub Models API
│       │   ├── windows_ai.py          # Windows AI / DirectML
│       │   └── ai_toolkit.py          # AI Toolkit integration
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py                # Base agent class
│       │   ├── vision_agent.py        # Mockup/image analysis
│       │   ├── requirements_agent.py  # Requirements parsing
│       │   ├── architect_agent.py     # System design
│       │   ├── coder_agent.py         # Code generation
│       │   ├── reviewer_agent.py      # Code review
│       │   └── test_agent.py          # Test generation
│       ├── workflows/
│       │   ├── __init__.py
│       │   ├── base.py                # Base workflow class
│       │   ├── fullstack_workflow.py  # Full-stack generation
│       │   ├── refactoring_workflow.py # Code refactoring
│       │   ├── debugging_workflow.py  # Bug analysis & fixing
│       │   └── architecture_workflow.py # Architecture review
│       ├── evaluation/
│       │   ├── __init__.py
│       │   ├── dataset_loader.py      # Load online code datasets
│       │   ├── scorer.py              # Scoring with rubrics
│       │   ├── comparator.py          # Compare to golden outputs
│       │   ├── metrics.py             # Performance metrics
│       │   └── reporter.py            # Evaluation reports
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── file_operations.py     # File read/write/search
│       │   ├── code_parser.py         # AST parsing
│       │   ├── git_operations.py      # Git integration
│       │   └── testing_tools.py       # Test execution
│       └── mcp/
│           ├── __init__.py
│           ├── filesystem_mcp.py      # File system MCP
│           ├── git_mcp.py             # Git MCP
│           └── code_analysis_mcp.py   # Code analysis MCP
├── workflows/
│   ├── 01_fullstack_generation.md     # Workflow documentation
│   ├── 02_legacy_refactoring.md
│   ├── 03_bug_triage_fix.md
│   └── 04_architecture_evolution.md
├── evaluation/
│   ├── datasets/                      # Cached datasets
│   ├── benchmarks/                    # Benchmark definitions
│   ├── rubrics/                       # Detailed rubrics per workflow
│   └── results/                       # Evaluation results and logs
├── docs/
│   ├── architecture.md
│   ├── api-reference.md
│   └── workflows/
├── examples/
│   ├── fullstack_example.py
│   ├── refactoring_example.py
│   ├── debugging_example.py
│   └── evaluation_example.py          # How to run evaluations
└── tests/
    ├── conftest.py
    ├── test_model_manager.py
    ├── test_agents.py
    ├── test_workflows.py
    └── test_evaluation.py
```

---

## Core Implementation Requirements

### 1. Model Manager Implementation

The `model_manager.py` should:

- **Replicate existing repository patterns** for model access (study `tools/llm_client.py`, don't reinvent)
- Support async/parallel execution across NPU, CPU/GPU, and cloud models
- Handle automatic fallback strategies (premium → mid-tier → local)
- Provide unified interface: `model_manager.generate(model_id, prompt, context)`
- Implement model health checking and availability verification
- Cache model instances for performance
- **LOG ALL MODEL CALLS** with full context (prompt, response, timing, tokens)

**CRITICAL**: If LangChain doesn't provide native support for:

- Windows AI/DirectML NPU access
- Ollama streaming with context caching
- GitHub Models API with specific model routing
- Detailed call logging and metrics

Then implement custom clients using the repository's existing patterns.

```python
class ModelManager:
    """
    Unified interface for all model providers with comprehensive logging.
    Wraps tools/llm_client.py patterns.
    """
    
    def __init__(self, config: dict, logger: VerboseLogger):
        self.config = config
        self.logger = logger
        self.providers = self._initialize_providers()
        
    async def generate(
        self,
        model_id: str,  # e.g., "gh:gpt-4o", "local:phi4", "ollama:qwen2.5-coder:14b"
        prompt: str,
        context: Optional[dict] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        stream: bool = False,
        system_prompt: Optional[str] = None
    ) -> Union[str, AsyncIterator[str]]:
        """
        Generate response with full logging.
        
        Logs:
        - Model ID and provider
        - Full prompt (sanitized if contains secrets)
        - Parameters (temp, max_tokens, etc.)
        - Response time
        - Token count
        - Full response
        - Any errors
        """
        start_time = time.time()
        
        # Log the call
        self.logger.log_model_call(
            model_id=model_id,
            prompt=prompt,
            params={'temperature': temperature, 'max_tokens': max_tokens, 'stream': stream}
        )
        
        try:
            provider = self._get_provider(model_id)
            response = await provider.generate(...)
            
            elapsed = time.time() - start_time
            tokens = self._count_tokens(response)
            
            self.logger.log_model_response(
                model_id=model_id,
                response=response,
                timing=elapsed,
                tokens=tokens
            )
            
            return response
        except Exception as e:
            self.logger.log_error(model_id, e)
            raise
        
    async def check_availability(self, model_id: str) -> bool:
        """Check if model is available and healthy"""
        
    async def list_models(self, provider: Optional[str] = None) -> List[dict]:
        """List available models, optionally filtered by provider"""
        
    def get_optimal_model(
        self,
        task_type: str,  # "vision", "reasoning", "code_gen", "review"
        complexity: int,  # 1-10
        prefer_local: bool = True
    ) -> str:
        """Get optimal model for task based on availability and quality"""
```

### 2. Agent Base Class

```python
class AgentBase:
    """
    Base class for all agents with built-in logging.
    """
    
    def __init__(
        self,
        name: str,
        model_id: str,
        tools: List[str],
        system_prompt: str,
        logger: VerboseLogger
    ):
        self.name = name
        self.model_id = model_id
        self.tools = tools
        self.system_prompt = system_prompt
        self.logger = logger
        
    async def execute(self, task: dict, context: dict) -> dict:
        """Execute agent task with context and full logging"""
        self.logger.log_agent_start(self.name, task, self.system_prompt)
        
        try:
            result = await self._process(task, context)
            self.logger.log_agent_output(self.name, result, self._get_metrics())
            return result
        except Exception as e:
            self.logger.log_agent_error(self.name, e)
            raise
        
    async def use_tool(self, tool_name: str, params: dict) -> Any:
        """Invoke a registered tool with logging"""
        self.logger.log_tool_invocation(tool_name, params)
        result = await self.tool_registry.invoke(tool_name, params)
        self.logger.log_tool_result(tool_name, result)
        return result
```

### 3. Workflow Engine

```python
class WorkflowEngine:
    """
    Orchestrates multi-agent workflows with evaluation integration.
    """
    
    def __init__(
        self,
        model_manager: ModelManager,
        tool_registry: ToolRegistry,
        evaluator: WorkflowEvaluator,
        logger: VerboseLogger
    ):
        self.model_manager = model_manager
        self.tool_registry = tool_registry
        self.evaluator = evaluator
        self.logger = logger
        
    async def execute_workflow(
        self,
        workflow_name: str,
        inputs: dict,
        config: Optional[dict] = None
    ) -> dict:
        """
        Execute a predefined workflow with full logging and evaluation.
        """
        workflow_id = self._generate_workflow_id()
        self.logger.log_workflow_start(workflow_id, workflow_name, inputs)
        
        try:
            workflow = self._load_workflow(workflow_name)
            context = {'inputs': inputs, 'config': config, 'artifacts': {}}
            
            for step in workflow.steps:
                step_result = await self.execute_step(step, context)
                context['artifacts'][step.name] = step_result
                
            final_output = self._compile_output(context)
            
            # Evaluate if golden output available
            if self.evaluator.has_golden(workflow_name, inputs):
                scores = await self.evaluator.score_output(final_output, workflow_name, inputs)
                final_output['evaluation'] = scores
                
            self.logger.log_workflow_complete(workflow_id, True, final_output)
            return final_output
            
        except Exception as e:
            self.logger.log_workflow_error(workflow_id, e)
            raise
        
    async def execute_step(
        self,
        step: dict,
        context: dict,
        parallel: bool = False
    ) -> dict:
        """Execute a single workflow step"""
```

---

## Verbose Logging System Requirements

### Logging Architecture

All agent interactions MUST be logged with this hierarchical detail:

```python
class VerboseLogger:
    """
    Hierarchical logging system that captures all multi-agent workflow execution details.
    Integrates with existing evaluation framework.
    """
    
    def __init__(self, workflow_id: str, config: dict):
        self.workflow_id = workflow_id
        self.config = config
        self.logs = []
        self.metrics = defaultdict(list)
        self.start_time = None
        self.structured_output = {}
        
    # Level 1: Workflow Execution
    def log_workflow_start(self, workflow_name: str, inputs: dict):
        """Log workflow initiation"""
        log.info(f"[WORKFLOW:{self.workflow_id}] Starting '{workflow_name}'")
        log.info(f"[WORKFLOW:{self.workflow_id}] Input: {self._sanitize(inputs)}")
        
    def log_workflow_complete(self, success: bool, final_output: dict, metrics: dict):
        """Log workflow completion with metrics"""
        log.info(f"[WORKFLOW:{self.workflow_id}] Completed in {self.total_duration}s")
        log.info(f"[WORKFLOW:{self.workflow_id}] Total tokens: {metrics['tokens']}, Cost: ${metrics['cost']}")
        
    # Level 2: Step Execution
    def log_step_start(self, step_id: str, step_name: str, context: dict):
        """Log workflow step start"""
        log.info(f"[WORKFLOW:{self.workflow_id}][STEP:{step_id}] Executing '{step_name}'")
        log.debug(f"[WORKFLOW:{self.workflow_id}][STEP:{step_id}] Context: {context}")
        
    def log_step_complete(self, step_id: str, success: bool, output: dict):
        """Log step completion"""
        
    # Level 3: Agent Execution
    def log_agent_start(self, agent_name: str, agent_input: dict, system_prompt: str):
        """Log agent execution start"""
        log.info(f"[WORKFLOW:{self.workflow_id}][AGENT:{agent_name}] Starting agent")
        log.debug(f"[WORKFLOW:{self.workflow_id}][AGENT:{agent_name}] Input: {agent_input}")
        log.debug(f"[WORKFLOW:{self.workflow_id}][AGENT:{agent_name}] System prompt: {system_prompt}")
        
    def log_agent_output(self, agent_name: str, output: dict, metrics: dict):
        """Log agent completion"""
        
    # Level 4: Model Calls
    def log_model_call(self, model_id: str, prompt: str, params: dict):
        """Log model API call"""
        log.info(f"[WORKFLOW:{self.workflow_id}][MODEL:{model_id}] Calling model")
        log.debug(f"[WORKFLOW:{self.workflow_id}][MODEL:{model_id}] Prompt: {prompt}")
        log.debug(f"[WORKFLOW:{self.workflow_id}][MODEL:{model_id}] Params: {params}")
        
    def log_model_response(self, model_id: str, response: str, timing: float, tokens: int):
        """Log model response with metrics"""
        log.info(f"[WORKFLOW:{self.workflow_id}][MODEL:{model_id}] Response time: {timing}ms, Tokens: {tokens}")
        log.debug(f"[WORKFLOW:{self.workflow_id}][MODEL:{model_id}] Response: {response}")
        
    # Level 5: Tool Invocations
    def log_tool_invocation(self, tool_name: str, params: dict):
        """Log tool usage"""
        log.info(f"[WORKFLOW:{self.workflow_id}][TOOL:{tool_name}] Invoking tool")
        log.debug(f"[WORKFLOW:{self.workflow_id}][TOOL:{tool_name}] Parameters: {params}")
        
    def log_tool_result(self, tool_name: str, result: Any):
        """Log tool result"""
        log.debug(f"[WORKFLOW:{self.workflow_id}][TOOL:{tool_name}] Result: {result}")
        
    # Export functions
    def get_structured_log(self) -> dict:
        """Return complete structured log for evaluation"""
        return {
            'workflow_id': self.workflow_id,
            'workflow_name': self.workflow_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_duration': self.total_duration,
            'success': self.success,
            'steps': self.steps,
            'agents': self.agents,
            'model_calls': self.model_calls,
            'tool_invocations': self.tool_invocations,
            'metrics': dict(self.metrics),
            'errors': self.errors
        }
        
    def export_to_json(self, filepath: str):
        """Export structured logs to JSON file"""
        
    def export_to_markdown(self, filepath: str):
        """Export human-readable log to Markdown"""
```

---

## Evaluation Framework Integration

### Evaluator Implementation

```python
class WorkflowEvaluator:
    """
    Integrates with existing evaluation framework.
    Loads datasets, runs workflows, scores outputs, generates reports.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.dataset_loader = DatasetLoader(config)
        self.scorer = Scorer(config)
        self.logger = None  # Set per workflow
        
    async def evaluate_workflow(
        self,
        workflow_name: str,
        dataset_name: str,
        num_samples: Optional[int] = None
    ) -> dict:
        """
        Run workflow evaluation on dataset.
        
        Steps:
        1. Load dataset samples (prompts + golden outputs)
        2. Execute workflow for each sample
        3. Log all execution details
        4. Score outputs against golden examples
        5. Generate evaluation report
        """
        
    async def load_dataset(self, dataset_name: str) -> List[dict]:
        """Load evaluation dataset from online source or cache"""
        
    async def run_sample(self, workflow, sample: dict) -> dict:
        """Run workflow on single dataset sample with logging"""
        
    def score_output(self, output: dict, golden: dict, rubric: dict) -> dict:
        """Score output against golden example using rubric"""
        
    def generate_report(self, results: List[dict]) -> dict:
        """Generate comprehensive evaluation report"""
        
    def compare_to_baseline(self, results: dict, baseline: dict) -> dict:
        """Compare results to baseline performance"""
```

### Scorer with Rubrics

```python
class Scorer:
    """
    Score workflow outputs using defined rubrics.
    Supports multiple scoring methods: exact match, fuzzy match, AST comparison, test execution.
    """
    
    def __init__(self, rubrics_config: dict):
        self.rubrics = self.load_rubrics(rubrics_config)
        
    def score(self, output: dict, golden: dict, rubric_name: str) -> dict:
        """
        Score output against golden using specified rubric.
        
        Returns:
        {
            'total_score': 85.5,
            'max_score': 100,
            'percentage': 85.5,
            'category_scores': {
                'functional_correctness': {'score': 38, 'max': 40, 'details': {...}},
                'code_quality': {'score': 22, 'max': 25, 'details': {...}},
                ...
            },
            'criteria_scores': [...],
            'feedback': "...",
            'strengths': [...],
            'weaknesses': [...]
        }
        """
        
    def score_functional_correctness(self, output: dict, golden: dict, criteria: dict) -> dict:
        """Score functional correctness (test pass rate, requirements coverage)"""
        
    def score_code_quality(self, code: str, criteria: dict) -> dict:
        """Score code quality (complexity, standards, security)"""
        
    def score_completeness(self, output: dict, golden: dict, criteria: dict) -> dict:
        """Score completeness of generated artifacts"""
        
    def score_documentation(self, docs: dict, criteria: dict) -> dict:
        """Score documentation quality and completeness"""
        
    def score_efficiency(self, metrics: dict, criteria: dict) -> dict:
        """Score efficiency (time, tokens, cost)"""
```

---

## Workflow Implementations

### Workflow 1: Full-Stack Application Generation

**Description**: Convert business requirements and UI mockups into a complete full-stack application

**Agents**:

| Agent | Model | Purpose |
|-------|-------|---------|
| Vision Agent | `gh:openai/gpt-4o` | Extract UI components from mockups |
| Requirements Analyst | `gh:gpt-4o-mini` | Parse business requirements |
| Technical Architect | `gh:gpt-4o` | Design system architecture |
| Database Designer | `gh:gpt-4o` | Schema design and optimization |
| API Designer | `gh:gpt-4o-mini` | REST/GraphQL contract design |
| Frontend Generator | `gh:gpt-4o` | React/Vue component generation |
| Backend Generator | `gh:gpt-4o-mini` | API and business logic |
| Integration Agent | `local:phi4mini` | Glue code and configs |
| Code Reviewer | `gh:o4-mini` | Security and quality review |
| Test Generator | `gh:gpt-4o` | Comprehensive test suites |
| Documentation Agent | `gh:gpt-4o-mini` | API docs and guides |

**Tools**:

- Image analysis (for mockups)
- File generation and directory creation
- Template rendering
- Package.json/requirements.txt generation
- Docker/docker-compose generation

**MCP Servers**:

- Filesystem MCP - File operations
- Git MCP - Repository initialization

**Evaluation Dataset**: Custom fullstack with requirements, mockups, golden application code

**Prompt Templates**:

```text
Vision Analysis: "Analyze this UI mockup and extract all interactive elements, layout structure, color palette, and component hierarchy. Output as structured JSON."

Requirements Parsing: "Parse these business requirements into user stories with acceptance criteria. Identify: functional requirements, non-functional requirements, business rules, edge cases, and data entities."

Architecture Design: "Design a system architecture for [requirements]. Consider: scalability, security, maintainability, deployment strategy. Output: tech stack recommendation, component diagram, API strategy, database choice with justification."

Database Design: "Design a database schema for [domain model]. Create: normalized tables, relationships, indexes, constraints. Consider: query patterns, data integrity, scalability. Output: SQL DDL, ER diagram, migration files."

API Design: "Design a RESTful API for [requirements]. Create: endpoint definitions, request/response schemas, authentication strategy, versioning approach. Output: OpenAPI 3.0 specification."

Frontend Generation: "Generate a React application based on [UI specs] and [API contract]. Create: component hierarchy, state management, routing, forms, error handling. Use: TypeScript, Tailwind CSS, modern hooks."

Backend Generation: "Generate a backend API implementation for [API spec]. Create: routes, controllers, services, middleware, validators. Include: error handling, logging, security. Use: [tech stack]."

Code Review: "Review this generated code for: security vulnerabilities, performance issues, best practices violations, maintainability concerns. Provide: specific issues, severity ratings, fix recommendations."

Test Generation: "Generate comprehensive tests for [code]. Create: unit tests (>80% coverage), integration tests, E2E tests. Include: happy paths, edge cases, error scenarios, mocks/fixtures."

Documentation: "Generate documentation for [application]. Create: README with setup instructions, API documentation, architecture overview, deployment guide. Use: clear examples, diagrams."
```

**Workflow Steps**:

1. Vision agent analyzes mockups → UI component tree
2. Requirements analyst parses business docs → user stories
3. Architect designs system → architecture decisions
4. Database designer creates schema → migrations
5. API designer creates contracts → OpenAPI spec
6. Frontend generator creates UI → React components
7. Backend generator creates API → Express/FastAPI
8. Integration agent creates configs → Docker, env files
9. Reviewer analyzes code → security findings
10. Test generator creates tests → Jest/Pytest suites
11. Documentation agent creates docs → README, API docs

**Logging Requirements**:

- Log each agent's input requirements and context
- Log all model calls with prompts and responses
- Log file generation operations
- Log evaluation scores at each step
- Log final comparison to golden output

**Output**: Complete, deployable full-stack application with tests and documentation

**Reference Resources**:

- Martin Fowler - Domain-Driven Design: <https://martinfowler.com/bliki/DomainDrivenDesign.html>
- Martin Fowler - Bounded Context: <https://martinfowler.com/bliki/BoundedContext.html>

---

### Workflow 2: Legacy Code Refactoring & Modernization

**Description**: Analyze legacy codebases and systematically refactor to modern patterns and best practices

**Research Basis**:

- "Working Effectively with Legacy Code" by Michael Feathers
- Strangler Fig Pattern: <https://martinfowler.com/bliki/StranglerFigApplication.html>
- Refactoring patterns: <https://refactoring.guru/refactoring/catalog>

**Agents**:

| Agent | Model | Purpose |
|-------|-------|---------|
| Code Archaeologist | `gh:deepseek-r1` | Deep analysis of legacy code structure |
| Dependency Mapper | `local:phi4` / `ollama:qwen2.5-coder:14b` | Map dependencies and coupling |
| Pattern Detector | `gh:o3-mini` | Identify anti-patterns and code smells |
| Test Coverage Analyst | `local:phi4` / `ollama:deepseek-r1:14b` | Analyze existing tests |
| Safety Net Generator | `gh:gpt-4o` | Generate characterization tests |
| Refactoring Planner | `gh:gpt-4o` | Create step-by-step refactoring plan |
| Code Transformer | `gh:gpt-4o` | Perform safe transformations |
| Migration Agent | `local:phi4` / `ollama:qwen3-coder:30b` | Migrate to modern frameworks |
| Validator | `gh:o4-mini` | Verify behavioral equivalence |
| Documentation Updater | `local:phi4` | Update docs for new code |

**Tools**:

- AST parsing and manipulation
- Code complexity metrics (cyclomatic, cognitive)
- Dependency graph generation
- Test coverage analysis
- Git operations (branch, commit, PR)
- Static analysis integration (pylint, eslint, sonarqube)

**MCP Servers**:

- Filesystem MCP - Code reading/writing
- Git MCP - Version control operations
- Code Analysis MCP - Metrics and AST operations

**Evaluation Dataset**: Legacy code with documented issues, golden refactored version

**Workflow Steps**:

1. Archaeologist scans codebase → structural analysis
2. Dependency mapper creates graph → coupling report
3. Pattern detector finds issues → prioritized anti-patterns
4. Test analyst checks coverage → coverage gaps
5. Safety net generator creates tests → characterization tests
6. Planner creates strategy → refactoring roadmap
7. Transformer applies changes → modernized code (iterative)
8. Migration agent updates frameworks → modern dependencies
9. Validator runs tests → behavioral verification
10. Documentation updater → updated architecture docs

**Logging Requirements**:

- Log all code analysis results
- Log detected patterns and anti-patterns with locations
- Log each refactoring step with diff
- Log test results before/after
- Log complexity metrics before/after
- Compare final output to golden refactored version

**Output**: Refactored codebase with improved maintainability, comprehensive tests, migration plan

**Reference Resources**:

- Martin Fowler - Practical Test Pyramid: <https://martinfowler.com/articles/practical-test-pyramid.html>
- Refactoring Catalog: <https://refactoring.com/catalog/>

---

### Workflow 3: Intelligent Bug Triage & Automated Fixing

**Description**: Analyze bug reports, reproduce issues, identify root causes, and generate fixes with tests

**Research Basis**:

- Automated Program Repair: <https://arxiv.org/abs/1810.12921>
- SWE-bench: <https://www.swebench.com/>
- Agentic debugging: <https://www.anthropic.com/research/swe-bench-sonnet>

**Agents**:

| Agent | Model | Purpose |
|-------|-------|---------|
| Bug Analyst | `gh:gpt-4o-mini` | Parse bug reports and extract details |
| Reproduction Agent | `local:phi4` / `ollama:qwen2.5-coder:14b` | Create minimal repro cases |
| Code Tracer | `gh:deepseek-r1` | Trace execution and identify failure points |
| Root Cause Analyzer | `gh:o3-mini` | Deep reasoning about bug causes |
| Fix Generator | `gh:gpt-4o` | Generate candidate fixes |
| Test Generator | `gh:gpt-4o` | Create regression tests |
| Validator | `local:phi4` / `ollama:deepseek-r1:14b` | Verify fix correctness |
| Side Effect Checker | `gh:o4-mini` | Analyze fix impact on codebase |
| Documentation Agent | `local:phi4` | Update comments and docs |
| PR Creator | `local:phi4mini` | Format and create pull request |

**Tools**:

- Bug tracking API integration (GitHub Issues, Jira)
- Test execution and debugging
- Code search and navigation
- Execution tracing and profiling
- Diff generation and analysis
- CI/CD integration

**MCP Servers**:

- Filesystem MCP - Code access
- Git MCP - Branch, commit, PR operations
- Testing MCP - Test execution and results
- Debugging MCP - Breakpoints, inspection

**Evaluation Dataset**: SWE-bench - real GitHub issues with golden patches

**Workflow Steps**:

1. Bug analyst parses issue → structured bug info
2. Reproduction agent creates test → minimal failing case
3. Code tracer follows execution → stack trace analysis
4. Root cause analyzer reasons → identified cause
5. Fix generator creates solutions → 2-3 candidate fixes
6. Test generator creates tests → regression test suite
7. Validator tests fixes → correctness verification
8. Side effect checker → impact analysis
9. Documentation agent → code comments
10. PR creator → formatted pull request

**Logging Requirements**:

- Log bug report parsing and structured extraction
- Log reproduction test creation and results
- Log execution trace with stack frames
- Log root cause reasoning process
- Log all candidate fixes generated
- Log test results for each candidate
- Log final fix selection reasoning
- Compare fix to golden patch from dataset

**Output**: Pull request with bug fix, regression tests, and analysis documentation

**Reference Resources**:

- SWE-bench Official: <https://www.swebench.com/>
- SWE-bench GitHub: <https://github.com/princeton-nlp/SWE-bench>
- GitHub AI for Developers: <https://github.blog/2023-11-08-ai-for-developers/>

---

### Workflow 4: Architecture Evolution & Technical Debt Assessment

**Description**: Analyze existing architecture, identify technical debt, and create evolution roadmap

**Research Basis**:

- Evolutionary Architecture: <https://www.thoughtworks.com/insights/books/building-evolutionary-architectures>
- Technical Debt: <https://martinfowler.com/bliki/TechnicalDebt.html>
- Architecture Decision Records: <https://adr.github.io/>

**Agents**:

| Agent | Model | Purpose |
|-------|-------|---------|
| Architecture Scanner | `gh:deepseek-r1` | Analyze current architecture |
| Debt Assessor | `gh:o3-mini` | Identify and quantify technical debt |
| Pattern Matcher | `local:phi4` / `ollama:phi4-reasoning` | Compare against best practices |
| Scalability Analyst | `gh:gpt-4o` | Analyze scaling limitations |
| Security Auditor | `gh:o4-mini` | Security architecture review |
| Modernization Planner | `gh:gpt-4o-mini` | Create evolution strategy |
| Cost Estimator | `local:phi4` / `ollama:qwen2.5-coder:14b` | Estimate migration effort |
| ADR Generator | `gh:gpt-4o-mini` | Create architecture decisions |
| Roadmap Builder | `local:phi4` | Multi-phase migration plan |
| Stakeholder Reporter | `local:phi4` | Executive summaries |

**Tools**:

- Architecture diagram generation (PlantUML, Mermaid)
- Dependency analysis
- Performance profiling
- Security scanning
- Cost calculation
- Risk assessment matrices

**MCP Servers**:

- Filesystem MCP - Code analysis
- Code Analysis MCP - Metrics and dependencies
- Documentation MCP - ADR management

**Evaluation Dataset**: Architecture case studies with golden evolution plans

**Workflow Steps**:

1. Architecture scanner maps system → component inventory
2. Debt assessor scores issues → prioritized debt list
3. Pattern matcher compares → gap analysis
4. Scalability analyst tests limits → bottleneck report
5. Security auditor finds vulnerabilities → security findings
6. Modernization planner creates strategy → evolution plan
7. Cost estimator calculates effort → time/resource estimates
8. ADR generator documents decisions → decision records
9. Roadmap builder creates phases → migration timeline
10. Stakeholder reporter → executive presentation

**Logging Requirements**:

- Log architecture component discovery
- Log each debt item with severity and impact
- Log pattern matching results
- Log scalability analysis with metrics
- Log security findings with CVE references
- Log planning reasoning and trade-offs
- Compare final plan to golden evolution strategy

**Output**: Architecture assessment report, evolution roadmap, ADRs, and migration plan

**Reference Resources**:

- C4 Model: <https://c4model.com/>
- Enterprise Integration Patterns: <https://www.enterpriseintegrationpatterns.com/>
- ThoughtWorks - Building Evolutionary Architectures: <https://www.thoughtworks.com/insights/books/building-evolutionary-architectures>
- ADR GitHub: <https://adr.github.io/>

---

## Configuration Files

### config/models.yaml

```yaml
providers:
  local_onnx:
    base_path: "C:\\Users\\tandf\\.cache\\aigallery"
    available:
      - id: "local:phi4"
        capabilities: ["text", "reasoning"]
        device: "npu"
      - id: "gh:openai/gpt-4o"
        capabilities: ["vision", "text"]
        device: "npu"
        
  ollama:
    host: "http://localhost:11434"
    available:
      - id: "ollama:qwen2.5-coder:14b"
        capabilities: ["code", "text"]
        context_length: 32768
        
  github_models:
    endpoint: "https://models.github.com/v1"
    available:
      - id: "gh:gpt-4o"
        capabilities: ["text", "reasoning", "code"]
        cost_tier: "premium"
      - id: "gh:o3-mini"
        capabilities: ["reasoning", "math"]
        cost_tier: "premium"
        
routing:
  vision: ["gh:openai/gpt-4o"]
  reasoning_complex: ["gh:o3-mini", "gh:deepseek-r1", "ollama:deepseek-r1:14b"]
  code_gen_premium: ["gh:gpt-4o", "gh:gpt-4o-mini", "ollama:qwen2.5-coder:14b"]
  code_gen_fast: ["ollama:qwen2.5-coder:14b", "gh:gpt-4o-mini"]
  coordination: ["local:phi4mini"]
```

### config/evaluation.yaml

```yaml
evaluation:
  enabled: true
  
  datasets:
    humaneval:
      url: "https://github.com/openai/human-eval"
      type: "code_generation"
      cache_path: "./evaluation/datasets/humaneval"
      
    mbpp:
      url: "https://github.com/google-research/google-research/tree/master/mbpp"
      type: "code_generation"
      cache_path: "./evaluation/datasets/mbpp"
      
    swe_bench:
      url: "https://github.com/princeton-nlp/SWE-bench"
      type: "bug_fixing"
      cache_path: "./evaluation/datasets/swe_bench"
      
    custom_fullstack:
      url: "custom"
      type: "fullstack_generation"
      cache_path: "./evaluation/datasets/fullstack"
      
  logging:
    level: "DEBUG"  # DEBUG, INFO, WARN, ERROR
    format: "structured"  # structured, plain, json
    output:
      - type: "file"
        path: "./evaluation/results/logs/{workflow_id}_{timestamp}.log"
      - type: "console"
        enabled: true
      - type: "structured_json"
        path: "./evaluation/results/structured/{workflow_id}_{timestamp}.json"
    
    capture:
      agent_inputs: true
      agent_outputs: true
      model_calls: true
      tool_invocations: true
      timing: true
      token_usage: true
      errors: true
      intermediate_steps: true
      
  metrics:
    - name: "functional_correctness"
      type: "pass_at_k"
      k_values: [1, 5, 10]
    - name: "test_pass_rate"
      type: "percentage"
    - name: "code_quality"
      type: "composite"
      components: [cyclomatic_complexity, maintainability_index, comment_ratio]
    - name: "security_score"
      type: "vulnerability_count"
    - name: "generation_time"
      type: "duration"
      unit: "seconds"
    - name: "tokens_used"
      type: "count"
    - name: "cost_estimate"
      type: "currency"
      
  scoring:
    normalize: true
    weights:
      correctness: 0.5
      code_quality: 0.25
      efficiency: 0.15
      documentation: 0.1
      
  reporting:
    generate_html: true
    generate_markdown: true
    include_graphs: true
    compare_to_baseline: true
```

### config/rubrics.yaml

```yaml
rubrics:
  fullstack_generation:
    name: "Full-Stack Application Generation Rubric"
    total_points: 100
    
    categories:
      functional_correctness:
        weight: 40
        criteria:
          - name: "Requirements Coverage"
            points: 15
            description: "All functional requirements implemented"
            levels:
              excellent: "100% of requirements met with edge cases"
              good: "90%+ requirements met"
              adequate: "75%+ requirements met"
              poor: "< 75% requirements met"
          - name: "Working Application"
            points: 15
            description: "Application runs without errors"
            levels:
              excellent: "Runs perfectly, all features work"
              good: "Runs with minor issues"
              adequate: "Runs but significant features broken"
              poor: "Does not run or crashes"
          - name: "Test Pass Rate"
            points: 10
            description: "Generated tests pass"
            levels:
              excellent: "100% tests pass"
              good: "90%+ tests pass"
              adequate: "75%+ tests pass"
              poor: "< 75% tests pass"
              
      code_quality:
        weight: 25
        criteria:
          - name: "Architecture Quality"
            points: 8
            description: "Clean architecture and separation of concerns"
          - name: "Code Standards"
            points: 7
            description: "Follows language best practices and conventions"
          - name: "Error Handling"
            points: 5
            description: "Proper error handling and validation"
          - name: "Security"
            points: 5
            description: "No critical security vulnerabilities"
            
      completeness:
        weight: 20
        criteria:
          - name: "Frontend Complete"
            points: 7
            description: "All UI components generated and styled"
          - name: "Backend Complete"
            points: 7
            description: "All API endpoints and business logic"
          - name: "Database Complete"
            points: 6
            description: "Schema, migrations, and models"
            
      documentation:
        weight: 10
        criteria:
          - name: "API Documentation"
            points: 4
            description: "Complete API documentation"
          - name: "Setup Guide"
            points: 3
            description: "Clear setup and deployment instructions"
          - name: "Code Comments"
            points: 3
            description: "Appropriate inline documentation"
            
      efficiency:
        weight: 5
        criteria:
          - name: "Generation Time"
            points: 3
            description: "Time to generate application"
            levels:
              excellent: "< 15 minutes"
              good: "15-30 minutes"
              adequate: "30-60 minutes"
              poor: "> 60 minutes"
          - name: "Resource Usage"
            points: 2
            description: "Tokens and cost efficiency"
            
  legacy_refactoring:
    name: "Legacy Code Refactoring Rubric"
    total_points: 100
    
    categories:
      correctness:
        weight: 50
        criteria:
          - name: "Behavioral Equivalence"
            points: 25
            description: "Refactored code maintains exact same behavior"
          - name: "Test Coverage"
            points: 15
            description: "Comprehensive test coverage maintained/added"
          - name: "No Regressions"
            points: 10
            description: "All existing tests still pass"
            
      improvement_quality:
        weight: 30
        criteria:
          - name: "Code Complexity Reduction"
            points: 10
            description: "Measurable reduction in cyclomatic complexity"
          - name: "Maintainability Improvement"
            points: 10
            description: "Better structure, naming, organization"
          - name: "Modern Patterns"
            points: 10
            description: "Updated to modern frameworks and patterns"
            
      safety:
        weight: 15
        criteria:
          - name: "Incremental Changes"
            points: 8
            description: "Small, safe, testable changes"
          - name: "Rollback Plan"
            points: 7
            description: "Clear migration and rollback strategy"
            
      documentation:
        weight: 5
        criteria:
          - name: "Migration Guide"
            points: 3
            description: "Clear before/after documentation"
          - name: "Architecture Updates"
            points: 2
            description: "Updated architecture documentation"
            
  bug_fixing:
    name: "Bug Triage and Fixing Rubric"
    total_points: 100
    
    categories:
      correctness:
        weight: 50
        criteria:
          - name: "Bug Fixed"
            points: 25
            description: "Original bug is completely resolved"
          - name: "Regression Tests"
            points: 15
            description: "Tests added to prevent regression"
          - name: "No New Bugs"
            points: 10
            description: "Fix doesn't introduce new issues"
            
      analysis_quality:
        weight: 25
        criteria:
          - name: "Root Cause Identification"
            points: 12
            description: "Correct identification of underlying issue"
          - name: "Impact Analysis"
            points: 8
            description: "Understanding of fix impact on codebase"
          - name: "Reproduction"
            points: 5
            description: "Created minimal reproduction case"
            
      solution_quality:
        weight: 15
        criteria:
          - name: "Minimal Change"
            points: 8
            description: "Fix is minimal and targeted"
          - name: "Code Quality"
            points: 7
            description: "Fix follows best practices"
            
      documentation:
        weight: 10
        criteria:
          - name: "PR Description"
            points: 5
            description: "Clear description of bug and fix"
          - name: "Code Comments"
            points: 5
            description: "Comments explain the fix"
            
  architecture_evolution:
    name: "Architecture Evolution Rubric"
    total_points: 100
    
    categories:
      analysis_depth:
        weight: 35
        criteria:
          - name: "Current State Assessment"
            points: 12
            description: "Comprehensive analysis of existing architecture"
          - name: "Technical Debt Identification"
            points: 12
            description: "All major debt items identified and prioritized"
          - name: "Scalability Analysis"
            points: 11
            description: "Bottlenecks and scaling limits identified"
            
      strategy_quality:
        weight: 35
        criteria:
          - name: "Evolution Plan"
            points: 15
            description: "Clear, phased migration strategy"
          - name: "Risk Assessment"
            points: 10
            description: "Risks identified with mitigation plans"
          - name: "Cost-Benefit Analysis"
            points: 10
            description: "Realistic effort estimates and ROI"
            
      documentation:
        weight: 20
        criteria:
          - name: "Architecture Diagrams"
            points: 8
            description: "Clear current and future state diagrams"
          - name: "ADRs"
            points: 7
            description: "Architecture Decision Records for key decisions"
          - name: "Stakeholder Summary"
            points: 5
            description: "Executive-level summary and recommendations"
            
      actionability:
        weight: 10
        criteria:
          - name: "Concrete Steps"
            points: 6
            description: "Specific, actionable next steps"
          - name: "Timeline"
            points: 4
            description: "Realistic timeline with milestones"
```

---

## Testing & Quality Requirements

- Unit tests for all core components (>80% coverage)
- Integration tests for workflow execution
- Mock model responses for testing
- Performance benchmarks
- Example workflows with sample data
- Tests should extend patterns in existing repository tests

---

## Documentation Requirements

- README with quick start guide
- Architecture documentation with diagrams
- API reference for all public interfaces
- Workflow documentation with examples
- Configuration guide
- Integration guide showing how to use with existing `tools/`

---

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

---

## Success Criteria

The implementation is complete when:

1. ✅ All 4 workflows fully implemented with working code
2. ✅ Model manager integrates all available model types via `tools/llm_client.py` patterns
3. ✅ At least 2 example workflows execute successfully end-to-end
4. ✅ Tests pass with >80% coverage
5. ✅ Documentation is comprehensive with examples
6. ✅ Integration points with existing `tools/` are clear
7. ✅ Code follows repository patterns and conventions
8. ✅ Evaluation framework integration with verbose logging working
9. ✅ Scoring rubrics implemented and validated

---

## Execution Instructions

1. **Analyze Repository**: Study `tools/llm_client.py`, `tools/local_model.py`, `tools/prompteval/`, and `multiagent-dev-system/` for patterns
2. **Create Structure**: Create `multiagent-workflows/` folder with complete directory structure
3. **Implement Core**: Build `src/multiagent_workflows/core/` (model_manager.py, logger.py, evaluator.py, scorer.py)
4. **Implement Models**: Create model provider integrations (reuse existing code where possible)
5. **Implement Agents**: Build base agent class and workflow-specific agents
6. **Implement Workflows**: Create all 4 workflows with agent chains
7. **Configure**: Create configuration files in `config/`
8. **Test**: Add comprehensive tests in `tests/`
9. **Document**: Write documentation in `docs/`
10. **Examples**: Create working examples in `examples/`
11. **Package**: Add `pyproject.toml` and `requirements.txt` for standalone installation

---

## Important Notes

- **Reuse existing repository code** for model access - import from `tools/` instead of duplicating
- **Study existing patterns** before implementing new abstractions
- **Prefer composition over inheritance** for flexibility
- **Make it modular** - each workflow should be independently usable
- **Include error handling** - graceful degradation when models unavailable
- **Add comprehensive logging** - every agent interaction logged with hierarchical structure
- **Make it configurable** - YAML configs for easy customization
- **Document everything** - inline comments and external docs
- **Integrate evaluation framework** - study and reuse `tools/prompteval/` patterns
- **Use LangChain where appropriate** - but implement custom clients when LangChain lacks support for Windows AI/DirectML NPU, Ollama streaming, or GitHub Models API

---

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

Logs: ./evaluation/results/logs/workflow_20260124_021500.json
```
