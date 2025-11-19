---
title: "M365 Sway Document to Story"
description: "Converts a standard Word document or report into an engaging Microsoft Sway storyline structure with visual suggestions."
category: "creative"
tags: ["m365", "sway", "storytelling", "presentation", "content-creation"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

Microsoft Sway is a powerful tool for digital storytelling, but pasting a flat Word document into it often looks boring. This prompt takes your text content and restructures it into Sway's native "Card" format—suggesting where to use Headings, Text Cards, Image Stacks, and Comparisons to make the content interactive and visually appealing.

## Goal

To transform linear text into a dynamic, interactive Sway storyline structure.

## Inputs

- **Document Content**: [document_content]
- **Target Audience**: [audience]
- **Key Message**: [key_message]

## Prompt

You are a Digital Storyteller expert in Microsoft Sway. I have a document that I want to turn into an engaging Sway presentation.

**Context:**

- **Source Text**: [document_content]
- **Audience**: [audience]
- **Key Takeaway**: [key_message]

Please restructure this content into a **Sway Storyline Plan**. For each section, specify:

1. **Card Type**: (e.g., Heading 1, Text, Image, Stack Group, Comparison, Grid).
2. **Content**: The specific text to put in that card (summarized/punchy).
3. **Visual Instruction**: What kind of image or media should go here?
4. **Emphasis**: (e.g., Subtle, Moderate, Intense).

**Structure the output like this:**

- **Section 1: Title & Intro**
- **Section 2: [Topic Name]**

## Variables

- `[document_content]`: The text from your Word doc or PDF (paste up to ~2000 words).
- `[audience]`: Who is viewing this Sway (e.g., "Students", "Clients", "Internal Team").
- `[key_message]`: The one thing they should remember.

## Example Usage

**Input:**

- `[document_content]`: "Our Q3 marketing results show a 20% increase in leads. The new Instagram campaign was the main driver. However, email open rates dropped by 5%. We recommend shifting budget to social media."
- `[audience]`: "Marketing Team"
- `[key_message]`: "Social is winning; Email needs a rethink."

**Output:**

### Sway Storyline Plan

**Section 1: Title & Intro**

- **Heading 1 (Background)**: "Q3 Marketing Review: The Shift to Social"
  - *Visual*: High-quality background image of people using smartphones.
- **Text Card**: "We saw a massive 20% jump in leads this quarter. Let's dive into what worked."
  - *Emphasis*: Moderate

**Section 2: The Wins (Social Media)**

- **Heading 2**: "Instagram Campaign Success"
- **Stack Group (Images)**: Screenshots of the top 3 performing posts.
- **Text Card**: "The new campaign was our primary driver for growth."

**Section 3: The Challenge (Email)**

- **Comparison Group**:
  - *Image A*: Graph showing Q2 Email Open Rates (High).
  - *Image B*: Graph showing Q3 Email Open Rates (Low).
- **Text Card**: "Email engagement dropped by 5%. It's time to pivot."

**Section 4: Conclusion**

- **Heading 1**: "Recommendation: Double Down on Social"
  - *Visual*: bold, inspiring abstract graphic.

## Tips

- Use "Stack Groups" for photo galleries (e.g., event photos).
- Use "Comparison" cards for Before/After scenarios.
- Copy the text from the "Content" fields directly into your Sway cards.

## Related Prompts

- `m365-sway-visual-newsletter`
- `m365-slide-content-refiner`

## Changelog

- 2025-11-18: Initial version created.
