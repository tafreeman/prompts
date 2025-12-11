---
title: "Pitch Deck Generator"
shortTitle: "Pitch Deck"
intro: "Generate compelling pitch deck outlines and content for investor presentations, sales pitches, and business proposals."
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
  - "sales"
  - "presentations"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Pitch Deck Generator

---

## Description

Create structured, persuasive pitch deck content for investor meetings, sales presentations, and business proposals. Generates slide-by-slide content with key messaging, data points, and visual recommendations.

---

## Use Cases

- Startup fundraising presentations for seed/Series A rounds
- Sales team pitch decks for enterprise deals
- Internal business case presentations to leadership
- Product launch presentations to stakeholders
- Partnership proposal decks

---

## Prompt

```text
You are an expert pitch deck consultant who has helped startups raise millions in funding.

Create a pitch deck outline for:

**Company/Product**: [company_name]
**Pitch Type**: [pitch_type]
**Target Audience**: [audience]
**Key Value Proposition**: [value_prop]
**Supporting Data**: [data_points]
**Ask/Goal**: [ask]

Generate a complete pitch deck with:

1. **Slide-by-Slide Content**
   - Title slide with tagline
   - Problem slide (pain points, market gap)
   - Solution slide (your product/approach)
   - Market opportunity (TAM/SAM/SOM)
   - Business model (revenue streams)
   - Traction slide (metrics, milestones)
   - Competitive advantage (moat, differentiation)
   - Team slide (key players, credibility)
   - Financial projections (3-year outlook)
   - The Ask (investment amount, use of funds)
   - Closing slide (contact, next steps)

2. **For Each Slide Include**:
   - Headline (one powerful statement)
   - 3-4 bullet points max
   - Suggested visual/chart type
   - Speaker notes (what to emphasize verbally)

3. **Storytelling Arc**:
   - Hook (attention-grabbing opener)
   - Build (escalate the problem)
   - Reveal (your solution)
   - Proof (evidence it works)
   - Vision (where you're going)
   - Call to action

Format output as a structured deck outline with clear slide separators.
```text

---

## Variables

- `[company_name]`: Company or product name and brief description
- `[pitch_type]`: Type of pitch (e.g., "Series A fundraise", "Enterprise sales", "Partnership proposal")
- `[audience]`: Target audience (e.g., "VC investors at growth stage firms", "CTO buyers at Fortune 500")
- `[value_prop]`: Core value proposition in one sentence
- `[data_points]`: Key metrics, traction data, market research to include
- `[ask]`: What you're asking for (e.g., "$5M Series A at $25M pre-money", "Annual contract at $500K ARR")

---

## Example Usage

**Input:**

```text
Company/Product: CloudSync - B2B SaaS platform that automates data synchronization across enterprise systems
Pitch Type: Series A fundraise ($8M raise)
Target Audience: Enterprise SaaS VCs (Bessemer, Battery, Accel)
Key Value Proposition: Reduce enterprise data integration time from 6 months to 6 days
Supporting Data: 
- 45 enterprise customers (including 3 Fortune 500)
- $2.1M ARR, growing 15% MoM
- NPS: 72
- Average contract value: $48K/year
Ask: $8M Series A at $40M pre-money valuation
```text

---

## Tips

- Lead with the problem, not your solution - investors invest in markets, not products
- Use concrete numbers wherever possible - "$2.1M ARR" beats "strong revenue growth"
- Keep slides visual - no more than 4 bullets, let speaker notes carry the story
- Practice the 10-minute version - most investor meetings run short on time
- Have backup slides ready for deep-dive questions on financials, competition, and tech

---

## Related Prompts

- [client-presentation-designer](./client-presentation-designer.md) - For non-fundraising presentations
- [business-strategy-analysis](./business-strategy-analysis.md) - For market analysis underlying your deck
- [stakeholder-communication-manager](./stakeholder-communication-manager.md) - For investor update communications
