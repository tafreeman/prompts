---
title: "LangChain Framework Prompts"
shortTitle: "LangChain"
intro: "LangChain integration patterns, LCEL examples, and agent workflows for building LLM applications."
type: "reference"
difficulty: "intermediate"
audience:

  - "senior-engineer"
  - "junior-engineer"

platforms:

  - "langchain"
  - "openai"
  - "anthropic"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:

  - "PII-safe"

dataClassification: "public"
reviewStatus: "approved"
---

# LangChain Framework Prompts

Comprehensive collection of LangChain patterns, LCEL (LangChain Expression Language) examples, and agent workflows for building production-ready LLM applications.

## 📋 Contents

```text
langchain/
├── README.md                # This file
├── agent-patterns/          # Agent architectures and workflows
│   └── langchain-agents.md  # Agent patterns and examples
└── lcel-patterns/           # LangChain Expression Language
    └── langchain-reflexion-example.md  # LCEL reflexion pattern
```

## 🎯 What is LangChain
LangChain is a framework for developing applications powered by language models. It provides:

- **Chains**: Compose LLM calls and data processing
- **Agents**: Dynamic decision-making and tool use
- **Memory**: Conversation and context management
- **LCEL**: Declarative way to compose chains
- **Integrations**: 100+ LLM providers and tools

## ✨ Key Features

### 1. LangChain Expression Language (LCEL)

Declarative syntax for building chains:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Build a chain with LCEL
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

chain = prompt | model | parser

# Invoke the chain
result = chain.invoke({"topic": "programming"})
```

### 2. Agents

Autonomous decision-making with tool use:

```python
from langchain.agents import create_openai_functions_agent
from langchain.tools import Tool

tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Useful for math calculations"
    )
]

agent = create_openai_functions_agent(llm, tools, prompt)
```

### 3. Memory

Maintain conversation context:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
memory.save_context({"input": "Hi!"}, {"output": "Hello!"})
```

### 4. Retrieval-Augmented Generation (RAG)

Combine LLMs with external knowledge:

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

vectorstore = Chroma.from_documents(documents, OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
```

## 🚀 Quick Start

### Installation

```bash
# Core LangChain
pip install langchain

# OpenAI integration
pip install langchain-openai

# Anthropic integration
pip install langchain-anthropic

# Community integrations
pip install langchain-community

# Full installation
pip install langchain langchain-openai langchain-anthropic langchain-community
```

### Basic Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

# Create model
model = ChatOpenAI(model="gpt-4")

# Build chain with LCEL
chain = prompt | model

# Use the chain
response = chain.invoke({"input": "What is LangChain?"})
print(response.content)
```

### Basic Agent

```python
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Define a tool
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

# Create agent
llm = ChatOpenAI(model="gpt-4")
tools = [multiply]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Run agent
result = agent_executor.invoke({"input": "What is 25 * 4?"})
```

## 📚 Available Patterns

### Agent Patterns

**Location:** `agent-patterns/langchain-agents.md`

Comprehensive guide covering:

- **ReAct Agents**: Reasoning + Acting pattern
- **OpenAI Functions Agents**: Function calling with GPT models
- **Structured Chat Agents**: Multi-input structured conversations
- **Conversational Agents**: Memory-enabled chat agents
- **Custom Agents**: Build your own agent architectures

**Example Use Cases:**

- Question answering with tools
- Code execution agents
- Research assistants
- Customer service bots

### LCEL Patterns

**Location:** `lcel-patterns/langchain-reflexion-example.md`

Advanced LCEL patterns including:

- **Reflexion Pattern**: Self-critique and improvement
- **Chain Composition**: Complex multi-step workflows
- **Parallel Execution**: Run chains concurrently
- **Conditional Logic**: Branch based on outputs
- **Fallback Chains**: Error handling and retries

**Example:**

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Parallel execution
chain = RunnableParallel({
    "context": retriever,
    "question": RunnablePassthrough()
}) | prompt | model
```

## 🎓 Common Patterns

### 1. Prompt Templates

```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an expert in {domain}."
    ),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
```

### 2. Output Parsers

```python
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

# JSON parsing
json_parser = JsonOutputParser()

# Structured output with Pydantic
class Response(BaseModel):
    answer: str = Field(description="The answer")
    confidence: float = Field(description="Confidence score")

parser = PydanticOutputParser(pydantic_object=Response)
```

### 3. Retrieval Chains

```python
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Combine retrieval with generation
combine_docs_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

result = retrieval_chain.invoke({"input": "What is the capital of France?"})
```

### 4. Conversational Chains

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)
```

## 🔧 Advanced Features

### Streaming

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

for chunk in chain.stream({"input": "Tell me a story"}):
    print(chunk, end="", flush=True)
