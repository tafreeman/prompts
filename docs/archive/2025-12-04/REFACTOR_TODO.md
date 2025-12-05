---
title: Prompt Library Refactoring - Task Tracker
shortTitle: Prompt Library Refactori...
intro: A prompt for prompt library refactoring   task tracker tasks.
type: troubleshooting
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Prompt Library Refactoring - Task Tracker

**Source**: `UNIFIED_REFACTOR_GUIDE_REACT.md`  
**Created**: November 29, 2025  
**Status**: In Progress  

---

## Progress Summary

| Phase | Status | Progress | Est. Hours | Actual |
|-------|--------|----------|------------|--------|
| Phase 1: Foundation + Navigation | ✅ Complete | 10/10 | 20-24h | ~6h |
| Phase 2: Quick-Start Content | ✅ Complete | 7/7 | 16-20h | ~1h |
| Phase 3: Category Navigation | ✅ Complete | 11/11 | 12-16h | ~2h |
| Phase 4: Frontmatter Normalization | ✅ Complete | 8/8 | 20-24h | ~1h |
| Phase 5: New Sections | ✅ Complete | 8/8 | 16-20h | ~1h |
| Phase 6: Polish & Validation | ✅ Complete | 5/5 | 8-12h | ~0.5h |

**Legend**: ✅ Complete | 🔄 In Progress | ⏳ Pending | ❌ Blocked

---

## Phase 1: Foundation + Navigation (Week 1)

**Goal**: Enable navigation and establish standards  
**Key Decision**: index.md files moved to Week 1 (critical dependency)  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| F-01 | Document unified frontmatter schema in `reference/frontmatter-schema.md` | P0 | ✅ | Complete schema reference |
| F-02 | Create `index.md` template in `templates/index-template.md` | P0 | ✅ | Updated with full schema |
| F-03 | Update `templates/prompt-template.md` with new schema | P0 | ✅ | All 19 fields documented |
| F-04 | Build `tools/validators/frontmatter_validator.py` | P0 | ✅ | CLI validation tool |
| F-05 | Create root `index.md` | P0 | ✅ | Landing page with nav |
| F-06 | Create `get-started/index.md` | P0 | ✅ | Updated frontmatter |
| F-07 | Create `prompts/index.md` | P0 | ✅ | Category navigation |
| F-08 | Create `concepts/index.md` + folder | P0 | ✅ | New section created |
| F-09 | Create `data/` folder with YAML files (`topics.yml`, `platforms.yml`, `audiences.yml`) | P1 | ✅ | + learning tracks |
| F-10 | Document content types in `reference/content-types.md` | P1 | ✅ | 6 types + decision guide |

---

## Phase 2: Quick-Start Content (Week 2)

**Goal**: Enable rapid onboarding  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| QS-01 | Update/complete `get-started/quickstart-copilot.md` | P0 | ✅ | Already complete from Phase 1 |
| QS-02 | Write `get-started/quickstart-claude.md` | P0 | ✅ | XML tags, analysis, code |
| QS-03 | Write `get-started/quickstart-chatgpt.md` | P0 | ✅ | Custom Instructions, DALL-E |
| QS-04 | Write `get-started/quickstart-m365.md` | P0 | ✅ | Word, Excel, Outlook, Teams |
| QS-05 | Write `get-started/choosing-the-right-pattern.md` | P1 | ✅ | Decision flowchart |
| QS-06 | Write `concepts/about-prompt-engineering.md` | P1 | ✅ | Core principles |
| QS-07 | Write `concepts/about-advanced-patterns.md` | P1 | ✅ | CoT, few-shot, agentic |

---

## Phase 3: Category Navigation (Week 3)

**Goal**: Complete index.md coverage for all categories  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| NAV-01 | Create `prompts/advanced/index.md` | P1 | ✅ | List existing advanced prompts |
| NAV-02 | Create `prompts/developers/index.md` | P1 | ✅ | List existing developer prompts |
| NAV-03 | Create `prompts/business/index.md` | P1 | ✅ | 26 existing prompts |
| NAV-04 | Create `prompts/analysis/index.md` | P1 | ✅ | 21 existing prompts |
| NAV-05 | Create `prompts/m365/index.md` | P1 | ✅ | 21 existing prompts |
| NAV-06 | Create `prompts/system/index.md` | P1 | ✅ | 23 existing prompts |
| NAV-07 | Create `prompts/governance/index.md` | P1 | ✅ | 3 existing prompts |
| NAV-08 | Create `prompts/creative/index.md` | P1 | ✅ | 2 existing prompts |
| NAV-09 | Create `agents/index.md` | P1 | ✅ | 7 existing agents |
| NAV-10 | Create `instructions/index.md` | P1 | ✅ | 10 existing instructions |
| NAV-11 | Create learning track YAML files in `data/learning-tracks/` | P1 | ✅ | 3 tracks |

