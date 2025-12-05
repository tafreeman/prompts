---
title: "Sales Objection Handler"
shortTitle: "Objection Handler"
intro: "Generate effective responses to common sales objections with persuasive rebuttals and conversation frameworks."
type: "how_to"
difficulty: "intermediate"
audience:
  - "business-analyst"
  - "project-manager"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "sales"
  - "negotiation"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Sales Objection Handler

## Description

Transform common sales objections into opportunities with structured rebuttals, empathy-driven responses, and proven conversation frameworks. Helps sales teams prepare for and overcome buyer resistance.

---

## Use Cases

- Preparing for discovery calls with known objection patterns
- Training new sales reps on objection handling
- Creating battlecards for competitive situations
- Developing scripts for pricing negotiations
- Building confidence for high-stakes enterprise deals

---

## Prompt

```text
You are an expert sales coach who has trained top-performing enterprise sales teams.

Help me handle this sales objection:

**Objection**: [objection]
**Context**: [context]
**Product/Service**: [product]
**Buyer Persona**: [buyer]
**Deal Stage**: [stage]

Provide:

1. **Objection Analysis**
   - Root cause (what they're really saying)
   - Emotional driver (fear, uncertainty, budget pressure)
   - Objection type (price, timing, competition, authority, need)

2. **Response Framework** (LAER Method)
   - **Listen**: Acknowledge their concern (exact words to use)
   - **Acknowledge**: Show empathy without agreeing
   - **Explore**: Probing questions to understand deeper
   - **Respond**: Value-based rebuttal

3. **Three Response Options**
   - **Direct Response**: Confident, fact-based rebuttal
   - **Soft Response**: Empathy-first, relationship-building approach
   - **Redirect Response**: Pivot to value/ROI discussion

4. **Follow-Up Questions**
   - 3 questions to keep the conversation moving forward
   - Questions that uncover the real blocker

5. **If They Push Back Again**
   - Escalation response if initial rebuttal fails
   - When to walk away vs. when to persist

Format responses as ready-to-use scripts with natural conversational language.
```text
## Variables

- `[objection]`: The exact objection the buyer stated (e.g., "Your price is too high", "We're happy with our current vendor")
- `[context]`: Background on the deal (e.g., "Second call, they loved the demo but CFO is pushing back")
- `[product]`: Your product/service and key differentiators
- `[buyer]`: Buyer persona and their priorities (e.g., "VP of IT, focused on security and uptime")
- `[stage]`: Deal stage (e.g., "Discovery", "Demo follow-up", "Negotiation", "Contract review")

---

## Example Usage

**Input:**

```text
Objection: "Your solution is too expensive. We've seen competitors offer similar features for 40% less."
Context: Third call, they've completed a successful POC with positive feedback from IT team. Now in procurement/negotiation phase. Deal size is $180K ARR.
Product/Service: CloudSecure - enterprise security platform with AI-powered threat detection, 24/7 SOC, and compliance automation
Buyer Persona: CISO at mid-market fintech (500 employees), highly regulated industry, had a breach 18 months ago
Deal Stage: Negotiation - they want to close this quarter but are playing hardball on price
```text
**Output:**

