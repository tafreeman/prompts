# Agentic Workflows v2 - File Inventory & Migration Checklist

**Generated:** February 2, 2026  
**Purpose:** Detailed inventory of all files related to agentic workflows with migration guidance

---

## 1. Files to COPY & ADAPT

These files have good foundations and should be migrated with modifications. All required components are duplicated into the new package; existing files remain untouched until migration completion and new repo creation.

### 1.1 Core Infrastructure

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/src/multiagent_workflows/core/contracts.py` | `agentic-workflows/contracts/base.py` | Convert to Pydantic BaseModel; add strict validation |
| `multiagent-workflows/src/multiagent_workflows/core/agent_base.py` | `agentic-workflows/agents/base.py` | Clean imports; remove dataclass, use Pydantic |
| `multiagent-workflows/src/multiagent_workflows/core/model_manager.py` | `agentic-workflows/models/manager.py` | Remove sys.path hacks; use proper imports |
| `multiagent-workflows/src/multiagent_workflows/core/logger.py` | `agentic-workflows/logging/logger.py` | Add OpenTelemetry hooks; keep verbose mode |
| `multiagent-workflows/src/multiagent_workflows/core/evaluator.py` | `agentic-workflows/evaluation/evaluator.py` | Update rubric loading paths |
| `tools/llm/llm_client.py` | *(import as dependency)* | No changes; import from `tools.llm` |
| `tools/llm/langchain_adapter.py` | *(import as dependency)* | No changes; import from `tools.llm` |

### 1.2 Agent Implementations

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/src/multiagent_workflows/agents/architect_agent.py` | `agentic-workflows/agents/implementations/architect.py` | Update imports; add contract validation |
| `multiagent-workflows/src/multiagent_workflows/agents/coder_agent.py` | `agentic-workflows/agents/implementations/coder.py` | Update imports; connect tools |
| `multiagent-workflows/src/multiagent_workflows/agents/reviewer_agent.py` | `agentic-workflows/agents/implementations/reviewer.py` | Update imports; add scoring output |
| `multiagent-workflows/src/multiagent_workflows/agents/test_agent.py` | `agentic-workflows/agents/implementations/tester.py` | Update imports; add coverage tracking |
| `multiagent-workflows/src/multiagent_workflows/agents/base.py` | `agentic-workflows/agents/implementations/__init__.py` | Extract shared utilities |

