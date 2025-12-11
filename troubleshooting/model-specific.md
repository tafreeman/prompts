---
title: "Model-Specific Troubleshooting"
shortTitle: "Model-Specific"
intro: "Platform-specific troubleshooting guides for GitHub Copilot, Claude, ChatGPT, and other AI assistants."
type: troubleshooting
difficulty: intermediate
audience:
  - junior-engineer
  - senior-engineer
  - solution-architect
  - business-analyst
platforms:
  - github-copilot
  - claude
  - chatgpt
  - azure-openai
  - m365-copilot
author: Prompt Library Team
version: '1.0'
date: '2025-11-29'
governance_tags:
  - PII-safe
dataClassification: public
reviewStatus: approved
---

# Model-Specific Troubleshooting

Each AI platform has unique characteristics, limitations, and optimal prompting patterns. This guide covers platform-specific issues and solutions.

---

## GitHub Copilot

### Issue: Suggestions Don't Match Project Style

**Symptoms:**
- Code suggestions use different naming conventions
- Imports don't match project patterns
- Wrong framework idioms

**Solutions:**

1. **Add context via comments:**
   ```python
   # Using Django REST Framework with snake_case naming
   # Following PEP 8 style guide
   ```

2. **Include examples in nearby code:**
   - Copilot learns from surrounding context
   - Add 2-3 functions following your style before requesting new ones

3. **Use a `.github/copilot-instructions.md` file:**
   ```markdown
   # Copilot Instructions
   - Use snake_case for Python variables
   - Prefer f-strings over .format()
   - Always include type hints
   ```

### Issue: Wrong Language or Framework

**Symptoms:**
- Getting JavaScript when you want TypeScript
- React suggestions in a Vue project
- Wrong test framework

**Solutions:**

1. **Specify in comment:**
   ```typescript
   // TypeScript with strict mode
   // Using Jest for testing
   ```

2. **Check file extension:**
   - Use `.ts` not `.js` for TypeScript
   - Use `.vue` for Vue single-file components

3. **Include framework imports at top:**
   ```typescript
   import { describe, it, expect } from 'vitest';
   ```

### Issue: Incomplete Function Generation

**Symptoms:**
- Function body is partial
- Missing error handling
- Incomplete logic

**Solutions:**

1. **Write signature and docstring first:**
   ```python
   def calculate_order_total(items: list[OrderItem], 
                            discount: float = 0) -> Decimal:
       """
       Calculate the total price for an order.
       
       Args:
           items: List of order items with price and quantity
           discount: Percentage discount (0-1)
           
       Returns:
           Total price after discount, rounded to 2 decimal places
           
       Raises:
           ValueError: If discount is not between 0 and 1
       """
       # Copilot will complete based on docstring
   ```

2. **Break complex functions into steps:**
   ```python
   def process_order(order):
       # Step 1: Validate order
       # Step 2: Calculate totals
       # Step 3: Apply discounts
       # Step 4: Return result
   ```

### Issue: Copilot Chat Not Understanding Context

**Solutions:**

1. **Use `@workspace` to include project context:**
   ```
   @workspace How do we handle authentication in this project?
   ```

2. **Reference specific files:**
   ```
   @workspace /src/auth/middleware.ts Explain this authentication flow
   ```

3. **Use agents for specific tasks:**
   ```
   @docs Create documentation for the UserService class
   ```

---

## Claude

### Issue: Response Cut Off Mid-Sentence

**Symptoms:**
- Response ends abruptly
- "I'll continue..." but doesn't
- Incomplete code blocks

**Solutions:**

1. **Request chunked output:**
   ```
   This is a long task. Please respond in parts:
   Part 1: [first section]
   Then say "CONTINUE?" and I'll ask for more.
   ```

2. **Be more specific to reduce length:**
   ```
   Focus only on the authentication module, not the entire codebase.
   ```

3. **Use explicit length guidance:**
   ```
   Provide a concise response (under 500 words).
   ```

### Issue: Over-Cautious or Excessive Caveats

**Symptoms:**
- Too many "however" and "it depends" qualifiers
- Reluctant to give direct recommendations
- Excessive disclaimers

**Solutions:**

1. **Give permission to be direct:**
   ```
   Please provide a direct recommendation. I understand 
   there are trade-offs; just tell me what you'd do.
   ```

2. **Set the context as internal/educational:**
   ```
   This is for an internal technical discussion. 
   Please be direct and specific.
   ```

3. **Request structured output:**
   ```
   Recommendation: [your pick]
   Confidence: [high/medium/low]
   Key caveat: [one sentence max]
   ```

### Issue: Not Using Full Context Window

**Symptoms:**
- Forgets information from earlier in conversation
- Asks for information you already provided
- Inconsistent with earlier statements

**Solutions:**

