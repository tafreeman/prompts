# Unified Prompt Library Refactoring Guide (ReAct Synthesis)

**Version**: 1.0  
**Date**: November 29, 2025  
**Synthesis Method**: ReAct (Reasoning + Acting) Pattern  
**Source Documents**:
- `KNOWLEDGE_BASE_ARCHITECTURE_RESEARCH.md` (5 industry sources)
- `LIBRARY_REFACTOR_PLAN.md` (Current state + migration plan)

---

## Executive Summary

This guide is the **single source of truth** for refactoring the `tafreeman/prompts` repository. It was created by systematically comparing and merging two planning documents using the ReAct pattern.

### Synthesis Decisions

| Topic | Research Doc | Refactor Plan | **Decision** | Rationale |
|-------|--------------|---------------|--------------|-----------|
| `shortTitle` length | ≤30 chars | ≤27 chars | **≤27 chars** | GitHub Docs standard |
| Folder nesting | Flat | Nested `prompts/prompts/` | **Flat** | Simpler, clearer |
| index.md timing | Week 1 | Week 3 | **Week 1** | Critical dependency |
| Governance fields | Optional | Required | **Required** | Enterprise compliance |
| Field naming | `topics` | `category` | **`topics`** | GitHub Docs pattern |
| Learning tracks | YAML only | YAML + frontmatter | **Both** | Flexibility |

---

## Part 1: Unified Frontmatter Schema

### Complete Schema

```yaml
---
# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED FIELDS (all content)
# Source: Both documents agree
# ═══════════════════════════════════════════════════════════════════════════════
title: "Human-readable title"                    # ≤60 chars
shortTitle: "Nav Label"                          # ≤27 chars (GitHub Docs standard)
intro: "One-sentence summary."                   # For search results, cards
type: "how_to"                                   # See Content Types table
difficulty: "intermediate"                       # beginner|intermediate|advanced

# ═══════════════════════════════════════════════════════════════════════════════
# REQUIRED FIELDS (prompts only)
# Source: Both documents agree
# ═══════════════════════════════════════════════════════════════════════════════
audience:                                        # Target personas
  - "junior-engineer"
  - "senior-engineer"
  - "solution-architect"
  - "qa-engineer"
  - "business-analyst"
  - "project-manager"
  - "functional-team"

platforms:                                       # Supported platforms
  - "github-copilot"
  - "claude"
  - "chatgpt"
  - "azure-openai"
  - "m365-copilot"

# ═══════════════════════════════════════════════════════════════════════════════
# RECOMMENDED FIELDS
# Source: Merged from both documents
# ═══════════════════════════════════════════════════════════════════════════════
topics:                                          # For filtering (replaces 'category')
  - "code-generation"
  - "debugging"
  - "refactoring"
  - "testing"
  - "documentation"
  - "analysis"

technique: "chain-of-thought"                    # For advanced prompts only
                                                 # Options: chain-of-thought | react |
                                                 # tree-of-thought | few-shot | zero-shot |
                                                 # reflection | rag

estimatedTime: "15 min"                          # Time to complete

prerequisites:                                   # From Refactor Plan (new)
  - "/get-started/quickstart-copilot"

learningTrack: "engineer-quickstart"             # Reference to learning track
                                                 # Options: engineer-quickstart |
                                                 # architect-depth | functional-productivity

# ═══════════════════════════════════════════════════════════════════════════════
# METADATA FIELDS
# Source: Both documents agree
# ═══════════════════════════════════════════════════════════════════════════════
author: "Author Name"
version: "1.0"
date: "2025-11-29"                               # YYYY-MM-DD format

# ═══════════════════════════════════════════════════════════════════════════════
# GOVERNANCE FIELDS (enterprise requirement)
# Source: Refactor Plan (extended from Research doc)
# ═══════════════════════════════════════════════════════════════════════════════
governance_tags:                                 # Classification labels
  - "PII-safe"
  - "client-approved"
  - "internal-only"
  - "requires-human-review"
  - "audit-required"

dataClassification: "internal"                   # public | internal | confidential
reviewStatus: "approved"                         # draft | reviewed | approved

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION FIELDS (index.md only)
# Source: Both documents agree (GitHub Docs pattern)
# ═══════════════════════════════════════════════════════════════════════════════
layout: "category-landing"

children:                                        # Ordered list of child pages
  - /child-page-1
  - /child-page-2

featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
  popular:
    - /prompts/advanced/chain-of-thought-debugging
---
```

