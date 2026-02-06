

# GitHub Copilot Instructions for `prompts`

This repository is a **prompt library and Python-based evaluation toolkit** for LLM prompt engineering, evaluation, and research. It is structured for modular, reproducible prompt development and robust evaluation workflows.

## Project Structure & Key Components

- `prompts/` — Main prompt library. Each subfolder is a category (e.g., `analysis/`, `business/`, `system/`). Prompts are Markdown with YAML frontmatter. Use [BRACKETED_VALUES] for variables and document them under a “Variables” section.
- `prompts/templates/` — Canonical prompt templates. Follow `prompt-template.md` for new prompts.
- `docs/` — Guidance, standards, and planning. See `docs/reference/frontmatter-schema.md` for required frontmatter fields.
- `tools/` — Python tools for prompt validation, evaluation, and LLM orchestration. Key modules:
    - `tools/prompteval/` — Main evaluation engine (PromptEval). All evaluations should use this.
    - `tools/llm/llm_client.py` — Model orchestration; supports multiple providers via prefixes (`local:*`, `gh:*`, `ollama:*`, etc.).
    - `tools/llm/model_probe.py` — Model discovery/probing.
- `testing/` — Pytest-based test suite for all Python tooling and prompt evaluation logic.
- `.github/instructions/` — Repo guardrails and checklists. See `prompts-repo.instructions.md` for required practices.

## Developer Workflows

- **Prompt Validation:** Use VS Code Task “🔍 Validate All Prompts” or run `python tools/validate_prompts.py --all`.
- **Testing:** Use “🧪 Run Python Tests” or `python -m pytest testing/ -v`.
- **Prompt Evaluation:** Use “📊 Eval: ...” tasks or run `python -m tools.prompteval prompts/<folder>/ --tier 2 --verbose --ci` for local evaluation. See `results/` for outputs.
- **Model Discovery:** Before batch LLM runs, probe models: `python -m tools.llm.model_probe --discover --force -o discovery_results.json`.
- **Environment:** Use `.env.example` as a template for required secrets (e.g., `GITHUB_TOKEN`). Never hardcode secrets.

## Project Conventions & Patterns

- **Prompt files:** Use lowercase-hyphenated filenames. Place in the correct category folder. Always include YAML frontmatter per `frontmatter-schema.md`.
- **Variables:** Use `[BRACKETED_VALUES]` for placeholders; document all under a “Variables” section in the prompt file.
- **Python imports:** Use `from tools...` for all internal tooling. Do not use `sys.path` hacks.
- **No app/service scaffolding:** Do not add web servers, apps, or unrelated frameworks unless explicitly requested.
- **Evaluation:** All prompt/model evaluation must use PromptEval (`tools/prompteval/`). Legacy scripts (e.g., `dual_eval.py`) are deprecated.
- **Results:** Store evaluation outputs in `results/`. Use subfolders for large runs.
- **Windows:** Activate the virtual environment with `.venv\Scripts\Activate.ps1` before running Python scripts.

## Examples

- To evaluate all prompts in a folder:
    ```sh
    python -m tools.prompteval prompts/analysis/ --tier 2 --verbose --ci
    ```
- To validate all prompts:
    ```sh
    python tools/validate_prompts.py --all
    ```
- To run all Python tests:
    ```sh
    python -m pytest testing/ -v
    ```

## See Also

- `.github/instructions/prompts-repo.instructions.md` — Full repo guardrails and checklists
- `docs/reference/frontmatter-schema.md` — Prompt frontmatter contract
- `prompts/templates/prompt-template.md` — Prompt authoring template

---
If any conventions or workflows are unclear or missing, please provide feedback for further refinement.
