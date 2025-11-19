# Quick Start: Platform-Specific Prompt Templates

Ready-to-use templates for GitHub Copilot, Microsoft 365, Windows Copilot, and other AI tools.

---

## GitHub Copilot Templates

### Software Development

#### 1. Feature Implementation
```python
# Implement a user authentication feature with the following requirements:
# - Support email/password login
# - Include password hashing with bcrypt
# - Generate JWT tokens for session management
# - Add rate limiting (5 attempts per 15 minutes)
# - Return proper HTTP status codes (200, 401, 429)
# - Include comprehensive error handling
# Technology: Python 3.10, Flask, SQLAlchemy
```

#### 2. Unit Test Creation
```javascript
// Create comprehensive Jest tests for the UserService class:
// Test cases:
// 1. createUser() with valid data - should return user object
// 2. createUser() with duplicate email - should throw error
// 3. findUserByEmail() with existing email - should return user
// 4. findUserByEmail() with non-existent email - should return null
// 5. updatePassword() - should hash and update password
// Include setup, teardown, and mocking for database calls
```

#### 3. API Endpoint Design
```typescript
// Design a RESTful API endpoint for managing project tasks:
// POST /api/projects/{projectId}/tasks
// - Request body: { title, description, assignee, dueDate, priority }
// - Response: 201 Created with task object and Location header
// - Validation: title required (3-200 chars), dueDate must be future
// - Authorization: User must be project member
// - Error handling: 400 for validation, 403 for authorization, 404 for project not found
// Include TypeScript interfaces and Zod validation schema
```

#### 4. Database Query Optimization
```sql
-- Optimize this slow query for better performance:
-- Current query takes 3.5 seconds on 10M rows
-- Requirements:
-- 1. Add appropriate indexes
-- 2. Rewrite using CTEs or subqueries if beneficial
-- 3. Explain index selection rationale
-- 4. Provide EXPLAIN ANALYZE output interpretation
-- Database: PostgreSQL 14
SELECT u.name, COUNT(o.id) as order_count, SUM(o.total) as revenue
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.created_at > NOW() - INTERVAL '90 days'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
ORDER BY revenue DESC;
```

#### 5. Security Code Review
```java
// Review this authentication code for security vulnerabilities:
// Check for:
// 1. SQL injection risks
// 2. Weak password hashing
// 3. Session management issues
// 4. Input validation gaps
// 5. Sensitive data exposure
// Provide specific line-by-line recommendations with severity ratings
public class AuthController {
    public User login(String email, String password) {
        String query = "SELECT * FROM users WHERE email = '" + email + "'";
        User user = database.query(query);
        if (user != null && user.password.equals(password)) {
            session.setAttribute("userId", user.id);
            return user;
        }
        return null;
    }
}
```

### Project Management

#### 6. Sprint Planning
```markdown
# Create a 2-week sprint plan based on these requirements:
# Project: E-commerce checkout redesign
# Team: 3 developers, 1 QA, 1 designer
# Capacity: 80 hours per person (holidays: Dec 25)
# Priority features:
# 1. Guest checkout flow (High) - 40 hours estimated
# 2. Saved payment methods (Medium) - 24 hours
# 3. Order confirmation email redesign (Low) - 16 hours
# 4. Mobile UI improvements (Medium) - 32 hours
# 
# Output format:
# - Sprint goal statement
# - Daily breakdown with task assignments
# - Risk assessment and mitigation
# - Definition of done checklist
```

---

## Microsoft 365 Copilot Templates

### Word Documents

#### 1. Executive Summary
```
Create an executive summary for this business proposal:
- Audience: C-level executives (non-technical)
- Length: 1 page maximum
- Include: Problem statement, solution overview, ROI projection, timeline
- Tone: Confident but factual, highlight business value
- Format: 4 sections with headers, bullet points for key facts
- Extract data from slides 5-8 in [attached PowerPoint]
```

#### 2. Meeting Notes
```
Convert this meeting transcript into structured notes:
- Format: Professional meeting minutes
- Sections: Attendees, Agenda Items, Decisions Made, Action Items, Next Steps
- For action items: Include owner name, due date, description
- Highlight: Any commitments made, budget numbers mentioned, risks identified
- Style: Concise, bullet points, ready for distribution
```

#### 3. Project Status Report
```
Generate a project status report from this week's data:
- Project: [PROJECT_NAME]
- Audience: Stakeholders and project sponsors
- Include: Progress summary, completed milestones, upcoming deliverables, 
  issues/risks, budget status, team highlights
- Format: 2-page report with executive summary at top
- Tone: Transparent about challenges, optimistic about solutions
- Add: RAG status indicators (Red/Amber/Green) for each work stream
```

