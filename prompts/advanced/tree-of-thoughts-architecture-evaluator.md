---
name: tree-of-thoughts-architecture-evaluator
description: 'AUTO-GENERATED: Tree-of-Thoughts architecture evaluator prompt. Please refine.'
type: how_to
difficulty: advanced
author: Prompt Engineering Team
date: '2025-11-18'
---
## Description

## Prompt

```text
---
name: Tree Of Thoughts Architecture Evaluator
description: title: 'Tree-of-Thoughts: Architecture Evaluator' shortTitle: ToT Architecture Evaluator intro: A specialized Tree-of-Thoughts prompt for evaluating multiple architecture options using systematic mult
type: how_to
---
```

title: 'Tree-of-Thoughts: Architecture Evaluator' shortTitle: ToT Architecture Evaluator intro: A specialized Tree-of-Thoughts prompt for evaluating multiple architecture options using systematic mult

## Description

## Prompt

```text
---
name: Tree Of Thoughts Architecture Evaluator
description: title: 'Tree-of-Thoughts: Architecture Evaluator' shortTitle: ToT Architecture Evaluator intro: A specialized Tree-of-Thoughts prompt for evaluating multiple architecture options using systematic mult
type: how_to
---
```

title: 'Tree-of-Thoughts: Architecture Evaluator' shortTitle: ToT Architecture Evaluator intro: A specialized Tree-of-Thoughts prompt for evaluating multiple architecture options using systematic mult


title: 'Tree-of-Thoughts: Architecture Evaluator'
shortTitle: ToT Architecture Evaluator
intro: A specialized Tree-of-Thoughts prompt for evaluating multiple architecture
  options using systematic multi-branch reasoning.
type: how_to
difficulty: advanced
audience:


platforms:


topics:


author: Prompt Engineering Team
version: '1.0'
date: '2025-11-18'
governance_tags:


dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
# Tree-of-Thoughts: Architecture Evaluator

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

## Variables

| Variable | Required? | Description | Example |
| --- |---:| --- | --- |
| `[PROBLEM_DESCRIPTION]` | Yes | The architectural problem statement to evaluate. | `Scale API from 10K to 1M users in 12 months` |
| `[EXISTING_ARCHITECTURE_OR_GREENFIELD]` | Yes | Current context or whether it is greenfield. | `Rails monolith + PostgreSQL` |
| `[FUNCTIONAL_REQUIREMENT_1]` | Yes | One functional requirement (add more as needed). | `Support web and mobile clients` |
| `[SCALABILITY_REQUIREMENTS]` | Yes | Scalability requirements and assumptions. | `Handle 5× traffic spikes` |
| `[LATENCY_THROUGHPUT_TARGETS]` | Yes | Performance targets. | `<200ms p99, 1k req/s` |
| `[UPTIME_REQUIREMENTS]` | Yes | Availability requirements. | `99.9% uptime` |
| `[SECURITY_COMPLIANCE_NEEDS]` | No | Security/compliance constraints. | `SOC2, GDPR` |
| `[TEAM_SIZE_EXPERIENCE_SKILLS]` | No | Team size and skill profile. | `10 devs; strong Rails; limited ops` |
| `[BUDGET_CONSTRAINTS]` | No | Budget constraints. | `$50k/month infra` |
| `[DELIVERY_DEADLINE]` | No | Timeline constraints. | `12 months` |
| `[ANY_OTHER_RELEVANT_INFO]` | No | Any additional context or constraints. | `must minimize downtime during deploys` |

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

## Use Cases

- Choosing between monolithic and microservices architectures
- Evaluating database technologies (SQL vs NoSQL vs polyglot)
- Selecting communication patterns (REST, GraphQL, gRPC, event-driven)
- Deciding on deployment models (serverless, containers, VMs, hybrid)
- Assessing frontend frameworks or state management approaches
- Migrating legacy systems (rewrite vs refactor vs strangle fig)

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
| ----------- | ---------- | ---------- | ---------- | ---------- | ---------- |
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

## Tips

- **Generate diverse options:** Avoid subtle variations; ensure each branch represents a meaningfully different approach
- **Use quantitative criteria:** Score options numerically to enable objective comparison
- **Document trade-offs explicitly:** Every architecture has downsides; make them visible
- **Consider team constraints:** The "best" architecture on paper may not fit your team's skills or timeline
- **Plan for evolution:** Choose architectures that can adapt as requirements change
- **Validate with data:** Use benchmarks, case studies, or prototypes to support scores
- **Involve stakeholders:** Share this analysis with engineering, product, and leadership for alignment

## Governance Notes

