---
name: M365 Weekly Review Coach
description: This prompt helps an individual knowledge worker run a weekly review using Microsoft 365 data. It summarizes key accomplishments, lessons learned, and generates a prioritized list of focus items fo...
type: how_to
---

# M365 Weekly Review Coach

## Use Cases

- Use case 1: A product manager reviewing a sprint and planning priorities for the next sprint.
- Use case 2: A team lead summarizing their week and preparing an update for their manager.
- Use case 3: An individual contributor aligning weekly work with personal development or OKRs.
- Use case 4: A consultant reviewing work across multiple client engagements.
- Use case 5: A support engineer reviewing incidents and planning process improvements.

## Example

**Inputs**

- `[week_start]`: `2025-11-10`
- `[week_end]`: `2025-11-14`
- `[focus_area]`: `customer onboarding`
- `[max_focus_items]`: `5`
- `[tone]`: `reflective but concise`

**Expected output (excerpt)**

```text
## Weekly Summary
This week you stabilized onboarding workflows and aligned stakeholders on a revised rollout plan.

## Key Accomplishments

- Closed two onboarding-related incidents and documented new troubleshooting steps.
- Updated onboarding FAQ content used by support.

## Focus for Next Week

- Secure leadership approval for the phased rollout and define success metrics.
- Validate the onboarding metrics dashboard and set up alerts.

```


## Tips

- Tip 1: Use `[focus_area]` to zoom the review in on a single project or theme when you're overloaded.
- Tip 2: Re-run the prompt mid-week with adjusted `[week_start]`/`[week_end]` for a mid-week checkpoint.
- Tip 3: Ask Copilot to turn the "Focus for Next Week" section into tasks in your preferred system.
- Tip 4: Share the Weekly Summary and Key Accomplishments as part of your regular manager update.

---

## Related Prompts

- `m365-daily-standup-assistant.md`
- `m365-project-status-reporter.md`
