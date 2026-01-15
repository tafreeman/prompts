
# GitHub Copilot instructions for `prompts`

This repo is a **prompt-library + Python tooling** project. Treat it as a docs/content repo: do not add app/service scaffolding unless explicitly working in `app.prompts.library/`.

## Key areas
- `prompts/` — prompt files (Markdown + YAML frontmatter)
- `templates/` — canonical templates (see `templates/prompt-template.md`)
- `reference/frontmatter-schema.md` — frontmatter contract (required fields/allowed values)
- `docs/` — guidance and architecture (e.g., `docs/ARCHITECTURE_PLAN.md`, `docs/prompt-authorship-guide.md`)
- `tools/` — Python tooling (e.g., `tools/llm_client.py`, `tools/model_probe.py`, `tools/prompteval/`)
- `testing/` — pytest suite + evaluation fixtures

## Developer workflows
- Use **VS Code Tasks** (see `TASKS_QUICK_REFERENCE.md`):
    - “🔍 Validate All Prompts”
    - “🧪 Run Python Tests”
    - “📊/📂 Eval …” (PromptEval runs)
- CLI equivalents:
    - `python -m pytest testing/ -v`
    - `python tools/validators/frontmatter_validator.py --all`
    - From `tools/` cwd: `python -m prompteval ../prompts/<folder>/ --tier 2 --verbose --ci`

## Evaluation: use PromptEval
- **PromptEval** (`tools/prompteval/`) is the canonical evaluation tool. Use it for all prompt scoring, CI, and local/cloud model runs. (Legacy: `dual_eval.py` is deprecated.)

## Model/provider conventions
- Models use prefixes: `local:*`, `windows-ai:*`, `gh:*`, `azure-foundry:*` (see `tools/llm_client.py`).
- Before any **batch** LLM run, probe availability and write `discovery_results.json`:
    - `python tools/model_probe.py --discover --force -o discovery_results.json`
- Cloud providers require env vars; use `.env.example` as the template (never hardcode secrets). Typical: `GITHUB_TOKEN` for `gh:*`.

## Authoring conventions
- Prompt files: Markdown with YAML frontmatter; filenames **lowercase-hyphenated** under the correct `prompts/<category>/`.
- Use `[BRACKETED_VALUES]` for placeholders and document each under “Variables” (see `docs/prompt-authorship-guide.md`).

## Python tools
- Prefer `tools/tool_init.py` to enforce: fail-fast prereqs, UTF-8 console safety on Windows, progress + JSONL logging, and standardized error codes (see `tools/EXECUTION_GUIDELINES.md`).
- Keep imports as `from tools...` (the repo packages `tools` via `pyproject.toml`); avoid `sys.path` hacks.

## Windows setup
- On Windows, activate the virtual environment with `.venv\Scripts\Activate.ps1` before running Python scripts.
