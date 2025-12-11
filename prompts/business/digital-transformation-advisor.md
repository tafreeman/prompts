---
title: "Digital Transformation Advisor"
shortTitle: "Digital Transformation"
intro: "Guides digital transformation initiatives with maturity assessment, technology roadmaps, and change management."
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
  - "digital-transformation"
  - "strategy"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Digital Transformation Advisor

---

## Description

Supports consultants and transformation leaders in designing end‑to‑end digital transformation programmes. Helps assess current digital maturity, define transformation goals, propose technology roadmaps, and plan change management and success metrics.

---

## Use Cases

- Defining a digital transformation strategy for a specific business unit or enterprise
- Preparing transformation proposals and roadmaps for executive approval
- Structuring discovery workshops and follow-up materials with clients
- Comparing alternative transformation paths under different budget scenarios
- Documenting success metrics and KPIs for transformation governance

---

## Prompt

```text
Plan digital transformation for:

Organization: [organization]
Current State: [current_state]
Transformation Goals: [goals]
Budget: [budget]
Timeline: [timeline]

Include:
1. Digital maturity assessment
2. Transformation strategy
3. Technology roadmap
4. Change management
5. Implementation phases
6. Success measurement
```text

---

## Variables

- `[organization]`: Organization name and description (e.g., "Guardian Mutual Insurance – mid-size P&C insurer")
- `[current_state]`: Current situation (e.g., "Legacy mainframe claims system, 21-day average cycle time")
- `[goals]`: Transformation objectives (e.g., "Reduce claims cycle to 5 days, enable digital self-service")
- `[budget]`: Available budget (e.g., "$8M over 3 years")
- `[timeline]`: Target timeline (e.g., "Phase 1 in 12 months, full rollout in 36 months")

---

## Example

### Context

An insurance company is struggling with slow, paper-heavy claims processing and fragmented customer experience. Executives have approved a multi‑year digital transformation budget but need a clear, phased roadmap and change plan.

### Input

```text
Plan digital transformation for:

Organization: Guardian Mutual Insurance – mid‑size P&C insurer operating in 3 countries.
Current State: Heavy reliance on legacy mainframe claims system and paper workflows; average claims cycle time is 21 days; limited digital self‑service for customers.
Transformation Goals: Cut average claims cycle time to under 7 days, move 70% of FNOL submissions to digital channels, and modernize core systems without a risky "big bang" replacement.
Budget: $25M over 3 years (CapEx + OpEx); preference for cloud‑first solutions.
Timeline: 3‑year programme starting Q2 2026, with visible wins in the first 9 months.

Include:
1. Digital maturity assessment
2. Transformation strategy
3. Technology roadmap
4. Change management
5. Implementation phases
6. Success measurement
```text

### Expected Output

The AI produces a structured "Digital Transformation Plan" that covers: a concise maturity assessment, a clear strategy narrative, a year‑by‑year technology roadmap, change management approach (people, process, communications), phased implementation plan, and success metrics with target KPIs and review cadence.

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- [Business Process Reengineering](./business-process-reengineering.md) - For process transformation components
- [Change Management Coordinator](./change-management-coordinator.md) - For managing digital change adoption
- [Process Optimization Consultant](../analysis/process-optimization-consultant.md) - For optimizing digital workflows
- [Gap Analysis Expert](../analysis/gap-analysis-expert.md) - For current/future state technology analysis