```markdown
# Objection Handler: "Your price is too expensive"

---

## 1. Objection Analysis

**Root Cause**: This isn't a pure price objection - they completed a successful POC and want to buy. They're negotiating to justify the spend internally and ensure they're getting the best deal.

**Emotional Driver**: 
- **Fear**: CISO had a breach 18 months ago. They need a solution that won't fail them again, but also need to justify the premium to CFO/board.
- **Pressure**: Procurement is doing their job - testing whether you'll discount. This is expected behavior, not a red flag.

**Objection Type**: Price objection with competitive leverage. The "40% less" is likely a bluff or comparison to a less comprehensive solution.

---

## 2. LAER Response Framework

### Listen (Acknowledge the concern)

*"I hear you - $180K is a significant investment, and I appreciate you being direct about pricing. You're right to push on this."*

### Acknowledge (Empathy without agreeing)

*"Honestly, if I were in your seat - especially after what happened 18 months ago - I'd be scrutinizing every dollar too. This is exactly the kind of rigor I'd expect from a CISO who takes security seriously."*

### Explore (Probing questions)

*"Help me understand - when you say competitors are 40% less, are you comparing apples to apples? Specifically:*
- *Does that include 24/7 SOC coverage, or is that an add-on?*
- *What's their SLA for threat detection response time?*
- *Are they SOC 2 Type II and PCI-DSS compliant out of the box?*

*I'm asking because I want to make sure we're solving for the same problem - not just checking a box."*

### Respond (Value-based rebuttal)

*"Here's my honest take: You could go with a cheaper solution. But after a breach, the question isn't 'how do I save 40%?' - it's 'how do I make sure this never happens again?'*

*Our customers pay a premium because:*
- *Average breach cost in fintech is $5.9M. We've prevented 147 breaches for customers like [Similar Company] last year.*
- *Your IT team already validated the POC. They're not going to get that same experience with [Competitor].*
- *You're in a regulated industry. Our compliance automation will save your team 200+ hours per audit cycle.*

*The real question is: what's the cost of choosing the cheaper option if it fails?"*

---

## 3. Three Response Options

### Option A: Direct Response (Confident, fact-based)

*"I appreciate the comparison, but let's be specific. [Competitor]'s base price doesn't include 24/7 SOC - that's a $60K add-on. When you factor that in, we're within 10% of each other, and our threat detection SLA is 4x faster.*

*I'll put this in writing: if we don't reduce your incident response time by at least 50% in the first 6 months, I'll personally review our engagement and make it right. Can [Competitor] make that commitment?"*

### Option B: Soft Response (Empathy-first)

*"Look, I get it. $180K is real money, and you have a CFO to answer to. Here's what I want to avoid: you choose a cheaper solution, and in 18 months, we're having a different conversation.*

*What if we did this - I can't discount the platform, but I can add value. What if we included our premium compliance module (normally $25K/year) at no cost for the first year? That gives you a win to take back to procurement and addresses your SOC 2 audit prep."*

### Option C: Redirect Response (Pivot to ROI)

*"Let me flip this around. Forget the sticker price for a second. Your last breach cost - what, $2M in response costs plus the reputational hit? Our platform would have detected that attack in minutes, not days.*

*At $180K/year, you're paying less than 10% of what a single incident costs. The question isn't whether we're expensive - it's whether your current risk exposure is acceptable.*

*What would it mean for your board renewal next year if you could show zero breaches and 100% audit compliance?"*

---

## 4. Follow-Up Questions

1. *"If price weren't a factor, would you choose CloudSecure based on the POC results?"*
   - (Confirms the objection is price-only, not a deeper issue)

2. *"What does your procurement process look like from here? Is there a specific budget threshold that would make approval easier?"*
   - (Uncovers if there's a magic number that triggers faster approval)

3. *"Who else needs to sign off on this? I want to make sure we're addressing everyone's concerns, not just yours."*
   - (Identifies hidden stakeholders who may be the real blocker)

---

## 5. If They Push Back Again

### Escalation Response

*"I respect the negotiation, but I want to be transparent: we don't discount our platform. Every customer pays the same rate - it's how we maintain the R&D investment that makes our threat detection best-in-class.*

*What I can do is get creative on terms. Would a 2-year commit with payment terms (50% now, 50% in 6 months) make this easier to approve? Or I can bring in my VP of Sales to discuss strategic partnership pricing if you're open to a case study commitment."*

### When to Walk Away

Walk away if:
- They explicitly say a competitor has already won
- They're asking for 40%+ discount (not negotiating in good faith)
- The CISO isn't the real decision-maker and can't get you to the CFO

### When to Persist

Persist if:
- They keep engaging in the conversation (interest signal)
- They're asking for creative terms (they want to buy)
- The POC feedback was genuinely positive

**Closing Line**:

*"Here's where I'm at: I believe CloudSecure is the right choice for [Company], and I think you do too based on the POC. I can hold this pricing through end of quarter. After that, I can't guarantee the same terms because we're adjusting pricing in Q1. Can we get this across the finish line this week?"*
```text
## Tips

- Never immediately discount - it signals your initial price wasn't fair
- Use silence strategically - after your rebuttal, let them respond first
- Validate the objection first - "You're right to push on this" disarms defensiveness
- Always tie back to value, not features - buyers care about outcomes
- Have a walk-away point - desperation kills deals

---

## Related Prompts

- [cold-email-generator](./cold-email-generator.md) - For outreach before objections arise
- [pitch-deck-generator](./pitch-deck-generator.md) - For presentations that preempt objections
- [stakeholder-communication-manager](./stakeholder-communication-manager.md) - For multi-stakeholder deal navigation
