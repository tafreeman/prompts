---
title: "Interview Questions Generator"
shortTitle: "Interview Questions"
intro: "Generate structured, behavioral interview questions tailored to specific roles, levels, and competencies."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "recruiting"
  - "hr"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Interview Questions Generator

## Description

Create structured interview questions that assess candidates fairly and effectively. Generates behavioral, situational, and technical questions with scoring rubrics and follow-up probes.

## Use Cases

- Preparing for candidate interviews
- Building standardized interview guides for roles
- Training new interviewers on behavioral interviewing
- Ensuring consistent evaluation across candidates
- Creating competency-based assessment frameworks

## Prompt

```text
You are an expert interviewer trained in behavioral and structured interviewing techniques.

Create interview questions for:

**Role**: [role]
**Level**: [level]
**Key Competencies**: [competencies]
**Interview Stage**: [stage]
**Time Available**: [time]

Generate:

1. **Opening Questions** (2 questions)
   - Rapport building
   - Background/motivation

2. **Behavioral Questions** (4-5 questions)
   - One per key competency
   - STAR format prompts
   - Follow-up probes for each

3. **Situational Questions** (2-3 questions)
   - Hypothetical scenarios relevant to the role
   - Tests judgment and approach

4. **Role-Specific Questions** (2-3 questions)
   - Technical or domain knowledge
   - Practical application

5. **Candidate Questions** (suggested topics)
   - What strong candidates typically ask
   - Red flags to watch for

6. **Scoring Rubric**
   - What "great" looks like for each competency
   - What "concerning" looks like

Format as an interview guide with timing suggestions.
```

## Variables

- `[role]`: Job title and brief description of the role
- `[level]`: Seniority level (e.g., "Senior IC", "First-time manager", "Director")
- `[competencies]`: 3-5 key competencies to assess (e.g., "Problem-solving, collaboration, technical depth")
- `[stage]`: Interview stage (e.g., "Phone screen", "Hiring manager round", "Final onsite")
- `[time]`: Duration of the interview (e.g., "45 minutes", "60 minutes")

## Example Usage

**Input:**

```text
Role: Product Manager - Growth team, responsible for user acquisition and activation funnels
Level: Senior (5+ years PM experience), individual contributor
Key Competencies: Data-driven decision making, cross-functional leadership, experimentation mindset, customer empathy, strategic thinking
Interview Stage: Hiring manager round (second interview, passed recruiter screen)
Time Available: 60 minutes
```

**Output:**

