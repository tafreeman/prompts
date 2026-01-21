---
name: Crisis Management Coordinator
description: Manages project crises with response plans, stakeholder communication, resource mobilization, and recovery strategy.
type: how_to
---

# Crisis Management Coordinator

## Description

This prompt helps manage project crises by creating structured response plans, stakeholder communications, resource mobilization strategies, and recovery roadmaps. It's designed for project managers and incident commanders who need to coordinate rapid response to critical issues.

## Use Cases

- Coordinating response to major production incidents or outages
- Managing high-impact project delays or deployment failures
- Preparing structured war-room plans for executive stakeholders
- Standardising crisis playbooks across programmes or portfolios
- Capturing post-incident lessons learned and improvements

## Variables

- `[project_name]`: Name of the project or system in crisis (e.g., "Global Payments Platform Migration")
- `[crisis]`: Description of the crisis situation (e.g., "New release caused 18% payment failure rate in EU region")
- `[impact]`: Business impact assessment (e.g., "$250K lost revenue per hour, reputational damage, contract breach risk")
- `[urgency]`: Severity level (e.g., "Critical (SEV-1) – immediate executive visibility required")

## Prompt

### System Prompt

```text
You are a crisis management expert with experience leading incident response for major technology and business disruptions. You help organizations respond effectively to crises with structured communication, rapid decision-making, and recovery planning.
```

### User Prompt

```text
Develop a crisis response plan for [project_name].

Crisis Situation:
- Description: [crisis]
- Business Impact: [impact]
- Severity Level: [urgency]

Please provide:
1. Immediate response actions (first 4 hours)
2. Crisis communication plan by stakeholder
3. War room structure and roles
4. Escalation matrix
5. Recovery timeline and milestones
6. Post-incident review framework
```

## Example

### Input

```text
Develop a crisis response plan for Global Payments Platform Migration.

Crisis Situation:
- Description: New release caused 18% payment failure rate in EU region
- Business Impact: $250K lost revenue per hour, reputational damage, contract breach risk
- Severity Level: Critical (SEV-1) – immediate executive visibility required
```

### Expected Output

```text
## Crisis Response Plan: Payment Platform Failure

### Severity Assessment
- **Level**: SEV-1 (Critical)
- **Impact**: $250K/hour revenue loss + reputational damage
- **Scope**: EU region (40% of transaction volume)
- **Contract Risk**: SLA breach if not resolved within 4 hours

### Immediate Actions (First 4 Hours)
| Time | Action | Owner | Status |
|------|--------|-------|--------|
| T+0 | Activate war room, page on-call | Incident Commander | |
| T+15min | Rollback decision point | Engineering Lead | |
| T+30min | Customer communication drafted | Comms Lead | |
| T+1hr | Executive briefing #1 | IC | |
| T+2hr | Status to affected merchants | Support Lead | |
| T+4hr | Resolution or escalation to CEO | IC | |

### War Room Structure
- **Incident Commander**: Makes final decisions, owns timeline
- **Engineering Lead**: Technical investigation and fix
- **Comms Lead**: All internal/external communications
- **Support Lead**: Customer-facing updates
- **Finance Lead**: Impact quantification

### Communication Cadence
| Audience | Channel | Frequency | Owner |
|----------|---------|-----------|-------|
| Executive Team | Slack #exec-incident | Every 30 min | IC |
| Affected Merchants | Email + Status Page | Every hour | Support |
| All Employees | Slack #company-wide | At resolution | Comms |
| Board | Email from CEO | If >6 hours | CEO |

### Recovery Timeline
- **Hour 0-2**: Contain (rollback or hotfix)
- **Hour 2-4**: Stabilize (confirm fix, monitor)
- **Hour 4-24**: Verify (extended monitoring)
- **Day 2-3**: Root cause analysis
- **Day 5**: Post-incident review
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- [Risk Management Analyst](./risk-management-analyst.md) - For proactive risk identification before crises
- [Stakeholder Communication Manager](./stakeholder-communication-manager.md) - For crisis communications
- [Change Management Coordinator](./change-management-coordinator.md) - For managing organizational change after crisis
- [Business Strategy Analysis](./business-strategy-analysis.md) - For strategic recovery planning
