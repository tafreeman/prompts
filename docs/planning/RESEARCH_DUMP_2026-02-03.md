# Research dump — 2026-02-03

Summary

This document consolidates the research artifacts and vendor repository excerpts gathered during the architecture discovery work for the `prompts` repo. It captures the public-source highlights, local repo artifacts relevant to the research, and suggested next steps.

Sources and highlights

- OpenAI Evals (https://github.com/openai/evals)
  - Python-first evaluation framework. Uses YAML eval templates, example evals, pip editable install. Uses Git-LFS for large data. Clear documentation for writing and running evals.

- OpenAI Cookbook (https://github.com/openai/openai-cookbook)
  - Jupyter notebook examples, recipe-style demos, agent notes (`AGENTS.md`). Good patterns for runnable demos and example-driven docs.

- PromptSource (https://github.com/bigscience-workshop/promptsource)
  - Structured prompt templates (Jinja-backed), Streamlit GUI, HF Datasets integration, separated prompt templates vs code.

- LM Evaluation Harness (EleutherAI) (https://github.com/EleutherAI/lm-evaluation-harness)
  - Unified harness with pluggable backends (HF, API, vLLM). CLI + YAML config patterns, caching/logging, multi-GPU considerations.

- Hugging Face `evaluate` (https://github.com/huggingface/evaluate)
  - Metric-loading API (`evaluate.load`), CLI to publish metrics, community metric hub concept; metrics as composable, reusable components.

- LangChain (https://github.com/langchain-ai/langchain)
  - Modular agent/workflow abstractions. Pattern: separate components (chains, agents, tools, clients), strong integration surface for observability.

- OpenPrompt (https://github.com/thunlp/OpenPrompt)
  - Prompt-learning primitives (Template, Verbalizer, PromptModel). Clear separation of prompt templates and training/application code.

- Transformers pipelines docs (https://huggingface.co/docs/transformers/main/en/pipeline_tutorial)
  - Pipeline abstraction, device_map / fp16 notes, extension points for custom pipelines.

- Anthropic research pages (https://www.anthropic.com/research)
  - Research and evaluation ideas focused on safety and interpretability; useful context for evaluation goals.

Local repo artifacts (selected)

- `iteration-plan.yaml` — root iteration plan (seeds, model tiers, runs_per_variant).
- `docs/planning/agentic-workflows-v2-architecture.md` — architecture research & notes.
- `docs/planning/agentic-workflows-v2-file-inventory.md` — inventory of files referenced by the research.
- `agentic-workflows-v2/docs/IMPLEMENTATION_PLAN_V2.md` — implementation plan derived from industry research.
- `discovery_results.json` — model probe / discovery results from local runs.
- `tools/results/model-matrix/*.json` — model-run matrices and evaluation artifacts.
- `validation_issues_full.txt` — validation issues and findings for prompts.

Key patterns observed

- Separate data/artifacts from code: many repos keep prompt templates, eval YAML, or datasets in clear, versioned folders and sometimes use Git-LFS for large artifacts.
- Config-driven evals: YAML or JSON templates to declare evals (tasks, metrics, model backends) so runs are reproducible and scriptable.
- Metric/component reuse: treat metrics as small, composable packages (see `evaluate`) rather than monolithic test code.
- Backend abstraction: decouple the evaluation harness from model backends (local, API, vLLM) with adapter layers.
- Clear dev experience: provide `pip install -e .` + examples/notebooks and small CLI entrypoints for common tasks.

Notes on repo modularization (starter recommendations)

- `prompts/evaluations/` — YAML eval templates, eval runners, adapters for backends.
- `prompts/metrics/` — reusable metric implementations and wrappers to `evaluate` where possible.
- `prompts/templates/` — structured prompt templates (Jinja/Markdown), separated from application code.
- `prompts/agents/` — agent definitions and orchestration logic (thin wrappers around chains/tools).
- `prompts/workflows/` — higher-level workflow configs and orchestrations (end-to-end plans).
- `tools/` — existing tooling (rubrics, validation, eval harness) may be kept and gradually refactored into the above modules.

Next steps

1. Review this dump and confirm any missing vendor repos you want included.
2. If approved, create a small RFC PR that proposes the directory layout above and migrates a single small example (e.g., move `tools/results` consumer or a single eval YAML) into `prompts/evaluations/` as a proof of concept.
3. Optionally, run `python -m tools.prompteval` on a small subset to validate the new layout and update CI to locate eval artifacts.

Research artifacts produced during session

- Internal todo (session): Create research plan, Collect example repos (in-progress), Analyze patterns (pending), Recommend modular structure (pending), Produce report (pending).
- This file: `docs/planning/RESEARCH_DUMP_2026-02-03.md` (consolidated research dump).

Prepared by: research assistant (session)
Date: 2026-02-03