### Field Quick Reference

| Field | Required | Constraint | Source |
|-------|----------|------------|--------|
| `title` | ✅ | ≤60 chars | Both |
| `shortTitle` | ✅ | ≤27 chars | GitHub Docs |
| `intro` | ✅ | 1-2 sentences | Both |
| `type` | ✅ | 6 values | Both |
| `difficulty` | ✅ | 3 values | Both |
| `audience` | ✅ | Valid personas | Both |
| `platforms` | ✅ | Valid platforms | Both |
| `topics` | ⚪ | From topics.yml | Research (replaces category) |
| `technique` | ⚪ | 7 values | Research |
| `estimatedTime` | ⚪ | "X min" format | Both |
| `prerequisites` | ⚪ | Valid paths | Refactor Plan |
| `learningTrack` | ⚪ | 3 values | Both |
| `author` | ✅ | Name | Both |
| `version` | ✅ | Semver | Both |
| `date` | ✅ | YYYY-MM-DD | Both |
| `governance_tags` | ✅ | Valid tags | Refactor Plan |
| `dataClassification` | ✅ | 3 values | Refactor Plan |
| `reviewStatus` | ✅ | 3 values | Refactor Plan |
| `children` | 📁 | index.md only | Both |
| `featuredLinks` | 📁 | index.md only | Both |

**Legend**: ✅ Required | ⚪ Recommended | 📁 index.md only

---

## Part 2: Definitive Folder Structure

### Merged Architecture

**Decision**: Use Research doc's flat structure + preserve existing repo folders from Refactor Plan.

