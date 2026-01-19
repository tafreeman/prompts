---
title: "Content Types Reference"
shortTitle: "Content Types"
intro: "Guide to the six content types used in the Prompt Library and when to use each."
type: "reference"
difficulty: "beginner"
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

author: "Prompt Library Team"
version: "1.0"
date: "2025-11-29"
governance_tags:

  - "PII-safe"

dataClassification: "public"
reviewStatus: "approved"
---

# Content Types Reference

The Prompt Library uses six standardized content types, based on the [GitHub Docs](https://docs.github.com) and [Microsoft Learn](https://learn.microsoft.com) documentation architectures.

## Quick Reference

| Type | Purpose | Title Pattern | Time |
| ------ | --------- | --------------- | ------ |
| `conceptual` | Explain what/why/when | "About [Subject]" | 10-30 min |
| `quickstart` | First success | "Quickstart for [Platform]" | ≤15 min |
| `how_to` | Complete a task | Gerund/imperative verb | 15-45 min |
| `tutorial` | End-to-end learning | Task-based | 30-90 min |
| `reference` | Quick lookup | Noun-based | 2-5 min |
| `troubleshooting` | Fix problems | "Troubleshooting [Topic]" | 5-15 min |

---

## Content Type Details

### Conceptual (`conceptual`)

**Purpose**: Explain what something is, why it matters, and when to use it.

**Title Pattern**: "About [Subject]"

**Structure**:

1. Introduction / What is it?
2. Why does it matter?
3. When should you use it?
4. How does it relate to other concepts?
5. Next steps

**Examples**:

- "About Prompt Engineering"
- "About Chain-of-Thought Reasoning"
- "About Model Capabilities"

**When to use**: When readers need to understand a concept before applying it.

---

### Quickstart (`quickstart`)

**Purpose**: Get readers to their first success in 15 minutes or less.

**Title Pattern**: "Quickstart for [Platform/Task]"

**Structure**:

1. Prerequisites (minimal)
2. Step 1: Setup (< 5 min)
3. Step 2-4: Core task (< 10 min)
4. Verify success
5. Next steps / deeper learning

**Examples**:

- "Quickstart for GitHub Copilot"
- "Quickstart for M365 Copilot"
- "Quickstart for Claude"

**When to use**: When introducing a new platform, tool, or major feature.

---

### How-To (`how_to`)

**Purpose**: Help readers complete a specific, focused task.

**Title Pattern**: Use a gerund (verb ending in -ing) or imperative verb

**Structure**:

1. Introduction (1-2 sentences)
2. Prerequisites
3. Step-by-step instructions
4. Expected result
5. Tips and variations
6. Related content

**Examples**:

- "Generating Unit Tests"
- "Creating Code Review Checklists"
- "Debugging with Chain-of-Thought"

**When to use**: When readers have a specific task they need to accomplish.

---

### Tutorial (`tutorial`)

**Purpose**: Guide readers through an end-to-end learning experience with multiple concepts.

**Title Pattern**: Task-based (what will be built/learned)

**Structure**:

1. Introduction and goals
2. Prerequisites
3. Multiple sections (each building on previous)
4. Verification at each major step
5. Summary of what was learned
6. Next steps for further learning

**Examples**:

- "Building Your First AI Feature"
- "Implementing a RAG Pipeline"
- "Enterprise Prompt Governance"

**When to use**: When readers need guided, hands-on learning that combines multiple concepts.

---

### Reference (`reference`)

**Purpose**: Provide quick lookup of information, schemas, or values.

**Title Pattern**: Noun-based (what information is provided)

**Structure**:

- Tables and lists (primary format)
- Minimal prose
- Quick navigation aids
- Code examples where relevant

**Examples**:

- "Frontmatter Schema"
- "Platform Comparison"
- "Governance Tags"
- "Glossary"

**When to use**: When readers need to quickly look up specific information.

---

### Troubleshooting (`troubleshooting`)

**Purpose**: Help readers diagnose and fix problems.

**Title Pattern**: "Troubleshooting [Topic]"

**Structure**:

For each problem:

1. Symptom (what the reader observes)
2. Cause (why it happens)
3. Solution (how to fix it)
4. Prevention (how to avoid it)

**Examples**:

- "Troubleshooting Prompt Quality"
- "Troubleshooting Context Limits"
- "Troubleshooting Output Formatting"

**When to use**: When addressing common problems readers encounter.

---

## Decision Flowchart

Use this flowchart to determine which content type to use:

```text
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

Is this for quick lookup (tables, lists, schemas)?
├── Yes → reference
└── No ↓

Is this about fixing a problem?
├── Yes → troubleshooting
└── No → Re-evaluate scope (may need to split content)
```text

---

## Content Type by Folder

| Folder | Primary Type | Secondary Types |
| -------- | -------------- | ----------------- |
| `get-started/` | quickstart | how_to |
| `concepts/` | conceptual | — |
| `prompts/` | how_to | reference |
| `tutorials/` | tutorial | — |
| `reference/` | reference | — |
| `troubleshooting/` | troubleshooting | — |

---

## See Also

- [Frontmatter Schema](/reference/frontmatter-schema) — Required metadata fields
- [Prompt Template](/templates/prompt-template) — Template for new prompts
- [Index Template](/templates/index-template) — Template for category pages
