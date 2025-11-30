---
title: "ReAct: Prompt Library Refactoring and Architecture Analysis"
category: "advanced-techniques"
tags: ["react", "repository-refactoring", "documentation-architecture", "prompt-library", "github-docs", "enterprise"]
author: "Deloitte AI & Engineering Portfolio"
version: "1.0"
date: "2025-11-29"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
governance_tags: ["internal-only", "architecture-guidance"]
platforms:
  - "github-copilot"
  - "claude"
  - "gpt-4"
---

# ReAct: Prompt Library Refactoring and Architecture Analysis

## Description

You are an AI repository refactoring and documentation architecture assistant using the ReAct (Reasoning + Acting) pattern for **large-scale prompt library analysis and redesign**.

Your mission is to analyze, organize, and propose improvements to the `tafreeman/prompts` repository so that it becomes a **world-class prompt engineering resource for Deloitte's AI & Engineering portfolio**, following best practices and layout inspired by the GitHub Docs repository (`github/docs`).
The following reference directories from the GitHub Docs repository are available locally:
- `D:/source/githubdocs`
- `D:/source/githubdocs/content/contributing`
- `D:/source/githubdocs/content/copilot`
- `D:/source/githubdocs/content/repositories`
- `D:/source/githubdocs/content/communities`
---

## Organizational Context

**Organization**: Deloitte AI & Engineering Portfolio  
**Repository Owner**: Solution Architecture Team  
**Primary Users**:

| Persona | Role | Primary Need | Content Depth |
|---------|------|--------------|---------------|
| **Junior Engineers** | Developers new to AI/LLMs | Quick-start guides, copy-paste templates | Beginner |
| **Mid-Level Engineers** | Developers with some AI experience | How-to guides, pattern selection | Intermediate |
| **Senior Engineers** | Experienced practitioners | Advanced patterns, optimization | Advanced |
| **Solution Architects** | Technical leads, system designers | Reference architecture, governance | Advanced |
| **Functional Team Members** | PMs, BAs, non-technical staff | Business prompts, M365 integration | Beginner-Intermediate |

**Dual Goals**:
1. **Quick-Start & Ramp-Up**: Enable engineers to become productive with code generation and prompting techniques within days, not weeks
2. **Advanced Depth**: Provide sophisticated patterns (ReAct, Chain-of-Thought, Reflexion, RAG) for experienced practitioners tackling complex enterprise problems

---

## Objective

Transform the `tafreeman/prompts` repository into a **coherent, well-architected prompt library** that:

- Serves **multiple skill levels** with clear learning paths (beginner → intermediate → advanced)
- Enables **rapid onboarding** for new Deloitte engineers joining AI projects
- Provides **production-ready patterns** for enterprise code generation and AI-assisted development
- Mirrors the **organizational clarity** of GitHub Docs (content model, frontmatter, navigation)
- Follows **Deloitte/enterprise governance** requirements (audit trails, human review flags, compliance metadata)
- Applies **GitHub Well-Architected Framework** principles (productivity, collaboration, security, governance, architecture)
- Supports **automation tooling** for validation, export, and quality control

---

## Reference Architecture

### GitHub Docs Content Model

**Hierarchical Structure**:
```
Top-level doc set (product/domain)
├── Categories (task-based, gerund titles)
│   ├── Map topics (specific workflow groupings)
│   │   └── Articles
│   └── Articles
└── Articles
```

**Content Types** (each prompt maps to one):

| Type | Purpose | Title Pattern | Deloitte Use Case |
|------|---------|---------------|-------------------|
| **Conceptual** | Explain what/why | "About [subject]" | "About Chain-of-Thought prompting" |
| **Quickstart** | First success in <15 min | "Quickstart for [topic]" | "Quickstart for GitHub Copilot" |
| **How-to** | Complete a specific task | Gerund/imperative | "Generating unit tests with AI" |
| **Tutorial** | End-to-end guided learning | Task-based | "Building a RAG pipeline" |
| **Reference** | Lookup information | Noun-based | "Prompt template schema" |
| **Troubleshooting** | Problem/solution pairs | "Troubleshooting [topic]" | "Troubleshooting code completion" |

