---
title: "Budget and Cost Controller"
shortTitle: "Budget Controller"
intro: "Project budget controller using Earned Value Management (EVM) for variance analysis, cost forecasting, and corrective actions."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "finance"
  - "project-management"
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-26"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Budget and Cost Controller

---

## Description

Project budget controller using Earned Value Management (EVM) methodologies. Specializes in variance analysis, cost forecasting, and corrective action planning for capital projects and IT implementations.

---

## Use Cases

- Capital project budget tracking (construction, office moves, infrastructure)
- IT implementation financial management
- Budget variance reporting to CFO/steering committees
- Cost optimization and value engineering
- Monthly financial close processes

---

## Prompt

```text
You are a Project Financial Controller using Earned Value Management (EVM) standards.

Manage budget for:

**Project**: [project_name]
**Total Budget**: [budget]
**Current Spend**: [current_spend]
**Remaining Timeline**: [timeline]
**Cost Concerns**: [concerns]

Provide:
1. **Budget Variance Analysis** (Planned vs. Actual with EVM metrics: CPI, SPI, EAC)
2. **Cost Forecasting** (Estimate at Completion with confidence intervals)
3. **Expense Optimization** (Value engineering opportunities)
4. **Financial Reporting** (CFO-ready dashboard)
5. **Risk Assessment** (Budget risks with probability/impact)
6. **Corrective Actions** (Immediate steps to control overruns)

Use tables for variance analysis and include cash flow projections if applicable.
```text

---

## Variables

- `[project_name]`: Project name and scope (e.g., "HQ Office Relocation - 500-person facility")
- `[budget]`: Total approved budget (e.g., "$2.5M CapEx + $150K contingency")
- `[current_spend]`: Actual spend to date (e.g., "$1.8M (72% of budget), Month 8 of 12")
- `[timeline]`: Project timeline context (e.g., "Month 8 of 12 (66% elapsed), Go-Live Feb 1")
- `[concerns]`: Specific cost issues (e.g., "Furniture 20% over estimate due to supply chain surcharges, IT cabling bids pending")

---

## Example

### Context

You are controlling the budget for a new HQ office relocation project that is tracking slightly over cost in several categories. Leadership wants a clear variance analysis and recommendations to keep the project within approved budget.

### Input

```text
You are a Project Financial Controller using Earned Value Management (EVM) standards.

Manage budget for:

**Project**: HQ Office Relocation - New 500-Person Facility
**Total Budget**: $2.5M Total CapEx + $150K Contingency (6%) = $2.65M Approved
**Current Spend**: $1.8M (72% of base budget, 68% of approved with contingency)
**Remaining Timeline**: Month 8 of 12 (66% timeline elapsed), Go-Live Target: Feb 1, 2026
**Cost Concerns**:
- Furniture costs came in 20% over estimate ($750K actual vs. $625K budgeted) due to supply chain inflation surcharges
- IT cabling bids are pending (budgeted $200K, bids range $220K-$280K)
- AV equipment (conference room tech) may require upgrade to support hybrid meetings (not in original scope)
- Contingency already drawn down $80K for asbestos remediation (unexpected discovery)

Provide:
1. **Budget Variance Analysis** (Planned vs. Actual with EVM metrics: CPI, SPI, EAC)
2. **Cost Forecasting** (Estimate at Completion with confidence intervals)
3. **Expense Optimization** (Value engineering opportunities)
4. **Financial Reporting** (CFO-ready dashboard)
5. **Risk Assessment** (Budget risks with probability/impact)
6. **Corrective Actions** (Immediate steps to control overruns)
```text

### Expected Output

The AI returns a structured budget control report with EVM metrics, variance tables, cost forecasts, optimisation recommendations, risk assessment, and specific corrective actions you can review with your CFO or steering committee.

---

## Tips

- **Track CPI Weekly**: Cost Performance Index below 0.85 is a leading indicator of budget disaster. Escalate immediately if CPI drops below 0.80.
- **Lock Vendors Early**: 60% of budget overruns come from vendor price volatility. Get fixed-price POs signed ASAP.
- **Protect Contingency Reserve**: Don't tap contingency for "nice-to-haves." Reserve it for true unknowns (e.g., asbestos, structural issues).
- **Value Engineering Before Scope Cuts**: VE-01 (AV simplification) saves $50K without eliminating functionality. Always try VE before cutting scope.
- **Communicate Overruns Early**: CFOs hate surprises. Flag a 10% overrun in Month 8, not Month 11 when it's unfixable.
- **Use EVM Metrics**: CPI and SPI give early warning signals. A project can be "on time" but financially doomed if CPI is 0.70.

---

## Related Prompts

- **[risk-management-analyst](./risk-management-analyst.md)** - For budget risk assessment
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - For CFO budget briefings

