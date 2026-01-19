# Workflows

This directory contains workflow definitions and process orchestration patterns for complex, multi-step AI-assisted tasks. Workflows combine prompts, reasoning patterns, and human oversight to accomplish sophisticated objectives.

## 📁 Directory Contents

```text
workflows/
├── business-planning-blueprint.md    # Strategic business planning framework
├── business-planning.md              # Executive business planning workflow
├── data-pipeline.md                  # Data processing and ETL workflows
├── incident-response-playbook.md     # Security incident response procedures
├── incident-response.md              # Incident management workflow
└── sdlc.md                          # Software Development Lifecycle workflow
```

## 🔄 What are Workflows
Workflows are **structured, multi-step processes** that orchestrate AI interactions with human oversight, external tools, and decision points. Unlike single prompts, workflows:

- **Chain multiple steps**: Connect prompts in a logical sequence
- **Include decision points**: Branch based on results or human input
- **Integrate tools**: Call external APIs, databases, or services
- **Require oversight**: Include human review and approval gates
- **Produce deliverables**: Generate concrete outputs (reports, code, documentation)

## 📚 Workflow Catalog

### Business Planning

#### [business-planning.md](business-planning.md)

**Purpose**: End-to-end business planning and strategy development

**Workflow Steps**:

1. Market analysis and research
2. Competitive landscape assessment
3. SWOT analysis generation
4. Strategic goal setting
5. Financial projections
6. Risk assessment
7. Executive summary compilation

**Best For**: Executives, business analysts, entrepreneurs  
**Duration**: 2-4 hours  
**Deliverables**: Business plan document, financial models, risk matrix

#### [business-planning-blueprint.md](business-planning-blueprint.md)

**Purpose**: Blueprint template for customizing business planning workflows

**Features**:

- Modular sections for different industries
- Customizable templates
- Integration with financial tools
- Compliance checklists

**Best For**: Consultants creating custom planning frameworks  
**Duration**: Initial setup 1-2 hours, then reusable

### Data Management

#### [data-pipeline.md](data-pipeline.md)

**Purpose**: Design, implement, and optimize data processing pipelines

**Workflow Steps**:

1. Requirements gathering and data source identification
2. Pipeline architecture design
3. ETL logic definition
4. Data validation rules
5. Error handling and monitoring
6. Performance optimization
7. Documentation generation

**Best For**: Data engineers, analytics teams  
**Duration**: 3-6 hours for new pipeline  
**Deliverables**: Pipeline code, documentation, monitoring dashboards

**Integrations**:

- Data warehouse platforms (Snowflake, BigQuery, Redshift)
- ETL tools (Airflow, dbt, Fivetran)
- Monitoring (Datadog, Grafana)

### Security & Incident Response

#### [incident-response.md](incident-response.md)

**Purpose**: Structured response to security incidents and operational issues

**Workflow Phases**:

1. **Detection**: Identify and triage incident
2. **Containment**: Limit scope and impact
3. **Investigation**: Root cause analysis
4. **Remediation**: Fix and restore services
5. **Documentation**: Incident report and lessons learned
6. **Follow-up**: Implement preventive measures

**Best For**: Security teams, SREs, operations  
**Severity Levels**: P0 (critical), P1 (high), P2 (medium), P3 (low)  
**Deliverables**: Incident report, remediation plan, post-mortem

#### [incident-response-playbook.md](incident-response-playbook.md)

**Purpose**: Detailed playbook with specific incident scenarios

**Covered Scenarios**:

- Security breaches (data leaks, unauthorized access)
- Service outages (downtime, performance degradation)
- Data corruption or loss
- Compliance violations
- Supply chain incidents

**Features**:

- Step-by-step checklists
- Communication templates
- Escalation procedures
- Compliance requirements (GDPR, SOX, HIPAA)

**Best For**: Security operations centers (SOCs), compliance teams

### Software Development

#### [sdlc.md](sdlc.md)

**Purpose**: AI-assisted Software Development Lifecycle from planning to deployment

**SDLC Phases**:

1. **Requirements**: User story creation, acceptance criteria
2. **Design**: Architecture decisions, system design
3. **Implementation**: Code generation, pair programming
4. **Testing**: Test generation, QA automation
5. **Review**: Code review, security scanning
6. **Deployment**: CI/CD, release notes
7. **Maintenance**: Bug fixes, monitoring

**Best For**: Development teams, engineering managers  
**Methodologies**: Agile, Scrum, Kanban  
**Deliverables**: Code, tests, documentation, deployment artifacts

**AI Integration Points**:

- Requirements: User story generation
- Design: Architecture review
- Code: GitHub Copilot integration
- Testing: Test case generation
- Review: Automated code review
- Docs: README and API doc generation

## 🎯 Choosing the Right Workflow

| Your Goal | Workflow | Duration | Complexity |
| ----------- | ---------- | ---------- | ------------ |
| Create business plan | business-planning.md | 2-4 hrs | Medium |
| Design data pipeline | data-pipeline.md | 3-6 hrs | High |
| Respond to incident | incident-response.md | Varies | High |
| Develop new feature | sdlc.md | 1-2 weeks | Medium |
| Custom planning framework | business-planning-blueprint.md | 1-2 hrs setup | Low |
| Security playbook | incident-response-playbook.md | Reference | Medium |

## 🔧 Workflow Anatomy

Each workflow document follows a consistent structure:

### 1. Overview

- **Purpose**: What the workflow achieves
- **When to use**: Applicable scenarios
- **Prerequisites**: Required tools, data, permissions

### 2. Workflow Steps
Numbered, sequential steps with:

- **Description**: What happens in this step
- **Prompts**: AI prompts to use
- **Tools**: External tools or APIs
- **Decision points**: Go/no-go criteria
- **Outputs**: Expected deliverables

### 3. Human Oversight

- **Review gates**: Where human approval is required
- **Escalation**: When to escalate to experts
- **Validation**: How to verify AI outputs

### 4. Deliverables

- **Artifacts**: What gets produced
- **Documentation**: Required documentation
- **Handoffs**: Who receives the output

### 5. Integration

- **Tools**: Compatible platforms and services
- **APIs**: External system connections
- **Automation**: CI/CD and orchestration

## 🚀 Running a Workflow

### Step 1: Preparation

```bash
# Clone the repository
git clone https://github.com/tafreeman/prompts.git
cd prompts/workflows

# Read the workflow file
cat sdlc.md
```

### Step 2: Setup

- Install required tools and dependencies
- Configure API keys and credentials
- Prepare input data or requirements

### Step 3: Execution

- Follow steps sequentially
- Use provided prompts at each stage
- Document decisions and outputs
- Checkpoint progress regularly

### Step 4: Review

- Human review at designated gates
- Validate AI outputs against criteria
- Escalate issues as needed

### Step 5: Completion

- Verify all deliverables produced
- Archive artifacts and documentation
- Conduct retrospective (for team workflows)

## 📊 Workflow Metrics

### Success Criteria

Track these metrics to evaluate workflow effectiveness:

- **Completion time**: Actual vs. estimated duration
- **Quality**: Deliverable quality scores
- **Efficiency**: AI vs. manual effort ratio
- **Accuracy**: Error rate in AI-generated outputs
- **Adoption**: Team usage frequency

### Improvement Opportunities

- **Bottlenecks**: Steps taking longer than expected
- **Errors**: Common failure points
- **Manual intervention**: Where automation could help
- **Tool gaps**: Missing integrations or capabilities

## 🔐 Security and Compliance

### Access Control

- **Sensitive workflows**: Require appropriate permissions
- **Audit trails**: Log all workflow executions
- **Data handling**: Follow PII and confidentiality rules

### Compliance Considerations

Different workflows have different compliance requirements:

| Workflow | Compliance Frameworks | Key Controls |
| ---------- | ---------------------- | -------------- |
| incident-response | SOX, ISO 27001, GDPR | Audit logs, encryption |
| data-pipeline | GDPR, CCPA, HIPAA | Data lineage, access control |
| business-planning | None (internal) | Confidentiality agreements |
| sdlc | SOC 2, ISO 27001 | Code review, security scanning |

## 🤝 Contributing Workflows

### Creating a New Workflow

1. **Identify the process**: Map out the end-to-end flow
2. **Define steps**: Break into discrete, actionable steps
3. **Add prompts**: Include specific AI prompts for each step
4. **Specify tools**: List required integrations
5. **Document oversight**: Where humans must intervene
6. **Test thoroughly**: Run the workflow end-to-end

### Workflow Template

```markdown
---
title: "Workflow Name"
category: "workflows"
tags: ["tag1", "tag2"]
author: "Author Name"
version: "1.0"
date: "2025-11-30"
duration: "X hours/days"
complexity: "low|medium|high"
---

# Workflow Name

## Overview
[Description of what this workflow achieves]

## Prerequisites

- Tool 1
- Permission 2
- Data source 3

## Workflow Steps

### Step 1: [Step Name]
**Objective**: What this step accomplishes

**Prompts**:
```

[AI prompt to use]

```

**Tools**: [External tools needed]
**Decision Point**: [Go/no-go criteria]
**Output**: [Expected deliverable]

[... additional steps ...]

## Deliverables

- Artifact 1
- Artifact 2

## Validation Checklist

- [ ] Check 1
- [ ] Check 2

## Troubleshooting
Common issues and solutions
```

### Quality Standards

Workflows must include:

- ✅ Clear step-by-step instructions
- ✅ Specific AI prompts (not generic)
- ✅ Decision criteria and review gates
- ✅ Tool integrations and API usage
- ✅ Real-world examples or case studies
- ✅ Compliance and security considerations
- ✅ Troubleshooting guidance

## 🔗 Integration with Other Components

### Prompts

Workflows reference prompts from the library:

```markdown
**Prompt**: Use [code-review-agent](../prompts/agents/code-review-agent.agent.md)
```

### Reasoning Patterns

Complex steps may use reasoning patterns:

```markdown
**Reasoning**: Apply [Chain-of-Verification](../reasoning/chain-of-verification.md)
```

### Tools

Workflows integrate with CLI tools:

```bash
# Evaluate workflow quality
prompttools evaluate workflows/sdlc.md

# Run workflow with automation
python tools/workflow_runner.py workflows/data-pipeline.md
```

## 📚 Related Resources

- **[Prompts](../prompts/)**: Individual prompts used in workflows
- **[Reasoning](../reasoning/)**: Reasoning patterns for complex steps
- **[Tools](../tools/)**: CLI utilities and automation
- **[Docs](../docs/)**: Conceptual documentation and tutorials

## 📖 Learning Resources

### Tutorials

- [Building Your First Workflow](../docs/tutorials/building-workflows.md)
- [Workflow Automation](../docs/tutorials/workflow-automation.md)

### Best Practices

- [Workflow Design Principles](../docs/concepts/workflow-design.md)
- [Human-in-the-Loop Patterns](../docs/concepts/human-oversight.md)

## 📄 License

All workflows are licensed under [MIT License](../LICENSE).

---

**Need help with a workflow?** Open an issue or discussion in the [main repository](https://github.com/tafreeman/prompts).
