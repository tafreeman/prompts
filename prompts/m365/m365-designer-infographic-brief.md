---
title: "M365 Designer Infographic Brief"
description: "Transforms raw data points and key messages into a structured design brief for creating infographics in Microsoft Designer."
category: "creative"
tags: ["m365", "designer", "infographic", "data-visualization", "communication"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

Creating an infographic in Microsoft Designer starts with a clear vision. This prompt takes your statistics and key takeaways and converts them into a "Design Brief" that describes the layout, icons, and text hierarchy. You can use this brief to prompt Designer or as a guide for manual assembly.

## Goal

To structure data and insights into a visual plan that Microsoft Designer can generate or help you build.

## Inputs

- **Topic**: [topic]
- **Key Data Points**: [data_points]
- **Target Audience**: [audience]
- **Visual Style**: [visual_style]

## Prompt

You are an expert Information Designer. I have some data that I need to turn into an infographic using Microsoft Designer.

**Context:**

- **Topic**: [topic]
- **Key Data/Stats**: [data_points]
- **Audience**: [audience]
- **Visual Style**: [visual_style]

Please generate a **Design Brief** for this infographic:

1. **Headline**: A catchy title for the graphic.
2. **Layout Concept**: Describe the visual structure (e.g., "Timeline", "Comparison Split", "Central Hub").
3. **Designer Prompt**: A specific text prompt I can paste into Microsoft Designer to generate the *background* or *base layout* for this infographic.
4. **Iconography**: Suggestions for 3-4 icons to search for in the Designer asset library.
5. **Text Hierarchy**: Which data point should be big (Hero) vs. small (Supporting).

## Variables

- `[topic]`: What the infographic is about (e.g., "Remote Work Trends").
- `[data_points]`: The numbers or facts to include (e.g., "70% productivity increase, 20% cost saving").
- `[audience]`: Who is reading it (e.g., "HR Managers").
- `[visual_style]`: The look (e.g., "Corporate Blue", "Playful Illustration", "Minimalist Line Art").

## Example Usage

**Input:**

- `[topic]`: "Benefits of Coffee"
- `[data_points]`: "Boosts energy, contains antioxidants, improves focus."
- `[audience]`: "Office Workers"
- `[visual_style]`: "Warm, cozy, cafe style"

**Output:**

### Infographic Design Brief

**Headline**: Fuel Your Day: The Power of Coffee

**Layout Concept**:
A central illustration of a steaming coffee cup with three arrows pointing outwards to the benefits.

**Designer Prompt**:
"A warm, cozy infographic background featuring a central illustration of a ceramic coffee cup on a wooden table. Steam rising in swirls. Surrounding space is clean cream color for text. Style is flat vector illustration with warm brown and orange tones."

**Iconography**:

- **Lightning Bolt** (for Energy)
- **Shield** (for Antioxidants)
- **Brain/Lightbulb** (for Focus)

**Text Hierarchy**:

- **HERO**: "Boosts Energy" (Largest font)
- **SUPPORTING**: "Antioxidants" & "Focus" (Medium font)

## Tips

- Microsoft Designer works best when you generate the *background* first, then add text and icons as layers on top.
- Use the "Designer Prompt" output to get that base image.

## Related Prompts

- `m365-designer-image-prompt-generator`
- `m365-slide-content-refiner`

## Changelog

- 2025-11-18: Initial version created.
