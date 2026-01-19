# 💼 Business Prompts Evaluation

Evaluation test files for business-focused prompts including email templates, meeting facilitation, project management, and professional communication.

## 📋 Overview

This directory contains evaluation prompt files for testing business and professional communication prompts used across Microsoft 365, Teams, and enterprise workflows.

## 📁 Contents

```
business/
├── README.md                       # This file
├── business-eval-1.prompt.yml      # Batch 1: Communication templates
├── business-eval-2.prompt.yml      # Batch 2: Meeting & collaboration
├── business-eval-3.prompt.yml      # Batch 3: Project management
└── business-eval-4.prompt.yml      # Batch 4: Professional writing
```

## 🎯 Purpose

These evaluation files test prompts for:

- **Email Templates** - Professional correspondence, announcements
- **Meeting Facilitation** - Agendas, notes, summaries
- **Project Management** - Status reports, planning, tracking
- **Professional Writing** - Reports, proposals, documentation
- **Collaboration** - Team communication, decision-making
- **M365 Integration** - Teams, Outlook, SharePoint use cases
- **Business Analysis** - Requirements, planning, strategy
- **Stakeholder Communication** - Executive summaries, updates

## 🚀 Quick Start

### Run Evaluations

```bash
# Evaluate all business prompts
python -m prompteval testing/evals/business/ --tier 2 --verbose

# Evaluate specific batch
python -m prompteval testing/evals/business/business-eval-1.prompt.yml --tier 2

# With GitHub Models
gh models eval testing/evals/business/business-eval-1.prompt.yml
```

### Run CI/CD Validation

```bash
# Fast evaluation for CI (changed files only)
python -m prompteval testing/evals/business/ --ci --changed-only --tier 3

# Full evaluation for release
python -m prompteval testing/evals/business/ --tier 2 -o release-report.json
```

## 📊 Evaluation Criteria

Business prompts are evaluated with focus on:

| Criterion | Weight | Focus for Business |
|-----------|--------|-------------------|
| **Clarity** | 1.3x | Clear professional tone |
| **Specificity** | 1.2x | Precise business requirements |
| **Actionability** | 1.4x | Clear next steps/CTAs |
| **Structure** | 1.3x | Professional formatting |
| **Completeness** | 1.2x | All business elements |
| **Factuality** | 1.0x | Accurate information |
| **Consistency** | 1.2x | Brand voice alignment |
| **Safety** | 1.2x | Professional, appropriate |

**Quality Standards:**
- Overall score ≥ 7.0 (professional quality)
- No dimension < 6.0 (acceptable for business use)
- Variance ≤ 1.3 (consistent professional tone)

## 📦 Evaluation Batches

### Batch 1: business-eval-1.prompt.yml

**Category:** Communication Templates

**Prompts Evaluated:** 10-12

**Content Types:**
- Professional email templates
- Announcement drafts
- Follow-up messages
- Request templates
- Confirmation messages
- Introduction emails

**Key Prompts:**

| Prompt Type | Use Case | Target Audience |
|-------------|----------|-----------------|
| Email: Project Update | Status communication | Stakeholders |
| Email: Meeting Request | Schedule coordination | Teams |
| Email: Announcement | Company-wide news | All staff |
| Email: Follow-up | Post-meeting action | Participants |
| Email: Request | Resource/approval request | Managers |
| Email: Introduction | Networking | External partners |

**Usage:**

```bash
python -m prompteval testing/evals/business/business-eval-1.prompt.yml --tier 2
```

### Batch 2: business-eval-2.prompt.yml

**Category:** Meeting & Collaboration

**Prompts Evaluated:** 10-12

**Content Types:**
- Meeting agendas
- Meeting minutes/notes
- Action item tracking
- Decision documentation
- Retrospective templates
- Brainstorming facilitation

**Key Prompts:**

| Prompt Type | Use Case | Format |
|-------------|----------|--------|
| Meeting Agenda | Structure meetings | Markdown |
| Meeting Minutes | Document discussions | Structured |
| Action Items | Track commitments | Checklist |
| Decision Log | Record decisions | Table |
| Retrospective | Team reflection | Framework |

**Usage:**

```bash
python -m prompteval testing/evals/business/business-eval-2.prompt.yml --tier 2
```

