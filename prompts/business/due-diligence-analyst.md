---
name: Due Diligence Analyst
description: Conducts comprehensive due diligence with analysis frameworks, risk assessment, findings summary, and recommendations.
type: how_to
---

# Due Diligence Analyst

## Description

This prompt conducts comprehensive due diligence analysis with structured frameworks, risk assessment, and actionable recommendations. It helps investors, acquirers, and executives evaluate opportunities by systematically analyzing key areas of concern.

## Use Cases

- Due Diligence for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[transaction]`: Transaction type (e.g., "Acquisition of FinAI for $50M")
- `[target]`: Target company (e.g., "FinAI Inc. – AI-powered fraud detection startup")
- `[focus]`: Focus areas (e.g., "Technical architecture, IP ownership, team retention")
- `[timeline]`: Due diligence timeline (e.g., "14 days before LOI expiration")
- `[stakeholders]`: Key stakeholders (e.g., "CEO, CFO, CTO, Legal Counsel")

## Prompt

### System Prompt

```text
You are an experienced due diligence analyst with expertise in M&A, investment analysis, and risk assessment. You help organizations evaluate opportunities through systematic investigation of financial, operational, legal, and technical factors.
```

### User Prompt

```text
Conduct due diligence analysis for the following transaction: [transaction]

Target Details:
- Target: [target]
- Focus Areas: [focus]
- Timeline: [timeline]
- Stakeholders: [stakeholders]

Please provide:
1. Due diligence framework and workstreams
2. Key findings by focus area
3. Risk assessment with severity ratings
4. Red flags and deal-breakers to investigate
5. Valuation considerations
6. Recommendations with go/no-go factors
```

## Example

### Input

```text
Conduct due diligence analysis for the following transaction: Acquisition of FinAI for $50M

Target Details:
- Target: FinAI Inc. – AI-powered fraud detection startup
- Focus Areas: Technical architecture, IP ownership, team retention
- Timeline: 14 days before LOI expiration
- Stakeholders: CEO, CFO, CTO, Legal Counsel
```

### Expected Output

```text
## Due Diligence Report: FinAI Acquisition

### Executive Summary
FinAI presents a compelling acquisition target with strong technology and team. Key risks center on IP ownership clarity and customer concentration. Recommend proceeding with conditions.

### Due Diligence Workstreams
| Workstream | Owner | Status | Days |
|------------|-------|--------|------|
| Technical Architecture | CTO | In Progress | 5 |
| IP & Legal | Legal Counsel | In Progress | 7 |
| Financial | CFO | In Progress | 5 |
| Team & Culture | CEO | Scheduled | 3 |
| Customer References | Sales | Scheduled | 4 |

### Key Findings by Focus Area

**Technical Architecture**
- ✅ Modern stack (Python, AWS, Kubernetes)
- ✅ ML models well-documented, retrainable
- ⚠️ Technical debt in data pipeline (~3 months to address)
- ❌ No disaster recovery tested in 12 months

**IP Ownership**
- ✅ Core algorithms patented (2 granted, 1 pending)
- ⚠️ 2 founders have prior employer IP clauses to verify
- ⚠️ Open source components need license audit

**Team Retention**
- ✅ Key engineers have 2-year retention agreements
- ⚠️ CTO considering departure (needs conversation)
- ✅ Strong culture scores in employee surveys

### Risk Assessment
| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| CTO departure | High | Medium | Retention package, earn-out structure |
| IP dispute | High | Low | Rep & warranty insurance |
| Customer concentration | Medium | Medium | Diversification plan |

### Recommendation
**Proceed with conditions:**
1. CTO retention agreement with 3-year earn-out
2. IP indemnification from founders
3. $5M holdback for technical debt remediation
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates
