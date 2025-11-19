---

title: "Tree-of-Thoughts: Architecture Evaluator"
category: "advanced-techniques"
tags: ["tree-of-thoughts", "architecture", "system-design", "developers", "trade-offs"]
author: "Prompt Engineering Team"
version: "1.0"
date: "2025-11-18"
difficulty: "advanced"
governance_tags: ["requires-human-review", "architecture-decision-record"]
platform: "Claude Sonnet 4.5"
---

# Tree-of-Thoughts: Architecture Evaluator

## Description

A specialized Tree-of-Thoughts prompt for evaluating multiple architecture options using systematic multi-branch reasoning. Explores alternatives (e.g., monolith vs microservices, SQL vs NoSQL, sync vs async), compares them across key dimensions, and converges on a justified recommendation with documented trade-offs.

## Research Foundation

Based on Tree-of-Thoughts (Yao et al., NeurIPS 2023) adapted for software architecture decisions. Incorporates principles from "Software Architecture in Practice" (Bass et al.) and architecture decision records (ADRs).

## Goal

Enable teams to evaluate architecture options systematically, document trade-offs explicitly, and make evidence-based decisions that can be reviewed and revisited as requirements evolve.

## Context

Use this prompt when facing architectural crossroads: choosing between patterns (monolith/microservices, layered/hexagonal), data stores (relational/document/graph), communication styles (REST/GraphQL/gRPC/events), deployment models (serverless/containers/VMs), or technology stacks. Best for decisions with long-term impact and multiple stakeholders.

## Inputs

- Problem statement or architectural challenge
- Current system context (if applicable)
- Requirements (functional and non-functional)
- Constraints (team size, budget, timeline, compliance)
- Key evaluation criteria (scalability, cost, complexity, etc.)

## Assumptions

- User has basic architecture knowledge
- Requirements are relatively stable (or areas of uncertainty are identified)
- Team can invest time in systematic evaluation (not emergency decisions)

## Constraints

- Focus on 3–5 architecture options (avoid analysis paralysis)
- Each option must be feasible within constraints
- Evaluation must be data-driven (benchmarks, case studies, team experience)
- Final recommendation must include risks and mitigations

## Process / Reasoning Style

**Tree-of-Thoughts (multi-branch exploration with evaluation and pruning)**

1. **Problem & Context:** Understand the architectural challenge
2. **Architecture Options (Branches):** Generate 3–5 distinct approaches
3. **Evaluation Criteria:** Define dimensions for comparison
4. **Branch Analysis:** Evaluate each option across criteria
5. **Trade-off Comparison:** Compare options head-to-head
6. **Pruning:** Eliminate clearly inferior options
7. **Deep Dive:** Explore top 2–3 options in detail
8. **Synthesis:** Recommend best option with rationale and risks

All branches and reasoning must be visible in the output.

## Output Requirements

Structured Markdown with the following sections:

1. **Problem & Context**
2. **Architecture Options (Branches)**
3. **Evaluation Criteria**
4. **Branch Analysis** (for each option)
5. **Trade-off Matrix** (comparison table)
6. **Pruned Options** (with justification)
7. **Deep Dive** (top 2–3 options)
8. **Recommendation** (final choice with rationale)
9. **Risks & Mitigations**
10. **Decision Record** (ADR-style summary)

## Use Cases

- Choosing between monolithic and microservices architectures
- Evaluating database technologies (SQL vs NoSQL vs polyglot)
- Selecting communication patterns (REST, GraphQL, gRPC, event-driven)
- Deciding on deployment models (serverless, containers, VMs, hybrid)
- Assessing frontend frameworks or state management approaches
- Migrating legacy systems (rewrite vs refactor vs strangle fig)

## Prompt

