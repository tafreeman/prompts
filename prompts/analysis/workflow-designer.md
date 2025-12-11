---
title: "Workflow Designer"
shortTitle: "Workflow Design"
intro: "Designs efficient business workflows with role definitions, decision points, exception handling, and automation opportunities."
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
  - "workflow"
  - "automation"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Workflow Designer

---

## Description

Designs efficient business workflows

---

## Use Cases

- Workflow Design for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

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

A DevOps Lead needs to design an incident response workflow that ensures rapid detection, triage, and resolution of production incidents with proper escalation and communication.

### Input

```text
Business Process: Production Incident Response
Stakeholders: On-call engineers, Site Reliability Team, Engineering Managers, Customer Success
Complexity Level: High (24/7 operations, multiple severity levels, regulatory requirements)
Automation Goals: Auto-detection, auto-triage for known issues, automated status page updates
```

### Expected Output

A comprehensive workflow design document including:

1. **Workflow Diagram** - Visual flowchart with decision points, parallel paths, and escalation branches
2. **Role Definitions** - On-call responder, Incident Commander, Communications Lead responsibilities
3. **Decision Points** - Severity classification criteria, escalation triggers, rollback decisions
4. **Exception Handling** - After-hours procedures, unavailable responder fallback, customer-impacting vs internal
5. **Automation Opportunities** - PagerDuty integration, Slack bot for status updates, auto-rollback triggers
6. **Performance Metrics** - MTTA (Mean Time to Acknowledge), MTTR, escalation frequency, customer notification SLA

---

## Related Prompts

- [Process Optimization Consultant](./process-optimization-consultant.md) - For optimizing existing workflows
- [Gap Analysis Expert](./gap-analysis-expert.md) - For identifying workflow gaps
- [Requirements Analysis Expert](./requirements-analysis-expert.md) - For workflow requirements
- [Metrics and KPI Designer](./metrics-and-kpi-designer.md) - For workflow performance metrics