```

### Batch Processing

```python
# Process multiple inputs efficiently
results = chain.batch([
    {"input": "What is AI?"},
    {"input": "What is ML?"},
    {"input": "What is DL?"}
])
```

### Async Support

```python
import asyncio

async def process():
    result = await chain.ainvoke({"input": "Hello"})
    return result

asyncio.run(process())
```

### Callbacks

```python
from langchain.callbacks import StdOutCallbackHandler

chain = prompt | model | parser

result = chain.invoke(
    {"input": "Hello"},
    config={"callbacks": [StdOutCallbackHandler()]}
)
```

## 📊 Integration Matrix

| Integration | Package | Use Case |
| ------------ | --------- | ---------- |
| **OpenAI** | `langchain-openai` | GPT-4, embeddings, function calling |
| **Anthropic** | `langchain-anthropic` | Claude models, constitutional AI |
| **Google** | `langchain-google-genai` | Gemini models |
| **Hugging Face** | `langchain-community` | Open-source models |
| **Local Models** | `langchain-community` | Ollama, LlamaCpp |
| **Vector Stores** | `langchain-community` | Chroma, Pinecone, Weaviate |
| **Document Loaders** | `langchain-community` | PDF, CSV, web scraping |

## 🎯 Use Case Examples

### Code Review Agent

```python
from langchain.agents import create_openai_functions_agent
from langchain.tools import tool

@tool
def analyze_code(code: str) -> str:
    """Analyze code for issues and suggest improvements."""
    # Your analysis logic here
    return "Analysis results..."

@tool
def check_security(code: str) -> str:
    """Check code for security vulnerabilities."""
    return "Security analysis..."

tools = [analyze_code, check_security]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({
    "input": "Review this Python function: def process_user_input(data): ..."
})
```

### Research Assistant

```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load and process documents
loader = WebBaseLoader(["https://example.com/article1", "..."])
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create retrieval chain
vectorstore = Chroma.from_documents(splits, OpenAIEmbeddings())
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

result = qa_chain.invoke({"query": "What are the main findings?"})
```

### Multi-Agent Collaboration

```python
from langchain.agents import AgentExecutor

# Create specialized agents
researcher_agent = create_openai_functions_agent(llm, researcher_tools, researcher_prompt)
writer_agent = create_openai_functions_agent(llm, writer_tools, writer_prompt)

# Orchestrate collaboration
research_result = researcher_agent.invoke({"input": "Research quantum computing"})
article = writer_agent.invoke({
    "input": f"Write an article based on: {research_result}"
})
```

## 🛠️ Best Practices

### 1. Use LCEL for Composability

✅ **Do:**

```python
chain = prompt | model | parser
```

❌ **Don't:**

```python
# Avoid manual chaining
output = model(prompt.format(input))
result = parser.parse(output)
```

### 2. Leverage Type Safety

```python
from typing import TypedDict

class ChainInput(TypedDict):
    input: str
    context: list[str]

chain = prompt | model
# Type hints help with IDE support and validation
```

### 3. Handle Errors Gracefully

```python
from langchain_core.runnables import RunnableWithFallbacks

chain_with_fallback = chain.with_fallbacks([backup_chain])
```

### 4. Monitor Performance

```python
from langchain.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke({"input": "Hello"})
    print(f"Tokens used: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")
```

## 📖 Additional Resources

### Official Documentation

- [LangChain Docs](https://python.langchain.com/)
- [LCEL Guide](https://python.langchain.com/docs/expression_language/)
- [API Reference](https://api.python.langchain.com/)

### Tutorials

- [LangChain Academy](https://academy.langchain.com/)
- [Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)

### Community

- [GitHub](https://github.com/langchain-ai/langchain)
- [Discord](https://discord.gg/langchain)
- [Twitter](https://twitter.com/langchainai)

## 🤝 Contributing

When adding LangChain patterns:

1. Test with latest LangChain version (>=0.1.0)
2. Use LCEL where possible
3. Include type hints
4. Provide runnable examples
5. Document dependencies and versions
6. Add error handling

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## 🐛 Common Issues

### Issue: Import errors

**Solution:** Install correct packages:

```bash
pip install langchain-openai  # Not langchain.openai
pip install langchain-anthropic
```

### Issue: Deprecated patterns

**Solution:** Use LCEL instead of legacy chains:

```python
# Old way (deprecated)
from langchain.chains import LLMChain

# New way (LCEL)
chain = prompt | model | parser
```

### Issue: Memory not persisting

**Solution:** Use proper memory implementation:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
# Pass memory to chain configuration
```

## 📝 Version History

- **1.0** (2025-11-30): Initial release with LCEL patterns and agent examples

---

**Need Help?** Check the [official docs](https://python.langchain.com/) or [open an issue](https://github.com/tafreeman/prompts/issues).
