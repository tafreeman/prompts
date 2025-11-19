# Enterprise SDLC Workflow Blueprint

**Version**: 1.0  
**Last Updated**: 2025-01-26  
**Methodology**: Agile + DevOps Hybrid  
**Target Audience**: Enterprise development teams (5-50+ engineers)

---

## Overview

This blueprint provides an end-to-end Software Development Lifecycle (SDLC) workflow that chains prompts from the repository for enterprise teams. It combines Agile sprint structure with DevOps automation to balance flexibility, speed, and quality.

### Methodology Selection Framework

```text
┌─────────────────────────────────────────────────────────────────┐
│ Choose Your SDLC Approach                                       │
├─────────────────────────────────────────────────────────────────┤
│ ✓ Use this blueprint IF:                                        │
│   • Team practices Agile/Scrum (2-4 week sprints)              │
│   • Requirements evolve during development                      │
│   • Need fast feedback loops (every sprint)                    │
│   • Have or building CI/CD infrastructure                      │
│                                                                 │
│ ✗ Consider alternative IF:                                     │
│   • Fixed scope + budget + timeline (Waterfall)                │
│   • Extremely stable requirements (Waterfall)                  │
│   • No infrastructure for automation (Manual Waterfall)        │
└─────────────────────────────────────────────────────────────────┘
```

---

## SDLC Phases & Prompt Chain

### Phase 0: Pre-Sprint Planning (Before Sprint Kickoff)

**Objective**: Establish project foundation and backlog

**Duration**: 1-3 days (one-time setup per project)

**Prompts to Use**:

1. **[business-case-developer](../../prompts/analysis/business-case-developer.md)** - Validate project ROI and strategic alignment
2. **[stakeholder-requirements-gatherer](../../prompts/analysis/stakeholder-requirements-gatherer.md)** - Identify all stakeholders and their needs
3. **[requirements-analysis-expert](../../prompts/analysis/requirements-analysis-expert.md)** - Translate business needs into functional/non-functional requirements
4. **[solution-architecture-designer](../../prompts/developers/solution-architecture-designer.md)** - Create high-level architecture and technology stack decisions

**Deliverables**:

- Business case document with success metrics
- Stakeholder map and communication plan
- Requirements backlog (prioritized using MoSCoW or story points)
- Architecture decision record (ADR) with technology choices

**Decision Point**: Proceed to Sprint 1 if:

- ✓ Business case approved
- ✓ Minimum 2-3 sprints of backlog ready
- ✓ Architecture reviewed by technical leadership

---

### Phase 1: Sprint Planning (Start of Each Sprint)

**Objective**: Select user stories, define sprint goal, estimate capacity

**Duration**: 4 hours (every 2 weeks for standard sprints)

**Prompts to Use**:

1. **[agile-sprint-planner](../../prompts/business/agile-sprint-planner.md)** - Facilitate sprint planning ceremony
2. **[requirements-analysis-expert](../../prompts/analysis/requirements-analysis-expert.md)** - Refine user stories with acceptance criteria
3. **[metrics-and-kpi-designer](../../prompts/analysis/metrics-and-kpi-designer.md)** - Define sprint success metrics (velocity, quality gates)

**Workflow**:

```text
1. Review previous sprint (velocity, completed stories, blockers)
2. Product Owner presents prioritized backlog
3. Team estimates stories (planning poker or t-shirt sizing)
4. Commit to sprint goal and stories (based on team capacity)
5. Define Definition of Done (DoD) for each story
6. Identify dependencies and risks
```

**Deliverables**:

- Sprint backlog (user stories with story points)
- Sprint goal statement (1-2 sentences)
- Team capacity plan (accounting for PTO, holidays)
- Risk register (blockers, dependencies, assumptions)

**Example User Story Format** (use requirements-analysis-expert):

```text
As a [persona]
I want [functionality]
So that [business value]

Acceptance Criteria:
- [ ] Criterion 1 with measurable outcome
- [ ] Criterion 2 with measurable outcome
- [ ] Non-functional requirement (e.g., response time < 2s)

Story Points: [1, 2, 3, 5, 8, 13]
Priority: [High / Medium / Low]
Dependencies: [List any blocking stories or external dependencies]
```

---

### Phase 2: Design & Architecture (First 2 Days of Sprint)

**Objective**: Detail technical design for sprint stories

**Duration**: 2 days (parallelized across team members)

**Prompts to Use**:

1. **[solution-architecture-designer](../../prompts/developers/solution-architecture-designer.md)** - Design system components and interactions
2. **[api-design-consultant](../../prompts/developers/api-design-consultant.md)** - Define API contracts (RESTful or GraphQL endpoints)
3. **[database-schema-designer](../../prompts/developers/database-schema-designer.md)** - Design database tables, relationships, indexes
4. **[security-code-auditor](../../prompts/governance-compliance/security-code-auditor.md)** - Identify security requirements early (authentication, authorization, data protection)

