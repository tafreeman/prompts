---
name: Follow-Up Email Generator
description: Generate effective follow-up email sequences that re-engage prospects without being pushy or annoying.
type: how_to
---

# Follow-Up Email Generator

## Description

This prompt generates effective follow-up email sequences that re-engage prospects without being pushy or annoying. It helps sales professionals and business developers maintain momentum with unresponsive contacts through value-added touchpoints.

## Use Cases

- Following up after no response to cold outreach
- Re-engaging after a demo or meeting with no next steps
- Reviving stalled deals in the pipeline
- Post-conference or networking event follow-ups
- Checking in after sending proposals or quotes

## Variables

- `[context]`: Original outreach context (e.g., "Sent cold email about OnCallAI after LinkedIn post")
- `[prospect]`: Prospect name and role (e.g., "Marcus Thompson, VP Engineering at Fintech Co")
- `[last_touch]`: Last interaction (e.g., "Cold email sent, no response")
- `[days]`: Days since last contact (e.g., "5 days")
- `[goal]`: Desired outcome (e.g., "Schedule 15-minute intro call")

## Prompt

### System Prompt

```text
You are a sales communication expert who specializes in follow-up sequences that convert. You understand that effective follow-ups add value, not just repeat asks. You know how to maintain persistence without being annoying.
```

### User Prompt

```text
Create a follow-up email for the following situation:

Context:
- Original Outreach: [context]
- Prospect: [prospect]
- Last Touch: [last_touch]
- Days Since Contact: [days]
- Goal: [goal]

Please provide:
1. Subject line (avoid "following up" or "checking in")
2. Email body with new value (under 100 words)
3. Clear but low-pressure call-to-action
4. Explanation of the psychological principle being used
```

## Example

### Input

```text
Create a follow-up email for the following situation:

Context:
- Original Outreach: Sent cold email about OnCallAI after LinkedIn post
- Prospect: Marcus Thompson, VP Engineering at Fintech Co
- Last Touch: Cold email sent, no response
- Days Since Contact: 5 days
- Goal: Schedule 15-minute intro call
```

### Expected Output

```text
**Subject**: forgot to mention this, Marcus

**Body**:
Hey Marcus,

Quick follow-up on my note about turnover analytics.

Realized I didn't mention - we just published data showing retail turnover spiked 23% in Q3. Happy to share the full report + how companies like Nordstrom are using predictive signals to get ahead of flight risks.

Worth a quick chat?

Alex

**Psychological Principle**: Reciprocity – offering something valuable (the report) creates a sense of obligation to respond. The email adds new information rather than repeating the original ask, demonstrating respect for their time.

**Why This Works**:
- Subject feels personal, not templated
- Leads with value (free report) before any ask
- Short and scannable
- Low-pressure CTA ("worth a quick chat?")
- No guilt-tripping about lack of response
```

## Follow-Up #1: The Value Add
**Send**: Day 4 (today)

**Subject**: forgot to mention this, Marcus

**Body**:

Hey Marcus,

Quick follow-up on my note about turnover analytics.

Realized I didn't mention - we just published data showing retail turnover spiked 23% in Q3. Happy to share the full report + how companies like Nordstrom are using predictive signals to get ahead of flight risks.

Worth a quick chat?

Alex

**Principle**: *Reciprocity* - offering something valuable (report) creates obligation to respond

## Follow-Up #3: The Case Study
**Send**: Day 16

**Subject**: how Target cut turnover 31%

**Body**:

Marcus,

Figured this might be more useful than another "just checking in" email.

Target's HR team used our platform to identify turnover risk signals 90 days before employees quit. Result: 31% reduction in voluntary turnover, $4.2M saved annually.

I can walk you through exactly how they did it in 20 minutes. If it's not relevant to Acme, I'll buy you a coffee for wasting your time.

Calendar link: [link]

Alex

**Principle**: *Social proof + risk reversal* - peer success story + offering compensation for their time

## Sequence Timing Summary

| Email | Day | Approach | Ask Level |
| ------- | ----- | ---------- | ----------- |
| Original | 0 | Cold outreach | Medium (call) |
| FU #1 | 4 | Value add | Medium (call) |
| FU #2 | 9 | Pattern interrupt | Low (yes/no) |
| FU #3 | 16 | Case study | Medium (call) |
| FU #4 | 25 | Breakup | Final (close file) |

## Tips

- Never say "just following up" or "circling back" - these are instant delete triggers
- Add new value in each follow-up - don't just repeat the same ask
- The breakup email often gets the highest response rate - use it strategically
- Space emails 3-7 days apart, not daily (respect their inbox)
- If no response after 4-5 touches, wait 30-60 days before a new sequence

---

## Related Prompts

- [cold-email-generator](./cold-email-generator.md) - For initial cold outreach
- [sales-objection-handler](./sales-objection-handler.md) - For when they respond with objections
- [meeting-summary](./meeting-summary.md) - For follow-ups after successful meetings
