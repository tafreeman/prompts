---
name: Landing Page Copy Builder
description: Generate landing page copy with clear positioning, benefits, objections, CTAs, and A/B variants.
type: template
---

# Landing Page Copy Builder

## Use Cases

- New feature or product launch pages
- Webinar or event registration pages
- Lead magnet and download pages
- Paid campaign landing pages

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

## Tips

- Use one primary CTA; keep the rest supportive.
- Replace proof placeholders with approved metrics before publishing.
- If you have multiple audiences, generate one page per audience to keep copy specific.

---

## Related Prompts

- [Ad Copy Generator](/prompts/creative/ad-copy-generator)
- [Marketing Campaign Strategist](/prompts/creative/marketing-campaign-strategist)
- [Product Description Generator](/prompts/creative/product-description-generator)