**Workflow**:

```text
1. Technical lead assigns design tasks to engineers
2. Each engineer uses prompts to generate design artifacts
3. Peer review of designs (1-hour design review meeting)
4. Update architecture decision records (ADRs) if needed
5. Commit finalized designs to repository (docs/ folder)
```

**Deliverables**:

- Component diagrams (C4 model: Context → Container → Component)
- API specifications (OpenAPI/Swagger or GraphQL schema)
- Database schema with migrations
- Security checklist (OWASP Top 10 considerations)
- Architecture Decision Records (ADRs) for non-trivial choices

**DevOps Integration**:

- Store design artifacts in Git repository (version controlled)
- Link designs to user stories in project management tool (Jira, Azure DevOps)
- Automated diagram generation from code (e.g., PlantUML, Mermaid)

---

### Phase 3: Development & Implementation (Days 3-8 of Sprint)

**Objective**: Write code, implement features, commit frequently

**Duration**: 6 days (60% of sprint time)

**Prompts to Use**:

1. **[code-generation-assistant](../../prompts/developers/code-generation-assistant.md)** - Generate boilerplate code, functions, classes
2. **[api-design-consultant](../../prompts/developers/api-design-consultant.md)** - Implement API endpoints with validation
3. **[database-schema-designer](../../prompts/developers/database-schema-designer.md)** - Write database queries, ORM models, migrations
4. **[documentation-generator](../../prompts/developers/documentation-generator.md)** - Generate inline comments, README updates, API docs
5. **[refactoring-specialist](../../prompts/developers/refactoring-specialist.md)** - Clean up code, reduce technical debt

**Workflow**:

```text
1. Create feature branch from main/develop branch (Git Flow)
2. Implement user story following design specifications
3. Write unit tests alongside code (TDD: Test-Driven Development)
4. Commit frequently with descriptive messages (Conventional Commits format)
5. Push to remote branch daily (enables CI/CD pipeline)
6. Update story status in project management tool (In Progress → Review)
```

**DevOps Integration (CI/CD Pipeline Triggers)**:

```yaml
# Example GitHub Actions / Azure Pipelines workflow
on:
  push:
    branches: [feature/*, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - Checkout code
      - Install dependencies
      - Run linters (ESLint, Pylint, etc.)
      - Run unit tests (Jest, pytest, etc.)
      - Run security scans (Snyk, Dependabot)
      - Generate test coverage report
      - Build artifacts (Docker image, binaries, etc.)
```

**Prompts for CI/CD Setup**:

1. **[devops-pipeline-architect](../../prompts/system/devops-pipeline-architect.md)** - Design CI/CD pipeline stages
2. **[test-automation-engineer](../../prompts/developers/test-automation-engineer.md)** - Write automated tests

**Deliverables**:

- Feature code with 80%+ test coverage
- Unit tests and integration tests
- Updated documentation (README, API docs)
- Green CI/CD pipeline (all checks passing)

---

### Phase 4: Code Review & Quality Assurance (Days 8-9 of Sprint)

**Objective**: Peer review code, ensure quality standards

**Duration**: 2 days (overlaps with late development)

**Prompts to Use**:

1. **[code-review-expert](../../prompts/developers/code-review-expert.md)** - Conduct thorough peer reviews
2. **[security-code-auditor](../../prompts/governance-compliance/security-code-auditor.md)** - Audit code for vulnerabilities
3. **[performance-optimization-specialist](../../prompts/developers/performance-optimization-specialist.md)** - Identify performance bottlenecks
4. **[refactoring-specialist](../../prompts/developers/refactoring-specialist.md)** - Suggest improvements for maintainability

**Workflow**:

```text
1. Engineer opens Pull Request (PR) / Merge Request (MR)
2. Automated checks run (CI/CD pipeline, code coverage, linting)
3. Assign 1-2 peer reviewers (rotating to spread knowledge)
4. Reviewers use prompts to conduct structured review:
   - Functionality: Does code meet acceptance criteria?
   - Security: Any OWASP Top 10 vulnerabilities?
   - Performance: Any inefficient queries or algorithms?
   - Maintainability: Is code readable and well-documented?
   - Tests: Are edge cases covered?
5. Reviewer leaves comments in PR with specific line references
6. Engineer addresses feedback, pushes updates
7. Reviewer approves PR (requires 1-2 approvals depending on policy)
8. Engineer merges to develop branch (squash or merge commit)
```

**Quality Gates** (must pass before merge):

