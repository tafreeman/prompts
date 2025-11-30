---
title: "Budget and Cost Controller"
shortTitle: "Budget Controller"
intro: "Project budget controller using Earned Value Management (EVM) for variance analysis, cost forecasting, and corrective actions."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "finance"
  - "project-management"
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-26"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Budget and Cost Controller

## Description

Project budget controller using Earned Value Management (EVM) methodologies. Specializes in variance analysis, cost forecasting, and corrective action planning for capital projects and IT implementations.

## Use Cases

- Capital project budget tracking (construction, office moves, infrastructure)
- IT implementation financial management
- Budget variance reporting to CFO/steering committees
- Cost optimization and value engineering
- Monthly financial close processes

## Prompt

```text
You are a Project Financial Controller using Earned Value Management (EVM) standards.

Manage budget for:

**Project**: [project_name]
**Total Budget**: [budget]
**Current Spend**: [current_spend]
**Remaining Timeline**: [timeline]
**Cost Concerns**: [concerns]

Provide:
1. **Budget Variance Analysis** (Planned vs. Actual with EVM metrics: CPI, SPI, EAC)
2. **Cost Forecasting** (Estimate at Completion with confidence intervals)
3. **Expense Optimization** (Value engineering opportunities)
4. **Financial Reporting** (CFO-ready dashboard)
5. **Risk Assessment** (Budget risks with probability/impact)
6. **Corrective Actions** (Immediate steps to control overruns)

Use tables for variance analysis and include cash flow projections if applicable.
```

## Variables

- `[project_name]`: Project name and scope (e.g., "HQ Office Relocation - 500-person facility")
- `[budget]`: Total approved budget (e.g., "$2.5M CapEx + $150K contingency")
- `[current_spend]`: Actual spend to date (e.g., "$1.8M (72% of budget), Month 8 of 12")
- `[timeline]`: Project timeline context (e.g., "Month 8 of 12 (66% elapsed), Go-Live Feb 1")
- `[concerns]`: Specific cost issues (e.g., "Furniture 20% over estimate due to supply chain surcharges, IT cabling bids pending")

## Example Usage

**Input:**

```text
Project: HQ Office Relocation - New 500-Person Facility
Total Budget: $2.5M Total CapEx + $150K Contingency (6%) = $2.65M Approved
Current Spend: $1.8M (72% of base budget, 68% of approved with contingency)
Timeline: Month 8 of 12 (66% timeline elapsed), Go-Live Target: Feb 1, 2026
Cost Concerns:
- Furniture costs came in 20% over estimate ($750K actual vs. $625K budgeted) due to supply chain inflation surcharges
- IT cabling bids are pending (budgeted $200K, bids range $220K-$280K)
- AV equipment (conference room tech) may require upgrade to support hybrid meetings (not in original scope)
- Contingency already drawn down $80K for asbestos remediation (unexpected discovery)
```

**Output:**

