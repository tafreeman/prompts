---
title: "Your First Prompt"
shortTitle: "First Prompt"
intro: "Learn the basics of prompting by creating and refining your first AI prompt."
type: tutorial
difficulty: beginner
audience:
  - junior-engineer
  - senior-engineer
  - business-analyst
  - project-manager
platforms:
  - github-copilot
  - claude
  - chatgpt
  - azure-openai
  - m365-copilot
topics:
  - fundamentals
  - getting-started
author: Prompt Library Team
version: '1.0'
date: '2025-11-29'
governance_tags:
  - PII-safe
dataClassification: public
reviewStatus: approved
---

# Your First Prompt

This tutorial will guide you through creating, testing, and refining your first AI prompt. By the end, you'll understand the basic principles that make prompts effective.

## Objectives

By completing this tutorial, you will:

- ✅ Write a basic prompt and get a useful response
- ✅ Understand why some prompts work better than others
- ✅ Learn the iteration process for improving prompts
- ✅ Apply three fundamental prompting techniques

## Prerequisites

- Access to any AI assistant (ChatGPT, Claude, Copilot, etc.)
- 15 minutes of time
- No prior prompting experience required

## Step 1: Start with a Simple Prompt

Let's start with the most basic prompt possible and see what happens.

### Try This Prompt

Open your AI assistant and enter:

```text
Write a summary.
```text
### What Happened?

The AI probably asked what you want summarized, or gave a generic response. This demonstrates the first principle:

> **Principle 1**: AI needs to know what you're working with.

The prompt failed because it lacked:
- Subject matter (what to summarize)
- Context (why you need it)
- Format (how long, what style)

## Step 2: Add Context

Let's improve by adding the subject matter.

### Try This Prompt

```text
Write a summary of the benefits of remote work.
```text
### What Happened?

You likely got a reasonable response this time! The AI had enough information to work with. But the output might be:
- Too long or too short for your needs
- Missing specific aspects you cared about
- In a format that doesn't work for you

> **Principle 2**: Specificity improves results.

## Step 3: Add Format Requirements

Now let's control how the output is structured.

### Try This Prompt

```text
Write a summary of the benefits of remote work.

Format as:
- A single paragraph
- Maximum 3 sentences
- Professional tone suitable for a business presentation
```text
### What Happened?

The response should now match your format requirements. This demonstrates:

> **Principle 3**: Explicit format instructions guide output structure.

## Step 4: Add Your Context

The best prompts include information about your specific situation.

### Try This Prompt

```text
I'm preparing a slide for our quarterly leadership meeting about updating our work-from-home policy.

Write a summary of the benefits of remote work.

Format as:
- A single paragraph
- Maximum 3 sentences  
- Professional tone suitable for executive audience
- Focus on productivity and retention benefits (our leadership cares most about these)
```text
### What Happened?

The response should now be:
- ✅ Correctly sized
- ✅ Appropriately toned
- ✅ Focused on your priorities
- ✅ Ready to use with minimal editing

## The Iteration Pattern

You've just experienced the iteration pattern that works for most prompts:

```text
Basic Prompt
    ↓ (not specific enough)
Add Subject
    ↓ (wrong format)
Add Format
    ↓ (not tailored to my situation)
Add Context
    ↓ (usable result!)
Done
```text
This pattern—starting simple and adding specificity—is faster than trying to write the perfect prompt on the first try.

## Practice Exercises

Try these exercises to reinforce what you learned:

### Exercise 1: Email Draft

Create a prompt for drafting an email, applying all three principles:

1. Start with: `Write an email.`
2. Add subject: What's the email about?
3. Add format: How long? What tone?
4. Add context: Who's it to? What's the situation?

### Exercise 2: Code Explanation

If you work with code, try:

1. Start with: `Explain this code.`
2. Add subject: Include actual code
3. Add format: Bullet points? Paragraph?
4. Add context: Who's the audience? What do they already know?

### Exercise 3: Meeting Agenda

Create a prompt for a meeting agenda:

1. Start with: `Create a meeting agenda.`
2. Add subject: What's the meeting about?
3. Add format: Duration? Number of items?
4. Add context: Who's attending? What's the goal?

## Common Mistakes to Avoid

### ❌ Too Vague

```text
Help me with my project.
```text
### ✅ Better

```sql
I'm working on a Python web scraper that collects product prices from e-commerce sites. I'm getting timeout errors when scraping large sites. What are some strategies to handle this?
```text
### ❌ Too Much at Once

```text
Write me a complete business plan with executive summary, market analysis, financial projections for 5 years, marketing strategy, operations plan, and team structure for a new AI startup.
```text
### ✅ Better

```text
Write an executive summary (250 words) for a business plan for an AI-powered customer service startup targeting mid-size e-commerce companies.
```text
(Then follow up with separate prompts for each section)

## What You Learned

✅ **Start simple** — Begin with basic prompts and add detail

✅ **Be specific** — Tell the AI exactly what you need

✅ **Specify format** — Describe how you want the output structured

✅ **Add context** — Explain your situation and requirements

✅ **Iterate** — Refine based on results

## Next Steps

Now that you understand the basics, continue learning:

1. **[Building Effective Prompts](/tutorials/building-effective-prompts)** — Learn all the prompt components
2. **[About Prompt Engineering](/concepts/about-prompt-engineering)** — Understand the theory
3. **[Platform Quickstarts](/get-started/)** — Apply skills to specific tools

---

**Congratulations!** You've written your first effective prompt. The skills you practiced here—adding context, specifying format, and iterating—apply to every AI interaction you'll have.
