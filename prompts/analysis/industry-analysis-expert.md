---

title: "Industry Analysis Expert"
category: "analysis"
tags: ["researcher", "industry-analysis", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Industry Analysis Expert

## Description

Performs detailed industry analysis

## Use Cases

- Industry Analysis for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze industry:

Industry: [industry]
Analysis Scope: [scope]
Key Questions: [questions]
Stakeholder Interest: [stakeholders]

Include:
1. Industry overview
2. Market dynamics
3. Competitive landscape
4. Trends and drivers
5. Future outlook
6. Strategic recommendations
```

## Variables

- `[industry]`: Industry
- `[questions]`: Questions
- `[scope]`: Scope
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[industry]: Electric Vehicle Charging Infrastructure
[scope]: North America, Public Charging Stations (Level 2 & DC Fast)
[questions]: "Will Tesla's NACS standard dominate?" "How will NEVI funding impact deployment?"
[stakeholders]: Utility Companies, Auto OEMs, Infrastructure Investors
```

**Output:**

```text
## Industry Analysis Report

### 1. Industry Overview
*   **Size:** $3B market in 2024, projected to reach $15B by 2030 (CAGR 25%).
*   **Structure:** Fragmented market consolidating around 3-4 major networks (Tesla, Electrify America, ChargePoint).

### 2. Market Dynamics
*   **Driver:** Federal NEVI funding ($5B) accelerating highway corridor buildout.
*   **Constraint:** Grid capacity bottlenecks delaying site energization by 12-18 months.

### 3. Future Outlook
*   **Standardization:** NACS (Tesla) adoption by Ford/GM signals the end of the "Connector War."
*   **Prediction:** 40% of smaller CPOs (Charge Point Operators) will be acquired by 2026.

[... continues with strategic recommendations ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Researcher prompts in this category
- Check the analysis folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
