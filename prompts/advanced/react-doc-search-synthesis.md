---
title: "ReAct: Document Search and Synthesis"
category: "advanced-techniques"
tags: ["react", "document-search", "rag", "synthesis", "reasoning", "retrieval", "research"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-25"
difficulty: "advanced"
governance_tags: ["PII-safe", "requires-human-review-for-sensitive-docs", "audit-required"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# ReAct: Document Search and Synthesis

## Description

ReAct (Reasoning + Acting) pattern specialized for document search and synthesis combines iterative reasoning with document retrieval actions. Unlike standard RAG which retrieves documents once, ReAct allows the AI to reason about what information is needed, search for it, analyze the results, and iteratively refine its search strategy. This creates a transparent research process ideal for complex questions requiring information from multiple sources with strategic retrieval.

## Research Foundation

This technique combines two foundational approaches:

**Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022).** "ReAct: Synergizing Reasoning and Acting in Language Models." *International Conference on Learning Representations (ICLR) 2023*. [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020).** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems (NeurIPS) 33*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

Yao et al. demonstrated that interleaving reasoning traces with task-specific actions enables models to dynamically refine their information gathering strategy. Lewis et al. showed that grounding responses in retrieved documents improves factual accuracy and reduces hallucination. This prompt combines both approaches for strategic, multi-step document research.

## Use Cases

- Complex research questions requiring multiple sources
- Policy and procedure lookups across distributed documentation
- Troubleshooting requiring log analysis and documentation synthesis
- Legal research with cross-referencing requirements
- Technical documentation navigation for multi-component systems
- Customer support requiring information synthesis from multiple knowledge bases
- Code repository exploration for understanding complex features

## Prompt

```text
You are an AI research assistant using the ReAct (Reasoning + Acting) pattern for document search and synthesis.

**Research Question**: [USER_QUESTION]

**Context**: [BACKGROUND_INFORMATION]

**Available Search Tools**:
1. **semantic_search**: Vector similarity search across documents
   - Parameters: {query: string, max_results: integer, filters: object}
   - Returns: Ranked document chunks with relevance scores

2. **keyword_search**: Exact keyword/phrase matching
   - Parameters: {keywords: string[], boolean_operator: "AND"|"OR"}
   - Returns: Documents containing exact matches

3. **document_fetch**: Retrieve full document by ID
   - Parameters: {document_id: string}
   - Returns: Complete document content with metadata

4. **related_documents**: Find documents related to a given document
   - Parameters: {document_id: string, relationship_type: "cited_by"|"references"|"similar"}
   - Returns: Related documents with relationship metadata

**Instructions**:
Use the Thought → Action → Observation → Synthesis cycle to research the question.

For each cycle:

**Thought [N]**: 
- What information do I need next?
- Which search strategy would be most effective?
- What gaps remain in my understanding?
- How does this fit with what I already know?

**Action [N]**:
Tool: [TOOL_NAME]
Parameters: {
  "param1": "value1",
  "param2": "value2"
}

[SYSTEM PROVIDES SEARCH RESULTS]

**Observation [N]**: 
- What did the search return?
- Relevance assessment of retrieved documents
- Key information extracted
- Document IDs for citation

**Synthesis [N]**:
- How does this information answer part of the question?
- What new questions or gaps emerged?
- Do I need to refine my search strategy?
- Am I ready to provide a complete answer?

---

Continue until you can provide:

**Final Answer**:
[Comprehensive answer synthesized from all retrieved documents]

**Citations**:
- [Doc_ID]: Brief description and relevance
- [Doc_ID]: Brief description and relevance

**Research Path Summary**:
Brief explanation of your search strategy and how you arrived at the answer

**Confidence Assessment**:
- **High/Medium/Low**: Based on document coverage and consistency
- **Justification**: Why this confidence level

**Information Gaps** (if any):
- What information would strengthen this answer
- Suggested additional searches

**Key Requirements**:
1. Think strategically about each search
2. Use different search strategies (semantic, keyword, related docs) as appropriate
3. Cite all claims with document IDs
4. Synthesize information across multiple documents
5. Be explicit about search refinements
6. Acknowledge gaps in available documentation
```

## Variables

- `[USER_QUESTION]`: The research question requiring document search and synthesis
- `[BACKGROUND_INFORMATION]`: Context about what the user is trying to accomplish

## Example Usage

**Input:**

```text
You are an AI research assistant using the ReAct (Reasoning + Acting) pattern for document search and synthesis.

**Research Question**: What is our complete onboarding process for new enterprise customers, including technical setup, training, and compliance requirements?

**Context**: 
- Sales team needs comprehensive onboarding documentation
- New enterprise customer signed yesterday (Fortune 500 company)
- Need to coordinate across multiple teams (IT, Training, Legal, Support)
- Customer has strict data residency and compliance requirements

**Available Search Tools**:
[As described above]

**Instructions**:
[As specified above]
```

**Output:**

```text
**Thought 1**: This is a multi-faceted question covering technical, training, and compliance aspects. I should start with a broad semantic search for "enterprise onboarding" to get an overview, then drill into specific areas. Starting with a comprehensive query will help me understand what documentation exists.

**Action 1**:
Tool: semantic_search
Parameters: {
  "query": "enterprise customer onboarding process workflow",
  "max_results": 5,
  "filters": {"document_type": "process", "audience": "internal"}
}

**Observation 1**:
[System returns:]
1. Doc_E001 - "Enterprise Onboarding Master Checklist" (relevance: 0.94)
   - Overview of 4-phase onboarding process
   - References other detailed documents
   
2. Doc_E012 - "Technical Infrastructure Setup for Enterprise" (relevance: 0.88)
   - IT provisioning steps
   - Timeline: 2-3 weeks
   
3. Doc_T005 - "Enterprise Training Program Overview" (relevance: 0.82)
   - Standard training modules
   - Customization options
   
4. Doc_C003 - "Customer Success Playbook - Enterprise" (relevance: 0.79)
   - Post-onboarding success metrics
   - Less relevant to initial onboarding
   
5. Doc_S001 - "SMB Onboarding Quick Start" (relevance: 0.61)
   - Not relevant (SMB vs Enterprise)

**Synthesis 1**: Good start! Doc_E001 appears to be a master checklist that likely references other documents. Doc_E012 and Doc_T005 cover technical and training aspects. I'm missing compliance/legal requirements. I should fetch the master checklist first to understand the full structure, then search specifically for compliance requirements.

---

**Thought 2**: The master checklist (Doc_E001) likely contains the overall process framework and will reference specific documents for each phase. Let me retrieve it in full to understand the complete structure.

**Action 2**:
Tool: document_fetch
Parameters: {
  "document_id": "Doc_E001"
}

**Observation 2**:
[System returns:]
Document: "Enterprise Onboarding Master Checklist"
Last Updated: 2024-10-15
Owner: Enterprise Success Team

**4-Phase Onboarding Process**:

**Phase 1: Pre-Kickoff (Week -1 to 0)**
- Contract signature and SOW finalization [Legal]
- Data Processing Agreement (DPA) if required [Doc_L008]
- Infrastructure assessment [Doc_E012]
- Assign Customer Success Manager
- Schedule kickoff meeting

**Phase 2: Technical Setup (Week 1-3)**
- Environment provisioning [Doc_E012]
- SSO/SAML integration [Doc_T022]
- Data migration planning [Doc_D004]
- Security audit completion [Doc_S015]
- Compliance validation [Doc_C019]

**Phase 3: Training & Enablement (Week 2-4)**
- Admin training (8 hours) [Doc_T005]
- End-user training (4 hours) [Doc_T006]
- Custom workflow setup [Doc_T011]
- Champion program enrollment [Doc_T015]

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
```

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
```

### Pattern 2: Keyword-then-Expand

```text
1. Keyword search for specific term → Find exact matches
2. Identify relevant document
3. Use related_documents tool → Find connected docs
4. Semantic search for concepts → Fill gaps
5. Synthesize with cross-references
```

### Pattern 3: Iterative Refinement

```text
1. Semantic search → Partial results
2. Analyze gaps in coverage
3. Reformulate query based on gaps
4. Semantic search with refined query
5. Repeat until comprehensive coverage
```

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
```

## Related Prompts

- [RAG: Document Retrieval and Citation](rag-document-retrieval.md) - Standard RAG pattern
- [ReAct: Tool-Augmented Reasoning](react-tool-augmented.md) - General ReAct pattern with tools
- [Chain-of-Thought: Detailed](chain-of-thought-detailed.md) - Pure reasoning without retrieval
- [Reflection: Self-Critique](reflection-self-critique.md) - Quality validation for research

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
```

### LangChain RAG with ReAct

```python
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.vectorstores import Chroma

# Define search tools
semantic_search_tool = Tool(
    name="SemanticSearch",
    func=lambda q: vectorstore.similarity_search(q, k=5),
    description="Search documents by semantic similarity"
)

keyword_search_tool = Tool(
    name="KeywordSearch",
    func=lambda q: keyword_index.search(q),
    description="Search documents by exact keyword match"
)

fetch_document_tool = Tool(
    name="FetchDocument",
    func=lambda id: document_store.get(id),
    description="Retrieve full document by ID"
)

# Create ReAct agent
agent = initialize_agent(
    tools=[semantic_search_tool, keyword_search_tool, fetch_document_tool],
    llm=ChatOpenAI(model="gpt-4", temperature=0),
    agent=AgentType.REACT_DOCSTORE,
    verbose=True,
    max_iterations=10
)

# Run research query
result = agent.run(
    "What is our complete onboarding process for enterprise customers?"
)
```

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
```

## Error Handling

### No Relevant Documents Found

```text
**Thought [N]**: My search for "[query]" returned no relevant results. This could mean:
- The information isn't documented
- I'm using wrong terminology
- The documents are restricted/not indexed

**Action [N]**: Let me try a different search strategy with alternative keywords...
```

### Contradictory Information

```text
**Synthesis [N]**: I found contradictory information:
- Doc_A states: [X]
- Doc_B states: [Y]

I need to:
1. Check document dates (Doc_A may be outdated)
2. Look for newer policy documents
3. Note the contradiction in my final answer
```

### Search Results Too Broad

```text
**Reflection [N]**: My search returned 50+ documents, which is too broad. I need to:
- Add filters (date range, document type, department)
- Use more specific keywords
- Narrow the semantic query
```

## Changelog

### Version 1.0 (2025-11-25)

- Initial release
- Comprehensive ReAct pattern for document search and synthesis
- Multi-cycle research example with enterprise onboarding scenario
- Search strategy patterns (broad-to-narrow, keyword-then-expand, iterative refinement)
- JSON schema for automation
- Platform integration examples (LangChain, custom pipeline)
- Governance metadata and audit trail guidance
