# GitHub Copilot Instructions for `prompts`

These instructions guide AI coding agents working in this repo.

## 1. Big Picture

- This repo is both a **Markdown prompt library** (`prompts/`) and a **Flask web app** in `src/` for browsing, customizing, and analyzing prompts.
- Markdown prompts follow a strict YAML-frontmatter + sections template defined in `templates/prompt-template.md` and described in `README.md` / `docs/getting-started.md`.
- The web app (`src/app.py`, `src/templates/`, `src/static/`) reads prompts via `src/load_prompts.py` into a SQLite DB (`prompt_library.db`), then exposes search, customization, copy, and analytics.
- Prompts are optimized for **Claude Sonnet 4.5 / Code 5**, but all code should remain **model-agnostic** (no hard-coded provider SDKs).

## 2. What to Prioritize

- **Prompt files (`prompts/**`)**
	- Preserve the existing sections: frontmatter, Description, Use Cases, Prompt, Variables, Example Usage, Tips, Related Prompts, Changelog.
	- Focus on improving clarity, placeholder naming, and concrete examples; avoid re-structuring the template unless explicitly requested.
	- Keep categories aligned with the five main groups (`developers`, `business`, `creative`, `analysis`, `system`) plus `advanced-techniques` and `governance-compliance`.
- **Web app (`src/`)**
	- Keep changes small and localized; follow existing patterns in `app.py` and `load_prompts.py` for DB access and prompt loading.
	- Maintain the current schema used in `load_prompts.py` and templates: `title`, `persona`, `use_case`, `category`, `platform`, `template`, `description`, `tags`, plus governance fields.
	- Preserve spell-check/autocorrect and copy-to-clipboard behavior in `static/js/app.js`, and text-visibility/accessibility fixes in `static/css/style.css`.
- **Deployment and docs (`deployment/**`, `docs/**`, `src/README.md`)**
	- Align any new instructions with existing IIS / Docker / AWS / Azure flows; do not introduce new platforms or deployment stacks without an explicit requirement.

## 3. Architecture & Data Flow

- **Backend (Flask)**
	- Single app in `src/app.py` with routes:
		- `/` for list + filters (persona/category/platform/search) using parameterized SQLite queries.
		- `/prompt/<id>` and `/customize/<id>` for detail and dynamic placeholder forms.
		- `/api/customize` for JSON-based customization (replacing `[placeholder]` values) and `/analytics` for usage dashboards.
	- Database access is via `get_db_connection()` with `row_factory=sqlite3.Row`; **keep this pattern** when adding queries.
- **Prompt ingestion (`src/load_prompts.py`)**
	- `load_prompts_from_repo()` scans `prompts/` subfolders, parses YAML frontmatter + markdown sections, and normalizes into a dict.
	- `load_expanded_prompts()` wipes and recreates table `prompts`, merges markdown-derived prompts with `additional_prompts` and legacy-migrated prompts from `get_migrated_prompts_from_legacy_dataset()`.
	- All templates must use `[placeholders]` (not `{var}`) so the UI can auto-detect them via `extract_placeholders()` in `app.py`.
- **Frontend**
	- Jinja2 templates in `src/templates/` share `base.html`; new views should extend it and reuse existing card/table/chart patterns.
	- `analytics.html` expects aggregated stats per persona/category/platform and a “top prompts” list; preserve these keys when modifying queries.

## 4. Conventions & Patterns

- **Prompt files**
	- Use lowercase, hyphenated filenames (e.g., `code-review-expert.md`).
	- Frontmatter should always include at least: `title`, `category`, `tags`, `author`, `version`, `date`, `difficulty`; governance-related fields (when present) should map cleanly into `load_prompts.py` keys: `governance_tags`, `data_classification`, `risk_level`, `regulatory_scope`, `approval_required`, `retention_period`.
	- Variables are written as `[variable_name]` and must be documented under a `## Variables` section.
- **Enterprise prompts in Python**
	- When adding prompts directly in `load_prompts.py`, match the dict structure used in `additional_prompts` / `get_migrated_prompts_from_legacy_dataset()` and keep `platform` as a plain string (e.g., `'Claude Sonnet 4.5'`).
	- Provide short, human-readable `description` values (≤ ~500 chars) and concise comma-separated `tags`.
- **Database / schema**
	- Keep `prompt_library.db` in `src/` and SQLite as the only DB; if you change the `prompts` schema, update `init_db()`, `load_expanded_prompts()`, and any templates that read those fields.

## 5. Workflows & Commands

- **Run the web app locally**
	- From repo root:
		- `cd src`
		- `pip install -r requirements.txt`
		- `python load_prompts.py`  # rebuilds `prompt_library.db`
		- `python app.py` and open `http://localhost:5000`.
- **Docker workflow**
	- From repo root: `docker-compose -f deployment/docker/docker-compose.yml up -d`.
- **IIS one-command deploy (Windows)**
	- Run `deployment\iis\deploy.ps1` from repo root in an elevated PowerShell session (see `deployment/iis/README.md` for details).

## 6. Testing & Validation

- For **prompt edits**:
	- Ensure YAML frontmatter is valid and matches `templates/prompt-template.md`.
	- Verify that all `[placeholders]` have entries in the `## Variables` section and that “Example Usage” uses realistic values.
- For **app changes**:
	- Start the app and verify: index list and filters work, prompt detail pages show placeholder-driven forms, `/analytics` renders with charts.
	- If you alter SQL, keep parameterized queries and confirm filter combinations still behave as expected.
- Keep `src/requirements.txt` lean; if you must add a dependency, update deployment docs that reference it.

## 7. Scope & PR Style

- Prefer focused changes:
	- Single prompt or a small related set per change.
	- One area of the app per PR (backend route, template, JS behavior, or deployment docs).
- Commit message patterns that fit this repo:
	- `Add: [prompt name]`
	- `Update: analytics persona breakdown`
	- `Docs: clarify Docker deployment steps`

If anything in these instructions conflicts with an explicit issue or PR description, follow the issue/PR first and update this file if needed.
