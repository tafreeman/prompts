---
title: 'RAG: Document Retrieval and Citation'
shortTitle: RAG Document Retrieval
intro: Retrieval-Augmented Generation pattern for grounding AI responses in specific
  documents with proper citations and attribution.
type: how_to
difficulty: advanced
audience:

- senior-engineer
- solution-architect

platforms:

- claude
- chatgpt
- github-copilot
- azure-openai

topics:

- rag
- retrieval

author: Prompts Library Team
version: '1.0'
date: '2025-11-17'
governance_tags:

- PII-safe
- requires-human-review
- audit-required

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# RAG: Document Retrieval and Citation Framework

---

## Description

Retrieval-Augmented Generation (RAG) is a pattern that grounds AI responses in specific documents or knowledge bases. This template provides a structured approach to chunking documents, retrieving relevant context, and generating answers with proper citations. Essential for enterprise applications where accuracy, attribution, and auditability are critical.

---

## Research Foundation

This technique is based on the paper:
**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020).** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems (NeurIPS) 33*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

Lewis et al. introduced RAG models that combine parametric memory (pre-trained seq2seq model) with non-parametric memory (dense vector index of Wikipedia accessed with a pre-trained neural retriever). This approach allows models to access and leverage knowledge in a more modular and interpretable way than storing all knowledge in model parameters, achieving state-of-the-art results on knowledge-intensive tasks while providing transparency through retrieved document citations.

---

## Use Cases

- Internal documentation Q&A systems
- Code repository search and explanation
- Policy and compliance document queries
- Customer support knowledge base integration
- Research paper analysis and summarization
- Legal document review with citations
- Technical troubleshooting from logs and docs

---

## Prompt

```text
You are an AI assistant using Retrieval-Augmented Generation (RAG) to answer questions grounded in specific documents.

**Question**: [USER_QUESTION]

**Context**: [BACKGROUND_INFORMATION]

**Retrieved Documents**:
[SYSTEM PROVIDES RETRIEVED CHUNKS]

Document ID: [DOC_1_ID]
Source: [DOC_1_SOURCE]
Content: [DOC_1_CONTENT]
Relevance Score: [DOC_1_SCORE]

Document ID: [DOC_2_ID]
Source: [DOC_2_SOURCE]
Content: [DOC_2_CONTENT]
Relevance Score: [DOC_2_SCORE]

[Additional documents...]

**Instructions**:

1. **Analyze Retrieved Documents**:
   - Review all provided document chunks
   - Assess relevance to the question
   - Identify key information and relationships
   - Note any contradictions or gaps

2. **Synthesize Answer**:
   - Ground your response ONLY in the provided documents
   - Do NOT use knowledge outside the retrieved context
   - If information is insufficient, explicitly state what's missing
   - Combine information from multiple documents when relevant

3. **Cite Sources**:
   - Every claim must have a citation [Doc_ID]
   - Use inline citations: "The API rate limit is 1000 requests/hour [Doc_2]"
   - If multiple documents support a claim, cite all: [Doc_1, Doc_3]
   - Direct quotes should be in "quotation marks" with citation

4. **Format Response**:

**Answer**:
[Your grounded answer with inline citations]

**Confidence Assessment**:

- **High**: Answer fully supported by multiple documents
- **Medium**: Answer supported but with some gaps
- **Low**: Limited information, significant gaps exist

**Sources Used**:

- [Doc_ID]: Brief description of what information this provided
- [Doc_ID]: Brief description...

**Information Gaps** (if any):

- What additional information would improve this answer
- What questions remain unanswered

**Recommended Follow-up**:

- Suggested additional searches or document retrieval
- Questions to clarify user intent

```text

---

## Variables

- `[USER_QUESTION]`: The specific question to answer using retrieved documents
- `[BACKGROUND_INFORMATION]`: Context about the user's goal, constraints, or situation
- `[DOC_X_ID]`: Unique identifier for each retrieved document chunk
- `[DOC_X_SOURCE]`: Source location (file path, URL, database record)
- `[DOC_X_CONTENT]`: The actual text content of the retrieved chunk
- `[DOC_X_SCORE]`: Relevance/similarity score from retrieval system

---

## Example Usage

**Input:**

