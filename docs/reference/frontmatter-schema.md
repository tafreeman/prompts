---
title: "Frontmatter Schema Reference"
shortTitle: "Frontmatter Schema"
intro: "Complete reference for YAML frontmatter fields required in all prompt library content."
type: "reference"
difficulty: "intermediate"
audience:
  - "junior-engineer"
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
  - "azure-openai"
  - "m365-copilot"
topics:
  - "documentation"
  - "governance"
author: "Prompt Library Team"
version: "1.0"
date: "2025-11-29"
governance_tags:
  - "PII-safe"
dataClassification: "public"
reviewStatus: "approved"
---

# Frontmatter Schema Reference

This document defines the complete YAML frontmatter schema for all content in the Prompt Library. Every Markdown file must include valid frontmatter to ensure consistency, discoverability, and governance compliance.

## Quick Start

Copy this template for new prompts:

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
date: "YYYY-MM-DD"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
```sql
---

## Field Reference

### Required Fields (All Content)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `title` | String | ≤60 chars | Human-readable title displayed in navigation and search |
| `shortTitle` | String | ≤27 chars | Abbreviated title for sidebar and breadcrumbs (GitHub Docs standard) |
| `intro` | String | 1-2 sentences | Summary shown in search results and content cards |
| `type` | Enum | 6 values | Content classification (see Content Types below) |
| `difficulty` | Enum | 3 values | `beginner` \| `intermediate` \| `advanced` |

### Required Fields (Prompts Only)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `audience` | Array | Valid personas | Target user roles (see Audience Values below) |
| `platforms` | Array | Valid platforms | AI platforms where this prompt works (see Platform Values below) |

### Metadata Fields (Required)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `author` | String | Name | Content owner or team |
| `version` | String | Semver | Semantic version (e.g., `1.0`, `1.1`, `2.0`) |
| `date` | String | YYYY-MM-DD | Last updated date |

### Governance Fields (Required)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `governance_tags` | Array | Valid tags | Classification labels for compliance |
| `dataClassification` | Enum | 3 values | `public` \| `internal` \| `confidential` |
| `reviewStatus` | Enum | 3 values | `draft` \| `reviewed` \| `approved` |

### Recommended Fields (Optional)

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| `topics` | Array | From topics.yml | Tags for filtering and search |
| `technique` | Enum | 7 values | Advanced prompting technique used |
| `estimatedTime` | String | "X min" format | Time to complete or learn |
| `prerequisites` | Array | Valid paths | Content that should be read first |
| `learningTrack` | Enum | 3 values | Associated learning track |

### Navigation Fields (index.md Only)

| Field | Type | Description |
|-------|------|-------------|
| `layout` | String | Page layout: `category-landing` \| `product-landing` |
| `children` | Array | Ordered list of child page paths |
| `featuredLinks` | Object | Highlighted links for landing pages |

---

## Allowed Values

### Content Types (`type`)

| Value | Purpose | Title Pattern | Example |
|-------|---------|---------------|---------|
| `conceptual` | Explain what/why/when | "About [Subject]" | "About Chain-of-Thought" |
| `quickstart` | 15-min first success | "Quickstart for [Platform]" | "Quickstart for Copilot" |
| `how_to` | Complete a specific task | Gerund/imperative verb | "Generating Unit Tests" |
| `tutorial` | End-to-end guided learning | Task-based | "Building a RAG Pipeline" |
| `reference` | Quick information lookup | Noun-based | "Frontmatter Schema" |
| `troubleshooting` | Solve problems | "Troubleshooting [Topic]" | "Troubleshooting Output Quality" |

### Audience Values (`audience`)

| Value | Description |
|-------|-------------|
| `junior-engineer` | Engineers with 0-2 years experience |
| `senior-engineer` | Engineers with 3+ years experience |
| `solution-architect` | Technical architects and tech leads |
| `qa-engineer` | Quality assurance engineers |
| `business-analyst` | Business analysts |
| `project-manager` | Project and program managers |
| `functional-team` | Non-technical functional roles |

### Platform Values (`platforms`)

| Value | Description |
|-------|-------------|
| `github-copilot` | GitHub Copilot (VS Code, JetBrains, etc.) |
| `claude` | Anthropic Claude (claude.ai, API) |
| `chatgpt` | OpenAI ChatGPT (chat.openai.com) |
| `azure-openai` | Azure OpenAI Service |
| `m365-copilot` | Microsoft 365 Copilot |

### Technique Values (`technique`)

| Value | Description |
|-------|-------------|
| `chain-of-thought` | Step-by-step reasoning |
| `react` | Reasoning + Acting with tools |
| `tree-of-thought` | Branching exploration of solutions |
| `few-shot` | Examples provided in prompt |
| `zero-shot` | No examples, direct instruction |
| `reflection` | Self-critique and improvement |
| `rag` | Retrieval-Augmented Generation |

### Governance Tags (`governance_tags`)

| Value | Description |
|-------|-------------|
| `PII-safe` | No personally identifiable information in prompt or expected output |
| `client-approved` | Cleared for use with client data/projects |
| `internal-only` | Restricted to internal use only |
| `requires-human-review` | Output must be validated by a human |
| `audit-required` | Usage must be logged for compliance |

### Learning Track Values (`learningTrack`)

| Value | Duration | Target Audience |
|-------|----------|-----------------|
| `engineer-quickstart` | 4 hours | Junior/Senior Engineers |
| `architect-depth` | 8 hours | Senior Engineers, Solution Architects |
| `functional-productivity` | 2 hours | Business Analysts, Project Managers |

---

## Complete Schema Example

### Standard Prompt

```yaml
---
title: "Chain-of-Thought Debugging Prompt"
shortTitle: "CoT Debugging"
intro: "Use step-by-step reasoning to systematically debug complex code issues."
type: "how_to"
difficulty: "intermediate"
audience:
  - "junior-engineer"
  - "senior-engineer"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "debugging"
  - "code-generation"
