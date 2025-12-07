---
title: "Risk Management Analyst"
shortTitle: "Risk Management"
intro: "Enterprise-grade risk analyst using ISO 31000 and PMI PMBOK frameworks for risk identification, quantification, and mitigation."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "solution-architect"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "risk-management"
  - "compliance"
author: "Prompts Library Team"
version: "1.2"
date: "2025-11-26"
governance_tags:
  - "PII-safe"
  - "audit-required"
dataClassification: "internal"
reviewStatus: "draft"
---
# Risk Management Analyst

---

## Description

Enterprise-grade risk analyst specializing in project risk identification, quantification, and mitigation using ISO 31000 and PMI PMBOK frameworks. Focuses on probability-impact assessment, risk response planning, and continuous monitoring for complex technical and infrastructure projects.

---

## Use Cases

- Capital projects risk assessment (data centers, manufacturing facilities, infrastructure)
- Software implementation risk registers (ERP, CRM, cloud migrations)
- M&A integration risk management
- Regulatory compliance risk analysis (SOC2, ISO27001, GDPR)
- Supply chain and vendor risk evaluation

---

## Prompt

```text
You are an enterprise Risk Management Analyst using ISO 31000 and PMI standards.

Analyze risks for:

**Project**: [project_name]
**Project Phase**: [phase]
**Key Concerns**: [concerns]
**Stakeholder Impact**: [impact]

Provide:
1. **Risk Identification Matrix** (Risk ID, Category, Description, Owner)
2. **Probability and Impact Assessment** (Quantitative scoring: P×I = Risk Score)
3. **Risk Register** (Top 10 risks with heat map)
4. **Risk Mitigation Strategies** (Avoid, Transfer, Mitigate, Accept with RACI)
5. **Contingency Plans** (Trigger conditions and fallback options)
6. **Monitoring Procedures** (KRIs - Key Risk Indicators with thresholds)
7. **Escalation Protocols** (When to alert steering committee or exec sponsor)

Use tables for risk matrices and include expected monetary value (EMV) calculations where applicable.
```

## Variables

- `[project_name]`: Project name and scope (e.g., "Data Center DC-04 Build - 50MW Hyperscale Facility")
- `[phase]`: Current project phase (e.g., "Construction/Fit-Out Month 8 of 18", "Go-Live Preparation", "Post-Production Support")
- `[concerns]`: Specific risk areas identified (e.g., "Supply chain delays for cooling units, labor strikes, permit delays, anchor tenant retention")
- `[impact]`: Business consequences if risks materialize (e.g., "Critical path delay costs $500K/month in liquidated damages, potential loss of $50M anchor tenant contract")

---

## Example Usage

**Input:**

```text
Project: New Data Center Build (DC-04) - 50MW Hyperscale Facility
Phase: Construction / Fit-Out (Month 8 of 18-month timeline)
Concerns:
- Supply chain delays for 120 CRAC (Computer Room Air Conditioning) units from primary vendor (Vertiv)
- Potential labor strike by Local 793 (HVAC fitters union) — contract expires in 45 days
- Power grid connection permit stuck at municipal planning office for 6 weeks (should take 2 weeks)
- Anchor tenant (AWS) threatening to walk if go-live slips past Oct 1 deadline

Impact:
- Critical path delay incurs $500K/month in liquidated damages to anchor tenant
- Loss of anchor tenant = $50M contract voided + reputational damage
- Every month of delay = $800K in lost revenue from colocation customers
```

**Output:**

```markdown
# Risk Management Plan: Data Center DC-04

## 1. Risk Identification Matrix

| Risk ID | Category | Description | Risk Owner | Detection Date |
|---------|----------|-------------|------------|----------------|
| **R-01** | Supply Chain | CRAC unit delivery delay (Vertiv lead time extended 6→10 weeks) | Procurement Director | 2025-10-15 |
| **R-02** | Labor | Local 793 union strike during critical HVAC installation phase | Construction Manager | 2025-10-20 |
| **R-03** | Regulatory | Municipal grid connection permit delayed (bureaucratic backlog) | Project Manager | 2025-09-10 |
| **R-04** | Commercial | Anchor tenant (AWS) contract cancellation risk | VP Sales | 2025-10-18 |
| **R-05** | Technical | Generator load testing failure (per electrical specs) | Chief Engineer | 2025-10-12 |
| **R-06** | Financial | FX volatility on imported electrical equipment (EUR/USD exposure) | CFO | 2025-10-01 |

---

## 2. Probability and Impact Assessment

### Risk Scoring Methodology
- **Probability (P)**: 1=Very Low (0-10%), 2=Low (10-30%), 3=Medium (30-50%), 4=High (50-75%), 5=Very High (75-100%)
- **Impact (I)**: 1=Negligible (<$100K), 2=Minor ($100K-$500K), 3=Moderate ($500K-$2M), 4=Major ($2M-$10M), 5=Catastrophic (>$10M)
- **Risk Score**: P × I (1-25 scale)

| Risk ID | Risk | Probability (P) | Impact (I) | Risk Score | EMV (Expected Monetary Value) | Priority |
|---------|------|-----------------|------------|------------|-------------------------------|----------|
| **R-04** | Anchor tenant cancellation | 3 (40%) | 5 ($50M loss) | **15** | $20M | 🔴 **Critical** |
| **R-01** | CRAC unit delay | 4 (70%) | 4 ($3M delay) | **16** | $2.1M | 🔴 **Critical** |
| **R-02** | Union strike | 2 (30%) | 4 ($2.5M delay) | **8** | $750K | 🟡 **High** |
| **R-03** | Permit delay | 3 (50%) | 3 ($1.5M delay) | **9** | $750K | 🟡 **High** |
| **R-05** | Generator test failure | 2 (25%) | 3 ($1M re-work) | **6** | $250K | 🟢 **Medium** |
| **R-06** | FX volatility (EUR) | 4 (60%) | 2 ($400K) | **8** | $240K | 🟢 **Medium** |

**Total Portfolio Risk Exposure (EMV Sum)**: $24.04M

### Risk Heat Map

```

