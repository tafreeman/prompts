---
name: M365 Designer Image Prompt Generator
description: Converts concepts into detailed prompts for Microsoft Designer image generation.
type: how_to
---

# M365 Designer Image Prompt Generator

## Description

Generate sophisticated image descriptions for Microsoft Designer (DALL-E powered). Convert rough ideas into detailed prompts specifying style, lighting, composition, and mood for professional visuals.

## Prompt

You are a Visual Design Consultant helping create prompts for Microsoft Designer.

Generate a detailed image prompt based on my requirements.

### Requirements
**Subject/Topic**: [subject]
**Mood/Vibe**: [mood]
**Art Style**: [art_style]
**Brand Colors**: [brand_colors]
**Usage**: [usage]

### Output Format
Generate a single, detailed prompt (100-150 words) that includes:
- Subject description
- Composition and framing
- Lighting and atmosphere
- Color palette
- Style references

## Variables

- `[subject]`: E.g., "Team collaboration", "Cybersecurity concept".
- `[mood]`: E.g., "Professional", "Futuristic", "Warm".
- `[art_style]`: E.g., "Photorealistic", "Isometric 3D", "Minimalist".
- `[brand_colors]`: E.g., "Blue and white", "Neon green accents".
- `[usage]`: E.g., "Blog header", "Presentation slide".

## Example

**Input**:
Subject: AI and human collaboration
Mood: Optimistic, forward-looking
Style: Modern tech illustration
Colors: Blue, white, subtle gold accents
Usage: LinkedIn post header

**Response**:
### Designer Prompt
"A modern tech illustration showing a human hand and a robotic hand reaching toward each other, meeting in the center where a glowing orb of light represents shared ideas. Clean, minimalist composition with a gradient background from deep blue to white. Soft, diffused lighting creates an optimistic, welcoming atmosphere. Blue and white color scheme with subtle gold accent lines suggesting innovation. Professional corporate style suitable for business communications. No text, high resolution, 16:9 aspect ratio."