1. **Summarize key points periodically:**
   ```
   To recap our requirements:
   - Python 3.11
   - FastAPI framework
   - PostgreSQL database
   
   Now, continuing from where we left off...
   ```

2. **Use XML tags for structured context:**
   ```xml
   <context>
   Project: E-commerce API
   Stack: Python, FastAPI, PostgreSQL
   Current task: User authentication
   </context>
   
   <request>
   Design the login endpoint
   </request>
   ```

---

## ChatGPT

### Issue: Verbose Responses

**Symptoms:**
- Getting essays when you want bullet points
- Unnecessary preamble and conclusions
- Repeating information

**Solutions:**

1. **Set explicit constraints:**
   ```
   Answer in exactly 3 bullet points. No introduction 
   or conclusion. Maximum 20 words per bullet.
   ```

2. **Use direct instruction:**
   ```
   Skip the preamble. Just give me the answer.
   ```

3. **Request format first:**
   ```
   Format: One sentence answer, then supporting details 
   only if I ask follow-up questions.
   ```

### Issue: Hallucinated APIs or Libraries

**Symptoms:**
- Suggests functions that don't exist
- Wrong method signatures
- Fabricated library names

**Solutions:**

1. **Request verification:**
   ```
   After your suggestion, confirm: Does this API/method 
   actually exist? If you're not 100% sure, say so.
   ```

2. **Specify version:**
   ```
   Use only APIs available in React 18.2 (released Dec 2022).
   Don't suggest anything from newer versions.
   ```

3. **Ask for official documentation links:**
   ```
   Provide a link to the official documentation for 
   any API you mention.
   ```

### Issue: Lost Context in Long Conversations

**Solutions:**

1. **Restart with summary:**
   ```
   Let's reset. Here's our context:
   [Key requirements]
   [Decisions made]
   [Current problem]
   ```

2. **Use Custom Instructions (Settings):**
   - Set project context that persists across conversations

---

## Azure OpenAI

### Issue: Different Behavior from OpenAI

**Symptoms:**
- Same prompt works differently
- Content filtering triggers unexpectedly
- Response format differs

**Solutions:**

1. **Check content filter settings:**
   - Azure has different default filters than OpenAI
   - Adjust in Azure Portal if needed for your use case

2. **Use system message explicitly:**
   ```json
   {
     "messages": [
       {
         "role": "system",
         "content": "You are a helpful coding assistant..."
       }
     ]
   }
   ```

3. **Specify output format in system message:**
   ```
   Always respond in valid JSON format. Never include 
   markdown code fences in your response.
   ```

### Issue: Rate Limiting

**Solutions:**

1. **Implement exponential backoff:**
   ```python
   import time
   
   for attempt in range(5):
       try:
           response = call_azure_openai(prompt)
           break
       except RateLimitError:
           time.sleep(2 ** attempt)
   ```

2. **Check TPM/RPM limits in Azure Portal**

3. **Consider provisioned throughput for production**

---

## M365 Copilot

### Issue: Not Finding Relevant Documents

**Symptoms:**
- "I couldn't find information about..."
- Returns generic responses instead of organizational data
- Misses documents you know exist

**Solutions:**

1. **Reference documents explicitly:**
   ```
   Look at the "Q4 Sales Report.xlsx" in the Sales SharePoint 
   and summarize the regional performance.
   ```

2. **Check permissions:**
   - Copilot can only access documents you can access
   - Verify SharePoint/OneDrive permissions

3. **Use specific file/folder paths:**
   ```
   In my OneDrive folder "Project Plans/2024", find the 
   document about the API migration.
   ```

### Issue: Wrong Data Source

**Symptoms:**
- Pulling from wrong file with similar name
- Mixing data from multiple sources
- Outdated information

**Solutions:**

1. **Be specific about which file:**
   ```
   Use ONLY "Budget_2024_Final.xlsx" not any draft versions.
   ```

2. **Specify the location:**
   ```
   From the Marketing team SharePoint site, in the 
   "Campaigns" library...
   ```

3. **Verify data after generation:**
   ```
   After your response, list exactly which documents 
   you referenced.
   ```

---

## Quick Reference Table

| Platform | Common Issue | Quick Fix |
|----------|--------------|-----------|
| Copilot | Wrong style | Add comments with conventions |
| Copilot | Incomplete code | Write docstring first |
| Claude | Too cautious | "Be direct, I understand tradeoffs" |
| Claude | Cut off | Request chunked output |
| ChatGPT | Too verbose | Explicit length constraints |
| ChatGPT | Hallucinations | Request verification |
| Azure OpenAI | Content filtered | Check filter settings |
| M365 Copilot | Wrong file | Specify exact filename and location |

---

## Related Resources

- [Common Issues](/troubleshooting/common-issues) — Cross-platform problems
- [Prompt Debugging](/troubleshooting/prompt-debugging) — Systematic debugging
- [Platform Quickstarts](/get-started/) — Platform-specific basics
