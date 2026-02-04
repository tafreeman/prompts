# Research dump — 2026-02-03 (expanded)

Summary

This expanded research dump builds on the initial notes and includes concrete repo patterns, folder-layout examples, eval/template snippets, CI/PR guidance, a phased migration plan for the `prompts` repository, and suggested next actions.

Expanded sources and highlights

- openai/evals — evaluation-first framework with YAML templates, registry-style evals, runner CLI, and clear guidance for publishing and caching results. Useful for eval metadata and runner design.
- openai/openai-cookbook — runnable notebook recipes and agent examples; pattern: cookbook-style docs + runnable examples that double as tests and demos.
- bigscience-workshop/promptsource — structured prompt templates (Jinja), prompt catalog, Streamlit GUI and dataset integration; good example for a prompt template store and curator workflows.
- EleutherAI/lm-evaluation-harness — CLI-driven harness with backend adapters (HF/API/vLLM), dataset/task catalog, caching and multi-GPU considerations.
- huggingface/evaluate — metrics-as-components (loadable API) and a publishing flow; pattern: small reusable metric modules and community-published metrics.
- langchain-ai/langchain — modular chains/agents/tools with an ecosystem (LangSmith); pattern: SDK-style components with many integrations and observability hooks.
- thunlp/OpenPrompt — prompt-learning primitives (Template/Verbalizer/PromptModel) with examples for prompt tuning workflows.
- huggingface/transformers — pipeline abstraction (task-based APIs), device_map and fp16 considerations, suggestions for custom pipeline extension points.
- microsoft/semantic-kernel and microsoft/autogen — SDK/agent orchestration concepts; useful references when designing an agent SDK layer.

Representative patterns and takeaways

- Keep templates separate from code: store prompt templates (jinja2 or markdown) in `templates/` so they can be versioned and edited independently.
- Use config-driven evals: YAML/JSON specs declare dataset, template, metrics, backend, and runtime options; this makes runs reproducible and scriptable.
- Metrics first-class: create small `metrics/` modules that wrap community libs like `evaluate` for consistency.
- Backend adapters: implement an adapter layer for local models, API-based models, and vLLM endpoints so the runner is backend-agnostic.
- Provide small CLI/Examples: `pip install -e .`, a lightweight CLI (e.g., `prompts-eval`) and `examples/` with minimal datasets improve developer onboarding.
- CI smoke tests: run a small set of evals on PRs to catch regressions early without running the full suite.

Concrete folder-layout recommendations

Minimal, evaluation-first layout (simple, quick to adopt)

```
prompts/
  evaluations/
    examples/
      sentiment_eval.yaml
    runner.py
  templates/
    sentiment_prompt.jinja2
  metrics/
    accuracy.py
  agents/
    researcher_agent.py
  workflows/
    end_to_end.yaml
  tools/
    validate_prompts.py
  docs/
    RESEARCH_DUMP_2026-02-03-EXPANDED.md
```

Monorepo / package layout (for larger projects)

```
prompts/
  packages/
    prompts-core/
    prompts-eval/
    prompts-metrics/
    prompts-agents/
  examples/
  ci/
  docs/
```

Sample eval YAML (evaluations/examples/sentiment_eval.yaml)

```yaml
name: sentiment-classification
description: Sample eval for sentiment classification
dataset: examples/data/sentiment_test.jsonl
template: templates/sentiment_prompt.jinja2
metrics:
  - accuracy
  - f1
backend:
  type: local
  model: local:thot-1@2026-01-28
  device: cpu
runtime:
  max_examples: 100
```

Metric wrapper example (prompts/metrics/accuracy.py)

```python
from evaluate import load

metric = load("accuracy")

def compute(preds, refs):
    return metric.compute(predictions=preds, references=refs)
```

Runner sketch (prompts/evaluations/runner.py)

```python
import yaml
from prompts.templates import render_template
from prompts.backends import get_backend
from prompts.metrics import compute_metrics


def run_eval(yaml_path, limit=None):
    spec = yaml.safe_load(open(yaml_path))
    backend = get_backend(spec['backend'])
    samples = load_dataset(spec['dataset'], limit)
    preds, refs = [], []
    for s in samples:
        prompt = render_template(spec['template'], s)
        out = backend.generate(prompt)
        preds.append(out)
        refs.append(s['label'])
    return compute_metrics(spec['metrics'], preds, refs)
```

Suggested CI smoke job (GitHub Actions)

```yaml
name: smoke-eval
on: [pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install -e .[dev]
      - name: Run smoke eval
        run: python -m prompts.evaluations.runner evaluations/examples/sentiment_eval.yaml --limit 10
```

Phased migration plan (low-risk)

1. Create an RFC describing the proposed directory structure, goals, CI changes and a sample POC move.
2. Add new top-level folders (`evaluations/`, `templates/`, `metrics/`) and place a single working eval+runner in them.
3. Add a GitHub Actions smoke job that runs the single eval on PRs.
4. Iteratively move other tools (validation, rubrics) into the new layout and update imports with small PRs.
5. Optional: publish metrics as small packages or adopt `evaluate`-style packaging for reuse.

PR checklist

- Adds minimal example eval and runner, with docs.
- Adds CI smoke job targeting the POC eval.
- Documentation updated: `docs/` architecture + `docs/planning/` file-inventory.
- Data handling policy noted: use Git-LFS for large artifacts and do not commit sensitive data.

Estimated effort

- RFC + POC: 2–4 hours
- CI + tests: 1–2 hours
- Phase migration of tools: 1–3 days depending on scope

Actionables (what I will do next if you confirm)

1) Expand the dump with direct folder-tree extracts (README or `git ls-tree`/`tree` outputs) from 8–12 open-source repos and produce a comparison matrix (requires public web fetches). Estimated: 1–2 hours.

2) Open a POC PR that adds the `evaluations/` layout and migrates a single YAML+runner from `tools/` as a proof-of-concept. Estimated: 2–4 hours.

3) Create a small discovery script that scans the repo for eval-like YAML or runner scripts and prints a suggested migration map (automated assistance for the migration). Estimated: 1–2 hours.

Local artifacts referenced (already in this workspace)

- `iteration-plan.yaml`
- `docs/planning/agentic-workflows-v2-architecture.md`
- `docs/planning/agentic-workflows-v2-file-inventory.md`
- `agentic-workflows-v2/docs/IMPLEMENTATION_PLAN_V2.md`
- `discovery_results.json`
- `tools/results/model-matrix/*.json`
- `validation_issues_full.txt`

Prepared by: research assistant (session)
Date: 2026-02-03
