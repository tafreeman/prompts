# Business Prompts Quality Uplift Plan

**Version**: 1.0  
**Date**: 2025-11-17  
**Target**: Tier 1 Quality (9-10/10) for Top 10 Business Prompts  
**Methodology**: Tree-of-Thoughts Multi-Branch Analysis

---

## Executive Summary

This uplift plan identifies the **top 10 business prompts** requiring quality improvements to reach Tier 1 (9-10/10) status, based on multi-branch Tree-of-Thoughts analysis. Using governance-compliance prompts as the gold standard (legal-contract-review, security-incident-response), we evaluated 27 business prompts across three prioritization branches:

- **Branch A**: Business impact (strategy, project management, stakeholder management)
- **Branch B**: Quality gap (prompts at 5-6/10 with highest improvement potential)
- **Branch C**: Workflow integration (SDLC and incident response workflows)

**Result**: Branch B (Quality Gap) selected as primary prioritization approach, combined with Branch A insights for business-critical prompts.

**Timeline**: 8-10 weeks across 3 batches  
**Estimated Effort**: 120-150 hours total (12-15 hours per prompt)

---

## Tree-of-Thoughts Analysis

### Branch A: Business Impact Prioritization

**Criteria**: Executive-level usage, strategic decision-making, stakeholder management

**Top Candidates**:
1. Strategic Planning Consultant (5/10) - C-suite strategy decisions
2. Management Consulting Expert (5/10) - Board-level consulting
3. Digital Transformation Advisor (5/10) - Enterprise-wide transformation
4. Business Strategy Analysis (6/10) - Market entry, M&A decisions
5. Risk Management Analyst (5/10) - Enterprise risk governance
6. Due Diligence Analyst (5/10) - M&A, investment decisions
7. Crisis Management Coordinator (5/10) - Executive crisis response
8. Stakeholder Communication Manager (5/10) - Executive communications
9. Innovation Strategy Consultant (5/10) - Product strategy, R&D
10. Market Entry Strategist (5/10) - International expansion

**Strengths**: High business value, immediate ROI if improved  
**Weaknesses**: Doesn't address mid-tier prompts with easier improvement paths

---

### Branch B: Quality Gap Prioritization

**Criteria**: Current score 5-6/10, highest improvement potential with moderate effort

**Top Candidates** (selected as primary approach):
1. Strategic Planning Consultant (5/10 → 9/10) - Missing frameworks, governance, examples
2. Management Consulting Expert (5/10 → 9/10) - Needs structured methodology, case studies
3. Digital Transformation Advisor (5/10 → 9/10) - Lacks maturity models, frameworks
4. Risk Management Analyst (5/10 → 9/10) - Missing risk frameworks, quantification
5. Due Diligence Analyst (5/10 → 9/10) - Needs checklists, regulatory scope
6. Crisis Management Coordinator (5/10 → 9/10) - Missing escalation protocols, playbooks
7. Change Management Coordinator (5/10 → 9/10) - Lacks change frameworks (ADKAR, Kotter)
8. Innovation Strategy Consultant (5/10 → 9/10) - Missing innovation frameworks
9. Organizational Change Manager (5/10 → 9/10) - Needs change impact assessment tools
10. Business Process Reengineering (5/10 → 9/10) - Lacks BPM frameworks, process mapping

**Strengths**: Clear improvement path, moderate effort, high impact  
**Weaknesses**: May miss workflow-critical prompts

---

### Branch C: Workflow Integration Prioritization

**Criteria**: Integration with SDLC blueprint, incident response, cross-functional workflows

**Top Candidates**:
1. Agile Sprint Planner (5/10) - Core to SDLC Phase 1
2. Risk Management Analyst (5/10) - Referenced in SDLC Phases 1, 4, 6
3. Stakeholder Communication Manager (5/10) - Cross-phase communication
4. Change Management Coordinator (5/10) - SDLC Phase 1-3 transitions
5. Crisis Management Coordinator (5/10) - Incident response workflow
6. Project Charter Creator (5/10) - SDLC Phase 0
7. Strategic Planning Consultant (5/10) - Pre-SDLC strategy
8. Business Strategy Analysis (6/10) - Phase 0 business case validation
9. Due Diligence Analyst (5/10) - Vendor/tool selection in SDLC
10. Innovation Strategy Consultant (5/10) - Phase 0 opportunity identification

**Strengths**: Maximizes ecosystem value, workflow coherence  
**Weaknesses**: Lower business impact if workflow adoption is low

---

### Decision: Hybrid Approach (Branch B + Branch A)

**Selected Strategy**: Use **Branch B (Quality Gap)** as primary prioritization, incorporate **Branch A (Business Impact)** for tie-breaking and batch sequencing.

**Rationale**:
- Branch B prompts have clearest improvement path (5/10 → 9/10 achievable)
- Branch A ensures highest business value prompts are prioritized first
- Branch C insights used for cross-linking related prompts in uplift

**Final Top 10** (in priority order):

1. **Strategic Planning Consultant** (Branch B + A - Highest business impact + quality gap)
2. **Management Consulting Expert** (Branch B + A - Executive-level consulting)
3. **Digital Transformation Advisor** (Branch B + A - Enterprise transformation)
4. **Risk Management Analyst** (Branch B + C - SDLC integration + risk governance)
5. **Due Diligence Analyst** (Branch B + A - M&A, investment decisions)
6. **Crisis Management Coordinator** (Branch B + C - Incident response workflow)
7. **Change Management Coordinator** (Branch B + C - SDLC transitions)
8. **Innovation Strategy Consultant** (Branch B + A - Product strategy, R&D)
9. **Organizational Change Manager** (Branch B + A - Enterprise change programs)
10. **Business Process Reengineering** (Branch B - Operational excellence, cost optimization)

