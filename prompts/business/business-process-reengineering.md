---

title: "Business Process Reengineering"
category: "business"
tags: ["consultant", "process-reengineering", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Business Process Reengineering

## Description

Reengineers business processes

## Use Cases

- Process Reengineering for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[constraints]`: Constraints
- `[performance]`: Performance
- `[process_name]`: Process Name
- `[targets]`: Targets

## Example Usage

**Input:**

```text
[process_name]: Order-to-Cash (O2C)
[performance]: Cycle time 14 days, Error rate 12% (mostly pricing disputes), Manual touchpoints: 8
[targets]: Cycle time < 3 days, Error rate < 1%, Touchless processing > 80%
[constraints]: Cannot replace core SAP ERP system; Budget limited to $200k
```

**Output:**

```text
## Process Reengineering Plan

### 1. Process Analysis
*   **Bottleneck:** "Pricing Approval" step takes 4 days due to email ping-pong between Sales and Finance.
*   **Waste:** 30% of orders are manually re-keyed from PDF purchase orders.

### 2. Reengineering Approach
*   **Eliminate:** Remove manual pricing approval for standard discount tiers (<10%).
*   **Automate:** Implement RPA (UiPath) to scrape PDF orders and input to SAP.

### 3. New Process Design (To-Be)
*   **Step 1:** Customer portal order entry (Self-service).
*   **Step 2:** Auto-validation of credit & stock.
*   **Step 3:** Auto-release to warehouse (if standard pricing).

[... continues with technology enablers and implementation ...]
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
