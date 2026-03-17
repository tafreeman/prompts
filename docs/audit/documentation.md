# Documentation Audit

**Date:** 2026-03-17
**Auditor:** Claude Code (automated)
**Scope:** Accuracy of CLAUDE.md, READMEs, command descriptions, and cross-references

---

## Findings Summary

| # | Severity | Finding | Location |
|---|----------|---------|----------|
| DOC-1 | CRITICAL | Workflow count overstated (12 vs actual 6) | `CLAUDE.md` |
| DOC-2 | CRITICAL | Persona count overstated (24 vs actual 12) | `CLAUDE.md` |
| DOC-3 | CRITICAL | No `presentation/README.md` | `presentation/` |
| DOC-4 | HIGH | Tool count off-by-one (11 vs actual 12) | `CLAUDE.md` |
| DOC-5 | HIGH | Source line count stale (30.6K vs actual 36.3K) | `CLAUDE.md` |
| DOC-6 | HIGH | README lists 6 deleted workflows | `agentic-workflows-v2/README.md` |
| DOC-7 | HIGH | Content registry system undocumented | `presentation/` |
| DOC-8 | HIGH | Adapter system undocumented | `agentic-workflows-v2/` |
| DOC-9 | MEDIUM | 7 of 11 commands missing description fields | `.claude/commands/` |
| DOC-10 | MEDIUM | Roadmap references deleted persona files | `docs/IMPLEMENTATION_ROADMAP.md` |
| DOC-11 | MEDIUM | `docs/REPO_MAP.md` referenced but doesn't exist | `README.md` |

---

## Detailed Findings

### DOC-1: Workflow Count -- 12 Claimed, 6 Actual (CRITICAL)

**Location:** `CLAUDE.md`, Architecture section

CLAUDE.md states "12 YAML workflow definitions" but only 6 workflow files exist in `agentic-workflows-v2/agentic_v2/workflows/definitions/`:

| Workflow | Status |
|----------|--------|
| `bug_resolution.yaml` | Exists |
| `code_review.yaml` | Exists |
| `conditional_branching.yaml` | Exists |
| `fullstack_generation.yaml` | Exists |
| `iterative_review.yaml` | Exists |
| `test_deterministic.yaml` | Exists |
| 6 others previously listed | **Deleted** |

The discrepancy was introduced when workflows were cleaned up but CLAUDE.md was not updated. Since CLAUDE.md is the primary onboarding document, this creates immediate confusion for new contributors.

**Fix:** Update CLAUDE.md to state "6 YAML workflow definitions" with the correct list.

### DOC-2: Persona Count -- 24 Claimed, 12 Actual (CRITICAL)

**Location:** `CLAUDE.md`, Architecture section

CLAUDE.md states "24 agent persona definitions (.md)" but only 12 persona files remain in `agentic-workflows-v2/agentic_v2/prompts/`. The other 12 were deleted during the cleanup sprints.

**Fix:** Update CLAUDE.md to state "12 agent persona definitions (.md)". A script exists at `scripts/fix-claudemd-counts.py`.

### DOC-3: Missing Presentation README (CRITICAL)

**Location:** `presentation/`

The presentation package has a `CLAUDE.md` (for agent context) but no `README.md` for human developers. All other packages in the monorepo have READMEs. The presentation system is the most complex frontend package (10 decks, 34 layouts, 15 themes, Storybook) and has no onboarding documentation.

**Fix:** Create `presentation/README.md` covering setup, architecture, how to add layouts/decks/themes, and Storybook usage.

### DOC-4: Built-in Tool Count Off-by-One (HIGH)

**Location:** `CLAUDE.md`, Architecture section

CLAUDE.md states "11 built-in tool modules" but there are actually 12 in `agentic-workflows-v2/agentic_v2/tools/builtin/`. The 12th tool was added during Sprint 7 (RAG tools) but the count was not updated.

