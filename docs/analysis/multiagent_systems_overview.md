# Multi-agent systems & tools - repository analysis

This document summarizes the functionality present in the repository's multi-agent toolchains and evaluation stacks. It was produced by scanning the following folders:
- `tools/`
- `multiagent-dev-system/`
- `multiagent-workflows/`

Purpose: provide a single, actionable reference that developers can use to understand components, integration points, gaps relative to AI Toolkit / Microsoft Agent Framework best practices, and prioritized next steps.

---

## Executive summary

This repo contains multiple, overlapping multi-agent and evaluation systems:

1. `tools/agents/` - a mature agent ecosystem focused on benchmarks, a LangChain-based fullstack generator, and a custom `MultiAgentOrchestrator`. It includes benchmark runner, evaluation agents, and glue to `tools.llm` abstractions.
2. `multiagent-workflows/` - a standalone package implementing a custom workflow engine, `AgentBase`, `WorkflowEngine`, `VerboseLogger`, an aiohttp server UI/API, and an `ExecutionScorer` for SWE-style execution evaluation.
3. `multiagent-dev-system/` - a smaller utility package with its own `ModelManager`, `VerboseLogger`, and `Scorer` that mirrors some functionality in `multiagent-workflows` and `tools/`.

All three are coherent and useful, but none are implemented on top of Microsoft Agent Framework. Instead the repo uses: custom orchestrators + LangChain/LangGraph adapters + a shared `tools.llm` client for model access.

Key strengths:
- Multiple evaluation harnesses (PromptEval integration, rubric-based scorers, and an execution-based `ExecutionScorer`).
- Rich, hierarchical logging (`VerboseLogger` implementations) and export to JSON/Markdown.
- LangChain/LangGraph integrations (optional) in the `fullstack_generator`.
- Well-structured benchmarks and runner code in `tools/agents/benchmarks`.

Key gaps vs AI Toolkit / Agent Framework best practices:
- No OpenTelemetry tracing (OTLP) instrumentation across services.
- No Agent Framework-based agent/server entrypoint (so AI Toolkit Agent Inspector `agentdev` cannot directly attach).
- A few `sys.path` injections and ad-hoc packaging patterns (affect reproducibility).
- Mixed scoring approaches: text-similarity used in many places where execution or AST/semantic checks would be more accurate.

---

## Folder-by-folder analysis

### 1) `tools/` (core utilities and agent ecosystem)

Primary subfolders examined:
- `tools/agents/` — full features: `multi_agent_orchestrator.py`, `fullstack_generator/`, `benchmarks/`, evaluation agent, and registries.
  - `multi_agent_orchestrator.py` - custom orchestrator that decomposes tasks, runs specialized agents (Analyst/Researcher/Strategist/Implementer), parallelizes phases, and integrates results. Calls `tools.llm.LLMClient` for model calls.
  - `fullstack_generator/` - LangChain/LangGraph-compatible hybrid full-stack generator with `HybridLLM` wrappers, agent registry (`AGENT_REGISTRY`), phased workflows, and saving of artifacts.
  - `benchmarks/` - benchmark definitions, dataset loaders, runner CLI. Supports `swe-bench`, `humaneval`, `mbpp`, etc. Good metadata-only design with caching and runner presets.
- `tools/llm/` — `llm_client.py`, `model_probe.py`, `local_model.py`, `windows_ai.py`. Centralized model abstraction used by all agent stacks.
- `tools/prompteval/` — evaluation framework for prompts with built-in evaluators, parser, and unified scorer. This is the canonical prompt evaluation engine used in the repo.
- `tools/core/` — config, cache, prompt DB, tool registry, `tool_init.py` (startup checks) and helpers.

Notes & recommendations for `tools/`:
- Very strong: central LLM abstraction, benchmark runner, and evaluator.
- Add tracing hooks in `tools/tool_init.py` and `tools/llm/llm_client.py` to emit spans for model calls (OTel). This enables AI Toolkit integration without rewriting orchestrators.
- Consider providing a thin `agentdev` wrapper task to launch `multi_agent_orchestrator` under debugpy/agentdev for inspector.


### 2) `multiagent-workflows/` (standalone workflow package)

