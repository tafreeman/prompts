# Repository Master Record - agentic-workflows-v2

This record provides a comprehensive overview of every file in the repository.


## 📁 `//` 

- `CONTRIBUTING.md`: Contributing to Agentic Workflows v2
- `MASTER_MANIFEST.md`: Repository Master Record - agentic-workflows-v2
- `README.md`: 🌌 Agentic Workflows v2
- `_gen_manifest.py`: No docstring

## 📁 `agentic_v2/` 

- `__init__.py`: Agentic Workflows V2 - Tier-based multi-model orchestration.

## 📁 `agentic_v2\agents/` 

- `__init__.py`: Agents module - Specialized AI agents for different tasks.
- `architect.py`: Architect agent for system design and architecture tasks.
- `base.py`: Base agent implementation.
- `capabilities.py`: Agent capability system for dynamic composition.
- `coder.py`: Coder agent for code generation tasks.

## 📁 `agentic_v2\agents\implementations/` 

- `__init__.py`: Agent implementations.

## 📁 `agentic_v2\agents/` 

- `orchestrator.py`: Orchestrator agent for coordinating multi-agent workflows.
- `reviewer.py`: Reviewer agent for code review tasks.
- `test_agent.py`: Test agent for comprehensive test generation.

## 📁 `agentic_v2\cli/` 

- `__init__.py`: CLI interface for agentic workflows v2.
- `main.py`: CLI interface for agentic workflows v2.

## 📁 `agentic_v2\config/` 

- `__init__.py`: Configuration management.

## 📁 `agentic_v2\config\defaults/` 

- `agents.yaml`: YAML configuration
- `evaluation.yaml`: YAML configuration
- `models.yaml`: YAML configuration

## 📁 `agentic_v2\contracts/` 

- `__init__.py`: Contracts module - Message and schema definitions.
- `messages.py`: Message contracts for agent communication.
- `schemas.py`: Task schemas for structured agent inputs/outputs.

## 📁 `agentic_v2\engine/` 

- `__init__.py`: Engine module - Workflow execution infrastructure.
- `agent_resolver.py`: Agent resolver for YAML-defined workflow steps.
- `context.py`: Execution context for workflow state management.
- `dag.py`: Directed Acyclic Graph (DAG) workflow definition.
- `dag_executor.py`: DAG executor with dynamic parallel scheduling.
- `executor.py`: Main workflow executor with full orchestration.
- `expressions.py`: Expression evaluation helpers for conditional execution.

## 📁 `agentic_v2\engine\patterns/` 

- `__init__.py`: Execution patterns (sequential, parallel, iterative, etc.).

## 📁 `agentic_v2\engine/` 

- `pipeline.py`: Pipeline orchestration for multi-step workflows.
- `runtime.py`: Runtime abstractions for isolated task execution.
- `step.py`: Step definition and execution.
- `step_state.py`: Step lifecycle state machine.

## 📁 `agentic_v2\integrations/` 

- `__init__.py`: Integrations with external frameworks.
- `base.py`: Base adapter interfaces for framework-neutral integration.
- `langchain.py`: LangChain integration for agentic-workflows-v2.
- `tracing.py`: Concrete trace adapter implementations.

## 📁 `agentic_v2\models/` 

- `__init__.py`: Models module - Model routing and statistics.
- `backends.py`: LLM backend implementations.
- `client.py`: LLM client wrapper with smart routing integration.
- `llm.py`: LLM Client Adapter for Agentic V2.
- `model_stats.py`: Model statistics tracking with advanced metrics.
- `router.py`: Model router with configurable fallback chains.
- `smart_router.py`: Smart model router with adaptive learning.

## 📁 `agentic_v2\prompts/` 

- `__init__.py`: Prompt templates for agentic_v2 agents.
- `analyst.md`: Markdown documentation
- `analyzer.md`: Markdown documentation
- `architect.md`: Markdown documentation
- `assembler.md`: Markdown documentation
- `coder.md`: full file content here
- `containment_checker.md`: Markdown documentation
- `debugger.md`: CORRECTED CODE
- `developer.md`: Markdown documentation
- `generator.md`: Markdown documentation
- `judge.md`: Markdown documentation
- `linter.md`: Markdown documentation
- `orchestrator.md`: Markdown documentation
- `planner.md`: Markdown documentation
- `reasoner.md`: Markdown documentation
- `researcher.md`: Markdown documentation
- `reviewer.md`: Markdown documentation
- `summarizer.md`: Markdown documentation
- `task_planner.md`: Markdown documentation
- `tester.md`: tests/test_user_service.py
- `validator.md`: Markdown documentation
- `vision.md`: Markdown documentation
- `writer.md`: Project Name

