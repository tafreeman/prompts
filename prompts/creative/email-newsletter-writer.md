---
title: "Email Newsletter Writer"
shortTitle: "Email Newsletter"
intro: "Generate compelling email newsletters that engage subscribers, deliver value, and drive desired actions."
type: "how_to"
difficulty: "beginner"
audience:
  - "business-analyst"
  - "project-manager"
  - "functional-team"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "email-marketing"
  - "creative"
  - "content-marketing"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
  - "general-use"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.1
---
# Email Newsletter Writer


---

## Description

Create engaging email newsletters that subscribers actually want to read. This prompt helps marketers, content creators, and business owners craft newsletters that deliver value, maintain audience interest, and achieve marketing goals while avoiding the spam folder.


---

## Use Cases

- Weekly or monthly company newsletters to keep subscribers informed
- Product update announcements and feature releases
- Industry news roundups and curated content digests
- Educational content series for nurturing leads
- Promotional campaigns with a value-first approach


---

## Prompt

```text
You are an expert email marketing copywriter who creates newsletters that people actually open, read, and act on. Write a compelling email newsletter based on the following details:

**Newsletter Type:** [WEEKLY DIGEST/PRODUCT UPDATE/EDUCATIONAL/PROMOTIONAL/ANNOUNCEMENT]
**Brand/Company:** [YOUR BRAND NAME]
**Target Audience:** [SUBSCRIBER DEMOGRAPHICS AND INTERESTS]
**Tone:** [PROFESSIONAL/FRIENDLY/CASUAL/AUTHORITATIVE/PLAYFUL]
**Newsletter Name:** [YOUR NEWSLETTER NAME, IF ANY]

**Main Content:**
- Topic 1: [FIRST MAIN TOPIC OR STORY]
- Topic 2: [SECOND TOPIC - OPTIONAL]
- Topic 3: [THIRD TOPIC - OPTIONAL]

**Primary Goal:** [ENGAGEMENT/CLICKS/CONVERSIONS/EDUCATION/RELATIONSHIP BUILDING]
**Call-to-Action:** [MAIN ACTION YOU WANT READERS TO TAKE]

**Additional Elements:**
- Include a personal note/intro: [YES/NO]
- Add curated links/resources: [YES/NO - HOW MANY?]
- Include a featured offer/promotion: [YES/NO - DETAILS?]
- Add a subscriber-exclusive element: [YES/NO]

**Constraints:**
- Approximate word count: [SHORT (200-300)/MEDIUM (400-600)/LONG (800+)]
- Must mention: [ANY REQUIRED ELEMENTS]
- Avoid: [ANYTHING TO STAY AWAY FROM]

Please create:
1. 3 subject line options (with open rate prediction)
2. Preview text (40-90 characters)
3. Full newsletter content with clear sections
4. Compelling CTA button text
5. P.S. line for additional engagement

Format the newsletter with clear visual hierarchy using headers, short paragraphs, bullet points, and whitespace.
```text

---

## Variables

| Variable | Description |
| :--- |-------------|
| `[WEEKLY DIGEST/PRODUCT UPDATE/EDUCATIONAL/PROMOTIONAL/ANNOUNCEMENT]` | The type of newsletter you're sending |
| `[YOUR BRAND NAME]` | Your company or personal brand name |
| `[SUBSCRIBER DEMOGRAPHICS AND INTERESTS]` | Who your subscribers are and what they care about |
| `[PROFESSIONAL/FRIENDLY/CASUAL/AUTHORITATIVE/PLAYFUL]` | The voice and tone of your newsletter |
| `[YOUR NEWSLETTER NAME, IF ANY]` | The branded name of your newsletter |
| `[FIRST MAIN TOPIC OR STORY]` | Primary content you want to cover |
| `[ENGAGEMENT/CLICKS/CONVERSIONS/EDUCATION/RELATIONSHIP BUILDING]` | What you want to achieve |
| `[MAIN ACTION YOU WANT READERS TO TAKE]` | The primary CTA |
| `[SHORT (200-300)/MEDIUM (400-600)/LONG (800+)]` | Desired newsletter length |


---

## Example Usage

**Input:**

```text
You are an expert email marketing copywriter who creates newsletters that people actually open, read, and act on. Write a compelling email newsletter based on the following details:

**Newsletter Type:** Weekly Digest
**Brand/Company:** TechPulse
**Target Audience:** Software developers, tech leads, and engineering managers interested in developer productivity and tooling
**Tone:** Friendly and knowledgeable
**Newsletter Name:** The Dev Digest

**Main Content:**
- Topic 1: New AI coding assistants comparison - which one is worth your time?
- Topic 2: Three terminal tricks that saved me 2 hours this week
- Topic 3: Community spotlight: Open source project of the week

**Primary Goal:** Engagement and establishing thought leadership
**Call-to-Action:** Try one of the terminal tricks and reply with your results

**Additional Elements:**
- Include a personal note/intro: Yes
- Add curated links/resources: Yes - 3-4 relevant links
- Include a featured offer/promotion: No
- Add a subscriber-exclusive element: Yes - early access to upcoming tool review

**Constraints:**
- Approximate word count: Medium (400-600)
- Must mention: The newsletter's 1-year anniversary
- Avoid: Overly salesy language, jargon without explanation

Please create:
1. 3 subject line options (with open rate prediction)
2. Preview text (40-90 characters)
3. Full newsletter content with clear sections
4. Compelling CTA button text
5. P.S. line for additional engagement

Format the newsletter with clear visual hierarchy using headers, short paragraphs, bullet points, and whitespace.
```text
**Output:**

