---
title: Prompt Library Refactoring Plan
shortTitle: Prompt Library Refactori...
intro: A prompt for prompt library refactoring plan tasks.
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
# Prompt Library Refactoring Plan

**Generated**: 2025-11-29  
**Analysis Method**: ReAct Pattern (Reasoning + Acting)  
**Reference Architecture**: GitHub Docs (`github/docs`)  
**Target Audience**: Deloitte AI & Engineering Portfolio

---

## Executive Summary

This document provides a comprehensive plan to refactor the `tafreeman/prompts` repository to align with GitHub Docs best practices, enabling:

1. **Rapid onboarding** for engineers new to AI/code generation
2. **Advanced depth** for experienced practitioners  
3. **Multi-persona navigation** (developers, architects, functional teams)
4. **Enterprise governance** compliance

---

## Current State Analysis

### Repository Metrics

| Metric | Value | Assessment |
| :--- |-------| :--- |
| Total prompts | 137 | ✅ Good foundation |
| Index files | 0 | ❌ Critical gap |
| Agents | 7 | ✅ Well-structured |
| Instructions | 10 | ✅ Persona-aware |
| Templates | 3 | ⚠️ Need updates |

### Content Distribution by Category

| Category | Count | % of Total |
| :--- |-------| :--- |
| business | 26 | 19% |
| developers | 25 | 18% |
| system | 23 | 17% |
| m365 | 21 | 15% |
| analysis | 21 | 15% |
| advanced | 16 | 12% |
| governance | 3 | 2% |
| creative | 2 | 1% |

### Difficulty Distribution

| Difficulty | Count | % | Assessment |
<<<<<<< HEAD
| :--- |-------| :--- | :--- |
=======
|------------|-------| :--- |------------|
>>>>>>> main
| Advanced | 56 | 41% | ⚠️ Heavy |
| Intermediate | 53 | 39% | ✅ Good |
| Beginner | 22 | 16% | ⚠️ Light |
| Missing | 6 | 4% | ❌ Fix |

**Insight**: Library skews toward advanced content. Need more beginner-friendly quickstarts for rapid onboarding.

### Frontmatter Field Coverage

| Field | Coverage | Target | Gap |
| :--- |----------| :--- |-----|
| `title` | 100% | 100% | ✅ None |
| `category` | 100% | 100% | ✅ None |
| `tags` | 100% | 100% | ✅ None |
| `difficulty` | 95% | 100% | ⚠️ 6 files |
| `platform` | 93% | 100% | ⚠️ 10 files |
| `type` | 0.7% | 100% | ❌ Critical |
| `audience` | 0% | 100% | ❌ Critical |
| `estimatedTime` | 0% | 50%+ | ❌ Major |

---

## Gap Analysis vs. GitHub Docs

### Structure Gaps

| GitHub Docs Pattern | Current State | Gap Severity |
| :--- |---------------| :--- |
| `index.md` in every folder | None exist | 🔴 Critical |
| `get-started/` quickstarts | No dedicated folder | 🔴 Critical |
| `concepts/` (About X) | No dedicated folder | 🟠 Major |
| `tutorials/` (end-to-end) | No dedicated folder | 🟠 Major |
| `reference/` (lookup) | No dedicated folder | 🟠 Major |
| `troubleshooting/` | No dedicated folder | 🟡 Medium |
| Content type field | 1/137 prompts | 🔴 Critical |
| Learning tracks | None defined | 🟠 Major |

### Navigation Gaps

- No landing page with persona cards
- No "featured links" for popular content
- No learning paths per persona
- No clear "start here" for beginners

---

## Target Architecture

### Folder Structure

