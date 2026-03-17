---
description: Enforce test-driven development workflow. Scaffold interfaces, generate tests FIRST, then implement minimal code to pass. Ensure 80%+ coverage.
---

# TDD Command

This command invokes the **tdd-guide** agent to enforce test-driven development methodology.

## What This Command Does

1. **Scaffold Interfaces** - Define types/interfaces first
2. **Generate Tests First** - Write failing tests (RED)
3. **Implement Minimal Code** - Write just enough to pass (GREEN)
4. **Refactor** - Improve code while keeping tests green (REFACTOR)
5. **Verify Coverage** - Ensure 80%+ test coverage

## When to Use

Use `/tdd` when:
- Implementing new features
- Adding new functions/components
- Fixing bugs (write test that reproduces bug first)
- Refactoring existing code
- Building critical business logic

## How It Works

The tdd-guide agent will:

1. **Define interfaces** for inputs/outputs
2. **Write tests that will FAIL** (because code doesn't exist yet)
3. **Run tests** and verify they fail for the right reason
4. **Write minimal implementation** to make tests pass
5. **Run tests** and verify they pass
6. **Refactor** code while keeping tests green
7. **Check coverage** and add more tests if below 80%

## TDD Cycle

```
RED → GREEN → REFACTOR → REPEAT

RED:      Write a failing test
GREEN:    Write minimal code to pass
REFACTOR: Improve code, keep tests passing
REPEAT:   Next feature/scenario
```

## Example Usage

```
User: /tdd I need a profile-specific recency window helper for deep research scoring

Agent (tdd-guide):
# TDD Session: Profile-Specific Recency Window

## Step 1: Define Interface (SCAFFOLD)

# agentic_v2/server/scoring_profiles.py
def resolve_recency_window(profile_name: str, overrides: dict[str, int] | None = None) -> int:
    raise NotImplementedError

## Step 2: Write Failing Test (RED)

# tests/test_multidimensional_scoring.py
def test_uses_profile_specific_window_when_present():
    assert resolve_recency_window("tax_law", {"tax_law": 183}) == 183

def test_falls_back_to_default_window():
    assert resolve_recency_window("general", None) == DEFAULT_RECENCY_WINDOW_DAYS

def test_rejects_non_positive_window():
    with pytest.raises(ValueError):
        resolve_recency_window("tax_law", {"tax_law": 0})

## Step 3: Run Tests - Verify FAIL

python -m pytest tests/test_multidimensional_scoring.py -k recency_window -v
FAILED - NotImplementedError
3 failed, 0 passed

## Step 4: Implement (GREEN) → Step 5: Verify PASS → Step 6: Refactor

## Step 7: Check Coverage

python -m pytest tests/test_multidimensional_scoring.py -k recency_window --cov=agentic_v2.server.scoring_profiles
Coverage: 100%
```

## TDD Best Practices

**DO:**
- ✅ Write the test FIRST, before any implementation
- ✅ Run tests and verify they FAIL before implementing
- ✅ Write minimal code to make tests pass
- ✅ Refactor only after tests are green
- ✅ Add edge cases and error scenarios
- ✅ Aim for 80%+ coverage (100% for critical code)

**DON'T:**
- ❌ Write implementation before tests
- ❌ Skip running tests after each change
- ❌ Write too much code at once
- ❌ Ignore failing tests
- ❌ Test implementation details (test behavior)
- ❌ Mock everything (prefer integration tests)

## Test Types to Include

**Unit Tests** (Function-level):
- Happy path scenarios
- Edge cases (empty, null, max values)
- Error conditions
- Boundary values

**Integration Tests** (Component-level):
- API endpoints (FastAPI routes)
- Pipeline stages (RAG ingest → retrieve → assemble)
- External service calls (LLM providers)

**E2E Tests** (use the `e2e-runner` agent or the project's browser test tooling):
- Critical user flows
- Multi-step processes
- Full stack integration

## Coverage Requirements

- **80% minimum** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

## Important Notes

**MANDATORY**: Tests must be written BEFORE implementation. The TDD cycle is:

1. **RED** - Write failing test
2. **GREEN** - Implement to pass
3. **REFACTOR** - Improve code

Never skip the RED phase. Never write code before tests.

## Integration with Other Commands

- Use `/plan` first to understand what to build
- Use `/tdd` to implement with tests
- Use `/build-fix` if build errors occur
- Use `/code-review` to review implementation
- Use `/test-coverage` to verify coverage

## Related Agents

This command invokes the `tdd-guide` agent located at:
`.claude/agents/tdd-guide.md`

Canonical testing expectations live in:
- `.claude/rules/common/testing.md`
- `.claude/rules/python/testing.md`
