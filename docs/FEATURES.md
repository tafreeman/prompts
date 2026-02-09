# Project Features

This repository is a prompt library and evaluation toolkit for prompt engineering and multi-agent workflows. Key features and components:

- prompts/: Collection of prompt files organized by category (advanced, agents, analysis, business, creative, developers, frameworks, m365, socmint, system, techniques, templates). Each prompt is a Markdown file with YAML frontmatter.

- tools/: Developer tooling and evaluation helpers
  - tools/prompteval/: PromptEval tooling for running and scoring prompts
  - tools/llm/: LLM adapters and integrations (LangChain adapters, model clients)
  - tools/dynamic_eval_manager.py: Lightweight evaluation manager (added) for orchestrating prompt evaluations and monitoring system load.
  - validate_prompts.py: Prompt validation utilities

- multiagent-workflows/: Example multi-agent workflows and agents
  - multiagent-workflows/src/multiagent_workflows/workflows/: Workflow definitions including `fullstack_workflow.py` which defines a multi-step full-stack generation workflow.

- testing/: Pytest-based test-suite verifying tooling and prompt behavior
  - tests cover prompt validation, evaluation utilities, workflow components, and example integrations.

- scripts/: Utility scripts for running evaluations, merging results, and updating reports.

- results/: Storage for evaluation outputs and previously-run matrices.

How to run key tasks

- Run the full test-suite (recommended after changes):

```bash
python -m pytest -q
```

- Run the Tiered evaluation tasks (examples are provided as VS Code tasks in the workspace):
  - Use provided tasks (e.g., "📊 Eval: Run Tiered Evaluation") or run the PromptEval CLI directly:

```bash
python -m tools.prompteval prompts/ --tier 2 --verbose
```

- Run the Full-stack workflow from Python:

```python
import asyncio
from multiagent_workflows.workflows.fullstack_workflow import run_fullstack_workflow
from multiagent_workflows.core.model_manager import ModelManager

async def main():
    mm = ModelManager()
    outputs = await run_fullstack_workflow("My requirements text", model_manager=mm)
    print(outputs)

asyncio.run(main())
```

Notes and recent fixes

- Added `tools/dynamic_eval_manager.py` as a lightweight module to provide `manage_evaluations`, `evaluate_prompt`, and `monitor_system` utilities used by tests and evaluation scripts.
- Added `conftest.py` shim to allow pytest to run `async def` test functions when `pytest-asyncio` is not installed in the environment. If you have `pytest-asyncio` available, the shim is harmless.

Server / UI improvements

- The example dashboard server now includes simulated run progress so the UI can display "running" workflows and step-level progress even when the full Workflow engine is not available. This makes it easy to demo pipelines locally.
- Added a comparison endpoint `/api/runs/compare?a=<run_id>&b=<run_id>` which returns a simple side-by-side summary and per-step diffs for two runs. Use this to power the UI's compare view.
- API endpoints available in the example server: `/api/health`, `/api/models`, `/api/tasks`, `/api/workflows`, `/api/runs`, `/api/runs/<run_id>`, `/api/runs/compare`.

Next steps

- If integrating the multi-agent workflows with a UI, ensure the UI calls async workflow entrypoints correctly (use asyncio.run or integrate with an async framework event loop).
- Review agent implementations in `multiagent-workflows/src/.../agents/` to ensure constructors match how `_create_agent` instantiates them in `fullstack_workflow.py`.

If you'd like, I can:
- Open a PR with these changes.
- Add more detailed developer docs for running the multi-agent flows and examples for each prompt category.
- Harden the `FullStackWorkflow._create_agent` method to support differing agent constructors.
