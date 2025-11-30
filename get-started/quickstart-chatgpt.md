---
title: "Quickstart for ChatGPT"
shortTitle: "ChatGPT Quickstart"
intro: "Get productive with OpenAI ChatGPT in 15 minutes. Learn the essential prompting patterns for conversation, analysis, and creative tasks."
type: "quickstart"
difficulty: "beginner"
audience:
  - "junior-engineer"
  - "mid-engineer"
  - "senior-engineer"
  - "product-manager"
  - "business-analyst"
platforms:
  - "chatgpt"
topics:
  - "quickstart"
  - "chatgpt"
  - "conversation"
author: "Deloitte AI & Engineering"
date: "2025-11-29"
version: "1.0"
governance_tags:
  - "PII-safe"
learningTrack: "engineer-quickstart"
---

# Quickstart for ChatGPT

Get productive with OpenAI ChatGPT in 15 minutes. By the end of this quickstart, you'll be able to have effective conversations, analyze data with Code Interpreter, generate creative content, and set up Custom Instructions for personalized interactions.

## Prerequisites

- Access to ChatGPT via [chat.openai.com](https://chat.openai.com) (free tier works, Plus recommended)
- 15 minutes of focused time

## Step 1: Your First Conversation (3 minutes)

ChatGPT excels at natural, conversational interactions. It maintains context throughout your chat session, so you can build on previous messages.

### Pattern: Clear Request with Context

```text
I'm preparing for a client presentation tomorrow. Help me create an executive summary.

Background:
- Project: Cloud migration for a retail company
- Duration: 6 months
- Budget: $2.5M
- Status: 85% complete, on schedule

Create a 3-sentence executive summary highlighting progress and key achievements.
```

**What happens**: ChatGPT uses the conversational context to produce a focused response. You can then follow up with "Make it more technical" or "Add risk factors" without re-explaining the project.

### Try It Now

1. Open ChatGPT (chat.openai.com)
2. Paste the prompt above
3. Follow up with a refinement: "Now expand the second sentence with specific metrics"

**Pro Tip**: ChatGPT remembers everything in your current conversation. Use this to iterate—ask for changes, additions, or different perspectives without starting over.

### Conversational Follow-up Pattern

```text
[After initial response]

That's good. Now:
1. Add a risk section
2. Make the tone more confident
3. Include a call-to-action for the client
```

## Step 2: Data Analysis Task (4 minutes)

ChatGPT Plus and Team users have access to Code Interpreter (Advanced Data Analysis), which can process files, run Python code, and create visualizations.

### Pattern: Data Analysis with Code Interpreter

```text
I'm uploading a CSV file with quarterly sales data. Please:

1. Show me the first 10 rows to confirm the data loaded correctly
2. Calculate total revenue by region
3. Create a bar chart comparing Q3 vs Q4 performance
4. Identify the top 3 performing products

Format the insights as bullet points suitable for a presentation.
```

### Try It Now (Plus/Team Users)

1. Click the attachment icon or drag a file into the chat
2. Upload a CSV, Excel, or text file
3. Ask ChatGPT to analyze it using the pattern above
4. Request different visualizations: "Show this as a pie chart instead"

### Alternative: Analysis Without File Upload (Free Tier)

```text
Here's my sales data in table format:

| Region | Q3 Revenue | Q4 Revenue |
|--------|-----------|-----------|
| North  | $450,000  | $520,000  |
| South  | $380,000  | $410,000  |
| East   | $290,000  | $350,000  |
| West   | $510,000  | $480,000  |

Analyze this data and provide:
- Growth rate by region
- Best and worst performing regions
- Recommended focus areas for next quarter
```

**Pro Tip**: For complex analysis, ask ChatGPT to "show your work" or "explain your methodology" to verify the calculations.

## Step 3: Creative Writing and Brainstorming (4 minutes)

ChatGPT is excellent for brainstorming, creative writing, and generating multiple variations of content.

### Pattern: Brainstorming with Constraints

```text
I need 5 creative taglines for a sustainable coffee brand.

Requirements:
- Target audience: environmentally-conscious millennials
- Tone: Warm, authentic, slightly playful
- Length: Under 8 words each
- Must reference sustainability without being preachy

After listing them, explain which one you think is strongest and why.
```

### Try It Now

1. Think of a creative challenge you're facing
2. Specify clear constraints (audience, tone, length)
3. Ask for multiple options
4. Request analysis of the options

### Pattern: Role-Play for Better Output

```text
You are an experienced marketing copywriter who specializes in B2B SaaS products.

Write a cold email introducing our project management tool to a VP of Engineering.

Context:
- Our tool integrates with GitHub and Jira
- Key differentiator: AI-powered sprint planning
- Target company size: 100-500 employees

Keep it under 150 words. Include a specific, low-commitment call-to-action.
```

### Generating Images with DALL-E

ChatGPT Plus users can generate images directly in chat:

```text
Create an image for my presentation slide about cloud computing.

Style: Clean, modern, corporate-appropriate
Elements: Abstract cloud shapes, connected nodes, blue and white color scheme
Avoid: Cartoonish elements, cluttered composition
Aspect ratio: 16:9 for a presentation slide
```

**Note**: Always verify generated images meet your organization's brand guidelines before using in official materials.

## Step 4: Custom Instructions Setup (4 minutes)

Custom Instructions let you set persistent preferences that apply to all new conversations, so ChatGPT knows your context without repeated explanation.

### Setting Up Custom Instructions

1. Click your profile icon (bottom left on desktop)
2. Select **Customize ChatGPT** (or **Custom Instructions**)
3. Fill in both sections:

#### Section 1: "What would you like ChatGPT to know about you?"

```text
I'm a Senior Product Manager at a B2B SaaS company (150 employees).
I work primarily with engineering, design, and customer success teams.
My company serves mid-market financial services clients.
I'm based in EST timezone and work standard business hours.
I value concise, actionable outputs over lengthy explanations.
```

#### Section 2: "How would you like ChatGPT to respond?"

```text
- Be direct and concise—skip unnecessary preamble
- Use bullet points for lists of 3+ items
- When I ask for help writing, match professional business tone
- For technical topics, assume I have basic knowledge but explain advanced concepts
- If you're uncertain, say so rather than guessing
- Include relevant examples when explaining concepts
- Format code blocks properly with language specified
```

### Try It Now

1. Open Custom Instructions in your settings
2. Adapt the templates above to your role and preferences
3. Start a new conversation and notice the difference

**Pro Tip**: Update Custom Instructions when your role or projects change. They're especially powerful for establishing your expertise level and communication preferences.

### Testing Your Custom Instructions

After setting up, try this simple test:

```text
Help me write a status update for my weekly team meeting.
```

Without good Custom Instructions, you'd need to specify your role, audience, and preferred format. With them set up, ChatGPT should produce something appropriate automatically.

## Quick Reference: ChatGPT-Specific Features

| Feature | Availability | Best For |
|---------|-------------|----------|
| **GPT-4o** | Plus, Team, Enterprise | Complex reasoning, nuanced tasks |
| **GPT-4** | Plus, Team, Enterprise | Long-form analysis, detailed code |
| **Code Interpreter** | Plus, Team, Enterprise | Data analysis, file processing, Python |
| **DALL-E** | Plus, Team, Enterprise | Image generation |
| **Web Browsing** | Plus, Team, Enterprise | Current information lookup |
| **Custom Instructions** | All tiers | Persistent preferences |
| **Memory** | Plus, Team (where enabled) | Long-term personalization |

## Quick Reference: Effective Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Iterative refinement** | Building on responses | "Make it shorter" / "Add more detail" |
| **Role assignment** | Specialized expertise | "You are an experienced data analyst..." |
| **Explicit constraints** | Controlling output | "Under 200 words" / "5 bullet points" |
| **Format specification** | Structured output | "Format as a table" / "Return JSON" |
| **Chain questions** | Complex tasks | Ask sequentially, building on answers |
| **Show your work** | Verification | "Explain your reasoning" |

## What You Learned

In 15 minutes, you learned to:

- ✅ Have effective conversations that build on context
- ✅ Analyze data using Code Interpreter or inline tables
- ✅ Generate creative content with clear constraints
- ✅ Set up Custom Instructions for personalized interactions

## Next Steps

Now that you have the basics, explore these paths:

### Continue Learning (Recommended)

1. **[About Prompt Engineering](/concepts/about-prompt-engineering)** - Understand the principles behind effective prompts
2. **[Chain-of-Thought Prompting](/concepts/about-chain-of-thought)** - Advanced reasoning techniques
3. **[System Prompts](/prompts/system/system-prompt-template)** - Configure AI behavior for specific tasks

### By Your Role

| Role | Next Step |
|------|-----------|
| Business Analyst | [Business Analysis Prompts](/prompts/business/business-analysis) |
| Product Manager | [Product Requirements](/prompts/business/product-requirements) |
| Engineer | [Code Review Assistant](/prompts/developers/code-review-assistant) |

### Learning Track

Continue the **[Engineer Quick-Start Track](/learning-tracks/engineer-quickstart)** to become proficient in 1 week.

---

## Troubleshooting

### Responses Are Too Generic

Add specific context and constraints:

```text
Instead of: "Help me write an email"

Try: "Help me write a 100-word email to my engineering team announcing 
a deployment freeze. Tone: Direct but not alarming. Include the specific 
dates (Dec 15-Jan 2) and who to contact for exceptions."
```

### ChatGPT Won't Answer My Question

ChatGPT has content policies and may decline certain requests. If this happens:

- Rephrase to focus on legitimate professional use cases
- Provide context about why you need the information
- Break down complex requests into smaller, clearer parts

### Output Format Is Wrong

Be explicit about format requirements:

```text
Return your response as a JSON object with this exact structure:
{
  "summary": "string (max 50 words)",
  "keyPoints": ["array of 3-5 strings"],
  "recommendation": "string"
}

Return ONLY the JSON, no additional text.
```

### Conversation Lost Context

ChatGPT sessions have a context window limit. If responses seem disconnected:

- Summarize key context at the start of your message
- Start a new conversation for distinct topics
- Use Custom Instructions for persistent preferences

### Code Interpreter Not Working

- Verify you have ChatGPT Plus, Team, or Enterprise
- Check that the file format is supported (CSV, Excel, PDF, images, text files)
- Try a simpler request first: "Read this file and show the first 5 rows"

### Need More Help?

- [Troubleshooting Prompts](/troubleshooting/common-prompting-mistakes)
- [OpenAI ChatGPT Documentation](https://help.openai.com)

---

**Time to complete**: ~15 minutes  
**Difficulty**: Beginner  
**Platform**: OpenAI ChatGPT

*Part of the [Engineer Quick-Start Track](/learning-tracks/engineer-quickstart)*