```text
You are an expert software architect using Tree-of-Thoughts (ToT) reasoning to evaluate architecture options systematically.

## Architectural Challenge

**Problem Statement:** [PROBLEM_DESCRIPTION]

**Current System Context:** [EXISTING_ARCHITECTURE_OR_GREENFIELD]

**Requirements:**

**Functional:**
- [FUNCTIONAL_REQUIREMENT_1]
- [FUNCTIONAL_REQUIREMENT_2]
- [FUNCTIONAL_REQUIREMENT_3]

**Non-Functional:**
- Scalability: [SCALABILITY_REQUIREMENTS]
- Performance: [LATENCY_THROUGHPUT_TARGETS]
- Availability: [UPTIME_REQUIREMENTS]
- Security: [SECURITY_COMPLIANCE_NEEDS]
- Maintainability: [TEAM_SIZE_SKILL_LEVEL]
- Cost: [BUDGET_CONSTRAINTS]

**Constraints:**
- Team: [TEAM_SIZE_EXPERIENCE_SKILLS]
- Timeline: [DELIVERY_DEADLINE]
- Compliance: [REGULATORY_REQUIREMENTS]
- Technical: [EXISTING_TECH_STACK_INTEGRATIONS]

**Additional Context:** [ANY_OTHER_RELEVANT_INFO]

---

## Task

Using Tree-of-Thoughts reasoning, evaluate architecture options systematically:

### Step 1: Problem & Context
Summarize the architectural challenge:
- What problem are we solving?
- What are the key requirements and constraints?
- What are the critical unknowns or risks?

### Step 2: Architecture Options (Branches)
Generate 3–5 distinct architecture options. For each option, provide a high-level description.

**Option A**: [Name, e.g., "Microservices with Event-Driven Communication"]
**Option B**: [Name, e.g., "Modular Monolith with Async Workers"]
**Option C**: [Name, e.g., "Serverless with API Gateway + Lambda"]
**Option D**: [Name] (optional)
**Option E**: [Name] (optional)

### Step 3: Evaluation Criteria
Define the dimensions for comparing options (typically 5–8 criteria):
1. Scalability (horizontal/vertical, traffic spikes)
2. Performance (latency, throughput)
3. Development Complexity (team ramp-up, debugging)
4. Operational Complexity (deployment, monitoring, troubleshooting)
5. Cost (infrastructure, licenses, engineering time)
6. Team Fit (skills, experience, learning curve)
7. Flexibility (future changes, extensibility)
8. Risk (unknowns, vendor lock-in, failure modes)

### Step 4: Branch Analysis
For each architecture option, evaluate it across the criteria:

**Option A: [Name]**

**Description:**
[Detailed description: components, data flow, communication patterns, technologies]

**Evaluation:**
- **Scalability**: [Score 1-10] - [Rationale]
- **Performance**: [Score 1-10] - [Rationale]
- **Development Complexity**: [Score 1-10] - [Rationale]
- **Operational Complexity**: [Score 1-10] - [Rationale]
- **Cost**: [Score 1-10] - [Rationale]
- **Team Fit**: [Score 1-10] - [Rationale]
- **Flexibility**: [Score 1-10] - [Rationale]
- **Risk**: [Score 1-10] - [Rationale]

**Overall Score**: [Sum or weighted average]

**Key Strengths**: [Top 2-3 advantages]
**Key Weaknesses**: [Top 2-3 disadvantages]

[Repeat for each option]

### Step 5: Trade-off Matrix
Create a comparison table:

| Criterion | Option A | Option B | Option C | Option D | Option E |
|-----------|----------|----------|----------|----------|----------|
| Scalability | [score] | [score] | [score] | [score] | [score] |
| Performance | [score] | [score] | [score] | [score] | [score] |
| Dev Complexity | [score] | [score] | [score] | [score] | [score] |
| Ops Complexity | [score] | [score] | [score] | [score] | [score] |
| Cost | [score] | [score] | [score] | [score] | [score] |
| Team Fit | [score] | [score] | [score] | [score] | [score] |
| Flexibility | [score] | [score] | [score] | [score] | [score] |
| Risk | [score] | [score] | [score] | [score] | [score] |
| **Total** | [sum] | [sum] | [sum] | [sum] | [sum] |

### Step 6: Pruned Options
Identify options to eliminate and explain why:

**Pruned: Option [X]**
- Reason: [Why this option is clearly inferior or infeasible]

**Pruned: Option [Y]**
- Reason: [Why this option doesn't meet requirements or constraints]

**Remaining Options**: [List the top 2–3 options to explore deeply]

### Step 7: Deep Dive
For each remaining option, explore in detail:

**Option [X]: [Name]**

**Detailed Architecture:**
[Describe components, data flow, technologies, deployment model]

**Implementation Plan:**
1. [Phase 1: Initial setup]
2. [Phase 2: Core features]
3. [Phase 3: Optimization and scale]

**Case Studies / References:**
- [Example of similar architecture in production]
- [Benchmarks or performance data]

**Edge Cases & Failure Modes:**
- [How does it handle X failure?]
- [What happens under extreme load?]

**Cost Estimate:**
- Infrastructure: [$X/month]
- Engineering: [Y person-months]
- Total: [$Z]

**Risk Assessment:**
- [Risk 1: description + mitigation]
- [Risk 2: description + mitigation]

[Repeat for each remaining option]

### Step 8: Recommendation
Based on the analysis, select the best option:

**Recommended Architecture**: [Option Name]

**Rationale:**
[Why this option is the best fit for the requirements, constraints, and team]

**Key Trade-offs Accepted:**
- [Trade-off 1: e.g., "Higher operational complexity for better scalability"]
- [Trade-off 2: e.g., "Steeper learning curve for long-term flexibility"]

**When This Recommendation Might Change:**
[Conditions under which a different option would be better, e.g., "If team grows to 50+, reconsider microservices"]

### Step 9: Risks & Mitigations

**Risk 1**: [Description]
- **Likelihood**: [High|Medium|Low]
- **Impact**: [High|Medium|Low]
- **Mitigation**: [How to address]

**Risk 2**: [Description]
- **Likelihood**: [High|Medium|Low]
- **Impact**: [High|Medium|Low]
- **Mitigation**: [How to address]

[Additional risks]

### Step 10: Decision Record (ADR-style)

**Status**: [Proposed | Accepted | Deprecated]

**Decision**: [One-sentence summary of the chosen architecture]

**Context**: [Why this decision was needed]

**Consequences**:
- Positive: [Benefits of this choice]
- Negative: [Downsides or costs]
- Risks: [Unknowns or concerns]

**Alternatives Considered**: [List other options and why they were rejected]

**Date**: [YYYY-MM-DD]

**Stakeholders**: [Who should review/approve this decision]

---

## Output Format

[Follow the structure above, filling in all sections with detailed analysis and reasoning]
```

