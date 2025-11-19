---
title: "M365 Designer Social Media Kit"
description: "Generates a cohesive set of image prompts for Microsoft Designer to create matching assets for Instagram, LinkedIn, and Twitter/X from a single content piece."
category: "creative"
tags: ["m365", "designer", "social-media", "marketing", "branding"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Intermediate"
platform: "Microsoft 365 Copilot"
---

## Description

Marketing teams often need to promote a single blog post or announcement across multiple channels with different visual requirements. This prompt takes your core content and generates specific Microsoft Designer prompts for a "Square" (Instagram), "Landscape" (LinkedIn/Twitter), and "Story" (Vertical) format, ensuring visual consistency across the campaign.

## Goal

To create a suite of matching social media visual prompts that can be generated in Microsoft Designer for a multi-channel campaign.

## Inputs

- **Content Topic**: [topic]
- **Key Headline**: [headline]
- **Brand Style**: [brand_style]
- **Visual Elements**: [visual_elements]

## Prompt

You are a Social Media Design Lead. I have a new piece of content to promote, and I need to generate a "Social Media Kit" using Microsoft Designer.

**Campaign Details:**

- **Topic**: [topic]
- **Headline**: [headline]
- **Brand Style**: [brand_style]
- **Key Visual Elements**: [visual_elements]

Please write **3 specific prompts** to paste into Microsoft Designer. All three must share the same aesthetic but be optimized for different aspect ratios and layouts:

1. **The "Feed Post" (Square 1:1)**: Focus on a central visual with space for the headline.
2. **The "Link Card" (Landscape 16:9)**: Optimized for LinkedIn/Twitter previews. Wide layout.
3. **The "Story" (Vertical 9:16)**: Tall layout with negative space at the top/bottom for stickers/text.

**For each prompt, include:**

- **Aspect Ratio keyword**: (e.g., "Square image", "Wide image").
- **Subject Description**: How to arrange the [visual_elements].
- **Style Instructions**: Ensuring the [brand_style] is consistent.

## Variables

- `[topic]`: e.g., "New Product Launch: Eco-Bottle".
- `[headline]`: e.g., "Hydration Reimagined".
- `[brand_style]`: e.g., "Minimalist, Matte finish, Pastel colors".
- `[visual_elements]`: e.g., "Water bottle, water splash, leaves".

## Example Usage

**Input:**

- `[topic]`: "Remote Work Tips Blog Post"
- `[headline]`: "Mastering the Home Office"
- `[brand_style]`: "Modern, Tech, Blue and Orange gradients"
- `[visual_elements]`: "Laptop, coffee cup, abstract connectivity lines"

**Output:**

### Designer Prompts

**1. Square Feed Post (Instagram)**
"A square 3D render of a modern home office desk setup with a laptop and coffee cup. Abstract blue and orange connectivity lines glowing in the background. Minimalist style, matte finish. Central composition with empty space in the center for text overlay."

**2. Landscape Link Card (LinkedIn)**
"A wide 16:9 image featuring a sleek laptop on the left side and abstract tech lines flowing to the right. Blue and orange gradient background. Professional and clean look suitable for a blog header. High resolution, 3D style."

**3. Vertical Story (TikTok/Reels)**
"A tall 9:16 vertical background image. At the bottom, a small 3D laptop and coffee cup. The top 70% is a clean, soft blue gradient with subtle orange abstract lines, leaving ample negative space for text and stickers. Modern tech aesthetic."

## Tips

- In Microsoft Designer, you can often select the aspect ratio *before* or *after* generation, but including keywords like "wide" or "tall" in the prompt helps the AI compose the scene correctly.
- Use the "Brand Kit" feature in Designer to apply your exact hex codes after the image is generated.

## Related Prompts

- `m365-designer-image-prompt-generator`
- `m365-sway-visual-newsletter`

## Changelog

- 2025-11-18: Initial version created.