```
prompts/                                    # Repository root
│
├── index.md                                # 🏠 Landing page
├── README.md                               # GitHub readme
│
├── get-started/                            # 🚀 QUICKSTARTS
│   ├── index.md                            #    Source: Both agree
│   ├── quickstart-copilot.md               #    ✅ Exists
│   ├── quickstart-claude.md                #    ❌ Create
│   ├── quickstart-chatgpt.md               #    ❌ Create
│   ├── quickstart-m365.md                  #    ❌ Create
│   └── choosing-the-right-pattern.md       #    Decision guide
│
├── concepts/                               # 📚 CONCEPTUAL
│   ├── index.md                            #    Source: Both agree
│   ├── about-prompt-engineering.md
│   ├── about-advanced-patterns.md
│   ├── model-capabilities.md
│   └── prompt-anatomy.md
│
├── prompts/                                # 🔧 PROMPT LIBRARY
│   ├── index.md                            #    Browse all prompts
│   │
│   ├── developers/                         #    Developer prompts
│   │   ├── index.md
│   │   ├── code-generation/                #    Nested per Research doc
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   ├── debugging/
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   ├── code-review/
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   └── refactoring/
│   │       ├── index.md
│   │       └── *.md
│   │
│   ├── advanced/                           #    Advanced techniques
│   │   ├── index.md
│   │   ├── chain-of-thought/               #    Nested per Research doc
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   ├── react/
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   ├── tree-of-thought/
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   ├── reflection/
│   │   │   ├── index.md
│   │   │   └── *.md
│   │   └── rag/
│   │       ├── index.md
│   │       └── *.md
│   │
│   ├── business/                           #    Business prompts
│   │   ├── index.md
│   │   └── [26 existing prompts]
│   │
│   ├── analysis/                           #    Analysis prompts
│   │   ├── index.md
│   │   └── [21 existing prompts]
│   │
│   ├── m365/                               #    M365 prompts
│   │   ├── index.md
│   │   └── [21 existing prompts]
│   │
│   ├── system/                             #    System prompts
│   │   ├── index.md
│   │   └── [23 existing prompts]
│   │
│   ├── governance/                         #    Governance prompts
│   │   ├── index.md
│   │   └── [3 existing prompts]
│   │
│   └── creative/                           #    Creative prompts
│       ├── index.md
│       └── [2 existing prompts]
│
├── tutorials/                              # 📖 END-TO-END LEARNING
│   ├── index.md                            #    Source: Refactor Plan
│   ├── building-first-ai-feature.md
│   ├── implementing-rag-pipeline.md
│   └── enterprise-prompt-governance.md
│
├── reference/                              # 📋 QUICK LOOKUP
│   ├── index.md                            #    Source: Both agree
│   ├── cheat-sheet.md
│   ├── frontmatter-schema.md
│   ├── content-types.md
│   ├── platform-comparison.md
│   ├── governance-tags.md
│   └── glossary.md
│
├── troubleshooting/                        # 🔍 PROBLEM/SOLUTION
│   ├── index.md                            #    Source: Both agree
│   ├── prompt-not-working.md
│   ├── output-quality-issues.md
│   └── context-limit-errors.md
│
├── agents/                                 # 🤖 AGENTS (existing)
│   ├── index.md                            #    Source: Refactor Plan
│   └── [7 existing agents]
│
├── instructions/                           # 📝 COPILOT INSTRUCTIONS (existing)
│   ├── index.md                            #    Source: Refactor Plan
│   └── [10 existing instructions]
│
├── templates/                              # 📄 TEMPLATES (existing)
│   ├── index.md
│   ├── prompt-template.md
│   ├── index-template.md
│   └── quickstart-template.md
│
├── techniques/                             # 🧠 TECHNIQUES (existing)
│   ├── index.md                            #    Source: Refactor Plan
│   └── [existing content]
│
├── frameworks/                             # 🏗️ FRAMEWORKS (existing)
│   ├── index.md                            #    Source: Refactor Plan
│   └── [existing content]
│
├── data/                                   # 📊 DATA FILES
│   ├── learning-tracks/                    #    Source: Both agree
│   │   ├── engineer-quickstart.yml
│   │   ├── architect-depth.yml
│   │   └── functional-productivity.yml
│   ├── topics.yml
│   ├── platforms.yml
│   └── audiences.yml
│
├── tools/                                  # 🔧 TOOLING (existing)
│   └── [existing tools]
│
└── docs/                                   # 📚 META-DOCS (existing)
    ├── UNIFIED_REFACTOR_GUIDE_REACT.md     #    ← This document
    └── [other docs]
```

### Folder Count Summary

| Category | Count | Status |
|----------|-------|--------|
| New top-level folders | 5 | concepts, tutorials, reference, troubleshooting, data |
| Existing folders preserved | 8 | agents, instructions, templates, techniques, frameworks, tools, docs, get-started |
| index.md files needed | 25+ | See implementation plan |

---

## Part 3: Content Types (Unified)

**Source**: Both documents define identical content types.

| Type | Purpose | Title Pattern | Example |
|------|---------|---------------|---------|
| **conceptual** | Explain what/why/when | "About [Subject]" | "About Chain-of-Thought" |
| **quickstart** | 15-min first success | "Quickstart for [Platform]" | "Quickstart for Copilot" |
| **how_to** | Complete a specific task | Gerund/imperative | "Generating Unit Tests" |
| **tutorial** | End-to-end guided learning | Task-based | "Building a RAG Pipeline" |
| **reference** | Quick information lookup | Noun-based | "Frontmatter Schema" |
| **troubleshooting** | Solve problems | "Troubleshooting [Topic]" | "Troubleshooting Output Quality" |

