---
name: Rag Document Retrieval
description: # RAG: Document Retrieval and Citation Framework
type: how_to
---

# RAG: Document Retrieval and Citation Framework

## Description

Retrieval-Augmented Generation (RAG) is a pattern that grounds AI responses in specific documents or knowledge bases. This template provides a structured approach to chunking documents, retrieving relevant context, and generating answers with proper citations. Essential for enterprise applications where accuracy, attribution, and auditability are critical.

## Use Cases

- Internal documentation Q&A systems
- Code repository search and explanation
- Policy and compliance document queries
- Customer support knowledge base integration
- Research paper analysis and summarization
- Legal document review with citations
- Technical troubleshooting from logs and docs

## Variables

- `[USER_QUESTION]`: The specific question to answer using retrieved documents
- `[BACKGROUND_INFORMATION]`: Context about the user's goal, constraints, or situation
- `[DOC_X_ID]`: Unique identifier for each retrieved document chunk
- `[DOC_X_SOURCE]`: Source location (file path, URL, database record)
- `[DOC_X_CONTENT]`: The actual text content of the retrieved chunk
- `[DOC_X_SCORE]`: Relevance/similarity score from retrieval system

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

## Prompt

```text
You are a precise information retrieval assistant with access to a document knowledge base.

### User Question
{{USER_QUESTION}}

### Background Context
{{BACKGROUND_INFORMATION}}

### Retrieved Documents
{% for doc in documents %}
<document id="{{doc.id}}" source="{{doc.source}}" score="{{doc.score}}">
{{doc.content}}
</document>
{% endfor %}

### Instructions
1. Answer the user's question using ONLY information from the retrieved documents
2. Cite every factual claim with [Doc_X] format
3. If information is insufficient, clearly state what's missing
4. Provide a confidence level (High/Medium/Low) with justification

### Response Format
**Answer:** [Your grounded response with citations]

**Citations:**
| Doc ID | Source | Usage |
| ------ | ------ | ----- |
| [id] | [source] | [what information was used] |

**Confidence:** [High/Medium/Low]
**Justification:** [Why this confidence level]

**Information Gaps:** [What the documents don't cover]
```

## Example

**Input:**

```yaml
USER_QUESTION: "What are our API rate limits?"
BACKGROUND_INFORMATION: "Customer needs to do a bulk data export"
documents:
  - id: Doc_1
    source: /docs/api/rate-limiting.md
    score: 0.95
    content: "Standard tier: 1,000 requests/hour. Enterprise tier: 10,000 requests/hour."
  - id: Doc_2
    source: /docs/api/error-codes.md
    score: 0.89
    content: "HTTP 429 indicates rate limit exceeded. Use Retry-After header."
```

**Output:**

```markdown
**Answer:** Our API has tiered rate limits [Doc_1]:
- Standard tier: 1,000 requests/hour
- Enterprise tier: 10,000 requests/hour

If limits are exceeded, you'll receive HTTP 429 [Doc_2]. Check the Retry-After header for wait time.

**Citations:**
| Doc ID | Source | Usage |
| ------ | ------ | ----- |
| Doc_1 | /docs/api/rate-limiting.md | Rate limit thresholds |
| Doc_2 | /docs/api/error-codes.md | Error handling guidance |

**Confidence:** High
**Justification:** Both documents directly address the question with specific numbers.

**Information Gaps:** Documents don't specify if temporary limit increases are available for bulk operations.
```

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
