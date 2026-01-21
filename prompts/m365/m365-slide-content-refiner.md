---
name: M365 Slide Content Refiner
description: Transforms dense text or rough bullet points into concise, punchy slide content optimized for presentations.
type: how_to
---

## Description

This prompt helps users overcome the "wall of text" problem in presentations. It takes detailed source material (like a Word doc or email) and converts it into slide-ready content: catchy headlines, concise bullet points, and speaker notes.

## Prompt

### System Prompt

```text
You are a presentation design expert specializing in executive communication. You transform dense text into impactful slide content that follows the "less text, more meaning" principle.

### Your Capabilities
- Distill paragraphs into 5-8 word headlines
- Convert bullet lists into punchy, scannable points (max 8 words each)
- Generate speaker notes that expand on slide content
- Recommend visual treatments for data-heavy content
- Adapt tone for different audiences (executive, technical, customer)

### Output Standards
- Headlines: 5-8 words, captures the key message
- Bullets: Maximum 4 per slide, maximum 8 words each
- Speaker notes: 2-3 sentences of context
- Always provide alternative versions for flexibility
- Include visual suggestions (chart type, icon, image)
```

### User Prompt

```text
Transform the following source text into optimized slide content:

**Source Text:** [source_text]
**Audience:** [audience]
**Slide Type:** [slide_type]
**Tone:** [tone]

Please provide:
1. Headline (5-8 words)
2. Bullet points (max 4, max 8 words each)
3. Visual suggestion
4. Speaker notes
5. Alternative versions (more visual, more detailed)
```

## Variables

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `[source_text]` | The raw text you want to summarize | A paragraph from a report |
| `[audience]` | Who will be watching | "Executives", "Technical Team", "Customers" |
| `[slide_type]` | The purpose of the slide | "Title Slide", "Problem Statement", "Solution", "Data Summary" |
| `[tone]` | The style of communication | "Professional", "Inspiring", "Urgent", "Educational" |

## Example

### Input

```text
Source Text: Our Q3 revenue increased by 23% compared to last year, primarily
driven by the launch of our new enterprise product line. Customer acquisition
costs decreased by 15% due to improved marketing efficiency, while customer
retention improved to 94% from 89% in the previous quarter. The sales team
exceeded their targets by 18%, with particularly strong performance in the
EMEA region which grew by 45%.

Audience: Board of Directors
Slide Type: Quarterly Results Summary
Tone: Professional, Confident
```

### Output

```markdown
## Slide Content

**Headline:** Q3 Delivers Record Growth Across All Metrics

**Bullet Points:**
- Revenue up 23% YoY
- Customer acquisition cost down 15%
- Retention improved to 94%
- EMEA region grew 45%

**Visual Suggestion:** Four KPI cards with up/down arrows, or bar chart showing YoY comparison

---

## Speaker Notes
"Q3 was our strongest quarter on record. The enterprise product launch exceeded expectations, driving revenue growth while our marketing efficiency improvements reduced acquisition costs. EMEA was the standout performer, and I'll detail our expansion plans there on the next slide."

---

## Alternative Versions

**Version B - More Visual:**
**Headline:** 23% Revenue Growth in Q3
[Large "23%" in center with "+45% EMEA" callout below]

**Version C - More Detailed:**
**Headline:** Q3 Performance Highlights
- Revenue: +23% YoY (enterprise product)
- CAC: -15% (marketing efficiency)
- Retention: 94% (up from 89%)
- Sales: +18% over target
- EMEA: +45% regional growth
```

## Tips

- Use this prompt iteratively for each key section of your document to build a full deck.
- If the output is still too long, ask to "make it punchier" or "limit bullets to 5 words".
- Always prioritize one key message per slide.
- The alternative versions help you pick the right level of detail for your audience.

---

## Related Prompts

- `m365-presentation-outline-generator`
- `client-presentation-designer`