### Decision Flowchart

```
Is this explaining what something is?
├── Yes → conceptual
└── No ↓

Is this a first-time setup (≤15 min)?
├── Yes → quickstart
└── No ↓

Is this a single, focused task?
├── Yes → how_to
└── No ↓

Is this a multi-step learning experience?
├── Yes → tutorial
└── No ↓

Is this for quick lookup?
├── Yes → reference
└── No ↓

Is this about fixing a problem?
├── Yes → troubleshooting
└── No → Re-evaluate scope
```

---

## Part 4: Implementation Roadmap (Merged)

### Timeline Overview

| Phase | Week | Focus | Source |
|-------|------|-------|--------|
| 1 | Week 1 | Foundation + Navigation | Merged (Research prioritizes index.md) |
| 2 | Week 2 | Quick-Start Content | Both agree |
| 3 | Week 3 | Category Navigation | Both agree |
| 4 | Week 4 | Frontmatter Normalization | Both agree |
| 5 | Week 5 | New Sections | Both agree |
| 6 | Week 6 | Polish & Validation | Refactor Plan |

---

### Phase 1: Foundation + Navigation (Week 1)

**Goal**: Enable navigation and establish standards  
**Effort**: 20-24 hours  
**Key Decision**: index.md files moved to Week 1 (was Week 3 in Refactor Plan)

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| F-01 | Document unified frontmatter schema | P0 | 2h | None |
| F-02 | Create `index.md` template | P0 | 1h | F-01 |
| F-03 | Update `prompt-template.md` | P0 | 2h | F-01 |
| F-04 | Build frontmatter validation script | P0 | 4h | F-01 |
| F-05 | Create root `index.md` | P0 | 3h | F-02 |
| F-06 | Create `get-started/index.md` | P0 | 1h | F-02 |
| F-07 | Create `prompts/index.md` | P0 | 1h | F-02 |
| F-08 | Create `concepts/index.md` | P0 | 1h | F-02 |
| F-09 | Create `data/` folder with YAML files | P1 | 2h | None |
| F-10 | Document content types | P1 | 2h | None |

---

### Phase 2: Quick-Start Content (Week 2)

**Goal**: Enable rapid onboarding  
**Effort**: 16-20 hours

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| QS-01 | Update/complete `quickstart-copilot.md` | P0 | 3h | F-06 |
| QS-02 | Write `quickstart-claude.md` | P0 | 3h | F-06 |
| QS-03 | Write `quickstart-chatgpt.md` | P0 | 3h | F-06 |
| QS-04 | Write `quickstart-m365.md` | P0 | 3h | F-06 |
| QS-05 | Write `choosing-the-right-pattern.md` | P1 | 2h | F-06 |
| QS-06 | Write `about-prompt-engineering.md` | P1 | 2h | F-08 |
| QS-07 | Write `about-advanced-patterns.md` | P1 | 2h | F-08 |

---

### Phase 3: Category Navigation (Week 3)

**Goal**: Complete index.md coverage for all categories  
**Effort**: 12-16 hours

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| NAV-01 | Create `prompts/advanced/index.md` | P1 | 1.5h | F-02 |
| NAV-02 | Create `prompts/developers/index.md` | P1 | 1.5h | F-02 |
| NAV-03 | Create `prompts/business/index.md` | P1 | 1h | F-02 |
| NAV-04 | Create `prompts/analysis/index.md` | P1 | 1h | F-02 |
| NAV-05 | Create `prompts/m365/index.md` | P1 | 1h | F-02 |
| NAV-06 | Create `prompts/system/index.md` | P1 | 1h | F-02 |
| NAV-07 | Create `prompts/governance/index.md` | P1 | 0.5h | F-02 |
| NAV-08 | Create `prompts/creative/index.md` | P1 | 0.5h | F-02 |
| NAV-09 | Create `agents/index.md` | P1 | 1h | F-02 |
| NAV-10 | Create `instructions/index.md` | P1 | 1h | F-02 |
| NAV-11 | Create learning track YAML files | P1 | 3h | F-09 |