```markdown
# Budget Control Report: HQ Office Relocation
**Report Date**: November 26, 2025  
**Project Month**: 8 of 12 (66% Complete by Timeline)

---

## 1. Budget Variance Analysis (EVM)

### Budget Summary

| Category | Budgeted (BAC) | Actual Cost (AC) | Committed (PO'd) | Forecast (EAC) | Variance |
|----------|----------------|------------------|------------------|----------------|----------|
| **Construction** | $800K | $780K | $800K | $800K | 🟢 -$20K (2.5% under) |
| **Furniture & FF&E** | $625K | $750K | $750K | $750K | 🔴 +$125K (20% over) |
| **IT Infrastructure** | $400K | $320K | $520K | $550K | 🔴 +$150K (38% over - pending cabling) |
| **AV Equipment** | $250K | $180K | $250K | $320K | 🔴 +$70K (28% over - scope change) |
| **Project Management** | $200K | $140K | $200K | $200K | 🟢 On track |
| **Moving & Logistics** | $225K | $0 | $0 | $225K | 🟢 Not started (Month 11-12) |
| **Subtotal** | **$2,500K** | **$2,170K** | **$2,520K** | **$2,845K** | 🔴 **+$345K (13.8% over)** |
| **Contingency** | $150K | $80K | - | $70K remaining | 🟡 53% consumed |
| **Total Approved** | **$2,650K** | **$2,250K** | **$2,520K** | **$2,915K** | 🔴 **+$265K (10% over approved)** |

### Earned Value Management (EVM) Metrics

| Metric | Formula | Value | Interpretation |
|--------|---------|-------|----------------|
| **BAC** (Budget at Completion) | Total approved budget | $2,650K | Baseline |
| **PV** (Planned Value) | Planned spend at Month 8 | $1,750K (66% of BAC) | Schedule-driven cost |
| **EV** (Earned Value) | Work completed (60% done per PM) | $1,590K (60% of BAC) | Value delivered |
| **AC** (Actual Cost) | Actual spend to date | $2,250K | Cash out the door |
| **CPI** (Cost Performance Index) | EV / AC | **0.71** | 🔴 Getting $0.71 value per $1 spent |
| **SPI** (Schedule Performance Index) | EV / PV | **0.91** | 🟡 9% behind schedule |
| **EAC** (Estimate at Completion) | BAC / CPI | **$3,732K** | 🔴 Projected final cost (worst case) |
| **VAC** (Variance at Completion) | BAC - EAC | **-$1,082K** | 🔴 41% budget overrun if no action |
| **TCPI** (To-Complete Perf Index) | (BAC - EV) / (BAC - AC) | **2.65** | 🔴 Need 265% efficiency to stay on budget (unrealistic) |

**Status**: 🔴 **CRITICAL** - Project is trending 41% over budget if no corrective action taken.

---

## 2. Cost Forecasting

### Scenario Analysis

| Scenario | Assumptions | Forecast EAC | Variance from Budget |
|----------|-------------|--------------|----------------------|
| **Worst Case** | No mitigation; IT cabling $280K; AV upgrade approved | $3,100K | +$450K (+17% over) |
| **Most Likely** | Moderate mitigation; IT cabling $240K; AV scaled down | $2,915K | +$265K (+10% over) |
| **Best Case** | Aggressive value engineering; IT cabling $220K; AV deferred | $2,720K | +$70K (+2.6% over) |

**Base Case Forecast (Most Likely)**: $2,915K

**Breakdown**:
- Furniture overrun locked in: +$125K
- IT cabling (midpoint bid): +$40K ($240K vs. $200K budgeted)
- AV equipment scope increase: +$70K (hybrid meeting tech)
- Contingency reserve: -$70K (remaining buffer applied)
- **Net Overrun**: +$265K (10% over approved budget)

### Cash Flow Projection

| Month | Planned Spend | Forecasted Spend | Cumulative Variance |
|-------|---------------|------------------|---------------------|
| **Month 9** | $200K | $280K | +$80K (IT cabling payments) |
| **Month 10** | $150K | $190K | +$120K (AV equipment arrives) |
| **Month 11** | $225K | $240K | +$135K (Moving costs slightly elevated) |
| **Month 12** | $75K | $75K | +$135K (Project close-out on budget) |
| **Total** | **$650K** | **$785K** | **+$135K additional spend** |

**Funding Gap**: $265K shortfall vs. approved $2.65M budget.

---

## 3. Expense Optimization (Value Engineering)

### Cost Reduction Opportunities

| Initiative | Category | Estimated Savings | Implementation Risk | Recommendation |
|------------|----------|-------------------|---------------------|----------------|
| **VE-01: AV Equipment Simplification** | AV Equipment | $50K | Low (functionality preserved) | ✅ **Approve** |
| **VE-02: Furniture Phased Approach** | Furniture | $80K | Medium (employee morale impact) | 🟡 **Consider** |
| **VE-03: IT Cabling Vendor Negotiation** | IT Infrastructure | $30K | Low (leverage competitive bids) | ✅ **Approve** |
| **VE-04: Defer Breakroom Upgrade** | Construction | $40K | Low (Phase 2 project) | ✅ **Approve** |
| **VE-05: Self-Move Option (No Movers)** | Moving & Logistics | $100K | High (employee time, logistics risk) | ❌ **Reject** |
| **Total Potential Savings** | | **$300K** | | **$120K realistic** |

#### VE-01: AV Equipment Simplification (Save $50K)

**Current Plan**: Cisco Webex Boards in all 12 conference rooms ($320K total)  
**Proposed**: 
- Tier 1 Rooms (4 exec rooms): Keep Cisco Webex Boards ($80K)
- Tier 2 Rooms (8 standard rooms): 4K TVs + Logitech MeetUp cameras + soundbars ($110K)
- **Savings**: $130K budgeted → $190K new plan = **+$60K overrun** BUT avoid $70K scope increase = **Net $50K savings vs. forecast**

**Trade-Off**: Tier 2 rooms lose touch-screen whiteboarding (can use laptops + screen share instead).

---

#### VE-02: Furniture Phased Approach (Save $80K - RISKY)

**Current Plan**: All 500 desks, chairs, and storage delivered Month 10 ($750K)  
**Proposed**: 
- Phase 1 (Move-In Feb 1): 400 desks only ($600K)
- Phase 2 (April 1): Remaining 100 desks when Finance team relocates ($150K in FY2027 budget)

**Savings**: Defer $150K to next fiscal year = **$80K avoided overrun** (rest of $150K is timing shift).

**RISK**: 
- 🔴 Employee morale: 100 employees work at temporary tables for 8 weeks
- 🔴 HR backlash if senior execs get desks first (optics issue)

**Mitigation**: Allocate temporary furniture to junior staff first (interns, contractors) to preserve morale.

---

#### VE-03: IT Cabling Vendor Negotiation (Save $30K)

**Current Situation**: 3 bids received ($220K, $240K, $280K)  
**Proposed Action**:
1. Re-bid with scope clarification (some bidders included patch panels, others didn't)
2. Negotiate $240K vendor down to $210K by:
   - Accepting Cat6 instead of Cat6a (sufficient for 10Gbps, saves $20K)
   - Using existing conduit runs where possible (saves $10K)

**Confidence**: High (80% likely to achieve $210-220K final price).

---

#### VE-04: Defer Breakroom Upgrade (Save $40K)

**Current Plan**: Full breakroom renovation with espresso machines, new cabinetry ($75K budgeted, trending $90K)  
**Proposed**: 
- Basic coffee makers + paint refresh only ($25K)
- Defer full renovation to "Phase 2 Amenities" project in FY2027

**Savings**: $65K avoided spend = **$40K savings vs. forecast**.

**RISK**: 🟢 Low - Employees care more about desk/tech than luxury breakroom.

---

### Recommended Cost Reduction Package

| Initiative | Savings | Risk | Status |
|------------|---------|------|--------|
| VE-01 (AV Simplification) | $50K | Low | ✅ Recommend |
| VE-03 (IT Cabling Negotiation) | $30K | Low | ✅ Recommend |
| VE-04 (Defer Breakroom) | $40K | Low | ✅ Recommend |
| **Total Package** | **$120K** | | |

**Net Budget Impact**:
- Forecasted overrun: +$265K
- Cost reduction: -$120K
- **Revised Forecast**: +$145K overrun (5.5% over approved budget)

---

## 4. Financial Reporting (CFO Dashboard)

### Executive Summary

**Project**: HQ Office Relocation  
**Status**: 🔴 **RED** - Budget overrun 10% (trending, pre-mitigation)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Budget Utilization** | 66% (Month 8/12) | 85% ($2.25M / $2.65M) | 🔴 Over-burn |
| **Cost Performance Index (CPI)** | \u003e 0.90 | **0.71** | 🔴 Critical |
| **Forecasted Completion** | $2.65M | $2.915M (-mitigation) → $2.795M (+mitigation) | 🔴 10% → 🟡 5.5% over |
| **Contingency Remaining** | $150K | $70K (53% consumed) | 🟡 Medium risk |
| **Funding Gap** | $0 | $145K (post-mitigation) | 🔴 Requires CFO approval |

### Variance Drivers (Top 3)

1. **Furniture Supply Chain Inflation** (+$125K): Market-wide 20% increase in lead times + surcharges (industry trend, not project-specific).
2. **IT Infrastructure Scope Clarity** (+$150K forecasted): Original estimate assumed Cat5e; building code requires Cat6. Cabling bids 10-40% over budget.
3. **AV

 Equipment Scope Creep** (+$70K): Post-COVID hybrid meeting requirements not anticipated in 2024 scope definition.

---

## 5. Risk Assessment

### Budget Risk Register

| Risk ID | Risk | Probability | Impact | EMV | Mitigation |
|---------|------|-------------|--------|-----|------------|
| **BR-01** | IT cabling bids exceed $240K (worst-case $280K) | 30% | $40K overrun | $12K | Lock $240K vendor now; VE-03 negotiation |
| **BR-02** | Moving costs spike due to Jan weather delays | 20% | $50K overrun | $10K | Book movers NOW (Dec rates lower than Jan) |
| **BR-03** | Asbestos discovery Phase 2 (additional floors) | 15% | $100K overrun | $15K | Conduct environmental survey NOW (Month 9) |
| **BR-04** | Employee headcount increase (550 vs. 500) | 40% | $80K (50 desks) | $32K | Confirm final headcount with HR by Dec 1 |
| **Total Budget Risk Exposure** | | | | **$69K** | Monitor monthly |

**Contingency Reserve Status**:
- Allocated: $150K
- Consumed: $80K (asbestos BR-03 partial realization)
- Remaining: $70K
- **Risk-Adjusted Reserve Needed**: $69K EMV + $145K known overrun = $214K  
- **Shortfall**: $214K - $70K = **$144K funding gap**

---

## 6. Corrective Actions (Immediate Steps)

### 30-Day Action Plan

| Action | Owner | Deadline | Expected Impact |
|--------|-------|----------|-----------------|
| **1. Approve VE Package** (VE-01, VE-03, VE-04) | PM + CFO | Dec 1 | -$120K cost reduction |
| **2. Lock IT Cabling Vendor** ($240K bid) | IT Director | Dec 5 | Prevent $280K worst-case |
| **3. Re-Forecast AV Equipment** (finalize Tier 1/2 split) | Facilities Manager | Dec 10 | Lock $190K actual cost |
| **4. Request $145K Budget Increase** | CFO | Dec 15 | Close funding gap |
| **5. Book Moving Company** (lock Jan rates) | PM | Dec 1 | Prevent BR-02 ($50K risk) |
| **6. Conduct Phase 2 Asbestos Survey** | Environmental Consultant | Dec 20 | Mitigate BR-03 ($100K risk) |

### Budget Increase Request (CFO Approval)

**Request Amount**: $145K (5.5% increase over approved $2.65M)

**Justification**:
1. **Market Conditions**: Furniture inflation industry-wide (20% across all vendors, not project-specific).
2. **Scope Evolution**: Hybrid meeting AV requirements post-COVID (business necessity, not scope creep).
3. **Mitigation Efforts**: $120K cost reduction achieved through value engineering (demonstrates fiscal discipline).

**Alternatives if Denied**:
- Implement VE-02 (Phased Furniture): Additional $80K savings → reduces gap to $65K
- Tap into corporate capital reserve fund (if available)
- Defer non-critical IT upgrades (e.g., WiFi 6E) to Phase 2

---

## Success Metrics

### Budget Control KPIs (Track Monthly)

| Metric | Target | Current (Month 8) | Trend |
|--------|--------|-------------------|-------|
| **CPI (Cost Performance Index)** | \u003e 0.90 | 0.71 | 🔴 Critical (needs corrective action) |
| **Budget Variance** | ±5% | +10% (pre-mitigation) | 🔴 → 🟡 (post-mitigation: +5.5%) |
| **Contingency Utilization** | \u003c 50% by Month 8 | 53% ($80K / $150K) | 🟡 Slightly elevated |
| **Forecast Accuracy** | ±10% vs. actual | Month 7 forecast was $2.7M; Month 8 actual trend $2.915M | 🔴 Forecast drift (7.9%) |
| **Purchase Order Compliance** | 100% PO'd before spend | 98% (1 invoice paid without PO) | 🟢 Good controls |

---

## Recommendations Summary

### Immediate Actions (This Week)
1. ✅ **Approve VE Package**: VE-01, VE-03, VE-04 ($120K savings)
2. ✅ **Lock IT Cabling Vendor**: $240K bid (prevent $40K additional risk)
3. ⏳ **Prepare CFO Budget Request**: $145K increase memo

### Strategic Decisions (Next 2 Weeks)
1. **CFO Approval Path**: If denied, implement VE-02 (Phased Furniture) as backup
2. **Risk Mitigation**: Conduct asbestos survey NOW to avoid $100K surprise in Month 10

### Governance
- **Escalate to Steering Committee**: Month 8 report (this document) + budget increase request
- **Monthly Financial Reviews**: Increase cadence from monthly → bi-weekly for Months 9-12
```

## Tips

- **Track CPI Weekly**: Cost Performance Index below 0.85 is a leading indicator of budget disaster. Escalate immediately if CPI drops below 0.80.
- **Lock Vendors Early**: 60% of budget overruns come from vendor price volatility. Get fixed-price POs signed ASAP.
- **Protect Contingency Reserve**: Don't tap contingency for "nice-to-haves." Reserve it for true unknowns (e.g., asbestos, structural issues).
- **Value Engineering Before Scope Cuts**: VE-01 (AV simplification) saves $50K without eliminating functionality. Always try VE before cutting scope.
- **Communicate Overruns Early**: CFOs hate surprises. Flag a 10% overrun in Month 8, not Month 11 when it's unfixable.
- **Use EVM Metrics**: CPI and SPI give early warning signals. A project can be "on time" but financially doomed if CPI is 0.70.

## Related Prompts

- **[risk-management-analyst](./risk-management-analyst.md)** - For budget risk assessment
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - For CFO budget briefings
- **[project-charter-creator](./project-charter-creator.md)** - For initial budget approval
