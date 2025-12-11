---
title: Prompt Authorship & Contribution Guide
shortTitle: Prompt Authorship & Cont...
intro: A prompt for prompt authorship & contribution guide tasks.
type: how_to
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
# Prompt Authorship & Contribution Guide

## Overview
Crafting a reliable prompt goes beyond clever words—it requires structure, metadata, validation, and security awareness. This guide walks you through reusing the established template, verifying the content, and shipping prompts that keep the library consistent and compliant.

## Prerequisites

- **Git branch**: create a feature branch off `main` before editing prompts.
- **Knowledge of placeholders**: All user-supplied inputs must use `[brackets]` with descriptive names.
- **Security awareness**: Prompts must never embed secrets, credentials, or unredacted PII; classify sensitive context via governance metadata so reviewers can gauge risk.

## Step-by-step instructions

1. **Choose the right folder** (developers, business, creative, analysis, system, advanced-techniques, governance-compliance) and add a lowercase, hyphenated filename (e.g., `prompts/developers/api-design-consultant.md`).
2. **Copy the template** (`templates/prompt-template.md`) and preserve every section even if you temporarily skip content. Replace placeholder text with your narrative, keeping headings and order intact.
3. **Fill in metadata**:
   - `title`, `category`, `tags`, `author`, `version`, `date`, and `difficulty` must be set.
   - Track compliance metadata if relevant: `governance_tags`, `data_classification`, `risk_level`, `approval_required`, `retention_period`, `regulatory_scope`.
4. **Describe the prompt**: Provide a description+goal, explain context, list inputs, assumptions, constraints, reasoning style, and output requirements. Use consistent terminology so downstream tooling can summarize the prompt reliably.
5. **Document variables**: For every `[PLACEHOLDER]` used in the prompt block, add an entry under `## Variables` clarifying what to replace it with.
6. **Provide realistic examples**: Fill `## Example Usage` with both input (actual values) and the expected AI output so publishers understand the intent.
7. **Add tips**: Share usage suggestions, security reminders, or variations to help the audience avoid missteps.
8. **Update changelog**: Reflect your change in `## Changelog` and bump the `version`.
9. **Verify the file visually**: The checklist at the bottom of the template is your quick visual aid to confirm the structure.

### Visual Aid Description

Imagine a stacked diagram where the top layer is the YAML frontmatter (metadata), the middle layer is narrative sections (description, goal, context), and the bottom layer highlights the structured prompt/variables/examples. This mental map helps prompt authors keep their files organized and readable.

## Code snippets with explanations

- **Frontmatter example**:

  ```yaml
  ---
  title: "Service Level Objective Coach"
  category: "developers"
  tags: ["observability", "SRE", "SLO"]
  author: "Avery Example"
  version: "1.2"
  date: "2025-11-19"
  difficulty: "intermediate"
  ---
  ```

  This snippet shows required fields. Keep tags meaningful and update the version/date for every iteration so reviewers know when the prompt changed.

- **Automation-friendly prompt block**:

  ```markdown
  ## Prompt
  You are an SRE who drafts readable SLO dashboards. Use `[SERVICE_NAME]` and `[CURRENT_ERROR_RATE]` when reasoning about reliability.
  Provide JSON-formatted recommendations with `severity`, `owner`, and `next_steps` keys.
  ```

  Always remind the model to return structured output when downstream tools process the response.

## Common pitfalls and how to avoid them

- **Missing placeholders**: Every `[BRACKETED_VALUE]` referenced in the prompt must appear in `## Variables`. If a placeholder is undocumented, reviewers will flag it during validation.
- **Forgetting governance metadata**: Security or compliance scenarios must declare `risk_level` and `approval_required`.
- **Files not parsed**: A stray blank line before the opening `---` or inconsistent indentation can break parsing. Keep the frontmatter contiguous and valid YAML.
- **Using proprietary secrets**: Don't paste API keys, tokens, or customer data. Replace them with placeholders like `[TEST_API_KEY]` and explain how authors should inject their own credentials securely.
- **Neglecting reasoning style**: If a task needs Chain-of-Thought or ReAct, call it out explicitly; otherwise the response may skip important analysis steps.

## Troubleshooting

| Symptom | Likely cause | Fix |
<<<<<<< HEAD
| :--- | :--- | :--- |
=======
| :--- | --- | :--- |
>>>>>>> main
| Parse failure | Missing `---` frontmatter or invalid YAML | Check for stray tabs, unclosed quotes, and ensure metadata keys exist. |
| Placeholders not detected | Placeholder uses curly braces or no brackets | Always wrap variables as `[LIKE_THIS]`. |
| Governance metadata warnings | Required fields empty (e.g., `risk_level`) | Add the relevant fields; refer to `governance-compliance` prompts for examples. |

## Next steps and related topics

- Browse `docs/getting-started.md` for guidance on using the library.
- Review `docs/best-practices.md` to align your prompt with the project's tone and naming conventions.
- Explore monitoring prompts in `docs/developer-prompts-uplift-plan.md` to understand what high-priority use cases look like.
- Consider contributing to `templates/prompt-template.md` if the checklist needs updates for new sections.
