---
title: "Job Description Writer"
shortTitle: "Job Description"
intro: "Generate compelling, inclusive job descriptions that attract qualified candidates while accurately representing role requirements."
type: "how_to"
difficulty: "beginner"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "hr"
  - "recruiting"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Job Description Writer

---

## Description

Create job descriptions that attract top talent while being clear, inclusive, and accurate. Generates structured postings with compelling company pitches, clear requirements, and inclusive language.

---

## Use Cases

- Writing new job postings for open roles
- Refreshing outdated job descriptions
- Creating consistent JD templates across the organization
- Adapting job descriptions for different job boards
- Ensuring inclusive language in recruiting materials

---

## Prompt

```text
You are an expert talent acquisition specialist who writes job descriptions that attract top candidates.

Create a job description for:

**Role**: [role_title]
**Company**: [company_info]
**Team**: [team_info]
**Level**: [level]
**Location**: [location]
**Salary Range**: [salary]

Generate a complete job description with:

1. **Compelling Opening** (2-3 sentences)
   - Hook that excites candidates
   - Why this role matters

2. **About the Company** (3-4 sentences)
   - Mission and impact
   - Culture highlights
   - Why people love working here

3. **About the Role** (4-5 bullets)
   - Key responsibilities (action-oriented)
   - What you'll own
   - Who you'll work with

4. **Requirements** (Split clearly)
   - Must-have (3-5 items, truly required)
   - Nice-to-have (3-4 items, bonus qualifications)

5. **What We Offer** (5-6 bullets)
   - Compensation and equity
   - Benefits highlights
   - Growth opportunities

6. **How to Apply**
   - Clear next steps
   - What to include

Use inclusive language. Avoid gendered terms and unnecessary requirements. Focus on outcomes over years of experience.
```text

---

## Variables

- `[role_title]`: Job title (e.g., "Senior Software Engineer", "Product Marketing Manager")
- `[company_info]`: Company name, industry, stage, mission
- `[team_info]`: Which team this role is on, team size, who they report to
- `[level]`: Seniority level and scope (e.g., "Individual contributor", "People manager of 5")
- `[location]`: Work location (remote, hybrid, on-site, specific office)
- `[salary]`: Compensation range and any equity/bonus information

---

## Example Usage

**Input:**

```text
Role: Senior Backend Engineer
Company: FinFlow - Series B fintech startup ($50M raised), building the future of B2B payments infrastructure. 80 employees, engineering-driven culture.
Team: Platform team (8 engineers), reporting to VP of Engineering. Owns core payment processing infrastructure.
Level: Senior IC (L5), no direct reports but expected to mentor junior engineers
Location: Remote-first (US timezones), optional SF office access
Salary Range: $180K-$220K base + 0.1-0.2% equity + annual bonus
```text

**Output:**

```markdown
# Senior Backend Engineer, Platform

## The Opportunity

We're looking for a Senior Backend Engineer to help build the payment infrastructure that powers thousands of businesses. You'll work on systems that process billions of dollars and directly shape the technical foundation of FinFlow. If you want your code to have real-world impact at scale, this is it.

---

## About FinFlow

FinFlow is building the future of B2B payments. We make it radically simple for businesses to send, receive, and manage payments—replacing the chaos of checks, ACH delays, and manual reconciliation with modern infrastructure.

We're a Series B company backed by Stripe, a]16z, and Ribbit Capital, with $50M raised and strong product-market fit (3x revenue growth last year). Our 80-person team is engineering-driven—we believe great products come from empowered engineers who own problems end-to-end.

**Why people love working here:**
- Real ownership: Engineers ship features to production in their first week
- Technical excellence: We invest heavily in developer experience and system reliability
- Growth stage: Big enough to have impact, small enough to shape the culture

---

## About the Role

As a Senior Backend Engineer on our Platform team, you'll own critical payment processing infrastructure that handles real money for real businesses.

**What you'll do:**
- Design, build, and scale backend systems processing $2B+ in monthly payment volume
- Own the reliability and performance of our core payment APIs (current target: 99.99% uptime)
- Lead technical initiatives from design through implementation—you'll write RFCs, get buy-in, and ship
- Collaborate with product and infrastructure teams to define platform capabilities
- Mentor engineers across the team through code reviews, pairing, and technical guidance

**You'll work with:**
- A Platform team of 8 engineers building distributed systems in Go and Python
- Our Infrastructure team on Kubernetes, AWS, and observability tooling
- Product engineers who depend on your APIs to build customer-facing features

---

## What We're Looking For

### Must-Have
- Strong backend engineering fundamentals—you can design systems that are reliable, scalable, and maintainable
- Experience with distributed systems (event-driven architectures, message queues, eventual consistency)
- Proficiency in Go, Python, or similar languages (we use Go primarily)
- Track record of shipping and operating production systems at scale
- Clear communication—you can explain complex technical concepts to engineers and non-engineers alike

### Nice-to-Have
- Experience in payments, fintech, or financial infrastructure
- Familiarity with compliance requirements (PCI-DSS, SOC 2)
- Background in platform/infrastructure engineering
- Experience mentoring or leading technical projects

*Note: We care about what you can do, not where you learned it. If you've built impressive things through non-traditional paths, we want to hear about it.*

---

## What We Offer

- **Compensation**: $180K-$220K base salary + 0.1-0.2% equity + annual performance bonus
- **Health**: Medical, dental, and vision coverage (we cover 100% of employee premiums)
- **Time Off**: Unlimited PTO with a 3-week minimum encouraged, plus company-wide recharge weeks
- **Remote-First**: Work from anywhere in US timezones; optional SF office for those who want it
- **Growth**: $2,500 annual learning budget + conference attendance + internal mobility
- **Equipment**: $2,000 home office stipend + top-tier laptop

---

## How to Apply

**Apply here**: [link]

**What to include:**
- Resume or LinkedIn profile
- Brief note on why this role interests you (2-3 sentences is fine)
- Optional: Link to GitHub, a project you're proud of, or writing you've done

**Our process:**
1. Application review (we respond within 5 business days)
2. 30-min recruiter screen
3. 60-min technical conversation with hiring manager
4. Virtual onsite (3 hours): system design + coding + team conversations
5. Offer + references

*FinFlow is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees. We do not discriminate based on race, religion, color, national origin, gender, sexual orientation, age, marital status, veteran status, or disability status.*
```text

---

## Tips

- Lead with impact, not requirements - candidates want to know why the role matters
- Split must-have vs. nice-to-have clearly - research shows women apply only if they meet 100% of requirements
- Avoid "rockstar/ninja/guru" language - it signals exclusionary culture
- Include salary range - transparency attracts more qualified candidates
- Keep it scannable - use bullets and clear headers for quick reading

---

## Related Prompts

- [interview-questions](./interview-questions.md) - For interview question preparation
- [performance-review](./performance-review.md) - For ongoing performance management
- [onboarding-checklist-creator](./onboarding-checklist-creator.md) - For new hire onboarding
