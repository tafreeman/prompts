---

title: "Client Presentation Designer"
category: "business"
tags: ["consultant", "presentations", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Client Presentation Designer

## Description

Creates compelling client presentations

## Use Cases

- Presentations for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[audience]`: Audience
- `[client]`: Client
- `[duration]`: Duration
- `[messages]`: Messages
- `[purpose]`: Purpose

## Example Usage

**Input:**

```text
[client]: Global Logistics Firm ("LogiWorld")
[purpose]: Pitch for $5M "Digital Twin" Warehouse Project
[audience]: CTO (Technical), COO (Operational Efficiency), VP Operations (End User)
[messages]: "Reduce downtime by 20%", "Predictive maintenance ROI in 18 months", "Seamless integration with existing SAP ERP"
[duration]: 45 minutes (30 min presentation, 15 min Q&A)
```

**Output:**

```text
## Presentation Outline

### 1. Executive Summary (5 mins)
*   **Hook:** "LogiWorld loses $2M/year to unplanned conveyor belt downtime."
*   **Solution:** A Digital Twin provides real-time visibility and predictive alerts.

### 2. Situation Analysis (5 mins)
*   **Current State:** Reactive maintenance (fix it when it breaks).
*   **Pain Points:** Missed SLAs during peak season.

### 3. Recommendations (10 mins)
*   **Phase 1:** Sensor deployment on critical sorting lines.
*   **Phase 2:** AI model training for failure prediction.

[... continues with implementation approach and next steps ...]
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