```sql
prompts/                              
├── index.md                          # Landing page with persona navigation
│
├── get-started/                      # 🚀 QUICK-START (15-min success)
│   ├── index.md
│   ├── quickstart-copilot.md         
│   ├── quickstart-claude.md
│   ├── quickstart-m365.md
│   └── choosing-the-right-pattern.md
│
├── concepts/                         # 📚 CONCEPTUAL (Understanding)
│   ├── index.md
│   ├── about-prompt-engineering.md
│   ├── about-chain-of-thought.md
│   ├── about-react-pattern.md
│   └── about-rag-retrieval.md
│
├── prompts/                          # 🔧 EXISTING PROMPTS (with index.md)
│   ├── index.md                      
│   ├── advanced/   (+ index.md)
│   ├── developers/ (+ index.md)
│   ├── business/   (+ index.md)
│   ├── analysis/   (+ index.md)
│   ├── m365/       (+ index.md)
│   ├── system/     (+ index.md)
│   ├── governance/ (+ index.md)
│   └── creative/   (+ index.md)
│
├── tutorials/                        # 📖 END-TO-END LEARNING
│   ├── index.md
│   ├── building-first-ai-feature.md
│   ├── implementing-rag-pipeline.md
│   └── enterprise-prompt-governance.md
│
├── reference/                        # 📋 LOOKUP CONTENT
│   ├── index.md
│   ├── frontmatter-schema.md
│   ├── content-types.md
│   ├── governance-tags.md
│   └── platform-compatibility.md
│
├── troubleshooting/                  # 🔍 PROBLEM/SOLUTION
│   ├── index.md
│   ├── common-prompting-mistakes.md
│   └── troubleshooting-code-generation.md
│
├── agents/        (+ index.md)
├── instructions/  (+ index.md)
├── techniques/
├── frameworks/
├── templates/     (update schemas)
├── tools/
└── docs/
```text
### Frontmatter Schema (Deloitte-Extended)

```yaml
---
# ════════════════════════════════════════════════════════════
# REQUIRED FIELDS
# ════════════════════════════════════════════════════════════
title: "Human-friendly title"
type: "conceptual|quickstart|how_to|tutorial|reference|troubleshooting"

# ════════════════════════════════════════════════════════════
# STRONGLY RECOMMENDED
# ════════════════════════════════════════════════════════════
shortTitle: "Nav title (≤27 chars)"
intro: "One-sentence description"
difficulty: "beginner|intermediate|advanced"
topics: ["code-generation", "testing", "refactoring"]

audience:
  - "junior-engineer"
  - "senior-engineer"
  - "solution-architect"
  - "functional-team"

platforms:
  - "github-copilot"
  - "claude"
  - "gpt-4"
  - "azure-openai"
  - "m365-copilot"

# ════════════════════════════════════════════════════════════
# RECOMMENDED
# ════════════════════════════════════════════════════════════
author: "Author name"
date: "YYYY-MM-DD"
version: "1.0"
estimatedTime: "15 min"

# Learning path
learningTrack: "engineer-quickstart|architect-depth|functional-productivity"
prerequisites:
  - "/get-started/quickstart-copilot"

# ════════════════════════════════════════════════════════════
# GOVERNANCE (Enterprise)
# ════════════════════════════════════════════════════════════
governance_tags:
  - "PII-safe"
  - "client-safe"
  - "requires-human-review"
  - "audit-required"
  - "internal-only"

dataClassification: "public|internal|confidential"
reviewStatus: "draft|reviewed|approved"

# ════════════════════════════════════════════════════════════
# NAVIGATION (for index.md files)
# ════════════════════════════════════════════════════════════
children:
  - /path/to/child

featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
  popular:
    - /prompts/advanced/chain-of-thought-detailed
---
```sql
### Content Type Definitions

| Type | Purpose | Title Pattern | Example |
| :--- |---------| :--- |---------|
| `conceptual` | Explain what/why | "About [subject]" | "About Chain-of-Thought" |
| `quickstart` | First success <15 min | "Quickstart for [topic]" | "Quickstart for Copilot" |
| `how_to` | Complete a task | Gerund/imperative | "Generating unit tests" |
| `tutorial` | End-to-end learning | Task-based | "Building a RAG pipeline" |
| `reference` | Lookup information | Noun-based | "Frontmatter schema" |
| `troubleshooting` | Problem/solution | "Troubleshooting [topic]" | "Troubleshooting code generation" |

---

## Learning Tracks

### Track 1: Engineer Quick-Start (4 hours)

**Audience**: Junior/Mid Engineers  
**Goal**: Productive with AI code generation in first week

| Day | Topic | Content |
| :--- |-------| :--- |
| Day 1 | First Success | quickstart-copilot.md → about-code-generation.md → generating-unit-tests.md |
| Day 2 | Core Patterns | about-prompt-engineering.md → refactoring-legacy-code.md |
| Day 3 | Intermediate | about-chain-of-thought.md → chain-of-thought-detailed.md |

### Track 2: Architect Deep Dive (8 hours)

**Audience**: Senior Engineers, Solution Architects  
**Goal**: Master advanced patterns and governance

