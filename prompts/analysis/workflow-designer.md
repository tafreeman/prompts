---

title: "Workflow Designer"
category: "analysis"
tags: ["business-analyst", "workflow-design", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Workflow Designer

## Description

Designs efficient business workflows

## Use Cases

- Workflow Design for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design workflow for:

Business Process: [process]
Stakeholders: [stakeholders]
Complexity Level: [complexity]
Automation Goals: [automation]

Provide:
1. Workflow diagram
2. Role definitions
3. Decision points
4. Exception handling
5. Automation opportunities
6. Performance metrics
```

## Variables

- `[automation]`: Automation
- `[complexity]`: Complexity
- `[process]`: Process
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[process]: Content Publishing (Corporate Blog)
[stakeholders]: Writers, Editors, SEO Specialist, Legal Compliance, CMS Admin
[complexity]: Medium (Multi-stage approval required)
[automation]: Auto-post to LinkedIn/Twitter upon publish; Slack notifications for approvals
```

**Output:**

```text
## Workflow Design Document

### 1. Workflow Diagram (Logic)
*   **Draft** -> **SEO Review** (If Fail: Return to Draft) -> **Editorial Review** -> **Legal Review** (Only if "Product Claim" tag is present) -> **Publish**.

### 2. Role Definitions
*   **SEO Specialist:** Gatekeeper. Must approve keyword usage before Editor sees it.
*   **Legal:** Consulted only on specific topics (Medical/Financial claims).

### 3. Automation Opportunities
*   **Trigger:** When status = "Published" in CMS.
*   **Action:** Zapier webhook posts title + link to Company LinkedIn Page.

[... continues with exception handling and performance metrics ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Business Analyst prompts in this category
- Check the analysis folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
