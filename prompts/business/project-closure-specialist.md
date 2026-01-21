---
name: Project Closure Specialist
description: Manages project closure activities with checklists, deliverable review, stakeholder sign-off, and post-project evaluation.
type: how_to
---

# Project Closure Specialist

## Description

This prompt manages project closure activities including checklists, deliverable reviews, stakeholder sign-offs, and post-project evaluations. It helps project managers ensure proper handoff and capture lessons learned for future projects.

## Use Cases

- Project Closure for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[project_name]`: Project name (e.g., "Website Redesign for Acme Corp")
- `[deliverables]`: Deliverables status (e.g., "All SOW items delivered, SEO audit delayed 1 week")
- `[satisfaction]`: Stakeholder satisfaction (e.g., "Client NPS 9/10, internal team satisfaction 8/10")
- `[lessons]`: Key lessons learned (e.g., "Tool API outage caused delays, need backup tools for critical path")

## Prompt

### System Prompt

```text
You are a project closure expert who ensures projects end properly with complete handoffs, documented lessons, and stakeholder satisfaction. You help teams close projects in a way that sets up future success.
```

### User Prompt

```text
Create a project closure plan for [project_name].

Closure Context:
- Deliverables Status: [deliverables]
- Stakeholder Satisfaction: [satisfaction]
- Lessons Learned: [lessons]

Please provide:
1. Closure checklist with owners
2. Deliverables sign-off matrix
3. Outstanding items and resolution plan
4. Lessons learned documentation
5. Knowledge transfer plan
6. Celebration and recognition recommendations
7. Post-project support transition
```

## Example

### Input

```text
Create a project closure plan for Website Redesign for Acme Corp.

Closure Context:
- Deliverables Status: All SOW items delivered, SEO audit delayed 1 week
- Stakeholder Satisfaction: Client NPS 9/10, internal team satisfaction 8/10
- Lessons Learned: Tool API outage caused delays, need backup tools for critical path
```

### Expected Output

```text
## Project Closure Plan: Acme Corp Website Redesign

### Closure Checklist
| Task | Owner | Status | Due Date |
|------|-------|--------|----------|
| Final deliverable review | PM | ✅ Complete | - |
| Client sign-off meeting | PM | 🟡 Scheduled | Jan 20 |
| Invoice all remaining milestones | Finance | ⏳ Pending | Jan 22 |
| Archive project files | PM | ⏳ Pending | Jan 25 |
| Update portfolio/case study | Marketing | ⏳ Pending | Jan 30 |
| Lessons learned session | PM | 🟡 Scheduled | Jan 18 |
| Team recognition | Director | ⏳ Pending | Jan 24 |

### Deliverables Sign-Off Matrix
| Deliverable | Status | Client Approval | Date |
|-------------|--------|-----------------|------|
| Homepage redesign | ✅ Delivered | ✅ Approved | Jan 5 |
| 25 page templates | ✅ Delivered | ✅ Approved | Jan 10 |
| Mobile responsive design | ✅ Delivered | ✅ Approved | Jan 10 |
| SEO audit | 🟡 In progress | ⏳ Pending | Jan 22 |
| Analytics setup | ✅ Delivered | ✅ Approved | Jan 12 |

### Outstanding Items
| Item | Resolution | Owner | ETA |
|------|------------|-------|-----|
| SEO audit | Complete and deliver | SEO Lead | Jan 22 |
| Training video updates | Record new UI screens | Designer | Jan 20 |

### Lessons Learned Summary
| Category | Lesson | Recommendation |
|----------|--------|----------------|
| Risk | Tool API outage caused 3-day delay | Identify backup tools for critical path dependencies |
| Scope | Mid-project scope additions strained timeline | Enforce change request process earlier |
| Success | Weekly client syncs built strong trust | Continue for all client projects |

### Knowledge Transfer
| Knowledge Area | Document | Recipient | Date |
|----------------|----------|-----------|------|
| CMS admin guide | Wiki article | Acme IT team | Jan 18 |
| Analytics dashboards | Training video | Acme Marketing | Jan 20 |
| Design system | Figma library | Acme Design | Jan 18 |

### Recognition
- **Team lunch**: Friday Jan 24
- **Shoutouts**: Company all-hands mention for on-time delivery
- **Bonus consideration**: Designer and Dev Lead went above and beyond
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
