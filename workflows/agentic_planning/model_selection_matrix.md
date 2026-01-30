# Model Selection Matrix & Agent Research

This document outlines the optimal model selections for **all 42 agent roles** across the four agentic workflows. Selections are based on the available providers: GitHub Models (`gh:`), Local ONNX (`local:`), Ollama (`ollama:`), and AI Toolkit (`aitk:`).

---

## 1. Available Model Capabilities Analysis

### Vision

| Tier | Model | Capabilities |
|:--|:--|:--|
| **Premium** | `gh:openai/gpt-4o` | Industry standard for multimodal reasoning |
| **Premium** | `gh:meta/llama-3.2-90b-vision-instruct` | Excellent open-weights alternative, high fidelity |
| **Efficient** | `local:phi3.5-vision` / `aitk:phi-3.5-vision` | Best-in-class for small local vision tasks |
| **Efficient** | `gh:microsoft/phi-4-multimodal-instruct` | Stronger reasoning than 3.5 |

### Reasoning (Planning, Architecture, Complex Logic)

| Tier | Model | Capabilities |
|:--|:--|:--|
| **Premium** | `gh:openai/o1` | Best for deep reasoning, complex planning, "thinking" tasks |
| **Premium** | `gh:deepseek/deepseek-r1` | SOTA open-weights reasoning, excellent at architectural decisions |
| **Fast** | `gh:openai/o3-mini` | Very fast, high reasoning capability |
| **Local** | `ollama:deepseek-r1:14b` | Distilled reasoning locally, amazing value/performance |
| **Local** | `aitk:phi-4-reasoning` | Microsoft's specialized small reasoning model |

### Coding (Implementation, Debugging, Tests)

| Tier | Model | Capabilities |
|:--|:--|:--|
| **Premium** | `gh:deepseek/deepseek-v3` | Extremely strong coding, rivals Claude 3.5 Sonnet |
| **Premium** | `gh:openai/gpt-4o` | Reliable, standard for coding agents |
| **Premium** | `gh:mistral-ai/codestral-2501` | Specialized for code generation |
| **Local** | `ollama:qwen2.5-coder:14b` | King of local coding (14B) |
| **Local** | `ollama:qwen3-coder:30b` | King of local coding (30B) |
| **Local** | `local:phi4` | Very capable for its size in Python/C# |

### General / Orchestration (Chat, Coordination, Triage)

| Tier | Model | Capabilities |
|:--|:--|:--|
| **Premium** | `gh:meta/meta-llama-3.1-405b-instruct` | Massive knowledge base, broad context |
| **Premium** | `gh:openai/gpt-5` | Next-gen flagship (preview) |
| **Fast** | `gh:openai/gpt-4o-mini` | Fast, cheap router |
| **Efficient** | `gh:meta/llama-3.1-8b-instruct` | Solid baseline |

---

## 2. Complete Agent Model Matrix (All 42 Agents)

### Workflow A: End-to-End Development (11 Agents)

