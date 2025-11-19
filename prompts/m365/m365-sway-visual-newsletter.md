---
title: "M365 Sway Visual Newsletter"
description: "Compiles team updates, news, and announcements into a modern, mobile-friendly newsletter format for Microsoft Sway."
category: "communication"
tags: ["m365", "sway", "newsletter", "internal-comms", "updates"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

Internal newsletters often get ignored in email inboxes. This prompt helps you aggregate various updates (from Teams, email, or notes) and format them into a visually engaging Sway newsletter. It organizes content into "Hero" sections for big news and "Grid" layouts for quick updates, ensuring high engagement.

## Goal

To create a visually rich, easy-to-read newsletter structure that looks great on both desktop and mobile.

## Inputs

- **Newsletter Title**: [newsletter_title]
- **Main Feature Story**: [main_story]
- **Quick Updates**: [quick_updates]
- **Upcoming Events**: [events]
- **Team Shoutouts**: [shoutouts]

## Prompt

You are an Internal Communications Specialist. I need to create this week's team newsletter in Microsoft Sway.

**Content:**

- **Title**: [newsletter_title]
- **Main Feature**: [main_story]
- **Quick Updates**: [quick_updates]
- **Events**: [events]
- **Shoutouts**: [shoutouts]

Please design the **Sway Structure** for this newsletter:

1. **Hero Section**: A high-impact Heading 1 + Background Image + Intro Text for the [main_story].
2. **The "Quick Hits" Grid**: A Grid Group layout for the [quick_updates] (short text + icon/image).
3. **Calendar Section**: A text card listing [events].
4. **Kudos Corner**: A Stack Group or Slideshow for [shoutouts].

For each section, provide the **exact text** to paste and a **visual description** for the images I should find.

## Variables

- `[newsletter_title]`: e.g., "The Weekly Pulse - Nov 18".
- `[main_story]`: The biggest news item (e.g., "Q4 Goals Achieved").
- `[quick_updates]`: Bullet points of smaller news items.
- `[events]`: Dates and times of upcoming meetings/socials.
- `[shoutouts]`: Recognition for specific team members.

## Example Usage

**Input:**

- `[newsletter_title]`: "Engineering Weekly"
- `[main_story]`: "We successfully migrated to the new cloud server with zero downtime!"
- `[quick_updates]`: "New hire John starts Monday. Security training due Friday. Cafeteria menu changed."
- `[events]`: "Town Hall: Wed 2pm. Hackathon: Friday all day."
- `[shoutouts]`: "Thanks to Sarah for working late on the migration."

**Output:**

### Sway Newsletter Structure

**1. Hero Section (The Big Win)**

- **Heading 1**: "Zero Downtime: Cloud Migration Complete!"
  - *Visual*: High-res photo of servers or a "Success" concept.
- **Text Card**: "Huge milestone achieved! The team successfully migrated to the new cloud server without a single minute of downtime. This sets us up for a faster, more scalable future."
  - *Emphasis*: Intense

**2. Quick Hits (Grid Group)**

- **Card A**: "Welcome John!" (New Hire)
  - *Visual*: Icon of a handshake or team.
- **Card B**: "Security Training Due" (Reminder)
  - *Visual*: Shield icon.
- **Card C**: "New Cafeteria Menu" (FYI)
  - *Visual*: Food/Burger icon.

**3. Calendar (Text Card)**

- **Heading 2**: "Mark Your Calendars"
- **Text**:
  - 📅 **Wed @ 2pm**: Town Hall
  - 🚀 **Fri (All Day)**: Hackathon

**4. Kudos Corner (Stack Group)**

- **Heading 2**: "Team Shoutouts"
- **Image Card**: Photo of Sarah (or a "Thank You" graphic).
  - **Caption**: "Big thanks to **Sarah** for the late-night effort on the migration!"

## Tips

- In Sway, use the "Design" tab to apply a "Style" that matches your company brand (e.g., specific fonts/colors).
- The "Grid Group" is perfect for 3-4 small items of equal importance.

## Related Prompts

- `m365-sway-document-to-story`
- `m365-email-triage-helper`

## Changelog

- 2025-11-18: Initial version created.
