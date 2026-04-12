# Prompt 06 — Rollout, validation, and documentation

## Use this for

Connecting the new behavior system to workflows, validating it end-to-end, and documenting how to operate it.

## Prompt

```markdown
# Role
You are an expert release engineer and AI workflow integrator specializing in safe rollout, validation strategy, and repository documentation.

# Objective
Finalize the rollout of self-correction loops and prompt sanitization in `C:\Users\tandf\source\prompts`.

# Reference source
Treat `C:\Users\tandf\source\claude-code-main` as the reference implementation source that inspired these repo changes.

As part of rollout and docs, make sure the implementation notes and documentation point back to the source patterns adapted from:

- `src/skills/`
- `src/tools/`
- `src/utils/tokenBudget.ts`
- `src/utils/diff.ts`
- `src/utils/treeify.ts`
- `src/bridge/`

# Tasks
1. Wire the new behavior system into the relevant workflows, runtime paths, and agent surfaces.
2. Validate the behavior end-to-end with representative scenarios.
3. Confirm which protections are advisory vs enforced.
4. Add or update documentation explaining:
   - how the skills are discovered and used
   - where sanitization runs
   - how retry limits work
   - how operators should interpret blocked/redacted results
5. Recommend any follow-on backlog items.

# Validation scenarios
Include tests or explicit checks for:
- successful self-correction after one failed test run
- verification loop stops after max retries
- clean prompt passes through unchanged
- secret-containing prompt gets redacted or blocked correctly
- false-positive candidate gets downgraded or approved correctly

# Constraints
- Prefer concrete test evidence over narrative claims.
- Keep docs aligned with actual implementation paths.
- Do not leave ambiguity about what is enforced in code.

# Deliverable format
1. Files updated
2. Validation evidence
3. Documentation changes
4. Remaining risks
5. Next backlog items
```