Impact ↑
5 |              R-04
4 |    R-01      R-02, R-03
3 |              R-05
2 |         R-06
1 |
  +------------------→ Probability
    1   2   3   4   5

🔴 Critical (Score 12-25): Immediate action required
🟡 High (Score 6-11): Active mitigation
🟢 Medium (Score 1-5): Monitor

```

---

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

---

### R-04: Anchor Tenant Cancellation (Priority 1)

**Response Strategy**: **MITIGATE** + **ACCEPT** (with negotiation)

**Primary Mitigation** (Cost: $150K legal + relationship management):
1. **Contract Amendment Negotiation**:
   - Propose 30-day extension (Oct 1 → Nov 1) in exchange for 3-month rent discount ($500K concession).
   - **Rationale**: AWS has no alternative DC capacity in region for Q4 workloads (leverage their dependency).
2. **Interim Capacity Offer**: Provide temporary space in adjacent DC-03 (10MW) at no cost for 60 days to bridge gap.
3. **Executive Escalation**: CEO-to-CEO call (our CEO + AWS VP Infrastructure) to reinforce partnership.

**Contingency Plan (If AWS walks)**:
- **Backup Tenant Pipeline**: 3 Tier-2 cloud providers (Oracle Cloud, Alibaba Cloud, IBM) pre-qualified and ready to sign.
- **Revenue Impact**: $50M AWS contract → $35M from 3 smaller tenants (30% revenue reduction vs. catastrophic loss).

**RACI**:
- **Responsible**: VP Sales
- **Accountable**: CEO
- **Consulted**: Legal, Project Manager
- **Informed**: Board of Directors

---

### R-02: Union Labor Strike (Priority 2)

**Response Strategy**: **TRANSFER** + **MITIGATE**

**Primary Mitigation**:
1. **Labor Agreement Pre-Negotiation**: Engage union rep NOW (before Oct 31 contract expiry) to offer 8% wage increase ($120K total cost vs. $2.5M strike delay).
2. **Non-Union Subcontractor Standby**: Contract backup HVAC team from out-of-state (higher cost but strike-proof).
   - **Cost**: $300K premium vs. union rates.
   - **Risk**: Quality may vary — require same manufacturer certifications (Vertiv-certified installers).
3. **Accelerate HVAC Work**: Fast-track installation schedule to complete critical units BEFORE contract expiry (28 days early finish).

**Trigger Condition for Escalation**: If union rejects offer by Nov 5, activate non-union contractor immediately.

---

### R-03: Permit Delay (Priority 2)

**Response Strategy**: **MITIGATE**

**Primary Mitigation**:
1. **Expeditor Hire**: Retain specialized municipal permit consultant ($25K/month) to navigate planning office bureaucracy.
   - **Track Record**: Consultant has 90% success rate unblocking permits within 2 weeks.
2. **Political Escalation**: Engage city council member (via Chamber of Commerce relationship) to flag delay (estimated 1-week resolution).
3. **Alternative Grid Connection**: Explore backup connection via adjacent industrial park substation (adds $150K but bypasses planning office).

**Monitoring**: Daily check-ins with planning office + weekly escalation to city manager if no progress.

---

## 4. Contingency Plans

### Contingency Budget Allocation

| Risk | Trigger Condition | Contingency Action | Reserved Budget | Approval Authority |
|------|-------------------|--------------------|-----------------|--------------------|
| R-01 | Vertiv confirms \u003e8-week delay | Activate Carrier backup order | $240K | PM (approved) |
| R-04 | AWS sends cancellation notice | Engage backup tenant pipeline | $2M (revenue gap fund) | CEO |
| R-02 | Union votes to strike (Nov 10) | Deploy non-union contractor | $300K | Construction Mgr |
| R-03 | Permit not issued by Nov 15 | Build alternative grid connection | $150K | PM |

**Total Contingency Reserve**: $2.69M (already allocated in project budget as 8% contingency fund).

---

## 5. Monitoring Procedures (Key Risk Indicators)

### KRI Dashboard (Weekly Review)

| Risk | Key Risk Indicator (KRI) | Green Threshold | Yellow Threshold | Red Threshold | Current Status |
|------|--------------------------|-----------------|------------------|---------------|----------------|
| R-01 | Vertiv production status | On-schedule | 1-week delay | \u003e2-week delay | 🟡 (Monitoring) |
| R-04 | AWS satisfaction score | \u003e8/10 (survey) | 6-8/10 | \u003c6/10 | 🟢 (Score: 7.5) |
| R-02 | Union negotiation progress | Agreement signed | Talks ongoing | Breakdown | 🟡 (In negotiation) |
| R-03 | Permit office response time | \u003c5 days | 5-10 days | \u003e10 days | 🔴 (14 days) |
| R-05 | Generator test results | All pass | 1 failure | \u003e1 failure | 🟢 (Scheduled Oct 30) |

**Review Cadence**: 
- **Daily**: PM reviews R-01, R-04 (critical risks)
- **Weekly**: Steering Committee reviews all KRIs
- **Monthly**: Board briefing on top 3 risks

---

## 6. Escalation Protocols

### Escalation Matrix

| Scenario | Immediate Action | Escalation Level | Communication |
|----------|-----------------|------------------|---------------|
| **Red KRI triggered** | PM investigates root cause (within 4 hours) | Level 1: Steering Committee (same day) | Email + emergency meeting |
| **Risk Score increases ≥5 points** | Re-assess mitigation plan | Level 2: Executive Sponsor (within 24 hours) | Written brief + phone call |
| **Contingency budget exceeded** | Halt non-critical spending | Level 3: CEO / CFO (immediate) | Board notification |
| **Anchor tenant sends legal notice** | Engage crisis management team | Level 4: Board of Directors (within 12 hours) | Emergency board session |

### Communication Templates

**Escalation Email (Sample for R-04 Red Alert)**:

```

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

