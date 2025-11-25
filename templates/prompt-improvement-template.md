# Prompt Improvement Template & Workflow

## Purpose

This template provides a systematic approach to upgrading low-quality prompts identified by the [Prompt Quality Evaluator](../prompts/system/prompt-quality-evaluator.md). Use this when a prompt scores below 70/100 or has critical issues flagged.

## Quick Reference: Common Issues & Fixes

| Issue | Solution | Effort | Impact |
|-------|----------|--------|--------|
| **<30 words** | Expand with context, constraints, output format | Low | +10-15 points |
| **Missing metadata** | Add complete YAML frontmatter | Low | +5 points |
| **No examples** | Create 1-2 realistic examples | Medium | +8-10 points |
| **Generic use cases** | Replace with specific, actionable scenarios | Low | +3-5 points |
| **No output format** | Specify structure (JSON/Markdown/table) | Low | +4-6 points |
| **Missing tips** | Add 3-5 actionable customization tips | Low | +3 points |
| **No advanced techniques** | Add CoT/structured reasoning where appropriate | Medium | +5-8 points |

## Upgrade Workflow

### Step 1: Assess Current State

Run the prompt through the [Prompt Quality Evaluator](../prompts/system/prompt-quality-evaluator.md) to get:

- Total score and tier
- Dimension breakdowns
- List of critical/high-priority issues
- Actionable recommendations ranked by impact

### Step 2: Fix Critical Issues (P0)

**Goal:** Get out of Tier 4 (<55 points) → Tier 3 (55-69 points)

If flagged as **<30 words**:

**Before:**

```text
## Prompt

```text
Analyze this data: [data]
Provide insights and recommendations.
```

```

**After:**
```text
## Prompt

```text
You are a senior data analyst specializing in extracting actionable business insights.

**Dataset:** [data_description]

**Analysis Goals:**
1. [primary_goal]
2. [secondary_goal]
3. [tertiary_goal]

**Context:**
- Business domain: [domain]
- Decision to inform: [decision]
- Constraints: [constraints]

Provide your analysis in the following format:

**Key Findings:**
- [Finding 1 with supporting data]
- [Finding 2 with supporting data]

**Recommendations:**
1. [Actionable recommendation with expected impact]
2. [Actionable recommendation with expected impact]

**Next Steps:**
- [Immediate actions]
```

```

If **missing YAML frontmatter**:

```yaml
---
title: "[Descriptive Title]"
category: "[Category]"  # developers, business, analysis, etc.
tags: ["tag1", "tag2", "tag3"]
author: "Prompts Library Team"
version: "1.0"
date: "YYYY-MM-DD"
difficulty: "beginner|intermediate|advanced"
platform: "Claude Sonnet 4.5"
governance_tags: ["PII-safe", "requires-human-review", etc.]  # optional
---
```

### Step 3: Address High Priority Issues (P1)

**Goal:** Tier 3 (55-69 points) → Tier 2 (70-84 points)

**Add Realistic Example Usage:**

**Template:**

```markdown
## Example Usage

**Input:**

```text
[Show the prompt with placeholders filled in with realistic values]

[data_description]: E-commerce sales data for Q4 2024
[primary_goal]: Identify top-performing products
[secondary_goal]: Understand seasonal patterns
[tertiary_goal]: Find growth opportunities

[domain]: Online retail
[decision]: Q1 2025 marketing budget allocation
[constraints]: Must complete analysis within 24 hours, focus on actionable insights
```

**Output:**

```text
[Show expected AI response formatted as specified]

**Key Findings:**
- Electronics category grew 45% YoY, driven by smart home devices
- Mobile traffic converted 12% better than desktop in Q4
- Cart abandonment rate spiked to 78% during week of 12/15 (holiday shipping deadline)

**Recommendations:**
1. **Increase smart home device inventory by 30%** (expected $150K revenue increase based on sell-through rate)
2. **Optimize mobile checkout flow** (estimated 8% conversion lift = $45K/month)
3. **Extend shipping deadline campaign to 12/20** (reduce abandonment by 15% = $22K recovery)

**Next Steps:**
- Meet with supply chain team to confirm smart home inventory capacity (by 12/1)
- A/B test mobile checkout improvements (launch 12/15)
- Update homepage shipping deadline messaging (deploy 12/10)
```

```

**Improve Variable Documentation:**

**Before:**
```markdown
## Variables

- `[data]`: Data
- `[goal]`: Goal
```

**After:**

