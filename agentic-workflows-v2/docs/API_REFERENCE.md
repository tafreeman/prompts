# API Reference

This document reflects the current public Python API exported by `agentic_v2.__all__`.

## Import Pattern

```python
from agentic_v2 import <symbol>
```

## Public Exports

### Version

- `__version__`: Package version string.

### Tools

- `BaseTool`: Base class for tool implementations.
- `ToolResult`: Standard tool execution result container.
- `ToolSchema`: Tool input/output schema definition.
- `ToolRegistry`: Runtime registry for tool discovery/lookup.
- `get_registry`: Access the global tool registry instance.

### Message And Schema Contracts

- `MessageType`
- `StepStatus`
- `AgentMessage`
- `StepResult`
- `WorkflowResult`
- `Severity`
- `IssueCategory`
- `TestType`
- `TaskInput`
- `TaskOutput`
- `CodeGenerationInput`
- `CodeGenerationOutput`
- `CodeIssue`
- `CodeReviewInput`
- `CodeReviewOutput`
- `TestCase`
- `TestGenerationInput`
- `TestGenerationOutput`

### Model Routing And Client

- `CircuitState`
- `ModelStats`
- `ModelTier`
- `FallbackChain`
- `ModelRouter`
- `SmartModelRouter`
- `get_router`
- `get_smart_router`
- `LLMClientWrapper`
- `TokenBudget`
- `get_client`

### Execution Context And Engine

- `EventType`
- `ServiceContainer`
- `ExecutionContext`
- `get_context`
- `reset_context`
- `RetryStrategy`
- `RetryConfig`
- `StepDefinition`
- `StepExecutor`
- `step`
- `run_step`
- `PipelineStatus`
- `ParallelGroup`
- `ConditionalBranch`
- `Pipeline`
- `PipelineBuilder`
- `PipelineExecutor`
- `run_pipeline`
- `DAG`
- `DAGExecutor`
- `MissingDependencyError`
- `CycleDetectedError`
- `ExpressionEvaluator`
- `StepState`
- `StepStateManager`
- `ExecutorEvent`
- `ExecutionConfig`
- `ExecutionHistory`
- `WorkflowExecutor`
- `get_executor`
- `reset_executor`
- `execute`
- `run`

### Agents And Capabilities

- `AgentConfig`
- `AgentEvent`
- `AgentState`
- `BaseAgent`
- `ConversationMemory`
- `ConversationMessage`
- `agent_to_step`
- `Capability`
- `CapabilityMixin`
- `CapabilitySet`
- `CapabilityType`
- `CodeGenerationMixin`
- `CodeReviewMixin`
- `OrchestrationMixin`
- `TestGenerationMixin`
- `get_agent_capabilities`
- `requires_capabilities`
- `CoderAgent`
- `ReviewerAgent`
- `OrchestratorAgent`
- `OrchestratorInput`
- `OrchestratorOutput`
- `SubTask`

## CLI Entry Point

- Command: `agentic`
- Module: `agentic_v2.cli.main`
- Core commands: `run`, `validate`, `list`, `serve`.
- `orchestrate` is currently marked as not implemented.

## Notes

- Private modules/functions (`_name`) are internal and may change without notice.
- Server APIs are documented separately via FastAPI OpenAPI docs at runtime.
