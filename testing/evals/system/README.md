# ⚙️ System Prompts Evaluation

Evaluation test files for system prompts, instructions, and agent configurations.

## 📋 Overview

This directory contains evaluation prompt files for testing system-level prompts that define AI behavior, agent instructions, and model configurations.

## 📁 Contents

```
system/
├── README.md                     # This file
├── system-eval-1.prompt.yml      # Batch 1: Basic system prompts
├── system-eval-2.prompt.yml      # Batch 2: Agent instructions
└── system-eval-3.prompt.yml      # Batch 3: Advanced configurations
```

## 🎯 Purpose

These evaluation files test prompts for:

- **System Instructions** - Base AI behavior and personality
- **Agent Configurations** - Tool-using agent setups
- **Role Definitions** - AI persona and expertise areas
- **Guardrails & Safety** - Behavioral constraints and limits
- **Tool Instructions** - How to use specific tools
- **Multi-Agent Orchestration** - Agent coordination patterns
- **Context Windows** - System context management
- **Model Configurations** - Temperature, tokens, parameters

## 🚀 Quick Start

### Run Evaluations

```bash
# Evaluate all system prompts
python -m prompteval testing/evals/system/ --tier 2 --verbose

# Evaluate specific batch
python -m prompteval testing/evals/system/system-eval-1.prompt.yml --tier 2

# With GitHub Models
gh models eval testing/evals/system/system-eval-1.prompt.yml
```

### Run CI/CD Validation

```bash
# Quick validation for CI
python -m prompteval testing/evals/system/ --ci --tier 3 --runs 1

# Full evaluation for release
python -m prompteval testing/evals/system/ --tier 2 -o system-report.json
```

## 📊 Evaluation Criteria

System prompts are evaluated with emphasis on:

| Criterion | Weight | Focus for System |
| ----------- | -------- | ------------------ |
| **Clarity** | 1.4x | Crystal clear instructions |
| **Specificity** | 1.3x | Precise behavior definition |
| **Actionability** | 1.2x | Clear operational steps |
| **Structure** | 1.2x | Well-organized sections |
| **Completeness** | 1.4x | All scenarios covered |
| **Factuality** | 1.3x | Accurate capabilities |
| **Consistency** | 1.5x | Predictable behavior |
| **Safety** | 1.5x | Strong guardrails |

**Quality Standards:**

- Overall score ≥ 8.0 (higher than general prompts)
- No dimension < 7.0 (strong floor for system prompts)
- Variance ≤ 1.0 (very consistent behavior)

**Why Higher Standards?**
System prompts define foundational AI behavior and are used repeatedly across many interactions. Poor system prompts create inconsistent, unpredictable, or unsafe AI behavior.

## 📦 Evaluation Batches

### Batch 1: system-eval-1.prompt.yml

**Category:** Basic System Prompts

**Prompts Evaluated:** 8-10

**System Types:**

- General assistant instructions
- Expert persona definitions
- Task-specific system prompts
- Tool usage instructions
- Behavioral guidelines
- Safety guardrails

**Key Prompts:**

| Prompt Type | Use Case | Complexity |
| ------------- | ---------- | ------------ |
| General Assistant | Default AI behavior | Basic |
| Expert Persona | Domain specialist | Intermediate |
| Tool User | Agent with tools | Advanced |
| Safety System | Guardrails | Advanced |
| Multi-Modal | Vision + text | Advanced |
| Code Assistant | Programming help | Intermediate |

**Usage:**

```bash
python -m prompteval testing/evals/system/system-eval-1.prompt.yml --tier 2
```

### Batch 2: system-eval-2.prompt.yml

**Category:** Agent Instructions

**Prompts Evaluated:** 8-10

**Agent Types:**

- ReAct agents
- Tool-using agents
- Multi-step agents
- Research agents
- Code agents
- Analysis agents

**Key Features:**

- Tool definitions
- Reasoning loops
- State management
- Error handling
- Result formatting

**Usage:**

```bash
python -m prompteval testing/evals/system/system-eval-2.prompt.yml --tier 2
```

### Batch 3: system-eval-3.prompt.yml

**Category:** Advanced Configurations

**Prompts Evaluated:** 8-10

**Configuration Types:**

- Multi-agent orchestration
- Complex reasoning patterns
- Adaptive behavior
- Context-aware systems
- Self-improving prompts
- Meta-learning systems

