# Agentic Planning Workflows

This directory contains enterprise-grade configuration files for advanced agentic workflows designed for the Microsoft Agent Framework.

## Workflow Summary

| Workflow | Agents | Phases | Use Case |
|----------|--------|--------|----------|
| End-to-End Development | 11 | Discovery → Design → Implementation → Assurance | Full software delivery from mockups to production |
| Defect Resolution | 11 | Intake → Analysis → Resolution → Verification → Closure | Bug triage, investigation, fix, and validation |
| Iterative System Design | 10 | Discovery → Design → Review → Refinement → Documentation | Architectural design with critic-refiner loop |
| Code Grading | 10 | Analysis → Security → Quality → Evaluation → Verdict | Comprehensive code quality assessment |

---

## Workflow 1: End-to-End Development

**File:** `configs/workflow_end_to_end.json`

### Pipeline

```
[Mockups] → Vision Analyst → UX Expert → Business Analyst 
         → System Architect → Database Architect 
         → Frontend Engineer → Backend Engineer → Cloud/DevOps 
         → Security Engineer → QA Engineer → Project Judge → [Delivered Code]
```

### Agents (11)

| Agent | Model | Role |
|-------|-------|------|
| Vision Analyst | `gh:openai/gpt-4o` | Extract UI specifications from mockups |
| UX Expert | `gh:openai/gpt-4o` | Evaluate usability and accessibility |
| Business Analyst | `gh:openai/o1` | Define business process and workflows |
| System Architect | `gh:deepseek/deepseek-r1` | Design high-level architecture |
| Database Architect | `gh:mistral-ai/codestral-2501` | Design data model |
| Frontend Engineer | `gh:deepseek/deepseek-v3` | Implement UI components |
| Backend Engineer | `gh:deepseek/deepseek-v3` | Implement API and business logic |
| Cloud/DevOps | `ollama:deepseek-r1:14b` | Infrastructure and deployment |
| Security Engineer | `gh:openai/o3-mini` | Vulnerability analysis |
| QA Engineer | `gh:openai/gpt-4o` | Generate and run tests |
| Project Judge | `gh:openai/gpt-5` | Final sign-off and compliance |

---

## Workflow 2: Defect Resolution

**File:** `configs/workflow_defect_resolution.json`

### Pipeline

```
[Bug Report] → Log Analyst → Triage Agent → Context Gatherer 
            → Reproduction Specialist → Root Cause Analyst → Impact Assessor 
            → Patch Engineer → Code Reviewer → Regression Tester 
            → Documentation Updater → Resolution Judge → [Fixed & Verified]
```

### Agents (11)

| Agent | Model | Role |
|-------|-------|------|
| Log Analyst | `local:phi4` | Parse and structure raw logs |
| Triage Agent | `gh:openai/gpt-4o-mini` | Classify severity and route |
| Context Gatherer | `gh:openai/gpt-4o` | Collect relevant code context |
| Reproduction Specialist | `gh:deepseek/deepseek-v3` | Create minimal reproduction case |
| Root Cause Analyst | `gh:openai/o1` | Deep investigation of underlying cause |
| Impact Assessor | `gh:openai/o3-mini` | Assess blast radius of bug and fix |
| Patch Engineer | `gh:deepseek/deepseek-v3` | Implement the selected fix |
| Code Reviewer | `gh:openai/gpt-4o` | Review the patch for quality |
| Regression Tester | `gh:openai/gpt-4o` | Run regression suite |
| Documentation Updater | `gh:openai/gpt-4o-mini` | Update changelog and docs |
| Resolution Judge | `gh:openai/gpt-5` | Final verification and closure |

---

## Workflow 3: Iterative System Design

**File:** `configs/workflow_system_design.json`

### Pipeline

```
[Requirements] → Requirements Clarifier → Domain Expert 
              → System Architect → Infrastructure Advisor → Security Advisor 
              → Design Critic ⟷ Design Refiner (Loop until convergence)
              → Cost Estimator → Spec Writer → Architecture Judge → [Approved Design]
```

