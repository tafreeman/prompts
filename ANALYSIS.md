# Repository Analysis (Draft)

## Focus
- Primary: Agentic workflows (multi-agent orchestration, evaluation, and tooling)
- Secondary: Prompt library structure and usage

## Initial Observations
- Repository presents as an enterprise prompt library with tooling and multi-agent workflow engines.
- Noted dedicated workflow directories and orchestrator configs that suggest evaluation and scoring pipelines.

## Evidence Collected So Far
- Root README highlights the prompt library structure and mentions advanced techniques and agent prompts.

(Updating this document as analysis continues.)

## Agentic Workflow Landscape (Draft)

### Multiagent Workflows Package
- Standalone engine in `multiagent-workflows/` with YAML-driven workflow definitions and model routing.
- Core execution uses a `WorkflowEngine` that loads agent configs, orchestrates steps, and supports evaluation hooks.
- Workflow definitions include end-to-end tasks like full-stack generation, refactoring, bug triage, and architecture evolution.
  - Workflow steps declare agent roles, model preferences, inputs/outputs, and iterative execution options.

### Agentic Planning Workflows
- `workflows/agentic_planning/` provides Microsoft Agent Framework-style JSON configs for multi-phase workflows (end-to-end dev, defect resolution, system design, and code grading).
- Each workflow lists explicit agent roles, model tiers, and handoff pipelines.

### LangChain-Oriented Orchestrator
- `workflows/langchain_orchestrator.py` offers a dependency-light orchestrator that reads `langchain_workflow.yaml` and simulates agent roles (criteria validation, scoring, implementation, validation).
- Provides a dry-run output summary to `results/<run_id>` for repeatable iterations.

### Copilot & Agent Prompt Ecosystem
- The repo includes Copilot custom agent guides and agent prompt templates under `prompts/agents/`, reinforcing structured roles, responsibilities, boundaries, and tool permissions.
- Existing repo instructions emphasize prompt frontmatter schema, canonical templates, and validation tooling, which should be reflected in Copilot workspace instructions.

## How the repo simulates agents (implementation notes)
- The LangChain-style orchestrator is intentionally dependency-light and simulates agent roles via local stub functions (criteria validator, scoring, implementer, validator) instead of real LLM calls. It uses random Gaussian scoring for per-criterion results and assembles a synthetic run summary for dry-run evaluations. The mapping of roles to stub chains is declared in `workflows/langchain_workflow.yaml` and executed in `workflows/langchain_orchestrator.py`. 

## Agentic workflow inventory (primary focus)

### 1) LangChain-style dry-run workflow
- **Config**: `workflows/langchain_workflow.yaml`
- **Roles/agents**: `orchestrator`, `criteria_validator`, `scoring`, `implementer`, `synthesizer`, `validator`, `recorder`
- **Simulation mechanics**: `workflows/langchain_orchestrator.py` wires these roles to stub implementations and writes a JSON run summary per iteration.

### 2) Microsoft Agent Framework-style planning workflows
Location: `workflows/agentic_planning/configs/*.json`

#### End-to-End Development (`workflow_end_to_end.json`)
- Agents: vision_analyst, ux_expert, business_analyst, system_architect, database_architect, frontend_dev, backend_dev, cloud_engineer, security_engineer, qa_engineer, project_judge

#### Defect Resolution (`workflow_defect_resolution.json`)
- Agents: log_analyst, triage_agent, context_gatherer, reproduction_specialist, root_cause_analyst, impact_assessor, patch_engineer, code_reviewer, regression_tester, documentation_updater, resolution_judge

#### Iterative System Design (`workflow_system_design.json`)
- Agents: requirements_clarifier, domain_expert, system_architect, infrastructure_advisor, security_advisor, design_critic, design_refiner, cost_estimator, spec_writer, architecture_judge

#### Code Grading (`workflow_code_grading.json`)
- Agents: static_analyst, test_coverage_analyst, documentation_reviewer, security_auditor, dependency_auditor, performance_reviewer, architecture_compliance, maintainability_scorer, best_practices_validator, head_judge

### 3) Multiagent Workflows engine (YAML-defined)
Location: `multiagent-workflows/config/workflows.yaml` + `multiagent-workflows/config/agents.yaml`