### 1.3 Agent Prompts

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/config/prompts/analyst.md` | `agentic-workflows/agents/prompts/analyst.md` | Add output schema examples |
| `multiagent-workflows/config/prompts/architect.md` | `agentic-workflows/agents/prompts/architect.md` | Add output schema examples |
| `multiagent-workflows/config/prompts/coder.md` | `agentic-workflows/agents/prompts/coder.md` | Add tool usage examples |
| `multiagent-workflows/config/prompts/debugger.md` | `agentic-workflows/agents/prompts/debugger.md` | Add output schema examples |
| `multiagent-workflows/config/prompts/judge.md` | `agentic-workflows/agents/prompts/judge.md` | Add scoring rubric |
| `multiagent-workflows/config/prompts/planner.md` | `agentic-workflows/agents/prompts/planner.md` | Add task decomposition format |
| `multiagent-workflows/config/prompts/reasoner.md` | `agentic-workflows/agents/prompts/reasoner.md` | Add chain-of-thought format |
| `multiagent-workflows/config/prompts/researcher.md` | `agentic-workflows/agents/prompts/researcher.md` | Add citation format |
| `multiagent-workflows/config/prompts/reviewer.md` | `agentic-workflows/agents/prompts/reviewer.md` | Add issue severity levels |
| `multiagent-workflows/config/prompts/tester.md` | `agentic-workflows/agents/prompts/tester.md` | Add test patterns |
| `multiagent-workflows/config/prompts/validator.md` | `agentic-workflows/agents/prompts/validator.md` | Add validation checklist |
| `multiagent-workflows/config/prompts/vision.md` | `agentic-workflows/agents/prompts/vision.md` | Add image analysis format |
| `multiagent-workflows/config/prompts/writer.md` | `agentic-workflows/agents/prompts/writer.md` | Add documentation templates |
| `multiagent-workflows/prompts/*.md` | `agentic-workflows/agents/prompts/` | Consolidate with config/prompts |

### 1.4 Configuration Files

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/config/agents.yaml` | `agentic-workflows/config/defaults/agents.yaml` | Add contract schemas; update tool refs |
| `multiagent-workflows/config/models.yaml` | `agentic-workflows/config/defaults/models.yaml` | Add routing rules |
| `multiagent-workflows/config/workflows.yaml` | `agentic-workflows/workflows/definitions/` | Split into individual workflow files |
| `multiagent-workflows/config/rubrics.yaml` | `agentic-workflows/evaluation/rubrics/` | Split into individual rubric files |
| `multiagent-workflows/config/evaluation.yaml` | `agentic-workflows/config/defaults/evaluation.yaml` | Update paths |

### 1.5 Workflow Implementations

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/src/multiagent_workflows/workflows/fullstack_workflow.py` | `agentic-workflows/workflows/implementations/fullstack.py` | Refactor to use new engine |
| `multiagent-workflows/scripts/run_repo_maintenance.py` | `agentic-workflows/workflows/implementations/maintenance.py` | Extract workflow logic; separate CLI |

### 1.6 Workflow Definitions (JSON/YAML)

| Source File | Target Location | Adaptations Needed |
|-------------|-----------------|-------------------|
| `multiagent-workflows/config/agentic_planning/workflow_code_grading.json` | `agentic-workflows/workflows/definitions/code_grading.yaml` | Convert to YAML; add patterns |
| `multiagent-workflows/config/agentic_planning/workflow_defect_resolution.json` | `agentic-workflows/workflows/definitions/defect_resolution.yaml` | Convert to YAML; add patterns |
| `multiagent-workflows/config/agentic_planning/workflow_end_to_end.json` | `agentic-workflows/workflows/definitions/end_to_end.yaml` | Convert to YAML; add patterns |
| `multiagent-workflows/config/agentic_planning/workflow_repository_maintenance.json` | `agentic-workflows/workflows/definitions/repository_maintenance.yaml` | Convert to YAML; add patterns |
| `multiagent-workflows/config/agentic_planning/workflow_system_design.json` | `agentic-workflows/workflows/definitions/system_design.yaml` | Convert to YAML; add patterns |

---

## 2. Files to REWRITE

These files have significant issues and should be rewritten from scratch using the existing code as reference.

### 2.1 Engine Components

| Source File | Issue | New Implementation |
|-------------|-------|-------------------|
| `multiagent-workflows/src/multiagent_workflows/core/workflow_engine.py` | Complex path resolution; incomplete validation | `agentic-workflows/engine/orchestrator.py` - Clean async execution |
| `multiagent-workflows/src/multiagent_workflows/core/tool_registry.py` | Tools not connected to implementations | `agentic-workflows/tools/registry.py` - Auto-discovery pattern |
| `tools/agents/multi_agent_orchestrator.py` | Duplicate; different patterns | Consolidate into `orchestrator.py` |
| `tools/agents/workflow_runner.py` | Duplicate; evaluation coupling | Consolidate into `orchestrator.py` |

### 2.2 Files to MOVE (Strict Layout Enforcement)

These files exist in the package root but violate the layout rules and must be moved to their proper submodules:

| Current Location | Target Location | Reason |
|------------------|-----------------|--------|
| `src/agentic_v2/agentmessage.py` | `src/agentic_v2/contracts/messages.py` | Contract models belong in `contracts/` |
| `src/agentic_v2/basetool.py` | `src/agentic_v2/tools/base.py` | Tool base class belongs in `tools/` |
| `src/agentic_v2/agenticworkflowsv2config.py` | `src/agentic_v2/config/settings.py` | Config belongs in `config/` |

> **Action Required:** Before Phase 4, move these files and update all imports. Run `python -m pytest tests/ -v` to verify no breakage.

### 2.3 New Components to Write

| Component | Location | Description |
|-----------|----------|-------------|
| `StepDefinition` | `agentic-workflows/engine/step.py` | Declarative step with deps, conditions, hooks ✅ |
| `ExecutionContext` | `agentic-workflows/engine/context.py` | Workflow context with variables, events ✅ |
| `Pipeline` | `agentic-workflows/engine/pipeline.py` | Sequential/parallel pipeline execution ✅ |
| `WorkflowExecutor` | `agentic-workflows/engine/executor.py` | Unified workflow executor ✅ |
| `DAG` | `agentic-workflows/engine/dag.py` | DAG definition with cycle detection, topological sort |
| `DAGExecutor` | `agentic-workflows/engine/dag_executor.py` | Dynamic parallel DAG execution (no sync barriers) |
| `ExpressionEvaluator` | `agentic-workflows/engine/expressions.py` | Condition expression evaluator (${ctx.var > 5}) |
| `StepStateManager` | `agentic-workflows/engine/step_state.py` | Step lifecycle state machine |
| `ModelRouter` | `agentic-workflows/models/router.py` | Model tier routing ✅ |
| `SmartModelRouter` | `agentic-workflows/models/smart_router.py` | Adaptive routing with circuit breaker ✅ |
| `BaseAgent` | `agentic-workflows/agents/base.py` | Agent lifecycle, memory, events ✅ |
| `CoderAgent` | `agentic-workflows/agents/coder.py` | Code generation agent ✅ |
| `ReviewerAgent` | `agentic-workflows/agents/reviewer.py` | Code review agent ✅ |
| `OrchestratorAgent` | `agentic-workflows/agents/orchestrator.py` | Multi-agent coordination ✅ |
| `CapabilitySet` | `agentic-workflows/agents/capabilities.py` | Agent capability system ✅ |
| `Sequential Pattern` | `agentic-workflows/engine/patterns/sequential.py` | Linear execution |
| `Parallel Pattern` | `agentic-workflows/engine/patterns/parallel.py` | Concurrent execution |
| `Conditional Pattern` | `agentic-workflows/engine/patterns/conditional.py` | Branching logic |
| `Iterative Pattern` | `agentic-workflows/engine/patterns/iterative.py` | Retry-with-feedback |
| `Self-Refine Pattern` | `agentic-workflows/engine/patterns/self_refine.py` | LATS loops |
| `Agent Registry` | `agentic-workflows/agents/registry.py` | Agent factory |
| `Workflow Registry` | `agentic-workflows/workflows/registry.py` | Workflow loader |
| `CLI` | `agentic-workflows/cli/` | Typer-based CLI |
| `HTTP Server` | `agentic-workflows/server/` | FastAPI server |

> **Note:** ✅ marks components already implemented in Phase 0-3.

---

## 3. Files to DELETE

These files are deprecated, duplicates, or generated artifacts. **Do not delete during migration.** Deletions occur only after the new repo is created and the cutover is complete.

### 3.1 Deprecated Code

| File | Reason |
|------|--------|
| `archive/prompttools-deprecated/` | Explicitly deprecated folder |
| `tools/agents/multi_agent_orchestrator.py` | After consolidation |
| `tools/agents/workflow_runner.py` | After consolidation |
| `tools/agents/fullstack_generator/` | Duplicate of multiagent-workflows agents |

### 3.2 Generated/Temporary Files

| File | Reason |
|------|--------|
| `multiagent-workflows/1` | Appears to be artifact |
| `maintenance_report_*.md` | Generated reports (keep latest) |
| `maintenance_results_*.json` | Generated results (keep latest) |
| `multiagent-workflows/.pytest_cache/` | Cache |
| `multiagent-workflows/src/multiagent_workflows.egg-info/` | Build artifact |
| `multiagent-workflows/server_debug.log` | Debug log |
| `multiagent-workflows/grading_output.txt` | Debug output |
| `multiagent-workflows/test_output.txt` | Debug output |
| `multiagent-workflows/ollama_models.txt` | Debug output |

### 3.3 Duplicate Configs

| File | Reason |
|------|--------|
| `workflows/agentic_planning/configs/*.json` | Duplicate of multiagent-workflows configs |

---

## 4. Files to KEEP IN PLACE

These files are dependencies used by the new system but should remain in their current location.

| File | Reason |
|------|--------|
| `tools/llm/llm_client.py` | Core LLM abstraction; import as dependency |
| `tools/llm/langchain_adapter.py` | LangChain integration; import as dependency |
| `tools/llm/model_probe.py` | Model discovery; import as dependency |
| `tools/llm/local_model.py` | Local model support; import as dependency |
| `tools/llm/windows_ai.py` | Windows AI integration; import as dependency |
| `tools/core/tool_init.py` | Shared utilities; import as dependency |
| `prompts/` folder | Prompt library; separate from workflow prompts |

---

## 5. New Files to CREATE

### 5.1 Package Structure

```
agentic-workflows/
├── __init__.py                           # Package exports
├── pyproject.toml                        # Package definition
├── README.md                             # Documentation
├── py.typed                              # PEP 561 marker
│
├── agents/
│   ├── __init__.py                       # Agent exports
│   ├── base.py                           # BaseAgent ABC
│   ├── registry.py                       # AgentRegistry
│   ├── implementations/
│   │   ├── __init__.py
│   │   └── (migrate existing agents)
│   └── prompts/
│       └── (migrate existing prompts)
│
├── contracts/
│   ├── __init__.py
│   ├── base.py                           # Pydantic base models
│   ├── messages.py                       # AgentMessage, StepResult
│   ├── agent_contracts.py                # Per-agent I/O schemas
│   ├── workflow_contracts.py             # Workflow I/O schemas
│   └── validation.py                     # Validation utilities
│
├── tools/
│   ├── __init__.py
│   ├── base.py                           # BaseTool, ToolResult
│   ├── registry.py                       # ToolRegistry
│   ├── builtin/
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   ├── code_execution.py
│   │   ├── search.py
│   │   └── formatting.py
│   └── integrations/
│       ├── __init__.py
│       └── mcp_adapter.py
│
├── workflows/
│   ├── __init__.py
│   ├── base.py                           # BaseWorkflow ABC
│   ├── registry.py                       # WorkflowRegistry
│   ├── definitions/
│   │   └── (migrate/convert YAML files)
│   └── implementations/
│       └── (migrate Python workflows)
│
├── engine/
│   ├── __init__.py
│   ├── orchestrator.py                   # Main orchestrator
│   ├── executor.py                       # Step executor
│   ├── context.py                        # Context management
│   ├── state.py                          # State & checkpoints
│   ├── routing.py                        # Model routing
│   └── patterns/
│       ├── __init__.py
│       ├── sequential.py
│       ├── parallel.py
│       ├── conditional.py
│       ├── iterative.py
│       ├── hierarchical.py
│       └── self_refine.py
│
├── evaluation/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── rubrics/
│   └── reporters/
│
├── logging/
│   ├── __init__.py
│   ├── logger.py
│   ├── tracing.py
│   └── exporters/
│
├── models/
│   ├── __init__.py
│   ├── manager.py
│   ├── providers/
│   └── routing.py
│
├── config/
│   ├── __init__.py
│   ├── loader.py
│   ├── defaults/
│   └── schemas/
│
├── cli/
│   ├── __init__.py
│   ├── main.py
│   ├── commands/
│   └── formatters.py
│
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── routes/
│   └── websocket.py
│
└── tests/
    ├── __init__.py
    ├── test_agents/
    ├── test_contracts/
    ├── test_engine/
    ├── test_tools/
    ├── test_workflows/
    └── fixtures/

ui/
├── README.md
├── package.json
├── src/
│   ├── app/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── styles/
└── public/
    └── index.html
```

### 5.2 Configuration Files

```
agentic-workflows/config/
├── defaults/
│   ├── agents.yaml            # Agent definitions with contracts
│   ├── models.yaml            # Model tiers and routing
│   ├── workflows.yaml         # Default workflow settings
│   └── evaluation.yaml        # Evaluation settings
│
└── schemas/
    ├── agent_config.schema.json
    ├── workflow_config.schema.json
    └── message.schema.json
```

---

## 6. Migration Checklist

### Phase 1: Foundation
- [ ] Create `agentic-workflows/` directory
- [ ] Create `pyproject.toml`
- [ ] Create package `__init__.py` files
- [ ] Copy and adapt `contracts.py` → Pydantic models
- [ ] Create `tools/base.py` and `tools/registry.py`
- [ ] Port built-in tools

### Phase 2: Core Engine
- [ ] Create `engine/orchestrator.py`
- [ ] Create `engine/executor.py`
- [ ] Create `engine/context.py`
- [ ] Create `engine/state.py`
- [ ] Create `engine/routing.py`
- [ ] Implement sequential pattern
- [ ] Implement parallel pattern

### Phase 3: Agents & Workflows
- [ ] Create `agents/base.py`
- [ ] Create `agents/registry.py`
- [ ] Migrate architect agent
- [ ] Migrate coder agent
- [ ] Migrate reviewer agent
- [ ] Migrate tester agent
- [ ] Migrate agent prompts
- [ ] Create `workflows/base.py`
- [ ] Create `workflows/registry.py`
- [ ] Convert workflow YAMLs
- [ ] Implement conditional pattern
- [ ] Implement iterative pattern

### Phase 4: Integration
- [ ] Migrate model manager
- [ ] Create CLI with Typer
- [ ] Migrate logger
- [ ] Create tracing module
- [ ] Migrate evaluator
- [ ] Create HTTP server (optional)
- [ ] Create UI package (simplified integration)
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Write documentation

### Phase 5: Cleanup (Post-Cutover)
- [ ] Delete deprecated files (after new repo creation and cutover)
- [ ] Update imports across repo
- [ ] Run full test suite
- [ ] Update repo documentation

---

## 7. Dependency Analysis

### 7.1 External Dependencies (New)

```toml
# pyproject.toml dependencies
[project]
dependencies = [
    "pydantic>=2.0",          # Schema validation
    "typer>=0.9",             # CLI
    "rich>=13.0",             # Console output
    "pyyaml>=6.0",            # YAML parsing
    "aiofiles>=23.0",         # Async file I/O
    "httpx>=0.25",            # Async HTTP client
]

[project.optional-dependencies]
server = [
    "fastapi>=0.100",         # HTTP server
    "uvicorn>=0.23",          # ASGI server
    "websockets>=12.0",       # WebSocket support
]
tracing = [
    "opentelemetry-api>=1.0",
    "opentelemetry-sdk>=1.0",
]
```

### 7.2 Internal Dependencies

```
agentic-workflows depends on:
├── tools.llm.llm_client     # LLM abstraction (existing)
├── tools.llm.langchain_adapter  # LangChain (existing)
├── tools.llm.model_probe    # Discovery (existing)
└── tools.core.tool_init     # Utilities (existing)
```

---

## 8. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing scripts | High | Keep old paths as aliases during transition |
| Import errors | Medium | Comprehensive test coverage |
| Missing tool implementations | Medium | Stub tools with clear errors |
| Config format changes | Medium | Versioned configs with migration script |
| Performance regression | Low | Benchmark before/after |

---

*This inventory should be updated as migration progresses.*
