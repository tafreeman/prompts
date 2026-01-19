---
title: Performance Improvement Consultant
shortTitle: Performance Improvement
intro: Improves organizational performance with diagnosis, root cause analysis, action
  plans, and monitoring frameworks.
type: how_to
difficulty: advanced
audience:

- solution-architect
- business-analyst

platforms:

- claude
- chatgpt
- github-copilot

topics:

- performance
- business

author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Performance Improvement Consultant

---

## Description

Improves organizational performance

---

## Use Cases

- Performance for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Improve performance for:

Organization: [organization]
Performance Issues: [issues]
Current Metrics: [metrics]
Improvement Goals: [goals]

Include:

1. Performance diagnosis
2. Root cause analysis
3. Improvement opportunities
4. Action plan
5. Implementation support
6. Monitoring framework

```text

---

## Variables

- `[organization]`: Organization name and context (e.g., "Metro General Hospital – Emergency Department")
- `[issues]`: Performance issues (e.g., "Average wait time 4.5 hours, patient satisfaction at 62%")
- `[metrics]`: Current metrics (e.g., "Door-to-doctor 45 min, LWBS rate 8%, NPS -12")
- `[goals]`: Improvement goals (e.g., "Reduce wait time to 2 hours, improve satisfaction to 80%")

---

## Example

```text
## Performance Improvement Plan

### 1. Performance Diagnosis

*   **Process Bottleneck:** Triage process takes 45 mins due to manual paperwork.
*   **Staffing:** Peak hours (6pm-10pm) are understaffed by 30%.

### 2. Root Cause Analysis (Fishbone)

*   **People:** High burnout due to mandatory overtime.
*   **Process:** No "Fast Track" for minor injuries.
*   **Technology:** EHR system slow during shift changes.

### 3. Action Plan

*   **Quick Win:** Implement "Fast Track" lane for ESI Level 4/5 patients (minor injuries).
*   **Strategic:** Invest in mobile triage tablets to reduce paperwork time by 50%.

[... continues with implementation support and monitoring ...]
```text

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
