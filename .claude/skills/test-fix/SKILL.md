---
name: test-fix
description: Autonomous test-and-fix loop. Runs tests, diagnoses failures, fixes source code (not tests unless tests are wrong), re-runs to verify, and commits each fix separately. Loops until green or max 3 attempts per failure.
---

# Test & Fix Loop

Autonomous red→green pipeline. Run tests, fix failures, verify, commit — no user input needed.

## Trigger

Use when:
- User says "fix tests", "make tests pass", "test and fix"
- After a large refactor that likely broke tests
- As part of a CI-local pipeline

## Algorithm

```
1. RUN full test suite, capture output
2. PARSE failures into a list: [{file, test_name, error}]
3. If 0 failures → REPORT success, STOP
4. For each failing test (max 10):
   a. READ the test file and the source file it tests
   b. DIAGNOSE root cause — is the test wrong or the source wrong?
   c. FIX the source code (prefer fixing source over tests)
      - Only fix the test if the test itself has a bug or tests outdated behavior
   d. RUN just that single test to verify the fix
   e. If still failing, retry up to 2 more times (3 total attempts)
   f. If fixed, stage and COMMIT with message: "fix: <what was broken>"
5. RUN full test suite again to check for regressions
6. REPORT summary: fixed N/M failures, any remaining
```

## Rules

- **Fix source, not tests** — unless the test is genuinely wrong
- **One commit per logical fix** — don't batch unrelated fixes
- **Max 3 attempts per failure** — if still broken after 3, skip and report
- **Max 10 failures per run** — if more than 10, fix first 10 and re-run
- **Never delete tests** — fix them or skip them
- **Run full suite at end** — catch regressions from fixes

## Test Commands

Detect the right test runner based on location:
- `agentic-workflows-v2/tests/` → `python -m pytest agentic-workflows-v2/tests/ -q --tb=short`
- `agentic-v2-eval/tests/` → `python -m pytest agentic-v2-eval/tests/ -q --tb=short`
- `tools/tests/` → `python -m pytest tools/tests/ -q --tb=short`
- `agentic-workflows-v2/ui/` → `cd agentic-workflows-v2/ui && npm test`
- If user specifies a path, use that path

## Output

```
## Test & Fix Report
- **Initial failures:** N
- **Fixed:** X (list each with commit SHA)
- **Remaining:** Y (list each with diagnosis)
- **Regressions:** Z (any new failures from fixes)
- **Final status:** ✅ ALL GREEN | ⚠️ X remaining
```
