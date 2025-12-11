---
title: "M365 Presentation Outline Generator"
shortTitle: "M365 Presentation Outlin..."
intro: "This prompt helps an individual quickly create a structured PowerPoint presentation outline using Microsoft 365 context. It generates slide titles, bullet points, and visual suggestions based on a ..."
m365App: "Copilot in PowerPoint"
type: "how_to"
difficulty: "beginner"
audience:
  - "junior-engineer"
  - "business-analyst"
platforms:
  - "github-copilot"
  - "m365-copilot"
topics:
  - "powerpoint"
  - "m365"
  - "business"
  - "copilot"
author: "Your Name"
version: "1.0"
date: "2025-11-18"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# M365 Presentation Outline Generator

---

## Description

This prompt helps an individual quickly create a structured PowerPoint presentation outline using Microsoft 365 context. It generates slide titles, bullet points, and visual suggestions based on a topic, source document, or project context, tailored to a specific audience.

## Goal

Enable a user to go from idea or source material to a complete presentation outline in minutes, reducing the time spent on structure and allowing more focus on content refinement and design.

## Context

Assume the user works in Microsoft 365 with access to PowerPoint, Word, OneDrive/SharePoint, and Teams. Presentations are often built from scratch or based on existing documents, meeting notes, or project updates.

The AI can reference:

- A source document (e.g., a Word doc, report, or meeting notes)
- Recent emails, chats, or documents related to the presentation topic
- The user's specified audience, topic, and emphasis areas

## Inputs

The user provides:

- `[topic]`: The main topic or title of the presentation (e.g., "Q4 Product Roadmap", "Customer Onboarding Strategy").
- `[audience]`: Who will see the presentation (e.g., "executives", "customers", "engineering team", "board of directors").
- `[emphasis]`: What to emphasize (e.g., "benefits and ROI", "technical details", "risks and mitigations", "customer stories").
- Optional: `[source_document]`: A Word doc, PDF, or other file to use as the primary source material.
- Optional: `[slide_count_target]`: Desired number of slides (e.g., "8–12 slides").

## Assumptions

- If a source document is provided, the AI should extract key themes and structure the presentation around them.
- If no source document is provided, the AI should infer structure from the topic and recent context (emails, chats, documents).
- The user wants slide titles that are clear and action-oriented, not generic.
- The user wants 3–5 bullet points per slide, plus suggestions for where visuals (charts, images, diagrams) would help.

## Constraints

- Generate a slide outline with the following for each slide:
  - Slide title
  - 3–5 bullet points summarizing content
  - Visual suggestion (e.g., "chart showing timeline", "customer quote callout", "architecture diagram")
- Tailor language and detail level to the `[audience]`.
- Keep the outline scannable; the user will refine and add details later.
- Aim for `[slide_count_target]` if specified; otherwise, default to 10–12 slides.

## Process / Reasoning Style

- Internally:
  - If a source document exists, extract the main narrative, key sections, and supporting data.
  - If no source document, synthesize from the topic and recent related context.
  - Structure the presentation with a clear flow: intro → body (key themes) → conclusion/next steps.
  - Identify where visuals would strengthen communication (trends, comparisons, timelines, testimonials).
- Externally (visible to the user):
  - Present a structured outline without exposing chain-of-thought.
  - Use a professional, supportive tone.
  - Provide actionable visual suggestions that the user can execute in PowerPoint.

## Output Requirements

Return the output in Markdown with:

- `## Presentation Title`
  - Suggested title for the deck.
- `## Slide Outline`
  - For each slide:
    - **Slide [number]: [Title]**
    - Bullet points (3–5)
    - Visual suggestion

---

## Use Cases

- Use case 1: A product manager creating a roadmap presentation for executive review.
- Use case 2: A consultant building a client presentation from a project report.
- Use case 3: An engineer preparing a technical deep-dive for a design review.
- Use case 4: A marketing lead outlining a campaign strategy deck.
- Use case 5: A team lead creating a quarterly business review presentation.

---

## Prompt

```text
You are my Presentation Outline Generator working in a Microsoft 365 environment.

Goal:
Help me create a PowerPoint outline for a presentation on [topic], tailored for
[audience] and emphasizing [emphasis].

Context:
- I use PowerPoint, Word, OneDrive/SharePoint, and Teams in Microsoft 365.
- I want a clear, structured outline with slide titles, bullet points, and visual
  suggestions that I can execute in PowerPoint.

Scope:
- If [source_document] is provided, extract key themes and structure the presentation
  around them.
- If no source document, synthesize from the topic and any recent related context
  (emails, chats, documents).
- Tailor language and detail level to [audience].
- Emphasize [emphasis].

Assumptions and constraints:
- Provide slide titles that are clear and action-oriented, not generic.
- For each slide, provide 3–5 bullet points and a visual suggestion (chart, image,
  diagram, callout).
- Aim for [slide_count_target] slides if specified; otherwise, default to 10–12 slides.
- Structure the presentation with a clear flow: intro → body → conclusion/next steps.

Process:
1. Identify the main narrative and key themes for [topic].
2. Structure slides logically: opening, key themes (1 theme per slide or section),
   conclusion, next steps.
3. For each slide, draft bullet points and suggest where visuals would help.

Output format:
Return the result in Markdown:

## Presentation Title
[Suggested title]

## Slide Outline

**Slide 1: [Title]**
- [Bullet]
- [Bullet]
- Visual suggestion: [suggestion]

**Slide 2: [Title]**
- [Bullet]
- [Bullet]
- Visual suggestion: [suggestion]

[Continue for all slides]

Now, generate a presentation outline for [topic], tailored for [audience] and
emphasizing [emphasis].
```text

