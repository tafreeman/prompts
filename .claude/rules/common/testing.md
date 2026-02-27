# Testing Requirements

## Minimum Test Coverage: 80%

Test Types (ALL required):
1. **Unit Tests** - Individual functions, utilities, components
2. **Integration Tests** - API endpoints, database operations, pipeline stages
3. **E2E Tests** - Critical user flows (full train-to-inference for ML)

## Test-Driven Development

MANDATORY workflow:
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

## Testing Best Practices

- **Test behavior, not implementation** — assert output correct for input, Arrange-Act-Assert pattern
- Use `@pytest.mark.slow` for heavy tests — keep unit tests <5 min
- Flaky tests are bugs — fix or remove them
- Target 70-80% coverage on business logic

## ML-Specific Testing

- Test data loading schema and column types
- Test deterministic preprocessing (set seeds)
- Test model input/output shapes and valid prediction ranges
- Test saved model reload produces same output
- Use pytest fixtures for synthetic data

## CI Integration

- Every PR triggers: Ruff lint, mypy check, pytest
- Single failure blocks merge — no exceptions
- Keep unit tests <5 min total

## Code Review

- Style enforced by Black + Ruff — humans review for logic
- Review for: correctness, edge cases, error handling, security, performance
- 1 approval required. PRs <400 lines. Use PR templates.

## Troubleshooting Test Failures

1. Use **tdd-guide** agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

## Agent Support

- **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first