```markdown
## Variables

- `[data_description]`: Type and scope of data (e.g., "Q4 2024 e-commerce sales data, 15K transactions across 5 product categories")
- `[primary_goal]`: Main analysis objective (e.g., "Identify which products drove revenue growth")
- `[secondary_goal]`: Supporting analysis objective (e.g., "Understand seasonal purchase patterns")
- `[tertiary_goal]`: Additional insight area (e.g., "Find untapped growth opportunities")
- `[domain]`: Business context (e.g., "Online retail", "SaaS analytics", "Healthcare reporting")
- `[decision]`: What this analysis will inform (e.g., "Q1 marketing budget allocation")
- `[constraints]`: Limitations or requirements (e.g., "Analysis must complete in 24 hours", "Focus on top 10 products only")
```

**Add Actionable Tips:**

**Template:**

```markdown
## Tips

- **For large datasets:** Break analysis into phases (summary → deep-dive → recommendations)
- **When time is limited:** Ask for executive summary first, then request details on specific findings
- **For stakeholder presentations:** Request visualization recommendations alongside insights
- **To improve accuracy:** Provide industry benchmarks in the context (e.g., "Industry avg conversion rate: 2.3%")
- **For recurring reports:** Save successful outputs as templates for future use
```

### Step 4: Medium Priority Enhancements (P2)

**Goal:** Tier 2 (70-84 points) → Tier 1 (85-100 points)

**Add Advanced Reasoning Techniques:**

When appropriate (complex analysis, multi-step problem-solving), add Chain-of-Thought:

```markdown
## Prompt

```text
[Existing prompt intro...]

**Reasoning Process:**

Before providing your final analysis, think through:

**Step 1: Data Understanding**
- What patterns do I see in the raw numbers?
- Are there any anomalies or outliers?
- What's the data quality level?

**Step 2: Insight Generation**
- What do these patterns mean for the business?
- What are potential root causes?
- What assumptions am I making?

**Step 3: Validation**
- Do my insights align with the stated goals?
- Are my recommendations actionable and measurable?
- Have I considered alternative explanations?

Then provide your structured output.
```

```

**Add Structured Output Schema:**

For automation-friendly prompts:

```markdown
## Output Schema (JSON)

If you need machine-readable output, request this format:

```json
{
  "executive_summary": "Brief 2-3 sentence overview",
  "key_findings": [
    {
      "finding": "Description",
      "supporting_data": "Specific numbers/evidence",
      "impact": "high|medium|low"
    }
  ],
  "recommendations": [
    {
      "action": "What to do",
      "expected_outcome": "Measurable result",
      "effort": "time/cost estimate",
      "priority": 1
    }
  ],
  "next_steps": ["Action 1", "Action 2"],
  "confidence": 0.85,
  "assumptions": ["Assumption 1", "Assumption 2"]
}
```

```

**Add Research Citations:**

```markdown
## Research Foundation

This prompt is based on:

- **[Relevant Paper/Framework]**: Citation and link
- **Industry Standard**: Name and source
- **Best Practice**: Authority and reference

Example:
- **The Prompt Report (arXiv:2406.06608)**: Comprehensive taxonomy of effective prompting techniques
- **OpenAI Best Practices**: Structured outputs and clear instruction guidelines
```

### Step 5: Validate Improvements

After making changes, re-run the [Prompt Quality Evaluator](../prompts/system/prompt-quality-evaluator.md):

- **Expected improvement:** +15-25 points for P0+P1 fixes
- **Target score:** 70+ for general use, 85+ for enterprise-critical prompts
- **Quality gate:** All critical issues (P0) must be resolved

## Before/After Examples

### Example 1: Minimal Business Prompt → Tier 2

**Before (Score: 48/100 - Tier 4)**

```markdown
---
title: "Budget Planner"
category: "business"
---

# Budget Planner

## Prompt

Create a budget for [project].
```

**After (Score: 75/100 - Tier 2)**

```markdown
---
title: "Project Budget Planner"
category: "business"
tags: ["budgeting", "project-management", "planning", "finance"]
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-25"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5, GPT-4"
---

# Project Budget Planner

## Description

Generate comprehensive project budgets with line-item breakdowns, risk contingencies, and approval-ready formatting for enterprise project management.

## Use Cases

- Creating initial project budget proposals for stakeholder approval
- Refining budget estimates during project planning phase
- Comparing actual vs. budgeted costs during project execution
- Generating budget variance reports for project reviews

## Prompt

```text
You are a senior project financial analyst creating a detailed project budget.

**Project Details:**
- Project Name: [project_name]
- Duration: [duration]
- Team Size: [team_size]
- Deliverables: [deliverables]

**Budget Constraints:**
- Total Budget Cap: [budget_cap]
- Must Include: [required_categories]
- Contingency Percentage: [contingency_pct]

**Context:**
- Organization: [organization_type]
- Approval Authority: [approver]
- Reporting Period: [period]

Create a detailed budget including:

1. **Executive Summary**
   - Total budget amount
   - Major cost categories with percentages
   - Key assumptions