### Batch 3: business-eval-3.prompt.yml

**Category:** Project Management

**Prompts Evaluated:** 10-12

**Content Types:**
- Status reports
- Project proposals
- Risk assessments
- Resource planning
- Timeline creation
- Milestone tracking

**Key Prompts:**

| Prompt Type | Use Case | Frequency |
|-------------|----------|-----------|
| Status Report | Weekly updates | Weekly |
| Project Proposal | Initiative planning | Ad-hoc |
| Risk Assessment | Risk identification | Monthly |
| Resource Plan | Capacity planning | Quarterly |
| Timeline | Schedule creation | Project start |

**Usage:**

```bash
python -m prompteval testing/evals/business/business-eval-3.prompt.yml --tier 2
```

### Batch 4: business-eval-4.prompt.yml

**Category:** Professional Writing

**Prompts Evaluated:** 10-12

**Content Types:**
- Business reports
- Executive summaries
- Technical documentation
- Proposals and RFPs
- Policy documents
- Standard Operating Procedures (SOPs)

**Key Prompts:**

| Prompt Type | Use Case | Length |
|-------------|----------|--------|
| Executive Summary | High-level overview | 1-2 pages |
| Technical Report | Detailed analysis | 5-10 pages |
| Proposal | Business case | 3-5 pages |
| Policy Document | Guidelines | 2-4 pages |
| SOP | Process documentation | 2-3 pages |

**Usage:**

```bash
python -m prompteval testing/evals/business/business-eval-4.prompt.yml --tier 2
```

## 🎯 Expected Results

### Good Business Prompt Example

```yaml
Score: 7.8/10 (Grade: B+)
Pass: ✅

Dimensions:
- clarity: 8        # Clear professional language
- specificity: 8    # Specific business context
- actionability: 9  # Clear next steps
- structure: 8      # Professional formatting
- completeness: 7   # All required elements
- factuality: 8     # Accurate information
- consistency: 8    # Consistent tone
- safety: 8         # Appropriate content

Strengths:
- Professional tone and formatting
- Clear call-to-action
- Appropriate for target audience
- Follows business communication best practices

Improvements:
- Add more context variables
- Include alternative tone options
- Provide more examples
```

### Business Prompt Quality Indicators

**Excellent Business Prompt (8.0+):**
- ✅ Clear, professional tone
- ✅ Appropriate for context
- ✅ Well-structured format
- ✅ Actionable next steps
- ✅ Customizable for audience
- ✅ Follows best practices

**Good Business Prompt (7.0-7.9):**
- ✅ Professional tone
- ✅ Clear structure
- ✅ Mostly actionable
- 🟡 Could be more specific
- 🟡 Minor improvements needed

**Needs Improvement (<7.0):**
- ❌ Unclear tone or purpose
- ❌ Poor structure
- ❌ Missing key elements
- ❌ Not actionable
- ❌ Inappropriate for audience

## 🎓 Best Practices for Business Prompts

### 1. Define Target Audience

```markdown
## Target Audience
- **Primary:** Engineering managers
- **Secondary:** Project stakeholders
- **Tone:** Professional but approachable
- **Technical Level:** Intermediate
```

### 2. Specify Business Context

```markdown
## Context
- **Situation:** [What's happening]
- **Background:** [Why this communication]
- **Objective:** [What you want to achieve]
- **Constraints:** [Deadlines, requirements]
```

### 3. Include Clear Structure

```markdown
## Email Structure

**Subject Line:** [Clear, actionable subject]

**Opening:**
- Greeting
- Context/purpose

**Body:**
- Main message
- Supporting details
- Evidence/data

**Closing:**
- Call to action
- Next steps
- Timeline

**Signature:**
- Professional sign-off
```

### 4. Provide Variables

```markdown
## Variables

{{recipient_name}} - Recipient's name
{{project_name}} - Project name
{{deadline}} - Due date
{{priority}} - Priority level (High/Medium/Low)
{{action_required}} - Specific action needed
```

### 5. Define Tone Options

```markdown
## Tone Variations

**Formal:** For executive communication
**Standard:** For team communication  
**Friendly:** For familiar colleagues
**Urgent:** For time-sensitive matters
```