**Output:**

```text
## Presentation Title
Q4 Customer Onboarding Roadmap: Timeline, Risks, and Customer Impact

## Slide Outline

**Slide 1: Executive Summary**
- Overview of the Q4 onboarding roadmap and goals.
- Key customer benefits: faster onboarding, better self-service, improved support.
- High-level timeline: internal beta (mid-Nov), public GA (early Dec).
- Visual suggestion: Timeline graphic showing phases and key dates.

**Slide 2: Current State and Challenges**
- Existing onboarding process takes 3–5 days on average.
- Customer feedback highlights confusion and lack of self-service options.
- Support team spends 60% of time on onboarding-related issues.
- Visual suggestion: Bar chart comparing current vs. target onboarding time.

**Slide 3: Proposed Solution Overview**
- New onboarding platform with improved flow and self-service capabilities.
- Phased rollout: internal beta → stabilization → public GA.
- Expected outcomes: 40% faster onboarding, reduced support load.
- Visual suggestion: Architecture diagram showing new onboarding flow.

**Slide 4: Phased Rollout Plan**
- Phase 1 (Internal Beta): Nov 18–29, 50 internal users, feedback collection.
- Phase 2 (Stabilization): Nov 30–Dec 4, fixes and final validation.
- Phase 3 (Public GA): Dec 5 (or Dec 12 contingency).
- Visual suggestion: Gantt chart showing phases and milestones.

**Slide 5: Success Criteria for Internal Beta**
- Zero critical incidents during beta period.
- Support documentation reviewed and approved by support team.
- At least 50 internal users successfully onboarded.
- Visual suggestion: Checklist graphic with success criteria.

**Slide 6: Timeline Risks**
- API timeout issues must be resolved by Nov 22.
- If not resolved, public GA shifts to Dec 12 (1-week delay).
- Support training materials behind schedule; risk to day-1 readiness.
- Visual suggestion: Risk matrix (likelihood vs. impact).

**Slide 7: Customer Impact**
- Faster onboarding reduces time-to-value for customers.
- Self-service options improve customer satisfaction and reduce support burden.
- Early feedback from beta users expected to validate improvements.
- Visual suggestion: Customer quote callout or testimonial.

**Slide 8: Budget and Resource Impact**
- 1-week delay adds ~$15K in engineering and QA costs.
- Additional QA resources requested to accelerate load testing.
- Budget impact is justified by reduced risk of post-launch incidents.
- Visual suggestion: Simple cost comparison table (on-time vs. delayed).

**Slide 9: Go/No-Go Decision Framework**
- Decision meeting scheduled for Dec 2.
- Key criteria: API stability, internal beta feedback, support readiness.
- Clear escalation path if criteria are not met.
- Visual suggestion: Decision tree diagram.

**Slide 10: Next Steps and Approvals Needed**
- Approve phased rollout plan and contingency timeline.
- Allocate additional QA resources for load testing.
- Confirm go/no-go decision process and attendees.
- Visual suggestion: Action items table with owners and dates.
```text

---


## Tips

- Tip 1: Use `[source_document]` to quickly turn a report or Word doc into a presentation without starting from scratch.
- Tip 2: Adjust `[emphasis]` based on your audience's priorities (e.g., execs care about ROI, engineers care about architecture).
- Tip 3: After generating the outline, ask Copilot to "expand slide 5 with more detail" or "suggest alternative visuals for slide 3."
- Tip 4: Copy the outline into PowerPoint's Outline View for fast slide creation.

---

## M365 Copilot Best Practices

- **Use in PowerPoint**: Open Copilot in PowerPoint and say "Create a presentation about [topic]" or paste this prompt with your variables filled in.
- **Reference files**: Use "Create from file" in Copilot to reference a Word document directly, then refine with this prompt.
- **Designer integration**: After creating slides, use PowerPoint Designer (Design Ideas) to apply professional layouts automatically.
- **Iterate with Copilot**: Ask follow-up questions like "Add a slide about risks" or "Make the executive summary more concise."

---

## Related Prompts

- `m365-document-summarizer.md`
- `m365-project-status-reporter.md`