**Fix:** Update CLAUDE.md to state "12 built-in tool modules".

### DOC-5: Source Line Count Stale (HIGH)

**Location:** `CLAUDE.md`, Architecture section

CLAUDE.md states "Source (~30,600 lines)" but a current count shows approximately 36,300 lines. The ~6,000-line increase came from RAG pipeline implementation (Sprints 4-9) and was never reflected in the documentation.

**Fix:** Update CLAUDE.md to state "Source (~36,300 lines)".

### DOC-6: README Lists 6 Deleted Workflows (HIGH)

**Location:** `agentic-workflows-v2/README.md`, lines 95-102

The package README lists 6 workflows that were deleted during cleanup. Users following the README will encounter errors when trying to run these workflows.

**Fix:** Remove the 6 deleted workflow entries from the README. Add the actual 6 workflows.

### DOC-7: Content Registry System Undocumented (HIGH)

**Location:** `presentation/src/content/content-registry.ts`

The content registry (`content-registry.ts`, 150+ lines) is a key abstraction in the presentation system -- it maps deck IDs to content structures and enables dynamic deck loading. It is not mentioned anywhere in CLAUDE.md or any README.

**Fix:** Document the content registry in CLAUDE.md's presentation section and in the future `presentation/README.md`.

### DOC-8: Adapter System Undocumented (HIGH)

**Location:** `agentic-workflows-v2/agentic_v2/adapters/`

The adapter registry (`AdapterRegistry`) and its protocol (`ExecutionEngine`) are briefly mentioned in CLAUDE.md but there is no extension guide. A developer wanting to add a new execution backend has no documentation to follow.

**Fix:** Add an "Extending the Adapter System" section to CLAUDE.md or create `docs/guides/adapters.md`.

### DOC-9: Commands Missing Description Fields (MEDIUM)

**Location:** `.claude/commands/`

7 of the 11 slash commands in `.claude/commands/` are missing the `description` frontmatter field. Without descriptions, users running `/help` see command names but no explanation of what each command does.

| Command | Has Description? |
|---------|-----------------|
| `/audit` | No |
| `/build` | No |
| `/deploy` | No |
| `/fix` | No |
| `/review` | No |
| `/sprint` | No |
| `/validate` | No |
| `/commit` | Yes |
| `/plan` | Yes |
| `/test` | Yes |
| `/update-docs` | Yes |

**Fix:** Add one-line descriptions to the 7 commands missing them.

### DOC-10: Roadmap References Deleted Personas (MEDIUM)

**Location:** `docs/IMPLEMENTATION_ROADMAP.md`

The implementation roadmap references persona files that were deleted during cleanup sprints. The roadmap is completed (all 11 sprints done) so this is informational staleness rather than a blocking issue.

**Fix:** Update or annotate the roadmap to reflect the current state.

### DOC-11: `docs/REPO_MAP.md` Referenced but Missing (MEDIUM)

**Location:** Root `README.md`

The root README references `docs/REPO_MAP.md` for a detailed repository map, but this file does not exist. The link leads to a 404.

**Fix:** Either create `docs/REPO_MAP.md` or remove the reference from the README.

---

## Scriptable Fixes

| Fix | Effort | Script Available? |
|-----|--------|-------------------|
| Update CLAUDE.md counts (workflows, personas, tools, lines) | 10 min | Yes (`scripts/fix-claudemd-counts.py`) |
| Remove deleted workflows from README | 10 min | Manual |
| Add command descriptions | 20 min | Manual |
| Create `presentation/README.md` | 30 min | Manual |

---

## Recommended Priority

1. **Immediate (misleads developers):** DOC-1, DOC-2 (fix counts in CLAUDE.md)
2. **Immediate (onboarding gap):** DOC-3 (create presentation README)
3. **Next sprint:** DOC-4 through DOC-8 (stale counts, missing docs)
4. **Backlog:** DOC-9 through DOC-11 (polish)