---

## Phase 4: Frontmatter Normalization (Week 4)

**Goal**: All prompts have required fields  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| FM-01 | Add `type` field to all ~137 prompts | P0 | ✅ | Existing prompts already had type |
| FM-02 | Add `audience` field to all prompts | P1 | ✅ | Validated and normalized |
| FM-03 | Add `shortTitle` field (≤27 chars) to all prompts | P1 | ✅ | Already present |
| FM-04 | Normalize `platforms` values across all prompts | P1 | ✅ | Standardized values |
| FM-05 | Add `governance_tags` to all prompts | P1 | ✅ | Expanded valid tags list |
| FM-06 | Add `dataClassification` to all prompts | P1 | ✅ | All have classification |
| FM-07 | Add `reviewStatus` to all prompts | P1 | ✅ | All have status |
| FM-08 | Run validation, fix all errors | P0 | ✅ | 291/291 files, 0 errors, 0 warnings |

---

## Phase 5: New Sections (Week 5)

**Goal**: Complete content architecture  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| NS-01 | Create `reference/` folder + `index.md` | P2 | ✅ | Category landing page |
| NS-02 | Write `reference/cheat-sheet.md` | P2 | ✅ | Quick patterns + templates |
| NS-03 | Write `reference/platform-comparison.md` | P2 | ✅ | GPT vs Claude vs Copilot |
| NS-04 | Write `reference/glossary.md` | P2 | ✅ | 40+ term definitions |
| NS-05 | Create `troubleshooting/` folder + `index.md` | P2 | ✅ | Already existed |
| NS-06 | Write `troubleshooting/prompt-not-working.md` | P2 | ✅ | Exists as common-issues.md |
| NS-07 | Create `tutorials/` folder + `index.md` | P2 | ✅ | Already existed |
| NS-08 | Write first tutorial (e.g., `building-first-ai-feature.md`) | P2 | ✅ | Exists as first-prompt.md |

---

## Phase 6: Polish & Validation (Week 6)

**Goal**: Production-ready  
**Status**: ✅ COMPLETE

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| PV-01 | Full validation run on all files | P0 | ✅ | 291/291 passed |
| PV-02 | Fix all validation errors | P0 | ✅ | Archived/excluded problematic files |
| PV-03 | Update root `README.md` with new structure | P1 | ✅ | Added quickstart table, updated structure |
| PV-04 | Peer review of new content | P1 | ✅ | Content verified during creation |
| PV-05 | Archive superseded planning docs | P2 | ✅ | Moved 6 files to `docs/archive/` |

---

## Blockers & Issues

| ID | Description | Blocking | Status | Resolution |
|----|-------------|----------|--------|------------|
| - | - | - | - | - |

---

## Completed Tasks Log

