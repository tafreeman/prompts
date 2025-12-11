---
title: "ReAct: OSINT & Cyber Resource Gathering"
shortTitle: "OSINT Resource Gathering"
intro: "ReAct pattern for iteratively finding, verifying, and cataloging OSINT, SOCMINT, and Cyber tools and resources."
type: "how_to"
difficulty: "advanced"
audience:
  - "security-researcher"
  - "intelligence-analyst"
  - "red-team"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "osint"
  - "socmint"
  - "cybersecurity"
  - "research"
  - "react"
author: "Prompts Library Team"
version: "2.0"
date: "2025-11-30"
governance_tags:
<<<<<<< HEAD
  - "security-tools"
  - "requires-verification"
dataClassification: "public"
=======
  - "PII-safe"
  - "requires-human-review"
  - "audit-required"
dataClassification: "internal"
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18
reviewStatus: "draft"
effectivenessScore: 4.8
---
# ReAct: OSINT & Cyber Resource Gathering

---

## Description

<<<<<<< HEAD
This prompt utilizes the ReAct (Reasoning + Acting) pattern to systematically gather, verify, and catalog resources for OSINT (Open Source Intelligence), SOCMINT (Social Media Intelligence), and Cybersecurity. Unlike simple search, this prompt enforces a rigorous cycle of finding a resource, verifying its credibility/freshness, and categorizing it within a larger library of tools.
=======
ReAct (Reasoning + Acting) pattern specialized for document search and synthesis combines iterative reasoning with document retrieval actions. Unlike standard RAG which retrieves documents once, ReAct allows the AI to reason about what information is needed, search for it, analyze the results, and iteratively refine its search strategy. This creates a transparent research process ideal for complex questions requiring information from multiple sources with strategic retrieval.

---

## Research Foundation

This technique combines two foundational approaches:

**Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022).** "ReAct: Synergizing Reasoning and Acting in Language Models." *International Conference on Learning Representations (ICLR) 2023*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020).** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems (NeurIPS) 33*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

Yao et al. demonstrated that interleaving reasoning traces with task-specific actions enables models to dynamically refine their information gathering strategy. Lewis et al. showed that grounding responses in retrieved documents improves factual accuracy and reduces hallucination. This prompt combines both approaches for strategic, multi-step document research.
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18

---

## Use Cases

- Building a curated library of OSINT tools for a specific domain (e.g., "Instagram Investigations").
- Gathering Cyber Threat Intelligence (CTI) feeds and repositories.
- Finding and verifying new SOCMINT utilities on GitHub.
- Creating "Awesome Lists" of cybersecurity resources.
- Vetting tools for operational security (OPSEC) risks before inclusion.

---

## Prompt

```text
You are an expert OSINT and Cybersecurity Intelligence Analyst using the ReAct (Reasoning + Acting) pattern to build a high-quality library of resources.

**Objective**: Gather, verify, and catalog a set of knowledge, repositories, websites, and tools for: [TOPIC]

**Context**: [BACKGROUND_INFORMATION]

**Available Research Tools**:
1. **web_search**: Broad search for tools, blogs, and directories.
   - Parameters: {query: string, site_filter: string (optional)}
2. **github_search**: Specific search for code repositories and tools.
   - Parameters: {query: string, language: string, min_stars: integer}
3. **verify_resource**: Check a resource's health, update status, and reputation.
   - Parameters: {url: string, check_type: "freshness"|"security"|"reputation"}
4. **find_alternatives**: Find similar tools to a given resource.
   - Parameters: {tool_name: string, category: string}

**Instructions**:
Use the Thought → Action → Observation → Synthesis cycle to build the library.

For each cycle:

**Thought [N]**: 
- What type of resource am I looking for next? (Tool, Guide, Dataset, Community)
- How do I verify if this resource is still active and safe?
- Does this fill a gap in the current collection?

**Action [N]**:
Tool: [TOOL_NAME]
Parameters: { ... }

[SYSTEM PROVIDES RESULTS]

**Observation [N]**: 
- What resources did I find?
- Are they maintained (last commit < 6 months)?
- Are there red flags (malware reports, abandoned)?

**Synthesis [N]**:
- Is this resource worthy of inclusion?
- How should it be categorized?
- What is the next logical gap to fill?

---

Continue until you have a comprehensive set. Then provide:

**Final Deliverable**:

## [TOPIC] Resource Library

### 1. Primary Tools & Repositories
| Name | Type | URL | Description | Last Verified |
|------|------|-----|-------------|---------------|
| ...  | CLI/Web | ... | ...         | YYYY-MM-DD    |

### 2. Knowledge Bases & Guides
- **[Title]** ([URL]): Brief summary of why this guide is valuable.

### 3. Key Data Sources
- **[Source Name]**: Description of the data provided.

<<<<<<< HEAD
### 4. Gaps & Limitations
- What areas are still lacking good public tools?
- Any OPSEC warnings for these specific tools?

**Research Summary**:
Briefly explain your methodology and how you vetted these resources.
```

