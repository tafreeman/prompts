---
name: Management Consulting Expert
description: Provides management consulting solutions with problem diagnosis, root cause analysis, and implementation plans.
type: how_to
---

# Management Consulting Expert

## Description

This prompt provides management consulting solutions with structured problem diagnosis, root cause analysis, and actionable implementation plans. It helps organizations tackle complex business challenges using proven consulting frameworks and methodologies.

## Use Cases

- Management for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[client]`: Client name and description (e.g., "SnackCo – $2B packaged food company")
- `[challenge]`: Business challenge (e.g., "Gen Z perceives 'Healthy' line as processed, losing market share")
- `[industry]`: Industry context (e.g., "Packaged food, health-conscious consumer segment")
- `[stakeholders]`: Key stakeholders (e.g., "CEO, CMO, Head of R&D, Board of Directors")
- `[criteria]`: Success criteria (e.g., "Regain 5% market share in 18 months, improve brand perception scores")

## Prompt

### System Prompt

```text
You are a senior management consultant with experience at top-tier firms (McKinsey, BCG, Bain). You use structured problem-solving, hypothesis-driven analysis, and proven frameworks to help organizations solve their most challenging problems.
```

### User Prompt

```text
Provide consulting analysis for [client].

Engagement Context:
- Business Challenge: [challenge]
- Industry: [industry]
- Key Stakeholders: [stakeholders]
- Success Criteria: [criteria]

Please provide:
1. Problem diagnosis and framing
2. Hypothesis tree with key questions to answer
3. Root cause analysis
4. Strategic options with evaluation
5. Recommended solution with implementation plan
6. Quick wins and long-term initiatives
7. Stakeholder management approach
```

## Example

### Input

```text
Provide consulting analysis for SnackCo – $2B packaged food company.

Engagement Context:
- Business Challenge: Gen Z perceives 'Healthy' line as processed, losing market share
- Industry: Packaged food, health-conscious consumer segment
- Key Stakeholders: CEO, CMO, Head of R&D, Board of Directors
- Success Criteria: Regain 5% market share in 18 months, improve brand perception scores
```

### Expected Output

```text
## Consulting Analysis: SnackCo Brand Repositioning

### Problem Framing
**Core Issue**: Gen Z consumers perceive SnackCo's "Healthy" line as inauthentic, despite clean ingredients, due to messaging and packaging that feels corporate.

**Hypothesis**: Brand perception, not product quality, is driving market share loss.

### Hypothesis Tree
1. Is the product actually meeting Gen Z health expectations?
   - Ingredient analysis vs. competitor clean labels
   - Nutritional profile benchmarking
2. Is the messaging resonating?
   - Brand perception research
   - Social media sentiment analysis
3. Is distribution reaching Gen Z?
   - Channel analysis (grocery vs. DTC vs. convenience)

### Root Cause Analysis
| Factor | Impact | Evidence |
|--------|--------|----------|
| Packaging looks "corporate" | High | Focus group: "Looks like my mom's food" |
| No social media presence | High | 10K followers vs. 500K for competitors |
| Wrong influencer partnerships | Medium | Partnered with fitness influencers, not lifestyle |
| Product is actually good | ✅ | Blind taste tests win 60% |

### Strategic Options
| Option | Cost | Timeline | Risk | Expected Impact |
|--------|------|----------|------|------------------|
| A: Rebrand packaging only | $5M | 6 months | Low | +2% share |
| B: Full brand refresh + influencer | $15M | 12 months | Medium | +5% share |
| C: Launch new Gen Z sub-brand | $25M | 18 months | High | +7% share |

### Recommendation: Option B - Full Brand Refresh
**Rationale**: Best balance of impact vs. risk. Preserves brand equity while addressing perception gap.

**Implementation Plan**:
- Month 1-3: Consumer research, influencer identification
- Month 4-6: Packaging redesign, content strategy
- Month 7-9: Pilot in 3 markets
- Month 10-12: National rollout

### Quick Wins (First 90 Days)
1. Pause current influencer partnerships
2. Launch TikTok presence with authentic content
3. A/B test new packaging concepts
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