### Excel Analysis

#### 4. Financial Analysis
```
Analyze this financial data for Q4 2024:
1. Calculate:
   - Revenue growth rate (QoQ and YoY)
   - Gross margin and net margin
   - Operating expense ratio
   - Cash burn rate

2. Identify:
   - Top 5 expense categories
   - Departments over/under budget
   - Revenue trends by product line

3. Create:
   - Summary table with key metrics
   - Recommendations for Q1 2025

Format: Use professional business terminology, add charts if beneficial
```

#### 5. Sales Performance Dashboard
```
Create a sales performance summary from this data:
- Time period: Last 6 months
- Metrics to include:
  * Total revenue by month
  * Top 10 sales reps (revenue + deals closed)
  * Win rate by product category
  * Average deal size trend
  * Sales cycle length (days)
  
- Output: Create a pivot table and suggest 3 visualizations
- Highlight: Any concerning trends or exceptional performance
```

### PowerPoint Presentations

#### 6. Investor Pitch Deck
```
Create a 12-slide investor pitch deck:
- Company: [YOUR_COMPANY]
- Round: Series A
- Slides needed:
  1. Title with tagline
  2. Problem (customer pain points)
  3. Solution (your product)
  4. Market size (TAM/SAM/SOM)
  5. Business model
  6. Traction (metrics, customers)
  7. Competitive landscape
  8. Go-to-market strategy
  9. Team
  10. Financial projections
  11. Funding ask and use of funds
  12. Closing/contact

- Style: Modern, visual-heavy, minimal text per slide
- Tone: Confident, data-driven, story-focused
- Source content from: [attached business plan document]
```

#### 7. Training Presentation
```
Create a training presentation for new employees about [TOPIC]:
- Duration: 45-minute session
- Audience: Non-technical business users
- Structure:
  * Introduction and objectives (2 slides)
  * Core concepts with examples (6-8 slides)
  * Hands-on exercise description (2 slides)
  * Best practices and tips (2 slides)
  * Q&A and resources (1 slide)

- Style: Friendly, educational, use icons and diagrams
- Include: Speaker notes for each slide
```

### Outlook Email

#### 8. Business Communication
```
Draft an email to the marketing team:
- Subject: Q1 2025 Campaign Kickoff and Budget Allocation
- Purpose: Announce campaign launch, share budget breakdown, request input
- Tone: Professional but enthusiastic
- Length: 3-4 paragraphs
- Include:
  * Campaign overview and goals
  * Budget allocation by channel
  * Key dates and milestones
  * Request for creative brief submissions by [DATE]
  * Next meeting time
- Call-to-action: Clear next steps for recipients
```

#### 9. Client Follow-up
```
Write a follow-up email after client demo:
- Recipient: [CLIENT_NAME], Senior VP of Operations
- Context: Demoed our project management software yesterday
- Tone: Helpful, consultative (not pushy)
- Include:
  * Thank you for their time
  * Recap of key features they showed interest in
  * Answer to their question about integrations
  * Suggested next steps (trial access, technical deep-dive)
  * Availability for follow-up call
- Length: 4-5 short paragraphs
```

---

## Windows Copilot Templates

### System Management

#### 1. File Organization
```
Organize my Downloads folder:
1. Create folders: Documents, Images, Videos, Archives, Installers, Other
2. Move files to appropriate folders based on extension
3. Delete temp files (*.tmp, *.log) older than 30 days
4. Create a summary report showing:
   - Number of files moved to each folder
   - Total space freed by deletions
   - Any files that couldn't be categorized
```

#### 2. Performance Troubleshooting
```
My computer is running slowly. Help me diagnose:
1. Check CPU and memory usage
2. Identify top 5 resource-consuming applications
3. Check for Windows updates pending
4. Scan for disk space issues (show drives with <10% free)
5. Check startup programs (list all, highlight unnecessary ones)

Provide a step-by-step action plan to improve performance.
```

#### 3. Network Diagnostics
```
I can't connect to the internet. Run diagnostics:
1. Check network adapter status
2. Test connection to router (ping gateway)
3. Test DNS resolution (ping google.com)
4. Check proxy settings
5. Review firewall rules

Provide results with explanation and suggested fixes.
```

### Productivity Setup

#### 4. Daily Workspace Setup
```
Set up my work environment for a productive morning:
1. Open applications:
   - Microsoft Teams
   - Outlook
   - Visual Studio Code (open project: C:\Work\ProjectX)
   - Chrome with tabs: Gmail, Jira, Confluence

2. System settings:
   - Enable Do Not Disturb mode
   - Set focus timer for 90 minutes
   - Increase screen brightness to 80%

3. Create today's folder: C:\Work\Daily\[TODAY'S_DATE]
```