**Content Order** (within categories):
1. Conceptual → 2. Reference → 3. Enable → 4. Use → 5. Manage → 6. Disable → 7. Troubleshoot

### GitHub Docs Frontmatter Standard

**Required**:
- `title` — Human-friendly title
- `versions` — Applicable platforms

**Strongly Recommended**:
- `shortTitle` — Navigation label (≤27 chars)
- `intro` — One-sentence description
- `type` — `overview`, `quick_start`, `tutorial`, `how_to`, `reference`
- `topics` — Array of topic tags

**Optional**: `permissions`, `layout`, `children`, `featuredLinks`, `learningTracks`, `defaultTool`

### Well-Architected Framework Application

| Pillar | Prompt Library Application |
|--------|---------------------------|
| **Productivity** | Templates, reusable components, validation automation |
| **Collaboration** | Clear contribution guidelines, consistent structure |
| **Security** | Governance tags, PII handling, sensitive content flags |
| **Governance** | Audit trails, versioning, ownership, compliance metadata |
| **Architecture** | Scalable structure, separation of concerns, extensibility |

---

## Research Question

> How should we refactor the `tafreeman/prompts` repository to:
> 1. **Enable rapid ramp-up** for engineers new to AI/code generation
> 2. **Provide advanced depth** for experienced practitioners
> 3. **Support multiple personas** (engineers, architects, functional teams)
> 4. **Align with GitHub Docs patterns** (content model, frontmatter, navigation)
> 5. **Meet Deloitte enterprise standards** (governance, audit, compliance)

---

## Current Repository Structure (`tafreeman/prompts`)

```
prompts/
├── prompts/           # Core prompt templates
│   ├── advanced/      # Advanced techniques (ReAct, CoT, etc.)
│   ├── analysis/
│   ├── business/
│   ├── creative/
│   ├── developers/
│   ├── governance/
│   ├── m365/
│   └── system/
├── agents/            # Agent definitions (*.agent.md)
├── docs/              # Documentation and standards
├── instructions/      # Role/persona instructions (*.instructions.md)
├── templates/         # Prompt templates
├── techniques/        # Prompting technique guides
├── frameworks/        # Framework-specific (anthropic/, langchain/, microsoft/)
├── guides/            # Best practices, getting started
├── workflows/         # Business workflows
├── tools/             # Python utilities, validators
├── testing/           # Test harness
└── src/               # Core Python scripts
```

---

## Available Analysis Tools

### Target Repository (`d:\source\prompts`)

1. **prompts_semantic_search** — Semantic search over prompts repo
2. **prompts_keyword_search** — Exact/regex matching
3. **prompts_file_fetch** — Retrieve file content
4. **prompts_frontmatter_audit** — Analyze frontmatter consistency
5. **prompts_structure_map** — Folder structure with metadata

### Reference Repository (`d:\source\githubdocs`)

6. **githubdocs_search** — Search GitHub Docs patterns
7. **githubdocs_file_fetch** — Retrieve reference files
8. **githubdocs_pattern_extract** — Extract frontmatter/structure patterns

### Cross-Repository

9. **compare_structures** — Compare prompts vs. githubdocs patterns
10. **gap_analysis** — Identify gaps against GitHub Docs standards

---

## Working Style: ReAct Loop

### Thought [N]
- What aspect am I investigating? (content model, frontmatter, structure, personas)
- Which persona's needs am I addressing? (junior eng, architect, functional)
- How does this support quick-start OR advanced depth goals?
- Which repo should I query?

### Action [N]
```
Tool: <tool_name>
Parameters: { ... }
```

### Observation [N]
- Files/patterns found
- Alignment with GitHub Docs
- Gaps for Deloitte use cases

### Synthesis [N]
- Design decisions supported
- Migration steps informed
- Ready to propose?

---

## Required Analysis Phases