## Variables

- `[PROBLEM_DESCRIPTION]`: The architectural challenge or decision to be made
- `[EXISTING_ARCHITECTURE_OR_GREENFIELD]`: Current system (if any) or "greenfield"
- `[FUNCTIONAL_REQUIREMENT_X]`: Core features or capabilities needed
- `[SCALABILITY_REQUIREMENTS]`: Expected traffic, growth projections
- `[LATENCY_THROUGHPUT_TARGETS]`: Performance SLOs
- `[UPTIME_REQUIREMENTS]`: Availability targets (e.g., 99.9%)
- `[SECURITY_COMPLIANCE_NEEDS]`: Regulatory or security requirements
- `[TEAM_SIZE_SKILL_LEVEL]`: Team composition and experience
- `[BUDGET_CONSTRAINTS]`: Cost limits
- `[DELIVERY_DEADLINE]`: Timeline
- `[REGULATORY_REQUIREMENTS]`: Compliance needs (GDPR, HIPAA, etc.)
- `[EXISTING_TECH_STACK_INTEGRATIONS]`: Must-use or must-avoid technologies
- `[ANY_OTHER_RELEVANT_INFO]`: Additional context

## Example Usage

**Input:**

```text
[Problem: E-commerce platform needs to scale from 10K to 1M users over 12 months, current monolith is hitting limits]
```

**Output:** (abbreviated)

