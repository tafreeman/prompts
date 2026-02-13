# prompts

A monorepo for AI prompt engineering, LLM tooling, and agentic workflow orchestration.

## What's here

|Directory|Description|
|---|---|
|[`agentic-workflows-v2/`](agentic-workflows-v2/)|DAG-based multi-model workflow engine with evaluation dashboard|
|[`prompts/`](prompts/)|Curated prompt library across techniques, agents, analysis, creative, and more|
|[`tools/`](tools/)|LLM client, prompt evaluation harness, and scoring utilities|
|[`testing/`](testing/)|Evaluation test suite|
|[`workflows/`](workflows/)|Workflow YAML definitions|
|[`docs/`](docs/)|Planning docs, evaluation roadmap, reports|

## Agentic Workflows v2

A production-grade workflow orchestration engine with:

- **DAG execution** — YAML-defined steps with dependency resolution (Kahn's algorithm)
- **Multi-backend LLM routing** — GitHub Models, OpenAI, Anthropic, Gemini
- **Evaluation framework** — LLM-as-judge scoring, dataset adaptation, run logging to SQLite
- **React dashboard** — Live run monitoring, DAG visualization, score breakdown

```bash
cd agentic-workflows-v2
pip install -e .
agentic serve          # starts API + UI at http://localhost:8000
```

See [`agentic-workflows-v2/README.md`](agentic-workflows-v2/README.md) for full docs.

## Prompt Library

Prompts organized by category under [`prompts/`](prompts/):

- `agents/` — Agent system prompts and orchestration patterns
- `analysis/` — Code analysis, review, and reasoning prompts
- `developers/` — Development workflow prompts
- `techniques/` — Chain-of-thought, ToT, ReAct, self-consistency
- `templates/` — Reusable prompt templates

## Setup

```bash
python -m venv .venv
.venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

## Requirements

- Python 3.11+
- See `requirements.txt` and `agentic-workflows-v2/pyproject.toml`

## License

MIT
