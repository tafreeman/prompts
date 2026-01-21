---
name: Cold Email Generator
description: Generate personalized, high-converting cold outreach emails for sales prospecting and business development.
type: how_to
---

# Cold Email Generator

## Use Cases

- Outbound sales prospecting to new accounts
- Business development partnership outreach
- Recruiting passive candidates
- Investor outreach for fundraising
- Event speaker or sponsor recruitment

## Variables

- `[prospect_info]`: Prospect name, title, company, and any relevant context (e.g., "Sarah – Engineering Director at Stripe who posted about on-call burnout")
- `[sender_info]`: Your name, role, and company (e.g., "Alex, founder of OnCallAI")
- `[goal]`: Desired outcome of the email (e.g., "Book a 15-minute intro call")
- `[value_prop]`: Key benefit you offer (e.g., "Reduces alert volume by 60% using AI triage")
- `[hook]`: Personalization hook based on research (e.g., "Reference their LinkedIn post about on-call fatigue")

## Email Body (Full Version)

Hi Sarah,

Your LinkedIn post about on-call fatigue stopped my scroll. Losing two senior engineers to burnout isn't just a retention problem—it's a $400K+ hit when you factor in recruiting and ramp time.

I built OnCallAI specifically for this. We use AI to auto-triage alerts (killing 60% of noise before it pages anyone) and draft runbooks from your incident history. Datadog's platform team cut their after-hours pages from 47/week to 12 after deploying us.

I know you're slammed, but would a 15-minute call be worth it if I could show you exactly how this would work with Stripe's stack?

Either way, really appreciated that post. It's a conversation more eng leaders need to have.

Alex

P.S. - Happy to send a teardown of how we'd integrate with PagerDuty if that's more useful than a call.

## Why This Works

- **Subject line**: References her content = instant relevance
- **Opening**: Shows I actually read her post (not a template)
- **Pain**: Quantifies the cost ($400K) to elevate urgency
- **Value prop**: Specific metric (60% reduction) + how it works
- **Social proof**: Datadog = credible peer company
- **CTA**: Low commitment (15 min) + clear value exchange
- **P.S.**: Offers alternative if call feels too high-friction

```text

## Related Prompts

- [follow-up-email](./follow-up-email.md) - For follow-up sequences after cold outreach
- [sales-objection-handler](./sales-objection-handler.md) - For when prospects respond with objections
- [pitch-deck-generator](./pitch-deck-generator.md) - For when cold email converts to meeting
