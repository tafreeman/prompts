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

## Example Usage

**Input:**

```text
Employee: Jordan Lee, 2.5 years at company, transitioned from IC to tech lead 8 months ago
Review Period: H2 2024 (July - December)
Role/Level: Senior Software Engineer / Tech Lead, Platform Team (5 direct reports)
Key Accomplishments:
- Led migration of payment service to new architecture, completed 2 weeks early
- Reduced on-call incidents by 40% through proactive monitoring improvements
- Mentored 2 junior engineers who both got promoted
- Initiated and ran weekly tech talks series (12 sessions, avg 25 attendees)
Areas for Growth:
- Struggles to delegate; tends to jump in and fix things rather than coach
- Written communication could be clearer in design docs
- Sometimes avoids difficult conversations with underperformers
Previous Goals:
1. Complete payment service migration (Q3)
2. Reduce P1 incidents by 25%
3. Develop leadership skills through management training
4. Improve documentation practices
Overall Rating: Exceeds Expectations
```text
**Output:**

```markdown
# Performance Review: Jordan Lee

**Review Period**: H2 2024 (July - December)  
**Role**: Senior Software Engineer / Tech Lead, Platform Team  
**Manager**: [Manager Name]  
**Overall Rating**: Exceeds Expectations ⭐⭐⭐⭐

---

## Executive Summary

Jordan has had an outstanding first year as a Tech Lead, successfully navigating the transition from individual contributor while delivering exceptional technical results. The payment service migration—completed two weeks early—demonstrated Jordan's ability to lead complex, high-stakes projects. Areas for continued development include delegation and navigating difficult performance conversations, which are natural growth edges for new leaders. Jordan is on a strong trajectory and is a high-potential leader for our organization.

---

## Accomplishments & Impact

### Payment Service Migration (Exceeds Expectations)
Led the end-to-end migration of our payment processing service to the new architecture. Project was delivered **2 weeks ahead of schedule** with zero production incidents during cutover. This reduced latency by 35% and positioned us for 3x transaction volume growth.

*"Jordan's technical leadership on this project was exceptional. They anticipated risks we hadn't considered and created contingency plans that saved us during the final migration week."* — VP Engineering

### Operational Excellence
Implemented proactive monitoring and alerting improvements that reduced P1 on-call incidents by **40% (from 12/month to 7/month)**. This directly improved team morale and reduced burnout during the holiday peak period.

### People Development
Mentored two junior engineers (Alex and Sam) who both received promotions this cycle. Jordan invested significant time in 1:1s, pair programming, and creating stretch opportunities. Both mentees cited Jordan as instrumental to their growth.

### Culture Building
Initiated and ran the Platform Team's weekly tech talks series—12 sessions with an average of 25 attendees. Topics ranged from distributed systems patterns to career development. This has become a highlight of our engineering culture.

### Cross-Team Collaboration
Partnered effectively with the Security team on PCI compliance requirements during the migration. Jordan's collaborative approach turned a potentially contentious review process into a smooth partnership.

---

## Strengths

### Technical Leadership
Jordan combines deep technical expertise with the ability to communicate complex concepts clearly. During the payment migration, they made architectural decisions that balanced immediate delivery with long-term maintainability. Team members consistently seek Jordan's guidance on technical challenges.

### Mentorship & Development
Jordan genuinely invests in others' growth. The promotion of two mentees is evidence of this, but the impact goes beyond metrics—Jordan creates psychological safety that enables junior engineers to take risks and learn from mistakes.

### Ownership Mentality
When Jordan commits to something, it gets done. The early delivery of the payment migration wasn't luck—it was the result of meticulous planning, risk identification, and proactive problem-solving. Jordan treats team deliverables as personal commitments.

### Initiative
Jordan doesn't wait for permission to improve things. The tech talks series, monitoring improvements, and documentation initiatives all came from Jordan identifying opportunities and driving them forward independently.

---

## Development Areas

### Delegation & Empowerment
Jordan's high standards and ownership mentality can sometimes work against them as a leader. There were several instances this period where Jordan jumped in to fix problems rather than coaching team members through the solution.

*Example*: During the October database incident, Jordan took over debugging rather than letting Sam (who was on-call) work through it with guidance. While this resolved the incident faster, it missed a development opportunity.

**Suggestion**: Practice the "ask three questions before giving the answer" technique. When a team member brings a problem, ask clarifying questions that guide them to the solution rather than providing it directly.

### Written Communication
Jordan's verbal communication is strong, but design documents sometimes lack the clarity needed for async decision-making. The initial payment migration RFC required significant revision before stakeholders could provide meaningful feedback.

**Suggestion**: Use the "5-minute test"—have someone unfamiliar with the project read the doc for 5 minutes and summarize the proposal. If they can't, the doc needs simplification.

### Difficult Conversations
Jordan has avoided addressing performance concerns with one team member whose output has declined. While Jordan provides excellent positive feedback, there's room to grow in delivering constructive criticism directly.

**Suggestion**: Prepare for difficult conversations using the SBI framework (Situation-Behavior-Impact). Practice with your manager before the actual conversation. Remember that avoiding feedback isn't kind—it prevents the person from improving.

---

## Goal Assessment (H1 2024 Goals)

| Goal | Status | Notes |
| :--- |--------| :--- |
| Complete payment service migration by end of Q3 | ✅ **Exceeded** | Delivered 2 weeks early with zero incidents |
| Reduce P1 incidents by 25% | ✅ **Exceeded** | Achieved 40% reduction |
| Complete management training program | ✅ **Met** | Completed "New Manager Foundations" course + leadership book club |
| Improve documentation practices | ⚠️ **Partially Met** | Created team documentation standards but personal doc quality still inconsistent |

---

## Goals for H1 2025

### Goal 1: Develop Team's Technical Independence (Development)
**Objective**: Enable team members to resolve complex technical issues without Jordan's direct involvement.  
**Key Results**:
- By end of Q1, create and document decision frameworks for the 3 most common technical decisions the team makes
- Reduce Jordan's involvement in incident resolution by 50% (measure via on-call handoff logs)
- Have 2 team members lead RFC reviews independently by end of H1

### Goal 2: Lead Platform Reliability Initiative (Performance)
**Objective**: Own the Platform team's reliability roadmap and deliver measurable improvements.  
**Key Results**:
- Achieve 99.95% uptime for payment service (current: 99.9%)
- Reduce mean-time-to-resolution (MTTR) from 45 min to 30 min
- Complete post-incident review process improvements by end of Q1

### Goal 3: Grow as a People Leader (Development)
**Objective**: Build skills in performance management and career development conversations.  
**Key Results**:
- Complete "Crucial Conversations" training by end of Q1
- Deliver at least one piece of constructive feedback to each direct report by end of Q1 (documented in 1:1 notes)
- Partner with HR on a performance improvement plan if needed (don't avoid the conversation)

### Goal 4: Expand Organizational Impact (Stretch)
**Objective**: Contribute beyond the Platform team to engineering-wide initiatives.  
**Key Results**:
- Present at one company-wide engineering all-hands
- Mentor one engineer outside of Platform team
- Contribute to at least one cross-team RFC or architecture decision

---

## Compensation Recommendation

**Recommendation**: 8% merit increase + refresh equity grant

**Justification**: Jordan has performed at the top of the Senior Engineer / Tech Lead band this period. The payment migration alone would justify strong performance, but combined with the operational improvements, people development, and culture contributions, Jordan is clearly exceeding expectations. The merit increase recognizes current performance; the equity refresh recognizes Jordan's trajectory as a future engineering leader.

**Promotion Consideration**: Jordan is not yet ready for Staff Engineer / Engineering Manager, but should be considered in the next 12-18 months if delegation and performance management skills continue to develop.

---

## Manager's Closing Note

Jordan, I'm incredibly proud of what you've accomplished this period. The transition from IC to Tech Lead is one of the hardest in engineering, and you've navigated it with grace and impact. Your technical excellence is clear, but what impresses me most is how much you care about the people around you—the promotions of Alex and Sam are direct reflections of your investment.

The development areas I've highlighted aren't weaknesses—they're the natural growth edges of a new leader with high standards. The fact that you want to fix things yourself comes from a good place. Our work together in H1 will be about channeling that energy into developing others.

I'm excited to see you continue to grow. You're on track for significant leadership opportunities at this company.

— [Manager Name]
```text

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