## Variables

- `[TOPIC]`: The specific OSINT/Cyber domain (e.g., "Telegram Investigations", "Cloud Forensics").
- `[BACKGROUND_INFORMATION]`: Context on why this collection is being built (e.g., "Preparing for a CTF", "Setting up a new SOC").

## Example Usage

**Input:**

```text
**Objective**: Gather resources for **Instagram SOCMINT**.
**Context**: Need a set of working tools for a new investigation team. Focus on Python scripts and active web viewers.
```
=======
**Key Requirements**:
1. Think strategically about each search
2. Use different search strategies (semantic, keyword, related docs) as appropriate
3. Cite all claims with document IDs
4. Synthesize information across multiple documents
5. Be explicit about search refinements
6. Acknowledge gaps in available documentation
```text
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18

**Output:**

```text
**Thought 1**: I need to find active Python-based tools for Instagram. Many old tools (like Instaloader forks) are broken due to API changes. I will start by searching GitHub for recently updated repositories.

**Action 1**:
Tool: github_search
Parameters: {
  "query": "instagram osint",
  "language": "python",
  "min_stars": 100
}

**Observation 1**:
Found:
1. `Instaloader` (Active, high stars) - Downloads photos/metadata.
2. `Osintgram` (Active, powerful) - Interactive shell for analysis.
3. `Toutatis` (Active) - Extract info from phone numbers/emails.
4. `InstaPy` (Deprecated/Botting focused) - Not suitable for pure OSINT.

**Synthesis 1**: `Instaloader` and `Osintgram` are core tools. `Toutatis` is excellent for attribution. I need to verify if `Osintgram` is currently working as IG updates often break it. I also need web-based viewers for passive reconnaissance without login.

**Thought 2**: Now I will look for web-based Instagram viewers that don't require an account (good for OPSEC).

**Action 2**:
Tool: web_search
Parameters: {
  "query": "best instagram anonymous viewer 2025 osint",
  "site_filter": "-reddit.com"
}

... [Cycles Continue] ...

**Final Deliverable**:

## Instagram SOCMINT Resource Library

### 1. Primary Tools & Repositories
| Name | Type | URL | Description | Last Verified |
|------|------|-----|-------------|---------------|
| Instaloader | Python | github.com/instaloader/instaloader | Robust media/metadata downloader. | 2025-11-01 |
| Osintgram | Python | github.com/Datalux/Osintgram | Interactive shell for deep analysis. | 2025-10-15 |
| Toutatis | Python | github.com/megadose/toutatis | Retrieve info from emails/phones. | 2025-09-20 |

### 2. Web Viewers (Passive)
- **Imginn**: View stories/posts without login.
- **Picuki**: Editor/Viewer, good for quick checks.

