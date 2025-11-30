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
| Phase 3: Category Navigation | 🔄 Ready | 0/11 | 12-16h | - |
| Phase 4: Frontmatter Normalization | ⏳ Pending | 0/8 | 20-24h | - |
| Phase 5: New Sections | ⏳ Pending | 0/8 | 16-20h | - |
| Phase 6: Polish & Validation | ⏳ Pending | 0/5 | 8-12h | - |

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

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| NAV-01 | Create `prompts/advanced/index.md` | P1 | ⏳ | List existing advanced prompts |
| NAV-02 | Create `prompts/developers/index.md` | P1 | ⏳ | List existing developer prompts |
| NAV-03 | Create `prompts/business/index.md` | P1 | ⏳ | 26 existing prompts |
| NAV-04 | Create `prompts/analysis/index.md` | P1 | ⏳ | 21 existing prompts |
| NAV-05 | Create `prompts/m365/index.md` | P1 | ⏳ | 21 existing prompts |
| NAV-06 | Create `prompts/system/index.md` | P1 | ⏳ | 23 existing prompts |
| NAV-07 | Create `prompts/governance/index.md` | P1 | ⏳ | 3 existing prompts |
| NAV-08 | Create `prompts/creative/index.md` | P1 | ⏳ | 2 existing prompts |
| NAV-09 | Create `agents/index.md` | P1 | ⏳ | 7 existing agents |
| NAV-10 | Create `instructions/index.md` | P1 | ⏳ | 10 existing instructions |
| NAV-11 | Create learning track YAML files in `data/learning-tracks/` | P1 | ⏳ | 3 tracks |

---

## Phase 4: Frontmatter Normalization (Week 4)

**Goal**: All prompts have required fields

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| FM-01 | Add `type` field to all ~137 prompts | P0 | ⏳ | Bulk update |
| FM-02 | Add `audience` field to all prompts | P1 | ⏳ | Bulk update |
| FM-03 | Add `shortTitle` field (≤27 chars) to all prompts | P1 | ⏳ | Bulk update |
| FM-04 | Normalize `platforms` values across all prompts | P1 | ⏳ | Standardize values |
| FM-05 | Add `governance_tags` to all prompts | P1 | ⏳ | Default: `["PII-safe"]` |
| FM-06 | Add `dataClassification` to all prompts | P1 | ⏳ | Default: `internal` |
| FM-07 | Add `reviewStatus` to all prompts | P1 | ⏳ | Default: `draft` |
| FM-08 | Run validation, fix all errors | P0 | ⏳ | Depends on FM-01..07 |

---

## Phase 5: New Sections (Week 5)

**Goal**: Complete content architecture

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| NS-01 | Create `reference/` folder + `index.md` | P2 | ⏳ | New section |
| NS-02 | Write `reference/cheat-sheet.md` | P2 | ⏳ | Quick patterns |
| NS-03 | Write `reference/platform-comparison.md` | P2 | ⏳ | GPT vs Claude vs Copilot |
| NS-04 | Write `reference/glossary.md` | P2 | ⏳ | Terms |
| NS-05 | Create `troubleshooting/` folder + `index.md` | P2 | ⏳ | New section |
| NS-06 | Write `troubleshooting/prompt-not-working.md` | P2 | ⏳ | Common issues |
| NS-07 | Create `tutorials/` folder + `index.md` | P2 | ⏳ | New section |
| NS-08 | Write first tutorial (e.g., `building-first-ai-feature.md`) | P2 | ⏳ | End-to-end |

---

## Phase 6: Polish & Validation (Week 6)

**Goal**: Production-ready

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| PV-01 | Full validation run on all files | P0 | ⏳ | |
| PV-02 | Fix all validation errors | P0 | ⏳ | Depends on PV-01 |
| PV-03 | Update root `README.md` with new structure | P1 | ⏳ | |
| PV-04 | Peer review of new content | P1 | ⏳ | |
| PV-05 | Archive superseded planning docs | P2 | ⏳ | Move to `docs/archive/` |

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

---

## Notes

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

*Last Updated: November 29, 2025*