---

## Claude / GPT Advanced Templates

### Business Analysis

#### 1. SWOT Analysis
```
Conduct a comprehensive SWOT analysis for [COMPANY/PRODUCT]:

**Context**: 
- Industry: [INDUSTRY]
- Market position: [DESCRIPTION]
- Recent developments: [KEY_CHANGES]
- Time frame: Next 12-18 months

**Analysis Framework**:

**Strengths** (Internal, Positive):
- List 5-7 key strengths
- For each: Explain why it's a strength, quantify if possible, compare to competitors

**Weaknesses** (Internal, Negative):
- List 5-7 key weaknesses
- For each: Assess severity, identify root cause, suggest improvement path

**Opportunities** (External, Positive):
- List 5-7 market opportunities
- For each: Estimate potential impact, assess feasibility, note timing considerations

**Threats** (External, Negative):
- List 5-7 potential threats
- For each: Evaluate likelihood, estimate impact, propose mitigation strategy

**Strategic Recommendations**:
- Top 3 actions to leverage strengths/opportunities
- Top 3 actions to address weaknesses/threats
- Priority order with rationale

Output format: Structured markdown with clear sections and bullet points.
```

#### 2. Market Research Report
```
Research and analyze [MARKET/INDUSTRY]:

**Scope**:
- Geographic focus: [REGION]
- Time period: [TIME_FRAME]
- Key segments: [SEGMENTS]

**Required Sections**:

1. **Market Overview** (300 words)
   - Current size and growth rate
   - Key drivers and trends
   - Regulatory environment

2. **Competitive Landscape** (400 words)
   - Top 5 players with market share
   - Competitive positioning
   - Recent M&A activity

3. **Customer Analysis** (300 words)
   - Buyer personas
   - Decision-making process
   - Key pain points

4. **Technology Trends** (300 words)
   - Emerging technologies
   - Adoption rates
   - Future disruptions

5. **Opportunities and Risks** (200 words)
   - Market opportunities for new entrants
   - Barriers to entry
   - Risk factors

6. **Forecast** (200 words)
   - 5-year market projection
   - Growth assumptions
   - Scenarios (optimistic, base, pessimistic)

Include citations for data sources. Format as professional report.
```

### Solution Architecture

#### 3. Architecture Decision Record (ADR)
```
Create an Architecture Decision Record for [DECISION]:

**Title**: ADR-[NUMBER]: [DECISION_TITLE]

**Status**: Proposed | Accepted | Deprecated | Superseded

**Context**:
- What is the issue we're addressing?
- What forces are at play (technical, political, social, project)?
- What constraints exist?

**Decision**:
- What are we doing? Be specific and prescriptive.
- Why this approach over others?

**Options Considered**:
For each option (minimum 3):
1. **Option A**: [NAME]
   - Description: [DETAILS]
   - Pros: [BENEFITS]
   - Cons: [DRAWBACKS]
   - Cost/Effort: [ESTIMATION]
   - Risks: [POTENTIAL_ISSUES]

**Selected Option**: [CHOSEN_OPTION]
**Rationale**: [WHY_THIS_ONE]

**Consequences**:
- Positive: [BENEFITS]
- Negative: [TRADE-OFFS]
- Neutral: [SIDE_EFFECTS]

**Implementation Notes**:
- Migration path: [STEPS]
- Timeline: [DURATION]
- Dependencies: [REQUIREMENTS]
- Success metrics: [KPIs]

**References**:
- [Link to related ADRs]
- [Documentation]
- [Research papers or blog posts]
```

### Content Creation

#### 4. Technical Blog Post
```
Write a technical blog post about [TOPIC]:

**Target Audience**: [LEVEL] developers/engineers
**Goal**: [EDUCATE | ANNOUNCE | TUTORIAL | OPINION]
**Length**: [WORD_COUNT] words

**Structure**:

1. **Intro** (100 words)
   - Hook: Start with a relatable problem or interesting fact
   - Context: Why this topic matters
   - Promise: What readers will learn

2. **Background** (200 words)
   - Explain the problem or concept
   - Provide necessary context
   - Link to prior knowledge

3. **Main Content** (800 words)
   - Break into 3-4 subsections
   - Use code examples (syntax-highlighted)
   - Include diagrams where helpful
   - Progressive complexity

4. **Practical Example** (300 words)
   - Real-world use case
   - Step-by-step implementation
   - Common pitfalls to avoid

5. **Conclusion** (100 words)
   - Summarize key takeaways
   - Suggest next steps or related topics
   - Call-to-action

**Style**:
- Technical but accessible
- Use analogies for complex concepts
- Active voice, present tense
- Include code snippets with comments
- Add "TL;DR" at the top

**SEO Keywords**: [LIST_KEYWORDS]
```