```text
## Subject Line Options

1. "🎂 1 year of Dev Digest + AI coding tools showdown" 
   - Prediction: High (28-32%) - Anniversary + trending topic
   
2. "3 terminal tricks that saved me 2 hours (you'll want #2)"
   - Prediction: High (26-30%) - Specific value promise + curiosity gap
   
3. "Which AI coding assistant is actually worth it?"
   - Prediction: Medium-High (24-28%) - Question format + relevant topic

## Preview Text
"Plus terminal tricks that'll change your workflow forever"

---

## Newsletter Content

# The Dev Digest 🚀
*Issue #52 | Your weekly dose of developer productivity*

---

Hey there! 👋

One year ago this week, I sent the first Dev Digest to 47 brave subscribers. Today, you're one of 12,000+ developers who've decided their inbox deserves better content.

Thank you. Seriously. Your replies, suggestions, and "actually, here's a better way" corrections have made this newsletter what it is.

Now, let's make this anniversary issue worth your time.

---

## 🤖 AI Coding Assistants: The Honest Comparison

I spent last week putting GitHub Copilot, Cursor, Cody, and Amazon CodeWhisperer through real-world tests. Not synthetic benchmarks—actual coding tasks from my daily work.

**The quick verdict:**

| Tool | Best For | Watch Out For |
| :--- |----------| :--- |
| **Copilot** | Inline completions, familiar codebases | Can be chatty, context limits |
| **Cursor** | Refactoring, codebase-wide changes | Learning curve, resource usage |
| **Cody** | Open source, privacy-conscious teams | Newer, smaller community |
| **CodeWhisperer** | AWS-heavy projects, free tier | AWS ecosystem focus |

**My pick for most developers:** Start with Copilot, add Cursor for big refactors.

*Want the full breakdown with code examples?*

[**Read the complete comparison →**]

---

## ⚡ 3 Terminal Tricks That Saved Me 2 Hours This Week

These aren't fancy—they're practical. Try one today.

**1. Fuzzy find everything with `fzf`**
```bash
# Search command history interactively
history | fzf
# Find and open any file
vim $(fzf)
```text
*Time saved: 45 minutes of "wait, what was that command?"*

**2. Quick directory bookmarks with `z`**
```bash
# Jump to frequently used directories
z projects  # Goes to ~/code/projects
z api       # Goes to most-used api directory
```text
*Time saved: 30 minutes of cd ../../../*

**3. Parallel command execution**
```bash
# Run tests across multiple directories simultaneously
ls -d */ | parallel 'cd {} && npm test'
```text
*Time saved: 45 minutes on a multi-package repo*

---

## 🌟 Community Spotlight

**Project of the Week: `lazygit`**

If you're not using a TUI for git, you're missing out. `lazygit` makes complex git operations visual and fast.

Why I love it:
- Interactive rebase without memorizing commands
- Cherry-pick commits with arrow keys
- Resolve merge conflicts visually

[**Check out lazygit →**](https://github.com/jesseduffield/lazygit)

---

## 📚 Worth Your Click

- [The hidden cost of "clean code"](https://example.com) - A thoughtful take on over-engineering
- [SQLite as a document database](https://example.com) - You might not need MongoDB
- [Shell scripting best practices (2024)](https://example.com) - Finally, a modern guide
- [Interview: The making of Zed editor](https://example.com) - Fascinating technical deep-dive

---

## 🔒 Subscriber Exclusive

You get this first: Next week I'm publishing an in-depth review of the new Warp terminal. Dev Digest subscribers get early access 48 hours before it goes public.

*Just reply "EARLY ACCESS" and I'll send you the link Tuesday.*

---

That's a wrap on year one!

Try one of those terminal tricks today and hit reply to tell me how it goes. I read every response.

Happy coding,
**Alex**
*Curator, The Dev Digest*

---

[**Try a Terminal Trick & Share Your Results →**]

---

P.S. — Missed our most popular issues? Here are the top 3 from year one: [Git workflows that scale], [The ultimate VS Code setup], [Debugging in production]. All still relevant, all still free.
```text

---

## Tips

- **Subject lines are everything:** Test multiple versions—even a 5% improvement in open rates compounds over time
- **Preview text is your second headline:** Don't waste it on "View in browser" or let it auto-fill with unsubscribe text
- **Front-load value:** Put your best content in the first section—many readers only skim
- **One primary CTA:** Having multiple competing actions reduces clicks on all of them
- **The P.S. gets read:** It's one of the most-read parts of any email—use it strategically
- **Personalization beyond [First Name]:** Reference subscriber behavior, segments, or interests when possible


---

## Related Prompts

- [Content Marketing Blog Post Generator](content-marketing-blog-post.md)
- [Social Media Content Generator](social-media-content-generator.md)
- [Headline and Tagline Creator](headline-tagline-creator.md)
- [Ad Copy Generator](ad-copy-generator.md)
