---

title: "Process Optimization Consultant"
category: "analysis"
tags: ["business-analyst", "process-improvement", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Process Optimization Consultant

## Description

Optimizes business processes

## Use Cases

- Process Improvement for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Optimize process for:

Process Name: [process_name]
Current Issues: [issues]
Stakeholders: [stakeholders]
Success Metrics: [metrics]

Include:
1. Current state analysis
2. Process mapping
3. Bottleneck identification
4. Optimization recommendations
5. Implementation roadmap
6. Change management
```

## Variables

- `[issues]`: Issues
- `[metrics]`: Metrics
- `[process_name]`: Process Name
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[process_name]: Employee Onboarding (IT Provisioning)
[issues]: Takes 2 weeks for new hires to get laptop/email access; 40% dissatisfaction rate
[stakeholders]: HR Director, IT Service Desk, Hiring Managers
[metrics]: "Time to Productivity" (Target: Day 1 Access), Ticket Re-open Rate
```

**Output:**

```text
## Process Optimization Plan

### 1. Current State Analysis
*   **Bottleneck:** HR sends new hire list via email on Friday; IT manually creates tickets on Monday.
*   **Waste:** 30% of tickets bounce back due to missing "Role/Permissions" info.

### 2. Process Mapping
*   **As-Is:** HR Email -> IT Inbox -> Ticket Creation -> Laptop Order (3 days lag).
*   **To-Be:** HRIS (Workday) -> API -> IT Service Management (ServiceNow) -> Auto-provisioning.

### 3. Optimization Recommendations
*   **Automation:** Implement SCIM integration to auto-create Active Directory accounts upon offer acceptance.
*   **Policy:** Maintain "Buffer Stock" of 5 laptops to eliminate shipping delays.

[... continues with implementation roadmap and change management ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Business Analyst prompts in this category
- Check the analysis folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