<<<<<<< HEAD
### 4. Gaps & Limitations
- **Private Profiles**: No public tool currently bypasses private profile restrictions reliably.
- **API Limits**: Aggressive use of Instaloader will trigger IP bans. Use proxies.
```
=======
**Phase 4: Go-Live & Handoff (Week 4-5)**
- Production cutover
- Hypercare support (2 weeks)
- Success metrics baseline [Doc_M003]
- Transition to standard support

**Synthesis 2**: Excellent! I now have the complete framework. I can see specific document references for each phase. The compliance aspect is covered in Phase 2 with Doc_C019 "Compliance validation". For Fortune 500 customers with data residency requirements, I need to get details on:
1. Doc_L008 (Data Processing Agreement)
2. Doc_C019 (Compliance validation)
3. Doc_S015 (Security audit)

Let me search for compliance and data residency requirements specifically.

---

**Thought 3**: Since the customer has "strict data residency and compliance requirements," I need to understand what compliance validation entails and whether we have specific processes for data residency. Let me search for compliance-related documents with focus on data residency.

**Action 3**:
Tool: keyword_search
Parameters: {
  "keywords": ["data residency", "compliance", "GDPR", "SOC 2"],
  "boolean_operator": "OR"
}

**Observation 3**:
[System returns:]
1. Doc_C019 - "Enterprise Compliance Validation Checklist"
   - Contains: GDPR, SOC 2, ISO 27001, HIPAA validation steps
   
2. Doc_L008 - "Data Processing Agreement (DPA) Template"
   - Standard DPA with EU data residency clauses
   
3. Doc_I002 - "Data Residency Configuration Guide"
   - Technical setup for region-specific data storage
   - Covers US, EU, APAC, UK regions
   
4. Doc_C021 - "Compliance Certification Matrix"
   - Lists which certifications apply to which regions

**Synthesis 3**: Perfect! Now I have the compliance documentation. Doc_I002 is critical for technical data residency setup. I should fetch Doc_C019 to understand the complete compliance validation process, and I need details on the technical setup (Doc_E012) and SSO integration (Doc_T022) since those are typically blocking items.

---

**Thought 4**: I have most of the pieces, but I need to understand the critical path items that could delay onboarding. Let me fetch the compliance validation checklist (Doc_C019) and the technical infrastructure setup (Doc_E012) to provide comprehensive guidance on timeline and requirements.

**Action 4**:
Tool: document_fetch
Parameters: {
  "document_id": "Doc_C019"
}

**Observation 4**:
[System returns:]
Document: "Enterprise Compliance Validation Checklist"

**Required for Fortune 500 / Regulated Industry Customers**:

**Pre-Kickoff Requirements**:
- Data Processing Agreement (DPA) signed [Doc_L008]
- Security questionnaire completed [Form_SEC_001]
- Data classification review [Doc_D007]

**Technical Compliance**:
- Data residency configuration [Doc_I002]
  - Must specify region during provisioning
  - Cannot be changed post-deployment
- Encryption at rest validation
- Encryption in transit validation
- Access logging enabled
- Audit trail configuration

**Certifications Verification** [Doc_C021]:
- SOC 2 Type II (annual)
- ISO 27001 (required for EU customers)
- GDPR compliance attestation
- HIPAA (if healthcare data)

**Timeline**: Add 1-2 weeks to standard onboarding for compliance validation

**Synthesis 4**: Now I have comprehensive compliance requirements. I have enough information to provide a complete answer covering all three aspects: technical setup, training, and compliance. Let me compile the final answer with proper citations.

---

**Final Answer**:

## Complete Enterprise Customer Onboarding Process

Your enterprise onboarding follows a **4-phase process spanning 5-7 weeks** for customers with compliance requirements [Doc_E001]. For your Fortune 500 customer with data residency requirements, plan for **6-7 weeks** due to additional compliance validation [Doc_C019].

### Phase 1: Pre-Kickoff (Week -1 to 0)

**Legal & Compliance Setup**:
1. **Data Processing Agreement (DPA)**: Must be signed before technical setup begins [Doc_L008]
   - Use standard DPA template with EU data residency clauses if applicable
   - Legal team handles this

2. **Security Assessment**: Customer completes security questionnaire [Doc_C019]
   - Form SEC_001 (typically takes 3-5 business days)
   
3. **Data Classification Review**: Determine data sensitivity levels [Doc_C019]
   - Critical for compliance validation later

**Team Assignment**:
- Customer Success Manager assigned
- Kickoff meeting scheduled with customer stakeholders [Doc_E001]

### Phase 2: Technical Setup (Week 1-3, +1 week for compliance)

**Infrastructure Provisioning** [Doc_E012]:
1. Environment creation (dev, staging, production)
2. **Data Residency Configuration** [Doc_I002]:
   - ⚠️ **CRITICAL**: Region must be specified during initial provisioning
   - Cannot be changed post-deployment
   - Options: US, EU, APAC, UK
   - For Fortune 500 with strict requirements, confirm region with customer legal team

3. **SSO/SAML Integration** [Doc_T022]:
   - Required for enterprise customers
   - Customer provides identity provider metadata
   - Timeline: 1-2 weeks (depends on customer IT responsiveness)

4. **Security Configuration** [Doc_S015]:
   - Security audit completion
   - Encryption validation (at rest and in transit)
   - Access logging enabled
   - Audit trail configuration

**Compliance Validation** [Doc_C019]:
- SOC 2 Type II attestation provided
- ISO 27001 certification (required for EU customers)
- GDPR compliance attestation
- HIPAA compliance if healthcare data involved

**Data Migration** [Doc_D004]:
- Migration planning if customer has existing data
- Usually runs parallel to technical setup

### Phase 3: Training & Enablement (Week 2-4)

**Administrator Training** [Doc_T005]:
- 8-hour comprehensive training (can be split across 2 days)
- Covers: user management, security settings, integrations, reporting

**End-User Training** [Doc_T006]:
- 4-hour training for end users
- Delivered to customer's training team who can cascade

**Custom Workflow Setup** [Doc_T011]:
- Configure customer-specific workflows
- Requires customer business analyst participation

**Champion Program** [Doc_T015]:
- Identify 3-5 power users to become internal champions
- Additional training and ongoing support

### Phase 4: Go-Live & Handoff (Week 4-5, or Week 5-7 with compliance)

**Production Cutover**:
- Coordinated go-live date
- Migration execution (if applicable)

**Hypercare Support**:
- 2 weeks of elevated support [Doc_E001]
- Daily check-ins with customer
- Rapid response SLA

**Success Metrics & Handoff** [Doc_M003]:
- Baseline metrics established
- Transition to standard Customer Success cadence

## Critical Path Items (Can Delay Onboarding)

1. **Data Processing Agreement** - Legal review can take 1-2 weeks
2. **Security Questionnaire** - Customer completion time varies (3-10 days typically)
3. **SSO/SAML Integration** - Depends on customer's IT team availability
4. **Data Residency Decision** - Must be made before provisioning starts

## Coordination Required Across Teams

| Team | Phase | Key Deliverables |
|------|-------|------------------|
| Legal | Pre-Kickoff | DPA signature [Doc_L008] |
| IT/DevOps | Technical Setup | Environment provisioning, data residency config [Doc_E012, Doc_I002] |
| Security | Technical Setup | Security audit, compliance validation [Doc_S015, Doc_C019] |
| Training | Training & Enablement | Admin/user training delivery [Doc_T005, Doc_T006] |
| Customer Success | All Phases | Overall coordination, kickoff, handoff [Doc_E001] |
| Support | Go-Live | Hypercare support (2 weeks) |

## Recommended Immediate Actions

1. **Today**: Sales team sends DPA template [Doc_L008] to customer legal
2. **This Week**: 
   - Customer Success Manager assigned
   - Security questionnaire (Form SEC_001) sent to customer
   - Kickoff meeting scheduled
3. **Before Kickoff**: 
   - Confirm data residency requirements with customer
   - Identify customer's identity provider for SSO integration

**Citations**:
- **Doc_E001**: Enterprise Onboarding Master Checklist - Overall 4-phase process framework
- **Doc_E012**: Technical Infrastructure Setup for Enterprise - IT provisioning steps and timeline
- **Doc_T005**: Enterprise Training Program Overview - Admin training details
- **Doc_T006**: End-User Training Program - User training curriculum
- **Doc_L008**: Data Processing Agreement (DPA) Template - Legal compliance document
- **Doc_C019**: Enterprise Compliance Validation Checklist - Compliance requirements for Fortune 500 customers
- **Doc_I002**: Data Residency Configuration Guide - Technical setup for region-specific data storage
- **Doc_T022**: SSO/SAML Integration Guide (referenced in Doc_E001)
- **Doc_S015**: Security Audit Process (referenced in Doc_E001)

**Research Path Summary**:
I started with a broad semantic search for enterprise onboarding, which identified the master checklist (Doc_E001). I then fetched that document to understand the complete framework. Based on the customer's compliance requirements, I conducted a keyword search for data residency and compliance documentation, which revealed the specific compliance validation process (Doc_C019) and data residency configuration guide (Doc_I002). This multi-step approach ensured I covered all three aspects: technical setup, training, and compliance requirements.

**Confidence Assessment**: **High**

**Justification**: 
- Found comprehensive master checklist that provides authoritative process framework
- Retrieved specific documents for each major component (technical, training, compliance)
- All critical aspects of the question are addressed with specific document citations
- Timeline estimates are grounded in documented processes
- Data residency requirements (customer's specific concern) are well-documented

**Information Gaps**: None significant for initial planning

**Suggested Next Steps**:
- Fetch Doc_T022 (SSO/SAML Integration Guide) for technical team
- Review Doc_D004 (Data Migration Planning) if customer has existing data to migrate
- Fetch Doc_M003 (Success Metrics) to understand how success will be measured post-onboarding
```text