- **Architecture Decision Record (ADR):** Save this analysis as an ADR for future reference
- **Human Review Required:** All architecture decisions should be reviewed by senior engineers and stakeholders
- **Cost Approval:** Ensure budget stakeholders approve cost estimates
- **Security Review:** Involve security team if architecture handles sensitive data
- **Compliance Check:** Ensure architecture meets regulatory requirements (GDPR, HIPAA, etc.)## Variables

| Variable | Description |
|---|---|
| `[ANY_OTHER_RELEVANT_INFO]` | AUTO-GENERATED: describe `ANY_OTHER_RELEVANT_INFO` |
| `[BUDGET_CONSTRAINTS]` | AUTO-GENERATED: describe `BUDGET_CONSTRAINTS` |
| `[DELIVERY_DEADLINE]` | AUTO-GENERATED: describe `DELIVERY_DEADLINE` |
| `[EXISTING_ARCHITECTURE_OR_GREENFIELD]` | AUTO-GENERATED: describe `EXISTING_ARCHITECTURE_OR_GREENFIELD` |
| `[FUNCTIONAL_REQUIREMENT_1]` | AUTO-GENERATED: describe `FUNCTIONAL_REQUIREMENT_1` |
| `[LATENCY_THROUGHPUT_TARGETS]` | AUTO-GENERATED: describe `LATENCY_THROUGHPUT_TARGETS` |
| `[PROBLEM_DESCRIPTION]` | AUTO-GENERATED: describe `PROBLEM_DESCRIPTION` |
| `[SCALABILITY_REQUIREMENTS]` | AUTO-GENERATED: describe `SCALABILITY_REQUIREMENTS` |
| `[SECURITY_COMPLIANCE_NEEDS]` | AUTO-GENERATED: describe `SECURITY_COMPLIANCE_NEEDS` |
| `[TEAM_SIZE_EXPERIENCE_SKILLS]` | AUTO-GENERATED: describe `TEAM_SIZE_EXPERIENCE_SKILLS` |
| `[UPTIME_REQUIREMENTS]` | AUTO-GENERATED: describe `UPTIME_REQUIREMENTS` |
| `[X]` | AUTO-GENERATED: describe `X` |
| `[Y]` | AUTO-GENERATED: describe `Y` |
| `[YYYY-MM-DD]` | AUTO-GENERATED: describe `YYYY-MM-DD` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[$X/month]` | AUTO-GENERATED: describe `$X/month` |
| `[$Z]` | AUTO-GENERATED: describe `$Z` |
| `[ANY_OTHER_RELEVANT_INFO]` | AUTO-GENERATED: describe `ANY_OTHER_RELEVANT_INFO` |
| `[Additional risks]` | AUTO-GENERATED: describe `Additional risks` |
| `[BUDGET_CONSTRAINTS]` | AUTO-GENERATED: describe `BUDGET_CONSTRAINTS` |
| `[Benchmarks or performance data]` | AUTO-GENERATED: describe `Benchmarks or performance data` |
| `[Benefits of this choice]` | AUTO-GENERATED: describe `Benefits of this choice` |
| `[Conditions under which a different option would be better, e.g., "If team grows to 50+, reconsider microservices"]` | AUTO-GENERATED: describe `Conditions under which a different option would be better, e.g., "If team grows to 50+, reconsider microservices"` |
| `[DELIVERY_DEADLINE]` | AUTO-GENERATED: describe `DELIVERY_DEADLINE` |
| `[Describe components, data flow, technologies, deployment model]` | AUTO-GENERATED: describe `Describe components, data flow, technologies, deployment model` |
| `[Description]` | AUTO-GENERATED: describe `Description` |
| `[Detailed description: components, data flow, communication patterns, technologies]` | AUTO-GENERATED: describe `Detailed description: components, data flow, communication patterns, technologies` |
| `[Downsides or costs]` | AUTO-GENERATED: describe `Downsides or costs` |
| `[EXISTING_ARCHITECTURE_OR_GREENFIELD]` | AUTO-GENERATED: describe `EXISTING_ARCHITECTURE_OR_GREENFIELD` |
| `[Example of similar architecture in production]` | AUTO-GENERATED: describe `Example of similar architecture in production` |
| `[FUNCTIONAL_REQUIREMENT_1]` | AUTO-GENERATED: describe `FUNCTIONAL_REQUIREMENT_1` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[High|Medium|Low]` | AUTO-GENERATED: describe `High|Medium|Low` |
| `[How does it handle X failure?]` | AUTO-GENERATED: describe `How does it handle X failure?` |
| `[How to address]` | AUTO-GENERATED: describe `How to address` |
| `[LATENCY_THROUGHPUT_TARGETS]` | AUTO-GENERATED: describe `LATENCY_THROUGHPUT_TARGETS` |
| `[List other options and why they were rejected]` | AUTO-GENERATED: describe `List other options and why they were rejected` |
| `[List the top 2–3 options to explore deeply]` | AUTO-GENERATED: describe `List the top 2–3 options to explore deeply` |
| `[Name]` | AUTO-GENERATED: describe `Name` |
| `[Name, e.g., "Microservices with Event-Driven Communication"]` | AUTO-GENERATED: describe `Name, e.g., "Microservices with Event-Driven Communication"` |
| `[Name, e.g., "Modular Monolith with Async Workers"]` | AUTO-GENERATED: describe `Name, e.g., "Modular Monolith with Async Workers"` |
| `[Name, e.g., "Serverless with API Gateway + Lambda"]` | AUTO-GENERATED: describe `Name, e.g., "Serverless with API Gateway + Lambda"` |
| `[One-sentence summary of the chosen architecture]` | AUTO-GENERATED: describe `One-sentence summary of the chosen architecture` |
| `[Option Name]` | AUTO-GENERATED: describe `Option Name` |
| `[PROBLEM_DESCRIPTION]` | AUTO-GENERATED: describe `PROBLEM_DESCRIPTION` |
| `[Phase 1: Initial setup]` | AUTO-GENERATED: describe `Phase 1: Initial setup` |
| `[Phase 2: Core features]` | AUTO-GENERATED: describe `Phase 2: Core features` |
| `[Phase 3: Optimization and scale]` | AUTO-GENERATED: describe `Phase 3: Optimization and scale` |
| `[Proposed | Accepted | Deprecated]` | AUTO-GENERATED: describe `Proposed | Accepted | Deprecated` |
| `[Rationale]` | AUTO-GENERATED: describe `Rationale` |
| `[Repeat for each option]` | AUTO-GENERATED: describe `Repeat for each option` |
| `[Repeat for each remaining option]` | AUTO-GENERATED: describe `Repeat for each remaining option` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[Risk 1: description + mitigation]` | AUTO-GENERATED: describe `Risk 1: description + mitigation` |
| `[Risk 2: description + mitigation]` | AUTO-GENERATED: describe `Risk 2: description + mitigation` |
| `[SCALABILITY_REQUIREMENTS]` | AUTO-GENERATED: describe `SCALABILITY_REQUIREMENTS` |
| `[SECURITY_COMPLIANCE_NEEDS]` | AUTO-GENERATED: describe `SECURITY_COMPLIANCE_NEEDS` |
| `[Score 1-10]` | AUTO-GENERATED: describe `Score 1-10` |
| `[Sum or weighted average]` | AUTO-GENERATED: describe `Sum or weighted average` |
| `[TEAM_SIZE_EXPERIENCE_SKILLS]` | AUTO-GENERATED: describe `TEAM_SIZE_EXPERIENCE_SKILLS` |
| `[Top 2-3 advantages]` | AUTO-GENERATED: describe `Top 2-3 advantages` |
| `[Top 2-3 disadvantages]` | AUTO-GENERATED: describe `Top 2-3 disadvantages` |
| `[Trade-off 1: e.g., "Higher operational complexity for better scalability"]` | AUTO-GENERATED: describe `Trade-off 1: e.g., "Higher operational complexity for better scalability"` |
| `[Trade-off 2: e.g., "Steeper learning curve for long-term flexibility"]` | AUTO-GENERATED: describe `Trade-off 2: e.g., "Steeper learning curve for long-term flexibility"` |
| `[UPTIME_REQUIREMENTS]` | AUTO-GENERATED: describe `UPTIME_REQUIREMENTS` |
| `[Unknowns or concerns]` | AUTO-GENERATED: describe `Unknowns or concerns` |
| `[What happens under extreme load?]` | AUTO-GENERATED: describe `What happens under extreme load?` |
| `[Who should review/approve this decision]` | AUTO-GENERATED: describe `Who should review/approve this decision` |
| `[Why this decision was needed]` | AUTO-GENERATED: describe `Why this decision was needed` |
| `[Why this option doesn't meet requirements or constraints]` | AUTO-GENERATED: describe `Why this option doesn't meet requirements or constraints` |
| `[Why this option is clearly inferior or infeasible]` | AUTO-GENERATED: describe `Why this option is clearly inferior or infeasible` |
| `[Why this option is the best fit for the requirements, constraints, and team]` | AUTO-GENERATED: describe `Why this option is the best fit for the requirements, constraints, and team` |
| `[X]` | AUTO-GENERATED: describe `X` |
| `[Y]` | AUTO-GENERATED: describe `Y` |
| `[Y person-months]` | AUTO-GENERATED: describe `Y person-months` |
| `[YYYY-MM-DD]` | AUTO-GENERATED: describe `YYYY-MM-DD` |
| `[score]` | AUTO-GENERATED: describe `score` |
| `[sum]` | AUTO-GENERATED: describe `sum` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