Primary contents:
- `src/multiagent_workflows/core/` — `agent_base.py`, `workflow_engine.py`, `model_manager.py`, `logger.py`, `evaluator.py`.
- `src/multiagent_workflows/evaluation/scorer.py` — includes `ExecutionScorer` (Docker-based execution harness) and similarity-based `Scorer`.
- `src/multiagent_workflows/server/` — `app.py` (aiohttp API + UI), `run_manager.py` (background RunStore executing tasks and using `ExecutionScorer` for `evaluation_method == 'execution'`).
- `workflows/` and config files (YAML) defining workflows, agents, and rubrics.

Notes & recommendations:
- `ExecutionScorer` is implemented to run tests inside Docker; this is the correct approach for SWE-bench style evaluation. Make sure Docker availability is detected earlier and fallbacks are documented.
- Replace selective `sys.path` injection patterns by documenting install/editable install (`pip install -e .`) and adjust `create_app()` to not mutate global `sys.path` if possible.
- Initialize OpenTelemetry tracing in `server/app.py` startup and add model-call spans in `core/model_manager.py` and agent executions in `core/agent_base.py`.
- Fix `VerboseLogger` to avoid adding multiple stream handlers per instance (check handler existence first).


### 3) `multiagent-dev-system/` (dev utilities)

Primary contents:
- `src/multiagent_dev_system/model_manager.py`, `logger.py`, `scorer.py`, utilities.
- Smaller surface area; mirrors much of the functionality in `multiagent-workflows` but lighter-weight.

Notes & recommendations:
- Consolidate common utilities between `multiagent-dev-system` and `multiagent-workflows` into a shared package if desired (avoid duplication).
- Add tracing/logging to match `tools/` and `multiagent-workflows` patterns.


## Cross-cutting observations

- Model access is centralized via `tools/llm/llm_client.py` and `model_probe.py` — this is a strong single integration point for adding tracing, metrics, and call-level instrumentation.
- Evaluation: there are multiple scoring implementations (Scorer classes across packages). Consider standardizing on `tools/prompteval/unified_scorer.py` or a common scoring interface with adapters (text-similarity vs execution vs AST-semantic checks).
- Packaging & imports: several modules use local `sys.path` insertions. Prefer using editable installs (`pip install -e .`) or configuring PYTHONPATH in dev docs vs mutating `sys.path` in code.


## Recommended prioritized next steps

1. Add OpenTelemetry tracing to the repo (low to medium effort). Plan:
   - Instrument `tools/llm/llm_client.py` model calls (start/stop spans, attributes: model_id, prompt_len, tokens, duration)
   - Initialize tracing in `tools/core/tool_init.py` and `multiagent-workflows/server/app.py` with OTLP exporter default `http://localhost:4318`.
   - Verify trace export with AI Toolkit traces viewer.
   Estimated effort: 1-2 days.

2. Add VS Code debug tasks / `agentdev` wrapper to launch orchestrators under debugpy (small change). Implement tasks for `tools/agents/multi_agent_orchestrator.py` and `multiagent-workflows` server.
   Estimated effort: 2-4 hours.

3. Standardize scoring interfaces and consolidate Scorer implementations (medium effort).
   - Create abstract `IScorer` with adapters for `text_similarity`, `execution` (`ExecutionScorer`), and `ast_semantic`.
   Estimated effort: 1-2 days.

4. Create a small Agent Framework adapter (optional, medium effort)
   - Wrap `MultiAgentOrchestrator.run()` or `HybridFullStackGenerator.generate()` as an Agent Framework `as_agent()` endpoint using `azure.ai.agentserver.agentframework` so AI Toolkit Agent Inspector can attach seamlessly.
   Estimated effort: 1-2 days + dependency pinning.

5. Replace `sys.path` injections with packaging guidance
   - Add developer README with `pip install -e .` and remove `sys.path` hacks from runtime code where safe.
   Estimated effort: 2-4 hours.


## Files created
- `docs/analysis/multiagent_systems_overview.md` (this file) — consolidated analysis across `tools/`, `multiagent-dev-system/`, and `multiagent-workflows/`.


## Next actions I can take (pick one)
- Implement OTEL tracing into `tools/llm/llm_client.py` and `multiagent-workflows/server/app.py` and add tests. (I can make small, focused patches.)
- Add VS Code tasks and launch configurations to `.vscode/` for running the orchestrator and attaching debugpy/agentdev.
- Implement a small Agent Framework adapter wrapper for `tools/agents/multi_agent_orchestrator.py` (adapter that depends on `azure-ai-agentserver-agentframework`).

Which would you like me to implement first? If you prefer, I can start with the tracing instrumentation (recommended) and then add the VS Code debug tasks.
