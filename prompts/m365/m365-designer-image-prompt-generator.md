---
title: "M365 Designer Image Prompt Generator"
description: "Converts abstract concepts or document themes into highly detailed, artistic prompts for Microsoft Designer to generate professional imagery."
category: "creative"
tags: ["m365", "designer", "image-generation", "dall-e", "visuals"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

Microsoft Designer (powered by DALL-E) requires specific, descriptive instructions to create high-quality images. This prompt takes your rough ideas or document context and expands them into a "prompt engineering" format that specifies style, lighting, composition, and mood, ensuring you get the perfect visual asset.

## Goal

To generate a sophisticated image description that can be pasted directly into Microsoft Designer to create professional, on-brand visuals.

## Inputs

- **Subject/Topic**: [subject]
- **Mood/Vibe**: [mood]
- **Art Style**: [art_style]
- **Brand Colors**: [brand_colors]

## Prompt

You are an expert AI Art Director. I need you to write a detailed image generation prompt that I can use in Microsoft Designer.

**Context:**

- **Subject**: [subject]
- **Desired Mood**: [mood]
- **Art Style**: [art_style]
- **Brand/Color Palette**: [brand_colors]

Please write **3 distinct prompt options** for Microsoft Designer. Each option should include details on:

1. **Subject**: What is happening in the scene?
2. **Environment**: Background and setting.
3. **Lighting**: (e.g., cinematic, soft, studio, natural).
4. **Style**: (e.g., 3D render, flat illustration, photorealistic, oil painting).
5. **Composition**: (e.g., wide angle, macro, isometric).

**Format the output as:**

- **Option 1 (Literal)**: A direct representation.
- **Option 2 (Abstract)**: A metaphorical or creative interpretation.
- **Option 3 (Minimalist)**: A clean, simple version suitable for backgrounds.

## Variables

- `[subject]`: The core concept (e.g., "Team collaboration", "Cybersecurity shield", "Future of AI").
- `[mood]`: The feeling (e.g., "Professional", "Energetic", "Calm", "Futuristic").
- `[art_style]`: The visual technique (e.g., "Photorealistic", "Isometric 3D", "Watercolor", "Tech Line Art").
- `[brand_colors]`: Specific colors to include (e.g., "Blue and White", "Neon Green accents").

## Example Usage

**Input:**

- `[subject]`: "Sustainable Energy in a Smart City"
- `[mood]`: "Optimistic and Clean"
- `[art_style]`: "Isometric 3D Render"
- `[brand_colors]`: "Green, White, and Soft Blue"

**Output:**

### Designer Prompts

**Option 1 (Literal)**
"A high-quality isometric 3D render of a futuristic smart city block, featuring solar panels on rooftops and wind turbines integrated into skyscrapers. The streets are clean with electric vehicles. Lighting is bright and sunny, casting soft shadows. Color palette focuses on fresh greens, crisp whites, and soft blues to convey sustainability."

**Option 2 (Abstract)**
"An artistic 3D composition showing a glowing green leaf transforming into a digital city grid. The leaf veins become roads and data streams. Floating particles of white and blue light surround the structure. Cinematic lighting with a shallow depth of field. Optimistic and futuristic atmosphere."

**Option 3 (Minimalist)**
"A simple, clean isometric icon of a single eco-friendly building with a small tree on top. White background with soft ambient occlusion. Minimal details, using only shades of green and blue. Perfect for a presentation icon."

## Tips

- Paste the output text directly into the "Describe the image you'd like to create" box in Microsoft Designer.
- If the result isn't right, try adding "no text" or "high resolution" to the generated prompt.

## Related Prompts

- `m365-designer-infographic-brief`
- `m365-slide-content-refiner`

## Changelog

- 2025-11-18: Initial version created.