---

### Phase 4: Frontmatter Normalization (Week 4)

**Goal**: All prompts have required fields  
**Effort**: 20-24 hours

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| FM-01 | Add `type` field to all 137 prompts | P0 | 8h | F-04 |
| FM-02 | Add `audience` field to all prompts | P1 | 4h | F-04 |
| FM-03 | Add `shortTitle` field (≤27 chars) | P1 | 3h | F-04 |
| FM-04 | Normalize `platforms` values | P1 | 2h | F-04 |
| FM-05 | Add `governance_tags` to all prompts | P1 | 3h | F-04 |
| FM-06 | Add `dataClassification` to all | P1 | 1h | F-04 |
| FM-07 | Add `reviewStatus` to all | P1 | 1h | F-04 |
| FM-08 | Run validation, fix errors | P0 | 4h | FM-01..07 |

---

### Phase 5: New Sections (Week 5)

**Goal**: Complete content architecture  
**Effort**: 16-20 hours

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| NS-01 | Create `reference/` folder + index.md | P2 | 1h | F-02 |
| NS-02 | Write `reference/cheat-sheet.md` | P2 | 3h | NS-01 |
| NS-03 | Write `reference/platform-comparison.md` | P2 | 2h | NS-01 |
| NS-04 | Write `reference/glossary.md` | P2 | 2h | NS-01 |
| NS-05 | Create `troubleshooting/` + index.md | P2 | 1h | F-02 |
| NS-06 | Write `troubleshooting/prompt-not-working.md` | P2 | 2h | NS-05 |
| NS-07 | Create `tutorials/` folder + index.md | P2 | 1h | F-02 |
| NS-08 | Write first tutorial | P2 | 4h | NS-07 |

---

### Phase 6: Polish & Validation (Week 6)

**Goal**: Production-ready  
**Effort**: 8-12 hours

| ID | Task | Priority | Effort | Dependency |
|----|------|----------|--------|------------|
| PV-01 | Full validation run | P0 | 2h | All |
| PV-02 | Fix all validation errors | P0 | 4h | PV-01 |
| PV-03 | Update README.md | P1 | 2h | All |
| PV-04 | Peer review of new content | P1 | 2h | All |
| PV-05 | Archive superseded planning docs | P2 | 1h | All |

---

## Part 5: Learning Tracks (Unified)

### Track 1: Engineer Quick-Start

```yaml
# data/learning-tracks/engineer-quickstart.yml
title: "Engineer Quick-Start"
description: "From zero to productive with AI code generation"
featured: true
estimatedTime: "4 hours"
audience: ["junior-engineer", "senior-engineer"]
modules:
  - path: /get-started/quickstart-copilot
    title: "Quickstart: GitHub Copilot"
    time: "15 min"
  - path: /concepts/about-prompt-engineering
    title: "About Prompt Engineering"
    time: "20 min"
  - path: /prompts/developers/code-generation/basic-generation
    title: "Basic Code Generation"
    time: "30 min"
  - path: /prompts/developers/debugging/error-analysis
    title: "Debugging with AI"
    time: "30 min"
  - path: /prompts/advanced/chain-of-thought/debugging
    title: "Chain-of-Thought Debugging"
    time: "45 min"
  - path: /reference/cheat-sheet
    title: "Prompt Patterns Cheat Sheet"
    time: "15 min"
```

### Track 2: Architect Deep Dive

