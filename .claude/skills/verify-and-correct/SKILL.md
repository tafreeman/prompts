---
name: verify-and-correct
description: >
  Bounded self-correction loop for code changes. Automatically runs tests,
  lint, and type checks after modifications, then retries fixes up to a limit.
whenToUse: >
  Use when: writing or modifying code, fixing bugs, implementing features,
  refactoring, resolving test failures, addressing code review feedback,
  making changes that could break existing tests.
aliases:
  - self-correct
  - fix-and-verify
  - retry-loop
  - bounded-retry
---

# Verify and Correct

## Purpose

Ensure every code change passes automated quality gates before being considered complete. This skill implements a bounded retry loop — never silently passing with known failures.

## Behavior

After ANY code change:

1. **Verify** — Run the verification suite:
   - `pytest tests/ -x --timeout=120` (fail-fast)
   - `ruff check .` (lint)
   - `mypy --strict src/` (type safety)
2. **Assess** — Check all results:
   - If ALL pass → **done**, report success
   - If ANY fail → proceed to step 3
3. **Analyze** — Read the failure output carefully:
   - Identify the root cause (not just the symptom)
   - Determine if this is a code bug, a test bug, or a configuration issue
4. **Correct** — Apply a targeted fix:
   - Fix the specific issue identified
   - Do NOT rewrite from scratch
   - Do NOT make unrelated changes
   - Prefer the smallest diff that fixes the problem
5. **Re-verify** — Run the full verification suite again
6. **Repeat** — Go to step 2, up to 3 times maximum

## Stop Conditions

Stop the loop when ANY of these are true:

- All verification checks pass
- **3 correction attempts** exhausted
- **Token budget** for corrections exceeded (25% of remaining budget)
- **Loop detected** — same failure repeats identically across 2 consecutive attempts
- **Scope escalation** — the fix requires changes outside the current file/module

## Loop Detection

If two consecutive attempts produce identical failing checks with identical error messages, STOP immediately. This indicates the correction strategy is not working and needs human input.

## Escalation Protocol

When stopping without full success:

1. **Summarize** what was attempted (list each correction and its result)
2. **List** remaining failures with exact error messages and file locations
3. **Diagnose** — explain why the corrections didn't resolve the issue
4. **Recommend** specific next steps for the orchestrator or human:
   - "This requires a design change in X"
   - "The test expectations need updating because Y changed"
   - "A dependency conflict between A and B needs resolution"
5. **NEVER** silently pass with known failures
6. **NEVER** delete or skip failing tests to make the suite pass

## Token Budget Awareness

- Before each correction attempt, estimate the cost
- If remaining budget is below 1000 tokens, skip verification entirely
- Track cumulative token usage across all attempts
- Report total tokens used in the escalation summary

## Examples

### Successful Correction
```
Attempt 1: pytest failed — NameError in test_sanitizer.py:42
Fix: Added missing import for `SanitizationResult`
Attempt 2: All checks pass ✓
Total: 2 attempts, 1 correction, 340 tokens
```

### Escalated Failure
```
Attempt 1: mypy error — incompatible return type in client.py:88
Fix: Changed return annotation to `SanitizationResult | None`
Attempt 2: mypy error — 3 new type errors from callers of client.py:88
Fix: Updated caller signatures in routes.py, execution.py
Attempt 3: pytest failed — integration test expects old return type
STOP: 3 attempts exhausted

Remaining failures:
- tests/test_integration.py::test_run_workflow — AssertionError: expected str, got SanitizationResult
Recommendation: Update integration test expectations to match new return type
```