---

## Functional Consulting Templates

### Requirements Gathering

#### 1. Business Requirements Document (BRD)
```
Create a Business Requirements Document for [PROJECT]:

**1. Executive Summary** (1 page)
- Project overview and objectives
- Success criteria
- High-level timeline and budget

**2. Business Objectives**
- Strategic alignment
- Expected benefits (qualitative and quantitative)
- Key stakeholders and their goals

**3. Current State Analysis**
- As-Is process description
- Pain points and inefficiencies
- Quantified impact (time, cost, quality)

**4. Functional Requirements**
For each requirement:
- REQ-[ID]: [DESCRIPTION]
- Priority: Must-Have | Should-Have | Nice-to-Have
- Acceptance Criteria: [SPECIFIC_CONDITIONS]
- Assumptions: [WHAT_WE_ASSUME]
- Dependencies: [RELATED_REQUIREMENTS]

**5. Non-Functional Requirements**
- Performance (response time, throughput)
- Security (authentication, authorization, encryption)
- Scalability (user load, data volume)
- Usability (accessibility, training needs)
- Compliance (regulations, standards)

**6. Constraints**
- Technical limitations
- Budget restrictions
- Timeline requirements
- Resource availability

**7. Risks and Mitigation**
- Identified risks with severity and likelihood
- Mitigation strategies
- Contingency plans

**8. Appendices**
- Glossary of terms
- Process diagrams
- User personas
- Mockups or wireframes

Format: Professional document with table of contents, page numbers, version history.
```

#### 2. Stakeholder Analysis
```
Conduct a stakeholder analysis for [PROJECT]:

**For each stakeholder group**:

1. **Identification**
   - Name/Role: [TITLE]
   - Department: [UNIT]
   - Level: Executive | Management | Staff | External

2. **Analysis**
   - Interest in project: [HIGH | MEDIUM | LOW]
   - Influence on project: [HIGH | MEDIUM | LOW]
   - Position: Advocate | Supporter | Neutral | Skeptic | Blocker
   - Key concerns: [LIST]
   - Success criteria from their perspective: [WHAT_THEY_WANT]

3. **Engagement Strategy**
   - Communication frequency: [CADENCE]
   - Communication method: [EMAIL | MEETINGS | REPORTS]
   - Key messages: [WHAT_TO_EMPHASIZE]
   - Actions to increase support: [TACTICS]

**Stakeholder Matrix**:
Create a 2x2 matrix (Power/Interest):
- High Power, High Interest: Manage Closely
- High Power, Low Interest: Keep Satisfied
- Low Power, High Interest: Keep Informed
- Low Power, Low Interest: Monitor

**RACI Matrix**:
For key decisions and deliverables, assign:
- R: Responsible (does the work)
- A: Accountable (final authority)
- C: Consulted (provides input)
- I: Informed (kept updated)

Output: Professional document with matrices in table format.
```

---

## Additional Platform-Specific Tips

### GitHub Copilot Chat
```
Use slash commands:
/explain - Explain selected code
/fix - Suggest fixes for problems
/tests - Generate test cases
/doc - Generate documentation
/refactor - Improve code structure
```

### M365 Copilot in Teams
```
Summarize meeting:
"Summarize the last team meeting, highlighting:
- Key decisions made
- Action items with owners
- Unresolved questions"
```

### Voice-Based Assistants (Alexa, Google, Siri)
```
Keep prompts conversational and action-oriented:
"Create a reminder to review the Q4 report every Monday at 9 AM"
"Add a calendar event for the product launch meeting next Friday at 2 PM"
```

---

## Template Customization Guide

### How to Adapt Templates

1. **Replace Placeholders**: 
   - [CAPS_IN_BRACKETS] = Required input
   - (Optional details) = Can omit if not needed

2. **Adjust Specificity**:
   - More detail = Better results but slower
   - Less detail = Faster but may need iteration

3. **Context Matters**:
   - Include relevant background
   - Reference related files/data
   - Specify audience and tone

4. **Output Format**:
   - Specify exactly what you want
   - Use examples when possible
   - Request structured data (JSON, tables, bullets)

5. **Iterate**:
   - Start with template
   - Refine based on output
   - Save your best variations

---

## Need More Help?

- **Full Guide**: See [ultimate-prompting-guide.md](./ultimate-prompting-guide.md)
- **Methodology**: See [prompt-effectiveness-scoring-methodology.md](./prompt-effectiveness-scoring-methodology.md)
- **Repository**: Browse [github.com/tafreeman/prompts](https://github.com/tafreeman/prompts)

---

**Last Updated**: 2025-11-19  
**Version**: 1.0
