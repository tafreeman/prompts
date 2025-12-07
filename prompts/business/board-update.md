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
```

## Variables

- `[company]`: Company name and brief context
- `[period]`: Reporting period (e.g., "November 2024", "Q3 2024")
- `[metrics]`: Key performance metrics and targets
- `[highlights]`: Major wins and accomplishments
- `[challenges]`: Issues, risks, and concerns
- `[asks]`: Decisions or input needed from the board
- `[audience]`: Board composition and any specific context

---

## Example Usage

**Input:**

```text
Company: TechFlow - Series B enterprise SaaS company, workflow automation platform
Period: November 2024 (monthly update)
Key Metrics:
- ARR: $12.4M (target: $12.8M) - 97% of target
- Net Revenue Retention: 118%
- New Logos: 8 (target: 10)
- Burn: $890K (budget: $950K)
- Runway: 22 months
Highlights:
- Closed Fortune 500 deal (Acme Corp) - $480K ACV, largest deal ever
- Launched AI features, 40% of users adopted in first 2 weeks
- Engineering shipped 23% faster after process improvements
- NPS increased from 42 to 51
Challenges:
- Pipeline coverage dropped to 2.1x (target: 3x) - concerning for Q1
- Lost 2 senior engineers to FAANG companies
- Enterprise sales cycle lengthening (now 120 days avg, was 90)
Asks:
- Approve $200K budget increase for sales team expansion (2 AEs)
- Board input on whether to pursue partnership with Microsoft
- Intro requests: Need intros to procurement at 3 target accounts
Audience: 5-person board (2 VCs, 2 independents, CEO). Monthly update format they prefer.
```

**Output:**

```markdown
# TechFlow Board Update: November 2024

**Prepared by**: [CEO Name]  
**Date**: December 2, 2024  
**Next Board Meeting**: December 15, 2024

---

## Executive Summary

November was a **mixed month** for TechFlow. We landed our largest deal ever (Acme Corp, $480K ACV) and saw strong early adoption of our AI features, but we're tracking 97% to ARR target with pipeline coverage at concerning levels heading into Q1. Our burn came in under budget, and runway remains healthy at 22 months.

The Acme win validates our enterprise motion, but we're seeing sales cycle elongation that needs attention. I'm requesting board approval for a $200K investment in sales capacity to address pipeline concerns, and I'd value your input on a potential Microsoft partnership opportunity before we proceed further.

**Overall Assessment**: On track but watchful. Execution is strong; market headwinds require proactive response.

---

## Key Metrics Dashboard

| Metric | November | Target | vs. Target | vs. October | Trend |
|--------|----------|--------|------------|-------------|-------|
| **ARR** | $12.4M | $12.8M | 97% ⚠️ | +$380K | ↑ |
| **Net Revenue Retention** | 118% | 115% | ✅ +3pts | +2pts | ↑ |
| **New Logos** | 8 | 10 | 80% ⚠️ | -2 | ↓ |
| **Pipeline Coverage (Q1)** | 2.1x | 3.0x | 70% 🔴 | -0.4x | ↓ |
| **Monthly Burn** | $890K | $950K | ✅ Under | -$30K | → |
| **Cash Position** | $19.6M | — | — | -$890K | → |
| **Runway** | 22 months | 18+ mo | ✅ | — | → |
| **NPS** | 51 | 50 | ✅ +1pt | +9pts | ↑ |

**Commentary**:
- ARR miss driven by 2 deals slipping to December (signed Dec 1, will appear in next update)
- Pipeline coverage is the key concern - addressed in Challenges section
- NPS jump reflects AI feature launch satisfaction

---

## Highlights & Wins 🎉

### 1. Acme Corp Closed: $480K ACV (Largest Deal Ever)
Fortune 500 manufacturer signed 3-year enterprise agreement. This validates:
- Our ability to compete in true enterprise ($500K+ deals)
- Security/compliance positioning resonating with regulated industries
- Land-and-expand playbook working (started as $80K pilot in Q2)

**Quote from Acme CIO**: *"TechFlow reduced our workflow approval time from 5 days to 4 hours."*

