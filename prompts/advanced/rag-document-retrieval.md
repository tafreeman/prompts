---
title: "RAG: Document Retrieval and Citation"
category: "advanced-techniques"
tags: ["rag", "retrieval-augmented-generation", "document-search", "citations", "context", "grounding"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-17"
difficulty: "advanced"
governance_tags: ["PII-safe", "requires-human-review-for-sensitive-docs", "audit-required"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# RAG: Document Retrieval and Citation Framework

## Description

Retrieval-Augmented Generation (RAG) is a pattern that grounds AI responses in specific documents or knowledge bases. This template provides a structured approach to chunking documents, retrieving relevant context, and generating answers with proper citations. Essential for enterprise applications where accuracy, attribution, and auditability are critical.

## Research Foundation

This technique is based on the paper:
**Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020).** "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems (NeurIPS) 33*. [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)

Lewis et al. introduced RAG models that combine parametric memory (pre-trained seq2seq model) with non-parametric memory (dense vector index of Wikipedia accessed with a pre-trained neural retriever). This approach allows models to access and leverage knowledge in a more modular and interpretable way than storing all knowledge in model parameters, achieving state-of-the-art results on knowledge-intensive tasks while providing transparency through retrieved document citations.

## Use Cases

- Internal documentation Q&A systems
- Code repository search and explanation
- Policy and compliance document queries
- Customer support knowledge base integration
- Research paper analysis and summarization
- Legal document review with citations
- Technical troubleshooting from logs and docs

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

```

## Variables

- `[USER_QUESTION]`: The specific question to answer using retrieved documents
- `[BACKGROUND_INFORMATION]`: Context about the user's goal, constraints, or situation
- `[DOC_X_ID]`: Unique identifier for each retrieved document chunk
- `[DOC_X_SOURCE]`: Source location (file path, URL, database record)
- `[DOC_X_CONTENT]`: The actual text content of the retrieved chunk
- `[DOC_X_SCORE]`: Relevance/similarity score from retrieval system

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

**Output:**

```text
**Answer**:

Our API rate limiting policy varies by customer tier. Standard accounts are limited to 1,000 requests per hour per API key, while Enterprise Premium customers receive 10,000 requests per hour [Doc_1]. These limits reset at the top of each hour in UTC timezone [Doc_1].

When rate limits are exceeded, the API returns HTTP 429 (Too Many Requests) status code [Doc_2]. The response includes a `Retry-After` header that specifies the number of seconds until the limit resets. For example, `Retry-After: 3600` indicates you should retry in 1 hour [Doc_2].

For violation handling, we have a progressive enforcement policy. Persistent rate limit violations—defined as exceeding the limit more than 5 times within 24 hours—trigger escalating consequences [Doc_3]:

1. **First violation**: You'll receive a warning email
2. **Second violation within 7 days**: 24-hour API key suspension
3. **Third violation**: Permanent suspension, subject to manual review

All enforcement actions are tracked per API key [Doc_3].

For bulk data export planning, consider:
- Calculate your request volume: If you need more than 1,000 requests/hour, consider upgrading to Enterprise Premium
- Implement retry logic with exponential backoff when you receive 429 responses
- Respect the `Retry-After` header value
- Spread requests evenly across the hour rather than bursting

**Confidence Assessment**: **High**

The retrieved documents comprehensively cover rate limiting policy, error handling, and violation consequences. All major aspects of the question are directly addressed.

**Sources Used**:
- **Doc_1** (/docs/api/rate-limiting.md): Provided rate limit thresholds and reset timing
- **Doc_2** (/docs/api/error-codes.md): Explained 429 error response format and retry headers
- **Doc_3** (/policies/api-usage-policy.md): Detailed violation handling and suspension policy
- **Doc_4** (/docs/api/authentication.md): Not used - covered key generation but not relevant to rate limiting

**Information Gaps**: None identified for this question

**Recommended Follow-up**:
- If customer needs >1,000 requests/hour, offer: "Would you like information about upgrading to Enterprise Premium tier?"
- If they're building automation, suggest: "Would you like code examples for implementing proper retry logic with exponential backoff?"
- Clarify their specific use case: "What is the total volume of data you need to export, and over what timeframe?"
```

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
```

### For Documentation

```text
Chunk by:
- Section (heading-based)
- 300-500 tokens with 50-token overlap
- Preserve context (don't split mid-sentence)

Metadata to include:
- Document title
- Section heading hierarchy
- Version/date
- URL (if applicable)
```

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
```

## Retrieval Strategies

### Semantic Search

```python
# Using embedding-based retrieval
query_embedding = embed(user_question)
chunks = vector_db.similarity_search(
    query_embedding,
    k=5,  # Top 5 chunks
    threshold=0.7  # Minimum similarity
)
```

### Hybrid Search

```python
# Combine semantic + keyword search
semantic_results = vector_db.similarity_search(query, k=10)
keyword_results = bm25_search(query, k=10)

# Merge and rerank
chunks = rerank(semantic_results + keyword_results, top_k=5)
```

### Contextual Retrieval

```python
# Retrieve chunk + surrounding context
main_chunk = retrieve(query)
previous_chunk = get_previous(main_chunk.id)
next_chunk = get_next(main_chunk.id)

context = f"{previous_chunk}\n{main_chunk}\n{next_chunk}"
```

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
```

### LangChain RAG Implementation

```python
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Setup
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings()
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Query
result = qa_chain({"query": "What is our rate limiting policy?"})
answer = result["result"]
sources = result["source_documents"]
```

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
```

## Related Prompts

- [ReAct: Document Search and Synthesis](react-doc-search-synthesis.md) - ReAct pattern for RAG
- [RAG: Code Ingestion](rag-code-ingestion.md) - Code-specific RAG patterns
- [Citation: Quality Framework](rag-citation-framework.md) - Citation best practices

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
```

### Contradictory Information

```text
"I found contradictory information in the documentation:

- Document A [Doc_1] states: [quote A]
- Document B [Doc_3] states: [quote B]

These documents may refer to different contexts:
- [Possible explanation]

Which scenario applies to your situation? Or would you like me to escalate this documentation discrepancy?"
```

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
```

## Changelog

### Version 1.0 (2025-11-17)

- Initial release
- Comprehensive RAG template with citation framework
- Chunking and retrieval best practices
- JSON schema for automation
- Platform integration examples
- Governance metadata and error handling patterns