| ID | Agent Name | Phase | Primary Model | Secondary Model | Tier | Rationale |
|:--|:--|:--|:--|:--|:--|:--|
| `vision_analyst` | Vision Analyst | Discovery | `gh:openai/gpt-4o` | `local:phi3.5-vision` | cloud_premium | High fidelity multimodal reasoning for accurate UI extraction |
| `ux_expert` | UX Expert | Discovery | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-v3` | cloud_premium | Visual understanding + empathy + WCAG knowledge |
| `business_analyst` | Business Analyst | Discovery | `gh:openai/o1` | `gh:openai/o3-mini` | cloud_reasoning | Deep reasoning to extrapolate complex business logic |
| `system_architect` | System Architect | Design | `gh:deepseek/deepseek-r1` | `ollama:deepseek-r1:14b` | cloud_reasoning | Excels at architectural trade-offs and structural planning |
| `database_architect` | Database Architect | Design | `gh:mistral-ai/codestral-2501` | `gh:deepseek/deepseek-v3` | cloud_coding | Specialized in code/SQL generation and structure |
| `frontend_dev` | Frontend Engineer | Implementation | `gh:deepseek/deepseek-v3` | `ollama:qwen2.5-coder:14b` | cloud_coding | State-of-the-art coding, modern framework expertise |
| `backend_dev` | Backend Engineer | Implementation | `gh:deepseek/deepseek-v3` | `gh:mistral-ai/codestral-2501` | cloud_coding | State-of-the-art coding, API design expertise |
| `cloud_engineer` | Cloud/DevOps Engineer | Implementation | `ollama:deepseek-r1:14b` | `gh:microsoft/phi-4` | local_reasoning | Good at configuration logic and deployment reasoning |
| `security_engineer` | Security Engineer | Assurance | `gh:openai/o3-mini` | `gh:deepseek/deepseek-r1` | cloud_reasoning_fast | Fast reasoning to detect logical vulnerabilities |
| `qa_engineer` | QA Engineer | Assurance | `gh:openai/gpt-4o` | `gh:meta/llama-3.3-70b-instruct` | cloud_premium | Comprehensive test cases mapping to user stories |
| `project_judge` | Project Judge | Assurance | `gh:openai/gpt-5` | `gh:openai/gpt-4o` | cloud_premium | High-level reasoning to synthesize all reports |

---

### Workflow B: Defect Resolution (11 Agents)

| ID | Agent Name | Phase | Primary Model | Secondary Model | Tier | Rationale |
|:--|:--|:--|:--|:--|:--|:--|
| `log_analyst` | Log Analyst | Intake | `local:phi4` | `local:mistral` | local_efficient | High-volume log processing needs speed and efficiency |
| `triage_agent` | Triage Agent | Intake | `gh:openai/gpt-4o-mini` | `gh:meta/llama-3.1-8b-instruct` | cloud_fast | Fast classification for high-volume initial analysis |
| `context_gatherer` | Context Gatherer | Analysis | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-v3` | cloud_std | Broad codebase understanding to gather relevant context |
| `reproduction_specialist` | Reproduction Specialist | Analysis | `gh:deepseek/deepseek-v3` | `ollama:qwen2.5-coder:14b` | cloud_coding | Strong coding ability for reliable failing test cases |
| `root_cause_analyst` | Root Cause Analyst | Analysis | `gh:openai/o1` | `gh:deepseek/deepseek-r1` | cloud_reasoning | Complex reasoning to trace logical errors |
| `impact_assessor` | Impact Assessor | Analysis | `gh:openai/o3-mini` | `gh:deepseek/deepseek-r1` | cloud_reasoning_fast | Fast reasoning about system-wide implications |
| `patch_engineer` | Patch Engineer | Resolution | `gh:deepseek/deepseek-v3` | `gh:mistral-ai/codestral-2501` | cloud_coding | Excellent coding for precise, minimal fixes |
| `code_reviewer` | Code Reviewer | Resolution | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-r1` | cloud_std | Broad knowledge to catch subtle issues in patches |
| `regression_tester` | Regression Tester | Verification | `gh:openai/gpt-4o` | `gh:meta/llama-3.3-70b-instruct` | cloud_std | Reliable at generating and interpreting test results |
| `documentation_updater` | Documentation Updater | Closure | `gh:openai/gpt-4o-mini` | `local:phi4` | cloud_fast | Fast and good at structured documentation generation |
| `resolution_judge` | Resolution Judge | Closure | `gh:openai/gpt-5` | `gh:openai/gpt-4o` | cloud_premium | High-level synthesis for final judgment on quality |

---

### Workflow C: Iterative System Design (10 Agents)

| ID | Agent Name | Phase | Primary Model | Secondary Model | Tier | Rationale |
|:--|:--|:--|:--|:--|:--|:--|
| `requirements_clarifier` | Requirements Clarifier | Discovery | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-v3` | cloud_std | Strong conversational ability to probe for missing details |
| `domain_expert` | Domain Expert | Discovery | `gh:openai/gpt-5` | `gh:meta/meta-llama-3.1-405b-instruct` | cloud_premium | Broad knowledge base for domain-specific expertise |
| `system_architect` | System Architect | Design | `gh:openai/o1` | `gh:deepseek/deepseek-r1` | cloud_reasoning | Best-in-class reasoning for architectural trade-offs |
| `infrastructure_advisor` | Infrastructure Advisor | Design | `gh:deepseek/deepseek-r1` | `ollama:deepseek-r1:14b` | cloud_reasoning | Reasoning about infrastructure trade-offs and optimization |
| `security_advisor` | Security Advisor | Design | `gh:openai/o3-mini` | `gh:deepseek/deepseek-r1` | cloud_reasoning_fast | Fast reasoning about security implications and attacks |
| `design_critic` | Design Critic | Review | `gh:openai/gpt-4o` | `gh:meta/meta-llama-3.1-405b-instruct` | cloud_std | Good at identifying inconsistencies, devil's advocate |
| `design_refiner` | Design Refiner | Refinement | `gh:deepseek/deepseek-r1` | `gh:openai/o1` | cloud_reasoning | Excellent at synthesizing feedback and restructuring |
| `cost_estimator` | Cost Estimator | Refinement | `gh:openai/gpt-4o` | `gh:meta/llama-3.3-70b-instruct` | cloud_std | Broad knowledge of cloud pricing and development effort |
| `spec_writer` | Specification Writer | Documentation | `gh:openai/gpt-4o-mini` | `local:phi4` | cloud_fast | Fast and efficient at structured documentation |
| `architecture_judge` | Architecture Judge | Documentation | `gh:openai/gpt-5` | `gh:meta/meta-llama-3.1-405b-instruct` | cloud_premium | High-level synthesis for final judgment on design quality |

