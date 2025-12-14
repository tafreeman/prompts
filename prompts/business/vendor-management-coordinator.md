---
title: Vendor Management Coordinator
shortTitle: Vendor Management
intro: Manages vendor relationships with evaluation criteria, contract management,
  and performance monitoring.
type: how_to
difficulty: intermediate
audience:
- project-manager
- business-analyst
platforms:
- claude
- chatgpt
- github-copilot
topics:
- vendor-management
- procurement
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Vendor Management Coordinator

---

## Description

Manages vendor relationships

---

## Use Cases

- Vendor Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Manage vendors for:

Project: [project_name]
Vendor Services: [services]
Contract Terms: [terms]
Performance Issues: [issues]

Include:
1. Vendor evaluation criteria
2. Contract management
3. Performance monitoring
4. Relationship management
5. Issue resolution
6. Payment processing
```text

---

## Variables

- `[project_name]`: Project name (e.g., "Cloud Infrastructure Migration")
- `[services]`: Vendor services (e.g., "AWS infrastructure, DevOps consulting, 24/7 support")
- `[terms]`: Contract terms (e.g., "$500K annual, 99.9% SLA, 3-year commitment")
- `[issues]`: Performance issues (e.g., "October SLA breach at 99.7%, slow ticket response times")

---

## Example

```text
## Vendor Management Plan

### 1. Vendor Evaluation Criteria
*   **Technical Capability:** AWS Advanced Partner status required.
*   **Cultural Fit:** Agile methodology alignment.
*   **Financial Health:** D&B Score > 80.

### 2. Contract Management
*   **SLA Monitoring:** Monthly review of uptime reports.
*   **Penalty Enforcement:** Apply 5% credit for October SLA breach per contract clause 4.2.
*   **Renewal Strategy:** Negotiate volume discounts for 3-year Reserved Instances.

### 3. Performance Monitoring (KPIs)
*   **Delivery:** On-time milestone completion rate (Target: >90%).
*   **Quality:** Defect density in delivered code (Target: <0.5 per KLOC).
*   **Responsiveness:** Mean Time to Respond (MTTR) to support tickets.

[... continues with relationship management and issue resolution ...]
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