```text
You are an AI assistant using Retrieval-Augmented Generation (RAG) to answer questions grounded in specific documents.

**Question**: What is our API rate limiting policy and how do we handle violations?

**Context**: Customer is asking about rate limits because they're planning a bulk data export. Need official policy to provide accurate guidance.

**Retrieved Documents**:

Document ID: Doc_1
Source: /docs/api/rate-limiting.md
Content: "All API endpoints are rate limited to 1000 requests per hour per API key. Enterprise customers with Premium tier receive 10,000 requests per hour. Rate limits reset at the top of each hour UTC."
Relevance Score: 0.95

Document ID: Doc_2
Source: /docs/api/error-codes.md
Content: "HTTP 429 (Too Many Requests) is returned when rate limit is exceeded. The response includes `Retry-After` header indicating seconds until limit resets. Example: `Retry-After: 3600` means retry in 1 hour."
Relevance Score: 0.89

Document ID: Doc_3
Source: /policies/api-usage-policy.md
Content: "Persistent rate limit violations (exceeding limit >5 times in 24 hours) may result in temporary API key suspension. First violation: warning email. Second violation (within 7 days): 24-hour suspension. Third violation: permanent suspension subject to review."
Relevance Score: 0.82

Document ID: Doc_4
Source: /docs/api/authentication.md
Content: "API keys can be generated from the developer dashboard at https://dashboard.example.com/api-keys. Each user can create up to 5 API keys. Keys should be kept secure and never committed to version control."
Relevance Score: 0.41

**Instructions**:
[As specified above]
```

**Expected Output:**

```markdown
## Answer

Based on the retrieved documentation, here's what you need to know about our API rate limiting policy:

### Rate Limits

| Tier | Rate Limit | Reset |
| ------ | ----------- | ------- |
| Standard | 1,000 requests/hour | Top of each hour (UTC) |
| Enterprise (Premium) | 10,000 requests/hour | Top of each hour (UTC) |

> "All API endpoints are rate limited to 1000 requests per hour per API key. Enterprise customers with Premium tier receive 10,000 requests per hour." — [Doc_1: /docs/api/rate-limiting.md]

### When Rate Limit is Exceeded

When you exceed your rate limit, the API returns **HTTP 429 (Too Many Requests)**. The response includes a `Retry-After` header indicating how many seconds until your limit resets [Doc_2].

**Example response header:**
```

Retry-After: 3600  (retry in 1 hour)

```

### Violation Policy

Persistent violations are handled progressively [Doc_3]:

| Violation | Consequence |
| ----------- | ------------- |
| 1st (>5 times in 24h) | Warning email |
| 2nd (within 7 days of 1st) | 24-hour API key suspension |
| 3rd | Permanent suspension (subject to review) |

### Recommendation for Bulk Export

For your bulk data export use case, I recommend:

1. **Check your tier**: If you're on Standard (1,000/hr), consider upgrading to Enterprise (10,000/hr) for bulk operations
2. **Implement rate limiting client-side**: Track requests and pause when approaching the limit
3. **Use the `Retry-After` header**: If you receive a 429, wait the indicated time before retrying
4. **Spread requests**: Instead of bursting, distribute requests evenly across the hour

---

## Citations

| Doc ID | Source | Relevance | Usage |
| -------- | -------- | ----------- | ------- |
| Doc_1 | /docs/api/rate-limiting.md | 0.95 | Rate limit thresholds and tiers |
| Doc_2 | /docs/api/error-codes.md | 0.89 | HTTP 429 handling and Retry-After header |
| Doc_3 | /policies/api-usage-policy.md | 0.82 | Violation escalation policy |
| Doc_4 | /docs/api/authentication.md | 0.41 | *(Not used — below relevance threshold, not directly relevant to rate limiting question)* |

## Confidence Assessment

**Confidence Level**: HIGH

**Justification**: 

- Three highly relevant documents (>0.8 relevance) directly address the question
- All factual claims are grounded in retrieved documents
- No contradictions between sources
- Policy language is clear and unambiguous

## Information Gaps

The retrieved documents do not cover:

- Whether rate limits can be temporarily increased for planned bulk operations
- Exact timing of rate limit reset (e.g., is it exactly on the hour, or rolling?)
- Whether Enterprise tier has options beyond 10,000/hr

## Recommended Follow-up

If the customer needs to exceed standard limits for their bulk export, suggest:

1. Contact sales about temporary limit increase
2. Explore batch/export API endpoints (may have different limits)
3. Request Enterprise tier upgrade for ongoing high-volume needs

```

---

## Tips