---

## Tips

- **Strategic search**: Start broad, then narrow based on what you find
- **Use multiple search types**: Combine semantic search (concepts) with keyword search (specific terms)
- **Follow document references**: Documents often reference other related documents - fetch those
- **Iterative refinement**: Each search should be informed by previous results
- **Cite everything**: Every fact needs a document ID citation
- **Synthesize as you go**: Don't just accumulate - connect information across documents
- **Know when to stop**: Once you have comprehensive coverage, provide the answer
- **Assess gaps honestly**: If information is missing, say so and suggest what would help

## When to Use ReAct Document Search vs Standard RAG

| Scenario | ReAct Document Search | Standard RAG |
|----------|----------------------|--------------|
| Simple lookup | ✗ (overkill) | ✓ |
| Complex multi-part question | ✓ | ✗ |
| Need to refine search strategy | ✓ | ✗ |
| Information scattered across docs | ✓ | Partial |
| Need audit trail of research | ✓ | ✗ |
| Simple Q&A from known source | ✗ | ✓ |
| Cross-referencing requirements | ✓ | ✗ |
| Strategic exploration needed | ✓ | ✗ |

## Search Strategy Patterns

### Pattern 1: Broad-to-Narrow

```text
1. Semantic search with broad query → Get overview
2. Identify most relevant document ID
3. Fetch full document → See references
4. Keyword search for specific terms → Get details
5. Synthesize complete answer
```text

