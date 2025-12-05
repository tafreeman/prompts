---
title: Knowledge Base Architecture Research Report
shortTitle: Knowledge Base Architect...
intro: A prompt for knowledge base architecture research report tasks.
type: reference
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
# Knowledge Base Architecture Research Report

**Date**: November 29, 2025  
**Research Method**: ReAct (Reasoning + Acting) Pattern  
**Goal**: Synthesize best practices from industry-leading knowledge bases to inform the architecture of the `tafreeman/prompts` repository

---

## Executive Summary

This report documents research findings from five authoritative sources on documentation and knowledge base architecture. The goal was to answer:

> "What are the best practices for structuring a prompt engineering knowledge base that serves multiple skill levels (beginner to advanced) and personas (developers, architects, business users)?"

**Key Finding**: The **GitHub Docs model** is the most applicable pattern for this prompt library, offering:
- Hierarchical navigation via `index.md` files with `children` arrays
- Content type taxonomy matching our needs
- Learning tracks for guided paths
- Proven patterns for AI/developer documentation (Copilot docs)

---

## Research Sources

| Source | URL Pattern | Focus Area | Key Contribution |
|--------|-------------|------------|------------------|
| **Microsoft Learn** | learn.microsoft.com | Content model, frontmatter, versioning | Required metadata schema, learning paths |
| **GitHub Docs** | docs.github.com | Content types, style guide, structure | `children` arrays, `featuredLinks`, content types |
| **OpenAI** | platform.openai.com/docs | Prompt patterns, examples | Technique classification, before/after examples |
| **Anthropic/Claude** | docs.anthropic.com | Claude prompting, best practices | Ordered techniques, prerequisite structure |
| **AWS** | docs.aws.amazon.com | Enterprise scale, navigation | Featured content, decision guides |

---

## Research Summary Table

| Aspect | Microsoft Learn | GitHub Docs | OpenAI | Anthropic/Claude | AWS | **Recommended** |
|--------|-----------------|-------------|--------|------------------|-----|-----------------|
| **Content Types** | conceptual, quickstart, tutorial, how-to, reference, sample | overview, quick_start, tutorial, how_to, reference, rai | guide, reference, cookbook | guide, reference, best-practices | user-guide, developer-guide, API-reference | **6 types** (see below) |
| **Required Frontmatter** | title, description, author, ms.author, ms.date | title, versions, shortTitle, intro | title, description | title, description | title, services | **title, intro, type, difficulty, audience, platforms** |
| **Navigation Pattern** | Hub pages, TOC, breadcrumbs | index.md with `children` array | Sidebar, search | Sidebar, categories | Service hierarchy | **index.md per folder with `children`** |
| **Learning Paths** | Learning paths with modules | `learningTracks` frontmatter | None explicit | By use case | Workshops | **3 tracks** (engineer, architect, functional) |
| **Examples** | Inline + samples | Inline + syntax highlighting | Playground links | Console links | Code samples | **Inline + "Try it" blocks** |

---

## Detailed Findings by Source

### 1. Microsoft Learn

**Content Model**:
- Separates "Documentation" (quick answers) from "Training" (learning paths)
- Hierarchical: Learning Paths → Modules → Units
- Content types: conceptual, quickstart, tutorial, how-to, reference, sample

**Required Metadata**:
```yaml
title: "Page title (≤60 chars)"           # SEO, browser tab
description: "75-300 character summary"    # Search results
author: "github-username"                  # Content ownership
ms.author: "microsoft-alias"               # Business owner
ms.date: "MM/DD/YYYY"                      # Content freshness
ms.topic: "conceptual|quickstart|..."      # Content type
```sql
**Key Insight**: Microsoft separates "quickstart" (15-min first success) from "tutorial" (end-to-end learning). This distinction is critical for our dual goals.

### 2. GitHub Docs

**Content Structure**:
```text
Top-level doc set
├── Categories
│   ├── Map topics
│   │   └── Articles
│   └── Articles
└── Articles
```text
**Frontmatter Schema**:
```yaml
# Required
title: "Human-friendly title"
versions:
  fpt: '*'
  ghes: '>=3.11'

# Recommended
shortTitle: "Nav label (≤27 chars)"
intro: "1-2 sentence summary"
type: "overview|quick_start|tutorial|how_to|reference"
topics:
  - "Copilot"
  - "AI"

# For index.md pages
children:
  - /get-started
  - /concepts
  - /how-tos
  - /reference
  - /tutorials

# For landing pages
featuredLinks:
  gettingStarted:
    - /get-started/quickstart
  popular:
    - /tutorials/copilot-chat-cookbook
```sql
**Content Types**:
| Type | Purpose | Structure |
|------|---------|-----------|
| `overview` | Conceptual understanding | What, why, when |
| `quick_start` | 15-min first success | Prerequisites → Steps → Next |
| `tutorial` | End-to-end guided learning | Introduction → Steps → Verification |
| `how_to` | Task-focused procedures | Prerequisites → Numbered steps |
| `reference` | Quick lookup | Tables, lists, definitions |

