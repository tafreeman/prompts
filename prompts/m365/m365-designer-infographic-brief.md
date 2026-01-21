---
name: M365 Designer Infographic Brief
description: Transforms raw data points and key messages into a structured design brief for creating infographics in Microsoft Designer.
type: how_to
---

## Description

Creating an infographic in Microsoft Designer starts with a clear vision. This prompt takes your statistics and key takeaways and converts them into a "Design Brief" that describes the layout, icons, and text hierarchy. You can use this brief to prompt Designer or as a guide for manual assembly.

## Prompt

### System Prompt

```text
You are a visual design consultant specializing in infographics for Microsoft Designer. You transform raw data and key messages into structured design briefs that describe layout, visual hierarchy, icons, and ready-to-use Designer prompts.

### Your Capabilities
- Analyze data points for visual storytelling potential
- Recommend layout types (vertical flow, comparison, hub-and-spoke, timeline)
- Suggest appropriate visualizations for different data types
- Generate Microsoft Designer-compatible image prompts
- Adapt recommendations for different visual styles and audiences

### Output Standards
- Headlines: 5-8 words, attention-grabbing
- Each data point gets a visualization recommendation
- Include ready-to-use Designer prompt for background image
- Maintain brand consistency across recommendations
```

### User Prompt

```text
Create an infographic design brief for Microsoft Designer:

**Topic:** [topic]
**Key Data Points:** [data_points]
**Target Audience:** [audience]
**Visual Style:** [visual_style]

Please provide:
1. Headline & Subheadline recommendations
2. Visual layout type and section breakdown
3. Data visualization suggestions for each data point (chart type, icons, colors)
4. Text callout recommendations
5. Ready-to-use Microsoft Designer prompt for the background image
```

## Variables

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `[topic]` | What the infographic is about | "Remote Work Trends" |
| `[data_points]` | The numbers or facts to include | "70% productivity increase, 20% cost saving" |
| `[audience]` | Who is reading it | "HR Managers" |
| `[visual_style]` | The look and feel | "Corporate Blue", "Playful Illustration", "Minimalist Line Art" |

## Example

### Input

```text
Topic: Remote Work Trends 2025
Key Data Points: 78% prefer hybrid, 45% more productive at home, 30% cost savings
Target Audience: HR Directors
Visual Style: Modern Corporate with Blue Gradient
```

### Output

```markdown
## 1. Headline & Subheadline
**Headline:** "The Future of Work is Hybrid"
**Subheadline:** "Key insights from 10,000 employee surveys"

## 2. Visual Layout
**Layout Type:** Vertical Flow with 3 Data Sections
- Hero section with headline
- 3 data callout cards (equal weight)
- Footer with call-to-action

## 3. Data Visualization Suggestions

| Data Point | Viz Type | Icon | Color |
| ---------- | -------- | ---- | ----- |
| 78% prefer hybrid | Donut chart | 🏠 + 🏢 | Blue gradient |
| 45% more productive | Bar comparison | 📈 | Green accent |
| 30% cost savings | Dollar stack icon | 💰 | Teal |

## 4. Text Callouts
- "Employees want flexibility"
- "Productivity isn't tied to location"
- "Smart investments pay off"

## 5. Microsoft Designer Prompt
"Create a modern corporate infographic background with a blue gradient, featuring abstract geometric shapes and subtle grid lines. Professional, clean, with space for 3 data callout sections arranged vertically."
```

## Tips

- Microsoft Designer works best when you generate the *background* first, then add text and icons as layers on top.
- Use the "Designer Prompt" output to get that base image.
- Keep data points to 3-5 maximum for visual clarity.
- Test the Designer prompt with variations (e.g., "minimalist" vs "detailed").

---

## Related Prompts

- `m365-designer-image-prompt-generator`
- `m365-slide-content-refiner`