```markdown
### Step 1: Problem & Context
We need to scale an e-commerce platform from 10K to 1M users in 12 months. Current monolith (Rails + PostgreSQL) is experiencing:
- Database bottlenecks (long queries, connection pool saturation)
- Deployment risks (downtime during deploys)
- Team coordination issues (10 developers committing to same codebase)

Key requirements: maintain < 200ms p99 latency, 99.9% uptime, support mobile and web clients.

### Step 2: Architecture Options (Branches)
**Option A**: Microservices with Event-Driven Communication (Kafka)
**Option B**: Modular Monolith with Read Replicas and Async Workers
**Option C**: Serverless (API Gateway + Lambda + DynamoDB)

### Step 4: Branch Analysis (Option B example)

**Option B: Modular Monolith with Read Replicas and Async Workers**

**Description:**
- Single deployable Rails app, but modularized internally (bounded contexts)
- PostgreSQL primary + 2 read replicas
- Sidekiq workers for async tasks (emails, analytics)
- Redis for caching and session storage
- Vertical scaling (larger DB instances) + horizontal scaling (app servers behind load balancer)

**Evaluation:**
- **Scalability**: 7/10 - Handles 1M users with read replicas and caching, but eventual limit
- **Performance**: 8/10 - Read replicas reduce DB load, caching improves latency
- **Development Complexity**: 9/10 - Team already knows Rails, modularization is incremental
- **Operational Complexity**: 8/10 - Simpler than microservices (single deploy, shared DB)
- **Cost**: 9/10 - Lower infrastructure cost than microservices
- **Team Fit**: 10/10 - Perfect match for current Rails team
- **Flexibility**: 6/10 - Can extract services later, but monolith limits independent deploys
- **Risk**: 8/10 - Lower risk (incremental change), but may need future migration

**Overall Score**: 65/80

**Key Strengths**: Low risk, team fit, cost-effective, incremental path
**Key Weaknesses**: Eventually hits scaling ceiling, tighter coupling than microservices

### Step 8: Recommendation

**Recommended Architecture**: Modular Monolith with Read Replicas and Async Workers (Option B)

**Rationale:**
- **Best fit for current team** (Rails expertise, no need to learn distributed systems)
- **Lowest risk** (incremental improvements to existing system)
- **Cost-effective** (avoids microservices overhead)
- **Sufficient for 1M users** (with read replicas and caching)
- **Future-proof** (modularization enables service extraction if needed beyond 1M users)

**Key Trade-offs Accepted:**
- **Accepting**: Tighter coupling and single deployment unit
- **Gaining**: Faster delivery, lower operational complexity, better team productivity

**When This Recommendation Might Change:**
- If traffic grows beyond 5M users, revisit microservices (Option A)
- If team grows beyond 30 developers, independent deployments become critical
- If compliance requires data isolation, consider service boundaries

### Step 9: Risks & Mitigations

**Risk 1**: Database becomes bottleneck even with read replicas
- **Likelihood**: Medium
- **Impact**: High
- **Mitigation**: Implement query optimization, add more read replicas, consider sharding hot tables

**Risk 2**: Modularization discipline erodes over time
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**: Enforce module boundaries with linting (packwerk), regular architecture reviews
```

## Tips

- **Generate diverse options:** Avoid subtle variations; ensure each branch represents a meaningfully different approach
- **Use quantitative criteria:** Score options numerically to enable objective comparison
- **Document trade-offs explicitly:** Every architecture has downsides; make them visible
- **Consider team constraints:** The "best" architecture on paper may not fit your team's skills or timeline
- **Plan for evolution:** Choose architectures that can adapt as requirements change
- **Validate with data:** Use benchmarks, case studies, or prototypes to support scores
- **Involve stakeholders:** Share this analysis with engineering, product, and leadership for alignment

## Related Prompts

- [Tree-of-Thoughts: Database Migration](tree-of-thoughts-database-migration.md) - For data migration decisions
- [Chain-of-Thought: Performance Analysis](chain-of-thought-performance-analysis.md) - For performance optimization
- [Refactoring Plan Designer](../developers/refactoring-plan-designer.md) - For incremental architecture changes
- [System Design Interview Prep](../developers/system-design-interview-prep.md) - Related system design patterns

## Governance Notes

- **Architecture Decision Record (ADR):** Save this analysis as an ADR for future reference
- **Human Review Required:** All architecture decisions should be reviewed by senior engineers and stakeholders
- **Cost Approval:** Ensure budget stakeholders approve cost estimates
- **Security Review:** Involve security team if architecture handles sensitive data
- **Compliance Check:** Ensure architecture meets regulatory requirements (GDPR, HIPAA, etc.)

## Changelog

- 2025-11-18: Initial version based on ToT repository evaluation recommendations
