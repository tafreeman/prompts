# Context Engineering Audit — Full Analysis & ADR Index

> **Audit date:** 2026-03-15
> **Scope:** `.claude/`, `docs/adr/`, `research/`, `.github/agents/`, CLAUDE.md, MEMORY.md
> **Finding count:** 14 issues (4 CRITICAL, 5 HIGH, 5 MEDIUM)

---

## Executive Summary

The repo's context engineering setup is **extensive and well-intentioned** but suffers from four systemic problems:

1. **Massive duplication** — 730 files replicated across 3 worktrees with zero differentiation
2. **Broken references** — Skills reference sub-files that don't exist
3. **Stale compiled records** — `ADR_COMPILED.md` is 14 days behind the latest individual ADRs
4. **Overlapping instruction surfaces** — The same guidance appears in CLAUDE.md, rules/, commands/, skills/, and `.github/agents/` with no clear precedence

---

## Part 1: Issues Found

### CRITICAL Issues

#### C-1: Worktree Duplication Explosion (730 files)

**Location:** `.claude/worktrees/{frosty-bohr,laughing-einstein,practical-payne}/.claude/`

All 3 worktrees contain **byte-identical copies** of every command, context, rule, skill, and config file. MD5 checksums confirm zero differentiation.

| Content Type | Files × 3 Worktrees | Total Duplicates |
|---|---|---|
| Commands (11) | 33 | 22 redundant |
| Contexts (3) | 9 | 6 redundant |
| Rules (12) | 36 | 24 redundant |
| Skills (9+) | ~50 | ~35 redundant |
| Configs (2) | 6 | 4 redundant |
| **TOTAL** | — | **~730 files, ~90% redundant** |

**Impact:** Any change to a rule or command requires manual propagation to 3 worktrees. Drift is inevitable. Each worktree's `.claude/` loads ALL rules into context — tripling the token budget consumed by identical instructions.

**Fix:** Worktrees should inherit from the parent `.claude/` directory. Only worktree-specific overrides should exist in worktree subdirectories.

---

#### C-2: Broken Skill References (Dead Links)

**Location:** `.claude/skills/context-engineering/SKILL.md`, `.claude/skills/code-review/SKILL.md`

The `context-engineering` skill references 9 sub-files that **do not exist**:

```
references/context-fundamentals.md     ← MISSING
references/context-degradation.md      ← MISSING
references/context-optimization.md     ← MISSING
references/context-compression.md      ← MISSING
references/memory-systems.md           ← MISSING
references/multi-agent-patterns.md     ← MISSING
references/evaluation.md               ← MISSING
references/tool-design.md              ← MISSING
references/project-development.md      ← MISSING
scripts/context_analyzer.py            ← MISSING
scripts/compression_evaluator.py       ← MISSING
```

The `code-review` skill references 3 sub-files that **do not exist**:

```
references/code-review-reception.md         ← MISSING
references/requesting-code-review.md        ← MISSING
references/verification-before-completion.md ← MISSING
```

**Impact:** Skills claim capabilities they cannot deliver. When invoked, they provide only the SKILL.md surface content — the detailed protocols and reference material are absent.

**Fix:** Either create the referenced files or consolidate the content into the SKILL.md files directly.

---

#### C-3: ADR Compiled Registry is Stale

**Location:** `docs/adr/ADR_COMPILED.md`

| File | Last Modified | Status |
|---|---|---|
| `ADR_COMPILED.md` | 2026-03-01 | **STALE** |
| `ADR-009-scoring-enhancements.md` | 2026-03-03 | Not in compiled |
| `ADR-010-eval-harness-methodology.md` | 2026-03-09 | Not in compiled |
| `ADR-011-eval-harness-api-interface.md` | 2026-03-09 | Not in compiled |
| `ADR-012-ui-evaluation-hub.md` | 2026-03-09 | Not in compiled |
| `ADR-008-testing-approach-overhaul.md` | 2026-03-09 | Listed but content may be stale |

The compiled registry is **missing 4 ADRs entirely** (009, 010, 011, 012) and the ADR-008 entry may be outdated since the source was modified 8 days after the compilation.

