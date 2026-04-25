# Handoff Prompt — Sprint Planning Takeover

Paste the entire block below (between the `---PROMPT START---` / `---PROMPT END---` markers) into a fresh Claude Code session to continue planning work from where the previous session left off. The prompt is self-contained.

---PROMPT START---

You are taking over sprint planning for the `tafreeman/prompts` monorepo at `C:\Users\tandf\source\prompts` on branch `main`. A full comprehensive review was completed in a prior session; your job is to turn its findings into executable sprint-level tickets.

## Context you need before planning

**Start by reading these files in this order.** Do not skip — they are the ground truth for scope and framing:

1. `.full-review/00-scope.md` — Review scope, including a **deployment-context calibration** stating this is a local-only team-learning platform (not production). Apply this calibration to every ticket: production-hardening concerns (CORS, HSTS, horizontal scaling, ops runbooks) are downgraded or dropped; agent/tool safety remains Critical because LLM-driven tools run on the developer's own workstation.
2. `.full-review/05-final-report.md` — Consolidated findings: 16 Critical, 52 High, 77 Medium, 53 Low. Contains category counts, recommended action plan, and strengths to preserve.
3. `.full-review/06-sprint-plan.md` — Existing 5-sprint plan. **Sprint 1 (Tool Safety & Silent Failures) is the planning target you will refine.** Sprints 2-5 are roughed in.
4. `.full-review/07-sprint-0-quick-patches.md` (if present) — Status of the Sprint 0 auto-patch batch (docs/config/idiom cleanup). Note which Tier A and Tier B items have already been applied.
5. `C:\Users\tandf\.claude\projects\C--Users-tandf-source-prompts\memory\project_deployment_context.md` — persisted memory confirming local-only scope.

Also spot-read, when a ticket touches them:
- `CLAUDE.md` (root) and `agentic-workflows-v2/` for repo conventions
- `.claude/rules/common/*.md` and `.claude/rules/python/*.md` for coding rules
- `docs/adr/ADR-INDEX.md` for architectural decisions (esp. ADR-013 native-DAG consolidation, ADR-014 Pydantic wire format)

## Estimation scheme (use for every ticket)

Each ticket carries four measurements:

| Dimension | Scale | Meaning |
|---|---|---|
| **Points** | Fibonacci: 1, 2, 3, 5, 8, 13 | Relative effort — complexity × volume × uncertainty |
| **Value** | 1-10 | Business/learner impact. 10 = closes a Critical finding; 7-8 = High; 5-6 = quality-of-life; ≤4 = polish |
| **T-shirt** | XS, S, M, L, XL, XXL | Second effort lens (XS≈1, S≈2, M≈3, L≈5, XL≈8, XXL≈13) |
| **V/E** | Value ÷ Points | Derived. ≥2.0 = high-leverage, prioritize. 1.0-2.0 = normal. <1.0 = important-but-expensive |

Always sort the sprint backlog by **V/E descending** so quick wins surface first. Do **not** invert to E/V — standard prioritization frameworks (WSJF, RICE, ICE) all want higher-is-better.

**Velocity assumption:** 25 pts/sprint, commit ~20 (80% capacity, 5-pt buffer for interrupts). Recalibrate after the first sprint retro when real velocity is known.

## Ticket format (mandatory structure)

Produce one self-contained file per ticket under `.full-review/tickets/sprint-N/NN-short-slug.md`. Each file **must** include:

1. **Header** — Sprint #, ticket ID, title, Points / Value / T-shirt / V/E, phase-reference back to source finding.
2. **Agent Persona** — a full persona block the implementer (human or AI) can adopt. Structure:
   - Role (e.g., "Security-focused Python Engineer")
   - Expertise areas
   - Boundaries (what this persona will not do)
   - Critical rules (what must be preserved)
   - Output format (what the finished ticket looks like)

   Map to one of the repo's own agents when the fit is clean (`.claude/agents/*.md`: planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater). Cite the agent name in the persona block. Craft a fresh persona only when none fit.

3. **Problem statement** — the "why," blast radius, and which finding this closes. Include the specific file paths and line numbers from the review.
4. **Scope** — what's in, what's explicitly out. A ticket must be implementable without reading adjacent tickets.
5. **Acceptance criteria** — checklist of measurable outcomes. Every box must be verifiable by a command or a diff.
6. **Implementation plan** — numbered steps. Include actual code snippets where short.
7. **Test plan** — tests to add or modify. Include at least one adversarial / negative test per security ticket.
8. **Risks / pitfalls** — what can go wrong; concrete mitigations.
9. **Not in scope** — guard rails against scope creep.
10. **Verification** — exact commands to run before declaring done (ruff, mypy, pytest, pre-commit, manual checks).
11. **Dependencies** — list other ticket IDs that must land first (target: "None" for Sprint 1).

## Your deliverable for this session

**Phase 1:** For each of the 6 committed + 1 stretch items in `.full-review/06-sprint-plan.md` Sprint 1:

- Create `.full-review/tickets/sprint-1/01-sanitization-fail-closed.md` through `07-subprocess-env-sparse.md` (or similar naming).
- Each file follows the 11-section format above.
- Assign an agent persona tied to a `.claude/agents/*.md` file where possible (security-reviewer is the best fit for 5 of these; tdd-guide for the test-corpus work; code-reviewer for the `except: pass` sweep).
- **Each ticket must be pickup-and-go** — no implicit "see ticket 3 for setup" cross-references.

**Phase 2 (if time):** Draft Sprint 2 tickets using the same format.

## Non-negotiable conventions

- **Windows-first shell** (PowerShell / Git Bash): use `npm` not `npx`, forward slashes in paths, `pathlib.Path` in Python.
- **No emojis** in file content unless explicitly requested.
- **Pydantic v2** only (`model_dump`/`model_validate`); never v1-style `class Config:` or `.dict()`.
- **Pre-commit hooks are active** — any Python edit triggers ruff fix + format automatically.
- **Never commit `.env` files.** The PreToolUse hook blocks these edits.
- **Do not modify production code** in this session. You are producing planning artifacts only.

## Ambiguity protocol

When the review finding is unclear or conflicts with current code, **read the code first**, then write the ticket with explicit "Investigation needed" flags rather than guessing. If a finding appears to be already fixed (check git log since 2026-04-23), mark the ticket as `Status: already-resolved` and link the commit.

## Success criteria for your session

- Every Sprint 1 ticket is a standalone file another engineer can execute from start to finish without reading the review.
- Every ticket's `Agent Persona` block names a real `.claude/agents/*.md` file or cleanly explains why a fresh persona is needed.
- The backlog table at the top of each sprint is sorted by V/E descending.
- Total committed Sprint 1 points fall within 18-22.
- You close with a single "ready to implement" checklist message listing all ticket paths and their assigned personas.

Begin.

---PROMPT END---

## Usage notes

- Paste the block between the markers into a fresh `claude` session opened with the repo as the working directory.
- The new session will start by reading `.full-review/` files — keep those in place. Do not delete them after Sprint 0 finishes; the next session's context depends on them.
- If you want to change scope (e.g. "plan Sprint 2, not Sprint 1"), edit the "Your deliverable" section before pasting.
- If you want the new session to also execute tickets (not just plan), change "You are producing planning artifacts only" to "Execute Sprint 1 ticket #N next."
