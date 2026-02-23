# GitHub Copilot instructions for `prompts`

This repo is a **prompt library + agentic workflow toolkit + Python tooling** project. Treat it as a docs/content repo with workflow configs and evaluation tooling.

- Do **not** add app/service scaffolding unless explicitly requested.
- For change checklists and guardrails, follow: `.github/instructions/prompts-repo.instructions.md`.
- **`prompts/`**: Main prompt library (Markdown + YAML frontmatter).
- **`agentic-workflows-v2/`**: Multi-agent workflow runtime (Python 3.11+, LangChain + LangGraph).
- **`agentic-v2-eval/`**: Evaluation framework (Python 3.10+, Scorer, Rubrics).
- **`tools/`**: Shared utilities (`prompts-tools`) for LLM orchestration and evaluation.

## Identity & Mission
Produce production-grade code, rigorous research, and reproducible evaluation artifacts that advance the state of the art in agentic AI.

## Code Quality Standards (Non-Negotiable)

1. **Immutability First:** Always create new objects. Never mutate existing ones. Use `@dataclass(frozen=True)`, `NamedTuple`, or `tuple`.
2. **Type Everything:** Full type annotations on all function signatures. No bare `Any` unless wrapping external untyped APIs.
3. **Small Units:** Functions < 50 lines. Files < 800 lines. Organize by feature/domain.
4. **Error Handling:** Never swallow exceptions. Use specific exception types. Validate at boundaries.
5. **Formatting:** `black` for code, `isort` for imports, `ruff` for linting.
6. **Testing:** At least one test per public function (happy path + error path).

## Architecture: Agentic Workflows

- **Execution Engine:** `langchain/` (primary) and `engine/` (native DAG executor).
- **LLM Routing:** `models/smart_router.py` dispatches based on tier and capability.
- **Workflows:** Declarative YAML under `workflows/definitions/`. Steps reference agents by tier name.
- **Contracts:** Pydantic models in `contracts/` define I/O. **Additive-only changes**.

## Architecture: Prompt Library

- **Prompt Files:** Use lowercase-hyphenated filenames. Place in the correct category folder. Include YAML frontmatter.
- **Variables:** Use `[BRACKETED_VALUES]` for placeholders; document all under a “Variables” section.
- **Templates:** Follow `prompts/templates/prompt-template.md`.

## Developer Workflows

### Agentic Workflows
- **Install:** `pip install -e ".[dev,server,langchain]"` (in `agentic-workflows-v2/`)
- **Run:** `agentic run <workflow> --input <file.json>`
- **Test:** `python -m pytest tests/ -v`

### Prompt Library
- **Validate:** `python tools/validate_prompts.py --all`
- **Evaluate:** `python -m tools.prompteval prompts/<folder>/ --tier 2 --verbose --ci`

## Research Standards

- **Source Governance:**
  - **Tier A (Always allowed):** Official vendor docs, Peer-reviewed papers, arXiv (known groups).
  - **Tier B (Conditional):** High-quality engineering blogs, Stack Overflow (high votes).
  - **Tier C (Blocked):** Unverified blogs, marketing materials.
- **Citations:** Every research claim must include inline citations with valid URLs: `[Claim text] (Source: Title, Publisher, Date — URL)`.

## Anti-Patterns — Never Do These

- **Never mutate state in place.** Always return new objects.
- **Never use bare `except:`.** Catch specific exceptions.
- **Never hardcode secrets.** Use `.env`.
- **Never produce TODOs in generated code.** All files must be complete.
- **Never add web servers or scaffolding unless explicitly requested.**
- **Never use sys.path hacks.** Use `from tools...` imports.
- **Never break existing contracts/schemas.** Additive-only.
- **Never skip the eval flywheel.** Define rubrics before building, run evals after.