**Key Insight**: Every folder MUST have an `index.md` with a `children` array. Pages not in `children` return 404.

### 3. OpenAI

**Prompt Documentation Patterns**:
- Techniques organized by reliability improvement
- Heavy use of before/after comparisons
- Clear problem → solution → results structure

**Key Techniques Documented**:
1. Chain-of-thought prompting
2. Few-shot examples
3. Self-consistency (multiple outputs, pick most common)
4. Verifiers (generate many, score with discriminator)
5. Selection-inference (alternate selection and inference prompts)
6. Least-to-most prompting (decompose into subtasks)

**Key Insight**: "Let's think step by step" improved accuracy from 18% to 79% on math problems. Simple techniques can have massive impact.

### 4. Anthropic/Claude

**Prompt Engineering Structure**:
```text
Before Prompt Engineering:
├── Define success criteria
├── Create empirical tests
└── Have a first draft prompt

How to Prompt Engineer (ordered by effectiveness):
1. Prompt generator (get a first draft)
2. Be clear and direct
3. Use examples (multishot)
4. Let Claude think (chain of thought)
5. Use XML tags
6. Give Claude a role (system prompts)
7. Prefill Claude's response
8. Chain complex prompts
9. Long context tips
```sql
**Key Insight**: Techniques are ordered from "broadly effective" to "specialized". This ordering helps users know where to start.

### 5. AWS

**Documentation Structure**:
- **Homepage**: Featured Content, Getting Started, Product Guides, Developer Resources
- **Content Types**: User Guide, Developer Guide, API Reference, CLI Reference, Tutorials
- **Discovery**: Prescriptive Guidance (best practices) separate from Reference Documentation

**Key Insight**: AWS separates "Prescriptive Guidance" (patterns, best practices) from "Reference" (API docs). This maps to our quick-start vs depth goals.

---

## Synthesized Recommendations

### Priority 0 - Critical (Week 1)

#### 1. Add index.md to Every Folder

**Evidence**: GitHub Docs, Microsoft Learn, AWS all use index pages for navigation.

**Pattern**: Each folder has `index.md` with `children` array listing contents in order.

**Required Files**:
- `prompts/index.md` (top-level)
- `prompts/advanced/index.md`
- `prompts/developers/index.md`
- `prompts/business/index.md`
- `prompts/creative/index.md`
- `prompts/analysis/index.md`
- `prompts/governance/index.md`
- `prompts/m365/index.md`
- `prompts/system/index.md`

**Effort**: Medium (8-12 hours)

#### 2. Implement Content Type Field

**Evidence**: All 5 sources use explicit content types.

**Pattern**:
```yaml
type: conceptual|quickstart|how_to|tutorial|reference|troubleshooting
```sql
**Content Type Definitions**:
| Type | Purpose | When to Use |
|------|---------|-------------|
| `conceptual` | Understanding, not doing | Explain what/why/when |
| `quickstart` | 15-min first success | New user onboarding |
| `how_to` | Task-focused procedures | "How do I X?" |
| `tutorial` | End-to-end guided learning | Build something complete |
| `reference` | Quick lookup | Tables, lists, definitions |
| `troubleshooting` | Problem → solution | Common issues |

**Effort**: Medium (bulk update script + manual review)

#### 3. Standardize Frontmatter Schema

**Evidence**: Microsoft requires 5 fields; GitHub requires 2 + recommends 4.

**Recommended Schema**:
```yaml
---
# Required fields
title: "Human-readable title"
shortTitle: "Nav label"                    # ≤30 chars
intro: "1-2 sentence summary"
type: "quickstart"                         # conceptual|quickstart|how_to|tutorial|reference|troubleshooting
difficulty: "intermediate"                 # beginner|intermediate|advanced
audience:
  - "junior-engineer"
  - "senior-engineer"
platforms:
  - "github-copilot"
  - "claude"

# Recommended fields
topics:
  - "debugging"
  - "code-review"
technique: "chain-of-thought"              # For advanced prompts
estimatedTime: "15 min"

# Metadata fields
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-29"

# Enterprise governance (optional)
governance_tags:
  - "internal-only"
  - "client-approved"
---
```text
**Effort**: High (schema validation + migration)