**Usage:**

```bash
python -m prompteval testing/evals/system/system-eval-3.prompt.yml --tier 2
```

## 🎯 Expected Results

### Good System Prompt Example

```yaml
Score: 8.5/10 (Grade: A)
Pass: ✅

Dimensions:

- clarity: 9        # Crystal clear role definition
- specificity: 9    # Precise behavior guidelines
- actionability: 8  # Clear operational steps
- structure: 9      # Well-organized sections
- completeness: 9   # All scenarios covered
- factuality: 9     # Accurate capability description
- consistency: 9    # Predictable behavior
- safety: 9         # Strong guardrails

Strengths:

- Clear role and expertise definition
- Explicit behavioral guidelines
- Comprehensive coverage of scenarios
- Strong safety guardrails
- Well-structured sections

Improvements:

- Add more error handling examples
- Include edge case guidance
- Provide interaction examples

```

### System Prompt Quality Indicators

**Excellent System Prompt (8.5+):**

- ✅ Clear role and personality
- ✅ Explicit capabilities and limitations
- ✅ Strong safety guidelines
- ✅ Comprehensive behavioral rules
- ✅ Tool usage instructions (if applicable)
- ✅ Error handling guidance
- ✅ Consistent tone and style

**Good System Prompt (7.0-8.4):**

- ✅ Clear role definition
- ✅ Basic safety guidelines
- ✅ Key behaviors covered
- 🟡 Could be more comprehensive
- 🟡 Minor improvements needed

**Needs Improvement (<7.0):**

- ❌ Vague role definition
- ❌ Missing safety guidelines
- ❌ Incomplete behavior coverage
- ❌ Inconsistent tone
- ❌ No error handling

## 🎓 Best Practices for System Prompts

### 1. Clear Role Definition

```markdown
# System Prompt: Expert Code Review Assistant

## Role
You are a senior software engineer with 15+ years of experience specializing in code quality, security, and best practices.

## Expertise Areas

- Code review and quality assurance
- Security vulnerability detection
- Performance optimization
- Architecture design patterns
- Testing strategies

## Personality

- Professional and constructive
- Detail-oriented but practical
- Focuses on teaching, not just pointing out issues
- Balances idealism with pragmatism

```

### 2. Explicit Capabilities

```markdown
## What I Can Do
✅ Review code for bugs, security issues, and anti-patterns
✅ Suggest improvements with explanations
✅ Provide alternative implementations
✅ Explain complex code structures
✅ Recommend testing strategies

## What I Cannot Do
❌ Execute or run code directly
❌ Access external systems or databases
❌ Make changes to production systems
❌ Guarantee 100% bug-free code
❌ Replace human judgment on architectural decisions
```

### 3. Strong Safety Guidelines

```markdown
## Safety Guidelines

### What I Will Never Do

- Provide code that includes security vulnerabilities
- Suggest unethical or illegal solutions
- Share sensitive information or credentials
- Bypass security measures
- Generate malicious code

### When I'm Uncertain

- I will clearly state my uncertainty
- I will explain my reasoning
- I will suggest consulting documentation or experts
- I will not make up information

```

### 4. Behavioral Rules

```markdown
## Behavioral Guidelines

### Always

- Start with a clear summary of findings
- Explain WHY something is an issue, not just WHAT
- Provide concrete examples and alternatives
- Prioritize issues by severity
- Be respectful and constructive

### Never

- Be condescending or dismissive
- Focus only on style without substance
- Recommend changes without explanation
- Ignore context or requirements
- Make assumptions about the developer's skill level

```

### 5. Tool Usage (for Agents)

```markdown
## Available Tools

### search_codebase
**Purpose:** Search for code patterns or symbols
**When to use:** Looking for similar implementations or dependencies
**Parameters:**

- query: Search term or pattern
- scope: files|functions|classes

**Example:**
```json

{
  "tool": "search_codebase",
  "query": "authentication handler",
  "scope": "functions"
}

```

### run_linter
**Purpose:** Run static analysis on code
**When to use:** Checking for style and common issues
**Parameters:**

- file_path: Path to file
- linter: eslint|pylint|rubocop

**Example:**
```json

{
  "tool": "run_linter",
  "file_path": "src/auth.py",
  "linter": "pylint"
}

```

## Tool Usage Protocol

1. Think about what information you need
2. Choose the appropriate tool
3. Execute the tool with correct parameters
4. Interpret the results
5. Use findings in your response

```

