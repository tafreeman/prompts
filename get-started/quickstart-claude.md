---
title: Quickstart for Claude
shortTitle: Claude Quickstart
intro: Get productive with Anthropic Claude in 15 minutes. Learn the essential prompting
  patterns for analysis, writing, and code generation.
type: quickstart
difficulty: beginner
audience:
- junior-engineer
- senior-engineer
- senior-engineer
- project-manager
- business-analyst
platforms:
- claude
topics:
- quickstart
- claude
- analysis
author: Deloitte AI & Engineering
version: '1.0'
date: '2025-11-29'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
learningTrack: engineer-quickstart
---

# Quickstart for Claude

Get productive with Anthropic Claude in 15 minutes. By the end of this quickstart, you'll be able to analyze documents, write professional content, and generate code using Claude's unique capabilities.

## Prerequisites

- Access to Claude via [claude.ai](https://claude.ai) or the Anthropic API
- 15 minutes of focused time

## Step 1: Your First Interaction with Claude (3 minutes)

Claude responds best to clear, structured prompts. Let's start with a simple pattern.

### Pattern: Basic Structured Request

```text
I need help summarizing a meeting.

<context>
We had a 30-minute team standup with 5 developers. Topics included:
- Sprint progress (80% complete)
- Blocker: API integration delayed by vendor
- New feature request from product team
</context>

<task>
Create a 3-bullet summary suitable for sending to stakeholders.
</task>
```

**What happens**: Claude uses the XML tags to understand the separation between context and task. This produces more focused, accurate responses.

### Try It Now

1. Open Claude (claude.ai or API)
2. Paste the prompt above
3. Notice how Claude organizes its response around your structure

**Pro Tip**: Claude excels with XML tags like `<context>`, `<task>`, `<format>`, and `<constraints>`. Use them to separate different parts of your request.

## Step 2: Document Analysis (4 minutes)

Claude excels at analyzing long documents. It can process up to 200,000 tokens—roughly 150,000 words or 500 pages.

### Pattern: Document Analysis with XML Structure

```text
<document>
[Paste your document, report, or data here]
</document>

<task>
Analyze this document and provide:
1. Executive summary (3 sentences)
2. Key findings (bullet points)
3. Potential concerns or gaps
4. Recommended actions
</task>

<format>
Use headers for each section. Be concise but thorough.
</format>
```

### Try It Now

1. Find a document you need to analyze (report, article, meeting notes)
2. Paste it between `<document>` tags
3. Use the analysis task above
4. Review Claude's structured analysis

**Expected Output**: Claude will provide a well-organized analysis with clear sections matching your requested format.

### Variation: Comparative Analysis

```text
<document_a>
[First document]
</document_a>

<document_b>
[Second document]
</document_b>

<task>
Compare these documents and identify:
- Common themes
- Contradictions or conflicts
- Unique insights from each
</task>
```

## Step 3: Writing and Summarization (4 minutes)

Claude produces high-quality writing across many formats and tones.

### Pattern: Role-Based Writing

```text
<role>
You are a technical writer creating documentation for a developer audience.
</role>

<task>
Write a README section explaining how to install and configure our authentication library.
</task>

<requirements>
- Include code examples in Python and JavaScript
- Assume readers have basic programming knowledge
- Keep it under 300 words
- Include a troubleshooting tip
</requirements>

<tone>
Professional but approachable. Use "you" to address the reader.
</tone>
```

### Try It Now

1. Identify something you need to write (email, documentation, report)
2. Define the role Claude should adopt
3. Specify requirements and tone
4. Review and refine the output

### Pattern: Email Drafting

```text
<context>
I need to decline a vendor's proposal while keeping the door open for future work.
The proposal was over budget by 40% and missing key security requirements.
</context>

<task>
Draft a professional email (under 150 words) that:
- Thanks them for the proposal
- Explains we're going another direction
- Leaves door open for future opportunities
- Maintains positive relationship
</task>
```

## Step 4: Code Generation (4 minutes)

Claude generates code with explanations and follows best practices.

### Pattern: Code with Context and Constraints

```text
<task>
Write a Python function to validate and sanitize user input for a web form.
</task>

<requirements>
- Handle email, phone number, and free text fields
- Return sanitized values or raise descriptive exceptions
- Include type hints
- Follow PEP 8 style
</requirements>

<constraints>
- No external dependencies (standard library only)
- Must handle Unicode characters
- Include docstrings with examples
</constraints>
```

### Try It Now

1. Describe the code you need
2. Add specific requirements and constraints
3. Ask Claude to explain its implementation choices
4. Request modifications if needed

### Pattern: Code Review

```text
<code>
def process(data):
    result = []
    for i in range(len(data)):
        if data[i] != None:
            result.append(data[i] * 2)
    return result
</code>

<task>
Review this code and provide:
1. Issues found (bugs, style, performance)
2. Improved version with explanations
3. Test cases to verify the fix
</task>
```

## Quick Reference: XML Tag Patterns

| Tag | Purpose | Example Use |
|-----|---------|-------------|
| `<context>` | Background information | Meeting notes, project state |
| `<task>` | What you want Claude to do | "Summarize...", "Analyze..." |
| `<format>` | Output structure | "Use bullet points", "Markdown table" |
| `<constraints>` | Limitations and rules | "Under 200 words", "No jargon" |
| `<role>` | Persona for Claude | "You are a technical architect" |
| `<document>` | Content to analyze | Reports, code, articles |
| `<requirements>` | Specific needs | Feature list, acceptance criteria |
| `<tone>` | Communication style | "Professional", "Casual" |

## Quick Reference: High-Value Patterns

| Pattern | Use For |
|---------|---------|
| System prompt + XML | Complex, multi-step tasks |
| Role assignment | Specialized expertise |
| Few-shot examples | Teaching output format |
| Chain-of-thought | Complex reasoning tasks |
| Document analysis | Long-form content review |

## What You Learned

In 15 minutes, you learned to:

- ✅ Structure prompts with XML tags
- ✅ Analyze documents with Claude's long-context capability
- ✅ Generate professional writing with role-based prompts
- ✅ Create code with specific constraints

## Next Steps

Now that you have the basics, explore these paths:

### Continue Learning (Recommended)

1. **[About Prompt Engineering](/concepts/about-prompt-engineering)** - Understand how to craft effective prompts
2. **[Chain-of-Thought Prompting](/concepts/about-chain-of-thought)** - Advanced reasoning patterns
3. **[System Prompts](/prompts/system/system-prompt-template)** - Configure Claude's behavior

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

### Claude Refuses to Help

Claude is designed with Constitutional AI principles and will decline requests that could be harmful, unethical, or dangerous. If Claude refuses:

- Review your request for potentially problematic content
- Rephrase to focus on legitimate use cases
- Provide more context about your professional need

### Responses Are Too Long or Short

Add explicit length constraints:

```text
<constraints>
Response must be between 100-150 words.
</constraints>
```

Or for structured output:

```text
<format>
- Executive summary: 2 sentences
- Details: 5 bullet points maximum
- Next steps: 3 items
</format>
```

### Claude Misunderstands the Task

- Add more context about your situation
- Use XML tags to separate different parts of your request
- Provide an example of desired output
- Break complex requests into smaller steps

### Output Format Is Wrong

Specify exactly what you want:

```text
<format>
Return ONLY a JSON object with no additional text:
{
  "summary": "string",
  "items": ["array", "of", "strings"],
  "score": number
}
</format>
```

### Need More Help?

- [Troubleshooting Prompts](/troubleshooting/common-prompting-mistakes)
- [Anthropic Claude Documentation](https://docs.anthropic.com)

---

**Time to complete**: ~15 minutes  
**Difficulty**: Beginner  
**Platform**: Anthropic Claude

*Part of the [Engineer Quick-Start Track](/learning-tracks/engineer-quickstart)*
