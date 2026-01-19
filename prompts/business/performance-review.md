---
title: "Performance Review Writer"
shortTitle: "Performance Review"
intro: "Generate constructive, balanced performance reviews with specific feedback, goal tracking, and development recommendations."
type: "how_to"
difficulty: "intermediate"
audience:

  - "project-manager"
  - "business-analyst"

platforms:

  - "github-copilot"
  - "claude"
  - "chatgpt"

topics:

  - "management"
  - "hr"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Performance Review Writer

---

## Description

Create balanced, actionable performance reviews that recognize achievements, address growth areas, and set clear development goals. Generates review content that is fair, specific, and focused on behaviors and outcomes.

---

## Use Cases

- Writing annual or semi-annual performance reviews
- Preparing mid-year check-in documentation
- Creating self-assessment drafts
- Documenting performance improvement plans
- Preparing calibration materials for managers

---

## Prompt

```text
You are an experienced people manager skilled at writing fair, constructive performance reviews.

Write a performance review for:

**Employee**: [employee_info]
**Review Period**: [period]
**Role/Level**: [role]
**Key Accomplishments**: [accomplishments]
**Areas for Growth**: [growth_areas]
**Goals from Last Period**: [previous_goals]
**Overall Rating**: [rating]

Generate:

1. **Executive Summary** (3-4 sentences)
   - Overall performance assessment
   - Key themes for the review period
   - Trajectory (improving, consistent, declining)

2. **Accomplishments & Impact** (4-5 bullets)
   - Specific achievements with measurable outcomes
   - Behaviors that drove success
   - Impact on team/company

3. **Strengths** (3-4 bullets)
   - What they do exceptionally well
   - Examples demonstrating each strength

4. **Development Areas** (2-3 bullets)
   - Growth opportunities with specific examples
   - Constructive framing (behavior-based, not personal)
   - Actionable suggestions

5. **Goal Assessment** (from previous period)
   - Status of each goal (Met/Partially Met/Not Met)
   - Context for any misses

6. **Goals for Next Period** (3-4 goals)
   - SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
   - Mix of performance and development goals

7. **Compensation/Promotion Recommendation** (if applicable)
   - Justification tied to accomplishments

Write in professional but warm tone. Be specific with examples. Avoid vague statements like "good communicator" - show, don't tell.
```text

---

## Variables

- `[employee_info]`: Name, tenure, and any relevant context
- `[period]`: Review period (e.g., "H1 2025", "Annual 2024")
- `[role]`: Current role, level, and team
- `[accomplishments]`: Key achievements and projects from the period
- `[growth_areas]`: Areas where improvement is needed
- `[previous_goals]`: Goals set in the last review cycle
- `[rating]`: Overall rating (e.g., "Exceeds Expectations", "Meets Expectations", "Needs Improvement")

---

## Example

### Context

You are writing a performance review for a senior engineer who recently transitioned into a tech lead role. You have bullet‑point notes on accomplishments and growth areas and want a balanced, structured review.

### Input

```text
You are an experienced people manager skilled at writing fair, constructive performance reviews.

Write a performance review for:

**Employee**: Jordan Lee, 2.5 years at company, transitioned from IC to tech lead 8 months ago
**Review Period**: H2 2024 (July - December)
**Role/Level**: Senior Software Engineer / Tech Lead, Platform Team (5 direct reports)
**Key Accomplishments**:

- Led migration of payment service to new architecture, completed 2 weeks early
- Reduced on-call incidents by 40% through proactive monitoring improvements
- Mentored 2 junior engineers who both got promoted
- Initiated and ran weekly tech talks series (12 sessions, avg 25 attendees)

**Areas for Growth**:

- Struggles to delegate; tends to jump in and fix things rather than coach
- Written communication could be clearer in design docs
- Sometimes avoids difficult conversations with underperformers

**Goals from Last Period**:

1. Complete payment service migration (Q3)
2. Reduce P1 incidents by 25%
3. Develop leadership skills through management training
4. Improve documentation practices

**Overall Rating**: Exceeds Expectations
```text

### Expected Output

The AI generates a review document with an executive summary, detailed accomplishments and impact, strengths, development areas, assessment of previous goals, and SMART goals for the next period written in a fair, coaching‑oriented tone.

---

## Tips

- Lead with specific accomplishments, not personality traits
- Use direct quotes from peers or stakeholders when possible
- Frame development areas as growth opportunities, not failures
- Make goals measurable - "improve communication" is not a goal
- Separate performance (what they did) from potential (what they could do)

---

## Related Prompts

- [interview-questions](./interview-questions.md) - For hiring decisions
- [job-description-writer](./job-description-writer.md) - For role clarity
- [meeting-summary](./meeting-summary.md) - For documenting 1:1 conversations
