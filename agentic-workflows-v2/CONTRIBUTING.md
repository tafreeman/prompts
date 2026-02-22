# Contributing to Agentic Workflows v2

Thanks for contributing. This project uses docs-as-code, typed contracts, and test-first changes.

## Scope

Contributions are welcome for:
- Workflow runtime improvements (`agentic_v2/engine`, `agentic_v2/workflows`)
- Agent/model/tool integrations
- API/UI improvements
- Tests and fixtures
- Documentation and examples

## Prerequisites

- Python 3.11+
- Node.js 20+ (for `ui/`)
- `pip` and `npm`

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,server,langchain]"
```

UI setup:

```bash
cd ui
npm install
cd ..
```

## Development Workflow

1. Create a branch for your change.
2. Make the smallest coherent change set.
3. Add or update tests.
4. Update docs for behavior, API, config, or workflow changes.
5. Run local checks before opening a PR.

## Required Local Checks

```bash
# Python style + lint hooks
pre-commit run --all-files

# Backend tests
python -m pytest tests -v

# Docs link checks
python scripts/check_docs_refs.py
```

UI checks (when frontend files changed):

```bash
cd ui
npm run build
npm test
```

## Pull Request Expectations

Use `.github/PULL_REQUEST_TEMPLATE.md` and include:
- Problem statement
- What changed
- Validation evidence (tests/screenshots/logs)
- Risks and rollback notes
- Documentation updates

## Documentation Rules

If your change affects users or contributors, update the docs in the same PR.

Typical mappings:
- New workflow: `docs/WORKFLOWS.md`
- New environment variable: `README.md` and `docs/DEVELOPMENT.md`
- New endpoint: `docs/API_REFERENCE.md`
- New architecture pattern: `docs/ARCHITECTURE.md`

## Code Style

- Keep functions and classes focused.
- Prefer explicit schemas/contracts over untyped dicts.
- Keep workflow YAML declarative; avoid hidden runtime coupling.
- Add concise comments only where behavior is non-obvious.

## Security

- Never commit secrets, keys, or production tokens.
- Prefer environment variables for credentials.
- Follow `SECURITY.md` for vulnerability reporting.

## Need Help?

Open a discussion or issue and use `SUPPORT.md` for support channels and expected response paths.
