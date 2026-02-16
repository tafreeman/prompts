# Contributing to Agentic Workflows v2

Thank you for your interest in contributing! We are building the next generation of multi-agent orchestration.

## 🛠️ Development Setup

1. **Python Environment**: We recommend Python 3.11+.

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -e ".[dev,server,langchain]"
   ```

2. **Pre-commit Hooks**: We use `ruff` and `black` for formatting.

   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Frontend Setup**:

   ```bash
   cd ui
   npm install
   ```

## 🧪 Testing Policy

- **New Features**: Must include unit tests in the `tests/` directory.
- **Bug Fixes**: Should include a regression test.
- **Agents**: Should be tested with mock backends unless integration testing is explicitly required.

## 📝 Roadmap

We are currently focused on:

- Completing the **LangGraph Migration**.
- Expanding **Tier 0 tools** for better local execution.
- Improving **Evaluation scoring** for coding benchmarks.

## 🤝 Code of Conduct

Please maintain a collaborative and professional tone in all issues and pull requests.
