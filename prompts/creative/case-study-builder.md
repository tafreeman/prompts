---
title: "Case Study Builder"
shortTitle: "Case Study"
intro: "Draft a credible, metrics-driven customer case study with a clear narrative, proof points, and reusable excerpts."
type: "how_to"
difficulty: "intermediate"
audience:
  - "functional-team"
  - "business-analyst"
  - "project-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "creative"
  - "documentation"
  - "business"
author: "Prompts Library Team"
version: "1.0"
date: "2026-01-03"
governance_tags:
  - "PII-safe"
  - "general-use"
  - "human-review-recommended"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---

# Case Study Builder

---

## Description

Create a structured, believable case study that clearly explains the customer problem, the solution, and measurable outcomes. This prompt produces a publication-ready draft plus optional excerpts for reuse across marketing channels.

---

## Use Cases

- Turning interview notes into a customer story
- Creating a sales enablement case study (PDF/web page)
- Drafting website success stories with proof points
- Generating shorter pull-quotes and social snippets

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `[company_name]` | Your company/product name | `Acme Analytics` |
| `[customer_name]` | Customer name (or "Anonymous Customer") | `Northwind Logistics` |
| `[customer_profile]` | Customer segment and context | `Mid-market 3PL with 500 employees` |
| `[problem_summary]` | What was broken/slow/costly before | `Manual reporting took 2 days/week` |
| `[solution_summary]` | What you implemented and how | `Automated pipelines + dashboards` |
| `[implementation_details]` | Timeline, scope, people, integrations | `6-week rollout; Salesforce + Snowflake` |
| `[results]` | Quantified outcomes (with time window) | `-35% churn; +18% conversion; 3x faster` |
| `[quotes]` | Approved quotes (or "None") | `“We saved 10 hours/week…” — VP Ops` |
| `[tone]` | Style constraints | `Professional, concise, credible` |
| `[length]` | Target length | `800-1200 words` |
| `[privacy_rules]` | What must be anonymized/redacted | `No personal names; mask revenue figures` |

---

## Prompt

```text
You are a senior B2B storyteller and technical marketing writer.

Write a customer case study in Markdown based on the inputs below.

## Inputs
Company: [company_name]
Customer: [customer_name]
Customer profile: [customer_profile]
Problem summary: [problem_summary]
Solution summary: [solution_summary]
Implementation details: [implementation_details]
Results: [results]
Quotes (approved only): [quotes]
Tone: [tone]
Target length: [length]
Privacy rules: [privacy_rules]

## Requirements
1) Be specific, but do NOT invent facts. If a detail is missing, add a bracketed placeholder like [ADD METRIC] or [ADD DETAIL] and list it in a "Missing Inputs" section.
2) If the customer name is "Anonymous" or privacy rules require it, anonymize identifiers (people, exact locations, contract values) and keep the story plausible.
3) Emphasize outcomes with numbers and timeframes. Prefer before/after framing.
4) Avoid hype. Use credible language and concrete evidence.

## Output format (Markdown)
- Title
- Executive summary (3–5 bullets)
- Customer overview
- The challenge
- The solution
- Implementation (timeline + scope)
- Results (table of metrics)
- Quote(s) (only if provided/approved)
- Lessons learned / what made it work
- Call to action (1–2 lines)
- Missing inputs (if any)

## Also include (appendices)
A) 5 pull-quotes (if quotes are missing, convert factual statements into pull-quote style without fabricating)
B) 3 short social posts (LinkedIn style) summarizing the win
```

---

## Example

**Input:**

```text
[company_name]=Acme Analytics
[customer_name]=Northwind Logistics
[customer_profile]=Mid-market 3PL with ~500 employees and 8 distribution centers
[problem_summary]=Weekly KPI reporting required exporting spreadsheets from 4 systems and took ~16 hours/week; leaders lacked near-real-time visibility
[solution_summary]=Implemented automated data ingestion to Snowflake and built Power BI dashboards for operations and finance
[implementation_details]=6-week project; integrated WMS + TMS + ERP + CRM; trained 25 users; set up role-based access
[results]=Reduced reporting time from ~16 hours/week to ~2 hours/week within 30 days; improved on-time shipment rate from 91% to 95% over 8 weeks
[quotes]=“We reclaimed at least two workdays a week and finally trust the numbers.” — VP Operations
[tone]=Professional, clear, not hypey
[length]=900–1100 words
[privacy_rules]=Do not include personal names beyond the approved quote; do not mention contract value
```

**Output (excerpt):**

```text
# Northwind Logistics streamlines KPI reporting with Acme Analytics

## Executive summary
- Reduced weekly KPI reporting time from ~16 hours/week to ~2 hours/week within 30 days
- Improved on-time shipment rate from 91% to 95% over 8 weeks
- Consolidated data from WMS, TMS, ERP, and CRM into governed dashboards

## Customer overview
Northwind Logistics is a mid-market third-party logistics provider operating eight distribution centers. Operations and finance teams rely on consistent, trusted KPIs to manage throughput, on-time delivery, and cost.

...

## Results
| Metric | Before | After | Timeframe |
|---|---:|---:|---|
| KPI reporting effort | ~16 hours/week | ~2 hours/week | 30 days |
| On-time shipment rate | 91% | 95% | 8 weeks |

...

## Missing inputs
- [ADD DETAIL] Primary business objective for the project (cost savings, service levels, growth support)
```

---

## Tips

- Provide at least 2–3 quantified outcomes (time saved, cost saved, revenue impact, quality metrics).
- Include timeline and scope to increase credibility.
- If you lack direct quotes, add a short "Stakeholder perspective" section with placeholders instead of inventing quotes.
- Keep each section skimmable; use bullets and a results table.

---

## Related Prompts

- [Ad Copy Generator](/prompts/creative/ad-copy-generator)
- [Product Description Generator](/prompts/creative/product-description-generator)
- [Email Newsletter Writer](/prompts/creative/email-newsletter-writer)
