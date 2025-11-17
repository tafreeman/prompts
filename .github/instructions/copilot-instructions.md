# GitHub Copilot Instructions for Prompts Library

## 1. Big Picture

- This repo is both a **prompt library** and a small **Flask web app** in `src/` that lets users browse, customize, and analyze prompts.
- Markdown prompts live under `prompts/` and follow a strict YAML + sections template; they are also loaded into SQLite via `src/load_prompts.py`.
- The web app (`src/app.py`, `src/templates/`, `src/static/`) is optimized for **Claude Sonnet 4.5 / Code 5**, but should remain model‑agnostic at the code level.
- Deployment is documented and scripted for IIS, Docker, AWS, and Azure in `deployment/`.

## 2. What Copilot Should Focus On

- For **prompt files** in `prompts/**`:
	- Keep the existing frontmatter + section structure described in `README.md` and `templates/prompt-template.md`.
	- Improve clarity, examples, variables, and tips; avoid large structural rewrites unless the issue explicitly asks.
	- Ensure new prompts fit the existing categories (`developers`, `business`, `creative`, `analysis`, `system`) and tagging style.
- For the **Flask app** in `src/`:
	- Keep changes small and localized; follow the current patterns in `app.py` and `load_prompts.py`.
	- Preserve SQLite usage and the schema/fields referenced in templates (e.g., `title`, `persona`, `use_case`, `platform`, `tags`, `template`).
	- Maintain compatibility with the analytics UI in `templates/analytics.html` and spell‑check features in `static/js/app.js`.
- For **deployment docs/scripts** in `deployment/**`:
	- Update commands, paths, and options; do not introduce new tooling or platforms without an explicit requirement.

## 3. Things to Avoid

- Do **not** change repository layout (folders, key filenames) without a clear issue asking for it.
- Do **not** introduce new frameworks (e.g., swap Flask, add ORMs, JS frameworks) or extra services.
- Do **not** change the database type (keep SQLite) or the core prompt fields without updating all call sites (`load_prompts.py`, `app.py`, templates, and docs).
- Do **not** make sweeping edits across many prompts or docs in a single PR unless explicitly requested.

## 4. Architecture & Patterns

- **Backend:**
	- Single Flask app in `src/app.py` with routes for listing prompts, detail view, customization, copy, and analytics.
	- SQLite database file (`prompt_library.db` in `src/`) accessed via simple helper functions, using parameterized queries.
	- Prompt content originates from markdown in `prompts/` plus additional records defined in `load_prompts.py`.
- **Frontend:**
	- Jinja2 templates in `src/templates/` follow a shared layout in `base.html`; reuse that structure when adding new views.
	- `static/css/style.css` contains accessibility and text‑visibility fixes—preserve the contrast and typography decisions.
	- `static/js/app.js` handles spell‑check/autocorrect, copy‑to‑clipboard, and small UX enhancements; keep JS minimal and vanilla.
- **Deployment:**
	- Local dev: `cd src`, `pip install -r requirements.txt`, `python load_prompts.py`, then `python app.py`.
	- Production guidance lives in `deployment/iis/README.md`, `deployment/docker/README.md`, `deployment/aws/README.md`, and `deployment/azure/README.md`; align any new instructions with these.

## 5. Conventions & Examples

- Use lowercase, hyphenated filenames for prompts (e.g., `code-review-assistant.md`).
- Keep YAML fields aligned with examples in `prompts/**/README.md` and the root `README.md` (include `title`, `category`, `tags`, `author`, `version`, `date`, `difficulty`).
- When adding new enterprise prompts via `load_prompts.py`, follow the existing dict structure:
	- Keys: `title`, `persona`, `use_case`, `category`, `platform`, `template`, `description`, `tags`.
	- Templates should use `[placeholders]` to enable dynamic forms in the UI.
- Preserve optimization notes for Claude (e.g., `platform: 'Claude Sonnet 4.5'`) but avoid hard‑coding model assumptions into logic.

## 6. Testing & Validation

- For prompt changes:
	- Manually sanity‑check that YAML parses, sections are present, and example usage matches the prompt.
- For app changes:
	- At minimum, run the app locally using the quick‑start commands in `README.md`/`src/README.md` and verify:
		- Prompt list loads without errors.
		- A prompt detail page renders with tags, placeholders, and copy button.
		- Analytics page still renders charts if data is present.
- Keep dependencies in `src/requirements.txt` minimal; only add a package if absolutely required and update relevant deployment docs when you do.

## 7. Contribution Scope

- Prefer PRs that:
	- Touch a single prompt or a small cohesive group.
	- Make focused improvements to one area of the app (backend route, template, JS, or deployment script).
- Use clear commit messages like `Add: [prompt name]`, `Update: web analytics chart labels`, or `Docs: clarify IIS deployment script usage`.