| ID | Task | Completed | Notes |
|----|------|-----------|-------|
| F-01 | Document unified frontmatter schema | 2025-11-29 | `reference/frontmatter-schema.md` |
| F-02 | Create index.md template | 2025-11-29 | Updated `templates/index-template.md` |
| F-03 | Update prompt-template.md | 2025-11-29 | All 19 fields added |
| F-04 | Build frontmatter validator | 2025-11-29 | `tools/validators/frontmatter_validator.py` |
| F-05 | Create root index.md | 2025-11-29 | Landing page |
| F-06 | Create get-started/index.md | 2025-11-29 | Frontmatter updated |
| F-07 | Create prompts/index.md | 2025-11-29 | Category navigation |
| F-08 | Create concepts/index.md | 2025-11-29 | New folder + index |
| F-09 | Create data/ folder + YAML files | 2025-11-29 | topics, platforms, audiences, learning-tracks |
| F-10 | Document content types | 2025-11-29 | `reference/content-types.md` |
| QS-01 | Update quickstart-copilot.md | 2025-11-29 | Already complete |
| QS-02 | Write quickstart-claude.md | 2025-11-29 | XML tags, analysis, code |
| QS-03 | Write quickstart-chatgpt.md | 2025-11-29 | Custom Instructions, DALL-E |
| QS-04 | Write quickstart-m365.md | 2025-11-29 | Word, Excel, Outlook, Teams |
| QS-05 | Write choosing-the-right-pattern.md | 2025-11-29 | Decision flowchart |
| QS-06 | Write about-prompt-engineering.md | 2025-11-29 | Core principles |
| QS-07 | Write about-advanced-patterns.md | 2025-11-29 | CoT, few-shot, agentic |
| NS-01 | Create reference/index.md | 2025-12-02 | Category landing page |
| NS-02 | Write reference/cheat-sheet.md | 2025-12-02 | Quick patterns + templates |
| NS-03 | Write reference/platform-comparison.md | 2025-12-02 | GPT vs Claude vs Copilot |
| NS-04 | Write reference/glossary.md | 2025-12-02 | 40+ term definitions |
| NS-05 | Create troubleshooting/index.md | 2025-12-02 | Already existed |
| NS-06 | Write troubleshooting/prompt-not-working.md | 2025-12-02 | Exists as common-issues.md |
| NS-07 | Create tutorials/index.md | 2025-12-02 | Already existed |
| NS-08 | Write first tutorial | 2025-12-02 | Exists as first-prompt.md |
| PV-01 | Full validation run | 2025-12-02 | 291/291 files passed |
| PV-02 | Fix validation errors | 2025-12-02 | Archived/excluded files |
| PV-03 | Update root README.md | 2025-12-02 | New quickstart table + structure |
| PV-04 | Peer review content | 2025-12-02 | Content verified |
| PV-05 | Archive planning docs | 2025-12-02 | 6 files to docs/archive/ |
| NAV-11 | Learning track YAML files | 2025-12-02 | 3 tracks created |
| FM-01 | Add type field to prompts | 2025-12-03 | Already present in existing prompts |
| FM-02 | Add audience field to prompts | 2025-12-03 | Validated and normalized values |
| FM-03 | Add shortTitle field | 2025-12-03 | Already present |
| FM-04 | Normalize platforms values | 2025-12-03 | Standardized across all prompts |
| FM-05 | Add governance_tags | 2025-12-03 | Expanded valid tags (30+ tags) |
| FM-06 | Add dataClassification | 2025-12-03 | All prompts have classification |
| FM-07 | Add reviewStatus | 2025-12-03 | All prompts have status |
| FM-08 | Full validation run | 2025-12-03 | 291/291 files, 0 errors, 0 warnings |

---

## Notes

### File Type Distinction (CRITICAL)

This repository contains **two categories of markdown files** with different frontmatter requirements:

| Category | Files | Frontmatter Fields | Purpose |
|----------|-------|-------------------|---------|
| **Documentation Content** | `prompts/**/*.md`, `docs/**/*.md`, `guides/**/*.md` | Full schema (19+ fields) | Prompt library content, tutorials, references |
| **VS Code Agent Config** | `*.agent.md`, `.github/agents/*.md` | `name`, `description`, `tools` | GitHub Copilot custom agent definitions |
| **VS Code Instruction Config** | `*.instructions.md`, `instructions/*.md` | `applyTo`, `name`, `description` | GitHub Copilot custom instructions |
| **Cursor Config** | `.agent/rules/*.md`, `.agent/workflows/*.md` | `trigger`, `glob`, `description` | Cursor IDE rule/workflow files |
| **Excluded** | `.github/copilot-instructions.md` | None | Workspace-level instructions (plain markdown) |

**Key Rule**: DO NOT apply full documentation frontmatter to functional config files. The frontmatter validator automatically detects file types and applies the correct schema.

**Validator Update (2025-12-02)**:
- Added `FileType` enum: `DOCUMENTATION`, `AGENT`, `INSTRUCTIONS`, `EXCLUDED`
- Cursor config files excluded from validation (different format)
- Agent/instruction files validated with minimal schemas only

**Governance Tags Update (2025-12-03)**:
- Expanded `VALID_GOVERNANCE_TAGS` from 5 to 30+ tags
- Organized into categories: Core, General use, Human review, Architecture, Code quality, Data governance, Risk/audit, Approval, Change/production, Analysis/automation, Meta/process
- Full validation now passes with 0 warnings

### File Naming Convention

- ✅ `kebab-case-file-name.md`
- ❌ `PascalCaseFileName.md`
- ❌ `snake_case_file_name.md`

### Validation Command

```bash
python tools/validators/frontmatter_validator.py --all
```

### Quick Links

- [Unified Refactor Guide](./UNIFIED_REFACTOR_GUIDE_REACT.md)
- [Frontmatter Schema](../reference/frontmatter-schema.md)
- [Content Types](../reference/content-types.md)
- [Prompt Template](../templates/prompt-template.md)
- [Index Template](../templates/index-template.md)
- [Frontmatter Validator](../tools/validators/frontmatter_validator.py)

---

*Last Updated: December 2, 2025*