```yaml
# data/learning-tracks/architect-depth.yml
title: "Architect Deep Dive"
description: "Master advanced patterns and enterprise governance"
featured: false
estimatedTime: "8 hours"
audience: ["senior-engineer", "solution-architect"]
prerequisites: ["engineer-quickstart"]
modules:
  - path: /concepts/about-advanced-patterns
    title: "About Advanced Patterns"
    time: "30 min"
  - path: /prompts/advanced/react/tool-augmented
    title: "ReAct: Tool-Augmented Reasoning"
    time: "45 min"
  - path: /prompts/advanced/tree-of-thought/architecture-evaluator
    title: "Tree-of-Thoughts for Architecture"
    time: "60 min"
  - path: /prompts/advanced/rag/document-retrieval
    title: "RAG Patterns"
    time: "45 min"
  - path: /tutorials/enterprise-prompt-governance
    title: "Enterprise Prompt Governance"
    time: "60 min"
```

### Track 3: Functional Team Productivity

```yaml
# data/learning-tracks/functional-productivity.yml
title: "Functional Team Productivity"
description: "AI assistance for business tasks without code"
featured: false
estimatedTime: "2 hours"
audience: ["business-analyst", "project-manager", "functional-team"]
modules:
  - path: /get-started/quickstart-m365
    title: "Quickstart: M365 Copilot"
    time: "15 min"
  - path: /concepts/about-prompt-engineering
    title: "About Prompt Engineering"
    time: "20 min"
  - path: /prompts/m365/writing-business-documents
    title: "Writing Business Documents"
    time: "20 min"
  - path: /prompts/business/meeting-summaries
    title: "Meeting Summaries"
    time: "15 min"
  - path: /reference/cheat-sheet
    title: "Prompt Patterns Cheat Sheet"
    time: "15 min"
```

---

## Part 6: Quick Reference Card

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     PROMPT LIBRARY CONTRIBUTOR QUICK REFERENCE               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  REQUIRED FRONTMATTER                                                        │
│  ────────────────────                                                        │
│  title:              "Title" (≤60 chars)                                     │
│  shortTitle:         "Nav" (≤27 chars)     ← GitHub Docs standard            │
│  intro:              "Summary sentence"                                      │
│  type:               conceptual | quickstart | how_to | tutorial |           │
│                      reference | troubleshooting                             │
│  difficulty:         beginner | intermediate | advanced                      │
│  audience:           [junior-engineer, senior-engineer, ...]                 │
│  platforms:          [github-copilot, claude, chatgpt, ...]                  │
│  author:             "Name"                                                  │
│  version:            "1.0"                                                   │
│  date:               "YYYY-MM-DD"                                            │
│  governance_tags:    [PII-safe, client-approved, ...]                        │
│  dataClassification: public | internal | confidential                        │
│  reviewStatus:       draft | reviewed | approved                             │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CONTENT TYPES                                                               │
│  ─────────────                                                               │
│  conceptual      → "About X" (what/why)                                      │
│  quickstart      → "Quickstart for X" (≤15 min first success)                │
│  how_to          → Gerund verb (task-focused)                                │
│  tutorial        → Task-based (end-to-end learning)                          │
│  reference       → Noun-based (quick lookup)                                 │
│  troubleshooting → "Troubleshooting X" (problem/solution)                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  WHERE TO PUT CONTENT                                                        │
│  ────────────────────                                                        │
│  Quickstart         → get-started/                                           │
│  Conceptual         → concepts/                                              │
│  Developer prompt   → prompts/developers/[subcategory]/                      │
│  Advanced technique → prompts/advanced/[technique]/                          │
│  Business prompt    → prompts/business/                                      │
│  M365 prompt        → prompts/m365/                                          │
│  Tutorial           → tutorials/                                             │
│  Reference          → reference/                                             │
│  Troubleshooting    → troubleshooting/                                       │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  INDEX.MD FILES                                                              │
│  ──────────────                                                              │
│  Every folder MUST have index.md with:                                       │
│    children: [/child-1, /child-2]    ← Order matters!                        │
│    featuredLinks:                                                            │
│      gettingStarted: [/path]                                                 │
│      popular: [/path]                                                        │
│                                                                              │
│  ⚠️  Pages not in children array will 404                                    │
│                                                                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  VALIDATION                                                                  │
│  ──────────                                                                  │
│  python tools/validators/frontmatter_validator.py --all                      │
│  Must pass before PR merge                                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 7: ReAct Synthesis Summary