| Phase | Topic | Content |
| :--- |-------| :--- |
| Advanced Patterns | ReAct, RAG, Agentic | react-doc-search-synthesis.md, rag-document-retrieval.md |
| Enterprise Governance | Compliance, Audit | enterprise-prompt-governance.md, governance-tags.md |
| Architecture Design | Design decisions | architecture-agent.agent.md, designing-ai-solutions.md |

### Track 3: Functional Team Productivity (2 hours)

**Audience**: PMs, BAs, Non-technical staff  
**Goal**: AI assistance for business tasks

| Phase | Topic | Content |
| :--- |-------| :--- |
| Getting Started | First prompts | quickstart-m365.md, writing-business-documents.md |
| M365 Integration | Office apps | copilot-for-word.md, copilot-for-excel.md |

---

## Migration Plan

### Phase 1: Foundation (Week 1)
**Effort**: 8-12 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| F-001 | Create `index.md` template | P0 | 1h |
| F-002 | Update `prompt-template.md` with new fields | P0 | 2h |
| F-003 | Create validation script for new schema | P0 | 4h |
| F-004 | Document content type definitions | P1 | 2h |

### Phase 2: Quick-Start Content (Week 2)
**Effort**: 12-16 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| QS-001 | Create `get-started/` folder | P0 | 0.5h |
| QS-002 | Write `quickstart-copilot.md` | P0 | 3h |
| QS-003 | Write `quickstart-claude.md` | P0 | 3h |
| QS-004 | Write `quickstart-m365.md` | P0 | 3h |
| QS-005 | Write `choosing-the-right-pattern.md` | P0 | 2h |
| QS-006 | Create `get-started/index.md` | P0 | 1h |

### Phase 3: Navigation (Week 3)
**Effort**: 8-12 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| NAV-001 | Create root `index.md` with persona cards | P0 | 3h |
| NAV-002 | Add `index.md` to `prompts/advanced/` | P1 | 1h |
| NAV-003 | Add `index.md` to `prompts/developers/` | P1 | 1h |
| NAV-004 | Add `index.md` to `prompts/business/` | P1 | 1h |
| NAV-005 | Add `index.md` to all other prompt folders | P1 | 3h |
| NAV-006 | Add `index.md` to `agents/` | P1 | 1h |

### Phase 4: Frontmatter Normalization (Week 4)
**Effort**: 16-24 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| FM-001 | Add `type` field to all 137 prompts | P0 | 8h |
| FM-002 | Add `audience` field to all prompts | P1 | 4h |
| FM-003 | Normalize `platform` field values | P1 | 2h |
| FM-004 | Add `estimatedTime` to tutorials/quickstarts | P2 | 2h |
| FM-005 | Fix 6 prompts missing `difficulty` | P1 | 1h |
| FM-006 | Run validation, fix issues | P0 | 4h |

### Phase 5: New Content Structure (Week 5)
**Effort**: 12-16 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| NC-001 | Create `concepts/` folder + index | P1 | 1h |
| NC-002 | Write `about-prompt-engineering.md` | P1 | 2h |
| NC-003 | Write `about-chain-of-thought.md` | P2 | 2h |
| NC-004 | Create `tutorials/` folder + index | P1 | 1h |
| NC-005 | Create `reference/` folder + content | P2 | 4h |
| NC-006 | Create `troubleshooting/` folder + content | P2 | 3h |

### Phase 6: Governance & Tooling (Week 6)
**Effort**: 8-12 hours

| Task ID | Task | Priority | Effort |
| :--- |------| :--- |--------|
| GOV-001 | Update CI validation for required fields | P1 | 4h |
| GOV-002 | Create PR template with checklist | P1 | 1h |
| GOV-003 | Update CONTRIBUTING.md | P1 | 2h |
| GOV-004 | Create ARCHITECTURE.md | P2 | 2h |
| GOV-005 | Define learning tracks in YAML | P2 | 2h |

---

## Prioritized Work Items (GitHub Issues)

### 🔴 P0 - Critical (Enable Quick-Start)

