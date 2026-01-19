---
title: "Board Update Generator"
shortTitle: "Board Update"
intro: "Generate professional board updates and investor communications with key metrics, highlights, and strategic context."
type: "how_to"
difficulty: "intermediate"
audience:

  - "business-analyst"
  - "project-manager"

platforms:

  - "github-copilot"
  - "claude"
  - "chatgpt"

topics:

  - "executive-communication"
  - "investor-relations"
  - "strategy"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Board Update Generator

---

## Description

Create polished board updates and investor communications that clearly convey company performance, strategic progress, and key decisions needed. Balances transparency with appropriate framing.

---

## Use Cases

- Monthly or quarterly board updates
- Investor email communications
- Pre-board meeting briefing documents
- Year-end shareholder letters
- Strategic update memos to stakeholders

---

## Prompt

```text
You are an experienced executive who writes clear, professional board communications.

Create a board update for:

**Company**: [company]
**Period**: [period]
**Key Metrics**: [metrics]
**Highlights**: [highlights]
**Challenges**: [challenges]
**Asks/Decisions Needed**: [asks]
**Audience**: [audience]

Generate:

1. **Executive Summary** (5-6 sentences)
   - Overall performance assessment
   - Key wins and concerns
   - Strategic trajectory

2. **Key Metrics Dashboard**
   - Actual vs. target vs. prior period
   - Trend indicators (↑↓→)
   - Brief commentary on variances

3. **Highlights & Wins**
   - Top 3-5 accomplishments
   - Impact and significance
   - Customer or market wins

4. **Challenges & Risks**
   - Honest assessment of headwinds
   - Mitigation actions underway
   - Where you need board input

5. **Strategic Update**
   - Progress on OKRs/annual goals
   - Key initiatives status
   - Any strategic pivots or adjustments

6. **Financial Summary**
   - Revenue/burn/runway highlights
   - Cash position
   - Forecast vs. actual

7. **Asks & Decisions**
   - Specific requests of the board
   - Decisions that need approval
   - Input being sought

8. **Looking Ahead**
   - Next period priorities
   - Key milestones to watch
   - Upcoming board agenda items

Write in confident but honest tone. No spin, but appropriate framing. Board members are time-constrained - be concise.
```text

---

## Variables

- `[company]`: Company name and brief context
- `[period]`: Reporting period (e.g., "November 2024", "Q3 2024")
- `[metrics]`: Key performance metrics and targets
- `[highlights]`: Major wins and accomplishments
- `[challenges]`: Issues, risks, and concerns
- `[asks]`: Decisions or input needed from the board
- `[audience]`: Board composition and any specific context

---

## Example

### Context

You are the CEO of a Series B SaaS company preparing a monthly board update. Growth is solid but slightly below target, and you need to communicate key metrics, wins, challenges, and specific asks clearly.

### Input

```text
You are an experienced executive who writes clear, professional board communications.

Create a board update for:

**Company**: TechFlow - Series B enterprise SaaS company, workflow automation platform
**Period**: November 2024 (monthly update)
**Key Metrics**:

- ARR: $12.4M (target: $12.8M) - 97% of target
- Net Revenue Retention: 118%
- New Logos: 8 (target: 10)
- Burn: $890K (budget: $950K)
- Runway: 22 months

**Highlights**:

- Closed Fortune 500 deal (Acme Corp) - $480K ACV, largest deal ever
- Launched AI features, 40% of users adopted in first 2 weeks
- Engineering shipped 23% faster after process improvements
- NPS increased from 42 to 51

**Challenges**:

- Pipeline coverage dropped to 2.1x (target: 3x) - concerning for Q1
- Lost 2 senior engineers to FAANG companies
- Enterprise sales cycle lengthening (now 120 days avg, was 90)

**Asks/Decisions Needed**:

- Approve $200K budget increase for sales team expansion (2 AEs)
- Board input on whether to pursue partnership with Microsoft
- Intro requests: Need intros to procurement at 3 target accounts

**Audience**: 5-person board (2 VCs, 2 independents, CEO). Monthly update format they prefer.

Generate the board update structure and content as specified in the prompt.
```text

### Expected Output

The AI produces a polished board update structured into: executive summary, key metrics dashboard, highlights and wins, challenges and risks, strategic update, financial summary, specific asks/decisions, and a "looking ahead" section, written in a concise, board‑friendly tone.

---

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