### 2. AI Features Launch: 40% Adoption in 2 Weeks
Released AI-powered workflow suggestions and auto-tagging. Adoption exceeded expectations:
- 40% of active users engaged with AI features (target was 25%)
- Early signal: AI users have 2x session length
- Zero critical bugs in launch (engineering's best release ever)

### 3. Engineering Velocity: 23% Improvement
Process changes implemented in October (smaller PRs, async standups) yielded measurable results:
- Cycle time reduced from 6.2 days to 4.8 days
- Deployment frequency up 35%
- Team morale survey: "Engineering processes" score improved from 3.2 → 4.1/5

### 4. Customer Satisfaction: NPS 42 → 51
Driven by:
- AI feature satisfaction
- Improved support response times (now <2 hours avg)
- Proactive customer success outreach program

---

## Challenges & Risks ⚠️

### 1. Pipeline Coverage at 2.1x (Target: 3x) 🔴

**What's happening**: Q1 pipeline is $2.6M against a $1.2M target. We need $3.6M for comfortable coverage.

**Root causes**:
- 2 senior AEs ramping slower than expected
- Outbound response rates dropped 15% (market fatigue? messaging?)
- Marketing events underperformed in October

**Mitigation actions**:
- Hired SDR manager (starts Dec 9) to improve outbound quality
- Refreshing outbound messaging with new AI positioning
- Accelerating 2 deals from Q2 pipeline into Q1

**Ask**: Requesting $200K budget increase for 2 additional AEs (see Asks section)

### 2. Senior Engineering Attrition

**What's happening**: Lost 2 senior engineers (1 to Meta, 1 to Stripe) in November.

**Impact**: 
- Short-term: Q1 roadmap at risk without backfill
- Long-term: Compensation may not be competitive at L5+

**Mitigation**:
- 2 candidates in final rounds (expecting offers this week)
- Reviewing compensation bands for senior roles (HR analysis due Dec 15)
- Retention conversations with remaining senior ICs

### 3. Enterprise Sales Cycle Lengthening

**What's happening**: Average sales cycle now 120 days (was 90 in Q2).

**Hypothesis**: 
- Larger deal sizes require more stakeholders
- Economic uncertainty making buyers cautious
- Security reviews taking longer

**Response**:
- Accelerating security certifications (ISO 27001 in progress)
- Creating ROI calculator to speed business case approval
- Piloting "executive sponsor" program for deals >$200K

---

## Strategic Update

### Q4 OKR Progress

| Objective | Key Result | Status | Notes |
|-----------|------------|--------|-------|
| **Hit $13.5M ARR** | $12.4M / $13.5M | 🟡 92% | Achievable if Dec deals close |
| **Launch AI Platform** | ✅ Shipped | 🟢 Done | Ahead of schedule |
| **Enterprise Expansion** | 3 F500 logos (Acme = 1) | 🟡 33% | 2 in late-stage pipeline |
| **Improve NPS to 50** | 51 achieved | 🟢 Done | Exceeded target |

### Strategic Initiatives Status

**1. Microsoft Partnership** *(seeking board input)*
- Microsoft reached out about potential Copilot integration
- Would accelerate enterprise distribution but requires 3-month eng investment
- Detailed analysis in Appendix A - recommend discussing at Dec 15 board meeting

**2. International Expansion**
- UK entity formation complete
- First UK AE starts January 6
- Pipeline: 4 qualified UK opportunities ($320K total)

---

## Financial Summary

| Metric | November | YTD | vs. Plan |
|--------|----------|-----|----------|
| Revenue | $1.08M | $10.2M | 96% |
| Gross Margin | 82% | 81% | +1pt |
| Operating Expenses | $1.97M | $19.8M | 94% |
| Net Burn | $890K | $9.6M | Under budget |
| Cash Balance | $19.6M | — | Healthy |

**Runway**: 22 months at current burn. If we increase burn by $200K/mo (sales expansion), runway = 18 months, still within policy.

---

## Asks & Decisions Needed

### 1. APPROVAL: $200K Budget Increase for Sales Expansion 🔴

**Request**: Approve $200K incremental budget for H1 2025 to hire 2 additional Account Executives.

**Rationale**:
- Pipeline coverage at 2.1x is unacceptable risk
- Current AE team at capacity; adding headcount is fastest lever
- Each AE expected to generate $800K-$1M ARR at steady state
- Payback: <12 months based on current metrics

**Impact on Runway**: Reduces from 22 → 18 months (still within policy)

**Recommendation**: Approve. Detailed business case in Appendix B.

---

### 2. INPUT: Microsoft Partnership Decision

**Context**: Microsoft approached us about integrating TechFlow into Copilot ecosystem.

**Opportunity**: Access to Microsoft's enterprise distribution, co-sell motions, marketplace listing
**Investment**: ~3 months of engineering, $100K in integration costs
**Risk**: Dependency on Microsoft platform; potential future competition

**Ask**: Would like board input on whether to pursue. Recommend 15-min discussion at December meeting.

---

### 3. INTRO REQUESTS

Seeking warm introductions to procurement/IT at:
1. **Delta Airlines** - Sarah, do you know their CIO from your time at [Company]?
2. **Walgreens** - Marcus, I believe you have a board connection here?
3. **Goldman Sachs** - Any paths in through your networks?

---

## Looking Ahead: December Priorities

1. **Close Q4 strong**: 3 deals totaling $680K in commit stage; all must close
2. **Rebuild pipeline**: SDR manager onboarding, outbound refresh
3. **Backfill engineering**: Extend offers to 2 senior candidates
4. **Microsoft decision**: Present analysis at Dec 15 board meeting

### December Board Meeting Agenda (Dec 15)
- 2025 Annual Plan Review (60 min)
- Microsoft Partnership Discussion (15 min)
- Compensation Analysis: Engineering Retention (15 min)
- Closed Session (30 min)

---

## Appendices

- **Appendix A**: Microsoft Partnership Analysis (5 pages)
- **Appendix B**: Sales Expansion Business Case (3 pages)
- **Appendix C**: Full Financial Statements
- **Appendix D**: Product Roadmap Update

---

*Questions before the board meeting? Email me directly or drop in #board-updates Slack channel.*

— [CEO Name]
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
