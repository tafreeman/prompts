---
title: "Chain-of-Thought: Detailed Mode"
category: "advanced-techniques"
tags: ["chain-of-thought", "cot", "reasoning", "detailed", "comprehensive", "problem-solving"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "intermediate"
governance_tags: ["PII-safe", "requires-human-review-for-critical-decisions"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# Chain-of-Thought: Detailed Mode

## Description

A comprehensive Chain-of-Thought prompt template that encourages thorough step-by-step reasoning with detailed explanations, justifications, and consideration of alternatives. This mode is ideal for complex problems, high-stakes decisions, teaching contexts, or when stakeholders need to understand the complete reasoning process.

## Use Cases

- Complex architectural decisions requiring full justification
- Critical business decisions with significant financial or strategic impact
- Teaching or mentoring contexts where explanation aids learning
- Compliance scenarios requiring extensive documentation
- Novel problems where extensive exploration is beneficial
- Debugging complex, multi-system issues

## Prompt

```text
You are an expert problem solver using detailed chain-of-thought reasoning.

**Task**: [DESCRIBE_YOUR_TASK]

**Context**: [PROVIDE_COMPREHENSIVE_CONTEXT]

**Success Criteria**: [DEFINE_WHAT_SUCCESS_LOOKS_LIKE]

**Constraints**: [LIST_CONSTRAINTS_AND_REQUIREMENTS]

**Instructions**:
Think through this problem systematically and thoroughly. For each step:
1. Explain your reasoning in detail
2. Consider alternatives and explain why you chose this approach
3. Acknowledge assumptions explicitly
4. Note any uncertainties or risks

Format your response as:

**Understanding the Problem**
- Restate the problem in your own words
- Identify key challenges and unknowns
- List critical assumptions

**Step 1: [Title of Step]**
- **What**: [What you're doing in this step]
- **Why**: [Reasoning and justification]
- **Alternatives Considered**: [What else you thought about]
- **Risks/Assumptions**: [What could go wrong or what you're assuming]
- **Outcome**: [Result of this step]

**Step 2: [Title of Step]**
[Continue the same detailed format]

...

**Synthesis and Validation**
- How the steps fit together
- Validation that this addresses the original problem
- Edge cases or scenarios not fully addressed

**Final Answer**
- Clear, actionable conclusion
- Confidence level (High/Medium/Low) with justification
- Recommended next steps
- Potential refinements or follow-up questions
```

## Variables

- `[DESCRIBE_YOUR_TASK]`: The complete problem statement with all relevant details
- `[PROVIDE_COMPREHENSIVE_CONTEXT]`: Full background, history, constraints, stakeholders, prior attempts
- `[DEFINE_WHAT_SUCCESS_LOOKS_LIKE]`: Clear success criteria and acceptance conditions
- `[LIST_CONSTRAINTS_AND_REQUIREMENTS]`: Budget, time, technical, organizational, compliance constraints

## Example Usage

**Input:**

```text
You are an expert problem solver using detailed chain-of-thought reasoning.

**Task**: Design a microservices migration strategy for our monolithic e-commerce platform

**Context**: 
- Current monolith: 500K LOC Java application, 15 years old
- 200 developers, 50M active users, $500M annual revenue
- Database: MySQL 8TB, 10K+ tables
- Peak: 50K requests/second during holidays
- Previous migration attempt failed after 18 months, $5M spent
- Board wants migration complete in 24 months
- Need to maintain 99.99% uptime during migration

**Success Criteria**: 
- Gradual migration with no service disruptions
- Each phase delivers measurable business value
- Reduced deployment time from weeks to hours
- Individual service scaling capability
- Clear rollback plan for each phase

**Constraints**: 
- $10M budget over 24 months
- Cannot hire more than 20 additional engineers
- Must maintain current feature delivery velocity
- No more than 5% performance degradation during migration
- Compliance with PCI-DSS and GDPR throughout

**Instructions**:
[Detailed instructions as shown above]
```

**Output:**

```text
**Understanding the Problem**

*Restating the problem*: We need to decompose a large, business-critical monolith into microservices while the system continues serving 50M users and processing transactions worth $500M annually. The previous attempt failed, so we must learn from that and design a more cautious, incremental approach.

*Key challenges*:
1. Identifying service boundaries in a 15-year-old codebase with likely technical debt
2. Managing data migration for 8TB across 10K+ tables
3. Maintaining 99.99% uptime (only 52 minutes downtime/year allowed)
4. Doing this with existing team + only 20 new hires
5. Learning from previous $5M failed attempt

*Critical assumptions*:
- The monolith has some logical separation we can exploit (needs verification)
- The previous failure left documentation we can learn from
- Infrastructure can support gradual dual-running of old and new services
- Team has or can quickly gain microservices expertise

**Step 1: Analyze Previous Failure and Establish Foundations**

- **What**: Before designing new strategy, thoroughly understand why the previous $5M attempt failed. Also establish foundational infrastructure (service mesh, observability, CI/CD) before touching application code.

- **Why**: Repeating previous mistakes would waste resources and credibility. Additionally, trying to migrate application code without proper infrastructure is like building a house without a foundation - it will collapse. The previous attempt likely failed due to insufficient preparation.

- **Alternatives Considered**: 
  - Start with small service extraction (Strangler pattern immediately)
  - Rewrite-from-scratch approach
  - Chose analysis-first because blind repetition risks same failure

- **Risks/Assumptions**: 
  - Assumes previous attempt was documented (may not be)
  - Risk: Analysis paralysis - need to timebox this to 6 weeks
  - Assumes team will be honest about what went wrong

- **Outcome**: 
  - Document previous failure modes
  - Infrastructure requirements checklist
  - "Do not repeat" patterns list
  - Foundation: Service mesh (Istio/Linkerd), observability (Jaeger, Prometheus, Grafana), mature CI/CD

**Step 2: Domain-Driven Design Bounded Context Mapping**

- **What**: Conduct 8-week DDD workshop with domain experts and senior engineers to map bounded contexts. Don't extract services yet - just understand domain boundaries in current monolith.

- **Why**: The 10K+ tables and 500K LOC suggest the monolith evolved without clear boundaries. Service extraction without understanding domain model leads to distributed monoliths (worse than monoliths). DDD provides systematic approach to find natural seams.

- **Alternatives Considered**:
  - Extract by technical layers (all APIs, all databases): Creates distributed monolith
  - Extract by team boundaries: Teams may not align with business domains
  - Extract smallest/easiest service first: May not learn enough about complex domains

- **Risks/Assumptions**:
  - Assumes domain experts available for 8-week engagement
  - Risk: May discover domains are hopelessly entangled
  - Assumption: Bounded contexts exist (may find "big ball of mud")
  - Mitigation: If entanglement too severe, consider targeted refactoring before extraction

- **Outcome**:
  - Bounded context map
  - Service candidate list (prioritized by business value and extraction difficulty)
  - Database dependency graph
  - Estimate: 15-25 potential services identified

**Step 3: Design Migration Phases with Business Value Prioritization**

- **What**: Create 6-phase migration plan (4 months per phase = 24 months total). Each phase extracts 3-5 services prioritized by: (1) business value delivered, (2) technical feasibility, (3) learning value for team.

- **Why**: Phased approach with business value per phase ensures continued stakeholder support and funding. If we hit issues, we have delivered value and can pause. Fixed time boxes prevent scope creep.

- **Alternatives Considered**:
  - Big-bang migration (all at once): Too risky given previous failure
  - Pure technical-risk-first (easiest services first): Doesn't deliver business value early
  - Random/opportunistic extraction: No clear progress tracking

- **Risks/Assumptions**:
  - Assumes we can identify services with independent business value
  - Risk: Early phases may take longer as team learns
  - Assumption: Can deliver value with just 3-5 services extracted
  - Mitigation: Phase 1 includes "pilot" service to validate tooling and process

- **Outcome**:
  - **Phase 1** (Months 1-4): Infrastructure + Authentication Service (high reuse, clear boundary)
  - **Phase 2** (Months 5-8): Product Catalog Service (read-heavy, high business value)
  - **Phase 3** (Months 9-12): Shopping Cart Service (complex but high scaling need)
  - **Phase 4** (Months 13-16): Order Processing Service (critical path, high value)
  - **Phase 5** (Months 17-20): Inventory Management Service (complex data, regulatory)
  - **Phase 6** (Months 21-24): Payment Service + final cleanup

**Step 4: Strangler Fig Pattern with Anti-Corruption Layer**

- **What**: For each service extraction, use Strangler Fig pattern: 
  1. Build new service alongside monolith
  2. Route small percentage of traffic to new service (canary)
  3. Gradually increase traffic
  4. Deprecate monolith code only when 100% on new service
  Add Anti-Corruption Layer (ACL) to translate between old and new models.

- **Why**: Strangler Fig allows zero-downtime migration and instant rollback. ACL prevents new service from being constrained by monolith's data model. This addresses the uptime requirement and provides safety net.

- **Alternatives Considered**:
  - Direct service extraction (stop monolith, start service): High risk, violates uptime requirement
  - Database-first migration: Risky - data migration is hardest part
  - API Gateway-only routing: Doesn't address data migration

- **Risks/Assumptions**:
  - Assumes traffic can be gradually shifted (requires feature flags/router)
  - Risk: Dual-running increases infrastructure costs temporarily
  - Assumption: ACL translation overhead acceptable (needs performance testing)
  - Risk: Data inconsistency during dual-running period

- **Outcome**:
  - Strangler Fig implementation guide for teams
  - ACL reference implementation
  - Rollback procedures for each phase
  - Traffic shifting playbook (0%→5%→25%→50%→100%)

**Step 5: Data Migration Strategy - Event Sourcing Bridge**

- **What**: Implement event sourcing bridge between monolith and new services during transition. Monolith publishes events for all data changes. New services consume events and build their own data stores. Use Change Data Capture (CDC) for initial data load.

- **Why**: 8TB across 10K+ tables is too large for big-bang data migration. Event sourcing provides gradual, auditable data migration. CDC (e.g., Debezium) allows new service to sync from monolith database without code changes in monolith.

- **Alternatives Considered**:
  - Shared database (let services query monolith DB): Creates tight coupling, defeats microservices purpose
  - ETL batch migration: Downtime required, no real-time sync
  - Dual-write (monolith writes to both DBs): Consistency issues, error-prone

- **Risks/Assumptions**:
  - Assumes event bus (Kafka) can handle volume: needs capacity planning
  - Risk: Schema evolution challenges - event versioning required
  - Assumption: Eventual consistency acceptable (needs verification per service)
  - Risk: Data inconsistency during migration window (needs reconciliation tools)

- **Outcome**:
  - Event sourcing architecture design
  - CDC pipeline using Debezium + Kafka
  - Data consistency monitoring dashboards
  - Reconciliation procedures for data divergence

**Step 6: Team Structure and Skill Development**

- **What**: Restructure teams from feature teams to service ownership teams (2-pizza teams, 6-8 people per service). Implement 3-month skill-up program covering microservices, domain modeling, operations, and incident response.

- **Why**: Conway's Law - team structure should match architecture. 200 developers + 20 new hires = ~30 teams of 7. Each team owns 1-2 services end-to-end. Skill development addresses the "can't learn while migrating" problem from previous attempt.

- **Alternatives Considered**:
  - Keep feature teams, rotate through services: Lack of ownership leads to quality issues
  - Specialized teams (microservices team): Bottleneck, doesn't scale
  - External consultants do migration: No knowledge transfer, unsustainable

- **Risks/Assumptions**:
  - Assumes willingness to restructure teams (organizational change is hard)
  - Risk: Productivity dip during restructuring (3-6 months)
  - Assumption: Can hire 20 engineers with microservices experience
  - Risk: Turnover if people don't like new structure

- **Outcome**:
  - Team topology diagram (30 service teams)
  - Skill matrix and training plan
  - 20 job descriptions for new hires (microservices specialists)
  - 6-month productivity forecast (expect 30% dip months 1-2, return to baseline month 6)

**Synthesis and Validation**

*How steps fit together*: The strategy has three parallel tracks:
1. **Foundation** (Step 1): Infrastructure and learning from past
2. **Planning** (Steps 2-3): Domain understanding and phased approach
3. **Execution** (Steps 4-5): Technical patterns for safe migration
4. **Enablement** (Step 6): Team structure and skills

This addresses the root causes of previous failure:
- Insufficient infrastructure → Fixed in Step 1
- Unclear domain boundaries → Fixed in Steps 2-3
- Big-bang risk → Mitigated by Strangler Fig (Step 4)
- Data migration complexity → Event sourcing bridge (Step 5)
- Skill gaps → Training program (Step 6)

*Validation against success criteria*:
✓ Gradual migration: Strangler Fig + 6 phases
✓ No disruptions: Canary deployments + rollback plans
✓ Business value per phase: Phase prioritization by value
✓ Reduced deployment time: CI/CD in Step 1
✓ Individual scaling: Microservices architecture
✓ Clear rollback: Strangler Fig allows instant rollback

*Edge cases not fully addressed*:
- What if bounded contexts are too entangled? (May need refactoring first)
- What if performance degrades >5% during migration? (Need performance budgets)
- What if team doesn't achieve skill level needed? (May need to slow down)

**Final Answer**

**Recommended Migration Strategy**:

Implement a 6-phase, 24-month migration using Domain-Driven Design, Strangler Fig pattern, and event sourcing for data migration. The strategy emphasizes:

1. **Learn from previous failure** - Analyze what went wrong before starting
2. **Infrastructure-first** - Build foundation before touching application  
3. **Domain-driven service boundaries** - 8-week DDD workshop before extraction
4. **Business value per phase** - Each 4-month phase delivers measurable value
5. **Strangler Fig with ACL** - Zero-downtime migration with instant rollback
6. **Event sourcing bridge** - Gradual, auditable data migration via CDC + Kafka
7. **Team restructuring** - 30 service teams with clear ownership
8. **Continuous skill development** - 3-month training program

**Confidence Level**: **Medium-High (70%)**

*Justification*:
- High confidence in technical approach (Strangler Fig + Event Sourcing are proven patterns)
- Medium confidence in execution (organizational change is hard, previous attempt failed)
- Risk factors: Team skill level, domain untangling difficulty, budget constraints

**Recommended Next Steps**:
1. **Week 1-2**: Review documentation from previous failed attempt
2. **Week 3-6**: Set up infrastructure (service mesh, observability, CI/CD)
3. **Week 7-14**: Conduct DDD workshops with domain experts
4. **Week 15-16**: Finalize phase plan with stakeholder buy-in
5. **Month 4+**: Begin Phase 1 execution

**Potential Refinements**:
- May need to adjust timeline after DDD workshops (if domains more entangled than expected)
- Budget may need to shift between infrastructure and services based on findings
- Team size may need adjustment if skill-up takes longer than 3 months
- Consider external DDD consultant for workshops (accounted in budget)

**Follow-up Questions to Address**:
1. What exactly went wrong in the previous attempt? (Need detailed post-mortem)
2. Can we achieve eventual consistency for all services, or do some require strong consistency?
3. What is current team's microservices maturity level?
4. Are there regulatory constraints (PCI-DSS, GDPR) that affect data migration strategy?
5. What is current infrastructure capacity and can it support dual-running?
```

## Tips

- **When to use Detailed CoT**: Use for high-stakes decisions, novel problems, teaching contexts, or when stakeholders need to understand full reasoning.
- **Be thorough but structured**: Use the template sections to organize thoughts. Don't just ramble - follow the format.
- **Explicitly state assumptions**: Hidden assumptions are the source of most reasoning errors.
- **Consider alternatives seriously**: Don't just list alternatives to dismiss them - genuinely explore their merits.
- **Acknowledge uncertainty**: Medium/Low confidence answers with clear reasoning are better than false confidence.
- **Time investment**: Detailed CoT can take 5-10x longer than concise mode. Use when the investment is justified.
- **Synthesis matters**: The "Synthesis and Validation" section is where you tie everything together - don't skip it.

## When NOT to Use

- Simple, straightforward problems with obvious solutions
- Time-critical situations requiring quick decisions
- When audience is already expert and doesn't need explanation
- Resource-constrained environments (token limits, etc.)

## Related Prompts

- [Chain-of-Thought: Concise Mode](chain-of-thought-concise.md) - For quicker reasoning
- [Chain-of-Thought Guide](chain-of-thought-guide.md) - Decision framework for choosing CoT modes
- [Tree-of-Thoughts Template](tree-of-thoughts-template.md) - When you need to explore multiple solution paths
- [Reflection: Evaluator](reflection-evaluator.md) - For critiquing detailed reasoning

## Output Schema (JSON)

For automation pipelines, request output in this format:

```json
{
  "problem_understanding": {
    "restatement": "...",
    "key_challenges": ["...", "..."],
    "assumptions": ["...", "..."]
  },
  "reasoning_steps": [
    {
      "step": 1,
      "title": "...",
      "what": "...",
      "why": "...",
      "alternatives_considered": ["...", "..."],
      "risks_assumptions": ["...", "..."],
      "outcome": "..."
    }
  ],
  "synthesis": {
    "how_steps_fit": "...",
    "validation": "...",
    "edge_cases": ["...", "..."]
  },
  "final_answer": {
    "recommendation": "...",
    "confidence": "high|medium|low",
    "confidence_justification": "...",
    "next_steps": ["...", "..."],
    "potential_refinements": ["...", "..."]
  }
}
```

## Governance Notes

- **PII Safety**: This template doesn't inherently process PII. Ensure your task description and context don't include sensitive data.
- **Human Review Required For**:
  - Decisions with >$100K impact
  - Architecture decisions affecting >10 engineers
  - Security or compliance-critical choices
  - Novel problem domains without precedent
- **Audit Trail**: The detailed format provides comprehensive audit trail. Archive reasoning for critical decisions (minimum 7 years for compliance).
- **Quality Assurance**: Consider having 2-3 experts review detailed CoT for critical decisions (similar to code review).

## Platform Adaptations

### GitHub Copilot Chat

```text
@workspace /explain [complex-issue] using detailed chain-of-thought reasoning. Include alternatives considered and risks for each step.
```

### API Integration

```python
response = client.chat.completions.create(
    model="gpt-5.1",
    messages=[
        {"role": "system", "content": "You use detailed chain-of-thought reasoning with alternatives and justifications."},
        {"role": "user", "content": detailed_cot_prompt}
    ],
    temperature=0.7,  # Slightly higher for exploration
    max_tokens=4000   # Detailed mode needs more tokens
)
```

## Changelog

### Version 1.0 (2025-11-17)

- Initial release
- Comprehensive detailed CoT template with structured sections
- JSON schema for automation
- Governance metadata for enterprise use
- Platform adaptation examples
