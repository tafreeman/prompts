---
title: Library Network Graph Generator
shortTitle: Network Graph Generator
intro: Guides generation of a Network Graph to visualize relationships and workflows
  between different prompts in the library.
type: how_to
difficulty: advanced
audience:

- senior-engineer
- solution-architect

platforms:

- claude
- chatgpt
- github-copilot

topics:

- visualization
- analysis

author: GitHub Copilot
version: '1.0'
date: '2025-11-18'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

<!-- markdownlint-disable MD025 -->
# Library Network Graph Generator

---

## Description

This prompt guides the generation of a Network Graph visualization to show relationships and workflows between different prompts in the library.

## Goal

To visualize how prompts connect to each other, revealing clusters of related capabilities and potential workflows.

## Context

The prompt library contains many individual files that can be used together in workflows (e.g., SDLC, Business Planning).

## Inputs

- `[PROMPT_LIST]`: List of prompts in the library.
- `[WORKFLOW_DEFINITIONS]`: Optional definitions of workflows connecting prompts.

## Assumptions

- Prompts in the same category are related.
- Prompts can be linked in sequence to form workflows.

## Constraints

- Treat each prompt file as a node.
- Draw edges between related prompts.

## Process / Reasoning Style

Analytical and creative visualization.

---

## Output Requirements

- A detailed description or code (e.g., Python/NetworkX, Mermaid, or Graphviz) to generate the graph.

---

## Use Cases

- Understanding dependencies between prompts.
- Designing new workflows by seeing connected capabilities.
- Visualizing the complexity and interconnectedness of the library.

---

## Prompt

```text
Generate a Network Graph visualization for this prompt library using the provided [PROMPT_LIST].

Treat each prompt file (e.g., "agile-sprint-planner.md", "code-review-assistant.md") as a node.
Draw edges (lines) between prompts that belong to the same category (e.g., all "Business" prompts connected).
Additionally, link prompts that are part of the same workflow (e.g., connect "requirements-analysis-expert.md" to "api-design-consultant.md" and "quality-assurance-planner.md" to represent an SDLC flow).

This should look like a constellation showing clusters of related capabilities.
```text

```

## Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `[PROMPT_LIST]` | List of prompts in the library | ["agile-sprint-planner.md", "code-review-assistant.md", "api-design-consultant.md"] |
| `[WORKFLOW_DEFINITIONS]` | Optional definitions of workflows connecting prompts | "SDLC: requirements-analysis → api-design → code-review → quality-assurance" |

## Example

**Input:**

```text

PROMPT_LIST:

- requirements-analysis-expert.md (category: analysis)
- api-design-consultant.md (category: developers)
- code-review-assistant.md (category: developers)
- market-research-analyst.md (category: analysis)

WORKFLOW_DEFINITIONS:

- "SDLC: requirements-analysis-expert.md -> api-design-consultant.md -> code-review-assistant.md"

```

**Output:**

```text

Return either:

- Mermaid/Graphviz code that creates one node per prompt file, edges connecting prompts in the same category,

  plus explicit edges for the SDLC workflow; or

- Python/NetworkX code that builds the graph with category-based coloring and renders a readable layout.

```

## Tips

- **Identify clusters**: Look for tightly connected groups of prompts that form natural workflows
- **Find gaps**: Disconnected nodes may indicate prompts that need better integration
- **Use color coding**: Assign different colors to different categories for easier visual parsing