- ✓ All automated tests passing (unit, integration, E2E)
- ✓ Code coverage ≥ 80% for new code
- ✓ No high/critical security vulnerabilities (Snyk, SonarQube)
- ✓ No linting errors (ESLint, Pylint, etc.)
- ✓ At least 1 peer approval (2 for critical paths)
- ✓ Acceptance criteria met (verified by Product Owner or QA)

**Deliverables**:

- Approved and merged Pull Request
- Code review comments and resolution log
- Updated test suite with passing results
- Security scan report (no high/critical issues)

---

### Phase 5: Testing & Validation (Days 9-10 of Sprint)

**Objective**: End-to-end testing, integration testing, acceptance testing

**Duration**: 2 days (can overlap with code review)

**Prompts to Use**:

1. **[test-automation-engineer](../../prompts/developers/test-automation-engineer.md)** - Create automated test suites
2. **[user-experience-analyst](../../prompts/analysis/user-experience-analyst.md)** - Validate user workflows and usability
3. **[performance-optimization-specialist](../../prompts/developers/performance-optimization-specialist.md)** - Run load tests and benchmarks

**Workflow**:

```text
1. QA Engineer writes/updates end-to-end (E2E) test scenarios
2. Run automated E2E tests (Selenium, Cypress, Playwright, etc.)
3. Perform exploratory testing (manual testing for edge cases)
4. Load testing for performance-critical features (JMeter, k6, Locust)
5. Accessibility testing (WCAG 2.1 AA compliance using axe, Lighthouse)
6. User Acceptance Testing (UAT) with Product Owner or stakeholders
7. Log defects in backlog (prioritize for current sprint or next sprint)
```

**Testing Layers**:

```text
┌─────────────────────────────────────────────────────────────┐
│ E2E Tests (GUI, User Workflows) - Slowest, Most Realistic  │
├─────────────────────────────────────────────────────────────┤
│ Integration Tests (API, Database, Services) - Medium Speed │
├─────────────────────────────────────────────────────────────┤
│ Unit Tests (Functions, Classes) - Fastest, Most Coverage   │
└─────────────────────────────────────────────────────────────┘
```

**Deliverables**:

- E2E test suite with passing results
- Performance test report (response times, throughput, error rates)
- Accessibility audit report (WCAG compliance)
- UAT sign-off from Product Owner
- Defect log (if any critical bugs found)

**Decision Point**: Proceed to deployment if:

- ✓ All E2E tests passing
- ✓ No critical or high-priority bugs
- ✓ Performance benchmarks met (e.g., API response time < 500ms p95)
- ✓ Product Owner approved UAT

---

### Phase 6: Deployment & Release (End of Sprint)

**Objective**: Deploy to staging/production, monitor rollout

**Duration**: 1 day (typically last day of sprint or start of next sprint)

**Prompts to Use**:

1. **[devops-pipeline-architect](../../prompts/system/devops-pipeline-architect.md)** - Orchestrate deployment pipeline
2. **[cloud-architecture-consultant](../../prompts/developers/cloud-architecture-consultant.md)** - Optimize cloud resources (AWS, Azure, GCP)
3. **[database-migration-specialist](../../prompts/developers/database-migration-specialist.md)** - Execute database migrations safely

**Workflow**:

```text
1. Merge develop branch to release branch (Git Flow)
2. Tag release version (Semantic Versioning: v1.2.3)
3. Deploy to staging environment (automated via CI/CD)
4. Run smoke tests on staging (quick validation of critical paths)
5. Product Owner approves staging environment
6. Deploy to production (automated with rollback capability)
   - Blue-green deployment or canary release (gradual rollout)
7. Monitor production deployment for 30-60 minutes
   - Application logs (errors, warnings)
   - Performance metrics (latency, throughput)
   - User analytics (active users, error rates)
8. If issues detected, rollback to previous version
9. If stable, mark deployment as successful
```

**Deployment Strategies**:

- **Blue-Green**: Deploy to new environment (green), switch traffic from old (blue)
- **Canary**: Gradually roll out to 5% → 25% → 50% → 100% of users
- **Rolling**: Update instances one-by-one with health checks

**DevOps Automation** (example tools):

- **CI/CD**: GitHub Actions, GitLab CI, Jenkins, Azure Pipelines, CircleCI
- **Infrastructure as Code**: Terraform, Pulumi, AWS CloudFormation, Azure ARM templates
- **Container Orchestration**: Kubernetes, Docker Swarm, AWS ECS
- **Monitoring**: Prometheus, Grafana, Datadog, New Relic, Azure Monitor

**Deliverables**:

- Deployed application to production
- Release notes (changelog with new features, bug fixes)
- Rollback plan documented (in case of issues)
- Monitoring dashboards configured (uptime, latency, errors)

