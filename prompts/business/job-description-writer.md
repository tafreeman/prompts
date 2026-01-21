---
name: Job Description Writer
description: Generate compelling, inclusive job descriptions that attract qualified candidates while accurately representing role requirements.
type: how_to
---

# Job Description Writer

## Description

This prompt generates compelling, inclusive job descriptions that attract qualified candidates while accurately representing role requirements. It helps recruiters and hiring managers create job postings that stand out in competitive talent markets.

## Use Cases

- Writing new job postings for open roles
- Refreshing outdated job descriptions
- Creating consistent JD templates across the organization
- Adapting job descriptions for different job boards
- Ensuring inclusive language in recruiting materials

## Variables

- `[role_title]`: Job title (e.g., "Senior Software Engineer", "Product Manager")
- `[company_info]`: Company name and brief description (e.g., "TechCorp – Series B fintech startup")
- `[team_info]`: Team context (e.g., "Platform Engineering team of 8")
- `[level]`: Seniority level (e.g., "Senior / L5", "Staff / L6")
- `[location]`: Work location (e.g., "Remote (US)", "Hybrid – NYC/SF")
- `[salary]`: Compensation range (e.g., "$150K-$180K base + equity")

## Prompt

### System Prompt

```text
You are an expert talent acquisition specialist who writes job descriptions that attract top talent. You balance accurate role requirements with compelling employer branding. You use inclusive language and focus on what candidates will achieve, not just what they'll do.
```

### User Prompt

```text
Write a job description for the following role:

Role Details:
- Title: [role_title]
- Company: [company_info]
- Team: [team_info]
- Level: [level]
- Location: [location]
- Compensation: [salary]

Please provide:
1. Compelling opening that sells the opportunity
2. About the company section (culture + mission)
3. Role overview and impact
4. Must-have and nice-to-have requirements
5. What we offer (benefits, growth, culture)
6. Clear application instructions
```

## Example

### Input

```text
Write a job description for the following role:

Role Details:
- Title: Senior Software Engineer
- Company: TechCorp – Series B fintech startup
- Team: Platform Engineering team of 8
- Level: Senior / L5
- Location: Remote (US)
- Compensation: $150K-$180K base + equity
```

### Expected Output

```text
# Senior Software Engineer, Platform

## Build the infrastructure that powers modern finance

We're looking for a Senior Software Engineer to join our Platform team and help us scale the systems that process millions of transactions daily. If you love solving hard distributed systems problems and want to see your work directly impact a growing fintech, this is your role.

## About TechCorp

TechCorp is building the future of B2B payments. We make it radically simple for businesses to send, receive, and manage payments. We're a Series B company backed by top-tier investors, with $50M raised and strong product-market fit.

**Why people love working here:**
- Real ownership: Ship to production in your first week
- Technical excellence: We invest in developer experience
- Growth stage: Big enough to have impact, small enough to shape culture

## What You'll Do

- Design and build scalable backend services handling 10K+ TPS
- Lead technical projects from architecture to deployment
- Mentor engineers and elevate team capabilities
- Partner with Product to shape our technical roadmap

## What We're Looking For

**Must-Have:**
- 5+ years backend engineering experience
- Strong distributed systems fundamentals
- Proficiency in Go, Python, or similar languages
- Track record shipping and operating production systems

**Nice-to-Have:**
- Fintech or payments experience
- Familiarity with compliance (PCI-DSS, SOC 2)

## Compensation & Benefits

- **Salary**: $150K-$180K base
- **Equity**: Meaningful ownership stake
- **Benefits**: Full health coverage, unlimited PTO, 401k match
- **Remote**: Work from anywhere in the US

## How to Apply

Send your resume and a brief note on why this role interests you. We respond within 5 business days.
```

## About FinFlow

FinFlow is building the future of B2B payments. We make it radically simple for businesses to send, receive, and manage payments—replacing the chaos of checks, ACH delays, and manual reconciliation with modern infrastructure.

We're a Series B company backed by Stripe, a]16z, and Ribbit Capital, with $50M raised and strong product-market fit (3x revenue growth last year). Our 80-person team is engineering-driven—we believe great products come from empowered engineers who own problems end-to-end.

**Why people love working here:**

- Real ownership: Engineers ship features to production in their first week
- Technical excellence: We invest heavily in developer experience and system reliability
- Growth stage: Big enough to have impact, small enough to shape the culture

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

## Related Prompts

- [interview-questions](./interview-questions.md) - For interview question preparation
- [performance-review](./performance-review.md) - For ongoing performance management
- [onboarding-checklist-creator](./onboarding-checklist-creator.md) - For new hire onboarding
