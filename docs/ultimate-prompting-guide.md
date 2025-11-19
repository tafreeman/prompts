# The Ultimate AI Prompting Guide

**A Curated Collection of the Most Effective Prompts from Industry Leaders and Research**

Version 1.0 | Last Updated: 2025-11-19

---

## Table of Contents

1. [Introduction](#introduction)
2. [Scoring Methodology](#scoring-methodology)
3. [Platform-Specific Guidelines](#platform-specific-guidelines)
   - [GitHub Copilot](#github-copilot)
   - [Microsoft 365 Copilot](#microsoft-365-copilot)
   - [Windows Copilot](#windows-copilot)
   - [Claude Sonnet 4.5 / GPT-4/5](#claude-and-gpt)
4. [Top 20% Curated Prompts](#top-20-curated-prompts)
5. [Prompt Patterns & Templates](#prompt-patterns--templates)
6. [Best Practices Summary](#best-practices-summary)
7. [Quick Reference](#quick-reference)

---

## Introduction

This guide represents the synthesis of:
- **Academic research** from NeurIPS, ICLR, and arXiv papers on prompt effectiveness
- **Industry best practices** from Anthropic, OpenAI, Microsoft, and GitHub
- **Empirical analysis** of 95+ prompts across 7 categories
- **Community insights** from top prompt libraries (awesome-chatgpt-prompts, LangChain, etc.)

### What Makes a Prompt Effective?

Through research and analysis, we've identified that effective prompts score highly across five dimensions:

1. **Clarity & Specificity** (20 points): Clear goals, specific instructions, defined success criteria
2. **Structure & Completeness** (20 points): All necessary sections, examples, documentation
3. **Usefulness & Reusability** (20 points): Solves common problems, adaptable to variations
4. **Technical Quality** (20 points): Proper reasoning style, structured output, best practices
5. **Ease of Use** (20 points): Simple to customize, minimal prerequisites, helpful tips

**Top 20% Selection**: Only prompts scoring 75+ out of 100 points and matching patterns found in 3+ top libraries are included.

---

## Scoring Methodology

### Academic Foundation

Our methodology is based on:

- **Wei et al. (NeurIPS 2022)**: Chain-of-Thought prompting improves reasoning by 20-40%
- **Yao et al. (NeurIPS 2023)**: Tree-of-Thoughts enables deliberate problem-solving
- **The Prompt Report (arXiv:2406.06608)**: Comprehensive taxonomy of prompting techniques
- **Springer 2024**: Framework combining objective/subjective metrics

### Industry Standards

- **Anthropic**: Clear/direct instructions, multishot examples, Chain-of-Thought, XML structure
- **OpenAI**: Structured outputs, delimiters, few-shot learning, explicit constraints
- **Microsoft 365**: Context-Action-Result-Example (CARE) pattern
- **GitHub Copilot**: The Four S's (Single, Specific, Short, Surround)

### Results from Our Analysis

From 95 prompts analyzed:
- **11 prompts** achieved Tier 1 (Exceptional): 85-100 points
- **14 prompts** achieved Tier 2 (Strong): 70-84 points
- **Top 20% (19 prompts)** represent the best-in-class examples

**See full methodology**: [docs/prompt-effectiveness-scoring-methodology.md](./prompt-effectiveness-scoring-methodology.md)

---

## Platform-Specific Guidelines

### GitHub Copilot

**The Four S's Framework**:
1. **Single**: One task per prompt
2. **Specific**: Detailed, explicit instructions
3. **Short**: Concise but information-rich
4. **Surround**: Use context from open files

#### Quick Start Templates

**Function Implementation**:
```python
# Write a Python function that merges two sorted lists into a single sorted list.
# Input: Two sorted lists of integers
# Output: A single sorted list containing all elements
# Handle edge cases: empty lists, single-element lists
def merge_sorted_lists(list1, list2):
    # Implementation here
```

**Test Generation**:
```python
# Write comprehensive unit tests for the following function using pytest.
# Include tests for: normal cases, edge cases, invalid inputs, boundary conditions
def is_prime(n):
    # function code
```

**Code Review**:
```javascript
// Review the following code for:
// 1. Security vulnerabilities
// 2. Performance bottlenecks  
// 3. Code style and best practices
// 4. Edge case handling
function processUserData(data) {
    // implementation
}
```

**Refactoring**:
```typescript
// Refactor this code to:
// 1. Improve readability using descriptive names
// 2. Extract complex logic into separate functions
// 3. Add TypeScript types
// 4. Handle errors gracefully
function calc(d) {
    // legacy code
}
```

#### Best Practices
- Use comments above code to provide context
- Open related files for better suggestions
- Break complex tasks into steps
- Specify language version and libraries
- Include example inputs/outputs

---

### Microsoft 365 Copilot

**CARE Framework**: Context → Action → Result → Example

#### App-Specific Templates

**Word - Document Summarization**:
```
Summarize this document in 3 paragraphs:
1. Main topic and purpose
2. Key findings or arguments (3-5 bullet points)
3. Conclusions and recommendations

Format: Professional business style, executive audience
```

**Excel - Data Analysis**:
```
Analyze this sales data and provide:
1. Top 5 products by revenue
2. Month-over-month growth trends
3. Underperforming categories (below 10% growth)
4. Visual recommendation: What chart type would best show this?

Create a summary table with these insights.
```

**PowerPoint - Presentation Creation**:
```
Create a 10-slide presentation about [TOPIC] for [AUDIENCE]:
- Slide 1: Title slide with compelling tagline
- Slides 2-3: Problem statement with statistics
- Slides 4-7: Solution overview (one concept per slide)
- Slide 8: Timeline and milestones
- Slide 9: Team and resources
- Slide 10: Call to action

Style: Modern, professional, use icons and minimal text
```

**Outlook - Email Drafting**:
```
Draft a professional email to [RECIPIENT] about [TOPIC]:
- Tone: Friendly but formal
- Length: 3 short paragraphs maximum
- Purpose: Request meeting to discuss Q4 strategy
- Include: Available time slots next week
- Call-to-action: Clear next step
```

**Teams - Meeting Summarization**:
```
Summarize the last team meeting:
1. Main topics discussed (bullet points)
2. Decisions made
3. Action items with owners and due dates
4. Open questions or unresolved issues

Format as a meeting notes document for distribution.
```

#### Best Practices
- Always specify the audience and tone
- Provide context from connected documents
- Ask for specific output formats
- Use natural, conversational language
- Iterate and refine with follow-up prompts

---

### Windows Copilot

**Template Structure**: Task + Context + Format + Tone

#### Quick Action Templates

**File Management**:
```
Find all Excel files modified in the last 7 days in [FOLDER_PATH] that contain the word "budget" and create a summary list showing:
- File name
- Last modified date
- File size

Sort by most recent first.
```

**System Analysis**:
```
Analyze my system performance:
1. Show CPU and memory usage over last hour
2. Identify top 5 resource-consuming applications
3. Recommend optimization actions if usage > 80%

Display as a simple dashboard with status indicators.
```

**Quick Setup**:
```
Help me set up a productive workspace:
1. Open VS Code
2. Open Chrome with tabs: GitHub, StackOverflow, Documentation
3. Start Spotify with focus playlist
4. Set do-not-disturb mode for 2 hours
```

#### Best Practices
- Be specific about what you want done
- Specify output format preferences
- Use for quick system tasks and queries
- Combine multiple related actions in one prompt

---

### Claude and GPT

**Advanced Prompting Techniques**

#### Chain-of-Thought (CoT)
```
You are an expert problem solver. Analyze [PROBLEM] step by step.

**Task**: [SPECIFIC_TASK]
**Context**: [RELEVANT_BACKGROUND]
**Constraints**: [LIMITATIONS]

Think through this systematically:

**Step 1: Understanding**
- Restate the problem
- Identify key challenges

**Step 2: Analysis**
- Break down the problem
- Consider alternatives

**Step 3: Solution**
- Propose approach
- Justify your reasoning

**Step 4: Implementation**
- Outline concrete steps
- Note potential risks

Format output as structured markdown with clear sections.
```

#### Tree-of-Thoughts (ToT)
```
Evaluate multiple solution approaches for [PROBLEM].

**Branch A: Conservative Approach**
- Description: [APPROACH_1]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Branch B: Balanced Approach**
- Description: [APPROACH_2]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Branch C: Innovative Approach**
- Description: [APPROACH_3]
- Pros: [BENEFITS]
- Cons: [DRAWBACKS]
- Score: [1-10]

**Recommendation**: Based on scores and trade-offs, select the best approach and explain why.
```

#### ReAct (Reasoning + Acting)
```
Use the ReAct pattern to solve [TASK] with available tools.

**Think**: What information do I need? What tools can help?
**Act**: [USE_TOOL] with [PARAMETERS]
**Observe**: [RESULT_FROM_TOOL]
**Reflect**: Did this get me closer to the goal? What's next?

Repeat until task is complete.

**Available Tools**:
- [TOOL_1]: [DESCRIPTION]
- [TOOL_2]: [DESCRIPTION]

Output format: Show each Think-Act-Observe-Reflect cycle clearly.
```

#### Structured JSON Output
```
Extract information from [SOURCE] and return as JSON:

{
  "summary": "Brief 1-2 sentence summary",
  "key_points": ["point1", "point2", "point3"],
  "entities": {
    "people": ["name1", "name2"],
    "organizations": ["org1", "org2"],
    "locations": ["loc1", "loc2"]
  },
  "dates": ["date1", "date2"],
  "action_items": [
    {"task": "description", "owner": "person", "due": "date"}
  ],
  "confidence": 0.95
}

Ensure all fields are present even if empty. Use null for missing data.
```

#### Best Practices
- Use XML tags for complex structure
- Assign roles/personas for expertise
- Request step-by-step reasoning for complex tasks
- Specify exact output format (JSON schema, markdown, etc.)
- Break long tasks into chained prompts

---

## Top 20% Curated Prompts

Based on our scoring methodology, these 19 prompts represent the top 20% most effective prompts across all categories.

### 🏆 Tier 1: Exceptional (85-100 points)

#### 1. Chain-of-Thought: Debugging & Root Cause Analysis (95/100)
**Category**: Advanced Techniques | **Difficulty**: Intermediate

**Why It's Excellent**:
- Perfect clarity with explicit reasoning requirements
- Comprehensive structure with all necessary sections
- Highly reusable across debugging scenarios
- Uses proven CoT technique with structured output

**Use Cases**:
- Production bug investigation
- Complex system failures
- Performance degradation analysis
- Multi-component issue diagnosis

**Location**: [prompts/advanced/chain-of-thought-debugging.md](../prompts/advanced/chain-of-thought-debugging.md)

---

#### 2. Chain-of-Thought: Performance Analysis & Profiling (94/100)
**Category**: Advanced Techniques | **Difficulty**: Intermediate

**Why It's Excellent**:
- Specialized for performance engineering workflows
- Data-driven with profiling tool integration
- Research-backed (Wei et al. + Gregg's "Systems Performance")
- Systematic bottleneck identification

**Use Cases**:
- CPU/memory profiling analysis
- Database query optimization
- Network latency troubleshooting
- Scalability issue resolution

**Location**: [prompts/advanced/chain-of-thought-performance-analysis.md](../prompts/advanced/chain-of-thought-performance-analysis.md)

---

#### 3. Tree-of-Thoughts: Architecture Evaluator (94/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Why It's Excellent**:
- Multi-branch evaluation for complex decisions
- Comprehensive trade-off analysis
- Research-backed (Yao et al. NeurIPS 2023)
- Structured comparison framework

**Use Cases**:
- Technology stack selection
- Architecture pattern comparison
- Design decision evaluation
- Strategic technical planning

**Location**: [prompts/advanced/tree-of-thoughts-architecture-evaluator.md](../prompts/advanced/tree-of-thoughts-architecture-evaluator.md)

---

#### 4. Refactoring Plan Designer (93/100)
**Category**: Developers | **Difficulty**: Intermediate

**Why It's Excellent**:
- Systematic approach to code improvement
- Clear before/after comparison
- Risk assessment included
- Actionable step-by-step plans

**Use Cases**:
- Legacy code modernization
- Technical debt reduction
- Code quality improvement
- Design pattern introduction

**Location**: [prompts/developers/refactoring-plan-designer.md](../prompts/developers/refactoring-plan-designer.md)

---

#### 5. Data Quality Assessment (91/100)
**Category**: Analysis | **Difficulty**: Intermediate

**Why It's Excellent**:
- Comprehensive data quality framework
- Multiple quality dimensions covered
- Actionable remediation recommendations
- Industry-standard metrics

**Use Cases**:
- Data pipeline validation
- ETL quality checks
- Dataset fitness assessment
- Data governance compliance

**Location**: [prompts/analysis/data-quality-assessment.md](../prompts/analysis/data-quality-assessment.md)

---

#### 6. Chain-of-Thought: Detailed Mode (90/100)
**Category**: Advanced Techniques | **Difficulty**: Intermediate

**Why It's Excellent**:
- Thorough reasoning with detailed explanations
- Explicit alternative consideration
- Teaching-oriented approach
- Compliance documentation support

**Use Cases**:
- Critical business decisions
- Teaching and mentoring contexts
- High-stakes architectural decisions
- Regulatory compliance scenarios

**Location**: [prompts/advanced/chain-of-thought-detailed.md](../prompts/advanced/chain-of-thought-detailed.md)

---

#### 7. ReAct: Tool-Augmented Reasoning (90/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Why It's Excellent**:
- Research-backed (Yao et al., Shinn et al.)
- Transparent reasoning + action loop
- Tool integration framework
- Auditable decision process

**Use Cases**:
- Research with multiple sources
- API workflow automation
- Multi-step troubleshooting
- RAG pattern implementation

**Location**: [prompts/advanced/react-tool-augmented.md](../prompts/advanced/react-tool-augmented.md)

---

#### 8. Tree-of-Thoughts: Multi-Branch Reasoning Template (90/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Why It's Excellent**:
- Explores multiple solution paths
- Systematic branch evaluation
- Backtracking capability
- Trade-off analysis framework

**Use Cases**:
- Strategic planning decisions
- Complex problem-solving
- Creative exploration tasks
- Optimization with multiple local maxima

**Location**: [prompts/advanced/tree-of-thoughts-template.md](../prompts/advanced/tree-of-thoughts-template.md)

---

#### 9. Tree-of-Thoughts Evaluator: Reflection & Self-Critique (89/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Why It's Excellent**:
- Meta-evaluation framework
- Self-improvement loop
- Quality assurance built-in
- Iterative refinement support

**Use Cases**:
- Repository evaluation
- Solution quality assessment
- Design review frameworks
- Continuous improvement processes

**Location**: [prompts/advanced/tree-of-thoughts-evaluator-reflection.md](../prompts/advanced/tree-of-thoughts-evaluator-reflection.md)

---

#### 10. Code Review Expert: Structured Output (87/100)
**Category**: Developers | **Difficulty**: Intermediate

**Why It's Excellent**:
- Structured JSON output format
- Multiple review dimensions
- Actionable feedback
- Automation-friendly

**Use Cases**:
- Automated code review
- PR quality gates
- Security vulnerability scanning
- Best practices enforcement

**Location**: [prompts/developers/code-review-expert-structured.md](../prompts/developers/code-review-expert-structured.md)

---

#### 11. RAG: Document Retrieval and Citation (86/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Why It's Excellent**:
- Proper citation framework
- Multi-document synthesis
- Source verification support
- Hallucination prevention

**Use Cases**:
- Research report generation
- Legal document analysis
- Knowledge base querying
- Compliance documentation

**Location**: [prompts/advanced/rag-document-retrieval.md](../prompts/advanced/rag-document-retrieval.md)

---

### 🥈 Tier 2: Strong (70-84 points)

#### 12. Tree-of-Thoughts Repository Evaluator for GPT-5.1 (83/100)
**Category**: System | **Difficulty**: Advanced

**Use Cases**: Repository quality assessment, competitive analysis
**Location**: [prompts/system/tree-of-thoughts-repository-evaluator.md](../prompts/system/tree-of-thoughts-repository-evaluator.md)

---

#### 13. Chain-of-Thought: Concise Mode (83/100)
**Category**: Advanced Techniques | **Difficulty**: Intermediate

**Use Cases**: Quick analysis, fast decision-making, brief reports
**Location**: [prompts/advanced/chain-of-thought-concise.md](../prompts/advanced/chain-of-thought-concise.md)

---

#### 14. Reflection: Initial Answer + Self-Critique (83/100)
**Category**: Advanced Techniques | **Difficulty**: Advanced

**Use Cases**: Quality improvement, self-correction, iterative refinement
**Location**: [prompts/advanced/reflection-self-critique.md](../prompts/advanced/reflection-self-critique.md)

---

#### 15. Code Review Assistant (79/100)
**Category**: Developers | **Difficulty**: Beginner

**Use Cases**: Beginner-friendly code review, learning best practices
**Location**: [prompts/developers/code-review-assistant.md](../prompts/developers/code-review-assistant.md)

---

#### 16. Security: Incident Response Framework (79/100)
**Category**: Governance & Compliance | **Difficulty**: Advanced

**Use Cases**: Security incidents, breach response, forensic analysis
**Location**: [prompts/governance/security-incident-response.md](../prompts/governance/security-incident-response.md)

---

#### 17. Legal: Contract Review Assistant (78/100)
**Category**: Governance & Compliance | **Difficulty**: Advanced

**Use Cases**: Contract analysis, legal risk assessment, clause review
**Location**: [prompts/governance/legal-contract-review.md](../prompts/governance/legal-contract-review.md)

---

#### 18-19. Additional Tier 2 Prompts
- **Code Generation Assistant** (77/100): [Link](../prompts/developers/code-generation-assistant.md)
- **Legacy System Modernization** (75/100): [Link](../prompts/developers/legacy-system-modernization.md)

---

## Prompt Patterns & Templates

### Common Patterns Found Across Top Libraries

#### 1. Role-Task-Format (RTF)
**Usage**: 68% of top prompts use this pattern

```
You are a [ROLE].

Your task is to [TASK].

Provide output in the following format:
[FORMAT_SPECIFICATION]
```

**Best for**: Software development, business analysis, reporting

---

#### 2. Task-Action-Goal (TAG)
**Usage**: 45% of top prompts

```
**Task**: [WHAT_TO_DO]
**Action**: [HOW_TO_DO_IT]
**Goal**: [DESIRED_OUTCOME]

[DETAILED_INSTRUCTIONS]
```

**Best for**: Sprint planning, process improvement, strategic initiatives

---

#### 3. Context-Action-Result-Example (CARE)
**Usage**: 52% of M365 prompts

```
**Context**: [BACKGROUND_INFORMATION]
**Action**: [WHAT_YOU_WANT]
**Result**: [EXPECTED_OUTPUT]
**Example**: [SAMPLE_OUTPUT]
```

**Best for**: Business communications, document generation, reporting

---

#### 4. Persona-Context-Task-Format
**Usage**: 73% of advanced technique prompts

```
You are a [PERSONA] with expertise in [DOMAIN].

**Context**: [SITUATION_BACKGROUND]
**Task**: [SPECIFIC_ASSIGNMENT]
**Format**: [OUTPUT_SPECIFICATION]

[DETAILED_REQUIREMENTS]
```

**Best for**: Technical documentation, code generation, architecture

---

#### 5. Think-Act-Observe-Reflect (ReAct)
**Usage**: Tool-augmented workflows

```
**Think**: [REASONING_ABOUT_NEXT_STEP]
**Act**: [TOOL_USAGE_OR_ACTION]
**Observe**: [RESULT_OF_ACTION]
**Reflect**: [EVALUATION_AND_NEXT_STEPS]

Repeat until goal achieved.
```

**Best for**: Research, data analysis, multi-step workflows

---

## Best Practices Summary

### Universal Best Practices (All Platforms)

1. **Be Specific**: Vague prompts produce vague outputs
   - ❌ "Analyze this data"
   - ✅ "Analyze this sales data for Q4 2024, identify top 5 products by revenue, and calculate month-over-month growth rates"

2. **Provide Context**: Background information improves relevance
   - Include purpose, audience, constraints
   - Reference related documents or data
   - Specify domain or industry

3. **Define Output Format**: Structure prevents confusion
   - JSON schema for automation
   - Markdown for documentation
   - Specific sections for reports

4. **Use Examples**: Show don't just tell
   - Provide sample inputs/outputs
   - Demonstrate desired style
   - Clarify edge cases

5. **Iterate and Refine**: First try rarely perfect
   - Start simple, add detail
   - Test with variations
   - Learn from results

### Platform-Specific Tips

**GitHub Copilot**:
- Use comments for context
- Keep prompts short (< 200 words)
- Open related files
- Specify language/version

**Microsoft 365**:
- Natural, conversational language
- Specify audience and tone
- Reference connected documents
- Use CARE pattern

**Claude/GPT**:
- Longer, detailed prompts OK
- Use XML tags for structure
- Request reasoning explicitly
- Specify exact format

**Windows Copilot**:
- Task-oriented requests
- Combine related actions
- Specify output preferences
- Use for quick system tasks

---

## Quick Reference

### Prompt Quality Checklist

Before using a prompt, verify:
- [ ] Clear, specific goal stated
- [ ] Necessary context provided
- [ ] Output format defined
- [ ] Constraints specified
- [ ] Examples included (if helpful)
- [ ] Edge cases addressed
- [ ] Appropriate reasoning style chosen
- [ ] Variables/placeholders documented

### Common Reasoning Styles

| Style | When to Use | Best For |
|-------|-------------|----------|
| **Direct** | Simple, straightforward tasks | Data extraction, formatting, quick edits |
| **Chain-of-Thought (CoT)** | Complex reasoning needed | Debugging, analysis, problem-solving |
| **Tree-of-Thoughts (ToT)** | Multiple approaches exist | Architecture, strategic decisions, trade-offs |
| **ReAct** | External tools/data required | Research, API integration, multi-step workflows |
| **Reflection** | Quality improvement needed | Self-review, iterative refinement, optimization |

### Scoring Quick Guide

Rate your prompt on each dimension (0-20):

| Dimension | Key Questions |
|-----------|---------------|
| **Clarity** | Is the goal clear? Are instructions specific? |
| **Structure** | Are all sections present? Is documentation complete? |
| **Usefulness** | Does it solve a common problem? Is it reusable? |
| **Technical** | Proper reasoning style? Structured output? Best practices? |
| **Ease of Use** | Simple to customize? Good examples? Helpful tips? |

**Target**: 75+ points for production use

---

## Additional Resources

### Research Papers
- Wei et al. (2022): "Chain-of-Thought Prompting" - NeurIPS
- Yao et al. (2023): "Tree of Thoughts" - NeurIPS
- White et al. (2024): "The Prompt Report" - arXiv:2406.06608

### Industry Guides
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/constructing-a-prompt)
- [OpenAI Best Practices](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-the-openai-api)
- [Microsoft 365 Copilot Adoption](https://adoption.microsoft.com/en-us/copilot/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

### Community Resources
- [awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) - 1000+ community prompts
- [LangChain Prompt Templates](https://github.com/langchain-ai/langchain) - Programmatic patterns
- [Microsoft Copilot Gallery](https://m365.cloud.microsoft/copilot-prompts) - Enterprise templates

---

## Contributing

Help us improve this guide:
1. Test prompts and share results
2. Suggest new patterns or techniques
3. Report issues or improvements
4. Share your success stories

**Repository**: [github.com/tafreeman/prompts](https://github.com/tafreeman/prompts)

---

**Version**: 1.0  
**Last Updated**: 2025-11-19  
**Maintainer**: Prompts Library Team

**License**: MIT - Free to use, modify, and distribute

---

*Made with research, analysis, and community contributions* ❤️