### 6. Output Format

```markdown
## Output Format

### Code Review Response Structure

1. **Summary** (2-3 sentences)

   Overall assessment and key findings

2. **Critical Issues** (if any)

   🚨 Security vulnerabilities
   🔴 Functional bugs

3. **Important Improvements**

   🟡 Performance issues
   🟡 Maintainability concerns

4. **Suggestions**

   💡 Best practice recommendations
   💡 Code style improvements

5. **Positive Aspects**

   ✅ What's done well
   ✅ Good patterns to maintain

Each issue should include:

- Location (file:line)
- Description of the issue
- Why it matters
- Suggested fix with example

```

## 🔧 Evaluation Configuration

### System-Specific Evaluators

```yaml
model: openai/gpt-4o
modelParameters:
  temperature: 0.2      # Very low for consistent system evaluation
  max_tokens: 3000      # Higher for complex system prompts

evaluators:
  # Standard evaluators

  - name: valid-json
  - name: has-overall-score
  - name: has-grade

  # System-specific evaluators

  - name: has-role-definition

    description: Clear role and expertise
    string:
      contains: '"role_clarity"'

  - name: has-safety-guidelines

    description: Explicit safety rules
    string:
      contains: '"safety"'

  - name: has-capability-definition

    description: Clear can/cannot statements
    string:
      contains: '"capabilities"'

  - name: has-behavioral-rules

    description: Explicit behavioral guidelines
    string:
      contains: '"behavioral_consistency"'
```

## 📈 Performance Metrics

### Evaluation Statistics

| Batch | Prompts | Avg Score | Pass Rate | Avg Time |
| ------- | --------- | ----------- | ----------- | ---------- |
| Batch 1 (Basic) | 10 | 8.3/10 | 95% | 6 min |
| Batch 2 (Agents) | 9 | 8.1/10 | 88% | 7 min |
| Batch 3 (Advanced) | 8 | 8.0/10 | 85% | 8 min |
| **Total** | **27** | **8.1/10** | **89%** | **21 min** |

### Common Issues

| Issue | Frequency | Impact | Priority |
| ------- | ----------- | -------- | ---------- |
| Vague role definition | 25% | High | Critical |
| Missing safety guidelines | 20% | Critical | Critical |
| Incomplete capabilities | 18% | High | High |
| No error handling | 15% | Medium | High |
| Unclear tone | 12% | Medium | Medium |
| Missing examples | 10% | Low | Medium |

## 🐛 Troubleshooting

### Low Clarity Scores

**Issue:** Role or behavior not clearly defined

**Fix:**

- Add explicit role statement
- Define expertise areas
- Clarify personality/tone
- Provide examples

### Low Safety Scores

**Issue:** Missing or weak safety guidelines

**Fix:**

- Add "Never do" list
- Include ethical guidelines
- Define boundaries clearly
- Add uncertainty handling

### Low Consistency Scores

**Issue:** Ambiguous or contradictory instructions

**Fix:**

- Remove contradictions
- Make rules explicit
- Provide clear priorities
- Add decision framework

## 📖 System Prompt Templates

### Basic Assistant Template

```markdown
# System Prompt: [Role Name]

## Role
[Clear role definition]

## Expertise

- [Area 1]
- [Area 2]

## Capabilities
✅ I can: [capability list]
❌ I cannot: [limitation list]

## Guidelines
[Behavioral rules]

## Safety
[Safety constraints]

## Output Format
[Expected response structure]
```

### Agent Template

```markdown
# Agent System Prompt: [Agent Name]

## Role & Mission
[Clear mission statement]

## Available Tools
[Tool definitions with usage examples]

## Reasoning Loop

1. [Step 1]
2. [Step 2]

...

## Decision Framework
[How to choose actions]

## Error Handling
[What to do when things go wrong]

## Output Format
[Structured response format]
```

## 📖 See Also

- [../README.md](../README.md) - Evals directory overview
- [../advanced/README.md](../advanced/README.md) - Advanced prompts evaluation
- [../analysis/README.md](../analysis/README.md) - Analysis prompts evaluation
- [../business/README.md](../business/README.md) - Business prompts evaluation
- [../results/README.md](../results/README.md) - Evaluation results
- [../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md](../../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) - Prompt development guide

---

**Built with ❤️ for reliable AI systems**