technique: "chain-of-thought"
estimatedTime: "15 min"
prerequisites:
  - "/get-started/quickstart-copilot"
learningTrack: "engineer-quickstart"
author: "Prompt Library Team"
version: "1.0"
date: "2025-11-29"
governance_tags:
  - "PII-safe"
  - "client-approved"
dataClassification: "internal"
reviewStatus: "approved"
---
```text
### Index Page (Category Landing)

```yaml
---
title: "Advanced Prompting Techniques"
shortTitle: "Advanced"
intro: "Master sophisticated prompting patterns for complex reasoning tasks."
type: "reference"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
  - "azure-openai"
author: "Prompt Library Team"
version: "1.0"
date: "2025-11-29"
governance_tags:
  - "PII-safe"
dataClassification: "public"
reviewStatus: "approved"
layout: "category-landing"
children:
  - /prompts/advanced/chain-of-thought
  - /prompts/advanced/react
  - /prompts/advanced/tree-of-thought
  - /prompts/advanced/reflection
  - /prompts/advanced/rag
featuredLinks:
  gettingStarted:
    - /get-started/quickstart-copilot
    - /concepts/about-advanced-patterns
  popular:
    - /prompts/advanced/chain-of-thought/debugging
    - /prompts/advanced/react/tool-augmented
---
```text
---

## Validation

Run the frontmatter validator before submitting any PR:

```bash
python tools/validators/frontmatter_validator.py --all
```text
To validate a specific file:

```bash
python tools/validators/frontmatter_validator.py path/to/file.md
```text
### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing required field: title` | Field not present | Add the `title` field |
| `shortTitle exceeds 27 characters` | Title too long | Shorten to ≤27 chars |
| `Invalid type value` | Unrecognized content type | Use one of the 6 valid values |
| `Invalid audience value` | Unrecognized persona | Use values from Audience table |
| `Invalid platform value` | Unrecognized platform | Use values from Platform table |

---

## See Also

- [Content Types Reference](/reference/content-types)
- [Governance Tags Reference](/reference/governance-tags)
- [Prompt Template](/templates/prompt-template)
- [Index Template](/templates/index-template)
