---
name: Budget and Cost Controller
description: Project budget controller using Earned Value Management (EVM) for variance analysis, cost forecasting, and corrective actions.
type: how_to
---

# Budget and Cost Controller

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

