---
name: Change Management Coordinator
description: Manages project changes with impact analysis, approval workflow, communication strategy, and implementation planning.
type: how_to
---

# Change Management Coordinator

## Description

This prompt helps manage project changes through structured impact analysis, approval workflows, communication strategies, and implementation planning. It's designed for project managers coordinating change requests across multiple teams and preparing materials for Change Advisory Board reviews.

## Use Cases

- Managing scope changes in large transformation or migration projects
- Coordinating change requests across multiple teams or vendors
- Preparing materials for Change Advisory Board (CAB) reviews
- Standardizing how change impact is documented across projects
- Turning ad-hoc change emails into formal, trackable change records

## Variables

- `[project_name]`: Project name (e.g., "CRM System Migration", "Cloud Infrastructure Upgrade", "ERP Implementation Phase 2")
- `[changes]`: Proposed changes (e.g., "Migration from Salesforce to Microsoft Dynamics 365, affecting 500 users across 3 departments")
- `[impact]`: Impact assessment (e.g., "2-week data migration window, 40 hours training required, $200K budget impact")
- `[concerns]`: Stakeholder concerns (e.g., "Sales team worried about data loss during Q4, IT concerned about integration with legacy inventory system")

## Prompt

### System Prompt

```text
You are an experienced change management professional with expertise in organizational change, project governance, and stakeholder management. You help organizations navigate complex changes while minimizing disruption and maximizing adoption.
```

### User Prompt

```text
Develop a change management plan for [project_name].

Change Context:
- Proposed Changes: [changes]
- Impact Assessment: [impact]
- Stakeholder Concerns: [concerns]

Please provide:
1. Change impact analysis (scope, timeline, resources, risk)
2. Stakeholder analysis and engagement strategy
3. Communication plan with key messages by audience
4. Training and support requirements
5. Implementation timeline with milestones
6. Success metrics and adoption KPIs
7. Rollback plan if needed
```

## Example

### Input

```text
Develop a change management plan for CRM System Migration.

Change Context:
- Proposed Changes: Migration from Salesforce to Microsoft Dynamics 365, affecting 500 users across 3 departments
- Impact Assessment: 2-week data migration window, 40 hours training required, $200K budget impact
- Stakeholder Concerns: Sales team worried about data loss during Q4, IT concerned about integration with legacy inventory system
```

### Expected Output

```text
## Change Management Plan: CRM Migration

### Change Impact Analysis
| Dimension | Impact | Severity |
|-----------|--------|----------|
| Users | 500 across Sales, Marketing, Support | High |
| Timeline | 2-week migration + 4-week stabilization | Medium |
| Budget | $200K direct + $50K contingency | Medium |
| Business | Q4 sales risk if timing wrong | Critical |

### Stakeholder Engagement Matrix
| Stakeholder | Concern | Strategy | Owner |
|-------------|---------|----------|-------|
| Sales Leadership | Data loss, Q4 impact | Early pilot, Q1 go-live | PMO |
| IT | Legacy integration | Dedicated API dev sprint | IT Director |
| End Users | Learning curve | Extended training, super-user program | Change Lead |

### Communication Plan
| Audience | Message | Channel | Timing |
|----------|---------|---------|--------|
| All Hands | Why we're changing | Town Hall | Week 1 |
| Sales | Your data is safe | Department meeting | Week 2 |
| Power Users | You'll help lead this | 1:1 meetings | Week 2-3 |

### Training Plan
- **Self-paced**: 8 hours online modules (mandatory)
- **Live workshops**: 4 hours hands-on (by role)
- **Super-user certification**: 20 hours advanced training

### Timeline
- **Month 1**: Planning, stakeholder alignment
- **Month 2**: Infrastructure setup, pilot group training
- **Month 3**: Pilot with 50 users, iterate
- **Month 4 (Jan)**: Full rollout post-Q4

### Rollback Plan
- Maintain Salesforce read-only for 90 days post-migration
- Daily data sync backup during transition
- Rollback trigger: >20% data discrepancy or >30% user escalations
```

## Tips

- **Avoid Q4 disruption**: Schedule major CRM changes during slower business periods (January is ideal for many organizations)
- **Train early, train often**: Give users 2+ weeks in sandbox before go-live to build muscle memory
- **Test integrations rigorously**: 80% of migration failures come from third-party connectors, not core data migration
- **Build rollback plans**: Always have a "return to old system" script ready for first 48 hours post-migration
- **Over-communicate**: Send 3x more updates than you think necessary—change anxiety is real
- **Budget 15% contingency**: Migrations always have unforeseen costs (API limits, additional licenses, custom development)
- **Celebrate wins**: Recognize early adopters and power users to build positive momentum

---

## Related Prompts

- **[agile-sprint-planner](./agile-sprint-planner.md)** - Plan migration work in 2-week sprints
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - Craft executive updates and user notifications
- **[risk-management-analyst](./risk-management-analyst.md)** - For change-related risk assessment
- **[Gap Analysis Expert](../analysis/gap-analysis-expert.md)** - For current/future state assessment
- **[Process Optimization Consultant](../analysis/process-optimization-consultant.md)** - For process improvements during change

