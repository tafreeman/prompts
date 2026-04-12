# Prompt 05 — Implement middleware and contracts

## Use this for

Building the Python runtime sanitization layer and verification-loop support contracts.

## Prompt

```markdown
# Role
You are an expert Python infrastructure engineer specializing in LLM middleware, safety enforcement, typed contracts, and workflow runtime integration.

# Objective
Implement the approved runtime enforcement pieces in `C:\Users\tandf\source\prompts` for:

1. prompt sanitization and security checks
2. verification-loop policies and result models

# Reference source
Use `C:\Users\tandf\source\claude-code-main` as the source repository for the patterns being adapted.

The implementation should explicitly trace back to concepts reviewed in:

- `src/utils/tokenBudget.ts`
- `src/utils/diff.ts`
- `src/utils/treeify.ts`
- `src/tools/`
- `src/bridge/`

# Tasks
1. Add the Python modules, dataclasses/Pydantic models, and helpers required for prompt sanitization.
2. Implement result classifications such as:
   - clean
   - redacted
   - blocked
   - requires-approval
3. Add verification-loop contracts and policy structures.
4. Integrate the sanitization step into the relevant outbound prompt path.
5. Add tests for:
   - happy-path clean input
   - redaction cases
   - blocked cases
   - false positives
   - retry/verification edge cases
6. Keep logging safe and never log raw secrets.

# Constraints
- Prefer additive changes.
- Use Python 3.11+ typing and repo conventions.
- Keep security-critical behavior enforced in code, not only in prompts.
- Avoid brittle regex-only design; allow extensibility for future detectors.

# Deliverable format
1. Files changed
2. Core contracts/models added
3. Integration points
4. Tests added
5. Remaining gaps or follow-ups
```
