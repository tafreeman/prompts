---
title: "Reflection: Initial Answer + Self-Critique"
category: "advanced-techniques"
tags: ["reflection", "self-critique", "iterative", "improvement", "quality", "validation"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["PII-safe", "requires-human-review-for-critical-decisions"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# Reflection: Initial Answer + Self-Critique Pattern

## Description

The Reflection pattern involves generating an initial answer and then systematically critiquing it to identify weaknesses, gaps, or errors. This two-phase approach improves answer quality by catching mistakes, considering alternatives, and refining reasoning. Essential for high-stakes decisions, complex problems, or when accuracy is paramount.

## Use Cases

- Critical business decisions requiring validation
- Complex technical solutions needing error-checking
- High-stakes communications (executive briefings, client proposals)
- Code review and architecture decisions
- Compliance and legal document review
- Research and analysis requiring accuracy
- Teaching and explanation where correctness matters

## Prompt

```text
You will answer a question using a two-phase reflection pattern.

**Question**: [USER_QUESTION]

**Context**: [BACKGROUND_AND_CONSTRAINTS]

**Phase 1: Initial Answer**

Provide your best answer to the question. Think through it carefully, but don't over-analyze yet.

Format as:
**Initial Answer**:
[Your answer here]

---

**Phase 2: Self-Critique and Reflection**

Now, critically evaluate your initial answer using this framework:

**1. Accuracy Check**:
- Are all facts correct?
- Are there any logical errors?
- Did I make unsupported assumptions?
- Are there edge cases I missed?

**2. Completeness Check**:
- Did I fully answer the question?
- Are there important aspects I overlooked?
- Is additional context needed?
- Are there alternative perspectives to consider?

**3. Quality Check**:
- Is the answer clear and well-structured?
- Is the reasoning sound?
- Are examples appropriate?
- Is the level of detail appropriate for the audience?

**4. Bias Check**:
- Am I overly confident in any claims?
- Did I favor familiar solutions over better alternatives?
- Are there unstated assumptions affecting my answer?
- Did I consider diverse viewpoints?

**5. Risk Assessment**:
- What could go wrong if this answer is followed?
- What am I uncertain about?
- What additional validation is needed?
- What's my confidence level (High/Medium/Low)?

Based on this critique, provide:

**Critique Summary**:
- **Strengths**: What was good about the initial answer
- **Weaknesses**: What needs improvement
- **Gaps**: What's missing
- **Risks**: What could go wrong

**Revised Answer**:
[Improved answer incorporating the critique]

**Confidence Level**: High/Medium/Low
**Confidence Justification**: [Explain your confidence level]

**Recommended Next Steps**: [If applicable]
```

## Variables

- `[USER_QUESTION]`: The question or problem to solve
- `[BACKGROUND_AND_CONSTRAINTS]`: Context, requirements, constraints, success criteria

## Example Usage

**Input:**

```text
You will answer a question using a two-phase reflection pattern.

**Question**: Should we migrate our monolithic application to microservices?

**Context**: 
- Current: 300K LOC Java monolith, 8 years old
- Team: 30 developers
- Users: 10M MAU
- Revenue: $50M annually
- Pain points: Slow deployment (2-week cycle), scaling issues during peak
- Budget: $2M for migration
- Timeline: Must decide and plan this quarter

**Phase 1: Initial Answer**
[Generate initial answer]

**Phase 2: Self-Critique and Reflection**
[Apply critical evaluation framework]
```

**Output:**

```text
**Phase 1: Initial Answer**

**Initial Answer**:

Yes, you should migrate to microservices. Your pain points (slow deployment, scaling issues) are classic monolith problems that microservices solve. With $2M budget and 30 developers, you have sufficient resources for a phased migration over 18-24 months.

Recommended approach:
1. Start with strangler fig pattern
2. Extract the most painful services first (likely the scaling bottlenecks)
3. Implement proper service mesh (Istio or Linkerd)
4. Migrate gradually, service by service

Expected benefits:
- Deployment frequency: From 2 weeks to multiple times per day
- Scaling: Individual service scaling instead of scaling entire monolith
- Team autonomy: Teams can work on services independently
- Technology flexibility: Can use different languages/frameworks per service

Timeline: 18-24 months for complete migration.

---

**Phase 2: Self-Critique and Reflection**

**1. Accuracy Check**:
❌ **Error**: I stated benefits as certainties without acknowledging microservices introduce complexity
❌ **Oversimplification**: "$2M and 30 developers is sufficient" - didn't calculate actual costs or capacity
✓ **Correct**: Strangler fig pattern is appropriate for this scenario
❌ **Missing**: Didn't mention the previous migration attempt mentioned in the original problem statement (which failed)

**2. Completeness Check**:
❌ **Incomplete**: Didn't assess whether current pain points could be solved without microservices
❌ **Missing alternative**: What about modular monolith as intermediate step?
❌ **Didn't address**: Team's microservices experience level
❌ **Overlooked**: Operational overhead increase (monitoring, tracing, etc.)
❌ **Ignored**: The "must decide this quarter" constraint - my answer assumed YES without exploring NO

**3. Quality Check**:
✓ **Clear structure**: Answer was well-organized
❌ **Insufficient evidence**: Claims about benefits lack supporting data or conditions
❌ **Over-confident**: Presented one solution as obvious without trade-off analysis
✓ **Appropriate level**: Technical detail matches audience

**4. Bias Check**:
❌ **Recency bias**: Microservices are popular, so I defaulted to YES
❌ **Confirmation bias**: Looked for reasons to support migration, not reasons against
❌ **Ignored context**: "8 years old" doesn't necessarily mean bad - might be stable and profitable
❌ **Assumption**: Assumed scaling issues = need microservices (could be database, caching, or algorithmic)

**5. Risk Assessment**:
⚠️ **High risk**: Microservices could fail (complexity, coordination overhead, distributed system challenges)
⚠️ **Cost risk**: $2M may be insufficient if major infrastructure needed
⚠️ **Timeline risk**: 18-24 months is aggressive; previous attempt failed suggests underestimation
⚠️ **Organizational risk**: May not have DevOps/SRE capability to support microservices
⚠️ **Confidence**: Actually LOW - initial answer was overconfident

**Critique Summary**:

**Strengths**: 
- Identified strangler fig pattern correctly
- Recognized phased approach needed
- Connected pain points to potential solutions

**Weaknesses**:
- Assumed YES without proper analysis
- Didn't consider alternatives
- Overconfident despite insufficient information
- Ignored failure history mentioned in context

**Gaps**:
- No cost-benefit analysis
- No risk assessment
- No evaluation of alternative solutions
- No consideration of team capabilities
- No investigation of root causes for current pain points

**Risks**:
- Failed migration could waste $2M and 18+ months
- Microservices complexity could make things worse
- Team may lack necessary skills
- Deployment frequency claims unvalidated

**Revised Answer**:

**I need to challenge the premise: Should you migrate, or should you first diagnose and fix?**

**Before deciding, investigate:**

1. **Root Cause Analysis** (2-4 weeks):
   - Why is deployment slow? (Process vs. technical?)
   - What specifically doesn't scale? (App logic, database, I/O?)
   - Can these be fixed without microservices?

2. **Team Assessment** (1-2 weeks):
   - Microservices experience level?
   - DevOps/SRE capability?
   - Appetite for operational complexity?

3. **Alternative Solutions Analysis**:

   **Option A: Optimize Current Monolith** (~$200K, 3-6 months)
   - Fix deployment pipeline (CI/CD improvements)
   - Add horizontal scaling (if stateless)
   - Database optimization/caching
   - Cost: 10% of migration cost
   - Risk: Lower
   - Pros: Fast, low risk, leverages existing knowledge
   - Cons: May hit architectural limits eventually

   **Option B: Modular Monolith** (~$500K, 6-12 months)
   - Refactor into modules with clear boundaries
   - Enables future extraction if needed
   - Cost: 25% of full migration
   - Risk: Medium
   - Pros: Gets many microservices benefits, easier to reverse
   - Cons: Still a monolith, limited independent scaling

   **Option C: Hybrid Approach** (~$1M, 12-18 months)
   - Keep monolith for stable, core functionality
   - Extract only problematic services (e.g., high-scale services)
   - Cost: 50% of full migration
   - Risk: Medium
   - Pros: Targeted solution, manageable complexity
   - Cons: Some organizational complexity

   **Option D: Full Microservices** (~$2M+, 24-36 months)
   - Complete migration as initially suggested
   - Cost: $2M+ (likely more based on failure history)
   - Risk: High
   - Pros: Full benefits (if successful)
   - Cons: High risk, high cost, operational complexity

**My Recommendation**:

Start with **Option A** (optimize monolith) while investigating:
- If deployment slowness is CI/CD pipeline issue → Fix pipeline (weeks, not years)
- If scaling issue is database → Optimize queries, add caching, consider read replicas
- If specific services are bottlenecks → Consider **Option C** (extract only those)

**Only proceed with full microservices if**:
1. Optimization doesn't solve pain points (after 3-month trial)
2. Team has/can acquire microservices expertise
3. You're willing to accept 2-3x longer timeline than estimated (based on previous failure)
4. You budget $3-4M instead of $2M (more realistic for 300K LOC migration)

**Decision Timeline for This Quarter**:
- Week 1-2: Root cause analysis of deployment and scaling issues
- Week 3-4: Assess team capabilities and define success criteria
- Week 5-6: Cost/benefit analysis of Options A-D
- Week 7-8: Build business case, present to stakeholders
- Week 9-12: Begin Option A (quick wins) while refining long-term strategy

**Confidence Level**: **Medium**

**Confidence Justification**: 
I'm confident that investigating before committing is the right approach. However, I lack detailed information about:
- Specific nature of scaling issues
- Team's skill level and capacity
- Previous migration failure details
- Current system's technical debt level
- Organizational appetite for change

These unknowns prevent High confidence in any specific recommendation.

**Recommended Next Steps**:
1. Conduct technical assessment of monolith (scaling bottlenecks, deployment pipeline)
2. Review post-mortem from previous migration attempt
3. Assess team's microservices readiness (training needs, hiring needs)
4. Define measurable success criteria for any migration
5. Create detailed cost model for each option
6. Pilot Option A improvements for 90 days, measure impact
```

## Tips

- **Be harsh in critique**: The goal is to find problems, not justify the initial answer
- **Look for unstated assumptions**: What did you assume without explicitly stating?
- **Consider alternatives seriously**: Don't just list them to dismiss them
- **Quantify uncertainty**: Replace "should" with "might" where appropriate
- **Check your confidence calibration**: Are you overconfident? Under-confident?
- **Time investment**: Reflection adds 50-100% to response time; use for high-stakes questions
- **Iterate if needed**: If critique reveals major flaws, revise and critique again

## When to Use Reflection

### Use When

- **High stakes**: >$10K impact, affects >5 people, irreversible decisions
- **Novel problems**: Unfamiliar territory where assumptions are risky
- **Complex analysis**: Multiple factors, trade-offs, or interdependencies
- **Compliance/legal**: Correctness is critical
- **Teaching**: Modeling good thinking for others

### Don't Use When

- Simple, factual questions
- Time-critical situations requiring fast response
- Low-stakes, easily reversible decisions
- Well-understood, routine problems

## Output Schema (JSON)

```json
{
  "initial_answer": "...",
  "critique": {
    "accuracy_issues": ["...", "..."],
    "completeness_gaps": ["...", "..."],
    "quality_concerns": ["...", "..."],
    "bias_detected": ["...", "..."],
    "risks": ["...", "..."]
  },
  "critique_summary": {
    "strengths": ["...", "..."],
    "weaknesses": ["...", "..."],
    "gaps": ["...", "..."],
    "risks": ["...", "..."]
  },
  "revised_answer": "...",
  "confidence": {
    "level": "high|medium|low",
    "justification": "...",
    "remaining_uncertainties": ["...", "..."]
  },
  "next_steps": ["...", "..."]
}
```

## Related Prompts

- [Reflection: Iterative Improvement](reflection-iterative-improvement.md) - Multi-round refinement
- [Chain-of-Thought: Detailed](chain-of-thought-detailed.md) - Thorough reasoning
- [Tree-of-Thoughts Template](tree-of-thoughts-template.md) - Explore multiple approaches

## Governance Notes

- **PII Safety**: No inherent PII handling; ensure question/context don't contain sensitive data
- **Human Review Required**: For critiques of high-impact decisions (>$100K, legal, compliance)
- **Audit Trail**: Save both initial answer and revised answer for accountability
- **Quality Assurance**: Reflection output should be reviewed by domain expert for critical decisions

## Platform Adaptations

### API Integration

```python
def reflection_pattern(question, context):
    # Phase 1: Initial answer
    initial = llm.generate(f"Answer this question: {question}\nContext: {context}")
    
    # Phase 2: Self-critique
    critique_prompt = f"""
    Critically evaluate this answer:
    Question: {question}
    Answer: {initial}
    
    Find errors, gaps, biases, and risks.
    Then provide a revised, improved answer.
    """
    
    reflection = llm.generate(critique_prompt)
    
    return {
        "initial_answer": initial,
        "reflection": reflection,
        "final_answer": extract_revised_answer(reflection)
    }
```

## Changelog

### Version 1.0 (2025-11-17)

- Initial release
- Two-phase reflection pattern (initial + critique)
- Comprehensive critique framework
- Example demonstrating bias detection and assumption checking
- JSON schema for automation