---

## Top 10 Prompts: Detailed Analysis

### 1. Strategic Planning Consultant

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No executive persona definition (e.g., "You are a McKinsey-level strategy consultant with 15+ years advising Fortune 500 CEOs")
- ❌ Missing strategic frameworks (Ansoff Matrix, Porter's Five Forces, Blue Ocean Strategy)
- ❌ No governance metadata (approval_required, stakeholder_impact, data_classification)
- ❌ Minimal structured output format (no JSON schema, no clear deliverables)
- ❌ Placeholder-heavy prompt (lacks concrete guidance)
- ❌ No realistic case studies or business scenarios
- ❌ Missing competitive intelligence analysis
- ❌ No risk quantification or sensitivity analysis

**Target State - Tier 1 Requirements**:
- ✅ Executive-level persona: "You are a senior strategy consultant (McKinsey, BCG, Bain-level) specializing in corporate strategy for Fortune 500 companies. You have 15+ years advising C-suite executives on strategic planning, M&A, market entry, and competitive positioning."
- ✅ Business frameworks integration:
  - **Porter's Five Forces**: Industry attractiveness analysis
  - **Ansoff Matrix**: Growth strategy options (market penetration, product development, market development, diversification)
  - **BCG Growth-Share Matrix**: Portfolio analysis
  - **VRIO Framework**: Competitive advantage assessment (Value, Rarity, Imitability, Organization)
  - **Scenario Planning**: 3-5 year strategic scenarios (best case, base case, worst case)
- ✅ Governance metadata:
  - `approval_required: "Board of Directors or CEO"`
  - `stakeholder_impact: "High - affects entire organization"`
  - `data_classification: "Confidential - strategic information"`
  - `risk_level: "Medium - strategic direction changes"`
- ✅ Structured outputs:
  - Strategic planning memo (executive summary, situation analysis, strategic options, recommendation, implementation roadmap)
  - Financial projections (3-5 year revenue, EBITDA, market share)
  - Risk assessment with quantified impacts
  - JSON schema for programmatic use
- ✅ Realistic case studies:
  - Example 1: SaaS company deciding between enterprise expansion vs SMB vertical specialization (similar to governance prompts' depth)
  - Example 2: Manufacturing company evaluating digital transformation strategy
  - Example 3: Retail company analyzing market entry into emerging markets
- ✅ Cross-links to related prompts:
  - `business-strategy-analysis.md` (tactical strategy)
  - `market-entry-strategist.md` (international expansion)
  - `innovation-strategy-consultant.md` (growth through innovation)

**Uplift Approach**:
1. Add executive persona with credentials and methodology expertise
2. Integrate 5-6 strategic frameworks with templates
3. Add governance metadata section (modeled after security-incident-response)
4. Create 2-3 detailed case studies with full input/output examples (1000+ words each)
5. Add structured output formats (markdown report template + JSON schema)
6. Include sensitivity analysis and risk quantification sections
7. Add workflow integration notes (when to use in SDLC Phase 0)

**Effort Estimate**: 14-16 hours
- Framework research and templates: 4 hours
- Case study development: 6 hours
- Governance metadata and structured outputs: 3 hours
- Testing and refinement: 3 hours

---

### 2. Management Consulting Expert

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ Generic "consulting" persona (not specific to McKinsey Method or structured problem-solving)
- ❌ No problem-solving frameworks (Hypothesis-Driven Approach, Issue Trees, MECE principles)
- ❌ Missing deliverable templates (consulting memo, slide deck structure)
- ❌ No stakeholder management guidance
- ❌ Lacks governance metadata
- ❌ No realistic client scenarios

**Target State - Tier 1 Requirements**:
- ✅ Management consulting persona: "You are a Principal at a top-tier management consulting firm (McKinsey, BCG, Bain) with 12+ years of experience. You specialize in hypothesis-driven problem-solving, MECE frameworks, and executive communication."
- ✅ Consulting frameworks:
  - **Hypothesis-Driven Approach**: Start with hypothesis, test with data
  - **Issue Tree / Logic Tree**: Break complex problems into MECE (Mutually Exclusive, Collectively Exhaustive) components
  - **80/20 Rule**: Focus on highest-impact areas
  - **Pyramid Principle**: Structure recommendations (answer first, then supporting arguments)
  - **Consulting Memo Format**: Situation, Complication, Question, Answer (SCQA)
- ✅ Governance metadata:
  - `approval_required: "Client Executive Sponsor"`
  - `stakeholder_impact: "High - organizational restructuring, cost reduction"`
  - `data_classification: "Confidential - client proprietary information"`
  - `retention_period: "7 years (client engagement records)"`
- ✅ Deliverable templates:
  - **Consulting Memo**: 1-2 page executive summary (SCQA format)
  - **Slide Deck Structure**: Title slide, situation, complication, answer, supporting analysis, recommendations, next steps
  - **Issue Tree Visual**: Decompose problem into sub-issues
- ✅ Case studies:
  - Example 1: Cost reduction for manufacturing company (target 20% OPEX reduction)
  - Example 2: Organizational restructuring for tech company (reduce layers, improve agility)
  - Example 3: Growth strategy for financial services firm (expand into new customer segments)
- ✅ Cross-links:
  - `strategic-planning-consultant.md` (strategy development)
  - `business-process-reengineering.md` (operational improvement)
  - `organizational-change-manager.md` (change implementation)

**Uplift Approach**:
1. Define management consulting persona with specific methodology (McKinsey Method)
2. Add 5 consulting frameworks with templates (Issue Tree, MECE, Pyramid Principle)
3. Create consulting deliverable templates (memo, slide deck, issue tree)
4. Develop 3 realistic case studies with full problem-solving walkthrough
5. Add governance metadata and stakeholder management section
6. Include data-driven analysis guidance (how to use data to test hypotheses)

**Effort Estimate**: 12-14 hours

---

### 3. Digital Transformation Advisor

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No digital maturity assessment framework
- ❌ Missing technology roadmap templates
- ❌ Lacks change management integration
- ❌ No governance metadata
- ❌ Generic transformation advice (not industry-specific)
- ❌ No realistic transformation case studies

**Target State - Tier 1 Requirements**:
- ✅ Digital transformation persona: "You are a digital transformation advisor with 15+ years guiding Fortune 500 companies through enterprise-wide technology modernization. You specialize in digital maturity assessments, change management, and technology roadmaps."
- ✅ Digital maturity frameworks:
  - **Deloitte Digital Maturity Model**: Assess current state (Digital Novice, Digital Explorer, Digital Player, Digital Leader, Digital Master)
  - **MIT CISR Digital Transformation Framework**: Operating model transformation (coordination vs autonomy, integration vs modularity)
  - **Gartner Pace-Layered Strategy**: Systems of Record (stability), Differentiation (agility), Innovation (experimentation)
- ✅ Technology roadmap templates:
  - **3-Horizon Model**: Horizon 1 (core business), Horizon 2 (emerging opportunities), Horizon 3 (future innovations)
  - **Technology Stack Assessment**: Legacy systems, cloud migration, data platforms, AI/ML capabilities
  - **Phased Implementation Plan**: Quick wins (0-6 months), foundational changes (6-18 months), transformational initiatives (18-36 months)
- ✅ Governance metadata:
  - `approval_required: "CIO, CTO, and CEO"`
  - `stakeholder_impact: "Very High - affects all departments, technology stack, processes"`
  - `data_classification: "Confidential - strategic technology plans"`
  - `risk_level: "High - organizational disruption, technology investment"`
  - `regulatory_scope: ["data-privacy", "cybersecurity", "industry-specific"]`
- ✅ Case studies:
  - Example 1: Traditional bank digital transformation (mobile banking, API platform, cloud migration)
  - Example 2: Manufacturing company Industry 4.0 transformation (IoT, predictive maintenance, digital twin)
  - Example 3: Retail company omnichannel transformation (e-commerce, in-store tech, unified customer data)
- ✅ Change management integration:
  - Link to `change-management-coordinator.md` for organizational change
  - Link to `organizational-change-manager.md` for large-scale change programs
  - Include stakeholder communication plan
- ✅ Cross-links:
  - `innovation-strategy-consultant.md` (innovation pipeline)
  - `business-process-reengineering.md` (process digitization)
  - `risk-management-analyst.md` (technology risk assessment)

**Uplift Approach**:
1. Add digital transformation persona with industry expertise
2. Integrate 3 digital maturity frameworks (Deloitte, MIT CISR, Gartner)
3. Create technology roadmap templates (3-Horizon Model, phased implementation)
4. Develop 3 industry-specific case studies (banking, manufacturing, retail)
5. Add governance metadata and regulatory compliance section
6. Include change management and stakeholder communication plans
7. Add quantified business outcomes (cost savings, revenue growth, time-to-market)

**Effort Estimate**: 14-16 hours

---

### 4. Risk Management Analyst

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Intermediate  

**Current State - What's Missing**:
- ❌ No risk assessment frameworks (ISO 31000, COSO ERM)
- ❌ Missing risk quantification methods (probability × impact)
- ❌ Lacks risk register templates
- ❌ No governance metadata
- ❌ Generic risk categories (not specific to project/enterprise/operational risks)
- ❌ No SDLC integration guidance

**Target State - Tier 1 Requirements**:
- ✅ Risk management persona: "You are an enterprise risk management analyst with expertise in ISO 31000, COSO ERM, and project risk management. You specialize in risk identification, quantification, and mitigation planning."
- ✅ Risk frameworks:
  - **ISO 31000**: International risk management standard
  - **COSO ERM Framework**: Enterprise risk management (strategy, operations, reporting, compliance)
  - **PMBOK Risk Management**: Project risk management (identify, analyze, respond, monitor)
  - **Risk Matrix**: Probability (1-5) × Impact (1-5) = Risk Score (1-25)
- ✅ Risk quantification methods:
  - **Qualitative**: Low, Medium, High, Critical
  - **Quantitative**: Probability (%) × Financial Impact ($) = Expected Monetary Value (EMV)
  - **Monte Carlo Simulation**: Range of possible outcomes with probabilities
- ✅ Risk register template:
  - Risk ID, Category, Description, Probability, Impact, Risk Score, Owner, Mitigation Strategy, Contingency Plan, Status
- ✅ Governance metadata:
  - `approval_required: "Risk Management Committee or CRO"`
  - `stakeholder_impact: "High - project success, financial exposure"`
  - `data_classification: "Confidential - risk exposure data"`
  - `retention_period: "7 years (risk records)"`
- ✅ SDLC integration:
  - Phase 1 (Sprint Planning): Identify sprint risks
  - Phase 4 (Code Review): Security risk assessment
  - Phase 6 (Deployment): Production deployment risks
  - Phase 7 (Monitoring): Operational risks
- ✅ Case studies:
  - Example 1: Software project risk assessment (technical risks, schedule risks, resource risks)
  - Example 2: Enterprise risk management for M&A transaction
  - Example 3: Operational risk assessment for cloud migration
- ✅ Cross-links:
  - `security-incident-response.md` (security risks)
  - `crisis-management-coordinator.md` (crisis response)
  - `due-diligence-analyst.md` (transaction risks)

**Uplift Approach**:
1. Add risk management persona with framework expertise (ISO 31000, COSO)
2. Integrate risk assessment frameworks and quantification methods
3. Create risk register template with probability × impact matrix
4. Add 3 realistic case studies (project, enterprise, operational risks)
5. Include governance metadata and escalation protocols
6. Add SDLC integration guidance (when to use in each phase)
7. Include risk monitoring and reporting procedures

**Effort Estimate**: 10-12 hours

---

### 5. Due Diligence Analyst

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No due diligence frameworks (financial, legal, operational, technical)
- ❌ Missing due diligence checklists
- ❌ Lacks regulatory scope (M&A compliance, antitrust, data privacy)
- ❌ No governance metadata
- ❌ Generic due diligence guidance (not specific to M&A, investment, vendor assessment)
- ❌ No realistic transaction scenarios

**Target State - Tier 1 Requirements**:
- ✅ Due diligence persona: "You are a due diligence analyst with 10+ years conducting M&A, investment, and vendor due diligence for private equity firms and Fortune 500 companies. You specialize in financial, legal, operational, and technical due diligence."
- ✅ Due diligence frameworks:
  - **Financial DD**: Revenue quality, EBITDA normalization, working capital, debt/equity structure
  - **Legal DD**: Contracts, litigation, IP ownership, regulatory compliance
  - **Operational DD**: Customer concentration, supply chain, key personnel, scalability
  - **Technical DD**: Technology stack, architecture, security, technical debt, scalability
  - **Commercial DD**: Market size, competitive position, customer satisfaction, growth potential
- ✅ Due diligence checklists (by type):
  - **M&A Transaction**: 50+ item checklist (financial statements, contracts, IP, litigation, customer list, etc.)
  - **Vendor Assessment**: 30+ item checklist (security, compliance, financial stability, SLA terms)
  - **Investment DD**: 40+ item checklist (market opportunity, team, product-market fit, financials)
- ✅ Governance metadata:
  - `approval_required: "General Counsel, CFO, or Investment Committee"`
  - `stakeholder_impact: "Critical - transaction success, financial exposure, legal liability"`
  - `data_classification: "Highly Confidential - M&A, investment, proprietary data"`
  - `risk_level: "Critical - multi-million dollar transactions"`
  - `regulatory_scope: ["HSR-antitrust", "GDPR", "SOX", "industry-specific"]`
  - `retention_period: "7-10 years (transaction records)"`
- ✅ Case studies:
  - Example 1: M&A due diligence for SaaS company acquisition ($50M transaction)
  - Example 2: Vendor due diligence for critical cloud infrastructure provider
  - Example 3: Investment due diligence for Series B funding ($20M)
- ✅ Cross-links:
  - `legal-contract-review.md` (contract analysis)
  - `risk-management-analyst.md` (transaction risk assessment)
  - `security-code-auditor.md` (technical due diligence for software)

**Uplift Approach**:
1. Add due diligence persona with M&A and investment expertise
2. Integrate 5 due diligence frameworks (financial, legal, operational, technical, commercial)
3. Create comprehensive checklists for M&A, vendor, and investment due diligence
4. Develop 3 realistic case studies with full due diligence reports
5. Add governance metadata with regulatory compliance requirements
6. Include red flag identification and escalation procedures
7. Add quantified risk assessment (deal-breaker risks, negotiable risks, acceptable risks)

**Effort Estimate**: 14-16 hours

---

### 6. Crisis Management Coordinator

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Intermediate  

**Current State - What's Missing**:
- ❌ No crisis response frameworks (ICS, NIMS)
- ❌ Missing escalation protocols and decision trees
- ❌ Lacks crisis communication templates
- ❌ No governance metadata
- ❌ Generic crisis guidance (not specific to types: PR crisis, operational crisis, security incident)
- ❌ No realistic crisis scenarios
- ❌ No integration with incident response workflow

**Target State - Tier 1 Requirements**:
- ✅ Crisis management persona: "You are a crisis management coordinator with 10+ years managing organizational crises for Fortune 500 companies. You specialize in Incident Command System (ICS), crisis communications, and business continuity. You have managed PR crises, operational disruptions, security incidents, and natural disasters."
- ✅ Crisis response frameworks:
  - **ICS (Incident Command System)**: Standardized approach (Command, Operations, Planning, Logistics, Finance/Admin)
  - **NIMS (National Incident Management System)**: Preparedness, Communications, Resource Management, Command and Management
  - **Crisis Lifecycle**: Prevention → Preparedness → Response → Recovery → Mitigation
- ✅ Crisis decision tree:
  - **Severity Assessment**: Level 1 (Minor), Level 2 (Moderate), Level 3 (Major), Level 4 (Critical)
  - **Escalation Triggers**: Financial impact, media attention, regulatory involvement, safety risk
  - **Response Team Activation**: Who to notify, when to activate crisis management team
- ✅ Governance metadata:
  - `approval_required: "CEO, General Counsel, or Crisis Management Team"`
  - `stakeholder_impact: "Very High - organizational reputation, legal liability, financial loss"`
  - `data_classification: "Highly Confidential - crisis details, response plans"`
  - `risk_level: "Critical - organizational survival"`
  - `retention_period: "10 years (crisis records, legal holds)"`
- ✅ Crisis communication templates:
  - **Internal Communication**: Notify employees (facts, actions taken, next steps)
  - **External Communication**: Press release, customer notification, social media response
  - **Stakeholder Communication**: Board, investors, regulators
- ✅ Integration with incident response workflow:
  - Link to `security-incident-response.md` (security crises)
  - Link to SDLC blueprint Phase 7 (production incidents)
- ✅ Case studies:
  - Example 1: Data breach crisis (GDPR notification, customer communication, media response)
  - Example 2: Product recall crisis (manufacturing defect, customer safety, regulatory compliance)
  - Example 3: Executive misconduct crisis (PR response, internal investigation, board communication)
- ✅ Cross-links:
  - `security-incident-response.md` (security incidents)
  - `stakeholder-communication-manager.md` (stakeholder comms)
  - `risk-management-analyst.md` (crisis risk assessment)

**Uplift Approach**:
1. Add crisis management persona with ICS/NIMS expertise
2. Integrate crisis response frameworks (ICS, NIMS, crisis lifecycle)
3. Create crisis decision tree and escalation protocols
4. Develop crisis communication templates (internal, external, stakeholder)
5. Add 3 realistic case studies (data breach, product recall, executive misconduct)
6. Include governance metadata and regulatory notification requirements
7. Add workflow integration with security-incident-response and SDLC

**Effort Estimate**: 12-14 hours

---

### 7. Change Management Coordinator

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Intermediate  

**Current State - What's Missing**:
- ❌ No change management frameworks (ADKAR, Kotter's 8-Step, Prosci)
- ❌ Missing change impact assessment templates
- ❌ Lacks stakeholder resistance management
- ❌ No governance metadata
- ❌ Generic change guidance (not specific to organizational, process, technology changes)
- ❌ No SDLC integration guidance

**Target State - Tier 1 Requirements**:
- ✅ Change management persona: "You are an organizational change management specialist with 10+ years implementing large-scale change programs using Prosci ADKAR, Kotter's 8-Step Process, and Lewin's Change Model. You specialize in change impact assessment, stakeholder engagement, and resistance management."
- ✅ Change management frameworks:
  - **ADKAR Model**: Awareness, Desire, Knowledge, Ability, Reinforcement
  - **Kotter's 8-Step Process**: Create urgency, build coalition, form vision, communicate, empower action, create wins, consolidate gains, anchor change
  - **Lewin's Change Model**: Unfreeze, Change, Refreeze
  - **Prosci 3-Phase Process**: Prepare, Manage, Reinforce
- ✅ Change impact assessment template:
  - **Stakeholder Analysis**: Who is affected? (Leadership, Managers, Employees, Customers, Partners)
  - **Impact Level**: High, Medium, Low (by stakeholder group)
  - **Resistance Level**: Expected resistance (High, Medium, Low)
  - **Change Readiness**: Organization's readiness for change (assess cultural, structural, resource factors)
- ✅ Governance metadata:
  - `approval_required: "Change Control Board or Executive Sponsor"`
  - `stakeholder_impact: "High - organizational processes, roles, technology"`
  - `data_classification: "Confidential - change plans, stakeholder analysis"`
  - `retention_period: "5 years (change records)"`
- ✅ SDLC integration:
  - Phase 1-3: Change management for new features/processes
  - Phase 6: Deployment communication and training
  - Phase 8: Retrospective - change adoption assessment
- ✅ Case studies:
  - Example 1: ERP system implementation (organizational, process, technology change)
  - Example 2: Agile transformation (cultural and process change)
  - Example 3: Organizational restructuring (role changes, reporting structure)
- ✅ Cross-links:
  - `organizational-change-manager.md` (enterprise-wide change)
  - `stakeholder-communication-manager.md` (change communication)
  - `digital-transformation-advisor.md` (technology change)

**Uplift Approach**:
1. Add change management persona with framework expertise (ADKAR, Kotter, Prosci)
2. Integrate 4 change management frameworks with application guidance
3. Create change impact assessment template (stakeholder analysis, resistance management)
4. Develop 3 realistic case studies (ERP, Agile transformation, restructuring)
5. Add governance metadata and change control board approval process
6. Include SDLC integration guidance (when to apply change management in each phase)
7. Add training and communication plan templates

**Effort Estimate**: 10-12 hours

---

### 8. Innovation Strategy Consultant

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No innovation frameworks (Design Thinking, Lean Startup, Stage-Gate)
- ❌ Missing innovation portfolio management (core, adjacent, transformational)
- ❌ Lacks governance metadata
- ❌ Generic innovation guidance (not specific to product, process, business model innovation)
- ❌ No realistic innovation case studies

**Target State - Tier 1 Requirements**:
- ✅ Innovation strategy persona: "You are an innovation strategy consultant with 12+ years advising Fortune 500 companies on innovation programs. You specialize in Design Thinking, Lean Startup, Stage-Gate process, and innovation portfolio management. You have launched 50+ new products and business models."
- ✅ Innovation frameworks:
  - **Design Thinking**: Empathize, Define, Ideate, Prototype, Test
  - **Lean Startup**: Build-Measure-Learn cycle, MVP (Minimum Viable Product), validated learning
  - **Stage-Gate Process**: Idea → Scoping → Business Case → Development → Testing → Launch
  - **Innovation Ambition Matrix**: Core (optimize existing), Adjacent (expand into new), Transformational (create new markets)
  - **Jobs-to-be-Done (JTBD)**: Understand customer jobs, not just features
- ✅ Innovation portfolio management:
  - **70-20-10 Rule**: 70% core business, 20% adjacent opportunities, 10% transformational bets
  - **Innovation Funnel**: Many ideas → few prototypes → fewer pilots → select launches
  - **Success Metrics**: Revenue from new products (%), time-to-market, innovation pipeline value
- ✅ Governance metadata:
  - `approval_required: "Chief Innovation Officer or Innovation Committee"`
  - `stakeholder_impact: "High - product roadmap, R&D budget, market positioning"`
  - `data_classification: "Confidential - innovation strategy, product pipeline"`
  - `risk_level: "Medium - R&D investment, market risk"`
- ✅ Case studies:
  - Example 1: Consumer goods company innovation strategy (new product categories, adjacent markets)
  - Example 2: Technology company innovation program (AI/ML capabilities, platform expansion)
  - Example 3: Healthcare company innovation portfolio (core optimization, telehealth, AI diagnostics)
- ✅ Cross-links:
  - `digital-transformation-advisor.md` (technology innovation)
  - `strategic-planning-consultant.md` (innovation as growth strategy)
  - `business-strategy-analysis.md` (competitive differentiation through innovation)

**Uplift Approach**:
1. Add innovation strategy persona with framework expertise
2. Integrate 5 innovation frameworks (Design Thinking, Lean Startup, Stage-Gate, Innovation Ambition Matrix, JTBD)
3. Create innovation portfolio management templates (70-20-10 rule, innovation funnel)
4. Develop 3 industry-specific case studies (consumer goods, tech, healthcare)
5. Add governance metadata and innovation committee approval process
6. Include innovation metrics and ROI calculation
7. Add innovation risk assessment (technical feasibility, market acceptance, competitive response)

**Effort Estimate**: 14-16 hours

---

### 9. Organizational Change Manager

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No organizational change frameworks (McKinsey 7S, Burke-Litwin)
- ❌ Missing change impact assessment tools
- ❌ Lacks governance metadata
- ❌ Generic change guidance (not specific to mergers, restructuring, cultural transformation)
- ❌ No realistic change program case studies

**Target State - Tier 1 Requirements**:
- ✅ Organizational change persona: "You are an organizational change management leader with 15+ years managing enterprise-wide transformations for Global 2000 companies. You specialize in McKinsey 7S, Burke-Litwin Model, and large-scale change programs (mergers, restructuring, cultural transformation)."
- ✅ Organizational change frameworks:
  - **McKinsey 7S Model**: Strategy, Structure, Systems, Shared Values, Style, Staff, Skills
  - **Burke-Litwin Model**: Transformational factors (external environment, mission/strategy, leadership, organizational culture) → Transactional factors (structure, systems, management practices, climate, motivation)
  - **Congruence Model**: Work, People, Formal Organization, Informal Organization (assess alignment)
  - **Organizational Culture Assessment (OCAI)**: Assess current vs desired culture (Clan, Adhocracy, Market, Hierarchy)
- ✅ Change impact assessment:
  - **Stakeholder Mapping**: Power/Interest Grid (Manage Closely, Keep Satisfied, Keep Informed, Monitor)
  - **Readiness Assessment**: Cultural readiness, structural readiness, leadership readiness, resource readiness
  - **Change Curve**: Denial → Resistance → Exploration → Commitment (support stakeholders through stages)
- ✅ Governance metadata:
  - `approval_required: "CEO and Board of Directors"`
  - `stakeholder_impact: "Very High - affects organizational structure, culture, leadership, processes"`
  - `data_classification: "Highly Confidential - org structure, leadership changes"`
  - `risk_level: "High - organizational disruption, talent retention"`
  - `retention_period: "7 years (change program records)"`
- ✅ Case studies:
  - Example 1: Post-merger integration (combine two companies, align cultures, rationalize systems)
  - Example 2: Organizational restructuring (reduce layers, move to matrix structure, cost reduction)
  - Example 3: Cultural transformation (shift from hierarchical to agile culture)
- ✅ Cross-links:
  - `change-management-coordinator.md` (project-level change)
  - `digital-transformation-advisor.md` (technology-driven change)
  - `management-consulting-expert.md` (organizational effectiveness)

**Uplift Approach**:
1. Add organizational change persona with enterprise transformation expertise
2. Integrate 4 organizational change frameworks (McKinsey 7S, Burke-Litwin, Congruence Model, OCAI)
3. Create change impact assessment templates (stakeholder mapping, readiness assessment)
4. Develop 3 realistic case studies (M&A integration, restructuring, cultural transformation)
5. Add governance metadata and board approval requirements
6. Include change communication and training plans (tailored by stakeholder group)
7. Add change success metrics (adoption rate, cultural assessment scores, retention)

**Effort Estimate**: 14-16 hours

---

### 10. Business Process Reengineering

**Current Score**: 5/10  
**Target Score**: 9/10  
**Difficulty**: Advanced  

**Current State - What's Missing**:
- ❌ No BPR frameworks (Hammer & Champy, Six Sigma, Lean)
- ❌ Missing process mapping templates (SIPOC, Value Stream Map, Swimlane)
- ❌ Lacks governance metadata
- ❌ Generic BPR guidance (not specific to operational excellence, cost reduction, customer experience)
- ❌ No realistic reengineering case studies

**Target State - Tier 1 Requirements**:
- ✅ Business process reengineering persona: "You are a business process reengineering expert with 12+ years leading operational excellence programs for Fortune 500 companies. You specialize in Hammer & Champy BPR, Lean Six Sigma, and value stream mapping. You have delivered $100M+ in cost savings and operational improvements."
- ✅ BPR frameworks:
  - **Hammer & Champy BPR**: Radical redesign of business processes (not incremental improvement)
  - **Lean**: Eliminate waste (muda), focus on value stream
  - **Six Sigma**: DMAIC (Define, Measure, Analyze, Improve, Control) for process improvement
  - **Theory of Constraints (TOC)**: Identify and optimize bottlenecks
- ✅ Process mapping tools:
  - **SIPOC**: Suppliers, Inputs, Process, Outputs, Customers
  - **Value Stream Map**: Visualize end-to-end process flow, identify waste
  - **Swimlane Diagram**: Show process steps across departments/roles
  - **RACI Matrix**: Responsible, Accountable, Consulted, Informed (clarify roles)
- ✅ Governance metadata:
  - `approval_required: "COO or Process Owner"`
  - `stakeholder_impact: "High - operational processes, roles, systems"`
  - `data_classification: "Confidential - process details, cost data"`
  - `risk_level: "Medium - process disruption, employee resistance"`
- ✅ Case studies:
  - Example 1: Order-to-cash process reengineering (reduce cycle time from 14 days to 3 days, improve cash flow)
  - Example 2: Customer service process optimization (reduce call handle time by 30%, improve CSAT)
  - Example 3: Procurement process reengineering (consolidate vendors, automate PO approval, reduce cost by 15%)
- ✅ Cross-links:
  - `digital-transformation-advisor.md` (technology-enabled BPR)
  - `change-management-coordinator.md` (manage process change)
  - `organizational-change-manager.md` (organizational impact of BPR)

**Uplift Approach**:
1. Add BPR persona with Lean Six Sigma and operational excellence expertise
2. Integrate 4 BPR frameworks (Hammer & Champy, Lean, Six Sigma, TOC)
3. Create process mapping templates (SIPOC, Value Stream Map, Swimlane, RACI)
4. Develop 3 realistic case studies with quantified benefits (cycle time reduction, cost savings, quality improvement)
5. Add governance metadata and process owner approval
6. Include change management and communication plans (process training, role changes)
7. Add success metrics (cycle time, cost, quality, customer satisfaction)

**Effort Estimate**: 12-14 hours

---

## Batch Grouping & Implementation Timeline

### Batch 1: Executive Strategy (Weeks 1-3)
**Theme**: C-suite decision-making, strategic planning  
**Effort**: 42-48 hours total

**Prompts**:
1. **Strategic Planning Consultant** (14-16h) - Corporate strategy, strategic planning frameworks
2. **Management Consulting Expert** (12-14h) - Problem-solving, hypothesis-driven approach
3. **Business Strategy Analysis** (10-12h, bonus uplift) - Tactical strategy, market analysis

**Rationale**: These prompts are frequently used together for strategic planning sessions. Uplifting them as a batch ensures consistency in frameworks, terminology, and cross-linking.

**Shared Elements**:
- Strategic frameworks (Porter's Five Forces, Ansoff Matrix, BCG Matrix)
- SWOT analysis templates
- Executive communication formats (consulting memo, board deck)
- Governance metadata (Board/CEO approval)

**Deliverables**:
- 3 uplifted prompts with Tier 1 quality
- Shared framework library (markdown files in `docs/frameworks/`)
- Cross-linked related prompts

---

### Batch 2: Risk & Transformation (Weeks 4-6)
**Theme**: Enterprise risk, digital transformation, organizational change  
**Effort**: 42-46 hours total

**Prompts**:
4. **Risk Management Analyst** (10-12h) - Risk assessment, quantification, mitigation
5. **Digital Transformation Advisor** (14-16h) - Technology roadmap, digital maturity
6. **Organizational Change Manager** (14-16h) - Enterprise-wide change programs

**Rationale**: These prompts address complementary aspects of enterprise transformation: managing risks, planning technology changes, and leading organizational change.

**Shared Elements**:
- Risk assessment frameworks (ISO 31000, COSO ERM)
- Change management frameworks (McKinsey 7S, ADKAR)
- Digital maturity models
- Governance metadata (CIO/CTO/CEO approval, regulatory compliance)

**Deliverables**:
- 3 uplifted prompts with Tier 1 quality
- Risk assessment templates
- Change impact assessment templates
- Digital maturity assessment checklist

---

### Batch 3: Crisis & Due Diligence (Weeks 7-9)
**Theme**: Crisis management, due diligence, operational excellence  
**Effort**: 38-44 hours total

**Prompts**:
7. **Due Diligence Analyst** (14-16h) - M&A, investment, vendor due diligence
8. **Crisis Management Coordinator** (12-14h) - Crisis response, incident management
9. **Change Management Coordinator** (10-12h) - Project-level change management
10. **Business Process Reengineering** (12-14h, bonus) - Operational excellence, process optimization

**Rationale**: These prompts are used for high-stakes, time-sensitive situations (M&A, crises, major changes). Uplifting them together ensures consistent governance, escalation protocols, and compliance frameworks.

**Shared Elements**:
- Crisis response protocols (ICS, NIMS)
- Due diligence checklists (financial, legal, operational, technical)
- Change management frameworks (ADKAR, Kotter)
- Governance metadata (legal/regulatory requirements, escalation triggers)

**Deliverables**:
- 4 uplifted prompts with Tier 1 quality
- Crisis response playbook templates
- Due diligence checklists (M&A, vendor, investment)
- Change management templates (stakeholder analysis, communication plan)

---

## Implementation Checklist

### For Each Prompt Uplift:

**Phase 1: Research & Planning (2-3 hours)**
- [ ] Review governance-compliance prompts for Tier 1 benchmark
- [ ] Research relevant frameworks (consulting, risk management, change management)
- [ ] Identify 2-3 realistic case studies (industry-specific scenarios)
- [ ] List cross-linked related prompts

**Phase 2: Prompt Development (6-8 hours)**
- [ ] Write executive-level persona definition (credentials, methodology expertise)
- [ ] Integrate 3-5 business frameworks with templates
- [ ] Create structured output formats (markdown report + JSON schema)
- [ ] Develop 2-3 detailed case studies (1000+ words each with full input/output)
- [ ] Add governance metadata section:
  - [ ] `approval_required`
  - [ ] `stakeholder_impact`
  - [ ] `data_classification`
  - [ ] `risk_level`
  - [ ] `regulatory_scope` (if applicable)
  - [ ] `retention_period`

**Phase 3: Quality Assurance (2-3 hours)**
- [ ] Test prompt with realistic scenarios (validate output quality)
- [ ] Peer review by domain expert (strategy consultant, risk analyst, etc.)
- [ ] Cross-check against governance prompts (ensure Tier 1 quality)
- [ ] Validate all cross-links (ensure related prompts exist and are linked)
- [ ] Spell-check and grammar review

**Phase 4: Documentation (1-2 hours)**
- [ ] Update changelog with version history
- [ ] Add "Related Prompts" section with cross-links
- [ ] Create or update framework documentation (if new frameworks added)
- [ ] Add to appropriate workflow documentation (SDLC blueprint, incident response playbook)

---

## Success Metrics

### Quality Metrics (Per Prompt):
- ✅ **Persona**: Executive-level definition with credentials (pass/fail)
- ✅ **Frameworks**: 3-5 business frameworks integrated (count)
- ✅ **Governance Metadata**: All required fields present (pass/fail)
- ✅ **Case Studies**: 2-3 detailed examples with 1000+ words each (count, word count)
- ✅ **Structured Outputs**: Markdown report template + JSON schema (pass/fail)
- ✅ **Cross-Links**: 3+ related prompts linked (count)
- ✅ **SDLC Integration**: Usage guidance for applicable phases (pass/fail)

### Business Impact Metrics (Post-Uplift):
- **Adoption Rate**: % increase in prompt usage (track via app.py analytics)
- **User Satisfaction**: Star ratings, feedback comments
- **Quality Rating**: Self-assessed score (5/10 → 9/10 target)
- **Workflow Integration**: # of references in SDLC blueprint and incident response playbook

---

## Risk & Mitigation

### Risk 1: Scope Creep (Effort Exceeds Estimate)
**Probability**: Medium  
**Impact**: High (timeline delay)  
**Mitigation**:
- Use governance prompts as templates (reduce research time)
- Time-box research phase (max 3 hours per prompt)
- Defer "nice-to-have" features to v2.0 (e.g., additional case studies)

### Risk 2: Domain Expertise Gap (Lack of Business Consulting Knowledge)
**Probability**: Medium  
**Impact**: Medium (quality issues)  
**Mitigation**:
- Research frameworks via authoritative sources (McKinsey Quarterly, HBR, Gartner)
- Peer review by domain experts (request feedback from business consultants)
- Use AI (Claude/GPT) to generate case study drafts, then refine

### Risk 3: Inconsistent Quality Across Batches
**Probability**: Low  
**Impact**: High (failed quality goal)  
**Mitigation**:
- Establish quality checklist (use for all prompts)
- Conduct mid-batch review (after first prompt in each batch, validate approach)
- Peer review all prompts before finalizing batch

---

## Appendix: Scoring Rubric (Tier Assessment)

### Tier 1 (9-10/10): Gold Standard
- ✅ Executive-level persona with credentials and methodology expertise
- ✅ 3-5+ business frameworks integrated (Porter's, SWOT, ADKAR, etc.)
- ✅ Comprehensive governance metadata (approval, risk, regulatory scope, retention)
- ✅ 2-3+ detailed case studies (1000+ words each, realistic scenarios)
- ✅ Structured output formats (markdown report + JSON schema)
- ✅ Cross-linked to 3+ related prompts
- ✅ SDLC or workflow integration guidance
- ✅ Quantified outcomes (cost savings, revenue growth, time reduction)
- ✅ Escalation protocols and decision trees

**Examples**: `security-incident-response.md`, `legal-contract-review.md`

### Tier 2 (7-8/10): Strong Quality
- ✅ Clear persona definition (some methodology expertise)
- ✅ 1-2 frameworks integrated
- ✅ Partial governance metadata (approval, risk level)
- ✅ 1-2 case studies (500-1000 words)
- ✅ Structured prompt format
- ✅ Some cross-links (1-2 related prompts)
- ❌ Missing: Detailed governance, multiple frameworks, workflow integration

**Example**: `business-strategy-analysis.md` (current state)

### Tier 3 (5-6/10): Acceptable Quality
- ✅ Basic persona ("You are a consultant...")
- ✅ Clear prompt structure
- ✅ Example usage section
- ❌ Missing: Frameworks, governance metadata, detailed case studies, cross-links

**Examples**: Most current business prompts (`strategic-planning-consultant.md`, `management-consulting-expert.md`, etc.)

### Tier 4 (3-4/10): Needs Improvement
- ✅ Placeholder-heavy prompt
- ❌ Missing: Persona, frameworks, examples, governance

### Tier 5 (1-2/10): Minimal Quality
- ❌ Generic prompt, no structure, no examples

---

## Next Steps

1. **Approval**: Review and approve uplift plan (stakeholders: repository maintainers, contributors)
2. **Kickoff**: Schedule Batch 1 kickoff (Week 1, Day 1)
3. **Assign**: Assign uplift tasks to contributors (1-2 contributors per batch)
4. **Execute**: Implement Batch 1 (Strategic Planning Consultant, Management Consulting Expert, Business Strategy Analysis)
5. **Review**: Mid-batch review (after first prompt, validate quality approach)
6. **Iterate**: Complete Batch 1, conduct retrospective, adjust approach for Batch 2

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-17 | Initial uplift plan created using Tree-of-Thoughts analysis (3 branches evaluated, Branch B + A selected) |

---

**Maintained by**: [Repository Contributors](../CONTRIBUTING.md)  
**Contact**: Submit feedback via GitHub Issues or Pull Requests

---

## Contributors Welcome

This uplift plan is a living document. If you have expertise in:
- Management consulting (McKinsey, BCG, Bain frameworks)
- Enterprise risk management (ISO 31000, COSO ERM)
- Change management (Prosci ADKAR, Kotter's 8-Step)
- Digital transformation
- Business process reengineering

Please contribute! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
