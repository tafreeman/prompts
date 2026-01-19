---
title: "Contributing to Prompts Library"
shortTitle: "Contributing"
intro: "Guidelines for contributing new prompts and improvements to the library."
type: "how_to"
difficulty: "beginner"
audience:

  - "junior-engineer"
  - "senior-engineer"

platforms:

  - "github-copilot"
  - "claude"
  - "chatgpt"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "public"
reviewStatus: "approved"
---

# Contributing to Prompts Library

Thank you for your interest in contributing to the Prompts Library! This guide will help you get started.

## 🌟 How to Contribute

There are many ways to contribute:

- **Add new prompts** to expand the library
- **Improve existing prompts** with better wording or examples
- **Fix errors** or typos
- **Enhance documentation** to help others
- **Suggest new categories** or organizational improvements
- **Report issues** with existing prompts

## 🚀 Getting Started

1. **Fork the repository** to your GitHub account
2. **Clone your fork** to your local machine:

   ```bash
   git clone https://github.com/YOUR-USERNAME/prompts.git
   cd prompts
   ```

3. **Create a new branch** for your changes:

   ```bash
   git checkout -b add-new-prompt
   ```

4. **Make your changes** following the guidelines below
5. **Test your prompt** to ensure it works as expected
6. **Commit your changes** with a clear message:

   ```bash
   git add .
   git commit -m "Add: Code review assistant prompt for developers"
   ```

7. **Push to your fork**:

   ```bash
   git push origin add-new-prompt
   ```

8. **Create a Pull Request** from your fork to the main repository

## 📝 Adding a New Prompt

### Step 1: Choose the Right Category

Place your prompt in the appropriate directory:

- `prompts/developers/` - Technical and coding-related prompts
- `prompts/business/` - Business analysis and strategy prompts
- `prompts/creative/` - Content creation and marketing prompts
- `prompts/analysis/` - Data analysis and research prompts
- `prompts/system/` - System-level AI agent prompts

### Step 2: Use the Prompt Template

Copy the template from `templates/prompt-template.md` or use this structure:

```markdown
---
title: "Your Prompt Title"
category: "developers"
tags: ["tag1", "tag2", "tag3"]
author: "Your Name"
version: "1.0"
date: "2025-10-29"
difficulty: "beginner"
---

# Your Prompt Title

## Description
Clear, concise description of what this prompt does.

## Use Cases

- Specific use case 1
- Specific use case 2
- Specific use case 3

## Prompt

[Your actual prompt text. Be clear, specific, and include any necessary context.]

## Variables

- `[variable1]`: What the user should replace this with
- `[variable2]`: What the user should replace this with

## Example Usage

**Input:**
```text

Show a real example with actual values

```text

**Output:**
```text

Show the expected result

```text

## Tips

- Helpful tip for better results
- Customization suggestions

```sql

### Step 3: Follow Best Practices

**Good Prompt Characteristics:**

- ✅ Clear and specific
- ✅ Includes context and constraints
- ✅ Has well-defined variables
- ✅ Provides example usage
- ✅ Tested and validated
- ✅ Appropriate difficulty level

**Things to Avoid:**

- ❌ Vague or ambiguous language
- ❌ Missing examples
- ❌ Untested prompts
- ❌ Overly complex for the target audience
- ❌ Inappropriate or biased content

### Step 4: Choose a Template

We provide two templates to help you get started:

**Full Template** (`templates/prompt-template.md`)

- Comprehensive structure with all optional sections
- Best for complex prompts with multiple use cases
- Includes sections for governance, examples, tips, and more

**Minimal Template** (`templates/prompt-template-minimal.md`) ⭐ **Recommended for most prompts**

- Simplified structure focusing on essentials
- Quick to fill out - perfect for straightforward prompts
- Includes: Description, Prompt, Variables, Example Usage

**When to use which:**

- Use **minimal** for: Simple, focused prompts with clear purpose
- Use **full** for: Complex patterns, multi-step workflows, governance-sensitive content

### Step 5: Required Sections Checklist

Every prompt MUST include these sections:

- [ ] **Frontmatter** with `title` and `description` fields
- [ ] **Description** - 2-3 sentences explaining what this prompt does
- [ ] **Prompt** - The actual prompt text in a code block
- [ ] **Variables** - Table listing all `[variables]` with descriptions and examples
- [ ] **Example Usage** - Real example showing input and expected output

**Optional but recommended:**

- [ ] **Use Cases** - Specific scenarios where this prompt helps
- [ ] **Tips** - Advice for better results or customization
- [ ] **Related Prompts** - Links to similar or complementary prompts

### Step 6: Frontmatter Requirements

All prompts must include proper YAML frontmatter:

```yaml
---
title: "Your Prompt Title"
description: "One-line description"
category: "developers|business|creative|analysis|governance|m365|advanced|system"
difficulty: "beginner|intermediate|advanced"
author: "Your Name"
version: "1.0"
date: "YYYY-MM-DD"
---
```

**Required fields:**

- `title`: Clear, descriptive title
- `description`: One-line summary (shown in search results)
- `category`: Must be one of the standard categories
- `difficulty`: User skill level required

**Validation:**
Run `python tools/validate_prompts.py` to check your frontmatter before submitting.

### Step 7: Name Your File

Use descriptive, lowercase filenames with hyphens:

- ✅ `code-review-assistant.md`
- ✅ `marketing-email-generator.md`
- ✅ `data-visualization-helper.md`
- ❌ `prompt1.md`
- ❌ `MyPrompt.md`

## 🔄 Improving Existing Prompts

When improving an existing prompt:

1. **Update the version number**:
   - Minor improvements: 1.0 → 1.1
   - Major changes: 1.0 → 2.0

2. **Update the date** to the current date

3. **Add a changelog** at the bottom of the file:

   ```markdown
   ## Changelog

   ### Version 1.1 (2025-10-29)

   - Improved clarity in step 3
   - Added additional example

   ### Version 1.0 (2025-10-15)

   - Initial version

   ```

4. **Explain your changes** in the pull request description

## 🏷️ Tagging Guidelines

Use relevant, specific tags to help users find prompts:

**Category Tags:**

- `code-generation`, `debugging`, `testing`, `documentation`
- `analysis`, `strategy`, `reporting`, `planning`
- `content`, `copywriting`, `social-media`, `marketing`
- `data-analysis`, `research`, `visualization`, `insights`

**Technology Tags:**

- `python`, `javascript`, `java`, `typescript`, etc.
- `react`, `node`, `django`, `flask`, etc.

**Use Case Tags:**

- `beginner-friendly`, `team-collaboration`, `automation`
- `seo`, `email`, `presentation`, `documentation`

**Skill Level:**

- Always include one: `beginner`, `intermediate`, or `advanced`

## 📋 Pull Request Guidelines

When creating a pull request:

1. **Use a clear title**:
   - ✅ "Add: SQL query optimization prompt"
   - ✅ "Improve: Marketing email generator with more examples"
   - ✅ "Fix: Typo in data analysis prompt"

2. **Provide a detailed description**:
   - What does this prompt do?
   - Why is it useful?
   - Have you tested it?
   - Any special considerations?

3. **Complete the PR checklist**:
   - [ ] Frontmatter includes all required fields (`title`, `description`, `category`, `difficulty`)
   - [ ] All required sections present (Description, Prompt, Variables, Example)
   - [ ] Ran `python tools/validate_prompts.py` - no errors
   - [ ] Ran `python tools/check_links.py` - no broken links
   - [ ] Tested prompt with at least 2 real examples
   - [ ] File named using lowercase-with-hyphens.md format

4. **Link related issues** if applicable:

   ```markdown
   Closes #123
   Related to #456
   ```

5. **Request review** from maintainers or the community

## 🧪 Testing Your Prompts

Before submitting, please test your prompt:

1. **Try it yourself** with at least 2-3 different inputs
2. **Verify the output** matches expectations
3. **Check for edge cases** or unusual inputs
4. **Get feedback** from others if possible

### Testing Locally

Run these commands to validate your changes:

```bash
# Validate prompt structure and frontmatter
python tools/validate_prompts.py

# Check for broken internal links
python tools/check_links.py
```

Fix any issues reported by these tools before submitting your PR.

## 🎯 Difficulty Levels

Assign appropriate difficulty levels:

- **Beginner**: Simple, straightforward prompts with clear instructions. Minimal customization needed.
- **Intermediate**: Requires some understanding of the domain. May need customization for specific use cases.
- **Advanced**: Complex prompts requiring deep knowledge. Significant customization expected.

## ⚖️ Content Guidelines

All contributions must:

- ✅ Be original or properly attributed
- ✅ Respect intellectual property rights
- ✅ Be free from bias, discrimination, or harmful content
- ✅ Provide value to the community
- ✅ Follow professional and respectful language

We do **NOT** accept:

- ❌ Plagiarized content
- ❌ Harmful, malicious, or unethical prompts
- ❌ Spam or promotional content
- ❌ Prompts that violate privacy or security

## 📞 Questions or Help
- **Unsure about something?** Open an issue with your question
- **Need feedback?** Create a draft pull request and ask for input
- **Want to discuss ideas?** Use GitHub Discussions

## 🎖️ Recognition

Contributors are recognized in several ways:

- Listed as the author in prompt metadata
- Mentioned in release notes for significant contributions
- Special recognition for major contributors

Thank you for helping make this library better for everyone! 🙏

---

**Note**: By contributing, you agree that your contributions will be licensed under the same license as this project (MIT License).
