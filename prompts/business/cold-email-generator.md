---
title: "Cold Email Generator"
shortTitle: "Cold Email"
intro: "Generate personalized, high-converting cold outreach emails for sales prospecting and business development."
type: "how_to"
difficulty: "beginner"
audience:
  - "business-analyst"
  - "project-manager"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "sales"
  - "email"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.8
---
# Cold Email Generator

---

## Description

Create personalized cold emails that get responses. Generates subject lines, opening hooks, value propositions, and clear calls-to-action tailored to specific prospects and industries.

---

## Use Cases

- Outbound sales prospecting to new accounts
- Business development partnership outreach
- Recruiting passive candidates
- Investor outreach for fundraising
- Event speaker or sponsor recruitment

---

## Prompt

```text
You are an expert cold email copywriter with a 40%+ open rate track record.

Write a cold email for:

**Prospect**: [prospect_info]
**My Company/Role**: [sender_info]
**Goal**: [goal]
**Value Proposition**: [value_prop]
**Personalization Hook**: [hook]

Generate:

1. **Three Subject Line Options**
   - Curiosity-driven (create intrigue)
   - Value-driven (clear benefit)
   - Personalized (references their company/role)

2. **Email Body** (under 150 words)
   - Opening line (personalized, NOT "I hope this finds you well")
   - Pain point acknowledgment (1 sentence)
   - Value proposition (1-2 sentences)
   - Social proof (1 brief example)
   - Clear CTA (specific ask, low commitment)

3. **P.S. Line** (optional pattern interrupt)

4. **Alternative Shorter Version** (under 75 words for mobile)

Keep tone conversational and human. Avoid corporate jargon. Write like a real person, not a marketing email.
```text

---

## Variables

- `[prospect_info]`: Prospect name, title, company, and any relevant context (e.g., "Sarah – Engineering Director at Stripe who posted about on-call burnout")
- `[sender_info]`: Your name, role, and company (e.g., "Alex, founder of OnCallAI")
- `[goal]`: Desired outcome of the email (e.g., "Book a 15-minute intro call")
- `[value_prop]`: Key benefit you offer (e.g., "Reduces alert volume by 60% using AI triage")
- `[hook]`: Personalization hook based on research (e.g., "Reference their LinkedIn post about on-call fatigue")

---

## Example

### Context

A founder of an on‑call optimisation startup wants to reach out to an engineering leader at Stripe after seeing a LinkedIn post about on‑call fatigue and burnout.

### Input

```text
You are an expert cold email copywriter with a 40%+ open rate track record.

Write a cold email for:

**Prospect**: Sarah – Engineering Director at Stripe who posted on LinkedIn about on-call burnout and losing two senior engineers
**My Company/Role**: Alex, founder of OnCallAI (startup focused on reducing alert fatigue for engineering teams)
**Goal**: Book a 15-minute intro call to explore whether OnCallAI could help reduce on-call load for her team
**Value Proposition**: OnCallAI reduces alert volume by ~60% using AI triage and runbook generation
**Personalization Hook**: Reference Sarah’s LinkedIn post about on-call fatigue and her recent team departures

Generate the subject lines, full email, and short mobile‑optimised version as described in the prompt.
```text

### Expected Output

The AI generates three subject lines, a personalised full‑length cold email, a shorter mobile‑optimised version, and a brief explanation of why the approach works—similar to the example that follows.

**Output:**

```markdown
## Subject Line Options

1. **Curiosity**: "Your on-call post hit home"
2. **Value**: "Cut Stripe's on-call alerts by 60%?"
3. **Personalized**: "Sarah - re: on-call fatigue at Stripe"

---

## Email Body (Full Version)

Hi Sarah,

Your LinkedIn post about on-call fatigue stopped my scroll. Losing two senior engineers to burnout isn't just a retention problem—it's a $400K+ hit when you factor in recruiting and ramp time.

I built OnCallAI specifically for this. We use AI to auto-triage alerts (killing 60% of noise before it pages anyone) and draft runbooks from your incident history. Datadog's platform team cut their after-hours pages from 47/week to 12 after deploying us.

I know you're slammed, but would a 15-minute call be worth it if I could show you exactly how this would work with Stripe's stack?

Either way, really appreciated that post. It's a conversation more eng leaders need to have.

Alex

P.S. - Happy to send a teardown of how we'd integrate with PagerDuty if that's more useful than a call.

---

## Short Version (Mobile-Optimized)

Hi Sarah,

Saw your post about on-call burnout and losing engineers—that's brutal.

Built OnCallAI to fix exactly this. We cut alert noise by 60% using AI triage. Datadog's team went from 47 pages/week to 12.

Worth 15 min to see if it'd work for Stripe?

Alex

---

## Why This Works

- **Subject line**: References her content = instant relevance
- **Opening**: Shows I actually read her post (not a template)
- **Pain**: Quantifies the cost ($400K) to elevate urgency
- **Value prop**: Specific metric (60% reduction) + how it works
- **Social proof**: Datadog = credible peer company
- **CTA**: Low commitment (15 min) + clear value exchange
- **P.S.**: Offers alternative if call feels too high-friction
```text

---


## Tips

- Research before writing - 5 minutes of LinkedIn stalking beats a generic template
- Keep it short - aim for under 150 words, under 75 for mobile-first prospects
- One CTA only - asking for multiple things kills response rates
- Send Tuesday-Thursday, 8-10am their timezone for best open rates
- Follow up 3x minimum - most responses come on follow-up 2 or 3

---

## Related Prompts

- [follow-up-email](./follow-up-email.md) - For follow-up sequences after cold outreach
- [sales-objection-handler](./sales-objection-handler.md) - For when prospects respond with objections
- [pitch-deck-generator](./pitch-deck-generator.md) - For when cold email converts to meeting
