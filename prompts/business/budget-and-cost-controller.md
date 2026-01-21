---
name: Budget and Cost Controller
description: Project budget controller using Earned Value Management (EVM) for variance analysis, cost forecasting, and corrective actions.
type: how_to
---

# Budget and Cost Controller

## Description

This prompt serves as a project budget controller using Earned Value Management (EVM) for variance analysis, cost forecasting, and corrective action planning. It helps project managers and finance teams maintain budget discipline and proactively address cost overruns.

## Use Cases

- Capital project budget tracking (construction, office moves, infrastructure)
- IT implementation financial management
- Budget variance reporting to CFO/steering committees
- Cost optimization and value engineering
- Monthly financial close processes

## Variables

- `[project_name]`: Project name and scope (e.g., "HQ Office Relocation - 500-person facility")
- `[budget]`: Total approved budget (e.g., "$2.5M CapEx + $150K contingency")
- `[current_spend]`: Actual spend to date (e.g., "$1.8M (72% of budget), Month 8 of 12")
- `[timeline]`: Project timeline context (e.g., "Month 8 of 12 (66% elapsed), Go-Live Feb 1")
- `[concerns]`: Specific cost issues (e.g., "Furniture 20% over estimate due to supply chain surcharges, IT cabling bids pending")

## Prompt

### System Prompt

```text
You are an expert project financial controller with deep experience in Earned Value Management (EVM), capital project budgeting, and cost optimization. You help organizations maintain budget discipline through proactive variance analysis, forecasting, and corrective action planning.
```

### User Prompt

```text
Analyze the budget status for [project_name].

Budget Context:
- Total Budget: [budget]
- Current Spend: [current_spend]
- Timeline: [timeline]
- Concerns: [concerns]

Please provide:
1. Earned Value Analysis (CPI, SPI, EAC, VAC)
2. Variance analysis with root causes
3. Cost forecast to completion
4. Recommended corrective actions prioritized by impact
5. Risk-adjusted contingency assessment
6. Executive summary for steering committee
```

## Example

### Input

```text
Analyze the budget status for HQ Office Relocation - 500-person facility.

Budget Context:
- Total Budget: $2.5M CapEx + $150K contingency
- Current Spend: $1.8M (72% of budget), Month 8 of 12
- Timeline: Month 8 of 12 (66% elapsed), Go-Live Feb 1
- Concerns: Furniture 20% over estimate due to supply chain surcharges, IT cabling bids pending
```

### Expected Output

```text
## Budget Analysis: HQ Office Relocation

### Earned Value Summary
| Metric | Value | Status |
|--------|-------|--------|
| Budget at Completion (BAC) | $2.65M | - |
| Planned Value (PV) | $1.75M | 66% elapsed |
| Earned Value (EV) | $1.65M | 62% complete |
| Actual Cost (AC) | $1.8M | 72% spent |
| Cost Performance Index (CPI) | 0.92 | ⚠️ Below 1.0 |
| Schedule Performance Index (SPI) | 0.94 | ⚠️ Slightly behind |
| Estimate at Completion (EAC) | $2.88M | $230K over budget |

### Variance Analysis
1. **Furniture (+$80K)**: Supply chain surcharges from delayed shipments
2. **IT Cabling (TBD)**: Bids pending - risk of additional $50K
3. **Labor Overtime (+$30K)**: Compressed timeline driving OT

### Corrective Actions
| Action | Savings | Timeline | Owner |
|--------|---------|----------|-------|
| VE-01: Simplify AV setup | $50K | Week 1 | Facilities |
| VE-02: Standard vs custom furniture | $35K | Week 2 | Procurement |
| Negotiate IT fixed-price | $20K | Week 1 | IT Director |

### Executive Summary
Project tracking $230K over budget (8.7%). CPI of 0.92 indicates cost efficiency issues. Recommend immediate VE review and CFO briefing on contingency drawdown.
```

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