2. **Line-Item Budget Breakdown**
   - Personnel costs (roles, hours, rates)
   - Technology/tools (licenses, infrastructure)
   - External services (contractors, vendors)
   - Travel and expenses
   - Miscellaneous/contingency

3. **Risk Analysis**
   - Potential cost overruns with likelihood
   - Mitigation strategies
   - Contingency allocation rationale

4. **Timeline-Based Allocation**
   - Monthly/quarterly cost distribution
   - Payment milestones

Output as a Markdown table for easy import into Excel/Google Sheets.
```

## Variables

- `[project_name]`: Project title (e.g., "Customer Portal Redesign", "Q4 Marketing Campaign")
- `[duration]`: Project timeline (e.g., "6 months", "Q1-Q2 2025")
- `[team_size]`: Number of team members (e.g., "5 FTE: 2 developers, 1 designer, 1 PM, 1 QA")
- `[deliverables]`: Key outputs (e.g., "New mobile app, API integration, admin dashboard")
- `[budget_cap]`: Maximum allowable budget (e.g., "$250K", "€180K")
- `[required_categories]`: Mandatory cost categories (e.g., "Personnel, Software, Training")
- `[contingency_pct]`: Risk buffer (e.g., "15%", "10-20% depending on risk level")
- `[organization_type]`: Company context (e.g., "Enterprise SaaS", "Healthcare provider")
- `[approver]`: Who needs to approve (e.g., "VP Engineering", "CFO")
- `[period]`: Budget period (e.g., "FY 2025", "Q1 2025")

## Example Usage

**Input:**

```text
[project_name]: Customer Portal Redesign
[duration]: 6 months (Jan-Jun 2025)
[team_size]: 7 FTE (3 frontend devs, 1 backend dev, 1 UX designer, 1 PM, 1 QA)
[deliverables]: Responsive web app, mobile app (iOS/Android), admin dashboard, API integration
[budget_cap]: $350,000
[required_categories]: Personnel, Software, External Services, Travel
[contingency_pct]: 15%
[organization_type]: B2B SaaS company
[approver]: VP Engineering & CFO
[period]: H1 2025
```

**Output:**

```text
## Executive Summary

**Total Project Budget:** $340,000 (within $350K cap)
- Personnel: 68% ($231,200)
- Software/Tools: 12% ($40,800)
- External Services: 8% ($27,200)
- Contingency/Risk: 12% ($40,800)

**Key Assumptions:**
- Developers: $85/hr blended rate
- 6-month duration with ramp-up in month 1
- Cloud hosting costs included in software budget
- No major scope changes requiring re-budgeting

[... full detailed budget breakdown ...]
```

## Tips

- **For budget approval:** Include executive summary first—decision-makers want totals before details
- **When under constraint:** Ask for options at different budget levels (e.g., "Show me at $250K, $300K, and $350K")
- **For recurring projects:** Reference historical budgets in context to improve accuracy
- **To manage stakeholder expectations:** Request a sensitivity analysis showing impact of ±20% changes
- **For compliance:** Add required categories in `[required_categories]` to ensure nothing is missed

## Related Prompts

- [Resource Planning Assistant](resource-planning-assistant.md) - For team capacity planning
- [ROI Calculator](roi-calculator.md) - For cost-benefit analysis
- [Risk Assessment Framework](../governance/risk-assessment.md) - For identifying budget risks

## Changelog

### Version 2.0 (2025-11-25)

- Upgraded from Tier 4 (48/100) to Tier 2 (75/100)
- Added comprehensive variable documentation
- Included realistic example with full output
- Added structured output format (Markdown table)
- Included actionable tips for different scenarios

### Version 1.0 (2025-11-15)

- Initial minimal version

```

**Improvement Summary:**
- Added 7 missing sections (Variables, Example, Tips, etc.)
- Expanded prompt from 12 words → 142 words
- Added complete YAML metadata
- Provided realistic example with expected output
- **Score improvement: +27 points (48 → 75)**

## Quality Gates

Before considering a prompt "upgraded," ensure:

- [ ] Score ≥70/100 (Tier 2 minimum)
- [ ] No P0 critical issues remaining
- [ ] At least 1 realistic example included
- [ ] All variables documented with examples
- [ ] YAML frontmatter complete
- [ ] Tips section with 3+ actionable items
- [ ] Related prompts linked (if applicable)

## Continuous Improvement

- **Re-evaluate quarterly:** Run prompts through evaluator to catch quality drift
- **Track metrics:** Monitor average repository score over time
- **Learn from top performers:** Study Tier 1 prompts and adopt their patterns
- **Gather user feedback:** Track which prompts users report as most/least helpful
- **Update based on research:** Incorporate new techniques from academic papers and industry updates