### Actions Taken

| Action | Input | Output | Conflicts Resolved |
|--------|-------|--------|-------------------|
| compare_sections | Frontmatter schemas | Field differences table | shortTitle length, new governance fields |
| compare_sections | Folder structures | Merged architecture | Flat vs nested, existing folders |
| merge_recommendations | Content types | Unified definitions | None (aligned) |
| compare_sections | Timelines | Merged phases | index.md timing |
| validate_consistency | Full output | Validation passed | technique field, topics vs category |

### Confidence Level: **High**

**Justification**:
- Both documents cite the same authoritative sources (GitHub Docs, Microsoft Learn)
- Content types are identical across both documents
- Folder structure differences were reconcilable
- Governance requirements from Refactor Plan preserved
- All unique insights from both documents captured

### Remaining Open Questions

1. **Subfolder depth limit**: Should advanced/ have 2 or 3 levels max?
2. **Validation automation**: Pre-commit hook vs PR check?
3. **Learning track gating**: Should advanced content require prerequisites?

---

## Appendix A: Recommended AI Models by Task

### Model Selection Guide

Use this reference to select the optimal AI model for each task type. Rankings are based on capability, cost-efficiency, and task fit.

#### Phase 1: Foundation + Navigation

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| F-01: Schema documentation | Claude Opus 4.5 | Gemini 2.5 Pro | Claude Sonnet 4.5 |
| F-02: index.md template | Claude Sonnet 4.5 | GPT-4o | Claude Haiku 4.5 |
| F-03: prompt-template.md | Claude Sonnet 4.5 | GPT-4o | Claude Haiku 4.5 |
| F-04: Validation script | Claude Sonnet 4.5 | GPT-4o | Gemini 2.5 Pro |
| F-05 to F-08: index.md files | Claude Haiku 4.5 | Gemini 2.5 Flash | Claude Sonnet 4.5 |
| F-09: data/ YAML files | Claude Sonnet 4.5 | Claude Haiku 4.5 | GPT-4o-mini |
| F-10: Content types doc | Claude Sonnet 4.5 | GPT-4o | Claude Opus 4.5 |

#### Phase 2: Quick-Start Content

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| QS-01 to QS-04: Quickstarts | Claude Sonnet 4.5 | GPT-4o | Claude Opus 4.5 |
| QS-05: Pattern guide | Claude Opus 4.5 | Gemini 2.5 Pro | Claude Sonnet 4.5 |
| QS-06 to QS-07: Conceptual | Gemini 2.5 Pro | Claude Opus 4.5 | Claude Sonnet 4.5 |

#### Phase 3: Category Navigation

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| NAV-01 to NAV-10: index.md | Claude Haiku 4.5 | Gemini 2.5 Flash | GPT-4o-mini |
| NAV-11: Learning tracks | Claude Sonnet 4.5 | Claude Haiku 4.5 | GPT-4o |

#### Phase 4: Frontmatter Normalization

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| FM-01 to FM-07: Bulk updates | Gemini 2.5 Flash | Claude Haiku 4.5 | Claude Sonnet 4.5 |
| FM-08: Validation & fixes | Claude Sonnet 4.5 | GPT-4o | Claude Opus 4.5 |

**Note**: Gemini 2.5 Flash is optimal for bulk updates due to its **1M token context window**, allowing all 137 files to be processed in a single pass.

