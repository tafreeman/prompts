---
name: Performance Review Writer
description: Generate constructive, balanced performance reviews with specific feedback, goal tracking, and development recommendations.
type: how_to
---

# Performance Review Writer

## Description

This prompt generates constructive, balanced performance reviews with specific feedback, goal tracking, and development recommendations. It helps managers write reviews that are fair, actionable, and growth-oriented.

## Use Cases

- Writing annual or semi-annual performance reviews
- Preparing mid-year check-in documentation
- Creating self-assessment drafts
- Documenting performance improvement plans
- Preparing calibration materials for managers

## Variables

- `[employee_info]`: Name, tenure, and any relevant context
- `[period]`: Review period (e.g., "H1 2025", "Annual 2024")
- `[role]`: Current role, level, and team
- `[accomplishments]`: Key achievements and projects from the period
- `[growth_areas]`: Areas where improvement is needed
- `[previous_goals]`: Goals set in the last review cycle
- `[rating]`: Overall rating (e.g., "Exceeds Expectations", "Meets Expectations", "Needs Improvement")

## Prompt

### System Prompt

```text
You are an HR specialist who helps managers write fair, constructive performance reviews. You focus on specific behaviors and outcomes rather than personality traits, and you frame development areas as growth opportunities.
```

### User Prompt

```text
Write a performance review for the following employee:

Employee Details:
- Name/Context: [employee_info]
- Review Period: [period]
- Role: [role]
- Key Accomplishments: [accomplishments]
- Growth Areas: [growth_areas]
- Previous Goals: [previous_goals]
- Recommended Rating: [rating]

Please provide:
1. Executive summary (2-3 sentences)
2. Accomplishments with specific impact
3. Goals assessment from previous cycle
4. Development areas with constructive framing
5. Goals for next cycle (SMART format)
6. Development recommendations
7. Overall rating justification
```

## Example

### Input

```text
Write a performance review for the following employee:

Employee Details:
- Name/Context: Alex Chen, 2 years tenure, promoted to Senior last cycle
- Review Period: H1 2025
- Role: Senior Software Engineer, Platform Team
- Key Accomplishments: Led migration to Kubernetes, reduced deploy time 70%, mentored 2 junior engineers
- Growth Areas: Needs to improve cross-team communication, sometimes misses deadlines on documentation
- Previous Goals: Complete K8s migration (done), improve code review turnaround (improved), lead a project (done)
- Recommended Rating: Exceeds Expectations
```

### Expected Output

```text
## Performance Review: Alex Chen
**Period**: H1 2025 | **Role**: Senior Software Engineer | **Rating**: Exceeds Expectations

### Executive Summary
Alex has had an exceptional first half of 2025, successfully leading the Kubernetes migration that delivered significant business value. He has grown into the Senior role, demonstrating technical leadership and mentorship while identifying clear areas for continued development.

### Key Accomplishments
| Accomplishment | Impact | Evidence |
|----------------|--------|----------|
| Led Kubernetes migration | Deploy time reduced 70% (4 hrs → 1.2 hrs) | Project delivered on time, under budget |
| Mentored 2 junior engineers | Both promoted to mid-level | Feedback: "Alex made me a better engineer" |
| Reduced on-call incidents | 40% reduction in P1 incidents | Improved monitoring and alerting |

### Previous Goals Assessment
| Goal | Status | Notes |
|------|--------|-------|
| Complete K8s migration | ✅ Achieved | Delivered 2 weeks early |
| Improve code review turnaround | ✅ Achieved | From 48 hrs to 12 hrs average |
| Lead a project end-to-end | ✅ Achieved | K8s migration leadership |

### Development Areas
**Cross-Team Communication**
Alex sometimes moves quickly on technical decisions without looping in dependent teams. In the K8s migration, the QA team learned about environment changes late, causing 2 days of test delays.

*Growth opportunity*: Develop a stakeholder communication checklist for major changes. Schedule bi-weekly syncs with dependent teams on large projects.

**Documentation Timeliness**
Technical documentation is high quality but often delivered after project completion rather than alongside it.

*Growth opportunity*: Build documentation into sprint planning as explicit tasks with deadlines.

### Goals for H2 2025
1. **Lead Platform API redesign** (Q3-Q4) - Own end-to-end delivery including stakeholder alignment
2. **Improve cross-team communication score** - Target: 8/10 on peer feedback (current: 6/10)
3. **Documentation concurrent with delivery** - Zero documentation debt at project completion

### Rating Justification
Alex exceeded expectations by delivering high-impact technical work, growing as a mentor, and demonstrating ownership. Development areas are normal growth edges for a newer Senior engineer and don't diminish the exceptional contributions.
```

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
