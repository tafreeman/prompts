---
name: Press Release Generator
description: Generate an AP-style press release with quotes, boilerplate, media contact details, and channel-ready variants.
type: template
---

# Press Release Generator

## Use Cases

- Product launches and feature announcements
- Partnerships and integration announcements
- Funding, awards, and milestone updates
- Event announcements (webinars, conferences)

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

## Tips

- Only include proof points that have been reviewed/approved.
- If you don’t have a customer quote, add a placeholder and get approvals first.
- Keep the lead paragraph strict: who/what/when/where/why.

---

## Related Prompts

- [Email Newsletter Writer](/prompts/creative/email-newsletter-writer)
- [Social Media Content Generator](/prompts/creative/social-media-content-generator)
- [Headline Tagline Creator](/prompts/creative/headline-tagline-creator)
