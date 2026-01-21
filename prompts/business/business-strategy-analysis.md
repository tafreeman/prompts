---
name: Business Strategy Analysis
description: Comprehensive business strategy analyzer for evaluating strategic options, SWOT analysis, and actionable recommendations.
type: how_to
---

# Business Strategy Analysis

## Description

This prompt provides comprehensive business strategy analysis for evaluating strategic options, conducting SWOT analysis, and developing actionable recommendations. It helps executives and strategists make data-driven decisions about market positioning, competitive dynamics, and growth opportunities.

## Use Cases

- Evaluate new business opportunities or market entries
- Analyze competitive positioning and market dynamics
- Support strategic planning sessions and workshops
- Conduct SWOT analysis for specific initiatives
- Make data-driven strategic decisions

## Variables

- `[COMPANY NAME]`: Organization name (e.g., "Acme Software Inc.")
- `[INDUSTRY]`: Industry sector (e.g., "B2B SaaS", "Healthcare Technology")
- `[BRIEF DESCRIPTION OF CURRENT STATE]`: Current business situation (e.g., "Growing 30% YoY with strong SMB base, considering enterprise expansion")
- `[WHAT YOU'RE TRYING TO DECIDE OR ACHIEVE]`: Strategic question or goal (e.g., "Should we move upmarket to mid-market and enterprise?")
- `[SMALL/MEDIUM/LARGE/ENTERPRISE]`: Company size category
- `[LEADER/CHALLENGER/FOLLOWER/NICHE]`: Market position
- `[LIST MAIN COMPETITORS]`: Key competitors (e.g., "Salesforce, HubSpot, Pipedrive")
- `[ANY RELEVANT BUDGET LIMITATIONS]`: Budget constraints (e.g., "$2M total investment available over 18 months")

## Prompt

### System Prompt

```text
You are a senior strategy consultant with expertise in competitive analysis, market dynamics, and strategic planning. You help organizations evaluate strategic options and develop actionable recommendations using proven frameworks like SWOT, Porter's Five Forces, and Blue Ocean Strategy.
```

### User Prompt

```text
Conduct a strategic analysis for [COMPANY NAME] in the [INDUSTRY] industry.

Context:
- Current State: [BRIEF DESCRIPTION OF CURRENT STATE]
- Strategic Question: [WHAT YOU'RE TRYING TO DECIDE OR ACHIEVE]
- Company Size: [SMALL/MEDIUM/LARGE/ENTERPRISE]
- Market Position: [LEADER/CHALLENGER/FOLLOWER/NICHE]
- Key Competitors: [LIST MAIN COMPETITORS]
- Budget Constraints: [ANY RELEVANT BUDGET LIMITATIONS]

Please provide:
1. SWOT analysis
2. Competitive positioning assessment
3. Strategic options with pros/cons
4. Recommended strategy with rationale
5. Implementation priorities
6. Key success metrics
```

## Example

### Input

```text
Conduct a strategic analysis for Acme Software Inc. in the B2B SaaS industry.

Context:
- Current State: Growing 30% YoY with strong SMB base, considering enterprise expansion
- Strategic Question: Should we move upmarket to mid-market and enterprise?
- Company Size: Medium (150 employees)
- Market Position: Challenger
- Key Competitors: Salesforce, HubSpot, Pipedrive
- Budget Constraints: $2M total investment available over 18 months
```

### Expected Output

```text
## Strategic Analysis: Acme Software Inc.

### SWOT Analysis

| Strengths | Weaknesses |
|-----------|------------|
| 30% YoY growth | No enterprise sales team |
| Strong SMB product-market fit | Limited feature parity with Salesforce |
| Efficient CAC ($800 vs industry $1200) | Single product dependency |

| Opportunities | Threats |
|---------------|----------|
| Enterprise segment 3x larger TAM | Salesforce downmarket moves |
| Integration partnerships | Funding winter limiting runway |
| AI feature differentiation | HubSpot free tier pressure |

### Strategic Options

| Option | Pros | Cons | Risk |
|--------|------|------|------|
| A: Enterprise Push | Higher ACV, 3x TAM | Long sales cycles, high CAC | High |
| B: SMB Deepening | Lower risk, faster wins | Limited TAM, price pressure | Low |
| C: Hybrid Approach | Balanced growth | Resource dilution | Medium |

### Recommendation: Option C - Phased Hybrid
1. **Phase 1 (6 mo)**: Build enterprise-ready features using SMB revenue
2. **Phase 2 (12 mo)**: Hire 2 enterprise AEs, test with 10 accounts
3. **Phase 3 (18 mo)**: Scale enterprise if CAC payback < 18 months

### Key Success Metrics
- Enterprise pilot close rate > 20%
- CAC payback < 18 months
- Net Revenue Retention > 110%
```

## Related Prompts

- [Competitive Analysis Framework](./competitive-analysis.md) - For detailed competitive intelligence
- [Competitive Analysis Researcher](../analysis/competitive-analysis-researcher.md) - For in-depth competitor research
- [Market Research Analyst](../analysis/market-research-analyst.md) - For market insights and trends
- [Industry Analysis Expert](../analysis/industry-analysis-expert.md) - For industry-level strategic analysis
- [Risk Management Analyst](./risk-management-analyst.md) - For strategic risk assessment
