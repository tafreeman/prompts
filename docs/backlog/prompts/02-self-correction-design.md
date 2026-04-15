# Prompt 02 — Self-correction and verification loop design

## Use this for

Designing reusable agent behaviors for bounded retry, verification, and failure escalation.

## Prompt

```markdown
# Role
You are an expert prompt-systems designer specializing in reliable coding agents, bounded repair loops, and workflow-safe verification behavior.

# Objective
Design a reusable self-correction and verification system for `C:\Users\tandf\source\prompts`.

This behavior should help agents:
- run tests after code changes
- inspect lint/type/test failures
- retry fixes up to a bounded maximum
- escalate clearly when they cannot resolve the issue

# Reference source
Base the design on patterns extracted from:

- `C:\Users\tandf\source\claude-code-main`

Focus especially on behavior ideas visible in:

- `src/skills/`
- `src/skills/bundled/verify.ts`
- `src/skills/bundled/batch.ts`
- `src/tools/TodoWriteTool/`
- `src/tools/TaskCreateTool/`
- `src/tools/TaskUpdateTool/`

# Tasks
1. Propose the best set of skills and/or instructions for this behavior.
2. Decide whether to create one generic verification-loop skill or several specialized skills.
3. Design behavior differences for:
   - code generation
   - workflow authoring
   - research / non-code tasks
4. Define retry limits, stop conditions, and escalation rules.
5. Propose exact filenames, descriptions, and trigger wording for each skill or instruction.
6. Draft the behavioral rules each file should contain.

# Constraints
- Use bounded retries; no infinite loops.
- Prefer reusable behaviors over persona-specific duplication.
- Separate advisory prompting from runtime-enforced checks.
- Align with Python-first orchestration and existing `.claude` conventions.

# Deliverable format
Return:
1. Recommended behavior model
2. Proposed skills/instructions
3. File names and locations
4. Retry and escalation policy
5. Example rule content for each file
6. Risks and tradeoffs
```
