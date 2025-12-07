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
```

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
```

**Output:**

```markdown
# CloudSync Pitch Deck: Series A

---

## Slide 1: Title

**Headline**: CloudSync - Enterprise Data Integration in Days, Not Months

**Subheadline**: The modern data fabric for enterprise systems

**Visual**: Logo + clean product screenshot showing connected systems

**Speaker Notes**: "Thank you for your time today. I'm [Name], CEO of CloudSync. We're solving one of the most painful problems in enterprise IT."

---

## Slide 2: The Problem

**Headline**: Enterprise Data Integration is Broken

**Bullets**:
- Average enterprise uses 1,295 cloud apps (Okta 2024)
- Data integration projects take 6-18 months average
- 70% of integration projects fail or exceed budget
- Data silos cost Fortune 500s $12.9M annually (IDC)

**Visual**: Diagram showing tangled web of disconnected systems

**Speaker Notes**: "Every enterprise CIO I talk to has the same nightmare - their data is trapped in silos. Integration projects are career-ending. The average Fortune 500 spends millions trying to connect their systems."

---

## Slide 3: Our Solution

**Headline**: CloudSync: 6 Months → 6 Days

**Bullets**:
- No-code visual data mapping interface
- Pre-built connectors for 200+ enterprise systems
- Real-time bi-directional sync (not batch)
- Enterprise-grade security (SOC 2 Type II, HIPAA)

**Visual**: Before/after: tangled wires → clean connected diagram

**Speaker Notes**: "CloudSync makes enterprise integration as easy as consumer apps. Our customers go live in days, not months. No consultants, no custom code, no $10M implementation fees."

---

## Slide 4: Market Opportunity

**Headline**: $50B+ Market Growing 25% CAGR

**Bullets**:
- **TAM**: $52B global data integration market (2025)
- **SAM**: $18B enterprise iPaaS segment
- **SOM**: $2.4B mid-market enterprise (our beachhead)
- Growing 25% CAGR through 2028 (Gartner)

**Visual**: Expanding concentric circles showing TAM/SAM/SOM

**Speaker Notes**: "The iPaaS market is massive and growing. We're focused on the mid-market enterprise segment where the pain is acute but budgets are real."

---

## Slide 5: Business Model

**Headline**: Land & Expand SaaS Model

**Bullets**:
- Annual subscription: $36K-$150K ACV
- Usage-based expansion (data volume tiers)
- 140% net revenue retention
- <6 month payback on CAC

**Visual**: Revenue growth chart showing expansion within accounts

**Speaker Notes**: "We land with a single integration use case, then expand across the organization. Our top customer started at $40K and is now at $180K ARR."

---

## Slide 6: Traction

**Headline**: Proven Product-Market Fit

**Bullets**:
- **45 Enterprise Customers** (3 Fortune 500)
- **$2.1M ARR** - 15% MoM growth
- **NPS: 72** - Best in category
- **0% logo churn** last 12 months

**Visual**: ARR growth chart (hockey stick), customer logos

**Speaker Notes**: "We're not pre-revenue anymore. We have real enterprise customers paying real money. Our NPS of 72 is exceptional for enterprise software."

---

## Slide 7: Competitive Advantage

**Headline**: Why We Win

**Bullets**:
- **Speed**: 50x faster deployment than MuleSoft
- **Cost**: 80% lower TCO than legacy platforms
- **Modern**: Built cloud-native (not legacy acquired)
- **Moat**: 200+ pre-built connectors (18-month head start)

**Visual**: Competitive matrix showing CloudSync vs. MuleSoft, Informatica, Boomi

**Speaker Notes**: "MuleSoft was bought by Salesforce for $6.5B but their product is 15 years old. We're the modern alternative purpose-built for today's cloud-first enterprises."

---

## Slide 8: Team

**Headline**: Built by Enterprise Integration Veterans

**Bullets**:
- **CEO**: 15 years at MuleSoft (VP Engineering, took them public)
- **CTO**: Ex-Snowflake, scaled data platform to $1B ARR
- **VP Sales**: Grew Segment enterprise from $5M to $80M ARR
- **Advisors**: Former CIOs of Adobe, Workday, ServiceNow

**Visual**: Team photos with logos of previous companies

**Speaker Notes**: "We've done this before. Our team built and scaled MuleSoft and Segment. We know the playbook."

---

## Slide 9: Financial Projections

**Headline**: Path to $50M ARR by 2027

| Metric | 2025 | 2026 | 2027 |
|--------|------|------|------|
| ARR | $2.1M | $8M | $25M |
| Customers | 45 | 150 | 400 |
| Gross Margin | 78% | 82% | 85% |
| Team Size | 25 | 60 | 120 |

**Visual**: Revenue projection chart with customer count overlay

**Speaker Notes**: "With this round, we'll hit $8M ARR by end of next year and $25M by 2027. We're targeting 3x growth annually."

---

## Slide 10: The Ask

**Headline**: $8M Series A to Scale Go-To-Market

**Use of Funds**:
- **50%**: Sales & Marketing (grow from 5 → 20 AEs)
- **30%**: Engineering (expand connector library)
- **20%**: G&A and buffer

**Milestones**:
- 150 customers by end of Year 1
- $8M ARR by Q4 2026
- Series B ready at $15M+ ARR

**Visual**: Pie chart of fund allocation

**Speaker Notes**: "We're raising $8M at a $40M pre-money valuation. This gets us to Series B metrics with 24 months runway."

---

## Slide 11: Closing

**Headline**: Join Us in Building the Data Fabric for Every Enterprise

**Next Steps**:
- Deep-dive product demo (30 min)
- Customer references available
- Data room access upon request

**Contact**: 
- [CEO Name] - ceo@cloudsync.io
- [Website] - cloudsync.io/investors

**Speaker Notes**: "Thank you for your time. We'd love to show you the product and connect you with customers. What questions do you have?"

---

## Appendix Slides (Backup)

- Detailed competitive analysis matrix
- Customer case study: Fortune 500 deployment
- Technical architecture diagram
- Full financials and unit economics
- Team bios with LinkedIn links
```

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
