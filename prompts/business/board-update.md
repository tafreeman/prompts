---
name: Board Update Generator
description: Generate professional board updates and investor communications with key metrics, highlights, and strategic context.
type: how_to
---

# Board Update Generator

## Description

This prompt generates professional board updates and investor communications that effectively convey key metrics, highlights, and strategic context. It helps executives create clear, concise updates that maintain board confidence while being transparent about challenges and asks.

## Use Cases

- Monthly or quarterly board updates
- Investor email communications
- Pre-board meeting briefing documents
- Year-end shareholder letters
- Strategic update memos to stakeholders

## Variables

- `[company]`: Company name and brief context
- `[period]`: Reporting period (e.g., "November 2024", "Q3 2024")
- `[metrics]`: Key performance metrics and targets
- `[highlights]`: Major wins and accomplishments
- `[challenges]`: Issues, risks, and concerns
- `[asks]`: Decisions or input needed from the board
- `[audience]`: Board composition and any specific context

## Prompt

### System Prompt

```text
You are an experienced executive communications specialist who helps CEOs and founders craft compelling board updates. You understand investor psychology, governance best practices, and how to present both wins and challenges in a way that maintains confidence while being transparent.
```

### User Prompt

```text
Generate a board update for [company] covering [period].

Context:
- Key Metrics: [metrics]
- Highlights: [highlights]
- Challenges: [challenges]
- Board Asks: [asks]
- Audience: [audience]

Please create a professional board update that:
1. Opens with an executive summary (3-4 sentences)
2. Presents key metrics with context and trends
3. Highlights major wins with business impact
4. Addresses challenges honestly with mitigation plans
5. Clearly states any asks or decisions needed from the board
6. Closes with forward-looking outlook
```

## Example

### Input

```text
Generate a board update for TechFlow Inc covering November 2024.

Context:
- Key Metrics: ARR $4.2M (up 18% QoQ), NRR 112%, CAC Payback 14 months
- Highlights: Closed 3 enterprise deals including Fortune 500 logo, launched V2.0 platform
- Challenges: Engineering velocity down 20% due to tech debt, missed hiring target by 2 heads
- Board Asks: Approve $500K budget increase for infrastructure modernization
- Audience: 5-person board including 2 VCs, 2 independents, CEO
```

### Expected Output

```text
## TechFlow Inc. - November 2024 Board Update

### Executive Summary
Strong revenue month with 18% QoQ ARR growth driven by enterprise expansion. Landed our first Fortune 500 customer (Acme Corp). Engineering velocity challenges require immediate attention - requesting infrastructure investment approval.

### Key Metrics
| Metric | November | vs. Target | Trend |
|--------|----------|------------|-------|
| ARR | $4.2M | +8% | ↑ |
| NRR | 112% | +2% | ↑ |
| CAC Payback | 14 mo | On target | → |

### Highlights
- **Enterprise Breakthrough**: Closed Acme Corp ($180K ACV) - first Fortune 500 logo
- **Product Launch**: V2.0 shipped on schedule with 95% positive user feedback
- **Expansion Revenue**: 3 upsells totaling $85K incremental ARR

### Challenges & Mitigation
- **Engineering Velocity**: Down 20% due to accumulated tech debt
  - *Mitigation*: Proposing dedicated sprint for infrastructure modernization
- **Hiring Gap**: 2 heads short on engineering target
  - *Mitigation*: Engaging specialized recruiting firm, pipeline building

### Board Ask
Approval requested for $500K infrastructure modernization budget to address tech debt and restore engineering velocity. Expected ROI: 40% velocity improvement within 90 days.

### Outlook
On track for $5M ARR by Q1 with current pipeline. Enterprise momentum strong.
```

## Tips

- Lead with the headline: good news or bad news first, don't bury it
- Be honest about challenges - boards respect transparency over spin
- Make asks specific and actionable - "need help" isn't an ask
- Include context for metrics - numbers without narrative are confusing
- Keep it under 3 pages for monthly updates; save details for appendices

---

## Related Prompts

- [meeting-summary](./meeting-summary.md) - For summarizing board meeting outcomes
- [pitch-deck-generator](./pitch-deck-generator.md) - For investor presentations
- [business-strategy-analysis](./business-strategy-analysis.md) - For strategic planning underlying updates
