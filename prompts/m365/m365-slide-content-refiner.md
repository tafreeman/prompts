---
title: "M365 Slide Content Refiner"
description: "Transforms dense text or rough bullet points into concise, punchy slide content optimized for presentations."
category: "creative"
tags: ["m365", "powerpoint", "presentation", "copywriting", "communication"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

This prompt helps users overcome the "wall of text" problem in presentations. It takes detailed source material (like a Word doc or email) and converts it into slide-ready content: catchy headlines, concise bullet points, and speaker notes.

## Goal

To distill complex information into clear, impactful slide content that follows presentation best practices (less text, more meaning).

## Inputs

- **Source Text**: [source_text]
- **Audience**: [audience]
- **Slide Type**: [slide_type]
- **Tone**: [tone]

## Prompt

You are an expert presentation designer and copywriter. I need you to refine the following text for a PowerPoint slide.

**Context:**

- **Source Material**: [source_text]
- **Target Audience**: [audience]
- **Slide Type**: [slide_type]
- **Desired Tone**: [tone]

Please generate content for **one slide** with the following structure:

1. **Headline**: A punchy, action-oriented title (max 8 words).
2. **Body Content**: 3-5 concise bullet points (max 15 words each). Focus on the "so what?" or key takeaways.
3. **Speaker Notes**: A short paragraph explaining the details that were removed from the slide, to be spoken verbally.
4. **Visual Idea**: A brief suggestion for an image, icon, or chart that would support this content.

## Variables

- `[source_text]`: The raw text you want to summarize (e.g., a paragraph from a report).
- `[audience]`: Who will be watching (e.g., "Executives", "Technical Team", "Customers").
- `[slide_type]`: The purpose of the slide (e.g., "Title Slide", "Problem Statement", "Solution", "Data Summary").
- `[tone]`: The style of communication (e.g., "Professional", "Inspiring", "Urgent", "Educational").

## Example Usage

**Input:**

- `[source_text]`: "We have observed that the current server infrastructure is aging and causing 15% downtime per month. This is leading to customer churn. We propose migrating to Azure to improve reliability to 99.9% and reduce maintenance costs by 20% over 3 years."
- `[audience]`: "CTO and Finance Director"
- `[slide_type]`: "Proposal/Solution"
- `[tone]`: "Persuasive and Data-driven"

**Output:**

### Slide Content

**Headline**: Modernizing Infrastructure to Stop Churn and Cut Costs

**Body Content**:

- **Current Issue**: Aging servers causing 15% monthly downtime.
- **Business Impact**: Direct correlation to increased customer churn.
- **The Solution**: Migrate to Azure cloud infrastructure.
- **ROI**: 99.9% uptime and 20% cost reduction (3-year horizon).

**Speaker Notes**:
"Currently, our on-prem hardware is the bottleneck, costing us both uptime and customers. By shifting to Azure, we not only solve the reliability issue immediately but also lock in significant long-term savings on maintenance. This isn't just a tech upgrade; it's a retention strategy."

**Visual Idea**: A split comparison chart: "Current State" (High Downtime/Cost) vs. "Future State" (High Reliability/Savings).

## Tips

- Use this prompt iteratively for each key section of your document to build a full deck.
- If the output is still too long, ask Copilot to "make it punchier" or "limit bullets to 5 words".

## Related Prompts

- `m365-presentation-outline-generator`
- `client-presentation-designer`

## Changelog

- 2025-11-18: Initial version created.