- **Ground firmly**: Never add information not in retrieved documents, even if you "know" it's true
- **Cite everything**: Every factual claim needs a citation. When in doubt, cite.
- **Assess confidence**: Be honest about information gaps. "I don't have that information" is better than guessing.
- **Chunk size matters**: 200-500 token chunks usually work best for retrieval
- **Relevance threshold**: Ignore documents with relevance score <0.5 unless critical
- **Handle contradictions**: If documents contradict, cite both and note the discrepancy
- **Quote vs. paraphrase**: Use direct quotes for policies, legal text, or precise specifications
- **Context window**: Be aware of token limits; prioritize highest-relevance documents

## Document Chunking Best Practices

### For Code Repositories

```text
Chunk by:

- Function/method (including docstring and signature)
- Class definition (with methods)
- Module-level documentation
- README sections

Metadata to include:

- File path
- Language
- Last modified date
- Author (if relevant)

```text

### For Logs/Incident Data

```text
Chunk by:

- Time range (e.g., 5-minute windows)
- Log level groups (errors together)
- Service/component

Metadata to include:

- Timestamp range
- Service name
- Log level
- Error codes (if present)

```text

```text

### Hybrid Search

```python

# Combine semantic + keyword search
semantic_results = vector_db.similarity_search(query, k=10)
keyword_results = bm25_search(query, k=10)

# Merge and rerank
chunks = rerank(semantic_results + keyword_results, top_k=5)

```text

### Contextual Retrieval

```python

# Retrieve chunk + surrounding context
main_chunk = retrieve(query)
previous_chunk = get_previous(main_chunk.id)
next_chunk = get_next(main_chunk.id)

context = f"{previous_chunk}\n{main_chunk}\n{next_chunk}"

```json

## Output Schema (JSON)

For automation pipelines:

```json

{
  "answer": "...",
  "confidence": "high|medium|low",
  "confidence_justification": "...",
  "citations": [
    {
      "doc_id": "Doc_1",
      "source": "/docs/api/rate-limiting.md",
      "relevance_score": 0.95,
      "content_excerpt": "...",
      "usage": "Provided rate limit thresholds"
    }
  ],
  "information_gaps": ["...", "..."],
  "recommended_followup": ["...", "..."],
  "grounding_quality": {
    "all_claims_cited": true,
    "external_knowledge_used": false,
    "contradictions_found": false
  }
}

```text

---

## Governance Notes

- **PII Safety**: Documents may contain PII. Implement:
  - PII detection before indexing
  - Access control on document retrieval
  - Redaction in responses if needed
- **Human Review Required For**:
  - Legal document interpretation
  - Compliance policy guidance
  - Security-sensitive information disclosure
  - Decisions with >$50K impact
- **Audit Trail**: Log all retrievals:
  - User question
  - Documents retrieved
  - Answer provided
  - Citations used
  - Timestamp and user ID
- **Data Classification**: Tag documents by sensitivity (Public, Internal, Confidential, Restricted)
- **Retention**: Comply with document retention policies when indexing

## Platform Adaptations

### GitHub Copilot with Retrieval

```text

@workspace search for rate limiting policy and explain with citations

```text

### Custom RAG Pipeline

```python

def rag_answer(question, context=""):
    # 1. Retrieve relevant documents
    chunks = vector_db.similarity_search(
        embed(question),
        k=5,
        filter={"access_level": user.access_level}
    )

    # 2. Format prompt with retrieved context
    prompt = format_rag_prompt(
        question=question,
        context=context,
        documents=chunks
    )

    # 3. Generate grounded answer
    response = llm.generate(prompt)

    # 4. Validate citations
    if not validate_all_claims_cited(response, chunks):
        response = llm.generate(prompt + "\nEnsure all claims are cited.")

    return {
        "answer": response,
        "sources": chunks,
        "confidence": assess_confidence(response, chunks)
    }

```text

---

## Related Prompts

- [ReAct: Document Search and Synthesis](react-doc-search-synthesis.md) - ReAct pattern for RAG

## Error Handling

### Insufficient Retrieved Documents

```text

If fewer than 3 relevant documents (score >0.7) retrieved:

"I found limited information about [topic]. Based on available documents:

[Provide what you can with citations]

To get a better answer, I would need:

- [Specific type of document needed]
- [Specific information missing]

Would you like me to search differently, or can you provide more context?"

```text

### No Relevant Documents Found

```text

"I couldn't find relevant documentation about [topic]. 

Possible reasons:

- Information may not be documented yet
- Different terminology might be used (can you rephrase?)
- Topic may be covered in restricted documents I don't have access to

Would you like me to:

1. Search using different keywords?
2. Escalate to documentation team to add this content?
3. Search in a different document set?"

```text
