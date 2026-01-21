---
type: template
name: Case Study Builder
description: Draft a credible, metrics-driven customer case study with a clear narrative, proof points, and reusable excerpts.
---

# Case Study Builder

## Description

Generates metrics-driven customer case studies with clear narratives, quantified outcomes, and reusable content. Converts interview notes and project data into credible B2B success stories with pull-quotes and social media snippets.

## Use Cases

- Turning interview notes into a customer story
- Creating a sales enablement case study (PDF/web page)
- Drafting website success stories with proof points
- Generating shorter pull-quotes and social snippets

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

## Tips

- Provide at least 2–3 quantified outcomes (time saved, cost saved, revenue impact, quality metrics).
- Include timeline and scope to increase credibility.
- If you lack direct quotes, add a short "Stakeholder perspective" section with placeholders instead of inventing quotes.
- Keep each section skimmable; use bullets and a results table.

---


## Variables

| Variable | Description |
| :--- | ------------- |
| `[company_name]` | The company featured in the case study |
| `[customer_name]` | The customer or client |
| `[customer_profile]` | Description of the customer |
| `[problem_summary]` | The main challenge or problem |
| `[solution_summary]` | The solution provided |
| `[implementation_details]` | How the solution was implemented |
| `[results]` | Quantitative or qualitative outcomes |
| `[quotes]` | Customer quotes |
| `[tone]` | Desired tone (e.g., professional, conversational) |
| `[length]` | Target length or word count |
| `[privacy_rules]` | Any privacy or anonymization requirements |

## Example

**Company:** Acme Corp
**Customer:** Beta Inc
**Customer profile:** SaaS provider in healthcare
**Problem summary:** Manual reporting led to errors and delays
**Solution summary:** Implemented Acme’s automated analytics platform
**Implementation details:** 2-week onboarding, integrated with existing EHR
**Results:** Reduced reporting time by 80%, eliminated manual errors
**Quotes:** “Acme’s platform changed our workflow overnight.”
**Tone:** Professional
**Length:** 500 words
**Privacy rules:** No PHI, anonymize staff names