#### Phase 5: New Sections

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| NS-01, NS-05, NS-07: Folders | Claude Haiku 4.5 | Gemini 2.5 Flash | GPT-4o-mini |
| NS-02: Cheat sheet | Claude Sonnet 4.5 | GPT-4o | Claude Opus 4.5 |
| NS-03: Platform comparison | Claude Opus 4.5 | Gemini 2.5 Pro | Claude Sonnet 4.5 |
| NS-04: Glossary | Claude Haiku 4.5 | GPT-4o-mini | Claude Sonnet 4.5 |
| NS-06: Troubleshooting | GPT-4o | Claude Sonnet 4.5 | Claude Opus 4.5 |
| NS-08: First tutorial | Claude Opus 4.5 | Claude Sonnet 4.5 | Gemini 2.5 Pro |

#### Phase 6: Polish & Validation

| Task | 1st Choice | 2nd Choice | 3rd Choice |
|------|------------|------------|------------|
| PV-01: Full validation | Claude Opus 4.5 | Claude Sonnet 4.5 | Gemini 2.5 Pro |
| PV-02: Fix errors | Claude Sonnet 4.5 | GPT-4o | Claude Haiku 4.5 |
| PV-03: Update README | Claude Sonnet 4.5 | GPT-4o | Claude Opus 4.5 |
| PV-04: Peer review | Claude Opus 4.5 | Gemini 2.5 Pro | GPT-4o |
| PV-05: Archive docs | Claude Haiku 4.5 | GPT-4o-mini | Gemini 2.5 Flash |

### Model Quick Reference

| Model | Best For | Context | Cost (MTok) |
|-------|----------|---------|-------------|
| **Claude Opus 4.5** | Complex reasoning, QA, synthesis | 200K | $5/$25 |
| **Claude Sonnet 4.5** | Coding, templates, balanced tasks | 200K-1M | $3/$15 |
| **Claude Haiku 4.5** | Bulk repetitive edits, speed | 200K | $1/$5 |
| **GPT-4o** | Content writing, debugging | 128K | $2.50/$10 |
| **GPT-4o-mini** | Simple tasks, cost-sensitive | 128K | $0.15/$0.60 |
| **Gemini 2.5 Pro** | Long context analysis, reasoning | 1M+ | ~$1.25/$5 |
| **Gemini 2.5 Flash** | Bulk ops, massive context | 1M | ~$0.08/$0.30 |

---

## Appendix B: Migration Cheat Sheet

### Quick Commands

```bash
# Validate all frontmatter
python tools/validators/frontmatter_validator.py --all

# Add missing field to all files
python tools/cli/bulk_update.py --field type --value how_to --filter "prompts/developers/**/*.md"

# Generate index.md from folder contents
python tools/cli/generate_index.py prompts/advanced/

# Check for orphan files (not in any children array)
python tools/cli/find_orphans.py
```

### File Naming Convention

```text
✅ kebab-case-file-name.md
❌ PascalCaseFileName.md
❌ snake_case_file_name.md
❌ File Name With Spaces.md
```

### Frontmatter Template (Copy/Paste)

```yaml
---
title: ""
shortTitle: ""
intro: ""
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
platforms:
  - "github-copilot"
  - "claude"
topics:
  - ""
author: ""
version: "1.0"
date: ""
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
```

## Appendix B: Documents to Archive

After Phase 6 completion, archive these superseded documents:

| Document | Action | Reason |
|----------|--------|--------|
| `KNOWLEDGE_BASE_ARCHITECTURE_RESEARCH.md` | Archive | Merged into this guide |
| `LIBRARY_REFACTOR_PLAN.md` | Archive | Merged into this guide |
| `COMPLEXITY_AND_ADOPTION_REPORT.md` | Archive | Analysis complete |
| `COMPLEXITY_ADOPTION_TODO.md` | Archive | Tasks moved to this guide |

---

*This guide was synthesized using the ReAct (Reasoning + Acting) pattern, systematically comparing sections, merging recommendations, and validating consistency across both source documents.*

```yaml---
# ═══════════════════════════════════════════════════════════════════════════════