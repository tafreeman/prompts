---
title: User Experience Analyst
shortTitle: UX Analysis
intro: Analyzes and improves user experiences through journey mapping, pain point
  analysis, and improvement recommendations.
type: how_to
difficulty: intermediate
audience:

- business-analyst
- senior-engineer

platforms:

- claude
- chatgpt
- github-copilot

topics:

- ux
- analysis

author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# User Experience Analyst

---

## Description

Analyzes and improves user experiences

---

## Use Cases

- User Experience for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Analyze user experience for:

System/Process: [system]
User Groups: [users]
Current Pain Points: [pain_points]
Business Goals: [goals]

Provide:

1. User journey mapping
2. Pain point analysis
3. Improvement opportunities
4. Solution recommendations
5. Success metrics
6. Implementation approach

```text

## Variables

| Variable | Description |
| ---------- | ------------- |
| `[system]` | The system/process/flow to evaluate |
| `[users]` | User groups/personas (and device/context) |
| `[pain_points]` | Known pain points, drop-offs, complaints, or evidence |
| `[goals]` | Business goals and success criteria for improvements |

**Output:**

```text
## UX Analysis Report

### 1. User Journey Mapping (Current)

*   **Step 4 (Friction):** User must scan receipt, email to self, save to desktop, then upload. (Time: 5 mins).
*   **Step 7 (Friction):** "Category" dropdown has 50 options not sorted alphabetically.

### 2. Pain Point Analysis

*   **Severity: Critical.** Mobile incompatibility forces users to do expenses on weekends (unpaid time), leading to resentment.

### 3. Improvement Opportunities

*   **Quick Win:** Enable "Drag and Drop" for receipt images.
*   **Feature:** Implement OCR (Optical Character Recognition) to auto-fill Date and Amount.

[... continues with solution recommendations and metrics ...]
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

A Product Manager needs to analyze the user experience of an e-commerce checkout flow that has a 68% cart abandonment rate and identify opportunities for improvement.

### Input

```text
System/Process: E-commerce checkout flow (5-step process)
User Groups: First-time buyers, returning customers, mobile users
Current Pain Points: High abandonment at shipping step, confusion about delivery options, payment failures
Business Goals: Reduce cart abandonment to <50%, increase mobile conversion by 25%
```

### Expected Output

A comprehensive UX analysis report including:

1. **User Journey Mapping** - Current checkout flow with emotional journey, drop-off points per step
2. **Pain Point Analysis** - Severity-ranked friction points with supporting data (heatmaps, session recordings)
3. **Improvement Opportunities** - Guest checkout, address autocomplete, one-page checkout for mobile
4. **Solution Recommendations** - Wireframes for key improvements with effort/impact matrix
5. **Success Metrics** - Conversion rate, time-to-checkout, error rate, mobile parity score
6. **Implementation Approach** - A/B testing plan with hypothesis for each change

---

## Related Prompts

- [Requirements Analysis Expert](./requirements-analysis-expert.md) - For detailed requirements
- [Workflow Designer](./workflow-designer.md) - For redesigning user flows
- [Process Optimization Consultant](./process-optimization-consultant.md) - For process improvements
- [Consumer Behavior Researcher](./consumer-behavior-researcher.md) - For understanding user psychology
