---
title: "Gap Analysis Expert"
shortTitle: "Gap Analysis"
intro: "Conducts comprehensive gap analyses to identify differences between current and desired states with bridging strategies."
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

  - "analysis"
  - "planning"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 3.2
---
# Gap Analysis Expert

---

## Description

Conducts comprehensive gap analyses

---

## Use Cases

- Gap Analysis for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Perform gap analysis for:

Current State: [current_state]
Desired State: [desired_state]
Business Area: [area]
Constraints: [constraints]

Include:

1. Current state assessment
2. Future state definition
3. Gap identification
4. Impact analysis
5. Bridging strategy
6. Implementation roadmap

```text

## Variables

| Variable | Description |
| ---------- | ------------- |
| `[current_state]` | Current-state process/technology/metrics (what exists today) |
| `[desired_state]` | Target future state (outcomes, capabilities, benchmarks) |
| `[area]` | Business area/scope of the analysis |
| `[constraints]` | Constraints (budget, compliance, timeline, tools, staffing) |

**Output:**

```text
## Gap Analysis Report

### 1. Current State Assessment

*   **Process:** Warehouse staff manually count items on Fridays. Data entry errors are common.
*   **Metric:** Stock accuracy is 85%.

### 2. Gap Identification

*   **Technology Gap:** No barcode scanning or WMS (Warehouse Management System).
*   **Process Gap:** No "Cycle Counting" procedure; reliance on full physical counts.

### 3. Bridging Strategy

*   **Tech:** Implement "TradeGecko" (or similar lightweight WMS) integrated with Shopify.
*   **Process:** Equip staff with handheld scanners for real-time "Pick and Pack" updates.

[... continues with impact analysis and roadmap ...]
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

A healthcare organization needs to assess the gap between their current patient scheduling system and a modern, patient-centric appointment experience to reduce no-shows and improve satisfaction.

### Input

```text
Current State: Manual phone scheduling, paper calendars, 48-hour confirmation calls
Desired State: Self-service online booking with automated reminders and waitlist management
Business Area: Patient Access and Scheduling
Constraints: HIPAA compliance, $200K budget, legacy EHR integration required
```

### Expected Output

A comprehensive gap analysis report including:

1. **Current State Assessment** - Detailed process mapping, pain points, metrics (15% no-show rate)
2. **Future State Definition** - Target experience, benchmarks from industry leaders
3. **Gap Identification** - Technology gaps (no patient portal), process gaps (no confirmation automation)
4. **Impact Analysis** - Quantified impact of each gap on revenue, satisfaction, efficiency
5. **Bridging Strategy** - Recommended solutions with build vs. buy analysis
6. **Implementation Roadmap** - 12-month phased plan with quick wins and long-term initiatives

---

## Related Prompts

- [Process Optimization Consultant](./process-optimization-consultant.md) - For process improvement
- [Requirements Analysis Expert](./requirements-analysis-expert.md) - For detailed requirements
- [Business Case Developer](./business-case-developer.md) - For building the investment case
- [Workflow Designer](./workflow-designer.md) - For designing new processes
