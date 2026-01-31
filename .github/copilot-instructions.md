# GitHub Copilot instructions for `prompts`

This repo is a **prompt library + agentic workflow toolkit + Python tooling** project. Treat it as a docs/content repo with workflow configs and evaluation tooling.

- Do **not** add app/service scaffolding unless explicitly requested.
- For change checklists and guardrails, follow: `.github/instructions/prompts-repo.instructions.md`.

## Key areas

- `prompts/` — prompt files (Markdown + YAML frontmatter)
- `prompts/templates/` — canonical templates (see `prompts/templates/prompt-template.md`)
- `prompts/agents/` — Copilot custom agents and agent templates
- `docs/reference/frontmatter-schema.md` — frontmatter contract (required fields/allowed values)
- `docs/` — guidance and planning (see `docs/README.md`, `docs/planning/`, `docs/reference/`)
- `workflows/` — agentic planning + LangChain-style orchestrators
- `multiagent-workflows/` — full multi-agent workflow engine (configs, agents, evaluation)
- `tools/` — Python tooling (e.g., `tools/llm/llm_client.py`, `tools/llm/model_probe.py`, `tools/prompteval/`)
- `testing/` — pytest suite + evaluation fixtures
- `.github/instructions/*.instructions.md` — targeted Copilot checklists (this repo: `.github/instructions/prompts-repo.instructions.md`)

```instructions
# GitHub Copilot instructions for `prompts`

This repo is a **prompt library + agentic workflow toolkit + Python tooling** project. Treat it as a docs/content repo with workflow configs and evaluation tooling.

- Do **not** add app/service scaffolding unless explicitly requested.
- For change checklists and guardrails, follow: `.github/instructions/prompts-repo.instructions.md`.

## Key areas

- `prompts/` — prompt files (Markdown + YAML frontmatter)
- `prompts/templates/` — canonical templates (see `prompts/templates/prompt-template.md`)
- `prompts/agents/` — Copilot custom agents and agent templates
- `docs/reference/frontmatter-schema.md` — frontmatter contract (required fields/allowed values)
- `docs/` — guidance and planning (see `docs/README.md`, `docs/planning/`, `docs/reference/`)
- `workflows/` — agentic planning + LangChain-style orchestrators
- `multiagent-workflows/` — full multi-agent workflow engine (configs, agents, evaluation)
- `tools/` — Python tooling (e.g., `tools/llm/llm_client.py`, `tools/llm/model_probe.py`, `tools/prompteval/`)
- `testing/` — pytest suite + evaluation fixtures
- `.github/instructions/*.instructions.md` — targeted Copilot checklists (this repo: `.github/instructions/prompts-repo.instructions.md`)

## Developer workflows

- Use **VS Code Tasks** (see `docs/reference/TASKS_QUICK_REFERENCE.md`):
    - “🔍 Validate All Prompts”
    - “🧪 Run Python Tests”
    - “📊/📂 Eval …” (PromptEval runs)
- CLI equivalents:
    - `python -m pytest testing/ -v`
    - `python tools/validate_prompts.py --all`
    - From repo root: `python -m tools.prompteval prompts/<folder>/ --tier 2 --verbose --ci`

## Evaluation: use PromptEval

- **PromptEval** (`tools/prompteval/`) is the canonical evaluation tool. Use it for all prompt scoring, CI, and local/cloud model runs. (Legacy: `dual_eval.py` is deprecated.)

## Model/provider conventions

- Models use prefixes such as: `local:*`, `ollama:*`, `aitk:*`, `windows-ai:*`, `gh:*` (see `tools/llm/llm_client.py`).
- Before any **batch** LLM run, probe availability and write `discovery_results.json`:
    - `python -m tools.llm.model_probe --discover --force -o discovery_results.json`
- Cloud providers require env vars; use `.env.example` as the template (never hardcode secrets). Typical: `GITHUB_TOKEN` for `gh:*`.

## Authoring conventions

- Prompt files: Markdown with YAML frontmatter; filenames **lowercase-hyphenated** under the correct `prompts/<category>/`.
- Use `[BRACKETED_VALUES]` for placeholders and document each under a “Variables” section.
- Keep prompt metadata aligned with `docs/reference/frontmatter-schema.md`.
- Prefer concrete examples and explicit input/output formats.

## Agentic workflow conventions

- Workflow configs live in `workflows/` and `multiagent-workflows/config/`.
- Preserve workflow IDs, step IDs, and input/output names unless you update all call sites and docs.
- Keep agent roles, model preferences, and tool assignments consistent with existing naming patterns.

## Python tools

- Prefer `tools/core/tool_init.py` to enforce: fail-fast prereqs, UTF-8 console safety on Windows, progress + JSONL logging, and standardized error codes (see `tools/documentation/EXECUTION_GUIDELINES.md`).
- Keep imports as `from tools...` (the repo packages `tools` via `pyproject.toml`); avoid `sys.path` hacks.

## Windows setup

- On Windows, activate the virtual environment with `.venv\\Scripts\\Activate.ps1` before running Python scripts.

```