**Impact:** Any consumer relying on `ADR_COMPILED.md` as the canonical source gets an incomplete picture. The CLAUDE.md references only ADR-001 through ADR-003 in the Implementation Roadmap.

**Fix:** Auto-generate `ADR_COMPILED.md` from individual ADR files, or abandon the compiled file in favor of a lightweight index.

---

#### C-4: Overlapping Instruction Surfaces with No Precedence Rules

The same topics are covered in multiple places with **no declared loading priority**:

| Topic | Locations | Overlap |
|---|---|---|
| Code review | `commands/code-review.md`, `skills/code-review/SKILL.md`, `rules/common/testing.md` (§Code Review), `.github/agents/code-review-agent.agent.md`, agent `code-reviewer` | 5 locations |
| Testing/TDD | `commands/tdd.md`, `rules/common/testing.md`, `rules/python/testing.md`, agent `tdd-guide` | 4 locations |
| Security | `rules/common/security.md`, `rules/python/security.md`, `.github/agents/security-agent.agent.md`, agent `security-reviewer` | 4 locations |
| Planning | `commands/plan.md`, `rules/common/agents.md` (§planner), `.github/agents/architecture-agent.agent.md`, agent `planner` | 4 locations |
| Build fixing | `commands/build-fix.md`, agent `build-error-resolver` | 2 locations |
| Coding style | `rules/common/coding-style.md`, `rules/python/coding-style.md`, `docs/CODING_STANDARDS.md` | 3 locations |

**Impact:** When rules, commands, skills, and agents all provide instructions on the same topic, the model receives contradictory or redundant guidance. Token budget is consumed by repetition. The Python testing rule says "See skill: `python-testing`" but no such skill exists. The Python security rule says "See skill: `django-security`" — this is a Django-specific skill reference in a non-Django project.

**Fix:** Establish a clear hierarchy: rules → canonical behavioral constraints; commands → invocation entry points (delegate to agents); skills → detailed multi-step protocols; agents → execution specialists. Each layer should reference the others, not duplicate content.

---

### HIGH Issues

#### H-1: `.github/agents/` Parallel Agent System

**Location:** `.github/agents/` (19 files)

A completely separate agent definition system exists under `.github/agents/` with its own:
- Agent template (`agent-template.md`)
- Registry schema (`registry-schema.json`)
- Guide (`AGENTS_GUIDE.md`)
- 15+ agent definitions

These `.github/agents/*.agent.md` files are **not loaded by Claude Code** — they're a GitHub-specific format. They duplicate roles already covered by the `.claude/` agents (code-reviewer, security-reviewer, architect, etc.) but with different instructions.

**Impact:** Two parallel agent systems with divergent instructions. Maintainers may update one without the other.

**Fix:** Consolidate to one system. If `.github/agents/` serves GitHub Copilot, mark it explicitly and cross-reference the `.claude/` agents as authoritative.

---

#### H-2: CLAUDE.md Duplicated in Worktree

**Location:** `CLAUDE.md` (root) vs `.claude/worktrees/frosty-bohr/CLAUDE.md`

The root CLAUDE.md and the worktree CLAUDE.md are identical. When working in the worktree, both are loaded, doubling the base instruction token cost.

**Fix:** Worktree CLAUDE.md should either be a symlink or contain only worktree-specific overrides.

---

#### H-3: settings.local.json Contains Stale Permissions

**Location:** `.claude/settings.local.json`

The permissions allowlist contains 87+ entries, many of which are:
- One-time PID-specific commands: `Bash(cmd /c "taskkill /PID 6676 /F")`
- Overly specific paths: `Bash(cmd.exe //c "D:\\\\source\\\\prompts\\\\...")`
- Duplicate patterns: Multiple `Bash(python:*)`, `Bash(python *)`
- Dead MCP references: `mcp__contextstream__init`, `mcp__filesystem__*`

**Impact:** Bloated permission file, confusing to audit, may grant unintended access to tools no longer in use.

**Fix:** Clean up to ~20 pattern-based permissions. Remove PID-specific one-offs and path-specific duplicates.

---

