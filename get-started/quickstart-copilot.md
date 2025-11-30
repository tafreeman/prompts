---
title: Quickstart for GitHub Copilot
shortTitle: Copilot Quickstart
intro: Get productive with GitHub Copilot in 15 minutes. Learn the essential prompting
  patterns for code generation, testing, and documentation.
type: quickstart
difficulty: beginner
audience:
- junior-engineer
- senior-engineer
- senior-engineer
platforms:
- github-copilot
topics:
- code-generation
- quickstart
- copilot
author: Deloitte AI & Engineering
version: '1.0'
date: '2025-11-29'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
learningTrack: engineer-quickstart
---

# Quickstart for GitHub Copilot

Get productive with GitHub Copilot in 15 minutes. By the end of this quickstart, you'll be able to generate code, write tests, and create documentation using AI assistance.

## Prerequisites

- GitHub Copilot enabled in your IDE (VS Code, JetBrains, or Neovim)
- Basic programming knowledge in any language
- 15 minutes of focused time

## Step 1: Your First Code Generation (3 minutes)

Open a new file in your preferred language and try this pattern:

### Pattern: Comment-Driven Generation

```python
# Function to validate email address using regex
# Returns True if valid, False otherwise
# Handle edge cases: empty string, None, missing @ symbol
```

**What happens**: Copilot reads your comments and generates the function. The more specific your comments, the better the code.

### Try It Now

1. Create a new file (e.g., `utils.py`)
2. Type the comment above
3. Press `Enter` and wait for Copilot's suggestion
4. Press `Tab` to accept, or `Esc` to reject

**Pro Tip**: If the suggestion isn't right, press `Alt+]` (Windows) or `Option+]` (Mac) to see alternatives.

## Step 2: Generate Unit Tests (4 minutes)

Testing is where Copilot really shines. Use this pattern:

### Pattern: Test Generation from Function

```python
# Given this function:
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)

# Write comprehensive unit tests for calculate_discount
# Include edge cases: zero discount, 100% discount, negative values, invalid types
```

### Try It Now

1. Paste the function above into your file
2. Add the test comment
3. Watch Copilot generate test cases
4. Accept with `Tab`

**Expected Output**: Copilot will generate tests covering:
- Normal cases (10%, 50% discount)
- Edge cases (0%, 100% discount)
- Error cases (negative discount, >100%)

## Step 3: Explain and Document Code (4 minutes)

Use Copilot Chat for explanations and documentation.

### Pattern: Code Explanation

In Copilot Chat, type:

```
/explain what does this code do and what are the potential issues?
```

Then select any code block you want explained.

### Pattern: Generate Documentation

```python
# Generate docstring for this function following Google style:
def process_user_data(users: list[dict], filter_active: bool = True) -> dict:
    result = {}
    for user in users:
        if filter_active and not user.get('active'):
            continue
        result[user['id']] = {
            'name': user['name'],
            'email': user['email'],
            'last_login': user.get('last_login')
        }
    return result
```

### Try It Now

1. Select the function above
2. Open Copilot Chat (`Ctrl+I` or `Cmd+I`)
3. Type `/doc` to generate documentation
4. Review and accept

## Step 4: Refactor with Copilot Chat (4 minutes)

Use chat for refactoring suggestions.

### Pattern: Improve Code Quality

In Copilot Chat:

```
/fix improve error handling and add input validation
```

Or for specific improvements:

```
Refactor this code to:
1. Use early returns instead of nested ifs
2. Add type hints
3. Follow PEP 8 naming conventions
```

### Try It Now

1. Select code you want to improve
2. Open Copilot Chat
3. Describe the improvement you want
4. Review the suggestion and apply

## Quick Reference: Essential Shortcuts

| Action | Windows/Linux | Mac |
|--------|---------------|-----|
| Accept suggestion | `Tab` | `Tab` |
| Reject suggestion | `Esc` | `Esc` |
| Next suggestion | `Alt+]` | `Option+]` |
| Previous suggestion | `Alt+[` | `Option+[` |
| Open Copilot Chat | `Ctrl+I` | `Cmd+I` |
| Inline chat | `Ctrl+Shift+I` | `Cmd+Shift+I` |

## Quick Reference: High-Value Commands

| Command | Use For |
|---------|---------|
| `/explain` | Understand unfamiliar code |
| `/fix` | Fix bugs or improve code |
| `/doc` | Generate documentation |
| `/tests` | Generate unit tests |
| `/simplify` | Reduce complexity |

## What You Learned

In 15 minutes, you learned to:

- ✅ Generate code from comments
- ✅ Create comprehensive unit tests
- ✅ Document code with docstrings
- ✅ Refactor using Copilot Chat

## Next Steps

Now that you have the basics, explore these paths:

### Continue Learning (Recommended)

1. **[About Prompt Engineering](/concepts/about-prompt-engineering)** - Understand how to craft effective prompts
2. **[Code Review Assistant](/prompts/developers/code-review-assistant)** - AI-powered code reviews
3. **[Chain-of-Thought Prompting](/concepts/about-chain-of-thought)** - Advanced reasoning patterns

### By Your Role

| Role | Next Step |
|------|-----------|
| Junior Engineer | [Generating Unit Tests](/prompts/developers/test-automation-engineer) |
| Mid-Level Engineer | [Refactoring Assistant](/prompts/developers/csharp-refactoring-assistant) |
| Senior Engineer | [Chain-of-Thought: Detailed](/prompts/advanced/chain-of-thought-detailed) |

### Learning Track

Continue the **[Engineer Quick-Start Track](/learning-tracks/engineer-quickstart)** to become proficient in 1 week.

---

## Troubleshooting

### Copilot Not Suggesting

- Check you're in a supported file type
- Ensure Copilot is enabled (look for icon in status bar)
- Try adding more context in comments

### Suggestions Are Wrong

- Be more specific in your comments
- Add examples of expected input/output
- Use `Alt+]` to see alternative suggestions

### Need More Help?

- [Troubleshooting Code Generation](/troubleshooting/troubleshooting-code-generation)
- [Common Prompting Mistakes](/troubleshooting/common-prompting-mistakes)

---

**Time to complete**: ~15 minutes  
**Difficulty**: Beginner  
**Platform**: GitHub Copilot

*Part of the [Engineer Quick-Start Track](/learning-tracks/engineer-quickstart)*
