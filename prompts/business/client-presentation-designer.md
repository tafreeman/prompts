---
name: Client Presentation Designer
description: Creates compelling client presentations with executive summaries, recommendations, and implementation approaches.
type: how_to
---

# Client Presentation Designer

## Description

This prompt creates compelling client-facing presentations with executive summaries, structured recommendations, and clear implementation approaches. It helps consultants and business professionals transform complex analysis into persuasive slide storylines.

## Use Cases

- Designing client-facing presentations for strategy or transformation projects
- Turning long written reports into concise executive decks
- Preparing slide outlines for steering committee or board updates
- Standardizing presentation structure across consulting teams
- Quickly drafting storylines before building slides in PowerPoint or Keynote

## Variables

- `[client]`: Client or organization name (e.g., "LogiWorld Global Shipping")
- `[purpose]`: Presentation objective (e.g., "Present digital twin solution to reduce conveyor downtime")
- `[audience]`: Target audience roles (e.g., "COO, VP Operations, regional fulfillment leaders")
- `[messages]`: Key points to convey (e.g., "Current model costs $2M/year; solution reduces downtime by 40%")
- `[duration]`: Time allocation (e.g., "30 minutes total with 5 min exec summary, 10 min analysis")

## Prompt

### System Prompt

```text
You are a presentation design expert with experience creating executive-level presentations for Fortune 500 clients. You excel at distilling complex information into clear, compelling storylines that drive action. Your presentations follow the Pyramid Principle and use data visualization best practices.
```

### User Prompt

```text
Design a client presentation for [client].

Presentation Brief:
- Purpose: [purpose]
- Audience: [audience]
- Key Messages: [messages]
- Duration: [duration]

Please provide:
1. Presentation storyline with slide-by-slide outline
2. Executive summary slide content
3. Key data visualization recommendations
4. Talking points for each major section
5. Anticipated questions and responses
6. Appendix recommendations
```

## Example

### Input

```text
Design a client presentation for LogiWorld Global Shipping.

Presentation Brief:
- Purpose: Present digital twin solution to reduce conveyor downtime
- Audience: COO, VP Operations, regional fulfillment leaders
- Key Messages: Current model costs $2M/year; solution reduces downtime by 40%
- Duration: 30 minutes total with 5 min exec summary, 10 min analysis
```

### Expected Output

```text
## Presentation Outline: Digital Twin Solution for LogiWorld

### Storyline Arc
1. **Hook**: Downtime costs $2M/year - there's a better way
2. **Problem**: Current reactive maintenance fails 40% of the time
3. **Solution**: Digital twin predicts failures before they happen
4. **Proof**: Case study - reduced downtime 40% at similar facility
5. **Ask**: Pilot program approval for 2 facilities

### Slide-by-Slide Outline

| Slide | Title | Content | Time |
|-------|-------|---------|------|
| 1 | Title | LogiWorld Digital Twin Proposal | 30s |
| 2 | Exec Summary | 3 bullets: Problem, Solution, ROI | 2 min |
| 3 | The $2M Problem | Downtime cost breakdown by facility | 2 min |
| 4 | Root Cause Analysis | Why current maintenance fails | 3 min |
| 5 | Digital Twin Solution | How predictive maintenance works | 3 min |
| 6 | Case Study | 40% reduction at CompetitorCo | 3 min |
| 7 | Implementation Plan | 90-day pilot roadmap | 2 min |
| 8 | Investment & ROI | $400K investment, $800K annual savings | 2 min |
| 9 | Recommendation | Approve 2-facility pilot | 2 min |
| 10 | Q&A | Discussion | 10 min |

### Executive Summary Slide
- **Challenge**: Conveyor downtime costs LogiWorld $2M annually
- **Solution**: Digital twin technology reduces unplanned downtime by 40%
- **Ask**: Approve $400K pilot for Chicago and Dallas facilities
- **ROI**: 6-month payback, $800K annual savings at scale

### Anticipated Questions
1. "Why these two facilities?" - Highest downtime, willing leadership
2. "What's the implementation risk?" - Phased approach, rollback capability
3. "How does this compare to upgrading equipment?" - 3x better ROI
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