```markdown
## Issue: QS-001 - Create get-started folder with quickstarts
**Labels**: priority-critical, content, quick-start
**Assignee**: @tafreeman
**Effort**: 12 hours

### Description
Create the `get-started/` folder with platform-specific quickstarts to enable 15-minute first success for new engineers.

### Acceptance Criteria
- [ ] `get-started/index.md` with navigation
- [ ] `quickstart-copilot.md` - GitHub Copilot quick-start
- [ ] `quickstart-claude.md` - Claude quick-start
- [ ] `quickstart-m365.md` - M365 Copilot quick-start
- [ ] `choosing-the-right-pattern.md` - Decision guide
- [ ] All files use new frontmatter schema with `type: quickstart`
```text
```markdown
## Issue: FM-001 - Add type field to all prompts
**Labels**: priority-critical, frontmatter, bulk-update
**Assignee**: TBD
**Effort**: 8 hours

### Description
Add the `type` field to all 137 prompts to enable content type filtering and navigation.

### Acceptance Criteria
- [ ] All prompts have `type` field
- [ ] Types correctly match content (conceptual, how_to, tutorial, reference)
- [ ] Validation script passes
```text
```markdown
## Issue: NAV-001 - Create root landing page
**Labels**: priority-critical, navigation
**Assignee**: @tafreeman
**Effort**: 3 hours

### Description
Create root `index.md` with persona-based navigation cards.

### Acceptance Criteria
- [ ] Persona cards: Engineers, Architects, Functional Teams
- [ ] Featured links to popular prompts
- [ ] Learning track references
- [ ] Quick navigation to get-started
```text
### 🟠 P1 - High Priority

```markdown
## Issue: NAV-002-006 - Add index.md to all folders
## Issue: FM-002 - Add audience field to all prompts
## Issue: F-003 - Create validation script for new schema
## Issue: GOV-001 - Update CI validation
```text
### 🟡 P2 - Medium Priority

```markdown
## Issue: NC-001-006 - Create concepts/tutorials/reference folders
## Issue: GOV-005 - Define learning tracks YAML
```text
---

## Validation Rules

### Required Fields (CI will fail if missing)

```yaml
required_fields:
  - title
  - type
  - category
  - difficulty

required_for_quickstarts:
  - estimatedTime
  - platforms

required_for_governance:
  - governance_tags
  - dataClassification
```text
### Content Type Validation

```yaml
title_patterns:
  conceptual: "^About .+"
  quickstart: "^Quickstart for .+"
  troubleshooting: "^Troubleshooting .+"

type_folder_mapping:
  conceptual: concepts/
  quickstart: get-started/
  tutorial: tutorials/
  reference: reference/
  troubleshooting: troubleshooting/
  how_to: prompts/*/
```text
---

## Success Metrics

| Metric | Current | Target | Measurement |
| :--- |---------| :--- |-------------|
| Time to first success (new engineer) | Unknown | <30 min | User survey |
| Index file coverage | 0% | 100% | Automation |
| `type` field coverage | 0.7% | 100% | Automation |
| Beginner content ratio | 16% | 30% | Automation |
| Quickstart satisfaction | N/A | >4/5 | User survey |

---

## Appendix: File Inventory

### Prompts by Category

<details>
<summary>prompts/advanced/ (16 files)</summary>

- chain-of-thought-concise.md
- chain-of-thought-debugging.md
- chain-of-thought-detailed.md
- chain-of-thought-guide.md
- chain-of-thought-performance-analysis.md
- library-analysis-react.md
- library.md
- prompt-library-refactor-react.md
- rag-document-retrieval.md
- react-doc-search-synthesis.md
- react-tool-augmented.md
- README.md
- reflection-self-critique.md
- tree-of-thoughts-architecture-evaluator.md
- tree-of-thoughts-evaluator-reflection.md
- tree-of-thoughts-template.md

</details>

<details>
<summary>prompts/developers/ (25 files)</summary>

- api-design-consultant.md
- cloud-migration-specialist.md
- code-generation-assistant.md
- code-review-assistant.md
- code-review-expert-structured.md
- code-review-expert.md
- csharp-enterprise-standards-enforcer.md
- csharp-refactoring-assistant.md
- data-pipeline-engineer.md
- database-schema-designer.md
- devops-pipeline-architect.md
- documentation-generator.md
- dotnet-api-designer.md
- frontend-architecture-consultant.md
- legacy-system-modernization.md
- microservices-architect.md
- mid-level-developer-architecture-coach.md
- mobile-app-developer.md
- performance-optimization-specialist.md
- README.md
- refactoring-plan-designer.md
- security-code-auditor.md
- sql-query-analyzer.md
- sql-security-standards-enforcer.md
- test-automation-engineer.md

</details>

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Create GitHub Issues** from P0 items
3. **Assign Week 1 tasks** (Foundation)
4. **Begin Phase 1** - Template and validation updates
5. **Track progress** via GitHub Project board

---

*Generated by ReAct Library Analysis Agent*