---

### Workflow D: Code Grading (10 Agents)

| ID | Agent Name | Phase | Primary Model | Secondary Model | Tier | Rationale |
|:--|:--|:--|:--|:--|:--|:--|
| `static_analyst` | Static Code Analyst | Analysis | `local:phi4` | `local:mistral` | local_efficient | Fast and efficient for processing large codebases |
| `test_coverage_analyst` | Test Coverage Analyst | Analysis | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-v3` | cloud_std | Understands both code and tests for coverage quality |
| `documentation_reviewer` | Documentation Reviewer | Analysis | `gh:openai/gpt-4o-mini` | `local:phi4` | cloud_fast | Fast at evaluating natural language documentation |
| `security_auditor` | Security Auditor | Security | `gh:openai/o3-mini` | `gh:deepseek/deepseek-r1` | cloud_reasoning_fast | Fast reasoning to find logic flaws and vulnerabilities |
| `dependency_auditor` | Dependency Auditor | Security | `gh:openai/gpt-4o-mini` | `local:mistral` | cloud_fast | Fast processing of dependency manifests and CVE databases |
| `performance_reviewer` | Performance Reviewer | Quality | `gh:deepseek/deepseek-v3` | `gh:mistral-ai/codestral-2501` | cloud_coding | Deep code understanding to analyze algorithms |
| `architecture_compliance` | Architecture Compliance Checker | Quality | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-r1` | cloud_std | Broad pattern knowledge to assess architectural adherence |
| `maintainability_scorer` | Maintainability Scorer | Evaluation | `gh:deepseek/deepseek-r1` | `gh:openai/o1` | cloud_reasoning | Reasoning about long-term code evolution and tech debt |
| `best_practices_validator` | Best Practices Validator | Evaluation | `gh:openai/gpt-4o` | `gh:deepseek/deepseek-v3` | cloud_std | Up-to-date knowledge of framework-specific patterns |
| `head_judge` | Head Judge | Verdict | `gh:openai/gpt-5` | `gh:openai/gpt-4o` | cloud_premium | High-level synthesis to weight and combine all assessments |

---

## 3. Model Tier Summary

| Tier | Description | Token Cost | Best For |
|:--|:--|:--|:--|
| `cloud_premium` | Top-tier cloud models | $$$ | Final decisions, synthesis, high-stakes reasoning |
| `cloud_reasoning` | Reasoning-optimized cloud models | $$ | Planning, architecture, complex analysis |
| `cloud_reasoning_fast` | Fast reasoning models | $$ | Security analysis, quick evaluations |
| `cloud_coding` | Coding-optimized cloud models | $$ | Implementation, debugging, code generation |
| `cloud_std` | Standard cloud models | $ | General tasks, reviews, documentation |
| `cloud_fast` | Fast/cheap cloud models | ¢ | Triage, routing, simple tasks |
| `local_reasoning` | Local reasoning models | Free | DevOps, configuration, offline work |
| `local_efficient` | Efficient local models | Free | Preprocessing, log analysis, bulk processing |

---

## 4. Recommended Settings

### Temperature Guidelines

| Agent Type | Temperature | Rationale |
|:--|:--|:--|
| **Coding Agents** | `0.1 - 0.2` | Precision and reproducibility |
| **Reasoning/Design Agents** | `0.6 - 0.7` | Creativity and exploration |
| **Review/Grading Agents** | `0.0` | Consistent, objective evaluation |
| **Documentation Agents** | `0.2 - 0.3` | Clarity with some flexibility |
| **Triage/Routing Agents** | `0.1` | Consistent classification |

### Output Format Standards

* **System Prompts**: Strict role-based definition (e.g., "You are a Senior Architect...")
* **Output Formats**: Enforce Markdown or JSON for all inter-agent communication
* **Error Handling**: All agents should output structured error objects on failure
* **Confidence Scores**: Reasoning agents should include confidence levels (0.0-1.0)

---

## 5. Fallback Strategy

When primary models are unavailable:

1. **Try Secondary Model** from the same tier
2. **Downgrade to Efficient Tier** if speed is acceptable
3. **Queue for Later** if quality cannot be compromised
4. **Alert Human** if no fallback is suitable

### Critical Path Agents (No Degradation Allowed)

* `project_judge` - Final delivery decision
* `resolution_judge` - Defect closure decision
* `architecture_judge` - Design approval decision
* `head_judge` - Final grading decision
* `root_cause_analyst` - Debugging accuracy critical