#### H-4: Python Rules Reference Non-Existent Skills

**Location:** `.claude/rules/python/*.md`

| Rule File | References | Exists? |
|---|---|---|
| `python/coding-style.md` | `skill: python-patterns` | ❌ No |
| `python/testing.md` | `skill: python-testing` | ❌ No |
| `python/security.md` | `skill: django-security` | ❌ No (wrong framework) |
| `python/hooks.md` | `common/hooks.md` | ❌ No common hooks rule |

**Fix:** Remove broken references or create the missing skills.

---

#### H-5: ADR Numbering Inconsistency

Two numbering schemes coexist:

| Scheme | ADRs | Format |
|---|---|---|
| 3-digit | ADR-001, ADR-002, ADR-003, ADR-007, ADR-008, ADR-009, ADR-010, ADR-011, ADR-012 | Individual files in `docs/adr/` |
| 4-digit | ADR-0001 through ADR-0023 | Referenced in `ADR_COMPILED.md` as "planned" |

The 4-digit ADRs (ADR-0001 through ADR-0003) cover package structure decisions that overlap with but are distinct from ADR-001 through ADR-003 (architecture decisions). The `ADR_IMPLEMENTATION_AUDIT.md` audits both schemes, creating confusion.

Additionally, ADR-004, ADR-005, ADR-006 are **missing** — the sequence jumps from 003 to 007.

**Fix:** Adopt a single numbering scheme. Document the gap (004-006 were either never created or merged into others).

---

### MEDIUM Issues

#### M-1: Research Library Orphaned Content

`research/library/material_manifest.json` and `research/library/source_registry.json` — JSON registries that may be stale. The research subagent reports (`CURATOR_REPORT.md`, `LIBRARIAN_REPORT.md`, etc.) are undated.

#### M-2: Contexts Are Too Thin

The 3 context files (`dev.md`, `research.md`, `review.md`) are 15-27 lines each — mostly behavioral hints. They add token cost without significantly altering behavior beyond what rules already provide.

#### M-3: MEMORY.md Contains Stale Server Notes

The auto-memory file references `Port 8000 blocked by elevated process — always use --port 8001` but `launch.json` configures port 8010. These may refer to different situations but create confusion.

#### M-4: ADR Supersession Chain Unclear

ADR-003 states "Superseded-By: ADR-007" but both files remain active. ADR-007 then ADR-009 extends ADR-007. The chain `ADR-003 → ADR-007 → ADR-009` is not documented as a unified lineage anywhere.

#### M-5: Command Examples Use Wrong Tech Stack

`/plan` and `/tdd` commands contain examples using TypeScript/Node.js patterns (Redis, BullMQ, SendGrid, npm test) despite the project being Python-first. This could mislead Claude about the project's tech stack.

---

## Part 2: ADR Registry — Structured Index

### Quick-Access ADR Deck