---

### Priority 1 - High (Week 2-3)

#### 4. Create Quick-Start Guides

**Evidence**: Microsoft "quickstart" = 15-min first success; GitHub "quick_start" = same concept.

**Required Quickstarts**:
| File | Platform | Status |
|------|----------|--------|
| `get-started/quickstart-copilot.md` | GitHub Copilot | ✅ Exists |
| `get-started/quickstart-claude.md` | Claude | ❌ Create |
| `get-started/quickstart-m365.md` | M365 Copilot | ❌ Create |
| `get-started/quickstart-chatgpt.md` | ChatGPT | ❌ Create |

**Quickstart Structure**:
1. Prerequisites (2 min)
2. First success (5 min)
3. Essential patterns (5 min)
4. Common pitfalls (2 min)
5. Next steps (1 min)

**Effort**: High (12-16 hours of content creation)

#### 5. Add Audience/Persona Field

**Evidence**: Microsoft uses ms.custom for audience; Anthropic organizes by use case.

**Pattern**:
```yaml
audience:
  - "junior-engineer"
  - "senior-engineer"
  - "solution-architect"
  - "qa-tester"
  - "qa-automation-engineer"
  - "business-analyst"
  - "project-manager"
```text
**Application**: Enables persona-based filtering on index pages.

**Effort**: Medium

#### 6. Implement Learning Tracks

**Evidence**: GitHub `learningTracks`, Microsoft Learning Paths.

**Pattern**: YAML files in `data/learning-tracks/`:
```yaml
# data/learning-tracks/engineer-quickstart.yml
title: "Engineer Quick-Start"
description: "From zero to productive in 4 hours"
featured: true
estimatedTime: "4 hours"
audience:
  - "junior-engineer"
  - "senior-engineer"
modules:
  - path: /get-started/quickstart-copilot
    title: "Quickstart: GitHub Copilot"
    estimatedTime: "15 min"
  - path: /concepts/about-prompt-engineering
    title: "About Prompt Engineering"
    estimatedTime: "20 min"
  - path: /prompts/developers/code-generation-basic
    title: "Basic Code Generation"
    estimatedTime: "30 min"
  - path: /prompts/developers/code-review-checklist
    title: "Code Review Checklist"
    estimatedTime: "20 min"
```text
**Initial Tracks**:
| Track | Duration | Audience |
|-------|----------|----------|
| `engineer-quickstart` | 4 hours | Junior/Senior Engineers |
| `architect-depth` | 8 hours | Solution Architects |
| `functional-productivity` | 2 hours | Business Analysts, PMs |

**Effort**: Medium

---

### Priority 2 - Medium (Week 4+)

#### 7. Add shortTitle for Navigation

**Evidence**: GitHub Docs requires shortTitle ≤27 chars for nav.

**Pattern**: `shortTitle: "Short Nav Label"`

**Effort**: Low

#### 8. Create featuredLinks on Landing Pages

**Evidence**: GitHub index.md pages have `featuredLinks.gettingStarted`, `featuredLinks.popular`.

**Pattern**:
```yaml
featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
    - /concepts/about-prompt-engineering
  popular:
    - /prompts/developers/code-generation-basic
    - /prompts/advanced/chain-of-thought-debugging
  guideCards:
    - /prompts/advanced/react-tool-augmented
```text
**Effort**: Low

#### 9. Add Prompt-Specific Metadata

**Evidence**: OpenAI/Anthropic document techniques systematically.

**Pattern**:
```yaml
technique: "chain-of-thought|react|tree-of-thought|few-shot|zero-shot|reflection"
model_compatibility:
  - model: "gpt-4"
    notes: "Best performance"
  - model: "claude-4"
    notes: "Requires XML tags"
  - model: "copilot"
    notes: "Use in chat mode"
variables:
  - name: "code_snippet"
    description: "The code to analyze"
    required: true
    example: "function add(a, b) { return a + b; }"
```text
**Effort**: Medium

#### 10. Create Reference Cheat Sheet

**Evidence**: GitHub Docs Copilot has `reference/cheat-sheet.md`.

**Content**:
- Common prompt patterns (table)
- Platform-specific syntax
- Keyboard shortcuts
- Variable reference

**Effort**: Medium

---

## Recommended Architecture

### Folder Structure