```markdown
# Interview Guide: Senior Product Manager, Growth

**Duration**: 60 minutes  
**Interviewer**: Hiring Manager  
**Stage**: Round 2 of 4

---

## Interview Structure

| Section | Time | Focus |
|---------|------|-------|
| Opening | 5 min | Rapport, background |
| Behavioral | 25 min | Core competencies |
| Situational | 15 min | Judgment, approach |
| Role-Specific | 10 min | Growth PM skills |
| Candidate Q&A | 5 min | Their questions |

---

## 1. Opening Questions (5 minutes)

### Q1: Rapport Builder
*"Thanks for joining today. Before we dive in, I'd love to hear - what's got you excited about this role specifically?"*

**Listen for**: Genuine enthusiasm, research they've done, alignment with growth focus

### Q2: Background Context
*"Walk me through your PM journey - how did you get into product, and what's drawn you toward growth specifically?"*

**Listen for**: Intentional career progression, passion for growth/experimentation, not just "fell into PM"

---

## 2. Behavioral Questions (25 minutes)

### Competency 1: Data-Driven Decision Making

**Main Question**:
*"Tell me about a time you had to make a significant product decision with incomplete or conflicting data. How did you approach it?"*

**Follow-up Probes**:
- "What data did you have vs. what did you wish you had?"
- "How did you validate your assumptions?"
- "What would you do differently now?"

**STAR Expectations**:
- **Situation**: Clear business context and stakes
- **Task**: Their specific ownership
- **Action**: Structured approach to synthesis, not just gut feel
- **Result**: Measurable outcome + learnings

---

### Competency 2: Cross-Functional Leadership

**Main Question**:
*"Describe a situation where you needed to get alignment from engineering, design, and other stakeholders who had competing priorities. How did you navigate it?"*

**Follow-up Probes**:
- "How did you prioritize whose concerns to address first?"
- "What did you do when someone still disagreed?"
- "How did you maintain the relationship after?"

**STAR Expectations**:
- Shows influence without authority
- Demonstrates empathy for other teams' constraints
- Found creative solutions, not just escalated

---

### Competency 3: Experimentation Mindset

**Main Question**:
*"Tell me about an experiment you ran that failed. What did you learn, and how did it influence your next steps?"*

**Follow-up Probes**:
- "How did you decide what to test in the first place?"
- "How did you communicate the failure to stakeholders?"
- "What did you do with the learnings?"

**STAR Expectations**:
- Embraces failure as learning (not defensive)
- Has a rigorous experimentation framework
- Can articulate statistical significance, sample sizes

---

### Competency 4: Customer Empathy

**Main Question**:
*"Walk me through a time you discovered a customer insight that fundamentally changed your product direction. How did you uncover it?"*

**Follow-up Probes**:
- "What methods did you use (interviews, data, observation)?"
- "How did you convince others the insight was valid?"
- "How did you avoid confirmation bias?"

**STAR Expectations**:
- Direct customer interaction (not just reading reports)
- Synthesized qualitative + quantitative
- Changed their own mind, not just validated assumptions

---

### Competency 5: Strategic Thinking

**Main Question**:
*"Tell me about a time you identified a growth opportunity that wasn't on anyone's roadmap. How did you build the case for it?"*

**Follow-up Probes**:
- "How big was the opportunity vs. current priorities?"
- "What tradeoffs did you have to make?"
- "How did you sequence the rollout?"

**STAR Expectations**:
- Thinks beyond current sprint/quarter
- Can quantify opportunity size
- Balances vision with pragmatic execution

---

## 3. Situational Questions (15 minutes)

### Scenario 1: Prioritization Under Pressure

*"Imagine you're 3 weeks into a quarter. Your team is working on an activation improvement projected to lift conversion 10%. Your CEO comes to you with a request from a key enterprise customer that would require pausing this work. The customer represents 15% of ARR. How do you handle this?"*

**What to assess**:
- Framework for evaluating tradeoffs (not just "it depends")
- Stakeholder management instincts
- Ability to push back respectfully

**Great answer includes**: Quantifies both opportunities, proposes alternatives (parallel path, timeline negotiation), aligns on decision criteria before deciding

---

### Scenario 2: Experiment Design

*"You're tasked with improving our onboarding flow. Activation rate is 34% (new users who complete setup within 7 days). You have 4 weeks and one engineer. Walk me through how you'd approach this."*

**What to assess**:
- Structured thinking (diagnose before prescribe)
- Experimentation rigor
- Scrappiness within constraints

**Great answer includes**: Starts with data/funnel analysis, talks to churned users, prioritizes highest-leverage tests, acknowledges what they'd do with more resources

---

### Scenario 3: Stakeholder Conflict

*"Your data science team's analysis shows Feature X will increase activation by 8%. Your UX researcher is convinced it will hurt long-term retention because it feels 'spammy.' You need to make a call. What do you do?"*

**What to assess**:
- Handles ambiguity without analysis paralysis
- Values both quantitative and qualitative input
- Makes decisions, doesn't just gather consensus

**Great answer includes**: Proposes ways to test both hypotheses, weighs short-term vs. long-term tradeoffs, makes a clear recommendation with rationale

---

## 4. Role-Specific Questions (10 minutes)

### Growth PM Technical Skills

**Q1: Metrics**
*"How would you structure the metrics for a growth team? What's your North Star vs. supporting metrics?"*

**Listen for**: Understands leading vs. lagging indicators, can articulate funnel stages, doesn't obsess over vanity metrics

**Q2: Tooling**
*"What's your experience with experimentation platforms and analytics tools? Walk me through your typical workflow for launching and analyzing an experiment."*

**Listen for**: Hands-on with Amplitude/Mixpanel, understands statistical significance, can configure experiments independently

**Q3: Growth Levers**
*"If you joined our Growth team next month, what's the first thing you'd want to understand about our acquisition and activation funnels?"*

**Listen for**: Asks smart questions (not generic), prioritizes understanding before acting, shows genuine curiosity

---

## 5. Candidate Questions (5 minutes)

### What Strong Candidates Ask
- "What does the current activation funnel look like? Where are the biggest drop-offs?"
- "How does the Growth team collaborate with Core Product?"
- "What experiments has the team run recently? What worked vs. didn't?"
- "What does success in this role look like at 90 days? 1 year?"
- "What's the biggest challenge the Growth team is facing right now?"

### Red Flag Questions
- Only asking about comp, title, or promotion timeline
- No questions prepared at all
- Questions that show they didn't read the job description
- "What does this company do again?"

---

## 6. Scoring Rubric

| Competency | Strong (4-5) | Adequate (3) | Concerning (1-2) |
|------------|--------------|--------------|------------------|
| **Data-Driven** | Cites specific metrics, acknowledges data limitations, makes probabilistic decisions | Uses data but can't explain methodology deeply | Relies on intuition, can't articulate how they'd measure success |
| **Cross-Functional** | Concrete examples of building consensus, shows empathy for other teams | Has collaborated but waited for decisions to come to them | Blames other teams, sees alignment as someone else's job |
| **Experimentation** | Can design rigorous experiments, embraces failures, iterates based on learnings | Has run experiments but didn't own the analysis | Hasn't run real experiments or sees them as "nice to have" |
| **Customer Empathy** | Direct customer contact, synthesizes qual + quant, changed their own mind | Reads user research but doesn't conduct it | Views customers as abstract personas, not real people |
| **Strategic** | Identifies opportunities independently, can size and sequence, thinks in quarters not sprints | Executes strategy given to them well | Focuses only on immediate tasks, no long-term view |

---

## Post-Interview Checklist

- [ ] Complete scorecard within 24 hours
- [ ] Note specific examples (not just impressions)
- [ ] Flag any concerns for hiring committee
- [ ] Avoid discussing with other interviewers before independent scoring
```

## Tips

- Ask the same core questions to every candidate for fair comparison
- Use follow-up probes to get past rehearsed answers
- Listen for specific examples with measurable results, not hypotheticals
- Take notes on exact quotes - they're more useful than your interpretations
- Leave time for candidate questions - how they ask reveals a lot

## Related Prompts

- [job-description-writer](./job-description-writer.md) - For creating the job posting
- [performance-review](./performance-review.md) - For evaluating employees post-hire
- [onboarding-checklist-creator](./onboarding-checklist-creator.md) - For successful new hire starts