---

### Phase 7: Monitoring & Observability (Continuous Post-Deployment)

**Objective**: Monitor production health, gather feedback, plan next sprint

**Duration**: Continuous (throughout sprint and post-deployment)

**Prompts to Use**:

1. **[metrics-and-kpi-designer](../../prompts/analysis/metrics-and-kpi-designer.md)** - Define success metrics and alerts
2. **[data-analysis-insights](../../prompts/analysis/data-analysis-insights.md)** - Analyze user behavior and system performance
3. **[incident-response-coordinator](../../prompts/governance-compliance/security-incident-response.md)** - Handle production incidents (see [Incident Response Playbook](./incident-response-playbook.md))

**Workflow**:

```text
1. Configure monitoring dashboards (real-time and historical)
2. Set up alerting rules (e.g., error rate > 1%, latency p95 > 2s)
3. Monitor production logs for errors and warnings
4. Collect user feedback (surveys, support tickets, analytics)
5. Weekly production review meeting:
   - Review uptime and performance metrics
   - Discuss user feedback and feature requests
   - Prioritize bug fixes for next sprint
6. Update backlog based on production insights
```

**Key Metrics to Monitor** (Four Golden Signals):

1. **Latency**: Response time (p50, p95, p99 percentiles)
2. **Traffic**: Requests per second, active users
3. **Errors**: Error rate (%), 4xx/5xx HTTP status codes
4. **Saturation**: CPU usage, memory usage, disk I/O, network bandwidth

**Observability Stack** (example):

- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, Datadog
- **Metrics**: Prometheus + Grafana, CloudWatch, Azure Monitor
- **Traces**: Jaeger, Zipkin, OpenTelemetry, AWS X-Ray
- **Alerts**: PagerDuty, Opsgenie, Slack integrations

**Deliverables**:

- Monitoring dashboards with SLA tracking
- Weekly production health report
- User feedback summary (feature requests, pain points)
- Incident log (if any outages or degradations occurred)

---

### Phase 8: Sprint Review & Retrospective (End of Sprint)

**Objective**: Demo completed work, gather feedback, improve process

**Duration**: 3 hours (last day of sprint)

**Prompts to Use**:

1. **[meeting-facilitator](../../prompts/business/meeting-facilitator.md)** - Run effective retrospectives
2. **[process-optimization-consultant](../../prompts/analysis/process-optimization-consultant.md)** - Identify process improvements

**Workflow - Sprint Review (1 hour)**:

```text
1. Product Owner introduces sprint goal and completed stories
2. Engineers demo new features (live in staging or production)
3. Stakeholders provide feedback (feature requests, usability issues)
4. Product Owner accepts or rejects user stories based on DoD
5. Update product backlog with new insights
```

**Workflow - Retrospective (1-2 hours)**:

```text
1. Facilitator sets ground rules (blameless, constructive)
2. Team reflects on sprint using framework (e.g., Start/Stop/Continue or 4Ls)
3. Identify 3 things that went well (celebrate wins)
4. Identify 3 things to improve (process, tools, communication)
5. Create 1-3 action items for next sprint (assign owners)
6. Document retrospective outcomes in shared wiki
```

**Retrospective Frameworks**:

- **Start/Stop/Continue**: What should we start doing? Stop doing? Continue doing?
- **4Ls**: What did we Love? What did we Learn? What did we Lack? What do we Long for?
- **Mad/Sad/Glad**: Categorize experiences by emotion

**Deliverables**:

- Sprint demo recordings (for stakeholders who couldn't attend)
- Stakeholder feedback log
- Retrospective action items (tracked in next sprint)
- Updated team working agreements (if process changes agreed)

---

## Real-World Example Walkthrough

### Scenario: E-Commerce Platform - Adding "Gift Card Purchase" Feature

**Context**:

- Team: 8 engineers (3 backend, 3 frontend, 1 DevOps, 1 QA)
- Sprint Duration: 2 weeks
- Tech Stack: React (frontend), Node.js (backend), PostgreSQL (database), AWS (cloud)
- Deployed: Production with 10,000 daily active users

---

#### Phase 0: Pre-Sprint Planning

1. **Business Case** (use business-case-developer):
   - Prompt: "Analyze the ROI of adding gift card functionality to our e-commerce platform. Consider revenue increase, development cost ($50k estimated), and market demand."
   - Output: Business case shows 15% revenue increase, 6-month payback period, approved by leadership

2. **Stakeholder Requirements** (use stakeholder-requirements-gatherer):
   - Prompt: "Identify stakeholders for gift card feature: customers, marketing, finance, compliance, engineering."
   - Output: Stakeholder map with communication plan (weekly updates to marketing, compliance review before launch)

3. **Requirements** (use requirements-analysis-expert):
   - Prompt: "Define functional and non-functional requirements for gift card purchase feature. Include purchase flow, redemption, balance checking, and compliance (no expiration per state laws)."
   - Output: 12 user stories created and prioritized in backlog

4. **Architecture** (use solution-architecture-designer):
   - Prompt: "Design architecture for gift card system. Consider database schema (gift_cards table), API endpoints (POST /gift-cards, GET /gift-cards/:id), and third-party payment integration (Stripe)."
   - Output: C4 diagrams, ADR to use Stripe for payment processing

---

#### Phase 1: Sprint Planning (Sprint 5)

1. **Sprint Planning** (use agile-sprint-planner):
   - Prompt: "Plan Sprint 5 with team capacity of 80 story points (8 engineers × 10 points each). Prioritize: 1) Gift card purchase API (13 pts), 2) Frontend purchase form (8 pts), 3) Gift card balance check (5 pts), 4) Database migrations (5 pts), 5) Admin dashboard for gift card management (8 pts). Total: 39 points (conservative for complex feature)."
   - Output: Sprint backlog with 5 user stories, sprint goal: "Enable customers to purchase and check balance of gift cards"

2. **Story Refinement** (use requirements-analysis-expert):
   - Prompt: "Refine user story: 'As a customer, I want to purchase a gift card with custom amount ($25-$500) so that I can give it as a gift.' Add acceptance criteria."
   - Output:

     ```text
     Acceptance Criteria:
     - [ ] User can select gift card amount ($25, $50, $100, $250, $500, or custom)
     - [ ] User can enter recipient email and personal message (optional)
     - [ ] Payment processed via Stripe (PCI DSS compliant)
     - [ ] Unique gift card code generated (16-digit alphanumeric)
     - [ ] Confirmation email sent to purchaser and recipient
     - [ ] Gift card stored in database with balance and expiration (never expires per state law)
     - [ ] Response time < 3 seconds for purchase flow
     ```

---

#### Phase 2: Design & Architecture (Days 1-2)

1. **API Design** (use api-design-consultant):
   - Prompt: "Design RESTful API for gift card purchase: POST /api/v1/gift-cards. Request body: {amount: number, recipientEmail: string, message: string}. Response: {giftCardCode: string, balance: number, expiresAt: null}."
   - Output: OpenAPI spec with validation rules (amount >= 25 && amount <= 500)

2. **Database Schema** (use database-schema-designer):
   - Prompt: "Design PostgreSQL schema for gift cards. Fields: id (UUID), code (unique 16-char string), balance (decimal), initialAmount (decimal), purchaserEmail (string), recipientEmail (string), message (text), createdAt (timestamp), expiresAt (nullable timestamp, always null per state law). Index on code for fast lookups."
   - Output: Migration script with schema and indexes

3. **Security Review** (use security-code-auditor):
   - Prompt: "Audit gift card API for security risks. Consider: code generation (cryptographically secure random), SQL injection (use parameterized queries), rate limiting (prevent abuse), PCI compliance (never store credit card data, use Stripe tokens)."
   - Output: Security checklist with 8 requirements (all addressed in design)

---

#### Phase 3: Development (Days 3-8)

1. **Backend Implementation** (use code-generation-assistant):
   - Prompt: "Generate Node.js Express API endpoint for gift card purchase. Use Stripe SDK for payment, generate 16-digit code with crypto.randomBytes(), save to PostgreSQL with Knex ORM, send email with SendGrid."
   - Output:

     ```javascript
     // routes/giftCards.js
     const express = require('express');
     const router = express.Router();
     const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
     const crypto = require('crypto');
     const db = require('../db');
     const sendEmail = require('../services/email');

     router.post('/gift-cards', async (req, res) => {
       const { amount, recipientEmail, message, paymentMethodId } = req.body;

       // Validate amount
       if (amount < 25 || amount > 500) {
         return res.status(400).json({ error: 'Amount must be between $25 and $500' });
       }

       try {
         // Process payment via Stripe
         const paymentIntent = await stripe.paymentIntents.create({
           amount: amount * 100, // Convert to cents
           currency: 'usd',
           payment_method: paymentMethodId,
           confirm: true
         });

         // Generate unique gift card code
         const giftCardCode = crypto.randomBytes(8).toString('hex').toUpperCase();

         // Save to database
         const [giftCard] = await db('gift_cards').insert({
           code: giftCardCode,
           balance: amount,
           initialAmount: amount,
           purchaserEmail: req.user.email,
           recipientEmail,
           message,
           createdAt: new Date(),
           expiresAt: null // Never expires per state law
         }).returning('*');

         // Send confirmation emails
         await sendEmail({
           to: recipientEmail,
           subject: 'You received a gift card!',
           body: `You received a $${amount} gift card with code: ${giftCardCode}. Message: ${message}`
         });

         await sendEmail({
           to: req.user.email,
           subject: 'Gift card purchase confirmation',
           body: `Your gift card purchase of $${amount} was successful. Code: ${giftCardCode}`
         });

         res.status(201).json({
           giftCardCode: giftCard.code,
           balance: giftCard.balance,
           expiresAt: giftCard.expiresAt
         });
       } catch (error) {
         console.error('Gift card purchase error:', error);
         res.status(500).json({ error: 'Failed to process gift card purchase' });
       }
     });

     module.exports = router;
     ```

2. **Unit Tests** (use test-automation-engineer):
   - Prompt: "Write Jest unit tests for gift card API. Test cases: 1) successful purchase, 2) invalid amount (< $25 or > $500), 3) payment failure (Stripe error), 4) duplicate code generation (retry logic), 5) email sending failure."
   - Output: 15 unit tests with 90% code coverage

3. **Frontend Implementation** (use code-generation-assistant):
   - Prompt: "Generate React form component for gift card purchase. Fields: amount (dropdown + custom), recipient email (validation), message (textarea, optional). Use Stripe Elements for payment. Display success message with gift card code after purchase."
   - Output: `GiftCardPurchaseForm.jsx` component with form validation and Stripe integration

---

#### Phase 4: Code Review (Days 8-9)

1. **Peer Review** (use code-review-expert):
   - Prompt: "Review gift card purchase API code. Check: 1) Stripe payment handling (error cases), 2) gift card code uniqueness (collision handling), 3) SQL injection prevention (parameterized queries), 4) email failure handling (async queue), 5) rate limiting (10 purchases per user per hour)."
   - Output: 7 comments on PR:
     - ✓ Payment handling looks good
     - ⚠️ Add retry logic for email failures (comment resolved: engineer added Redis job queue)
     - ⚠️ Consider race condition for gift card code uniqueness (comment resolved: added unique constraint + retry)
     - ✓ SQL injection prevention confirmed (Knex ORM parameterizes queries)
     - ⚠️ Add rate limiting (comment resolved: engineer added express-rate-limit middleware)

2. **Security Audit** (use security-code-auditor):
   - Prompt: "Audit gift card code for OWASP Top 10 vulnerabilities. Check: 1) Broken Access Control (ensure user can't purchase gift cards on behalf of others), 2) Cryptographic Failures (gift card code must be cryptographically secure), 3) Injection (SQL, NoSQL, command), 4) Insecure Design (validate state law compliance: no expiration), 5) Security Misconfiguration (Stripe API keys in environment variables, not committed to Git)."
   - Output: No high/critical vulnerabilities found. Recommendation: Add logging for all gift card purchases (audit trail).

3. **PR Approved**: 2 engineers approved, PR merged to develop branch

---

#### Phase 5: Testing (Days 9-10)

1. **E2E Tests** (use test-automation-engineer):
   - Prompt: "Write Cypress E2E test for gift card purchase flow. Steps: 1) Navigate to gift card page, 2) Select $100 amount, 3) Enter recipient email and message, 4) Enter test credit card (Stripe test mode), 5) Submit form, 6) Verify success message with gift card code, 7) Check database for gift card record."
   - Output: Cypress test suite with 5 E2E scenarios (all passing)

2. **Load Testing** (use performance-optimization-specialist):
   - Prompt: "Run k6 load test for gift card purchase API. Simulate 100 concurrent users purchasing gift cards over 5 minutes. Measure: 1) Average response time, 2) p95 response time, 3) Error rate, 4) Throughput (requests/sec)."
   - Output: Load test results:
     - Average response time: 850ms
     - p95 response time: 1.8s (⚠️ slightly above target of 1.5s)
     - Error rate: 0.2%
     - Throughput: 45 requests/sec
     - Recommendation: Optimize Stripe payment call (cache Stripe client, use connection pooling)

3. **UAT** (Product Owner approval):
   - Product Owner tests gift card purchase in staging environment
   - ✓ All acceptance criteria met
   - ✓ Approved for production deployment

---

#### Phase 6: Deployment (Day 10)

1. **Deployment to Staging** (use devops-pipeline-architect):
   - GitHub Actions workflow triggered on merge to release branch
   - Database migration runs (creates gift_cards table)
   - Docker image built and pushed to AWS ECR
   - Deployed to staging ECS cluster
   - Smoke tests run (gift card purchase with test Stripe card)
   - ✓ All checks passing

2. **Deployment to Production**:
   - Product Owner approves staging environment
   - Blue-green deployment to production ECS cluster
   - Traffic switched from blue (old version) to green (new version)
   - Monitor production for 1 hour:
     - No errors in CloudWatch Logs
     - Latency p95: 1.2s (within target)
     - 5 gift cards purchased in first hour (early adopters)
   - ✓ Deployment successful

3. **Release Notes**:

   ```text
   # Release v2.5.0 - Gift Card Feature
   
   ## New Features
   - 🎁 Gift Card Purchase: Customers can now purchase gift cards ($25-$500) and send them via email
   - 💳 Stripe Integration: Secure payment processing for gift cards
   
   ## Technical Changes
   - Added `gift_cards` table to database
   - New API endpoint: POST /api/v1/gift-cards
   - Gift card codes are 16-digit alphanumeric (cryptographically secure)
   - No expiration per state law compliance
   
   ## Deployment
   - Database migration: 20250126_create_gift_cards_table
   - Requires STRIPE_SECRET_KEY environment variable
   ```

---

#### Phase 7: Monitoring (Continuous)

1. **Monitoring Dashboard** (use metrics-and-kpi-designer):
   - Prompt: "Create Grafana dashboard for gift card feature. Metrics: 1) Gift cards purchased (count per day), 2) Total gift card revenue (sum of amounts), 3) Average gift card amount, 4) API response time (p50, p95, p99), 5) Error rate, 6) Stripe payment success rate."
   - Output: Grafana dashboard with 6 panels, real-time updates

2. **Alerting**:
   - Alert 1: Gift card purchase error rate > 5% (PagerDuty to on-call engineer)
   - Alert 2: API response time p95 > 3s (Slack notification to team)
   - Alert 3: Stripe payment failure rate > 10% (PagerDuty to on-call engineer)

3. **Week 1 Production Report**:
   - Gift cards purchased: 127 (exceeding initial projections of 100)
   - Total revenue: $8,340
   - Average amount: $65.67
   - API response time p95: 1.1s (✓ within target)
   - Error rate: 0.1% (✓ within target)
   - User feedback: 4.8/5 stars (positive reception)

---

#### Phase 8: Sprint Review & Retrospective

1. **Sprint Review**:
   - Engineers demo gift card purchase flow to stakeholders
   - Marketing team provides feedback: "Can we add a 'Send Later' option for gift cards?" (added to backlog for next sprint)
   - Product Owner accepts all user stories (Definition of Done met)

2. **Retrospective** (use process-optimization-consultant):
   - **What Went Well**:
     - Gift card feature delivered on time and within budget
     - Cross-functional collaboration (engineering, marketing, compliance) was excellent
     - Stripe integration was straightforward (good third-party API)
   - **What to Improve**:
     - Load testing revealed performance issue (Stripe payment latency) - Action: Add caching for Stripe client
     - Code review took 2 days (bottleneck) - Action: Add third reviewer to rotation
     - Email sending failures not handled gracefully - Action: Add Redis job queue for async email processing
   - **Action Items for Next Sprint**:
     - Optimize Stripe payment call (caching, connection pooling) - Owner: Backend Engineer
     - Add third code reviewer - Owner: Tech Lead
     - Implement Redis job queue for emails - Owner: DevOps Engineer

---

## Prompt Chain Summary

### Quick Reference: Phase → Prompts

| Phase | Primary Prompts | Secondary Prompts |
|-------|-----------------|-------------------|
| **Phase 0: Pre-Sprint Planning** | business-case-developer, stakeholder-requirements-gatherer, requirements-analysis-expert, solution-architecture-designer | competitive-analysis-researcher, market-research-analyst |
| **Phase 1: Sprint Planning** | agile-sprint-planner, requirements-analysis-expert, metrics-and-kpi-designer | meeting-facilitator |
| **Phase 2: Design & Architecture** | solution-architecture-designer, api-design-consultant, database-schema-designer, security-code-auditor | cloud-architecture-consultant, microservices-design-expert |
| **Phase 3: Development** | code-generation-assistant, api-design-consultant, database-schema-designer, documentation-generator, refactoring-specialist | devops-pipeline-architect, test-automation-engineer |
| **Phase 4: Code Review** | code-review-expert, security-code-auditor, performance-optimization-specialist, refactoring-specialist | documentation-generator |
| **Phase 5: Testing** | test-automation-engineer, user-experience-analyst, performance-optimization-specialist | data-analysis-insights |
| **Phase 6: Deployment** | devops-pipeline-architect, cloud-architecture-consultant, database-migration-specialist | incident-response-coordinator (if issues arise) |
| **Phase 7: Monitoring** | metrics-and-kpi-designer, data-analysis-insights, incident-response-coordinator | performance-optimization-specialist |
| **Phase 8: Review & Retro** | meeting-facilitator, process-optimization-consultant | agile-sprint-planner (for next sprint) |

---

## Scaling Considerations

### Small Teams (2-5 engineers)

- Reduce sprint duration to 1 week (faster feedback loops)
- Combine roles (e.g., one engineer handles code review + testing)
- Use fewer prompts (focus on core: requirements, code generation, code review, testing)
- Simpler deployment (Heroku, Vercel, Netlify instead of Kubernetes)

### Large Teams (20-50+ engineers)

- Organize into squads (5-8 engineers per squad, each squad owns a feature area)
- Implement stricter quality gates (require 2+ peer reviews, 90%+ test coverage)
- Use advanced DevOps (Kubernetes, service mesh, blue-green deployments)
- Add specialized roles (dedicated DevOps engineer, security engineer, QA engineer)
- Use all prompts for comprehensive coverage

### Enterprise Scale (100+ engineers)

- Multiple scrum teams coordinating via Scrum of Scrums
- Shared services team (authentication, payments, notifications)
- Platform team (infrastructure, CI/CD, monitoring)
- Architecture review board (ARB) for major design decisions
- Comprehensive governance (see [Governance & Compliance Workflows](../../prompts/governance-compliance/README.md))

---

## Troubleshooting Common Issues

### Issue 1: Sprint Velocity is Inconsistent

**Symptoms**: Team commits to 80 story points but only completes 40-50  
**Root Cause**: Over-optimistic estimates, unclear requirements, frequent context switching  
**Solution**:

1. Use agile-sprint-planner to analyze historical velocity (last 3-5 sprints)
2. Commit to 70% of theoretical capacity (leave buffer for unknowns)
3. Refine user stories earlier (use requirements-analysis-expert in backlog refinement sessions)
4. Reduce work-in-progress (WIP) limits (no engineer should have >2 stories in progress)

### Issue 2: Code Reviews are Bottleneck (PRs waiting 2-3 days)

**Symptoms**: PRs pile up, engineers blocked, frustration  
**Root Cause**: Too few reviewers, unclear review expectations, large PRs  
**Solution**:

1. Implement rotating reviewer schedule (use agile-sprint-planner to assign)
2. Set PR review SLA: 4 hours for urgent, 1 day for normal
3. Break large PRs into smaller chunks (<300 lines of code)
4. Use code-review-expert to create review checklist (standardize expectations)
5. Automate trivial checks (linting, formatting) so reviewers focus on logic

### Issue 3: Production Incidents are Frequent (weekly outages)

**Symptoms**: Pager alerts at 3am, customer complaints, revenue loss  
**Root Cause**: Insufficient testing, lack of monitoring, no rollback plan  
**Solution**:

1. Increase test coverage to 80%+ (use test-automation-engineer)
2. Add comprehensive monitoring (use metrics-and-kpi-designer to define SLIs/SLOs)
3. Implement blue-green deployments or canary releases (use devops-pipeline-architect)
4. Conduct blameless postmortems after each incident (use incident-response-coordinator)
5. Create runbooks for common issues (use documentation-generator)

### Issue 4: Technical Debt is Accumulating (codebase is messy)

**Symptoms**: Developers complain about code quality, velocity decreasing over time  
**Root Cause**: "Move fast" culture without refactoring, tight deadlines  
**Solution**:

1. Allocate 20% of sprint capacity to technical debt reduction (use agile-sprint-planner)
2. Use refactoring-specialist to identify high-impact refactoring opportunities
3. Implement strict code review standards (use code-review-expert checklist)
4. Add "Definition of Done" requirement: code must be refactored and documented
5. Conduct monthly "Code Health" reviews with architecture team

---

## Next Steps

After implementing this SDLC workflow, consider exploring:

1. **[Incident Response Playbook](./incident-response-playbook.md)** - Handle production incidents using structured prompts
2. **[Business Planning Blueprint](./business-planning-blueprint.md)** - Chain business-focused prompts for strategic planning
3. **[Governance & Compliance Workflows](../../prompts/governance-compliance/README.md)** - Ensure regulatory compliance throughout SDLC

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-26 | Initial blueprint created (Tree-of-Thoughts evaluation: Waterfall vs Agile vs DevOps, selected Agile + DevOps hybrid) |

---

## Contributing

To improve this blueprint:

1. Test workflow with your team (document pain points)
2. Suggest additional prompts or phases
3. Share real-world examples from your projects
4. Submit feedback via GitHub Issues

---

**Maintained by**: [Repository Contributors](../../CONTRIBUTING.md)  
**License**: MIT