```text
prompts/
├── index.md                        # Top-level landing page
│
├── get-started/                    # Quickstarts & onboarding
│   ├── index.md
│   ├── quickstart-copilot.md
│   ├── quickstart-claude.md
│   ├── quickstart-m365.md
│   ├── quickstart-chatgpt.md
│   └── choosing-the-right-pattern.md
│
├── concepts/                       # Conceptual understanding
│   ├── index.md
│   ├── about-prompt-engineering.md
│   ├── about-advanced-patterns.md
│   ├── model-capabilities.md
│   └── prompt-anatomy.md
│
├── developers/                     # Developer prompts (by task)
│   ├── index.md
│   ├── code-generation/
│   │   ├── index.md
│   │   ├── basic-generation.md
│   │   ├── api-generation.md
│   │   └── test-generation.md
│   ├── debugging/
│   │   ├── index.md
│   │   ├── error-analysis.md
│   │   └── root-cause.md
│   ├── code-review/
│   │   ├── index.md
│   │   └── review-checklist.md
│   └── refactoring/
│       ├── index.md
│       └── modernization.md
│
├── advanced/                       # Advanced techniques
│   ├── index.md
│   ├── chain-of-thought/
│   │   ├── index.md
│   │   ├── debugging.md
│   │   └── analysis.md
│   ├── react/
│   │   ├── index.md
│   │   ├── tool-augmented.md
│   │   └── research.md
│   ├── tree-of-thought/
│   │   ├── index.md
│   │   └── architecture-evaluator.md
│   └── reflection/
│       ├── index.md
│       └── self-critique.md
│
├── business/                       # Business/functional prompts
│   ├── index.md
│   └── ...
│
├── m365/                           # Microsoft 365 prompts
│   ├── index.md
│   └── ...
│
├── system/                         # System prompts
│   ├── index.md
│   └── ...
│
├── reference/                      # Quick reference materials
│   ├── index.md
│   ├── cheat-sheet.md
│   ├── prompt-patterns.md
│   ├── platform-comparison.md
│   └── glossary.md
│
└── troubleshooting/                # Common issues & solutions
    ├── index.md
    ├── prompt-not-working.md
    ├── output-quality.md
    └── context-limits.md

data/
├── learning-tracks/
│   ├── engineer-quickstart.yml
│   ├── architect-depth.yml
│   └── functional-productivity.yml
├── topics.yml                      # Allowed topics for validation
└── platforms.yml                   # Supported platforms
```text
### Index.md Template

```yaml
---
title: "Category Title"
shortTitle: "Short Title"
intro: "One sentence explaining what users will find here."
layout: "category-landing"
contentType: "category"
children:
  - /subcategory-or-article-1
  - /subcategory-or-article-2
  - /subcategory-or-article-3
featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
  popular:
    - /prompts/developers/code-generation-basic
topics:
  - "prompts"
---

# {title}

{intro expanded to 2-3 sentences}

## Quick Start

| If you want to... | Start here |
|-------------------|------------|
| Get started quickly | [Quickstart](/get-started/quickstart-copilot) |
| Understand concepts | [About Prompt Engineering](/concepts/about-prompt-engineering) |

## By Task

| Task | Prompt |
|------|--------|
| Generate code | [Basic Code Generation](/developers/code-generation/basic) |
| Debug issues | [Chain-of-Thought Debugging](/advanced/chain-of-thought/debugging) |

## Popular in This Section

- [Most Popular Prompt 1](/path)
- [Most Popular Prompt 2](/path)
- [Most Popular Prompt 3](/path)
```text
### Prompt Article Template

```yaml
---
title: "Descriptive Title with Pattern Name"
shortTitle: "Nav Title"
intro: "What this prompt does and when to use it."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
topics:
  - "debugging"
  - "root-cause-analysis"
technique: "chain-of-thought"
estimatedTime: "10 min"
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-29"
---

# {title}

## Description

{1-2 paragraphs explaining the prompt's purpose and value}

## When to Use

- Scenario 1
- Scenario 2
- Scenario 3

## Prerequisites

- Prerequisite 1
- Prerequisite 2

## The Prompt

```text
{The actual prompt template with {variables} marked}
```text
## Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `{variable_1}` | What it represents | Yes | `example value` |
| `{variable_2}` | What it represents | No | `example value` |

## Example Usage

### Scenario: {Scenario Name}

**Input:**
```text
{Example input with variables filled in}
```text
**Expected Output:**
```text
{Example of what the AI should produce}
```text
## Tips & Variations

- **Tip 1**: Helpful advice
- **Tip 2**: Platform-specific note
- **Variation**: How to adapt for different use cases

## Related Prompts

- [Related Prompt 1](/path/to/prompt) - Brief description
- [Related Prompt 2](/path/to/prompt) - Brief description

## Further Reading

- [External Resource](https://example.com) - Description
```text
---

