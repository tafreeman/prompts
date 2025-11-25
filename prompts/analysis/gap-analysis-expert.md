---

title: "Gap Analysis Expert"
category: "analysis"
tags: ["business-analyst", "gap-analysis", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Gap Analysis Expert

## Description

Conducts comprehensive gap analyses

## Use Cases

- Gap Analysis for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[area]`: Area
- `[constraints]`: Constraints
- `[current_state]`: Current State
- `[desired_state]`: Desired State

## Example Usage

**Input:**

```text
[current_state]: Manual inventory tracking in Excel; Stock counts updated once/week
[desired_state]: Real-time automated inventory management; <1% stockout rate
[area]: Supply Chain Operations
[constraints]: Budget < $50k, Must integrate with Shopify
```

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
