---
title: Introduction to AI Prompts
shortTitle: Introduction to AI Prompts
intro: A prompt for introduction to ai prompts tasks.
type: how_to
difficulty: intermediate
audience:
- senior-engineer
- junior-engineer
platforms:
- github-copilot
- claude
- chatgpt
author: Prompts Library Team
version: '1.0'
date: '2025-11-30'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
---
# Introduction to AI Prompts

A beginner-friendly guide to understanding and using AI prompts effectively.

---

## What is a Prompt?

A **prompt** is the text you provide to an AI system to get a response. Think of it as giving instructions to a very capable assistant who needs clear direction to help you effectively.

### Simple Example

**Prompt:**
```
Write a professional email declining a meeting invitation due to a schedule conflict.
```

**AI Response:**
```
Subject: Re: Meeting Request - Unable to Attend

Dear [Name],

Thank you for the meeting invitation. Unfortunately, I have a prior commitment 
that conflicts with the proposed time.

I would be happy to:
- Receive meeting notes afterward
- Schedule an alternative time to discuss
- Provide any input beforehand

Please let me know how I can best contribute.

Best regards,
[Your Name]
```

---

## Why Do Prompts Matter?

The quality of your prompt directly affects the quality of the AI's response:

| Prompt Quality | Result Quality |
|----------------|----------------|
| Vague | Generic, unhelpful responses |
| Specific | Targeted, useful responses |
| Well-structured | Organized, professional output |
| With examples | Output matching your expectations |

### Example: The Difference Specificity Makes

❌ **Vague prompt:**
```
Help me with my presentation.
```
*Result: Generic tips about presentations*

✅ **Specific prompt:**
```
Create a 5-slide outline for a presentation about Q3 sales results 
to the executive team. Include: key metrics, top performers, 
challenges, and next quarter recommendations.
```
*Result: A structured outline you can actually use*

---

## Basic Prompt Structure

A good prompt typically includes these elements:

### 1. The Task

What do you want the AI to do?

```
Write / Summarize / Analyze / Create / Review / Explain...
```

### 2. The Subject

What is the prompt about?

```
...a code review / sales report / marketing email / project plan...
```

### 3. The Context

Any background information needed:

```
...for a software development team / targeting enterprise customers / 
following company guidelines...
```

### 4. The Format

How should the output be structured?

```
...as bullet points / in 3 paragraphs / as a table / in JSON format...
```

### Putting It Together

```
[TASK] [SUBJECT] [CONTEXT]. [FORMAT].
```

**Example:**
```
Summarize this customer feedback report for the product team. 
Focus on recurring themes and actionable improvements. 
Present as a prioritized bullet list with quick wins first.
```

---

## Types of Prompts

### Direct Prompts

Simple, straightforward requests:

```
Translate this text to Spanish: "Hello, how are you today?"
```

### Instructional Prompts

Step-by-step guidance:

```
Explain how to set up a Python virtual environment, 
step by step, for a Windows user new to programming.
```

### Role-Based Prompts

Assign a persona to the AI:

```
You are an experienced financial advisor. 
Review this investment portfolio and suggest improvements 
for a 35-year-old with moderate risk tolerance.
```

### Few-Shot Prompts

Provide examples to guide the output:

```
Convert these notes to formal action items:

Example:
Note: "talked to dev team - need more testing before release"
Action Item: • Development team requires additional testing phase before product release

Now convert:
Note: "marketing wants new landing page by friday"
```

### Chain-of-Thought Prompts

Ask the AI to show its reasoning:

```
Analyze whether we should expand to the European market.
Think through this step by step:
1. Current market conditions
2. Resource requirements
3. Potential challenges
4. Expected ROI
5. Final recommendation
```

---

## Placeholders: Making Prompts Reusable

**Placeholders** are variables in prompts that you replace with specific values. They're marked with `[BRACKETS]`:

```
Write a [TONE] email to [RECIPIENT] about [TOPIC].
Include a call to action to [DESIRED_ACTION].
```

**Filled in:**
```
Write a professional email to the sales team about Q4 targets.
Include a call to action to schedule planning meetings this week.
```

### Common Placeholders

| Placeholder | Replace With |
|-------------|--------------|
| `[YOUR_CODE]` | The code you want reviewed |
| `[TOPIC]` | The subject you're writing about |
| `[AUDIENCE]` | Who will read/use the output |
| `[FORMAT]` | How you want output structured |
| `[LANGUAGE]` | Programming or spoken language |
| `[TONE]` | Formal, casual, technical, etc. |

---

## Tips for Beginners

### Start Simple

Begin with straightforward prompts and add complexity as needed:

1. **First try:** "Summarize this article"
2. **If too long:** "Summarize this article in 3 bullet points"
3. **If too general:** "Summarize this article's main argument and supporting evidence in 3 bullet points"

### Be Explicit About Format

Tell the AI exactly how you want the output:

- "Answer in 2-3 sentences"
- "Create a table with columns for X, Y, Z"
- "List 5 bullet points"
- "Format as JSON"

### Provide Examples When Possible

Show the AI what you want:

```
Write product descriptions like this example:

Example: "The CloudPro 3000: Enterprise-grade cloud storage with 
military-grade encryption and 99.99% uptime guarantee."

Now write one for: A project management software for small teams
```

### Iterate and Refine

If the first response isn't right:

1. Add more specific instructions
2. Include an example of desired output
3. Clarify any misunderstood elements
4. Try rephrasing the request

---

## Using Prompts from This Library

### Step 1: Find a Prompt

Browse the `prompts/` folders by category:
- `developers/` - Coding and technical tasks
- `business/` - Business analysis and strategy
- `creative/` - Content and marketing
- `analysis/` - Data and research
- `advanced/` - Advanced AI techniques

### Step 2: Read the Description

Each prompt file includes:
- What the prompt does
- When to use it
- Required inputs
- Example usage

### Step 3: Copy the Prompt

Find the `## Prompt` section and copy the text.

### Step 4: Customize

Replace `[PLACEHOLDERS]` with your specific values.

### Step 5: Use

Paste into your AI tool (ChatGPT, Claude, Copilot, etc.).

---

## Common Beginner Mistakes

### ❌ Being too vague

**Instead of:** "Help me code"
**Try:** "Help me write a Python function that sorts a list of dictionaries by a specific key"

### ❌ Asking too many things at once

**Instead of:** "Write code, document it, test it, and deploy it"
**Try:** Start with one task, then follow up with the next

### ❌ Not specifying format

**Instead of:** "Analyze this data"
**Try:** "Analyze this data and present findings as a table with columns: Finding, Evidence, Recommendation"

### ❌ Assuming the AI knows context

**Instead of:** "Continue where we left off"
**Try:** Include necessary context in each prompt, or reference specific prior content

---

## Next Steps

Ready to learn more?

1. **Browse prompts**: Explore `prompts/` folders for examples
2. **Read best practices**: [Best Practices Guide](best-practices.md)
3. **Learn advanced techniques**: [Advanced Techniques](advanced-techniques.md)
4. **Create your own**: Use the [Prompt Template](../templates/prompt-template.md)

---

## Glossary

| Term | Definition |
|------|------------|
| **Prompt** | Text input to an AI system |
| **Placeholder** | Variable in `[BRACKETS]` to be replaced |
| **Few-shot** | Providing examples to guide output |
| **Chain-of-thought** | Asking AI to show reasoning steps |
| **Frontmatter** | YAML metadata at the top of prompt files |
| **LLM** | Large Language Model (ChatGPT, Claude, etc.) |

---

*Last Updated: 2025-11-28*
