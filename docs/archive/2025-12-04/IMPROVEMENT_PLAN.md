# Prompt Improvement Plan

> Based on evaluation results from December 2, 2025
> **Status: ✅ COMPLETED - All prompts improved on December 2, 2025**

## Reference Guide

**Primary Reference:** [Comprehensive Prompt Development Guide](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md)

This improvement plan follows the standards and patterns defined in the Comprehensive Prompt Development Guide, including:
- **The Seven Components**: Context, Role, Task, Format, Constraints, Examples, Tone
- **Quality Evaluation Criteria**: 8 dimensions (Clarity, Specificity, Actionability, Structure, Completeness, Factuality, Consistency, Safety)
- **Pass/Fail Thresholds**: ≥7.0 overall, no criterion below 5.0
- **Industry Best Practices**: OpenAI, Anthropic, Google Gemini, Microsoft patterns

---

## Executive Summary

- **24 prompts evaluated**, 23 passed (96% pass rate)
- **Weakest criterion:** Specificity (7.4/10 average)
- **Strongest criteria:** Safety (9.1/10), Factuality (8.9/10), Structure (8.7/10)
- **1 failed prompt:** Code Review Expert: Structured Output (specificity: 5, completeness: 5)
- **7 prompts need enhancement** (passed but scored < 8.0)

### Implementation Status (December 2, 2025)

| Priority | Prompts | Status |
| :--- |---------| :--- |
| **P1 (Failed)** | 1 prompt | ✅ Fixed |
| **P2 (7.0-7.9)** | 7 prompts | ✅ Enhanced |
| **P3 (8.0-8.4)** | 4 prompts | ✅ Minor improvements |

---

## Pattern Analysis: What Makes High-Scoring Prompts Succeed

Analyzing top performers (8.5+ scores), the following patterns emerge:

### ✅ High-Scoring Prompt Patterns

