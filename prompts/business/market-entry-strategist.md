---
name: Market Entry Strategist
description: Develops market entry strategies with market analysis, go-to-market plans, and risk assessment.
type: how_to
---

# Market Entry Strategist

## Description

This prompt develops comprehensive market entry strategies including market analysis, go-to-market plans, and risk assessment. It helps organizations expand into new markets or geographies with confidence and clear execution roadmaps.

## Use Cases

- Market Entry for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[company]`: Company name and description (e.g., "HRTech SaaS – US-based HR software company")
- `[market]`: Target market (e.g., "Germany – mid-market enterprises 500-5000 employees")
- `[offering]`: Product or service (e.g., "Cloud HR management platform with payroll integration")
- `[competition]`: Competitive landscape (e.g., "SAP SuccessFactors, Personio, local players")
- `[resources]`: Available resources (e.g., "$5M budget, 2-year timeline, existing UK team")

## Prompt

### System Prompt

```text
You are a market entry strategist with experience helping companies expand into new markets. You understand local market dynamics, competitive landscapes, regulatory requirements, and go-to-market execution. You balance opportunity with pragmatic risk assessment.
```

### User Prompt

```text
Develop a market entry strategy for [company] entering [market].

Market Entry Context:
- Product/Service: [offering]
- Competitive Landscape: [competition]
- Available Resources: [resources]

Please provide:
1. Market opportunity assessment
2. Competitive positioning strategy
3. Entry mode recommendation (direct, partnership, acquisition)
4. Go-to-market plan with phases
5. Localization requirements
6. Risk assessment and mitigation
7. Investment and timeline projections
```

## Example

### Input

```text
Develop a market entry strategy for HRTech SaaS – US-based HR software company entering Germany – mid-market enterprises 500-5000 employees.

Market Entry Context:
- Product/Service: Cloud HR management platform with payroll integration
- Competitive Landscape: SAP SuccessFactors, Personio, local players
- Available Resources: $5M budget, 2-year timeline, existing UK team
```

### Expected Output

```text
## Market Entry Strategy: Germany

### Market Opportunity Assessment
| Factor | Assessment | Impact |
|--------|------------|--------|
| Market Size | €2.1B HR software market | High |
| Growth Rate | 12% CAGR | High |
| Target Segment | 8,500 mid-market companies | High |
| Digital Readiness | High (but privacy-conscious) | Medium |

### Competitive Positioning
| Competitor | Position | Our Advantage |
|------------|----------|---------------|
| SAP SuccessFactors | Enterprise, complex | Simpler, faster implementation |
| Personio | SMB focus | More robust for mid-market |
| Local players | Legacy, on-premise | Cloud-native, modern UX |

**Positioning Statement**: "The modern HR platform built for German mid-market companies who've outgrown simple tools but don't need SAP complexity."

### Recommended Entry Mode: Hybrid Partnership
- **Year 1**: Partner with German system integrator for initial customers
- **Year 2**: Establish direct sales team once product-market fit proven

**Rationale**: Reduces risk, provides local expertise, faster time to first customer.

### Go-to-Market Plan

**Phase 1: Foundation (Months 1-6) - $1.5M**
- GDPR compliance certification
- German payroll integration (DATEV)
- Localize product and support
- Partner agreements with 2 SIs

**Phase 2: Pilot (Months 7-12) - $1.5M**
- 10 pilot customers via partners
- Hire Country Manager + 2 sales
- Build reference cases

**Phase 3: Scale (Months 13-24) - $2M**
- Direct sales team (5 reps)
- Marketing investment (events, content)
- Target: 50 customers, €2M ARR

### Risk Mitigation
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GDPR non-compliance | Medium | Critical | External audit, DPO hire |
| Payroll integration issues | High | High | Partner with DATEV expert |
| Local competition response | Medium | Medium | Focus on US innovation advantage |
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
