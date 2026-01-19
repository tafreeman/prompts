---
title: "Client Presentation Designer"
shortTitle: "Presentation Designer"
intro: "Creates compelling client presentations with executive summaries, recommendations, and implementation approaches."
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

  - "communication"
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
# Client Presentation Designer

---

## Description

Helps consultants and account teams turn analysis and recommendations into clear, client-ready slide narratives. Focuses on structuring executive summaries, storyline flow, recommendations, and next steps so presentations land with senior stakeholders.

---

## Use Cases

- Designing client-facing presentations for strategy or transformation projects
- Turning long written reports into concise executive decks
- Preparing slide outlines for steering committee or board updates
- Standardizing presentation structure across consulting teams
- Quickly drafting storylines before building slides in PowerPoint or Keynote

---

## Prompt

```text
Create presentation for:

Client: [client]
Presentation Purpose: [purpose]
Audience: [audience]
Key Messages: [messages]
Time Allocation: [duration]

Include:

1. Executive summary
2. Situation analysis
3. Recommendations
4. Implementation approach
5. Expected outcomes
6. Next steps

```text

---

## Variables

- `[client]`: Client or organization name (e.g., "LogiWorld Global Shipping")
- `[purpose]`: Presentation objective (e.g., "Present digital twin solution to reduce conveyor downtime")
- `[audience]`: Target audience roles (e.g., "COO, VP Operations, regional fulfillment leaders")
- `[messages]`: Key points to convey (e.g., "Current model costs $2M/year; solution reduces downtime by 40%")
- `[duration]`: Time allocation (e.g., "30 minutes total with 5 min exec summary, 10 min analysis")

---

## Example

### Context

You need to present a logistics optimization proposal to a global shipping client. The goal is to move from reactive maintenance to a predictive model that reduces downtime and missed SLAs during peak season.

### Input

```text
Create presentation for:

Client: LogiWorld Global Shipping
Presentation Purpose: Present a digital twin–based solution to reduce conveyor downtime and SLA breaches during peak season.
Audience: COO, VP Operations, and regional fulfillment center leaders.
Key Messages: Current reactive maintenance model is costing $2M/year; digital twin and predictive maintenance can reduce downtime by 40%; phased rollout minimizes risk while delivering quick wins in peak regions.
Time Allocation: 30 minutes total (5 min exec summary, 10 min situation analysis, 10 min recommendations & roadmap, 5 min Q&A).

Include:

1. Executive summary
2. Situation analysis
3. Recommendations
4. Implementation approach
5. Expected outcomes
6. Next steps

```text

### Expected Output

The AI generates a slide-by-slide outline with: an executive summary hook and key messages, a concise situation analysis of the current operating model, 2–3 prioritised recommendations, an implementation approach broken into phases with timelines, quantified outcome estimates, and clear next steps for decision and follow-up.

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates
