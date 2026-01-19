---
title: "Context Optimization Techniques"
shortTitle: "Context Optimization"
intro: "Advanced techniques for managing long contexts, maximizing token efficiency, and optimizing information retrieval."
type: "reference"
difficulty: "advanced"
audience:

  - "senior-engineer"
  - "ai-researcher"

platforms:

  - "claude"
  - "gpt-4"
  - "langchain"

author: "AI Research Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "public"
reviewStatus: "approved"
---

# Context Optimization Techniques

Advanced techniques for managing extended context windows, optimizing token usage, and maximizing information density. Essential for working with long documents, large codebases, and complex multi-turn conversations.

## 📋 Contents

```text
context-optimization/
├── README.md                        # This file
├── context_optimizer.py             # Python utilities for context optimization
├── compression/                     # Context compression techniques
│   ├── hierarchical-compression.md  # Multi-level compression
│   └── semantic-compression.md      # Meaning-preserving compression
├── many-shot-learning/              # Extended few-shot learning
│   └── many-shot-learning.md        # Leverage long contexts with examples
└── retrieval-augmented/             # RAG patterns
    └── (RAG implementation patterns)
```

## 🎯 Why Context Optimization Matters

Modern LLMs have extended context windows:

- **GPT-4 Turbo**: 128K tokens (~400 pages)
- **Claude 3**: 200K tokens (~500 pages)
- **Gemini 1.5**: 1M+ tokens (~2,800 pages)

But challenges remain:

- 💰 **Cost**: Longer contexts = higher costs
- ⏱️ **Latency**: More tokens = slower responses
- 🎯 **Attention**: Models may miss information in long contexts ("lost in the middle")
- 🧠 **Relevance**: Not all context is equally important

## ✨ Key Techniques

### 1. Compression

**Reduce token count while preserving meaning.**

Types:

- **Extractive**: Select most important sentences
- **Abstractive**: Rewrite in condensed form
- **Hierarchical**: Multi-level summaries
- **Semantic**: Preserve key concepts

**When to Use:**

- Document exceeds context limit
- Cost optimization needed
- Reduce latency
- Multiple documents to process

### 2. Many-Shot Learning

**Leverage long contexts with many examples.**

Traditional few-shot (3-5 examples) vs Many-shot (dozens or hundreds):

```text
Few-Shot (GPT-3.5):
Example 1
Example 2
Example 3
Now: [Task]

Many-Shot (Claude/GPT-4):
Example 1
Example 2
...
Example 50
Now: [Task]
```

**Benefits:**

- Better edge case handling
- Consistent formatting
- Domain-specific knowledge
- Complex pattern learning

### 3. Retrieval-Augmented Generation (RAG)

**Fetch relevant context dynamically.**

```text
Query → Retrieval → Relevant Docs → LLM → Response
```

**Advantages:**

- No context limit on knowledge base
- Up-to-date information
- Cost-efficient
- Source attribution

### 4. Semantic Compression

**Preserve meaning, reduce tokens.**

```text
Original (150 tokens):
"The quarterly financial report indicates that our revenue 
for Q4 2024 was $5.2M, representing a 23% increase compared 
to Q3. This growth was primarily driven by expansion in the 
enterprise segment, which saw 45 new customers..."

Compressed (50 tokens):
"Q4 2024: $5.2M revenue (+23% QoQ)

- Enterprise: 45 new customers (primary driver)
- Key metrics: [condensed]"

```

## 🚀 Quick Start

### Basic Compression

```python
from context_optimizer import ContextOptimizer

optimizer = ContextOptimizer()

# Compress long text
long_document = open('document.txt').read()  # 10,000 tokens
compressed = optimizer.compress(
    text=long_document,
    target_ratio=0.3,  # Compress to 30% of original
    method='semantic'
)

# Result: ~3,000 tokens preserving key information
```

### Many-Shot Learning

```python
# Build many-shot prompt
examples = load_examples()  # 50+ examples

prompt = f"""
Convert natural language to SQL queries.

Examples:
{format_examples(examples)}  # All 50 examples

Now convert: "Show users who joined last week"
"""

response = llm.invoke(prompt)
```

### RAG Implementation

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Create vector store
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings()
)

# Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    return_source_documents=True
)

# Query
result = qa_chain.invoke({"query": "What is the refund policy?"})
```

## 📚 Technique Details

### Hierarchical Compression

**File:** [compression/hierarchical-compression.md](./compression/hierarchical-compression.md)

Multi-level document summarization:

```text
Original Document (10,000 tokens)
    ↓
Level 1: Section summaries (2,000 tokens)
    ↓
Level 2: Chapter summaries (500 tokens)
    ↓
Level 3: Document summary (100 tokens)
```

**Use Cases:**

- Large documents
- Progressive detail retrieval
- Multi-granularity search

**Implementation:**

```python
def hierarchical_compress(document, levels=3):
    current = document
    summaries = []

    for level in range(levels):
        # Compress to 1/5 of current size
        summary = summarize(current, target_ratio=0.2)
        summaries.append(summary)
        current = summary

    return summaries  # [detailed, medium, brief]
```

### Semantic Compression

**File:** [compression/semantic-compression.md](./compression/semantic-compression.md)

Preserve meaning while reducing tokens:

**Techniques:**

1. **Entity extraction**: Keep key entities, remove fluff
2. **Relation preservation**: Maintain relationships
3. **Fact consolidation**: Merge redundant information
4. **Structure retention**: Keep logical flow

**Example:**

```python
semantic_compressor = SemanticCompressor(
    preserve_entities=True,
    preserve_relations=True,
    remove_redundancy=True
)

compressed = semantic_compressor.compress(
    text=document,
    target_tokens=500
)
```

### Many-Shot Learning

**File:** [many-shot-learning/many-shot-learning.md](./many-shot-learning/many-shot-learning.md)

Leverage extended context with numerous examples:

**Benefits:**

- **Accuracy**: +15-35% over few-shot
- **Edge cases**: Better handling
- **Consistency**: More stable outputs
- **Domain adaptation**: Learn domain-specific patterns

**Optimal Example Count:**

| Model | Context | Optimal Examples | Max Practical |
| ------- | --------- | ------------------ | --------------- |
| GPT-3.5 | 16K | 5-10 | 20 |
| GPT-4 | 8K | 5-15 | 30 |
| GPT-4 Turbo | 128K | 20-100 | 500+ |
| Claude 3 | 200K | 30-150 | 1000+ |

**Implementation:**

```python
# Generate many-shot prompt
def create_many_shot_prompt(task, examples, num_examples=50):
    selected_examples = examples[:num_examples]

    prompt = f"""Task: {task}

Examples:
"""
    for i, ex in enumerate(selected_examples, 1):
        prompt += f"\nExample {i}:\n"
        prompt += f"Input: {ex['input']}\n"
        prompt += f"Output: {ex['output']}\n"

    prompt += f"\nNow solve:\nInput: {{input}}\nOutput:"

    return prompt
```

### Retrieval-Augmented Generation

**File:** `retrieval-augmented/`

Combine retrieval with generation:

**Architecture:**

```text
┌──────────────┐
│   Question   │
└──────┬───────┘
       │
   ┌───▼────────────┐
   │   Embedding    │
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │ Vector Search  │ → Database of Documents
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │ Top K Docs     │
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │   LLM + Docs   │
   └───┬────────────┘
       │
   ┌───▼────────────┐
   │   Response     │
   └────────────────┘
```

**Key Components:**

1. **Embedding Model**: Convert text to vectors
2. **Vector Store**: Efficient similarity search
3. **Retriever**: Fetch relevant documents
4. **Generator**: LLM that uses retrieved docs

**Implementation:**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# 1. Split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# 2. Create embeddings and store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# 3. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# 4. Build QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    retriever=retriever,
    return_source_documents=True
)

# 5. Query
result = qa_chain.invoke({
    "query": "What are the key findings?"
})
```

## 🎓 Best Practices

### 1. Choose the Right Technique

| Scenario | Recommended Technique | Why |
| ---------- | ---------------------- | ----- |
| **Fixed document, many queries** | RAG | Efficient reuse of embeddings |
| **Need full context** | Compression | Preserve all information |
| **Pattern learning** | Many-shot | Learn from examples |
| **Real-time updates** | RAG | Dynamic knowledge base |
| **Token budget tight** | Semantic compression | Best token efficiency |

### 2. Optimize Chunk Size

```python
# Too small: loses context
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,  # ❌ Too small
    chunk_overlap=20
)

# Too large: less precise retrieval
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,  # ❌ Too large
    chunk_overlap=500
)

# Just right: balance context and precision
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # ✅ Good default
    chunk_overlap=200
)
```

### 3. Implement Hybrid Approaches

```python
# Combine RAG + Compression
def hybrid_retrieval(query, docs, max_tokens=4000):
    # 1. Retrieve relevant docs
    relevant_docs = retrieve_top_k(query, docs, k=10)

    # 2. Calculate total tokens
    total_tokens = sum(count_tokens(doc) for doc in relevant_docs)

    # 3. Compress if needed
    if total_tokens > max_tokens:
        relevant_docs = [
            compress(doc, target_ratio=max_tokens/total_tokens)
            for doc in relevant_docs
        ]

    return relevant_docs
```

### 4. Monitor Performance

```python
import time

def measure_rag_performance(query, qa_chain):
    start = time.time()

    result = qa_chain.invoke({"query": query})

    metrics = {
        "latency": time.time() - start,
        "tokens": count_tokens(result["result"]),
        "sources": len(result["source_documents"]),
        "relevance": calculate_relevance(query, result)
    }

    return result, metrics
```

## 🔧 Utilities Reference

### ContextOptimizer Class

```python
from context_optimizer import ContextOptimizer

optimizer = ContextOptimizer()

# Compress text
compressed = optimizer.compress(
    text=long_text,
    target_ratio=0.3,
    method='semantic'  # or 'extractive', 'hierarchical'
)

# Calculate token count
tokens = optimizer.count_tokens(text)

# Split optimally
chunks = optimizer.smart_split(
    text=document,
    chunk_size=1000,
    overlap=200,
    preserve_sentences=True
)

# Measure information density
density = optimizer.calculate_density(text)
```

## 📊 Performance Comparison

| Technique | Token Reduction | Information Retention | Latency Impact | Cost Impact |
| ----------- | ---------------- | ---------------------- | ---------------- | ------------- |
| **Extractive** | 50-70% | 70-80% | Low | -50% |
| **Semantic** | 60-80% | 80-90% | Medium | -60% |
| **Hierarchical** | 70-90% | 75-85% | High | -70% |
| **RAG** | N/A (dynamic) | 85-95% | Medium | Variable |
| **Many-shot** | -100% (adds tokens) | 95%+ | High | +100% |

## 🛠️ Advanced Patterns

### Context Windows Management

```python
class ContextWindow:
    """Manage rolling context window."""

    def __init__(self, max_tokens=4000):
        self.max_tokens = max_tokens
        self.messages = []

    def add_message(self, role, content):
        """Add message, removing old ones if needed."""
        self.messages.append({"role": role, "content": content})

        # Trim if over limit
        while self.total_tokens() > self.max_tokens:
            # Keep system message, remove oldest user/assistant
            if len(self.messages) > 1:
                self.messages.pop(1)
            else:
                break

    def total_tokens(self):
        return sum(count_tokens(m["content"]) for m in self.messages)
```

### Smart Chunking

```python
def semantic_chunking(text, max_chunk_size=1000):
    """Split by semantic boundaries."""
    sentences = split_sentences(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)

        if current_size + sentence_tokens > max_chunk_size:
            # Start new chunk
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_size += sentence_tokens

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks
```

### Relevance Ranking

```python
from sklearn.metrics.pairwise import cosine_similarity

def rank_by_relevance(query, documents, top_k=5):
    """Rank documents by relevance to query."""

    # Embed query and documents
    query_embedding = embed(query)
    doc_embeddings = [embed(doc) for doc in documents]

    # Calculate similarity
    similarities = [
        cosine_similarity([query_embedding], [doc_emb])[0][0]
        for doc_emb in doc_embeddings
    ]

    # Sort and return top K
    ranked = sorted(
        zip(documents, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:top_k]]
```

## 📖 Additional Resources

### Research Papers

- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Context position effects
- [Long-Context Language Models](https://arxiv.org/abs/2307.03170)
- [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

### Tools & Libraries

- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [LlamaIndex](https://www.llamaindex.ai/) - Data framework for LLMs
- [Chroma](https://www.trychroma.com/) - Vector database

### Benchmarks

- [RULER Benchmark](https://arxiv.org/abs/2404.06654) - Long-context evaluation
- [LongBench](https://github.com/THUDM/LongBench) - Long-context understanding

## 🤝 Contributing

When adding context optimization techniques:

1. **Benchmark performance**: Token reduction, information retention
2. **Test on various content**: Code, prose, structured data
3. **Document tradeoffs**: Speed vs quality vs cost
4. **Provide comparisons**: Show before/after examples
5. **Include utilities**: Helper functions for implementation

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## 📝 Version History

- **1.0** (2025-11-30): Initial release with compression, RAG, and many-shot patterns

---

**Need Help?** Check the [LangChain documentation](https://python.langchain.com/) or [open an issue](https://github.com/tafreeman/prompts/issues).
