---

title: "Competitive Intelligence Researcher"
category: "analysis"
tags: ["researcher", "competitive-intelligence", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Competitive Intelligence Researcher

## Description

Conduct comprehensive competitive intelligence research using structured frameworks (Porter's Five Forces, SWOT analysis) to gather actionable insights about competitors' strategies, products, market positioning, and vulnerabilities. This prompt helps researchers, strategists, and business analysts build data-driven competitive intelligence reports while maintaining ethical and legal boundaries.

## Use Cases

- Gathering pre-acquisition due diligence on target companies
- Monitoring competitor product roadmaps and feature releases
- Analyzing competitor pricing strategies and market positioning
- Identifying competitive threats and opportunities for strategic planning
- Building competitive landscapes for investor presentations
- Supporting sales teams with battle cards and competitive differentiators

## Prompt

```text
You are a senior competitive intelligence analyst with expertise in strategic analysis frameworks and ethical intelligence gathering.

**Intelligence Target:**
- Company: [company_name]
- Competitors to Analyze: [competitor_list]
- Intelligence Focus Areas: [focus_areas]
- Decision Context: [decision_context]

**Research Parameters:**
- Time Horizon: [time_horizon]
- Geographic Scope: [geographic_scope]
- Information Sensitivity Level: [sensitivity_level]

**Analysis Framework:**

Using publicly available information (company filings, press releases, news articles, job postings, patent databases, social media, customer reviews, analyst reports), provide:

1. **Intelligence Gathering Framework**
   - Primary data sources to prioritize
   - Secondary data sources for validation
   - Data collection methodology
   - Verification approach for claims

2. **Data Collection Strategy**
   - Key information to gather (product features, pricing, partnerships, hiring patterns, technology stack)
   - Monitoring cadence and triggers
   - Tools and platforms to leverage
   - Red flags for early warning signals

3. **Competitive Analysis**
   - Strengths and weaknesses assessment (SWOT)
   - Competitive positioning map
   - Product/feature comparison matrix
   - Pricing and go-to-market strategy analysis
   - Customer sentiment analysis

4. **Strategic Insights**
   - What are competitors doing well that we should learn from?
   - What vulnerabilities can we exploit?
   - What market gaps exist that neither we nor competitors address?
   - How are competitive dynamics shifting?

5. **Threat Assessment**
   - Immediate threats (0-6 months)
   - Medium-term concerns (6-18 months)
   - Long-term strategic risks (18+ months)
   - Likelihood and impact scoring (High/Medium/Low)

6. **Opportunity Identification**
   - Market opportunities competitors are missing
   - Potential partnership or acquisition targets
   - Underserved customer segments
   - Technology or capability gaps we can fill

**Ethical and Legal Boundaries:**
- Use ONLY publicly available information
- Do NOT recommend espionage, misrepresentation, or unethical tactics
- Cite sources for all major claims
- Flag any information that seems proprietary or confidential

**Output Format:**
Provide results as a structured Markdown report with executive summary, detailed findings by competitor, and actionable recommendations ranked by impact and feasibility.
```

## Variables

- `[company_name]`: Your company name (e.g., "Acme SaaS Inc.", "TechCorp Analytics")
- `[competitor_list]`: 2-5 competitors to research (e.g., "Salesforce, HubSpot, Zoho CRM")
- `[focus_areas]`: Specific intelligence priorities (e.g., "Product roadmap analysis", "Pricing strategies", "Market expansion plans", "Technology stack evolution", "Key personnel changes")
- `[decision_context]`: What this research will inform (e.g., "2025 product roadmap prioritization", "Series B pitch deck competitive positioning", "Market entry strategy for EMEA")
- `[time_horizon]`: Research time scope (e.g., "Last 12 months", "Q1-Q3 2024", "Past 5 years for trend analysis")
- `[geographic_scope]`: Market focus (e.g., "North America", "Global", "APAC region")
- `[sensitivity_level]`: Information handling (e.g., "Internal use only", "Board-level confidential", "Public-facing")

## Example Usage

**Input:**

```text
[company_name]: Acme SaaS (mid-market CRM platform)
[competitor_list]: Salesforce, HubSpot, Zoho CRM
[focus_areas]: Product roadmap intelligence (specifically AI/automation features), pricing model changes, partnership strategies
[decision_context]: Planning 2025 product roadmap and feature prioritization to maintain competitive differentiation
[time_horizon]: Last 18 months (Jan 2023 - Jun 2024)
[geographic_scope]: North America and Western Europe
[sensitivity_level]: Internal strategy team only, not for external distribution
```

**Output (Excerpt):**

```text
## Executive Summary

**Key Findings:**
- All three competitors have heavily invested in AI-powered automation (30+ features launched in 18 months)
- HubSpot has shifted to consumption-based pricing for AI features, creating revenue opportunity
- Salesforce announced 5 major acquisitions focused on customer data platforms
- Zoho is aggressively targeting SMB segment with 40% price reduction

**Strategic Implications:**
- **Urgent:** We risk falling behind on AI capabilities; competitors have 12-18 month lead
- **Opportunity:** Mid-market segment underserved by consumption pricing models
- **Threat:** Salesforce acquisitions signal intent to dominate CDP integration space

---

## 1. Intelligence Gathering Framework

**Primary Data Sources:**
- Company investor relations sites and SEC filings (10-K, 10-Q, 8-K)
- Product release notes and changelogs (salesforce.com/releases, hubspot.com/product-updates)
- Job postings on LinkedIn, Greenhouse (analyze hiring patterns for AI/ML roles)
- Patent filings (USPTO database, Google Patents)
- G2, TrustRadius, Capterra reviews (customer sentiment and feature requests)

**Secondary Sources for Validation:**
- Industry analyst reports (Gartner Magic Quadrant, Forrester Wave)
- Technology news (TechCrunch, VentureBeat, SaaStr coverage)
- Conference presentations and demo videos (Dreamforce, INBOUND recordings)
- LinkedIn employee posts (product managers, engineers discussing features)

[... continues with full competitive analysis ...]

## 6. Opportunity Identification

**Market Gaps:**
1. **AI for Small Teams (<10 users):** Competitors focus on enterprise; SMB AI tooling underserved
   - Impact: High | Feasibility: Medium | Timeline: 6-9 months
2. **Privacy-First AI:** No competitor offers on-premise AI model deployment
   - Impact: Medium | Feasibility: High | Timeline: 12 months
3. **Vertical-Specific CRM:** Healthcare and financial services lack compliant AI features
   - Impact: High | Feasibility: Low (regulatory complexity) | Timeline: 18+ months
```

## Tips

- **For product intelligence:** Monitor GitHub repos, technical blogs, and developer forums where engineers discuss upcoming features
- **When time-limited:** Focus on 1-2 competitors deeply rather than 5+ superficially
- **For pricing analysis:** Use Wayback Machine to track historical pricing page changes
- **To validate findings:** Cross-reference 3+ independent sources before making strategic claims
- **For early warning signals:** Set up Google Alerts, RSS feeds, and social listening for competitors
- **When presenting to executives:** Lead with threats/opportunities, not methodology details

## Related Prompts

- [Market Research Analyst](market-research-analyst.md) - For broader market trend analysis
- [SWOT Analysis Expert](../business/swot-analysis.md) - For framework-driven strategy analysis
- [Business Case Developer](business-case-developer.md) - For turning intelligence into investment proposals

## Changelog

### Version 2.0 (2025-11-25)

- **MAJOR UPGRADE:** Expanded from 33 words to 150+ word comprehensive framework
- Added intelligence gathering methodology with data source guidance
- Included ethical and legal boundary guidelines
- Added realistic example with complete competitive intelligence report excerpt
- Enhanced variable documentation with specific examples
- Added tips for different research scenarios
- **Score improvement:** 42/100 (Tier 4) → 72/100 (Tier 2)

### Version 1.0 (2025-11-16)

- Initial minimal version migrated from legacy prompt library