### Pattern 2: Keyword-then-Expand

```text
1. Keyword search for specific term → Find exact matches
2. Identify relevant document
3. Use related_documents tool → Find connected docs
4. Semantic search for concepts → Fill gaps
5. Synthesize with cross-references
```text

## Output Schema (JSON)

For automation and audit trails:

```json
{
  "question": "...",
  "research_cycles": [
    {
      "cycle": 1,
      "thought": "...",
      "action": {
        "tool": "semantic_search",
        "parameters": {}
      },
      "observation": {
        "documents_found": 5,
        "top_relevance_score": 0.94,
        "key_documents": ["Doc_E001", "Doc_E012"]
      },
      "synthesis": "..."
    }
  ],
  "final_answer": "...",
  "citations": [
    {
      "doc_id": "Doc_E001",
      "title": "...",
      "relevance": "..."
    }
  ],
  "research_path_summary": "...",
  "confidence": {
    "level": "high|medium|low",
    "justification": "..."
  },
  "information_gaps": [],
  "documents_retrieved": 8,
  "total_cycles": 4
}
```text

---

## Related Prompts

- [RAG: Document Retrieval and Citation](rag-document-retrieval.md) - Standard RAG pattern
- [ReAct: Tool-Augmented Reasoning](react-tool-augmented.md) - General ReAct pattern with tools
- [Chain-of-Thought: Detailed](chain-of-thought-detailed.md) - Pure reasoning without retrieval
- [Reflection: Self-Critique](reflection-self-critique.md) - Quality validation for research

