---
title: "Follow-Up Email Generator"
shortTitle: "Follow-Up Email"
intro: "Generate effective follow-up email sequences that re-engage prospects without being pushy or annoying."
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
# Follow-Up Email Generator

<<<<<<< HEAD

=======
>>>>>>> main
---

## Description

Create follow-up email sequences that get responses without damaging relationships. Generates multi-touch sequences with varied approaches for different stages of prospect engagement.

<<<<<<< HEAD

=======
>>>>>>> main
---

## Use Cases

- Following up after no response to cold outreach
- Re-engaging after a demo or meeting with no next steps
- Reviving stalled deals in the pipeline
- Post-conference or networking event follow-ups
- Checking in after sending proposals or quotes

<<<<<<< HEAD

=======
>>>>>>> main
---

## Prompt

```text
You are an expert at writing follow-up emails that get responses without being annoying.

Create a follow-up sequence for:

**Original Context**: [context]
**Prospect**: [prospect]
**Last Touchpoint**: [last_touch]
**Days Since Last Contact**: [days]
**Goal**: [goal]

Generate a 4-email follow-up sequence:

1. **Follow-Up #1** (2-3 days after)
   - Gentle nudge with new value
   - Different angle than original email

2. **Follow-Up #2** (5-7 days after)
   - Pattern interrupt (humor, story, or bold statement)
   - Acknowledge they're busy

3. **Follow-Up #3** (10-14 days after)
   - Add significant new value (case study, relevant news)
   - Lower the ask if needed

4. **Follow-Up #4 - Breakup Email** (21+ days)
   - Give them an easy out
   - Clear final ask

For each email include:
- Subject line
- Email body (under 100 words)
- Psychological principle being used

Keep tone human and respectful. No guilt-tripping or desperation.
```text

---

## Variables

- `[context]`: What the original email/interaction was about
- `[prospect]`: Name, title, company of the prospect
- `[last_touch]`: What was your last communication (cold email, demo, proposal, etc.)
- `[days]`: How many days since last contact
- `[goal]`: What you're trying to achieve (meeting, response, deal close)

<<<<<<< HEAD

=======
>>>>>>> main
---

## Example Usage

**Input:**

```text
Original Context: Sent cold email about our HR analytics platform that helps reduce employee turnover
Prospect: Marcus Thompson, CHRO at Acme Corp (2,000 employees, retail industry, high turnover rates)
Last Touchpoint: Cold email sent, no response
Days Since Last Contact: 4 days
Goal: Book a 20-minute discovery call
```text
<<<<<<< HEAD
=======

>>>>>>> main
**Output:**

```markdown
# Follow-Up Sequence for Marcus Thompson

---

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

---

## Follow-Up #2: Pattern Interrupt
**Send**: Day 9

**Subject**: should I send a carrier pigeon? 🐦

**Body**:

Marcus,

I know you're drowning in emails (I counted 147 in my inbox this morning before coffee).

One question: Is reducing turnover even a priority right now, or am I barking up the wrong tree?

A "yes, let's chat" or "no, bad timing" works perfectly.

Alex

**Principle**: *Pattern interrupt + binary choice* - humor breaks monotony, easy yes/no removes friction

---

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

---

## Follow-Up #4: The Breakup
**Send**: Day 25

**Subject**: closing your file

**Body**:

Marcus,

I've reached out a few times about reducing turnover at Acme - going to assume the timing isn't right.

I'll close out your file on my end, but if this becomes a priority later, my inbox is open.

If I read this wrong and you've just been slammed, reply "interested" and I'll send over times to chat.

Either way, best of luck navigating retail turnover this holiday season.

Alex

**Principle**: *Scarcity + takeaway* - removing the opportunity often triggers action; gives them easy out without guilt

---

## Sequence Timing Summary

| Email | Day | Approach | Ask Level |
| :--- |-----| :--- |-----------|
| Original | 0 | Cold outreach | Medium (call) |
| FU #1 | 4 | Value add | Medium (call) |
| FU #2 | 9 | Pattern interrupt | Low (yes/no) |
| FU #3 | 16 | Case study | Medium (call) |
| FU #4 | 25 | Breakup | Final (close file) |

---

## If They Respond

### If "Yes, interested":
Great! Send calendar link immediately. Don't add more content or you'll lose them.

### If "No, bad timing":
"Totally understand. When should I check back - Q1 or later?"
(Gets permission for future outreach)

### If "We went with someone else":
"Appreciate you letting me know. Curious - what made you choose [competitor]? Always looking to improve."
(Intel gathering for next time)
```text

---

## Tips

- Never say "just following up" or "circling back" - these are instant delete triggers
- Add new value in each follow-up - don't just repeat the same ask
- The breakup email often gets the highest response rate - use it strategically
- Space emails 3-7 days apart, not daily (respect their inbox)
- If no response after 4-5 touches, wait 30-60 days before a new sequence

<<<<<<< HEAD

=======
>>>>>>> main
---

## Related Prompts

- [cold-email-generator](./cold-email-generator.md) - For initial cold outreach
- [sales-objection-handler](./sales-objection-handler.md) - For when they respond with objections
- [meeting-summary](./meeting-summary.md) - For follow-ups after successful meetings