### Agents (10)

| Agent | Model | Role |
|-------|-------|------|
| Requirements Clarifier | `gh:openai/gpt-4o` | Elicit and clarify ambiguous requirements |
| Domain Expert | `gh:openai/gpt-5` | Provide domain-specific knowledge |
| System Architect | `gh:openai/o1` | Design high-level system architecture |
| Infrastructure Advisor | `gh:deepseek/deepseek-r1` | Design cloud infrastructure |
| Security Advisor | `gh:openai/o3-mini` | Design security architecture |
| Design Critic | `gh:openai/gpt-4o` | Critically evaluate the design |
| Design Refiner | `gh:deepseek/deepseek-r1` | Iterate on design based on feedback |
| Cost Estimator | `gh:openai/gpt-4o` | Estimate development and operational costs |
| Spec Writer | `gh:openai/gpt-4o-mini` | Compile final technical specification |
| Architecture Judge | `gh:openai/gpt-5` | Final approval of architecture |

---

## Workflow 4: Code Grading

**File:** `configs/workflow_code_grading.json`

### Pipeline

```
[Code Submission] → Static Analyst → Test Coverage Analyst → Documentation Reviewer 
                 → Security Auditor → Dependency Auditor 
                 → Performance Reviewer → Architecture Compliance → Maintainability Scorer 
                 → Best Practices Validator → Head Judge → [Final Grade Card]
```

### Agents (10)

| Agent | Model | Role |
|-------|-------|------|
| Static Analyst | `local:phi4` | Linting, style, complexity |
| Test Coverage Analyst | `gh:openai/gpt-4o` | Analyze test coverage and quality |
| Documentation Reviewer | `gh:openai/gpt-4o-mini` | Assess code comments and docs |
| Security Auditor | `gh:openai/o3-mini` | Identify security vulnerabilities |
| Dependency Auditor | `gh:openai/gpt-4o-mini` | Audit dependencies |
| Performance Reviewer | `gh:deepseek/deepseek-v3` | Analyze algorithmic efficiency |
| Architecture Compliance | `gh:openai/gpt-4o` | Verify code follows patterns |
| Maintainability Scorer | `gh:deepseek/deepseek-r1` | Assess long-term maintainability |
| Best Practices Validator | `gh:openai/gpt-4o` | Validate framework-specific practices |
| Head Judge | `gh:openai/gpt-5` | Aggregate scores and issue final grade |

### Grading Weights

- Security: 20%
- Test Coverage: 15%
- Performance: 15%
- Static Analysis: 10%
- Documentation: 10%
- Architecture: 10%
- Maintainability: 10%
- Dependencies: 5%
- Best Practices: 5%

---

## Model Tier Reference

| Tier | Purpose | Examples |
|------|---------|----------|
| `cloud_premium` | Highest capability | `gh:openai/gpt-5`, `gh:openai/o1` |
| `cloud_reasoning` | Complex reasoning | `gh:deepseek/deepseek-r1`, `gh:openai/o1` |
| `cloud_reasoning_fast` | Fast reasoning | `gh:openai/o3-mini` |
| `cloud_coding` | Code generation | `gh:deepseek/deepseek-v3`, `gh:mistral-ai/codestral-2501` |
| `cloud_std` | General purpose | `gh:openai/gpt-4o` |
| `cloud_fast` | Quick tasks | `gh:openai/gpt-4o-mini` |
| `local_reasoning` | Local reasoning | `ollama:deepseek-r1:14b`, `ollama:phi4-reasoning:latest` |
| `local_efficient` | High-volume local | `local:phi4`, `local:mistral` |

---

## Usage

Each agent in these workflows includes:

- **Primary model**: Best-in-class selection
- **Compatible models**: Fallback alternatives
- **System prompt**: Role-specific instructions
- **Temperature**: Tuned for the task type
- **Max tokens**: Sized for expected output

Load these JSON configurations into your orchestrator to execute the workflows.
