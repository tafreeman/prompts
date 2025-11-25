---

title: "Requirements Analysis Expert"
category: "analysis"
tags: ["business-analyst", "requirements", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Requirements Analysis Expert

## Description

Analyzes and documents business requirements

## Use Cases

- Requirements for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze requirements for:

Project: [project_name]
Stakeholders: [stakeholders]
Business Objectives: [objectives]
Current Challenges: [challenges]

Provide:
1. Functional requirements
2. Non-functional requirements
3. User stories
4. Acceptance criteria
5. Requirements traceability
6. Impact analysis
```

## Variables

- `[challenges]`: Challenges
- `[objectives]`: Objectives
- `[project_name]`: Project Name
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[project_name]: Mobile Banking "Bill Split" Feature
[stakeholders]: Product Manager, iOS Dev Team, Legal/Compliance
[objectives]: Increase P2P transaction volume by 20% among Gen Z users
[challenges]: Complex logic for unequal splits, recurring bills, and cross-border payments
```

**Output:**

```text
## Requirements Analysis Document

### 1. Functional Requirements
*   **FR-01:** User must be able to select a transaction from history and click "Split".
*   **FR-02:** User must be able to select contacts from phone book or enter email/phone.
*   **FR-03:** System must calculate split amounts (Equal or Custom).

### 2. Non-functional Requirements
*   **Security:** All split requests must be authenticated via FaceID/TouchID.
*   **Performance:** Split notification must be delivered < 5 seconds.

### 3. User Stories
*   **US-1:** "As a roommate, I want to split the rent unequally (based on room size), so we pay our fair share."
*   **Acceptance Criteria:** Input fields accept decimal values; Total must equal 100%.

[... continues with traceability and impact analysis ...]
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