| ADR | Title | Status | File | Domain | Dependencies |
|-----|-------|--------|------|--------|-------------|
| **001** | Dual Execution Engine (LangGraph vs. Kahn's DAG) | 🟢 Accepted | [ADR-001-002-003](adr/ADR-001-002-003-architecture-decisions.md) | Engine | — |
| **002** | SmartModelRouter Circuit-Breaker Hardening | 🟢 Accepted | [ADR-001-002-003](adr/ADR-001-002-003-architecture-decisions.md) | Models | — |
| **003** | Deep Research Supervisor / CI Gating | ⚫ Superseded | [ADR-001-002-003](adr/ADR-001-002-003-architecture-decisions.md) | Research | → ADR-007 |
| **007** | Multidimensional Classification Matrix & Stop Policy | 🟡 Proposed | [ADR-007](adr/ADR-007-classification-matrix-stop-policy.md) | Research | ← ADR-003, → ADR-009 |
| **008** | Testing Approach Overhaul (Value Taxonomy) | 🟡 Proposed | [ADR-008](adr/ADR-008-testing-approach-overhaul.md) | Testing | — |
| **009** | Scoring Enhancements (Exponential Decay, Lexicographic) | 🟢 Accepted | [ADR-009](adr/ADR-009-scoring-enhancements.md) | Research | ← ADR-007 |
| **010** | Commit-Driven A/B Eval Harness Methodology | 🟡 Proposed | [ADR-010](adr/ADR-010-eval-harness-methodology.md) | Eval | — |
| **011** | Eval Harness API & Interface Design | 🟡 Proposed | [ADR-011](adr/ADR-011-eval-harness-api-interface.md) | Eval | ← ADR-010 |
| **012** | UI Evaluation Hub & A/B Comparison | 🟡 Proposed | [ADR-012](adr/ADR-012-ui-evaluation-hub.md) | UI | ← ADR-011 |

### ADR Lineage Chains

```
Engine Domain:
  ADR-001 (Dual Engine) ─── standalone, ~40% implemented

Models Domain:
  ADR-002 (Circuit Breaker) ─── standalone, ~100% implemented

Research Domain:
  ADR-003 (CI Gating) ──superseded-by──→ ADR-007 (Classification Matrix)
                                              └──extended-by──→ ADR-009 (Scoring Enhancements)

Testing Domain:
  ADR-008 (Test Value Taxonomy) ─── standalone, Phase 0 completed

Evaluation Domain:
  ADR-010 (Harness Methodology) ──extended-by──→ ADR-011 (API Interface)
                                                      └──extended-by──→ ADR-012 (UI Hub)
```

### Implementation Status Matrix

| ADR | Decision Made | Implemented | Tests | Audit Date |
|-----|:---:|:---:|:---:|---|
| 001 | ✅ | ~40% | ✅ Protocol tests | 2026-02-28 |
| 002 | ✅ | ~100% | ✅ 67 tests | 2026-02-28 |
| 003 | ⚫ Superseded | N/A | N/A | — |
| 007 | ✅ | ~50% | Partial | 2026-02-28 |
| 008 | ✅ | Phase 0 ✅ | N/A (meta-ADR) | 2026-03-09 |
| 009 | ✅ | ✅ | 28 new tests | 2026-03-03 |
| 010 | 🔲 Proposed | 0% | — | — |
| 011 | 🔲 Proposed | 0% | — | — |
| 012 | 🔲 Proposed | 0% | — | — |

---

## Part 3: Configuration Preset Structure

### Recommended Preset Layout

To make all context engineering "decks" accessible as configuration presets, restructure as follows:

```
.claude/
├── CLAUDE.md                      # Root instructions (auto-loaded)
├── settings.local.json            # Permissions (cleaned up)
├── launch.json                    # Dev server configs
│
├── presets/                       # NEW — switchable configuration decks
│   ├── preset-index.yaml          # Registry of all presets
│   ├── dev.yaml                   # Development mode preset
│   ├── research.yaml              # Research mode preset
│   ├── review.yaml                # Code review mode preset
│   └── eval.yaml                  # Evaluation mode preset
│
├── commands/                      # Slash commands (entry points only)
│   ├── build-fix.md               # → delegates to build-error-resolver agent
│   ├── checkpoint.md
│   ├── code-review.md             # → delegates to code-reviewer agent
│   ├── plan.md                    # → delegates to planner agent
│   ├── tdd.md                     # → delegates to tdd-guide agent
│   └── ...
│
├── rules/                         # Behavioral constraints (auto-loaded, minimal)
│   ├── common/
│   │   ├── coding-style.md        # Core immutability, naming, file org
│   │   ├── security.md            # Mandatory security checks
│   │   ├── git-workflow.md        # Commit format, PR workflow
│   │   └── testing.md             # Coverage floors, TDD mandate
│   └── python/
│       ├── coding-style.md        # PEP 8, type hints, formatting
│       └── testing.md             # pytest specifics
│
├── skills/                        # Multi-step protocols (on-demand)
│   ├── context-engineering/
│   │   ├── SKILL.md               # Master reference (SELF-CONTAINED)
│   │   └── references/            # Sub-files (CREATE THESE)
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── references/            # Sub-files (CREATE THESE)
│   └── ...
│
└── adr/                           # NEW — ADR index as context deck
    └── ADR-INDEX.md               # Auto-generated from docs/adr/
```

### Preset Configuration Format

Each preset defines which rules, contexts, and agents activate for a given workflow mode:

```yaml
# .claude/presets/dev.yaml
name: development
description: Active development — code first, test after
rules:
  - common/coding-style
  - common/security
  - common/testing
  - python/coding-style
  - python/testing
agents:
  primary: [tdd-guide, code-reviewer, build-error-resolver]
  on_demand: [planner, architect, security-reviewer]
behaviors:
  - Write code first, explain after
  - Run tests after changes
  - Keep commits atomic
priorities: [working, correct, clean]
```

```yaml
# .claude/presets/research.yaml
name: research
description: Exploration and investigation
rules:
  - common/security
  - common/ml-practices
agents:
  primary: [planner, architect]
  on_demand: [code-reviewer]
behaviors:
  - Read widely before concluding
  - Document findings as you go
  - Don't write code until understanding is clear
adrs:
  relevant: [007, 009, 003]
```

```yaml
# .claude/presets/review.yaml
name: code-review
description: PR review and quality analysis
rules:
  - common/coding-style
  - common/security
  - common/testing
agents:
  primary: [code-reviewer, security-reviewer]
  on_demand: [build-error-resolver]
behaviors:
  - Read thoroughly before commenting
  - Prioritize by severity
  - Suggest fixes, don't just point out problems
```

---

## Part 4: Remediation Priority

### Phase 1 — Critical Fixes (Immediate)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 1 | Delete duplicated worktree `.claude/` contents; use symlinks or inheritance | Low | Eliminates ~650 redundant files |
| 2 | Create missing skill reference files OR consolidate into SKILL.md | Medium | Fixes 14 broken references |
| 3 | Remove broken skill references from Python rules | Low | Eliminates confusion |
| 4 | Clean `settings.local.json` to ~20 pattern-based permissions | Low | Reduces audit surface |

### Phase 2 — Structural Improvements (Sprint)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 5 | Create `presets/` directory with mode-specific configs | Medium | Unified configuration access |
| 6 | Regenerate `ADR_COMPILED.md` or replace with `ADR-INDEX.md` | Low | Eliminates staleness |
| 7 | Establish instruction hierarchy (rules > commands > skills > agents) | Medium | Eliminates redundancy |
| 8 | Fix command examples to use Python/pytest instead of TypeScript | Low | Prevents tech-stack confusion |

### Phase 3 — Consolidation (Quarter)

| # | Action | Effort | Impact |
|---|--------|--------|--------|
| 9 | Resolve `.github/agents/` vs `.claude/` agent duplication | Medium | Single source of truth |
| 10 | Unify ADR numbering (drop 4-digit scheme, document gaps) | Low | Clear lineage |
| 11 | Merge thin contexts into presets | Low | Reduces token cost |
| 12 | Add automated ADR index generation to CI | Medium | Prevents future staleness |

---

## Part 5: Token Budget Analysis

### Current Context Load (Estimated)

| Source | Tokens (est.) | Auto-Loaded? |
|--------|---:|:---:|
| CLAUDE.md (root) | ~3,500 | ✅ |
| CLAUDE.md (worktree duplicate) | ~3,500 | ✅ |
| Rules (common/ × 7) | ~5,600 | ✅ |
| Rules (python/ × 5) | ~1,200 | ✅ |
| MEMORY.md | ~2,800 | ✅ |
| **Total auto-loaded** | **~16,600** | |

With worktree dedup fix, this drops to ~13,100 tokens (saving ~3,500).

### Per-Invocation Additions

| Source | Tokens (est.) | Loaded When |
|--------|---:|---|
| Context: dev/research/review | ~200-400 | @context-name |
| Command: plan/tdd/code-review | ~1,000-3,000 | /command |
| Skill: code-review/context-eng | ~1,500-2,000 | /skill |
| ADR (single) | ~3,000-8,000 | Manual read |
| ADR_COMPILED.md | ~15,000+ | Manual read |

---

## Appendix: Complete File Inventory

### ADR Files (docs/adr/)

| File | Size | Modified |
|------|------|----------|
| ADR-001-002-003-architecture-decisions.md | ~12KB | 2026-02-28 |
| ADR-007-classification-matrix-stop-policy.md | ~8KB | 2026-02-28 |
| ADR-008-testing-approach-overhaul.md | ~20KB | 2026-03-09 |
| ADR-009-scoring-enhancements.md | ~6KB | 2026-03-03 |
| ADR-010-eval-harness-methodology.md | ~8KB | 2026-03-09 |
| ADR-011-eval-harness-api-interface.md | ~8KB | 2026-03-09 |
| ADR-012-ui-evaluation-hub.md | ~8KB | 2026-03-09 |
| ADR_COMPILED.md | ~41KB | 2026-03-01 ⚠️ STALE |
| ADR_IMPLEMENTATION_AUDIT.md | ~8KB | 2026-02-28 |
| ADR_RESEARCH_JUSTIFICATIONS.md | ~64KB | 2026-02-28 |
| RAG-pipeline-blueprint.md | ~5KB | 2026-02-28 |

### Commands (11)

build-fix, checkpoint, code-review, eval, orchestrate, plan, python-review, refactor-clean, tdd, test-coverage, update-docs

### Rules (12)

common/: agents, coding-style, git-workflow, ml-practices, patterns, security, testing
python/: coding-style, hooks, patterns, security, testing

### Skills (9)

changelog-generator, code-review, context-engineering, debugging, langsmith-fetch, mcp-builder, problem-solving, sequential-thinking, webapp-testing

### Contexts (3)

dev, research, review

---

## Remediation Log

| Date | Issue | Action Taken | Status |
|------|-------|-------------|--------|
| 2026-03-15 | C-1: Worktree duplication | Deleted 3 worktrees + branches via `git worktree remove` + `git branch -D`. Git references pruned. 2 orphaned directories locked by other processes — require manual cleanup after closing sessions. | Done (git clean, dirs pending) |
| 2026-03-15 | C-2: Broken skill references | Removed 9 missing `references/` links + 2 missing `scripts/` links from context-engineering SKILL.md. Removed 3 missing `references/` links from code-review SKILL.md. | Done |
| 2026-03-15 | C-3: Stale ADR registry | Created `docs/adr/ADR-INDEX.md` with all 9 ADRs, lineage chains, implementation status. Added deprecation header to `ADR_COMPILED.md`. | Done |
| 2026-03-15 | C-4: Overlapping instructions | Added Loading Hierarchy to `.claude/README.md`. Slimmed `/code-review` command to delegation-only. | Done |
| 2026-03-15 | H-3: Bloated settings.local.json | Reduced from 87 to 31 pattern-based permissions. Removed PID-specific, path-specific, and stale MCP entries. | Done |
| 2026-03-15 | H-4: Python rules broken refs | Removed `skill: python-patterns`, `skill: python-testing`, `skill: django-security` references. Fixed `hooks.md` extends reference. | Done |
| 2026-03-15 | M-5: Command tech-stack mismatch | Replaced TypeScript/Node.js examples in `/plan` and `/tdd` with Python/pytest examples matching this project. | Done |
| 2026-03-15 | Cherry-picks | Cherry-picked `1711be25` (CI integration job) and `07ecb4fb` (7 arch debt backlog items) from backlog-phase-3. Skipped `6ac26971` (already on main via PR #99). | Done |

### Remaining Items (Phase 3 — deferred)

| Issue | Status | Notes |
|-------|--------|-------|
| H-1: `.github/agents/` parallel system | Deferred | Requires decision on GitHub Copilot vs Claude Code agent strategy |
| H-2: Worktree CLAUDE.md duplicate | Resolved | Worktrees deleted — no longer applies |
| H-5: ADR numbering inconsistency | Deferred | Low impact — documented gap (004-006) in ADR-INDEX.md |
| M-1: Research library orphaned content | Deferred | Needs research library audit |
| M-2: Thin contexts | Deferred | Consider merging into presets in future |
| M-3: MEMORY.md stale port note | Deferred | Auto-memory — will self-correct |
| M-4: ADR supersession chain | Resolved | Documented in ADR-INDEX.md lineage chains |