## 📁 `agentic_v2\server/` 

- `__init__.py`: Server module for agentic workflows v2.
- `app.py`: FastAPI application for agentic workflows v2.
- `evaluation.py`: Dataset selection and scoring helpers for workflow evaluation runs.
- `judge.py`: LLM-as-judge helpers for hybrid workflow scoring.
- `models.py`: API request and response models.
- `normalization.py`: Normalization formula registry for workflow scoring.

## 📁 `agentic_v2\server\routes/` 

- `__init__.py`: API routes for the agentic server.
- `agents.py`: Agent routes.
- `health.py`: Health check routes.
- `workflows.py`: Workflow routes.

## 📁 `agentic_v2\server/` 

- `scoring_profiles.py`: Workflow-family scoring profile defaults.
- `websocket.py`: WebSocket streaming for real-time execution updates.

## 📁 `agentic_v2\tools/` 

- `__init__.py`: Tool system for agentic workflows v2.
- `base.py`: Base classes for the tool system.

## 📁 `agentic_v2\tools\builtin/` 

- `__init__.py`: Built-in tools for Tier 0-2 operations.
- `code_analysis.py`: Tier 1 code analysis tools - Small model required.
- `code_execution.py`: Tier 0 Code execution tool with sandboxing.
- `context_ops.py`: Tier 0 context utilities.
- `file_ops.py`: Tier 0 file operation tools - No LLM required.
- `git_ops.py`: Tier 0 Git operation tools - No LLM required.
- `http_ops.py`: Tier 0 HTTP request tools - No LLM required.
- `memory_ops.py`: Tier 0 persistent memory tools.
- `search_ops.py`: Tier 2 semantic search tools - Medium model required.
- `shell_ops.py`: Tier 0 Shell execution tools - No LLM required.
- `transform.py`: Tier 0 transformation tools - No LLM required.

## 📁 `agentic_v2\tools/` 

- `registry.py`: Tool registry with auto-discovery.

## 📁 `agentic_v2\workflows/` 

- `__init__.py`: Workflow definitions and orchestration.
- `artifact_extractor.py`: Artifact extractor — writes FILE blocks from step outputs to disk.

## 📁 `agentic_v2\workflows\definitions/` 

- `bug_resolution.yaml`: YAML configuration
- `code_review.yaml`: YAML configuration
- `fullstack_generation.yaml`: YAML configuration
- `fullstack_generation_bounded_rereview.yaml`: YAML configuration
- `multi_agent_codegen_e2e.yaml`: YAML configuration
- `plan_implementation.yaml`: YAML configuration

## 📁 `agentic_v2\workflows/` 

- `loader.py`: Workflow loader for YAML workflow definitions.
- `run_logger.py`: Structured JSON run logger for workflow evaluations.
- `runner.py`: Workflow runner — unified entry point for YAML workflows.

## 📁 `//` 

- `dev.sh`: Source file

## 📁 `docs/` 

- `API_REFERENCE.md`: Build Sphinx
- `LANGCHAIN_MIGRATION_PLAN.md`: LangChain Migration Plan & Feature Documentation

## 📁 `docs\adr/` 

- `0001-package-structure.md`: ADR 0001 — Package Structure: Agents and Workflows in same package
- `0002-evaluation-package.md`: ADR 0002 — Evaluation as a Separate Optional Package
- `0003-server-optional.md`: ADR 0003 — Server as Optional Install

## 📁 `docs\reports/` 

- `ACTIVE_VS_LEGACY_TOOLING_MAP.md`: Active vs Legacy Tooling Map

## 📁 `docs\tutorials/` 

- `building_workflow.md`: Markdown documentation
- `creating_agent.md`: Markdown documentation
- `getting_started.md`: Markdown documentation

## 📁 `examples/` 

- `README.md`: Examples
- `simple_agent.py`: Simple agent example for `agentic_v2`.
- `workflow_run.py`: Minimal workflow run example.

## 📁 `fixtures/` 

- `README.md`: Workflow Execution Fixtures

## 📁 `//` 

- `pyproject.toml`: Project configuration

## 📁 `scripts/` 

- `test_sentinel_e2e.py`: Quick end-to-end test: run one coder step and inspect whether sentinel

## 📁 `tests/` 

- `__init__.py`: Test suite for agentic-workflows-v2.
- `conftest.py`: Shared test fixtures.

## 📁 `tests\fixtures/` 

- `__init__.py`: No docstring

## 📁 `tests\fixtures\datasets/` 