#### Workflow definitions (step → agent)
- **fullstack_generation**: vision_analysis → vision_agent; requirements_parsing → requirements_agent; architecture_design → architect_agent; database_design → database_agent; api_design → api_agent; frontend_generation → coder_agent; backend_generation → coder_agent; integration → integration_agent; code_review → reviewer_agent; test_generation → test_agent; documentation → documentation_agent
- **legacy_refactoring**: code_archaeology → archaeologist_agent; dependency_mapping → dependency_agent; pattern_detection → pattern_agent; test_coverage_analysis → test_analyst_agent; safety_net_generation → test_agent; refactoring_planning → planner_agent; code_transformation → transformer_agent; migration → migration_agent; validation → validator_agent; documentation_update → documentation_agent
- **bug_fixing**: bug_analysis → bug_analyst_agent; reproduction → reproduction_agent; code_tracing → tracer_agent; root_cause_analysis → root_cause_agent; fix_generation → fix_generator_agent; test_generation → test_agent; fix_validation → validator_agent; side_effect_check → side_effect_agent; documentation → documentation_agent; pr_creation → pr_agent
- **architecture_evolution**: architecture_scan → architecture_scanner_agent; debt_assessment → debt_assessor_agent; pattern_matching → pattern_matcher_agent; scalability_analysis → scalability_agent; security_audit → security_auditor_agent; modernization_planning → modernization_planner_agent; cost_estimation → cost_estimator_agent; adr_generation → adr_agent; roadmap_building → roadmap_agent; stakeholder_report → reporter_agent
- **code_grading**: static_analysis → static_analyst_agent; test_analysis → test_analyst_agent; documentation_review → documentation_reviewer_agent; security_audit → security_auditor_agent; dependency_audit → dependency_auditor_agent; performance_review → performance_reviewer_agent; architecture_check → architecture_compliance_agent; maintainability_score → maintainability_agent; best_practices_check → best_practices_agent; final_grading → head_judge_agent

#### Agent definitions currently declared in `config/agents.yaml`
- vision_agent, requirements_agent, architect_agent, coder_agent, reviewer_agent, test_agent, documentation_agent
- archaeologist_agent, pattern_agent, transformer_agent
- bug_analyst_agent, root_cause_agent, fix_generator_agent
- architecture_scanner_agent, debt_assessor_agent, adr_agent

#### Implemented agent classes in code
- `multiagent_workflows/agents`: BaseAgent, ArchitectAgent, CoderAgent, ReviewerAgent, TestAgent

## Agentic prompts (secondary)
- The agentic prompt catalog lives in `prompts/techniques/agentic/`, with multi-agent and single-agent patterns documented under `multi-agent/` and `single-agent/`.
- The standardized agentic evaluation loop is captured in `prompts/advanced/lats-self-refine-evaluator-agentic-workflow.md`, which defines a multi-role evaluator workflow aligned to the dry-run orchestrator concepts.

## LangChain readiness assessment (what’s missing for full agent usage)

### Current LangChain integration state
- `workflows/langchain_orchestrator.py` is a dry-run skeleton that simulates roles via local stubs (criteria validator, scoring, implementer, validator) rather than running LangChain chains or agents.
- `workflows/langchain_workflow.yaml` only maps role names to stub chain identifiers, with no concrete LangChain execution layer.

### Tooling + MCP coverage (current)
- The multiagent-workflows engine has a `ToolRegistry` with built-in tools (file read/write/list, run command, JSON parse/stringify).
- MCP integration is stubbed: `multiagent_workflows/mcp/__init__.py` is empty and marked for future MCP server integrations.
- The multiagent-workflows server API exposes `tools` and `mcp_servers` fields in agent payloads, but these are not wired to actual MCP clients.

### What’s needed to “fully use agents correctly with LangChain” (tools + MCP)
1) **Concrete LangChain execution layer**
   - Implement real LangChain chains/agents for each role in `langchain_workflow.yaml` (or map to LCEL runnables).
   - Replace stub functions in `langchain_orchestrator.py` with LangChain `Runnable` or `AgentExecutor` invocations.

2) **Tool registry ↔ LangChain tool binding**
   - Define LangChain-compatible tools that wrap `ToolRegistry` functions.
   - Ensure tool schemas align with agent prompts and with the expected function-calling interfaces.

3) **MCP client implementations**
   - Implement MCP server clients under `multiagent_workflows/mcp/` and register them in the tool registry.
   - Wire `mcp_servers` definitions from agent configs into runtime tool availability.

4) **Agent config coverage**
   - Many workflow steps reference agents that are not defined in `config/agents.yaml` (e.g., `api_agent`, `integration_agent`, `dependency_agent`, `planner_agent`, etc.). These should be defined if used by the engine.

5) **Evaluation / logging parity**
   - Align LangChain run outputs with the existing evaluation/logging expectations in the multiagent-workflows engine (so scoring and reporting are consistent across engines).

## Copilot Instructions Alignment (Draft)
- The repo already has Copilot guardrails and instructions; updating them to emphasize agentic workflows (workflows/ and multiagent-workflows/) aligns tooling with the core multi-agent orchestration focus.
- Copilot guidance should point contributors toward prompt frontmatter schema, agent templates, and workflow ID stability to keep evaluation pipelines consistent.