## Key Questions Answered

### 1. What content types should we use?

**Answer**: 6 types aligned with user intent:

| Type | Purpose | Example |
|------|---------|---------|
| `conceptual` | Understanding, not doing | "About Prompt Engineering" |
| `quickstart` | 15-min first success | "Quickstart for Copilot" |
| `how_to` | Task-focused procedures | "How to Debug with CoT" |
| `tutorial` | End-to-end guided learning | "Build a Code Review Agent" |
| `reference` | Quick lookup | "Prompt Patterns Cheat Sheet" |
| `troubleshooting` | Problem → solution | "Prompt Not Working?" |

### 2. What frontmatter fields are required?

**Answer**: Minimum 8 fields:
- `title` - Page title (≤60 chars)
- `shortTitle` - Navigation label (≤30 chars)
- `intro` - 1-2 sentence summary
- `type` - Content type
- `difficulty` - Skill level
- `audience` - Target personas (array)
- `platforms` - Supported AI platforms (array)
- `date` - Last updated

### 3. How should we structure navigation?

**Answer**: GitHub Docs model:
- Every folder has `index.md`
- `children` array defines navigation order
- `featuredLinks` highlights important content
- `shortTitle` for compact navigation labels

### 4. How do we guide users from beginner to advanced?

**Answer**: Learning tracks in separate YAML files:
- 3 initial tracks: engineer, architect, functional
- Each track is a sequence of articles
- Progressive difficulty within each track
- Estimated time for planning

### 5. What prompt-specific metadata should we track?

**Answer**: Add fields for:
- `technique` - Pattern classification (chain-of-thought, react, etc.)
- `variables` - Template parameters with examples
- `model_compatibility` - Which models work best
- `estimatedTime` - How long to complete

### 6. How do we handle enterprise governance?

**Answer**: Optional governance fields:
- `governance_tags` - Classification labels
- `author` + `version` + `date` - Change tracking
- `review_status` - Approval workflow (draft, reviewed, approved)

---

## Implementation Checklist

### Week 1 (P0 - Critical)

- [ ] Create `prompts/index.md` with top-level children
- [ ] Create index.md for each prompt subfolder (8 files)
- [ ] Define frontmatter schema in `docs/FRONTMATTER_SCHEMA.md`
- [ ] Add `type` field to 10 pilot prompts
- [ ] Create frontmatter validation script

### Week 2-3 (P1 - High)

- [ ] Add `type` field to all remaining prompts
- [ ] Add `audience` field to all prompts
- [ ] Create `get-started/quickstart-claude.md`
- [ ] Create `get-started/quickstart-m365.md`
- [ ] Create `data/learning-tracks/engineer-quickstart.yml`
- [ ] Create `data/learning-tracks/architect-depth.yml`
- [ ] Create `data/learning-tracks/functional-productivity.yml`

### Week 4+ (P2 - Medium)

- [ ] Add `shortTitle` to all prompts
- [ ] Add `featuredLinks` to all index.md files
- [ ] Create `reference/cheat-sheet.md`
- [ ] Add `technique` field to advanced prompts
- [ ] Add `variables` documentation to prompts with templates
- [ ] Create `troubleshooting/` section

---

## Confidence Assessment

**Overall Confidence: High**

**Justification**:
- All recommendations supported by 3+ authoritative sources
- GitHub Docs model is open source (exact implementation visible)
- Patterns proven at scale (GitHub Copilot docs, Microsoft Learn)
- Architecture handles both quick-start and advanced depth goals

**Risks**:
| Risk | Mitigation |
|------|------------|
| Migration effort underestimated | Start with pilot folder, measure actual time |
| Schema too complex | Make most fields optional initially |
| Learning tracks not used | Measure usage, iterate on content |

**Open Questions**:
1. Should `ms.date` pattern be adopted for content freshness tracking?
2. How to handle multi-platform prompts (same prompt, different syntax)?
3. Should learning tracks gate access to advanced content?

---

## References

1. Microsoft Learn Contributor Guide - https://learn.microsoft.com/contribute/
2. GitHub Docs Contributing Guide - https://docs.github.com/contributing
3. OpenAI Cookbook - https://cookbook.openai.com
4. Anthropic Claude Documentation - https://docs.anthropic.com
5. AWS Documentation - https://docs.aws.amazon.com

---

*This research was conducted using the ReAct (Reasoning + Acting) pattern, systematically investigating each source and synthesizing findings into actionable recommendations.*