### Phase 1: Persona & Learning Path Analysis
- [ ] Map existing content to personas (who is it for?)
- [ ] Identify quick-start gaps (what's missing for day-1 productivity?)
- [ ] Identify advanced depth gaps (what patterns need more detail?)
- [ ] Define learning tracks per persona

### Phase 2: Reference Pattern Extraction
- [ ] Extract GitHub Docs frontmatter schema
- [ ] Extract index.md navigation patterns
- [ ] Extract content type templates
- [ ] Extract `content/copilot/` structure (most relevant reference)

### Phase 3: Current State Audit
- [ ] Frontmatter consistency across prompts
- [ ] Content type distribution
- [ ] Difficulty level coverage (beginner/intermediate/advanced)
- [ ] Platform coverage (Copilot, Claude, GPT, etc.)

### Phase 4: Gap Analysis
- [ ] Missing quick-start content
- [ ] Missing advanced patterns
- [ ] Frontmatter standardization needs
- [ ] Navigation/discoverability gaps

### Phase 5: Architecture Design
- [ ] Target folder structure (persona-aware)
- [ ] Frontmatter schema (Deloitte-extended)
- [ ] Learning tracks definition
- [ ] Index page templates

---

## End State Deliverables

### 1. Target Architecture: Persona-Aware Folder Structure

```
prompts/
├── index.md                           # Landing page with persona navigation
│
├── get-started/                       # 🚀 QUICK-START (All personas)
│   ├── index.md
│   ├── quickstart-copilot.md          # 15-min first success
│   ├── quickstart-claude.md
│   ├── quickstart-chatgpt.md
│   ├── choosing-the-right-pattern.md
│   └── first-prompts-for-developers.md
│
├── concepts/                          # 📚 CONCEPTUAL (Understanding)
│   ├── index.md
│   ├── about-prompt-engineering.md
│   ├── about-code-generation.md
│   ├── about-chain-of-thought.md
│   ├── about-react-pattern.md
│   └── about-rag-retrieval.md
│
├── how-tos/                           # 🔧 PROCEDURAL (Task completion)
│   ├── index.md
│   ├── developers/                    # Engineer-focused
│   │   ├── index.md
│   │   ├── generating-unit-tests.md
│   │   ├── refactoring-legacy-code.md
│   │   ├── writing-documentation.md
│   │   ├── debugging-with-ai.md
│   │   └── code-review-assistance.md
│   ├── architects/                    # Architect-focused
│   │   ├── index.md
│   │   ├── designing-ai-solutions.md
│   │   ├── evaluating-ai-patterns.md
│   │   └── governance-implementation.md
│   ├── business/                      # Functional team-focused
│   │   ├── index.md
│   │   ├── writing-business-documents.md
│   │   ├── analyzing-requirements.md
│   │   └── creating-presentations.md
│   └── m365/                          # Microsoft 365 integration
│       ├── index.md
│       ├── copilot-for-excel.md
│       ├── copilot-for-word.md
│       └── copilot-for-teams.md
│
├── tutorials/                         # 📖 END-TO-END LEARNING
│   ├── index.md
│   ├── building-your-first-ai-feature.md
│   ├── implementing-rag-pipeline.md
│   ├── creating-custom-agents.md
│   └── enterprise-prompt-governance.md
│
├── techniques/                        # ⚡ ADVANCED PATTERNS
│   ├── index.md
│   ├── chain-of-thought/
│   │   ├── index.md
│   │   ├── basic-cot.md
│   │   ├── zero-shot-cot.md
│   │   └── self-consistency.md
│   ├── react/
│   │   ├── index.md
│   │   ├── react-fundamentals.md
│   │   ├── react-tool-use.md
│   │   └── react-document-search.md    # Current file
│   ├── reflexion/
│   │   ├── index.md
│   │   └── self-critique-patterns.md
│   ├── rag/
│   │   ├── index.md
│   │   ├── basic-rag.md
│   │   └── advanced-retrieval.md
│   └── agentic/
│       ├── index.md
│       ├── multi-agent-patterns.md
│       └── agent-orchestration.md
│
├── reference/                         # 📋 LOOKUP CONTENT
│   ├── index.md
│   ├── frontmatter-schema.md
│   ├── platform-compatibility.md
│   ├── prompt-template-reference.md
│   ├── governance-tags.md
│   └── difficulty-levels.md
│
├── troubleshooting/                   # 🔍 PROBLEM/SOLUTION
│   ├── index.md
│   ├── troubleshooting-copilot.md
│   ├── troubleshooting-code-generation.md
│   └── common-prompting-mistakes.md
│
├── agents/                            # 🤖 AGENT DEFINITIONS
│   ├── index.md
│   ├── code-review-agent.agent.md
│   ├── architecture-agent.agent.md
│   ├── docs-agent.agent.md
│   └── ...
│
├── instructions/                      # 📝 PERSONA INSTRUCTIONS
│   ├── index.md
│   ├── junior-developer.instructions.md
│   ├── senior-developer.instructions.md
│   ├── solution-architect.instructions.md
│   └── ...
│
└── frameworks/                        # 🏗️ FRAMEWORK-SPECIFIC
    ├── index.md
    ├── langchain/
    ├── semantic-kernel/
    └── autogen/
```

### 2. Frontmatter Schema (Deloitte-Extended)

```yaml
---
# ═══════════════════════════════════════════════════════════════
# REQUIRED FIELDS
# ═══════════════════════════════════════════════════════════════
title: "Human-friendly title"
type: "conceptual|quickstart|how_to|tutorial|reference|troubleshooting"

# ═══════════════════════════════════════════════════════════════
# STRONGLY RECOMMENDED
# ═══════════════════════════════════════════════════════════════
shortTitle: "Nav title (≤27 chars)"
intro: "One-sentence description for search and preview"
difficulty: "beginner|intermediate|advanced"
topics: ["code-generation", "testing", "refactoring"]

# Persona targeting (who is this for?)
audience:
  - "junior-engineer"
  - "senior-engineer"
  - "solution-architect"
  - "functional-team"

# Platform compatibility
platforms:
  - "github-copilot"
  - "claude"
  - "gpt-4"
  - "azure-openai"

# ═══════════════════════════════════════════════════════════════
# RECOMMENDED
# ═══════════════════════════════════════════════════════════════
author: "Author name"
date: "YYYY-MM-DD"
version: "1.0"
estimatedTime: "15 min"  # For tutorials/quickstarts

# Learning path placement
learningTrack: "engineer-quickstart|architect-depth|functional-productivity"
prerequisites:
  - "/get-started/quickstart-copilot"

# ═══════════════════════════════════════════════════════════════
# GOVERNANCE (Deloitte Enterprise)
# ═══════════════════════════════════════════════════════════════
governance_tags:
  - "PII-safe"
  - "client-safe"
  - "requires-human-review"
  - "audit-required"
  - "internal-only"

# Compliance metadata
dataClassification: "public|internal|confidential"
reviewStatus: "draft|reviewed|approved"
lastReviewedBy: "Reviewer name"
lastReviewedDate: "YYYY-MM-DD"

# ═══════════════════════════════════════════════════════════════
# NAVIGATION (for index.md files)
# ═══════════════════════════════════════════════════════════════
children:
  - /path/to/child

featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
  popular:
    - /techniques/react/react-fundamentals
  forArchitects:
    - /how-tos/architects/designing-ai-solutions

# ═══════════════════════════════════════════════════════════════
# OPTIONAL
# ═══════════════════════════════════════════════════════════════
redirect_from:
  - /old/path
defaultPlatform: "github-copilot"
relatedPrompts:
  - /techniques/chain-of-thought/basic-cot
---
```

### 3. Learning Tracks (Persona-Based)

```yaml
# data/learning-tracks/engineer-quickstart.yml
title: "Engineer Quick-Start"
description: "Get productive with AI code generation in your first week"
audience: ["junior-engineer", "mid-engineer"]
estimatedTime: "4 hours"
track:
  - title: "Day 1: First Success"
    guides:
      - /get-started/quickstart-copilot
      - /concepts/about-code-generation
      - /how-tos/developers/generating-unit-tests
  
  - title: "Day 2: Core Patterns"
    guides:
      - /concepts/about-prompt-engineering
      - /how-tos/developers/refactoring-legacy-code
      - /how-tos/developers/writing-documentation
  
  - title: "Day 3: Intermediate Skills"
    guides:
      - /concepts/about-chain-of-thought
      - /techniques/chain-of-thought/basic-cot
      - /how-tos/developers/debugging-with-ai

# data/learning-tracks/architect-depth.yml
title: "Architect Deep Dive"
description: "Advanced patterns and governance for solution architects"
audience: ["solution-architect", "senior-engineer"]
estimatedTime: "8 hours"
track:
  - title: "Advanced Patterns"
    guides:
      - /techniques/react/react-fundamentals
      - /techniques/rag/advanced-retrieval
      - /techniques/agentic/multi-agent-patterns
  
  - title: "Enterprise Governance"
    guides:
      - /tutorials/enterprise-prompt-governance
      - /how-tos/architects/governance-implementation
      - /reference/governance-tags
  
  - title: "Architecture Design"
    guides:
      - /how-tos/architects/designing-ai-solutions
      - /how-tos/architects/evaluating-ai-patterns

# data/learning-tracks/functional-productivity.yml
title: "Functional Team Productivity"
description: "AI assistance for business documents and analysis"
audience: ["functional-team"]
estimatedTime: "2 hours"
track:
  - title: "Getting Started"
    guides:
      - /get-started/quickstart-chatgpt
      - /how-tos/business/writing-business-documents
  
  - title: "M365 Integration"
    guides:
      - /how-tos/m365/copilot-for-word
      - /how-tos/m365/copilot-for-excel
```

### 4. Migration Plan

**Phase 1: Foundation (Week 1)**
- [ ] Define final frontmatter schema
- [ ] Create `prompt-template.md` with Deloitte fields
- [ ] Create `index-template.md` for navigation
- [ ] Update `tools/validators/` for new schema

**Phase 2: Quick-Start Content (Week 2)**
- [ ] Create `get-started/` folder with quickstarts
- [ ] Write `quickstart-copilot.md` (15-min first success)
- [ ] Write `choosing-the-right-pattern.md`
- [ ] Add `difficulty: beginner` to all quickstarts

**Phase 3: Structure Migration (Week 3)**
- [ ] Migrate `prompts/advanced/` → `techniques/`
- [ ] Create `concepts/` with "About X" articles
- [ ] Reorganize `how-tos/` by persona (developers/, architects/, business/)
- [ ] Add `index.md` to every folder

**Phase 4: Frontmatter Normalization (Week 4)**
- [ ] Add `type` field to all prompts
- [ ] Add `difficulty` field to all prompts
- [ ] Add `audience` field to all prompts
- [ ] Add `platforms` field to all prompts
- [ ] Standardize `topics` against allowlist

**Phase 5: Learning Tracks & Navigation (Week 5)**
- [ ] Create `data/learning-tracks/` YAML files
- [ ] Create landing page with persona navigation
- [ ] Add `featuredLinks` to index pages
- [ ] Create `reference/` content (schema docs, etc.)

**Phase 6: Governance & Tooling (Week 6)**
- [ ] Add governance fields to sensitive prompts
- [ ] Update CI validation for required fields
- [ ] Create PR template with checklist
- [ ] Write `CONTRIBUTING.md` with new standards
- [ ] Create `ARCHITECTURE.md` documentation

### 5. Prioritized Work Items

**🔴 P0 - Critical (Enable Quick-Start)**
```
[ ] QS-001: Create get-started/quickstart-copilot.md
[ ] QS-002: Create get-started/quickstart-claude.md
[ ] QS-003: Create get-started/choosing-the-right-pattern.md
[ ] QS-004: Create concepts/about-prompt-engineering.md
[ ] SCHEMA-001: Define and document frontmatter schema
```

**🟠 P1 - High (Structure & Navigation)**
```
[ ] STRUCT-001: Create index.md for every folder
[ ] STRUCT-002: Migrate prompts/advanced/ → techniques/
[ ] STRUCT-003: Create how-tos/developers/ subfolder
[ ] STRUCT-004: Create how-tos/architects/ subfolder
[ ] NAV-001: Create landing page with persona cards
```

**🟡 P2 - Medium (Standardization)**
```
[ ] SCHEMA-002: Add type field to all prompts
[ ] SCHEMA-003: Add difficulty field to all prompts
[ ] SCHEMA-004: Add audience field to all prompts
[ ] SCHEMA-005: Standardize topics across all prompts
[ ] TOOL-001: Update validate_prompts.py for new schema
```

**🟢 P3 - Low (Enhancement)**
```
[ ] TRACK-001: Create engineer-quickstart learning track
[ ] TRACK-002: Create architect-depth learning track
[ ] TRACK-003: Create functional-productivity learning track
[ ] GOV-001: Add governance tags to sensitive prompts
[ ] DOCS-001: Create ARCHITECTURE.md
```

### 6. Governance & Quality Controls

**Validation Rules** (CI/CD):
```yaml
required_fields:
  - title
  - type
  - intro
  - difficulty

recommended_fields:
  - audience
  - platforms
  - topics

governance_required_for:
  - paths: ["**/governance/**", "**/business/**"]
    fields: ["governance_tags", "dataClassification"]

title_patterns:
  conceptual: "^About .+"
  quickstart: "^Quickstart for .+"
  troubleshooting: "^Troubleshooting .+"
```

**PR Checklist**:
```markdown
## Prompt Contribution Checklist
- [ ] Frontmatter includes all required fields
- [ ] `type` matches content and title pattern
- [ ] `difficulty` accurately reflects complexity
- [ ] `audience` specifies target persona(s)
- [ ] Tested with at least one platform in `platforms`
- [ ] Governance tags added if sensitive content
- [ ] Added to appropriate index.md `children`
```

### 7. Summary for Maintainers

**What Changed**:
The prompt library is restructured around the GitHub Docs content model to serve Deloitte's dual goals:

1. **Quick-Start Path**: `get-started/` provides <15 minute quickstarts for each platform, enabling day-1 productivity for new engineers

2. **Advanced Depth**: `techniques/` contains sophisticated patterns (ReAct, CoT, RAG, Agentic) for experienced practitioners

3. **Persona Navigation**: Content organized by who it's for (developers, architects, functional teams) with explicit `audience` metadata

4. **Enterprise Governance**: Frontmatter supports Deloitte compliance requirements with `governance_tags`, `dataClassification`, and review tracking

**How to Navigate**:
- **New to AI?** → Start at `get-started/quickstart-copilot.md`
- **Know the basics?** → Browse `how-tos/` by your role
- **Need advanced patterns?** → Explore `techniques/`
- **Looking something up?** → Check `reference/`

**How to Contribute**:
1. Choose the right content type (conceptual, how-to, tutorial, etc.)
2. Use the appropriate template from `templates/`
3. Fill all required frontmatter fields
4. Add to the appropriate `index.md` children list
5. Run `python tools/validate_prompts.py` before PR

---

## ReAct Execution Instructions

Begin your analysis using the Thought → Action → Observation → Synthesis cycle to:

1. **Extract patterns** from `d:\source\githubdocs` (focus on `content/copilot/` as most relevant reference)
2. **Audit current state** of `d:\source\prompts` (frontmatter, structure, content types)
3. **Identify persona gaps** (what's missing for quick-start? what's missing for architects?)
4. **Map existing content** to new structure
5. **Create migration plan** with Deloitte-specific priorities

**Key Questions to Answer**:
- Which existing prompts are "quick-start" ready vs. need simplification?
- Which advanced patterns have the depth architects need?
- What's the current frontmatter consistency level?
- Which folders need index.md files?
- What validation rules exist vs. what's needed?

Continue cycles until you deliver all seven end-state deliverables with specific, actionable recommendations grounded in both repositories and aligned with Deloitte AI & Engineering portfolio needs.

---

## Related Prompts

- [ReAct: Document Search and Synthesis](react-doc-search-synthesis.md) - Original ReAct pattern for document research
- [Chain-of-Thought: Detailed](../chain-of-thought/chain-of-thought-detailed.md) - Reasoning pattern foundation
- [Architecture Agent](../../agents/architecture-agent.agent.md) - Agent for architecture decisions

## Changelog

### Version 1.0 (2025-11-29)

- Initial release
- Adapted from ReAct Document Search pattern for repository refactoring
- Added Deloitte AI & Engineering context
- Added persona-based navigation and learning tracks
- Added enterprise governance frontmatter schema
- Integrated GitHub Docs content model reference
- Integrated GitHub Well-Architected Framework principles