```

---

## Success Metrics

### Risk Management Effectiveness KPIs

| Metric | Target | Current (Month 8) | Trend |
|--------|--------|-------------------|-------|
| **% Risks Identified Before Impact** | \u003e90% | 85% | 🟡 (Improved from 70% in Month 5) |
| **Average Risk Response Time** | \u003c48 hours | 36 hours | 🟢 (Exceeding target) |
| **Contingency Budget Utilization** | \u003c50% | 12% ($324K of $2.69M) | 🟢 (Healthy reserve) |
| **Critical Risks (Score \u003e12) Mitigated** | 100% | 50% (1 of 2 mitigated) | 🔴 (R-04 remains critical) |
| **Steering Committee Satisfaction** | \u003e4/5 | 4.2/5 | 🟢 (Good visibility) |

---

## FMEA (Failure Mode and Effects Analysis) - Optional Deep Dive

For high-complexity risks (e.g., R-05 Generator Testing), use FMEA methodology:

| Failure Mode | Potential Effects | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN (Risk Priority Number) | Mitigation |
|--------------|-------------------|-----------------|-------------------|------------------|----------------------------|------------|
| Generator fails load test | Cannot achieve required 50MW capacity | 9 | 3 | 2 | **54** | Pre-test with vendor engineer present; backup generator on-site |
| Cooling system leak | Equipment damage, downtime | 8 | 2 | 4 | **64** | Pressure test all lines before commissioning; leak detection sensors |

**RPN Scoring**: Severity × Occurrence × Detection (1-1000 scale)
- **RPN \u003e 100**: Immediate action required
- **RPN 50-100**: High priority mitigation
- **RPN \u003c 50**: Monitor and review quarterly
```

## Tips

- **Quantify Impact in Dollar Terms**: Executives understand "$500K/month delay" better than "high impact." Always convert impact to EMV (Expected Monetary Value).
- **Update Risk Register Weekly**: Stale risk registers are useless. Review KRIs weekly and adjust probability/impact scores as conditions change.
- **Don't Over-Mitigate Low Risks**: Focus 80% of effort on the top 20% of risks (Pareto principle). Risk R-06 (FX volatility) may not need active mitigation if EMV is \u003c$250K.
- **Link Risks to Project Schedule**: Use critical path analysis to identify which risks directly threaten the go-live date (R-01, R-03, R-04 in this example).
- **Maintain Contingency Reserves**: Never allocate 100% of contingency budget. Reserve 30-40% for unknown-unknowns ("black swan" events).
- **Use Trigger-Based Contingencies**: Don't activate contingency plans too early. Define clear triggers (e.g., "If permit not issued by Nov 15...").
- **Escalate Early**: If a risk score increases ≥5 points in one week, escalate immediately. Waiting causes exponential damage.

---

## Related Prompts

- **[change-management-coordinator](./change-management-coordinator.md)** - For managing organizational change risks
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - For communicating risks to stakeholders
- **[budget-and-cost-controller](./budget-and-cost-controller.md)** - For managing financial impact of risks
- **[project-charter-creator](./project-charter-creator.md)** - For initial risk identification during project planning
