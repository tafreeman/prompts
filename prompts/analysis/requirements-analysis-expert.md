---
title: "Requirements Analysis Expert"
shortTitle: "Requirements Analysis"
intro: "Analyzes and documents business requirements with user stories, acceptance criteria, and traceability."
type: "how_to"
difficulty: "intermediate"
audience:
  - "business-analyst"
  - "solution-architect"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "requirements"
  - "analysis"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Requirements Analysis Expert

---

## Description

Analyzes and documents business requirements

---

## Use Cases

- Requirements for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

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
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Example Usage

### Context

A Business Analyst is gathering requirements for a new customer self-service portal that will allow customers to manage their accounts, view invoices, and submit support tickets.

### Input

```text
Project: Customer Self-Service Portal
Stakeholders: Customer Support, IT, Finance, Marketing, End Customers
Business Objectives: Reduce support call volume by 40%, improve customer satisfaction (NPS +10)
Current Challenges: 60% of calls are for routine account inquiries, no 24/7 support option
```

### Expected Output

A comprehensive requirements analysis document including:

1. **Functional Requirements** - User authentication, account dashboard, invoice history, payment processing, ticket submission
2. **Non-functional Requirements** - Performance (<2s page load), security (SOC 2 compliance), availability (99.9% uptime)
3. **User Stories** - "As a customer, I want to download my invoices so I can submit them for expense reimbursement"
4. **Acceptance Criteria** - Testable conditions for each requirement
5. **Requirements Traceability** - Matrix linking requirements to business objectives
6. **Impact Analysis** - Dependencies on existing systems, integration requirements

---

## Related Prompts

- [Stakeholder Requirements Gatherer](./stakeholder-requirements-gatherer.md) - For stakeholder interview planning
- [User Experience Analyst](./user-experience-analyst.md) - For UX requirements
- [Gap Analysis Expert](./gap-analysis-expert.md) - For current/desired state comparison
- [Business Case Developer](./business-case-developer.md) - For building the project justification