These patterns align with the [Seven Components](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#the-seven-components-of-effective-prompts) from our guide:

| Pattern | Guide Component | Example from Top Prompts |
| :--- |-----------------| :--- |
| **Explicit persona with approach** | **Role** | "You are a **Senior Database Security Engineer**. Your Approach: Zero Trust, Defense in Depth..." |
| **Numbered standards/principles** | **Constraints** | "1. General Security Principles... 2. Injection Prevention... 3. Least Privilege..." |
| **Structured output format** | **Format** | "Use this structure: 1. Summary (≤ 3 sentences) 2. Standards-Linked Actions (bullet list)..." |
| **Concrete examples** | **Examples (Few-Shot)** | Full input/output examples with real code |
| **Variable definitions** | **Context** | Clear `[variable]` placeholders with descriptions |
| **Tips section** | **Tone/Usability** | Actionable guidance for best results |
| **Related prompts** | **Completeness** | Cross-references to complementary prompts |

### ❌ Low-Scoring Prompt Anti-Patterns

These anti-patterns violate principles from the [Common Mistakes and Fixes](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#common-mistakes-and-fixes) section:

| Anti-Pattern | Violated Principle | Impact |
| :--- |-------------------| :--- |
| Vague placeholders without examples | "Missing Examples" anti-pattern | Reduces specificity |
| Missing output format specification | "Ignoring Output Format" anti-pattern | Reduces consistency |
| No concrete examples | "Expecting AI to guess output style" | Reduces actionability |
| Generic "Include:" lists | Insufficient **Constraints** component | Reduces completeness |
| Missing edge case guidance | Incomplete **Context** component | Reduces reliability |

---

## Improvement Plan by Priority

### 🔴 Priority 1: Failed Prompt (Immediate Fix) ✅ COMPLETED

#### Code Review Expert: Structured Output (6.5/10 → Fixed)
**Issues:** Specificity (5), Completeness (5)

**Changes Applied:**
- ✅ Added severity classification tables with explicit criteria
- ✅ Added decision tree for APPROVE vs REQUEST_CHANGES
- ✅ Added example issue classifications for security, performance, bugs
- ✅ Enhanced Variables section with description/example table
- ✅ Added comprehensive Tips with severity thresholds

**Root Cause Analysis:**
- Has good structure but lacks concrete review criteria
- Output schema is defined but no guidance on *what to look for*
- Missing examples of issue categorization logic

**Recommended Changes** (using [RTF Pattern](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#pattern-1-rtf-role-task-format)):
1. Add explicit review criteria checklist (what constitutes Critical vs Major)
2. Add examples of each issue category (security, performance, bug)
3. Add guidance on when to APPROVE vs REQUEST_CHANGES
4. Add example of a complete review for different languages
5. Strengthen the **Role** component with specific expertise areas
6. Add **Constraints** for issue severity classification

---

### 🟡 Priority 2: Prompts Needing Enhancement (7.0-7.9 range) ✅ COMPLETED

> **Improvement Strategy:** Apply the [Seven Components](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#the-seven-components-of-effective-prompts) framework to each prompt, focusing on missing or weak components.

#### 1. Data Pipeline Engineer (7.25/10) ✅ IMPROVED
**Issues:** Specificity (6), Completeness (7)
**Missing Components:** Examples, Constraints

**Changes Applied:**
- ✅ Added expert persona with specializations (Spark, Airflow, Kafka)
- ✅ Enhanced prompt with architecture patterns and tool selection guidance
- ✅ Added comprehensive Variables table with descriptions and examples
- ✅ Added data quality framework and monitoring alert examples
- ✅ Added Tips section with batch vs streaming decision guide

#### 2. Code Review Assistant (7.3/10) ✅ IMPROVED
**Issues:** Specificity (6), Completeness (6)
**Missing Components:** Constraints, Examples, Format

**Changes Applied:**
- ✅ Added Role component with expertise areas
- ✅ Added Variables table with descriptions and examples
- ✅ Added experience-level customization tips (beginner/intermediate/advanced)
- ✅ Updated frontmatter with platforms and review status

#### 3. Code Review Expert (7.5/10) ✅ IMPROVED
**Issues:** Specificity (6), Completeness (7)
**Missing Components:** Examples, Format

**Changes Applied:**
- ✅ Added Variables table with descriptions and examples
- ✅ Updated frontmatter with additional platforms

#### 4. Documentation Generator (7.5/10) ✅ IMPROVED
**Issues:** Specificity (6), Completeness (7)
**Missing Components:** Examples, Format templates

**Changes Applied:**
- ✅ Added expert persona (Senior Technical Writer, 10+ years)
- ✅ Added Diátaxis framework (Tutorials, How-tos, Reference, Explanation)
- ✅ Enhanced prompt with structured documentation deliverables
- ✅ Added comprehensive Variables table
- ✅ Added audience adaptation tips with customization guidance
- ✅ Added Diátaxis framework visual reference

#### 5. Frontend Architecture Consultant (7.5/10) ✅ IMPROVED
**Issues:** Specificity (6), Completeness (7)
**Missing Components:** Examples, Constraints

**Changes Applied:**
- ✅ Added Principal Frontend Architect persona (12+ years)
- ✅ Added framework selection guide table
- ✅ Added performance budget reference table (LCP, FID, CLS)
- ✅ Added Atomic Design architecture pattern diagram
- ✅ Added state management decision tree
- ✅ Added common pitfalls to avoid section

#### 6. Microservices Architect (7.75/10) ✅ IMPROVED
**Issues:** Clarity (7), Actionability (7)
**Missing Components:** Examples, clearer Task

**Changes Applied:**
- ✅ Converted Variables to table format with examples
- ✅ Added service count decision guide by team size
- ✅ Added common decomposition mistakes table
- ✅ Added ADR template quick reference
- ✅ Added input quality checklist
- ✅ Updated frontmatter with additional topics

#### 7. Mobile App Developer (7.875/10) ✅ IMPROVED
**Issues:** Specificity (7), Completeness (7)
**Missing Components:** Platform-specific Examples

**Changes Applied:**
- ✅ Added Senior Mobile Engineer persona (10+ years)
- ✅ Added platform selection guide (Native vs React Native vs Flutter)
- ✅ Added iOS-specific and Android-specific tips
- ✅ Added performance benchmarks table
- ✅ Added App Store review pitfalls section
- ✅ Added testing device matrix template

---

### 🟢 Priority 3: Enhancements for B-Grade Prompts (8.0-8.4 range) ✅ COMPLETED

These prompts pass well but could be elevated to A-grade using [Advanced Techniques](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#advanced-techniques):

| Prompt | Score | Enhancement Applied | Status |
| :--- |-------| :--- |--------|
| API Design Consultant | 8.4 | Variables table, updated frontmatter | ✅ |
| Cloud Migration Specialist | 8.0 | Variables table, updated frontmatter, added platforms | ✅ |
| C# Refactoring Assistant | 8.0 | Role persona, Variables table, updated frontmatter | ✅ |
| DevOps Pipeline Architect | 8.0 | Variables table, updated frontmatter | ✅ |

---

## Implementation Templates

> **Note:** These templates implement patterns from the [Comprehensive Prompt Development Guide](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#templates-and-checklists).

### Template: Adding Specificity

Per the guide's [Examples (Few-Shot)](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#6-examples-few-shot-learning) component:

For each variable, add:
```markdown
## Variables

- `[variable_name]`: Description of what to provide

### Example Values

| Variable | Example 1 | Example 2 |
| :--- |-----------| :--- |
| `[variable_name]` | Concrete example | Another example |
```

### Template: Adding Completeness

Per the guide's [Format](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#4-format) component:

Add explicit output structure:
```markdown
## Expected Output Structure

Your response should include:

### 1. Section Name
- What to include
- How detailed
- Example snippet

### 2. Another Section
...
```

### Template: Adding Review Criteria

Per the guide's [Constraints](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#5-constraints) component:

For code review prompts:
```markdown
## Review Criteria

### Critical Issues (Must Fix)
- Security vulnerabilities (injection, XSS, auth bypass)
- Data loss or corruption risks
- Breaking changes to public APIs

### Major Issues (Should Fix)
- Performance issues affecting users
- Missing error handling
- Logic bugs

### Minor Issues (Consider Fixing)
- Code style violations
- Missing documentation
- Non-idiomatic patterns
```

### Template: Adding Role/Persona

Per the guide's [Role (Persona)](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#2-role-persona) component:

```markdown
You are a [SPECIFIC_ROLE] with expertise in [DOMAIN].

**Your Approach:**
- [Principle 1]
- [Principle 2]
- [Principle 3]

**Your Focus Areas:**
1. [Priority area]
2. [Secondary area]
```

### Template: Adding Chain-of-Thought

Per the guide's [Advanced Techniques](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#advanced-techniques) section:

```markdown
## Reasoning Process

Before providing your final output, think through:

**Step 1: Understanding**
- Restate the problem
- Identify key constraints

**Step 2: Analysis**
- Break down the problem
- Consider alternatives

**Step 3: Solution**
- Propose approach
- Justify reasoning
```

---

## Implementation Order

### Week 1: Critical Fixes
1. [ ] Fix Code Review Expert: Structured Output (failed)
2. [ ] Enhance Data Pipeline Engineer
3. [ ] Enhance Code Review Assistant

### Week 2: Enhancement Batch 1
4. [ ] Enhance Code Review Expert
5. [ ] Enhance Documentation Generator
6. [ ] Enhance Frontend Architecture Consultant

### Week 3: Enhancement Batch 2
7. [ ] Enhance Microservices Architect
8. [ ] Enhance Mobile App Developer
9. [ ] Review and enhance B-grade prompts

### Week 4: Validation
10. [ ] Re-run evaluations on all modified prompts
11. [ ] Generate comparison report
12. [ ] Document lessons learned

---

## Success Criteria

After implementing improvements:

| Metric | Current | Target |
| :--- |---------| :--- |
| Pass Rate | 96% (23/24) | 100% (24/24) |
| Average Score | 8.0/10 | 8.5/10 |
| Specificity Average | 7.4/10 | 8.0/10 |
| Prompts with A Grade | 3 | 8+ |
| Prompts < 8.0 | 8 | 0 |

---

## Tracking

### Progress Dashboard

| Prompt | Original | Target | Current | Status |
| :--- |----------| :--- |---------| :--- |
| Code Review Expert: Structured Output | 6.5 | 8.0 | :--- | 🔴 Not Started |
| Data Pipeline Engineer | 7.25 | 8.0 | :--- | 🔴 Not Started |
| Code Review Assistant | 7.3 | 8.0 | :--- | 🔴 Not Started |
| Code Review Expert | 7.5 | 8.0 | :--- | 🔴 Not Started |
| Documentation Generator | 7.5 | 8.0 | :--- | 🔴 Not Started |
| Frontend Architecture Consultant | 7.5 | 8.0 | :--- | 🔴 Not Started |
| Microservices Architect | 7.75 | 8.0 | :--- | 🔴 Not Started |
| Mobile App Developer | 7.875 | 8.0 | :--- | 🔴 Not Started |

---

## Next Steps

1. **Review this plan** - Get team approval on priorities
2. **Consult the guide** - Reference [Comprehensive Prompt Development Guide](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md) for each improvement
3. **Start with Priority 1** - Fix the failed prompt immediately
4. **Batch improvements** - Work through Priority 2 systematically
5. **Re-evaluate** - Run evals after each batch to measure progress
6. **Iterate** - Use findings to improve evaluation criteria and prompt templates

---

## Quick Reference: Guide Sections for Common Issues

| Issue | Guide Section to Reference |
| :--- |---------------------------|
| Low Specificity | [Examples (Few-Shot)](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#6-examples-few-shot-learning) |
| Low Completeness | [Format](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#4-format) + [Constraints](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#5-constraints) |
| Low Clarity | [Task](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#3-task) |
| Low Actionability | [Chain-of-Thought](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#chain-of-thought-cot-prompting) |
| Low Consistency | [Platform Guidelines](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#platform-specific-guidelines) |
| Need Structure | [Prompt Structure Patterns](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#prompt-structure-patterns) |
| Anti-patterns | [Common Mistakes and Fixes](../../docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md#common-mistakes-and-fixes) |

---

## Additional Resources

- [Standard Prompt Template](../../templates/prompt-template.md)
- [Prompt Improvement Template](../../templates/prompt-improvement-template.md)
- [Reference Cheat Sheet](../../reference/cheat-sheet.md)
- [Prompt Anatomy](../../concepts/prompt-anatomy.md)
- [Best Practices](../../docs/best-practices.md)
