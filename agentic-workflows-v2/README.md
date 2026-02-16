# 🌌 Agentic Workflows v2

> **Enterprise-grade, tier-based multi-model AI orchestration.**

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=for-the-badge)]()
[![Status](https://img.shields.io/badge/status-LangChain%20Migration-orange?style=for-the-badge)]()
[![License](https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge)]()

---

**Agentic Workflows v2** is a modular framework for building and executing complex AI agent topologies. It uses a **Tier-based Routing** system to intelligently select models based on task complexity, cost, and latency, transitioning from deterministic logic to large-scale LLMs seamlessly.

The project is currently undergoing a **LangGraph migration** to provide industry-standard persistence, cycle handling, and "time-travel" debugging.

## ✨ Core Pillars

### 🧩 Tier-Based Orchestration

Agents are assigned capability tiers (0-5). Our **SmartRouter** automatically selects the best available model for each tier—using fast, free models for routing and small tasks, while reserving flagship models for reasoning and code generation.

### 🕸️ Graph-Based Execution

Workflows are defined as Directed Acyclic Graphs (DAGs) in YAML, which are then compiled into executable **LangGraph** runtimes. This enables complex feedback loops, parallel step execution, and robust error recovery.

### 🧪 Unified Evaluation Framework

Built-in support for **SWE-bench**, **HumanEval**, and custom datasets. Every run is logged with structured telemetry, allowing for automated scoring and regression testing via an LLM-as-a-Judge protocol.

### 📺 Real-Time Live Monitoring

A full React-based dashboard provides live views of multi-agent conversations, token usage tracking, and dynamic graph visualization.

---

## 🚀 Quick Start

### Installation

```bash
# Clone and install with server and langchain extras
git clone https://github.com/tafreeman/agentic-workflows-v2.git
cd agentic-workflows-v2
pip install -e ".[server,langchain,dev]"
```

### Run a Coder Agent

```python
import asyncio
from agentic_v2 import CodeGenerationInput, CoderAgent

async def main():
    agent = CoderAgent()
    result = await agent.run(
        CodeGenerationInput(
            description="Build a FastAPI endpoint for user registration",
            language="python"
        )
    )
    print(result.code)

asyncio.run(main())
```

---

## 🖥️ Dashboard & API

Launch the backend server to access the UI and API endpoints:

```bash
# Default port 8010 to avoid common conflicts
python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010
```

- **Live Dashboard**: [http://127.0.0.1:8010](http://127.0.0.1:8010)
- **API Documentation**: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)

---

## 🛠️ Project Structure

For a complete map of all files, see [MASTER_MANIFEST.md](./MASTER_MANIFEST.md).

```text
agentic_v2/
├── agents/             # Reusable AI Agent implementations (Coder, Reviewer, etc.)
├── engine/             # Core execution logic (DAG, Pipeline, State Management)
├── langchain/          # (Ongoing) LangGraph-native engine implementation
├── models/             # SmartRouter, LLM clients, and Backend adapters
├── server/             # FastAPI backend and WebSocket handlers
├── tools/              # Tier-based tool registry (File, Shell, Search, etc.)
└── workflows/          # YAML-to-Graph loading and execution
```

---

## 🧪 Testing

```bash
# Run backend tests
pytest tests/ -v

# Run UI tests
cd ui && npm test
```

## 📄 License & Contributing

This project is licensed under the **MIT License**. We welcome contributions focusing on agent quality, tool diversity, and evaluation metrics. See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.
