# Repository Analysis — prompts (top-level)

Generated: 2026-01-25

This document summarizes a file- and folder-level scan of the `prompts` repository focused on multi-agent workflows, tooling, and evaluation components. It consolidates findings from inspecting `multiagent-workflows`, `multiagent-dev-system`, and `tools/agents`, plus repository-level tasks and docs.

## High-level summary

- Repository purpose: prompt library + multi-agent workflow tooling + evaluation harnesses for LLM-based code generation and SWE-style benchmarks.
- Languages & tech: Python (3.10+), aiohttp, Docker (for execution scoring), LangChain/LangGraph (optional), GitHub Models API, local ONNX models, optional Ollama, model probe tooling in `tools/llm`.
- Key packages inspected: `multiagent-workflows`, `multiagent-dev-system`, `tools/agents`, `tools/llm`, `tools/prompteval`, `testing`.

## Per-folder findings

### multiagent-workflows/
- Role: primary custom multi-agent runtime + evaluation server. Implements:
  - `server/app.py` — aiohttp server exposing dataset/benchmark endpoints and run management.
  - `server/run_manager.py` — `RunStore` that executes evaluation runs; supports `evaluation_method == "execution"` and wires `ExecutionScorer`.
  - `core/` — `WorkflowEngine`, `AgentBase`, `ModelManager`, `VerboseLogger`, `WorkflowEvaluator` (rubric-based scoring).
  - `evaluation/scorer.py` — `ExecutionScorer` performing fully containerized repo clone, patch apply, install, and test command inside Docker.

Issues & notes:
- Strong structured logging via `VerboseLogger`. No OpenTelemetry tracing present.
- Some `sys.path` insertions exist (for `tools/` imports) — recommend packaging / editable installs instead.
- `WorkflowEngine` and agents are custom; not based on Microsoft Agent Framework (no `agentdev`/`azure.ai.agentserver` usage).
- `ExecutionScorer` is implemented and containerized but live runs depend on Docker availability and per-repo test command metadata.

### multiagent-dev-system/
- Role: companion library with `ModelManager`, `VerboseLogger`, `Scorer`, and small utilities.
- Simpler, more compact implementations of similar concepts (logger, model manager) used by other tooling.

Notes:
- Also not Agent Framework-based. Uses `tools.llm.LLMClient` and `tools.llm.model_probe`.

### tools/agents/
- Contains multiple agent implementations and orchestrators:
  - `multi_agent_orchestrator.py` — custom real multi-agent orchestrator (threadpool parallelism, prompt-based decomposition).
  - `fullstack_generator/` — LangChain/LangGraph-enabled hybrid full-stack generator (optional LangChain adapters).
  - `benchmarks/` — benchmark runner/registry for HumanEval, MBPP, SWE-bench, with CLI runner and dataset loaders.

Notes:
- This folder is the clearest example of multi-agent orchestration implemented with existing repo primitives and optional LangChain integration.

### tools/llm/
- Supplies `LLMClient`, `model_probe`, and local model bridges (Ollama, GitHub Models, local ONNX). This is the abstraction layer used by nearly all agent code to call models.

### tools/prompteval and testing/
- Prompt evaluation tooling and tests for the prompt library. Provides the repo's evaluation pipeline used for prompt scoring (Tiered eval tasks via VS Code tasks).

### prompts/
- Canonical prompt library organized by category with templates, examples, and registry. This is the primary content being evaluated by tools.

## Cross-cutting observations

- No Microsoft Agent Framework usage anywhere in the inspected files — there are no `agentdev` or `azure.ai.agentserver.agentframework` imports. That means AI Toolkit Agent Inspector / Agent Framework serverization guidance does not apply directly.
- Tracing: no OpenTelemetry instrumentation. `VerboseLogger` is good, but adding OTLP spans would enable AI Toolkit trace visualizations.
- Debugging: `.vscode` contains rich task definitions for prompt evaluation, but `launch.json` is a placeholder (C#). Recommend adding Python debug configs for `multiagent` server and `agentdev`-style run tasks if you adopt Agent Framework.
- Packaging: multiple places use `sys.path` modifications to import `tools.*`. Recommend converting `tools/` into an installable package (editable install via pyproject/requirements) or adding a single canonical env activation step for developers.

## Prioritized recommendations

1. Add OpenTelemetry tracing with OTLP exporter in `multiagent-workflows/server/app.py` and instrument key spans (server request, run execution, agent execution, model calls, tool calls).
2. Replace `sys.path` inserts with a clear packaging strategy: make `tools` installable or document consistent PYTHONPATH usage.
3. Add VS Code debug `launch.json` for Python and tasks to run and attach to `multiagent` server under `debugpy` (or `agentdev` if adopting Agent Framework).
4. Introduce per-repo test command metadata (e.g., `config/repo_test_commands.yaml`) and wire it into `ExecutionScorer`.
5. Add an Agent Framework adapter (optional) that wraps existing orchestrators so you can use Agent Inspector without migrating everything at once.

## Files inspected (representative)

- multiagent-workflows/src/multiagent_workflows/server/app.py
- multiagent-workflows/src/multiagent_workflows/server/run_manager.py
- multiagent-workflows/src/multiagent_workflows/core/workflow_engine.py
- multiagent-workflows/src/multiagent_workflows/core/agent_base.py
- multiagent-workflows/src/multiagent_workflows/core/logger.py
- multiagent-workflows/src/multiagent_workflows/evaluation/scorer.py
- multiagent-dev-system/src/multiagent_dev_system/model_manager.py
- multiagent-dev-system/src/multiagent_dev_system/logger.py
- multiagent-dev-system/src/multiagent_dev_system/scorer.py
- tools/agents/multi_agent_orchestrator.py
- tools/agents/fullstack_generator/*
- tools/llm/*
- tools/prompteval/*

## Next steps I can take (pick one or more)

1. Implement OpenTelemetry tracing + OTLP configuration in `multiagent-workflows` (small diff).
2. Add VS Code Python `launch.json` + tasks to run and attach to the `multiagent` server under `debugpy`.
3. Add an Agent Framework adapter (wrapper) for `multi_agent_orchestrator.py` so you can run it as an Agent Framework agent and use Agent Inspector.
4. Add `config/repo_test_commands.yaml` and wire it into `ExecutionScorer` to choose per-repo test commands safely.

If you tell me which to start with, I will implement small, focused patches and update this document with the changes.

---
Generated by repository scan on 2026-01-25.
