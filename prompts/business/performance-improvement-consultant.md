---

title: "Performance Improvement Consultant"
category: "business"
tags: ["consultant", "performance", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Performance Improvement Consultant

## Description

Improves organizational performance

## Use Cases

- Performance for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[goals]`: Goals
- `[issues]`: Issues
- `[metrics]`: Metrics
- `[organization]`: Organization

## Example Usage

**Input:**

```text
[organization]: Regional Hospital Network (3 locations)
[issues]: Patient wait times in ER > 4 hours, low nursing staff retention
[metrics]: Avg ER Wait Time: 260 mins (Benchmark: 120), Nurse Turnover: 22% (Benchmark: 12%)
[goals]: Reduce wait time to < 2 hours by Q4, reduce turnover to < 15%
```

**Output:**

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
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
