---
title: "Press Release Generator"
shortTitle: "Press Release"
intro: "Generate an AP-style press release with quotes, boilerplate, media contact details, and channel-ready variants."
type: "how_to"
difficulty: "beginner"
audience:
  - "functional-team"
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
  - "requires-human-review"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---

# Press Release Generator

---

## Description

Create a clean, publication-ready press release in a standard format, with optional subject lines and social snippets for distribution. This prompt avoids invented claims by forcing placeholders for missing approvals, numbers, or quotes.

---

## Use Cases

- Product launches and feature announcements
- Partnerships and integration announcements
- Funding, awards, and milestone updates
- Event announcements (webinars, conferences)

---

## Variables

| Variable | Description | Example |
|---|---|---|
| `[headline]` | Headline (plain, factual) | `Acme Analytics launches real-time inventory dashboards` |
| `[subheadline]` | Optional supporting line | `New dashboards reduce reporting time for operations teams` |
| `[date_location]` | Dateline | `SEATTLE — January 3, 2026` |
| `[announcement]` | What happened, in plain language | `Released dashboards for WMS/TMS inventory visibility` |
| `[who_it_helps]` | Intended audience/customer | `Operations leaders at 3PLs` |
| `[proof_points]` | Approved metrics/claims only | `Early adopters cut reporting time by 50%` |
| `[quotes]` | Approved quotes (or "None") | `CEO quote + customer quote` |
| `[boilerplate]` | Company boilerplate paragraph | `Acme Analytics is...` |
| `[media_contact]` | Name/email/phone (or placeholder) | `Press: press@acme.com` |
| `[constraints]` | Embargo, compliance, do-not-say list | `No competitor comparisons; no revenue numbers` |

---

## Prompt

```text
You are a PR writer experienced with AP-style press releases.

Write a press release using the inputs below. If any item is missing or not approved, insert a clear placeholder like [ADD APPROVED QUOTE] rather than making something up.

## Inputs
Headline: [headline]
Subheadline (optional): [subheadline]
Dateline: [date_location]
Announcement: [announcement]
Who it helps: [who_it_helps]
Approved proof points: [proof_points]
Approved quotes: [quotes]
Company boilerplate: [boilerplate]
Media contact: [media_contact]
Constraints: [constraints]

## Output requirements
- 1) Headline + subheadline
- 2) Dateline + lead paragraph (who/what/when/where/why)
- 3) Body paragraphs (details, context, customer impact)
- 4) Quotes section (include up to 2 quotes; if none, add placeholders)
- 5) Boilerplate paragraph
- 6) Media contact block
- 7) "About" section (if boilerplate is short, expand with safe, factual statements)
- 8) Optional: 3 email subject lines + 3 social posts (LinkedIn + X-style)

## Style
- Clear, factual, non-hypey.
- Keep it under ~600 words unless otherwise requested.
- Avoid unverified claims; prefer concrete details.
```

---

## Example

**Input:**

```text
[headline]=Acme Analytics introduces real-time inventory dashboards for 3PL operations
[subheadline]=Dashboards connect WMS and TMS data to reduce manual reporting
[date_location]=SEATTLE — January 3, 2026
[announcement]=Acme Analytics released a new dashboard suite that consolidates inventory and shipment KPIs into one view
[who_it_helps]=Operations and finance leaders at mid-market logistics companies
[proof_points]=Pilot customers reduced weekly KPI reporting effort from ~10 hours to ~3 hours within 30 days
[quotes]=“This release makes it easier to act on inventory signals the same day.” — Jane Doe, CEO, Acme Analytics
[boilerplate]=Acme Analytics builds operational intelligence tools for logistics teams.
[media_contact]=Press: press@acme.com | +1 (555) 010-1234
[constraints]=Do not mention pricing; avoid naming competitors
```

**Output (excerpt):**

```text
# Acme Analytics introduces real-time inventory dashboards for 3PL operations
## Dashboards connect WMS and TMS data to reduce manual reporting

SEATTLE — January 3, 2026 — Acme Analytics today announced the availability of a new suite of real-time inventory dashboards designed to help mid-market logistics teams consolidate WMS and TMS signals into a single operational view.

...

### Quote
“​​This release makes it easier to act on inventory signals the same day,” said Jane Doe, CEO of Acme Analytics.

...

### Media Contact
Press: press@acme.com | +1 (555) 010-1234
```

---

## Tips

- Only include proof points that have been reviewed/approved.
- If you don’t have a customer quote, add a placeholder and get approvals first.
- Keep the lead paragraph strict: who/what/when/where/why.

---

## Related Prompts

- [Email Newsletter Writer](/prompts/creative/email-newsletter-writer)
- [Social Media Content Generator](/prompts/creative/social-media-content-generator)
- [Headline Tagline Creator](/prompts/creative/headline-tagline-creator)