- `__init__.py`: Dataset fixtures for workflow testing.

## 📁 `tests/` 

- `test_agents.py`: Tests for agent components.
- `test_agents_integration.py`: Integration tests for OrchestratorAgent with DAG execution.
- `test_agents_orchestrator.py`: Tests for OrchestratorAgent DAG generation and execution.
- `test_cli.py`: Tests for CLI interface.
- `test_contracts.py`: Tests for contract messages and schemas.
- `test_dag.py`: Tests for DAG workflow execution.
- `test_dag_executor.py`: Tests for DAGExecutor parallel execution engine.
- `test_dataset_workflows.py`: Tests using Hugging Face dataset fixtures against workflow runner.
- `test_engine.py`: Tests for execution engine components.
- `test_expressions.py`: Tests for ExpressionEvaluator.
- `test_integrations_base.py`: Unit tests for base adapter contracts and tracing.
- `test_memory_context_tools.py`: Tests for memory/context builtin tools.
- `test_model_router.py`: Tests for model routing and smart routing.
- `test_new_agents.py`: Tests for Architect and Test agents.
- `test_normalization.py`: Tests for score normalization formulas and reliability adjustment.
- `test_phase2d_tools.py`: Tests for Phase 2D enhanced tools (git, http, shell, code_analysis,
- `test_registry.py`: Tests for tool registry.
- `test_run_logger.py`: Tests for workflow run logger record shaping.
- `test_runtime.py`: Tests for runtime abstraction and factory behavior.
- `test_scoring_profiles.py`: Tests for scoring profile templates.
- `test_server_evaluation.py`: Tests for server-side evaluation helpers.
- `test_server_judge.py`: Tests for LLM-as-judge protocol helpers.
- `test_server_workflow_routes.py`: Route-level tests for workflow evaluation API behavior.
- `test_step_state.py`: Tests for StepState lifecycle state machine.
- `test_tier0.py`: Tests for Tier 0 tools (no LLM required).
- `test_workflow_loader.py`: Tests for workflow loader.
- `test_workflow_runner.py`: Integration tests for WorkflowRunner + DAG execution.
- `test_workflow_tracing.py`: Integration test for tracing in WorkflowRunner.

## 📁 `ui\dist\assets/` 

- `index-6cqpkL6b.css`: Source file

## 📁 `ui\dist/` 

- `index.html`: Source file

## 📁 `ui/` 

- `index.html`: Source file

## 📁 `ui\src/` 

- `App.tsx`: Source file

## 📁 `ui\src\__tests__/` 

- `DurationDisplay.test.tsx`: Source file
- `RunConfigForm.test.tsx`: Source file
- `StatusBadge.test.tsx`: Source file
- `apiClient.test.ts`: Source file
- `dagLayout.test.ts`: Source file
- `setup.ts`: Source file
- `useWorkflowStream.test.ts`: Source file

## 📁 `ui\src\api/` 

- `client.ts`: Source file
- `types.ts`: Source file
- `websocket.ts`: Source file

## 📁 `ui\src\components\common/` 

- `DurationDisplay.tsx`: Source file
- `JsonViewer.tsx`: Source file
- `StatusBadge.tsx`: Source file

## 📁 `ui\src\components\dag/` 

- `StepNode.tsx`: Source file
- `WorkflowDAG.tsx`: Source file
- `dagLayout.ts`: Source file

## 📁 `ui\src\components\layout/` 

- `Sidebar.tsx`: Source file

## 📁 `ui\src\components\live/` 

- `StepLogPanel.tsx`: Source file
- `TokenCounter.tsx`: Source file

## 📁 `ui\src\components\runs/` 

- `RunConfigForm.tsx`: Source file
- `RunDetail.tsx`: Source file
- `RunList.tsx`: Source file
- `RunSummaryCards.tsx`: Source file

## 📁 `ui\src\hooks/` 

- `useRuns.ts`: Source file
- `useWorkflowStream.ts`: Source file
- `useWorkflows.ts`: Source file

## 📁 `ui\src/` 

- `main.tsx`: Source file

## 📁 `ui\src\pages/` 

- `DashboardPage.tsx`: Source file
- `LivePage.tsx`: Source file
- `RunDetailPage.tsx`: Source file
- `WorkflowDetailPage.tsx`: Source file
- `WorkflowsPage.tsx`: Source file

## 📁 `ui\src\styles/` 

- `globals.css`: Source file

## 📁 `ui\src/` 

- `vite-env.d.ts`: Source file

## 📁 `ui/` 

- `vite.config.ts`: Source file
- `vitest.config.ts`: Source file
