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
# From the repo root
just setup
```

If you prefer a containerized workspace, open the repo in the provided devcontainer instead of bootstrapping locally.

## Development Workflow

1. Create a branch for your change.
2. Make the smallest coherent change set.
3. Add or update tests.
4. Update docs for behavior, API, config, or workflow changes.
5. Run local checks before opening a PR.

## Required Local Checks

```bash
# From the repo root
just test
just docs
pre-commit run --all-files
```

UI checks (when frontend files changed):

```bash
cd ui
npm run build
npm test
npm run test:coverage
```

The UI package enforces a 60% coverage floor in `ui/vitest.config.ts`.

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
- New bootstrap command or devcontainer behavior: `README.md`, `docs/ONBOARDING.md`, and `CONTRIBUTING.md`

## Code Style

- Keep functions and classes focused.
- Prefer explicit schemas/contracts over untyped dicts.
- Keep workflow YAML declarative; avoid hidden runtime coupling.
- Add concise comments only where behavior is non-obvious.

## Security

- Never commit secrets, keys, or production tokens.
- Prefer environment variables for credentials.
- Resolve runtime secrets through `agentic_v2.models.secrets.get_secret()` / `get_first_secret()` instead of reading `os.environ` directly in application code.
- Follow `SECURITY.md` for vulnerability reporting.

## Need Help?

Open a discussion or issue and use `SUPPORT.md` for support channels and expected response paths.