## 🔧 Evaluation Configuration

### Business-Specific Evaluators

```yaml
model: openai/gpt-4o-mini
modelParameters:
  temperature: 0.3
  max_tokens: 2000

evaluators:
  # Standard evaluators
  - name: valid-json
  - name: has-overall-score
  - name: has-grade
  
  # Business-specific evaluators
  - name: professional-tone
    description: Maintains professional tone
    string:
      contains: '"tone_quality"'
  
  - name: clear-action
    description: Has clear call-to-action
    string:
      contains: '"actionability"'
  
  - name: audience-appropriate
    description: Appropriate for target audience
    string:
      contains: '"audience_fit"'
  
  - name: format-quality
    description: Professional formatting
    string:
      contains: '"structure"'
```

## 📈 Performance Metrics

### Evaluation Statistics

| Batch | Prompts | Avg Score | Pass Rate | Avg Time |
|-------|---------|-----------|-----------|----------|
| Batch 1 (Communication) | 12 | 7.6/10 | 92% | 5 min |
| Batch 2 (Meetings) | 11 | 7.8/10 | 91% | 5 min |
| Batch 3 (Projects) | 10 | 7.4/10 | 85% | 5 min |
| Batch 4 (Writing) | 10 | 7.7/10 | 88% | 6 min |
| **Total** | **43** | **7.6/10** | **89%** | **21 min** |

### Common Issues

| Issue | Frequency | Impact | Priority |
|-------|-----------|--------|----------|
| Too generic | 30% | Medium | High |
| Missing context | 20% | High | High |
| Unclear CTA | 15% | High | High |
| Poor formatting | 15% | Medium | Medium |
| Wrong tone | 10% | High | High |
| Missing variables | 10% | Medium | Medium |

## 🐛 Troubleshooting

### Low Clarity Scores

**Issue:** Prompt language is unclear or ambiguous

**Fix:**
- Use simple, direct language
- Define all acronyms
- Clarify purpose upfront
- Add examples

### Low Actionability Scores

**Issue:** No clear next steps or call-to-action

**Fix:**
- Add explicit CTA
- Define specific actions
- Include timeline
- Specify responsible parties

### Low Structure Scores

**Issue:** Poor formatting or organization

**Fix:**
- Use consistent headers
- Add clear sections
- Include bullets/lists
- Follow standard business format

### Wrong Tone

**Issue:** Inappropriate formality level

**Fix:**
- Define target audience
- Specify tone requirements
- Add tone examples
- Include tone variations

## 📖 Business Prompt Templates

### Email Template

```markdown
# Email: [Purpose]

## Context
**To:** {{recipient_name}}
**Subject:** {{subject_line}}
**Purpose:** {{purpose}}
**Tone:** {{tone_level}}

## Structure

**Opening:**
Hi {{recipient_name}},

{{context_sentence}}

**Body:**
{{main_message}}

**Key Points:**
- {{point_1}}
- {{point_2}}
- {{point_3}}

**Closing:**
{{call_to_action}}

{{timeline}}

Best regards,
{{sender_name}}
```

### Meeting Agenda Template

```markdown
# Meeting Agenda: [Topic]

**Date:** {{date}}
**Time:** {{time}}
**Duration:** {{duration}}
**Location:** {{location}}
**Attendees:** {{attendees}}

## Objectives
- {{objective_1}}
- {{objective_2}}

## Agenda Items

1. **Opening** (5 min)
   - Introductions
   - Agenda review

2. **{{topic_1}}** (15 min)
   - {{subtopic}}
   - Discussion points

3. **{{topic_2}}** (20 min)
   - {{subtopic}}
   - Decision needed

4. **Action Items & Next Steps** (10 min)
   - Review commitments
   - Set follow-up meeting

5. **Closing** (5 min)
```

## 📖 See Also

- [../README.md](../README.md) - Evals directory overview
- [../advanced/README.md](../advanced/README.md) - Advanced prompts evaluation
- [../analysis/README.md](../analysis/README.md) - Analysis prompts evaluation
- [../system/README.md](../system/README.md) - System prompts evaluation
- [../results/README.md](../results/README.md) - Evaluation results

---

**Built with ❤️ for professional business communication**
