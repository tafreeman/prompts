---
name: Interview Questions Generator
description: Generate structured, behavioral interview questions tailored to specific roles, levels, and competencies.
type: how_to
---
## Description

## Prompt

```text
You are an expert interviewer and talent assessment specialist. You create structured behavioral interview guides that help organizations identify top talent while ensuring fair, consistent evaluation. You understand STAR methodology and competency-based interviewing.
```

Generate structured, behavioral interview questions tailored to specific roles, levels, and competencies.

## Description

## Prompt

```text
You are an expert interviewer and talent assessment specialist. You create structured behavioral interview guides that help organizations identify top talent while ensuring fair, consistent evaluation. You understand STAR methodology and competency-based interviewing.
```

Generate structured, behavioral interview questions tailored to specific roles, levels, and competencies.


# Interview Questions Generator

## Description

This prompt generates structured, behavioral interview questions tailored to specific roles, levels, and competencies. It helps hiring managers create consistent, effective interview guides that assess candidates fairly and thoroughly.

## Use Cases

- Preparing for candidate interviews
- Building standardized interview guides for roles
- Training new interviewers on behavioral interviewing
- Ensuring consistent evaluation across candidates
- Creating competency-based assessment frameworks

## Variables

- `[role]`: Job title (e.g., "Senior Product Manager")
- `[level]`: Seniority level (e.g., "Senior / IC5")
- `[competencies]`: Key competencies to assess (e.g., "Strategic thinking, stakeholder management, data-driven decision making, technical acumen")
- `[stage]`: Interview stage (e.g., "Hiring manager round", "Final panel")
- `[time]`: Available time (e.g., "45 minutes")

## Prompt

### System Prompt

```text
You are an expert interviewer and talent assessment specialist. You create structured behavioral interview guides that help organizations identify top talent while ensuring fair, consistent evaluation. You understand STAR methodology and competency-based interviewing.
```

### User Prompt

```text
Create an interview guide for the following role:

Role Details:
- Position: [role]
- Level: [level]
- Key Competencies: [competencies]
- Interview Stage: [stage]
- Available Time: [time]

Please provide:
1. Interview structure with time allocation
2. Behavioral questions for each competency with follow-up probes
3. STAR expectations for strong answers
4. Situational/case questions relevant to the role
5. Scoring rubric with examples of strong/weak answers
6. Red flags to watch for
```

## Example

### Input

```text
Create an interview guide for the following role:

Role Details:
- Position: Senior Product Manager
- Level: Senior / IC5
- Key Competencies: Strategic thinking, stakeholder management, data-driven decision making, technical acumen
- Interview Stage: Hiring manager round
- Available Time: 45 minutes
```

### Expected Output

```text
## Interview Guide: Senior Product Manager (IC5)

### Interview Structure (45 minutes)
| Section | Time | Focus |
|---------|------|-------|
| Opening | 5 min | Rapport, role overview |
| Behavioral | 25 min | Core competencies (3 questions) |
| Situational | 10 min | Case scenario |
| Q&A | 5 min | Candidate questions |

### Behavioral Question 1: Strategic Thinking
**Question**: "Tell me about a time you identified a product opportunity that wasn't on anyone's roadmap. How did you build the case for it?"

**Follow-up Probes**:
- "How big was the opportunity vs. current priorities?"
- "What data did you use to size the opportunity?"
- "How did you get stakeholder buy-in?"

**Strong Answer (STAR)**:
- **Situation**: Clear business context with quantified stakes
- **Task**: Specific ownership and initiative taken
- **Action**: Data-driven approach, stakeholder management
- **Result**: Measurable outcome (revenue, adoption, etc.)

### Situational Question: Prioritization
**Scenario**: "You have 3 features requested by: (1) your largest customer threatening to churn, (2) sales team for competitive deals, (3) engineering to pay down tech debt. You can only do one this quarter. Walk me through your decision."

**What to Assess**:
- Framework for prioritization (impact vs. effort, strategic alignment)
- How they balance stakeholder needs
- Willingness to make hard trade-offs

### Scoring Rubric
| Competency | Strong (4-5) | Concerning (1-2) |
|------------|--------------|------------------|
| Strategic Thinking | Quantifies opportunities, thinks in quarters not sprints | Focuses only on immediate tasks |
| Data-Driven | Cites specific metrics, acknowledges limitations | Relies on intuition |

### Red Flags
- Can't give specific examples (only hypotheticals)
- Blames others for failures
- No questions about the product or team
```

## Interview Structure

| Section | Time | Focus |
| --------- | ------ | ------- |
| Opening | 5 min | Rapport, background |
| Behavioral | 25 min | Core competencies |
| Situational | 15 min | Judgment, approach |
| Role-Specific | 10 min | Growth PM skills |
| Candidate Q&A | 5 min | Their questions |

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

### Scenario 2: Experiment Design

*"You're tasked with improving our onboarding flow. Activation rate is 34% (new users who complete setup within 7 days). You have 4 weeks and one engineer. Walk me through how you'd approach this."*

**What to assess**:

- Structured thinking (diagnose before prescribe)
- Experimentation rigor
- Scrappiness within constraints

**Great answer includes**: Starts with data/funnel analysis, talks to churned users, prioritizes highest-leverage tests, acknowledges what they'd do with more resources

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

## 6. Scoring Rubric

| Competency | Strong (4-5) | Adequate (3) | Concerning (1-2) |
| ------------ | -------------- | -------------- | ------------------ |
| **Data-Driven** | Cites specific metrics, acknowledges data limitations, makes probabilistic decisions | Uses data but can't explain methodology deeply | Relies on intuition, can't articulate how they'd measure success |
| **Cross-Functional** | Concrete examples of building consensus, shows empathy for other teams | Has collaborated but waited for decisions to come to them | Blames other teams, sees alignment as someone else's job |
| **Experimentation** | Can design rigorous experiments, embraces failures, iterates based on learnings | Has run experiments but didn't own the analysis | Hasn't run real experiments or sees them as "nice to have" |
| **Customer Empathy** | Direct customer contact, synthesizes qual + quant, changed their own mind | Reads user research but doesn't conduct it | Views customers as abstract personas, not real people |
| **Strategic** | Identifies opportunities independently, can size and sequence, thinks in quarters not sprints | Executes strategy given to them well | Focuses only on immediate tasks, no long-term view |

## Tips

- Ask the same core questions to every candidate for fair comparison
- Use follow-up probes to get past rehearsed answers
- Listen for specific examples with measurable results, not hypotheticals
- Take notes on exact quotes - they're more useful than your interpretations
- Leave time for candidate questions - how they ask reveals a lot

---

## Related Prompts

- [job-description-writer](./job-description-writer.md) - For creating the job posting
- [performance-review](./performance-review.md) - For evaluating employees post-hire
- [onboarding-checklist-creator](./onboarding-checklist-creator.md) - For successful new hire starts## Variables

_No bracketed variables detected._

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
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[competencies]` | AUTO-GENERATED: describe `competencies` |
| `[job-description-writer]` | AUTO-GENERATED: describe `job-description-writer` |
| `[level]` | AUTO-GENERATED: describe `level` |
| `[onboarding-checklist-creator]` | AUTO-GENERATED: describe `onboarding-checklist-creator` |
| `[performance-review]` | AUTO-GENERATED: describe `performance-review` |
| `[role]` | AUTO-GENERATED: describe `role` |
| `[stage]` | AUTO-GENERATED: describe `stage` |
| `[time]` | AUTO-GENERATED: describe `time` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

