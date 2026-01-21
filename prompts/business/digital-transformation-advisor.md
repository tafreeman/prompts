---
name: Digital Transformation Advisor
description: Guides digital transformation initiatives with maturity assessment, technology roadmaps, and change management.
type: how_to
---

# Digital Transformation Advisor

## Description

This prompt guides organizations through digital transformation initiatives by providing maturity assessments, technology roadmaps, and change management strategies. It helps leaders plan and execute transformation programs that modernize operations and deliver measurable business value.

## Use Cases

- Defining a digital transformation strategy for a specific business unit or enterprise
- Preparing transformation proposals and roadmaps for executive approval
- Structuring discovery workshops and follow-up materials with clients
- Comparing alternative transformation paths under different budget scenarios
- Documenting success metrics and KPIs for transformation governance

## Variables

- `[organization]`: Organization name and description (e.g., "Guardian Mutual Insurance – mid-size P&C insurer")
- `[current_state]`: Current situation (e.g., "Legacy mainframe claims system, 21-day average cycle time")
- `[goals]`: Transformation objectives (e.g., "Reduce claims cycle to 5 days, enable digital self-service")
- `[budget]`: Available budget (e.g., "$8M over 3 years")
- `[timeline]`: Target timeline (e.g., "Phase 1 in 12 months, full rollout in 36 months")

## Prompt

### System Prompt

```text
You are a digital transformation advisor with expertise in enterprise technology modernization, change management, and business process optimization. You help organizations navigate complex transformations while managing risk and delivering measurable ROI.
```

### User Prompt

```text
Develop a digital transformation strategy for [organization].

Transformation Context:
- Current State: [current_state]
- Transformation Goals: [goals]
- Budget: [budget]
- Timeline: [timeline]

Please provide:
1. Digital maturity assessment
2. Transformation vision and objectives
3. Technology roadmap with phases
4. Change management strategy
5. Investment priorities and ROI projections
6. Risk assessment and mitigation
7. Success metrics and governance model
```

## Example

### Input

```text
Develop a digital transformation strategy for Guardian Mutual Insurance – mid-size P&C insurer.

Transformation Context:
- Current State: Legacy mainframe claims system, 21-day average cycle time
- Transformation Goals: Reduce claims cycle to 5 days, enable digital self-service
- Budget: $8M over 3 years
- Timeline: Phase 1 in 12 months, full rollout in 36 months
```

### Expected Output

```text
## Digital Transformation Strategy: Guardian Mutual Insurance

### Digital Maturity Assessment
| Dimension | Current | Target | Gap |
|-----------|---------|--------|-----|
| Claims Processing | Level 1 (Manual) | Level 4 (Automated) | High |
| Customer Experience | Level 2 (Basic) | Level 4 (Omnichannel) | High |
| Data & Analytics | Level 1 (Siloed) | Level 3 (Integrated) | Medium |
| Technology | Level 1 (Legacy) | Level 3 (Cloud-native) | High |

### Transformation Vision
"Become the fastest, most customer-friendly insurer in our market through digital-first claims processing and self-service capabilities."

### Technology Roadmap

**Phase 1: Foundation (Months 1-12) - $3M**
- Cloud infrastructure setup (AWS/Azure)
- Claims system API layer for legacy integration
- Customer portal MVP with status tracking
- *Outcome*: Claims visibility, 21 → 14 days

**Phase 2: Automation (Months 13-24) - $3M**
- AI-powered claims triage and routing
- Document digitization and OCR
- Mobile app launch
- *Outcome*: 14 → 7 days, 40% self-service

**Phase 3: Optimization (Months 25-36) - $2M**
- Predictive analytics for fraud detection
- Straight-through processing for simple claims
- Legacy system sunset
- *Outcome*: 7 → 5 days, 70% self-service

### ROI Projection
| Metric | Current | Year 3 | Value |
|--------|---------|--------|-------|
| Claims Cycle | 21 days | 5 days | $2M/year cost savings |
| Customer Satisfaction | 65% | 85% | 15% retention improvement |
| Self-Service | 5% | 70% | $1.5M/year call center savings |
| **Total 3-Year ROI** | | | **$10.5M** |
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- [Business Process Reengineering](./business-process-reengineering.md) - For process transformation components
- [Change Management Coordinator](./change-management-coordinator.md) - For managing digital change adoption
- [Process Optimization Consultant](../analysis/process-optimization-consultant.md) - For optimizing digital workflows
- [Gap Analysis Expert](../analysis/gap-analysis-expert.md) - For current/future state technology analysis
