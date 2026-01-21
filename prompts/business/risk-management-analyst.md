---
name: Risk Management Analyst
description: Enterprise-grade risk analyst using ISO 31000 and PMI PMBOK frameworks for risk identification, quantification, and mitigation.
type: how_to
---

# Risk Management Analyst

## Use Cases

- Capital projects risk assessment (data centers, manufacturing facilities, infrastructure)
- Software implementation risk registers (ERP, CRM, cloud migrations)
- M&A integration risk management
- Regulatory compliance risk analysis (SOC2, ISO27001, GDPR)
- Supply chain and vendor risk evaluation

## Variables

- `[project_name]`: Project name and scope (e.g., "Data Center DC-04 Build - 50MW Hyperscale Facility")
- `[phase]`: Current project phase (e.g., "Construction/Fit-Out Month 8 of 18", "Go-Live Preparation", "Post-Production Support")
- `[concerns]`: Specific risk areas identified (e.g., "Supply chain delays for cooling units, labor strikes, permit delays, anchor tenant retention")
- `[impact]`: Business consequences if risks materialize (e.g., "Critical path delay costs $500K/month in liquidated damages, potential loss of $50M anchor tenant contract")

## 3. Risk Mitigation Strategies

### R-01: CRAC Unit Supply Chain Delay (Priority 1)

**Response Strategy**: **AVOID** + **TRANSFER**

**Primary Mitigation** (Cost: $240K, Timeline: Immediate):

1. **Dual-Source Procurement**: Pre-order 60 units from secondary vendor (Carrier) at 10% premium ($200K).
   - **Rationale**: Vertiv lead time is 10 weeks; Carrier can deliver in 6 weeks.
   - **Risk Reduction**: Probability drops from 70% → 20% (backup units ensure critical path continuity).
2. **Vendor Penalty Clause**: Negotiate $50K/week late delivery penalty with Vertiv (already in contract but not enforced).
3. **Expedited Shipping**: Charter cargo flight if units miss sea freight window ($40K vs. 4-week delay).

**RACI**:

- **Responsible**: Procurement Director
- **Accountable**: Project Manager
- **Consulted**: Construction Manager, Finance
- **Informed**: Steering Committee

**Success Metric**: Confirm secondary vendor PO by Nov 1, 2025.

### R-02: Union Labor Strike (Priority 2)

**Response Strategy**: **TRANSFER** + **MITIGATE**

**Primary Mitigation**:

1. **Labor Agreement Pre-Negotiation**: Engage union rep NOW (before Oct 31 contract expiry) to offer 8% wage increase ($120K total cost vs. $2.5M strike delay).
2. **Non-Union Subcontractor Standby**: Contract backup HVAC team from out-of-state (higher cost but strike-proof).
   - **Cost**: $300K premium vs. union rates.
   - **Risk**: Quality may vary — require same manufacturer certifications (Vertiv-certified installers).
3. **Accelerate HVAC Work**: Fast-track installation schedule to complete critical units BEFORE contract expiry (28 days early finish).

**Trigger Condition for Escalation**: If union rejects offer by Nov 5, activate non-union contractor immediately.

## 4. Contingency Plans

### Contingency Budget Allocation

| Risk | Trigger Condition | Contingency Action | Reserved Budget | Approval Authority |
| ------ | ------------------- | -------------------- | ----------------- | -------------------- |
| R-01 | Vertiv confirms \u003e8-week delay | Activate Carrier backup order | $240K | PM (approved) |
| R-04 | AWS sends cancellation notice | Engage backup tenant pipeline | $2M (revenue gap fund) | CEO |
| R-02 | Union votes to strike (Nov 10) | Deploy non-union contractor | $300K | Construction Mgr |
| R-03 | Permit not issued by Nov 15 | Build alternative grid connection | $150K | PM |

**Total Contingency Reserve**: $2.69M (already allocated in project budget as 8% contingency fund).

## 6. Escalation Protocols

### Escalation Matrix

| Scenario | Immediate Action | Escalation Level | Communication |
| ---------- | ----------------- | ------------------ | --------------- |
| **Red KRI triggered** | PM investigates root cause (within 4 hours) | Level 1: Steering Committee (same day) | Email + emergency meeting |
| **Risk Score increases ≥5 points** | Re-assess mitigation plan | Level 2: Executive Sponsor (within 24 hours) | Written brief + phone call |
| **Contingency budget exceeded** | Halt non-critical spending | Level 3: CEO / CFO (immediate) | Board notification |
| **Anchor tenant sends legal notice** | Engage crisis management team | Level 4: Board of Directors (within 12 hours) | Emergency board session |

### Communication Templates

**Escalation Email (Sample for R-04 Red Alert)**:

```text

Subject: [URGENT] DC-04 Risk Escalation — Anchor Tenant Risk (R-04)

To: Steering Committee
CC: CEO, CFO

RISK ALERT: R-04 (Anchor Tenant Cancellation) has escalated to RED status.

TRIGGER: AWS sent formal notice of concern re: Oct 1 deadline.

IMPACT: $50M contract at risk + $800K/month revenue delay.

IMMEDIATE ACTIONS TAKEN (Last 4 hours):

1. VP Sales scheduled emergency call with AWS VP Infrastructure (today 3pm).
2. Legal reviewing contract amendment options.
3. Backup tenant pipeline activated (Oracle Cloud contacted).

DECISION NEEDED (Within 24 hours):

- Approve CEO-to-CEO escalation call?
- Authorize $500K rent concession for 30-day extension?

NEXT UPDATE: Tomorrow 9am (or sooner if status changes).

[Project Manager Name]

```text

## FMEA (Failure Mode and Effects Analysis) - Optional Deep Dive

For high-complexity risks (e.g., R-05 Generator Testing), use FMEA methodology:

| Failure Mode | Potential Effects | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN (Risk Priority Number) | Mitigation |
| -------------- | ------------------- | ----------------- | ------------------- | ------------------ | ---------------------------- | ------------ |
| Generator fails load test | Cannot achieve required 50MW capacity | 9 | 3 | 2 | **54** | Pre-test with vendor engineer present; backup generator on-site |
| Cooling system leak | Equipment damage, downtime | 8 | 2 | 4 | **64** | Pressure test all lines before commissioning; leak detection sensors |

**RPN Scoring**: Severity × Occurrence × Detection (1-1000 scale)

- **RPN \u003e 100**: Immediate action required
- **RPN 50-100**: High priority mitigation
- **RPN \u003c 50**: Monitor and review quarterly

```

---

## Related Prompts

- [Gap Analysis Expert](../analysis/gap-analysis-expert.md) - For identifying gaps that create risks
- [Crisis Management Coordinator](./crisis-management-coordinator.md) - For managing risk events when they occur
- [Business Strategy Analysis](./business-strategy-analysis.md) - For strategic risk considerations
- [Change Management Coordinator](./change-management-coordinator.md) - For managing change-related risks
- [Stakeholder Communication Manager](./stakeholder-communication-manager.md) - For risk communication to stakeholders