---

## Governance Notes

- **PII Safety**: Documents may contain PII
  - Implement access control on document retrieval
  - Log all searches with user ID and timestamp
  - Redact PII in responses if policy requires
- **Human Review Required For**:
  - Legal document interpretation
  - Compliance guidance
  - High-impact decisions (>$50K)
  - Customer-facing communications
- **Audit Trail**: The Thought-Action-Observation-Synthesis cycle provides built-in audit trail
  - Log all research cycles
  - Preserve search queries and results
  - Track which documents were accessed
  - Record timestamps for compliance
- **Document Access Control**:
  - Respect document permissions and classification levels
  - Filter search results based on user access level
  - Log unauthorized access attempts

## Platform Adaptations

### GitHub Copilot with Workspace Search

```text
@workspace use ReAct pattern to research: [question]

Follow the Thought → Action → Observation → Synthesis cycle:
1. Think about what information you need
2. Search for relevant files
3. Analyze the results
4. Refine your search based on findings
```text
```text

### Custom ReAct Document Research Pipeline

```python
def react_document_research(question, max_cycles=8):
    """ReAct pattern for document research"""
    
    research_trail = []
    documents_found = {}
    
    for cycle in range(1, max_cycles + 1):
        # Thought: What do I need next?
        thought = generate_thought(
            question=question,
            research_trail=research_trail,
            documents_found=documents_found,
            cycle=cycle
        )
        
        # Action: Choose and execute search
        action = generate_action(thought)
        tool_name = action["tool"]
        params = action["parameters"]
        
        # Execute search
        results = execute_tool(tool_name, params)
        
        # Observation: Analyze results
        observation = analyze_results(
            results=results,
            previous_findings=documents_found
        )
        
        # Update documents found
        for doc in observation["relevant_docs"]:
            documents_found[doc["id"]] = doc
        
        # Synthesis: Assess progress
        synthesis = synthesize_progress(
            thought=thought,
            observation=observation,
            question=question,
            documents_found=documents_found
        )
        
        # Record cycle
        research_trail.append({
            "cycle": cycle,
            "thought": thought,
            "action": action,
            "observation": observation,
            "synthesis": synthesis
        })
        
        # Check if ready for final answer
        if synthesis["ready_to_answer"]:
            break
    
    # Generate final answer
    final_answer = generate_answer(
        question=question,
        documents=documents_found,
        research_trail=research_trail
    )
    
    return {
        "answer": final_answer,
        "citations": list(documents_found.keys()),
        "research_trail": research_trail,
        "total_cycles": len(research_trail)
    }
```text

### Contradictory Information

```text
**Synthesis [N]**: I found contradictory information:
- Doc_A states: [X]
- Doc_B states: [Y]

I need to:
1. Check document dates (Doc_A may be outdated)
2. Look for newer policy documents
3. Note the contradiction in my final answer
```text
```sql
>>>>>>> 7dc5218e3127cfdaacb10749fd0b592524b03b18
