# Coding Style

## Immutability (CRITICAL)

ALWAYS create new objects, NEVER mutate existing ones:

```
// Pseudocode
WRONG:  modify(original, field, value) → changes original in-place
CORRECT: update(original, field, value) → returns new copy with change
```

Rationale: Immutable data prevents hidden side effects, makes debugging easier, and enables safe concurrency.

## Formatting & Linting (Python)

Automated consistency, zero debates:
- **Black** (line-length 88) + **isort** (profile=black) on every save via pre-commit hooks
- **Ruff** as single linter — replaces Flake8, pylint, pycodestyle. Enable rules: E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF. Block merge on errors.
- **mypy --strict** in CI. Type hints on all function signatures and class attributes.
- For ML: annotate tensor shapes in docstrings (e.g., `# shape: (batch, seq_len, d_model)`)

## Naming (Python)

- **PEP 8 strictly:** snake_case functions/variables/modules, PascalCase classes, UPPER_SNAKE constants, _private prefix for internal APIs
- **Booleans as questions:** `is_trained`, `has_converged`
- **Name by intent, not type:** Avoid `df`, `model`, `X_train`. Prefer `customer_transactions`, `churn_classifier`, `training_features`
- Exception: short-lived loop vars and well-known ML conventions (X, y) in small scopes

## File Organization

MANY SMALL FILES > FEW LARGE FILES:
- High cohesion, low coupling
- 200-400 lines typical, 800 max
- Extract utilities from large modules
- Organize by feature/domain, not by type
- **pyproject.toml** as single config source — no scattered setup.cfg, .flake8, mypy.ini

## Error Handling

ALWAYS handle errors comprehensively:
- Handle errors explicitly at every level — `except: pass` is **forbidden**
- Provide user-friendly error messages in UI-facing code
- Log detailed error context on the server side with **structlog** or **loguru** (not print)
- Never silently swallow errors
- Use custom exception hierarchy: `DataValidationError`, `ModelNotTrainedError`, `PipelineTimeoutError`
- Map exceptions to HTTP codes at API boundaries
- **Never log secrets, PII, or raw model weights** (GDPR/CCPA compliance)

## Input Validation

ALWAYS validate at system boundaries:
- **Pydantic BaseModel** for API inputs, configs, pipeline interfaces
- **pandera** for data schemas before training
- Fail fast with clear error messages — reject bad data before a 3-hour training run
- Never trust external data (API responses, user input, file content)

## Constants & Configuration

- No magic numbers — extract all hyperparameters to config files (YAML/TOML) or dataclasses
- Use Hydra, OmegaConf, or Pydantic Settings for config management
- Makes experiments reproducible

## Code Quality Checklist

Before marking work complete:
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Proper error handling (no bare except)
- [ ] No hardcoded values (use constants or config)
- [ ] No mutation (immutable patterns used)
- [ ] Type hints on all signatures
- [ ] Structured logging (no print statements)
