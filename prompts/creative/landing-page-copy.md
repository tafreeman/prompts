---
title: "Landing Page Copy Builder"
shortTitle: "Landing Page"
intro: "Generate landing page copy with clear positioning, benefits, objections, CTAs, and A/B variants."
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

# Landing Page Copy Builder

---

## Description

Create conversion-focused landing page copy that communicates value quickly and answers common objections. This prompt outputs a full page structure plus A/B variants you can test.

---

## Use Cases

- New feature or product launch pages
- Webinar or event registration pages
- Lead magnet and download pages
- Paid campaign landing pages

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `[product]` | Product/service name | `Acme Analytics` |
| `[audience]` | Who the page is for | `Operations managers at 3PLs` |
| `[primary_pain]` | Main pain point | `Manual KPI reporting` |
| `[value_prop]` | 1–2 sentence value proposition | `Real-time dashboards in weeks, not months` |
| `[key_benefits]` | 3–6 benefits (bullets) | `Faster decisions; fewer errors; less toil` |
| `[proof]` | Social proof (approved only) | `Case study metrics, logos (if approved)` |
| `[objections]` | Common concerns | `Implementation time, security, cost` |
| `[cta]` | Primary call to action | `Book a demo` |
| `[keywords]` | Optional SEO keywords | `inventory dashboard, 3PL analytics` |
| `[tone]` | Brand voice | `Direct, helpful, confident` |
| `[constraints]` | Word count, compliance, do-not-say list | `No competitor claims; under 400 words` |

---

## Prompt

```text
You are a conversion copywriter and UX writer.

Write landing page copy using the inputs below. Do not invent facts. If proof points are missing, add placeholders like [ADD APPROVED METRIC].

## Inputs
Product: [product]
Audience: [audience]
Primary pain: [primary_pain]
Value proposition: [value_prop]
Key benefits: [key_benefits]
Approved proof: [proof]
Common objections: [objections]
Primary CTA: [cta]
SEO keywords (optional): [keywords]
Tone: [tone]
Constraints: [constraints]

## Output format
1) Hero section
   - Headline (max 10 words)
   - Subheadline (1–2 sentences)
   - Primary CTA button text + microcopy
2) Benefits section (3–6 bullets)
3) How it works (3 steps)
4) Proof section (placeholders if needed)
5) Objection handling / FAQ (5 Q&As)
6) Secondary CTA section
7) A/B variants
   - 3 alternative headlines
   - 2 alternative CTAs

## Writing rules
- Keep sentences short and concrete.
- Prefer benefits over features.
- Use the audience’s language (from the inputs).
- If constraints include a word limit, prioritize hero + benefits + CTA first.
```

---

## Example

**Input:**

```text
[product]=Acme Analytics
[audience]=Operations managers at mid-market logistics companies (3PL)
[primary_pain]=Weekly KPI reporting is manual and delayed
[value_prop]=Get real-time inventory and shipment dashboards in weeks—without a dedicated engineering team.
[key_benefits]=Reduce reporting toil; spot exceptions same-day; align ops + finance; role-based access
[proof]=Pilot customers reduced weekly reporting from ~10 hours to ~3 hours within 30 days
[objections]=“Will this work with our WMS/TMS?”; “Is it secure?”; “How long to implement?”
[cta]=Book a demo
[keywords]=3PL dashboards, logistics analytics
[tone]=Confident, plainspoken, not hypey
[constraints]=Under ~420 words; do not mention pricing; no competitor comparisons
```

**Output (excerpt):**

```text
## Hero
**Headline:** Real-time 3PL dashboards—without the spreadsheet grind

**Subheadline:** Acme Analytics consolidates WMS and TMS signals into a single view so ops and finance can act the same day.

**CTA:** Book a demo
*Microcopy:* See a sample dashboard and an implementation plan.

## Benefits
- Cut weekly KPI reporting time with automated refresh
- Spot inventory and shipment exceptions before they become customer issues
- Align ops + finance with one source of truth
- Control access with role-based permissions

...

## A/B headlines
1. Stop waiting a week for logistics KPIs
2. The 3PL dashboard your teams actually trust
3. Turn WMS/TMS data into decisions—fast
```

---

## Tips

- Use one primary CTA; keep the rest supportive.
- Replace proof placeholders with approved metrics before publishing.
- If you have multiple audiences, generate one page per audience to keep copy specific.

---

## Related Prompts

- [Ad Copy Generator](/prompts/creative/ad-copy-generator)
- [Marketing Campaign Strategist](/prompts/creative/marketing-campaign-strategist)
- [Product Description Generator](/prompts/creative/product-description-generator)
