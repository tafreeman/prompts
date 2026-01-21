---
name: Stakeholder Communication Manager
description: Strategic communications specialist for complex stakeholder management with executive updates and crisis communication.
type: how_to
---

# Stakeholder Communication Manager

## Description

This prompt serves as a strategic communications specialist for complex stakeholder management, including executive updates, change communications, and crisis messaging. It helps project leaders maintain alignment and trust across diverse stakeholder groups.

## Use Cases

- Quarterly executive board updates for technical transformation projects
- Change management communications for ERP/CRM migrations
- Crisis communication during service outages or project delays
- Multi-stakeholder alignment for cross-functional initiatives
- Vendor/partner relationship communication management

## Variables

- `[project_name]`: Project name and scope (e.g., "SAP S/4HANA Implementation - Finance & Supply Chain Modules")
- `[stakeholders]`: List of stakeholder groups with roles (e.g., "CFO (Sponsor), VP Supply Chain (Key User), IT Director, Warehouse Staff (End Users)")
- `[phase]`: Current project phase (e.g., "Blueprinting/Design", "UAT", "Go-Live", "Post-Production Support")
- `[challenges]`: Specific communication obstacles (e.g., "Resistance to change from warehouse staff, CFO demanding faster ROI visibility, offshore vendor language barriers")

## Prompt

### System Prompt

```text
You are a strategic communications expert with experience managing complex stakeholder relationships in large transformation programs. You help leaders craft the right message for the right audience at the right time.
```

### User Prompt

```text
Develop a stakeholder communication plan for [project_name].

Communication Context:
- Stakeholder Groups: [stakeholders]
- Current Phase: [phase]
- Communication Challenges: [challenges]

Please provide:
1. Stakeholder analysis matrix (power/interest)
2. Key messages by stakeholder group
3. Communication cadence and channels
4. RACI for communication ownership
5. Escalation and issue management process
6. Feedback collection mechanisms
7. Success metrics
```

## Example

### Input

```text
Develop a stakeholder communication plan for SAP S/4HANA Implementation - Finance & Supply Chain Modules.

Communication Context:
- Stakeholder Groups: CFO (Sponsor), VP Supply Chain (Key User), IT Director, Warehouse Staff (End Users)
- Current Phase: Blueprinting/Design
- Communication Challenges: Resistance to change from warehouse staff, CFO demanding faster ROI visibility, offshore vendor language barriers
```

### Expected Output

```text
## Stakeholder Communication Plan: SAP S/4HANA Implementation

### Stakeholder Analysis Matrix
| Stakeholder | Power | Interest | Strategy | Risk |
|-------------|-------|----------|----------|------|
| CFO | High | High | Manage Closely | Low |
| VP Supply Chain | High | High | Manage Closely | Medium |
| IT Director | Medium | High | Keep Informed | Low |
| Warehouse Staff | Low | High | Build Support | High |
| Offshore Vendor | Medium | Medium | Keep Satisfied | Medium |

### Key Messages by Audience

| Audience | Core Message | Tone | Frequency |
|----------|--------------|------|------------|
| CFO | ROI tracking, milestone progress, risk status | Executive, data-driven | Bi-weekly |
| VP Supply Chain | Process improvements, user readiness | Collaborative, detailed | Weekly |
| Warehouse Staff | "What's in it for me" - easier processes, better tools | Empathetic, simple | Weekly |
| IT Director | Technical progress, integration status | Technical, specific | Weekly |

### Communication Cadence
| Communication | Audience | Channel | Frequency | Owner |
|---------------|----------|---------|-----------|-------|
| Executive Dashboard | CFO | Email + PPT | Bi-weekly | PM |
| Steering Committee | Leadership | Meeting | Monthly | Sponsor |
| Team Updates | Project Team | Slack/Teams | Daily | PM |
| Town Halls | All Impacted | Virtual meeting | Monthly | Change Lead |
| Floor Huddles | Warehouse | In-person | Weekly | Super Users |

### Communication RACI
| Activity | Project Manager | Sponsor | Change Lead | IT |
|----------|-----------------|---------|-------------|-----|
| Exec Updates | R | A | C | I |
| User Communications | C | I | R | I |
| Technical Updates | R | I | I | A |
| Crisis Communications | C | A | R | C |

### Addressing Communication Challenges

| Challenge | Strategy |
|-----------|----------|
| Warehouse resistance | Super-user program, floor presence, "what's in it for me" messaging |
| CFO ROI pressure | Monthly ROI dashboard with leading indicators |
| Offshore language | Video calls with visuals, written follow-ups, simple English |

### Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Stakeholder satisfaction | >80% | Monthly survey |
| Message reach | 100% | Open rates, attendance |
| "Surprised by issue" incidents | Zero | Tracking log |
| Super-user adoption | 100% trained | Training completion |
```

## Tips

- **Tailor Messaging to Decision Authority**: Executives want ROI and risk; end users want "What's in it for me?" (WIIFM). Never use the same message for both audiences.
- **Use RACI to Clarify Ownership**: Ambiguous accountability kills stakeholder trust. Make it explicit who owns each communication stream.
- **Schedule Communication Cadence BEFORE Project Start**: Don't improvise. Lock in meeting rhythms (weekly, bi-weekly, monthly) and publish a 6-month calendar.
- **Over-Communicate During Crisis**: If the project is at risk, triple your communication frequency. Silence breeds speculation and panic.
- **Measure Effectiveness, Not Just Activity**: Don't just track "emails sent." Track stakeholder satisfaction, survey scores, and "surprised by issue" incidents.
- **Leverage Asynchronous Tools for Offshore Teams**: Record Loom videos, use Miro for design reviews, and post meeting summaries in Confluence to bridge time zones.
- **Celebrate Wins Publicly**: Monthly pizza parties, shoutouts in newsletters, and "Contributor of the Month" awards build momentum and morale.

---

## Related Prompts

- **[change-management-coordinator](./change-management-coordinator.md)** - For deeper change management playbooks
- **[risk-management-analyst](./risk-management-analyst.md)** - For quantifying communication risks
- **[agile-sprint-planner](./agile-sprint-planner.md)** - For structuring communication around sprints

