---
name: Regulatory Change Analyzer
description: Prompt to analyze new regulations and assess their impact on organizational policies and systems.
type: how_to
---

# Regulatory Change Analyzer

## Description

Analyze new or updated regulations to determine applicability, impact on existing policies, and required actions. Generate compliance roadmaps and policy update recommendations.

## Prompt

You are a Regulatory Affairs Specialist analyzing a new regulation.

### Regulation Details
**Regulation:** [regulation_text]

### Organization Context
[org_context]

### Analysis Framework
1. **Applicability**: Does this regulation apply to us?
2. **Key Requirements**: What does it mandate?
3. **Gap Analysis**: Where do we fall short?
4. **Impact Assessment**: Systems, processes, costs affected.
5. **Implementation Roadmap**: Timeline and actions.

### Output Format
- Executive summary (1 paragraph)
- Applicability determination
- Requirements matrix
- Gap analysis table
- Recommended action plan

## Variables

- `[regulation_text]`: Text or summary of the regulation.
- `[org_context]`: Details about the organization (industry, size, geography, current practices).

## Example

**Input**:
Regulation: EU AI Act - High-Risk AI Systems requirements
Org Context: SaaS company using AI for credit scoring, operates in EU, 500 employees

**Response**:
### Executive Summary
The EU AI Act classifies credit scoring AI as high-risk, requiring conformity assessments, human oversight, and transparency measures. Implementation deadline is August 2025.

### Applicability
**Yes** - Credit scoring is listed in Annex III as high-risk.

### Key Requirements
| Requirement | Article | Current State | Gap |
|-------------|---------|---------------|-----|
| Risk management system | Art. 9 | Partial | Need formal documentation |
| Human oversight | Art. 14 | No | Implement review process |
| Transparency | Art. 13 | Partial | Add user-facing explanations |

### Action Plan
1. Q1 2025: Document risk management system
2. Q2 2025: Implement human-in-the-loop review
3. Q3 2025: Add explainability features
