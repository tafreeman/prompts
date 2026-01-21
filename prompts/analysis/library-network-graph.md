---
name: Library Network Graph Generator
description: Guides generation of a Network Graph to visualize relationships and workflows between different prompts in the library.
type: how_to
---

<!-- markdownlint-disable MD025 -->
# Library Network Graph Generator

## Description

Creates network graph visualizations showing relationships and workflows between prompts. Identifies clusters of related capabilities, workflow connections, and disconnected prompts that need better integration across the library.

## Output Requirements

- A detailed description or code (e.g., Python/NetworkX, Mermaid, or Graphviz) to generate the graph.

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
