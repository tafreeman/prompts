---
title: "Business Process Reengineering"
shortTitle: "Process Reengineering"
intro: "Reengineers business processes with analysis, new design, technology enablers, and implementation strategy."
type: "how_to"
difficulty: "advanced"
audience:

  - "solution-architect"
  - "business-analyst"

platforms:

  - "claude"
  - "chatgpt"
  - "github-copilot"

topics:

  - "process-improvement"
  - "business"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Business Process Reengineering

---

## Description

Helps consultants and process owners redesign broken or inefficient business processes from the ground up. Focuses on diagnosing bottlenecks, designing a future-state process, identifying technology enablers, and defining implementation and measurement plans.

---

## Use Cases

- Redesigning order-to-cash, procure-to-pay, or quote-to-cash processes
- Streamlining manual, email-driven workflows into automated workflows
- Preparing before/after process views for executive decision-making
- Identifying where to introduce RPA, low-code, or workflow tools
- Standardizing process reengineering deliverables across consulting teams

---

## Prompt

```text
Reengineer process for:

Process: [process_name]
Current Performance: [performance]
Target Improvements: [targets]
Constraints: [constraints]

Include:

1. Process analysis
2. Reengineering approach
3. New process design
4. Technology enablers
5. Implementation strategy
6. Performance metrics

```text

---

## Variables

- `[process_name]`: Name of the business process to reengineer (e.g., "Quote-to-Cash for mid-market customers", "Procure-to-Pay for indirect spend")
- `[performance]`: Current process performance metrics (e.g., "Average cycle time 18 days; 12% rework rate")
- `[targets]`: Desired improvements (e.g., "Reduce cycle time to 6 days, cut rework to under 3%")
- `[constraints]`: Limitations to work within (e.g., "Existing ERP must remain; limited budget in year one")

---

## Example

### Context

A manufacturing company has a slow, error-prone quote-to-cash process that relies heavily on email approvals and manual data entry into the ERP system. Leadership wants to cut cycle time in half and reduce rework while introducing more automation.

### Input

```text
Reengineer process for:

Process: Quote-to-Cash for mid-market manufacturing customers
Current Performance: Average cycle time 18 days from quote to invoice; 12% of orders require manual rework due to pricing or data entry errors.
Target Improvements: Reduce cycle time to 6 days or less, cut rework to under 3%, and improve on-time delivery to 98%.
Target Improvements: Reduce cycle time to 6 days or less, cut rework to under 3%, and improve on-time delivery to 98%.
Constraints: Existing SAP ERP must remain system of record; limited budget for new tools in year one; sales team highly resistant to extra data entry steps.

Include:

1. Process analysis
2. Reengineering approach
3. New process design
4. Technology enablers
5. Implementation strategy
6. Performance metrics

```text

### Expected Output

The AI produces a "Process Reengineering Plan" document with: a current-state analysis highlighting key bottlenecks and waste, a set of reengineering principles, a detailed future-state process map, recommended technology enablers (e.g., workflow tools, RPA, integrations), a phased implementation roadmap with owners and timeline, and a set of KPIs and targets to monitor post-implementation.

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- [Process Optimization Consultant](../analysis/process-optimization-consultant.md) - For detailed process mapping and bottleneck analysis
- [Gap Analysis Expert](../analysis/gap-analysis-expert.md) - For identifying current-to-future state gaps
- [Change Management Coordinator](./change-management-coordinator.md) - For managing organizational change during process improvements
- [Digital Transformation Advisor](./digital-transformation-advisor.md) - For technology-enabled process modernization
