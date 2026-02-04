#!/usr/bin/env python
"""Agentic-Workflows-V2 Implementation Runner.

Orchestrates the implementation of agentic-workflows-v2 using:
- Requirements Analyst: Processes architecture docs into engineering specs
- Orchestrator: Breaks work into chunks and assigns to agents
- Developer + AI Expert: Implement code in parallel/sequential chunks
- Researcher: Validates against latest docs
- Tester: Runs tests
- Judge: GO/NO-GO decision

Uses SmartModelRouter for rate limit handling and provider fallback.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add parent paths for imports
_script_path = Path(__file__).resolve()
sys.path.insert(0, str(_script_path.parents[2]))  # d:\source\prompts
sys.path.insert(
    0, str(_script_path.parents[1] / "src")
)  # d:\source\prompts\multiagent-workflows\src

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_script_path.parents[2] / ".env")  # Load from repo root

# Enable remote providers
os.environ.setdefault("PROMPTEVAL_ALLOW_REMOTE", "1")

from tools.llm.llm_client import LLMClient  # noqa: E402

from multiagent_workflows.core.smart_model_router import SmartModelRouter  # noqa: E402
from multiagent_workflows.mcp import setup_default_mcp_servers  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("implementation_runner")


# =============================================================================
# DATA STRUCTURES
# =============================================================================


@dataclass
class Task:
    """A discrete implementation task."""

    id: str
    title: str
    description: str
    phase: int
    tier: int  # Model tier required
    assigned_to: str  # "developer", "ai_expert", "researcher", etc.
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed
    output: Optional[str] = None
    files_created: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class IterationState:
    """State for one iteration of the implementation loop."""

    iteration: int
    tasks: List[Task]
    completed_tasks: List[str] = field(default_factory=list)
    failed_tasks: List[str] = field(default_factory=list)
    score: float = 0.0
    judge_decision: str = "pending"
    feedback: str = ""


# =============================================================================
# AGENT PROMPTS
# =============================================================================

REQUIREMENTS_ANALYST_PROMPT = """You are a Senior Engineering Requirements Analyst.

CONTEXT: We are building a NEW standalone Python package called "agentic-workflows-v2" at d:\\source\\prompts\\agentic-workflows-v2\\.

GOAL: Tiered multi-model AI workflows - route tasks to appropriate model sizes (small for simple, large for complex).

INPUT DOCUMENTS:
{documents}

YOUR TASK: Analyze these documents and extract ACTIONABLE engineering requirements.

OUTPUT FORMAT (valid JSON only):
{{
  "summary": "2-3 sentence executive summary of what we're building",
  "key_requirements": [
    "Standalone package with pyproject.toml using Hatchling",
    "SmartModelRouter with tier 0-3 routing and adaptive fallback",
    "Pydantic v2 contracts for all inputs/outputs",
    "Async agent interface with uniform run() signature",
    "Built-in tier-0 tools (file ops, JSON transforms) - no LLM",
    "Evaluation framework with YAML rubrics and JSON/MD reports"
  ],
  "constraints": [
    "Python >=3.11 required",
    "No heavy frameworks (LangChain, Haystack)",
    "Zero modifications to existing multiagent-workflows/",
    "All tests use temporary directories",
    "≥80% line coverage"
  ],
  "milestones": [
    {{
      "name": "Phase 0: Package Foundation",
      "deliverables": [
        "pyproject.toml with dependencies",
        "src/agentic_v2/ package structure",
        "README.md with quick-start"
      ]
    }},
    {{
      "name": "Phase 1: Core Contracts",
      "deliverables": [
        "Pydantic models for messages and results",
        "Base tool and agent interfaces",
        "Tool registry system"
      ]
    }},
    {{
      "name": "Phase 2: Model Router",
      "deliverables": [
        "SmartModelRouter with tier-based selection",
        "ModelStats tracking and persistence",
        "Adaptive fallback logic"
      ]
    }}
  ],
  "first_iteration_tasks": [
    "Create pyproject.toml and package structure",
    "Define Pydantic contracts (AgentMessage, StepResult, TaskInput/Output)",
    "Implement tier-0 tools (FileCopyTool, JsonTransformTool)",
    "Create base agent interface (BaseAgent, AgentConfig)"
  ]
}}

FOCUS ON:
1. Concrete deliverables (files, modules, classes)
2. Clear acceptance criteria per milestone
3. Dependencies between components
4. What to build FIRST (foundation → contracts → routing → agents)"""

ORCHESTRATOR_PROMPT = """You are the Implementation Orchestrator for the agentic-workflows-v2 package.

GOAL: Create a NEW standalone Python package at d:\\source\\prompts\\agentic-workflows-v2\\ with tier-based AI workflow routing.

CRITICAL: This is iteration {iteration}. You MUST create concrete implementation tasks.

REQUIREMENTS SUMMARY:
{requirements}

CURRENT PROGRESS:
- Iteration: {iteration}/{max_iterations}
- Tasks Completed: {completed}
- Tasks Failed: {failed}

YOUR JOB:
1. Break down the implementation into 3-5 concrete tasks for THIS iteration
2. Focus on foundational work first (pyproject.toml, package structure, core contracts)
3. Each task produces actual FILES (no analysis-only tasks unless iteration 1)
4. Assign appropriate tier (0=no-LLM, 1=small, 2=medium, 3=large)

TASK ASSIGNMENT RULES:
- "PackageArchitect" → tier 0-1 → Creates pyproject.toml, package structure, __init__.py files
- "APIDesigner" → tier 0-1 → Creates Pydantic contracts (messages.py, schemas.py)
- "ToolBuilder" → tier 1-2 → Implements tools (file_ops.py, transform.py)
- "AgentBuilder" → tier 2 → Implements agent base classes and registry
- "RouterDeveloper" → tier 2-3 → Implements SmartModelRouter with tier logic
- "TestWriter" → tier 2 → Creates pytest tests

REQUIRED OUTPUT FORMAT (valid JSON only, no markdown):
{{
  "tasks": [
    {{
      "id": "TASK-001",
      "title": "Create Package Foundation",
      "description": "Generate pyproject.toml with dependencies: pydantic>=2.0, httpx, jinja2, jmespath. Create src/agentic_v2/__init__.py with version export. Create README.md with quick-start.",
      "phase": 0,
      "tier": 0,
      "assigned_to": "PackageArchitect",
      "dependencies": [],
      "output_files": ["pyproject.toml", "src/agentic_v2/__init__.py", "README.md"]
    }}
  ],
  "parallel_groups": [["TASK-001"]],
  "notes": "Starting with foundation - pyproject and package structure"
}}

EXAMPLE TASKS FOR ITERATION 1:
1. TASK-001: Create pyproject.toml + package structure (tier 0, PackageArchitect)
2. TASK-002: Define Pydantic contracts (messages, schemas) (tier 1, APIDesigner)  
3. TASK-003: Implement tier-0 tools (file ops, transforms) (tier 1, ToolBuilder)
4. TASK-004: Create base agent interface (tier 1, APIDesigner)

NOW CREATE THE TASK LIST FOR ITERATION {iteration}:"""

# =============================================================================
# LANGUAGE STANDARDS (Dynamic Injection)
# =============================================================================
# Based on industry best practices from OpenAI, GitHub, and Anthropic:
# - Inject ONLY relevant language rules for the current task
# - Avoid language bias (don't show Python examples for C# tasks)
# - Keep prompts focused and scoped

LANGUAGE_STANDARDS = {
    "python": {
        "version": "3.11+",
        "rules": [
            "Pydantic v2 (BaseModel, Field, model_validator)",
            "Async everywhere: async def run(...)",
            "Type hints on ALL functions and methods",
            "Google-style docstrings",
            "pathlib.Path for all paths (POSIX compatible)",
        ],
        "imports_example": """from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field""",
    },
    "csharp": {
        "version": "11+",
        "rules": [
            "Nullable reference types enabled",
            "Async/await for I/O operations",
            "XML documentation comments",
            "Records for immutable data",
            "Top-level statements where appropriate",
        ],
        "imports_example": """using System;
using System.Threading.Tasks;
using System.Collections.Generic;""",
    },
    "java": {
        "version": "17+",
        "rules": [
            "Records for data classes",
            "var for local type inference",
            "Javadoc comments",
            "CompletableFuture for async operations",
            "Stream API for collections",
        ],
        "imports_example": """package com.example;

import java.util.*;
import java.util.concurrent.*;""",
    },
    "typescript": {
        "version": "5+",
        "rules": [
            "Strict mode enabled",
            "ESM imports (import/export)",
            "JSDoc comments for public APIs",
            "async/await for promises",
            "Type inference where clear",
        ],
        "imports_example": """import type { Config } from './types';
import { logger } from './utils';""",
    },
    "javascript": {
        "version": "ES2023+",
        "rules": [
            "ESM imports (import/export)",
            "JSDoc comments for public APIs",
            "async/await for promises",
            "Destructuring and spread operators",
            "Optional chaining (?.) and nullish coalescing (??)",
        ],
        "imports_example": """import { config } from './config.js';
import { logger } from './logger.js';""",
    },
    "yaml": {
        "version": "1.2",
        "rules": [
            "Use 2-space indentation",
            "Include comments for complex sections",
            "Quote strings with special characters",
            "Use explicit keys for clarity",
        ],
        "imports_example": "",
    },
    "json": {
        "version": "JSON5 where supported",
        "rules": [
            "Valid JSON syntax (no trailing commas in strict JSON)",
            "Use 2-space indentation",
            "Meaningful key names",
        ],
        "imports_example": "",
    },
}

DEVELOPER_PROMPT = """You are a Senior Developer implementing agentic-workflows-v2.

TARGET: d:\\source\\prompts\\agentic-workflows-v2\\ (NEW standalone package)

{language_specific_rules}

TASK: {task_title}

DESCRIPTION:
{task_description}

CONTEXT:
{context}

OUTPUT FORMAT (applies to ALL file types):
You MUST use this EXACT format for each file:

# File: path/to/file.ext
```language
... complete code ...
```

Supported: .py, .cs, .java, .yaml, .yml, .json, .toml, .md, .html, .css, .js, .ts, .tsx, .jsx

REQUIREMENTS:
1. Complete, runnable code (no placeholders like "... existing code ...")
2. All necessary imports at the top
3. Type annotations/hints where applicable
4. Documentation comments (docstrings, JSDoc, XML docs, etc.)
5. Proper error handling
6. Meaningful names for variables, functions, and classes

If creating multiple files, repeat the format for each file.

NOW GENERATE THE COMPLETE IMPLEMENTATION:"""

JUDGE_PROMPT = """You are the Quality Judge evaluating the agentic-workflows-v2 implementation.

ITERATION {iteration}/{max_iterations}

PROJECT GOAL: Build a standalone Python package with tier-based AI workflow routing.

PLAN SUMMARY:
{plan_summary}

TASKS COMPLETED THIS ITERATION:
{completed_tasks}

TASKS FAILED:
{failed_tasks}

TEST RESULTS:
{test_results}

CONTAINMENT CHECK (no modifications to multiagent-workflows/):
{containment_report}

YOUR DECISION CRITERIA:

**PASS** (implementation complete):
- All foundation files exist (pyproject.toml, __init__.py, core contracts)
- Core functionality implemented (model router, agents, tools)
- Tests written and passing (≥80% coverage)
- No modifications to existing multiagent-workflows/
- Documentation complete (README, API docs)

**ITERATE** (continue working):
- Good progress made this iteration
- Foundation tasks completed
- More implementation needed
- No critical blockers

**FAIL** (stop and report issues):
- No progress for 2+ iterations
- Fundamental design issues
- Dependencies on non-existent code
- Containment violated (modified existing code)

OUTPUT (valid JSON only):
{{
  "decision": "PASS or ITERATE or FAIL",
  "score": 0-100,
  "completeness_score": 0-100,
  "correctness_score": 0-100,
  "quality_score": 0-100,
  "completed_milestones": ["Phase 0: Package Foundation"],
  "pending_milestones": ["Phase 1: Core Contracts", "Phase 2: Model Router"],
  "issues": ["Specific problems found"],
  "required_fixes": ["What must be fixed next iteration"],
  "iteration_feedback": "Focus on X next iteration (be specific about files/modules)"
}}

EVALUATE NOW:"""


# =============================================================================
# IMPLEMENTATION RUNNER
# =============================================================================


class ImplementationRunner:
    """Runs the agentic-workflows-v2 implementation workflow."""

    def __init__(
        self,
        plan_path: str,
        architecture_docs: List[str],
        target_dir: str = "agentic-workflows-v2",
        max_iterations: int = 5,
        dry_run: bool = False,
        use_cloud: bool = False,
        max_doc_chars: Optional[int] = None,
        max_prompt_chars: Optional[int] = None,
        cloud_models: Optional[List[str]] = None,
        enable_mcp: bool = False,
        mcp_memory_path: Optional[str] = None,
    ):
        self.plan_path = Path(plan_path)
        self.architecture_docs = [Path(p) for p in architecture_docs]
        self.target_dir = Path(target_dir)
        self.max_iterations = max_iterations
        self.dry_run = dry_run
        self.use_cloud = use_cloud

        # MCP integration (local, in-process). This does NOT use VS Code's `.vscode/mcp.json`
        # automatically; instead it provides a reliable runtime memory store for the workflow.
        self.enable_mcp = enable_mcp
        self.mcp_memory_path = mcp_memory_path
        self._mcp_registry = None

        # Prompt/document sizing: Ollama set to 256k context, use full docs.
        self.max_doc_chars = max_doc_chars if max_doc_chars is not None else 200_000
        self.max_prompt_chars = (
            max_prompt_chars if max_prompt_chars is not None else 200_000
        )

        # Cloud models: large-context cloud-hosted Ollama models.
        self.cloud_models: List[str] = cloud_models or [
            "ollama:deepseek-v3.1:671b-cloud",
            "ollama:qwen3-coder:480b-cloud",
            "ollama:gpt-oss:120b-cloud",
        ]

        # Summarizer: same large models (256k context, no need for small).
        self.cloud_summarizer_models: List[str] = [
            "ollama:gpt-oss:120b-cloud",
        ]

        # Token budget: 256k context means ~60k tokens safe.
        self.cloud_prompt_token_budget = 60_000

        # Initialize router (no rate limiting).
        self.router = SmartModelRouter(
            prefer_local=not use_cloud, rate_limit_strategy="none"
        )

        # State
        self.requirements: Optional[Dict] = None
        self.tasks: List[Task] = []
        self.iteration_history: List[IterationState] = []

        logger.info(f"Initialized runner for {self.plan_path}")
        logger.info(f"Target directory: {self.target_dir}")
        logger.info(f"Dry run: {self.dry_run}")
        logger.info(f"Use cloud: {self.use_cloud}")
        logger.info(f"Enable MCP: {self.enable_mcp}")

    def _extract_and_write_files(self, response: str, task_id: str) -> List[str]:
        """Extract code blocks from LLM response and write them to files.

        Supports multiple formats and languages:
        - # File: path/to/file.ext followed by code
        - ```language filename="path/to/file.ext"
        - Explicit file markers in the response

        Handles: .py, .cs, .java, .yaml, .yml, .json, .md, .toml, .txt, .html, .css, .js, .ts, .tsx, .jsx, etc.

        Returns:
            List of file paths that were written.
        """
        import re

        written_files: List[str] = []

        if self.dry_run:
            logger.info(f"[DRY RUN] Would extract and write files for {task_id}")
            return written_files

        # Common file extensions we support
        file_ext_pattern = r"\.(py|cs|java|yaml|yml|json|md|toml|txt|html|css|js|ts|tsx|jsx|xml|ini|cfg|sh|bat|ps1|sql)"

        # Pattern 1: # File: path/to/file.ext followed by code block (any language)
        file_pattern = re.compile(
            r"#\s*(?:File|file|FILE):\s*([^\n]+" + file_ext_pattern + r")\s*\n"
            r"(?:```(?:\w*)?\s*)?\n?"
            r"(.*?)"
            r"(?:```|\Z|(?=\n#\s*(?:File|file|FILE):))",
            re.DOTALL,
        )

        # Pattern 2: ```language with filename attribute (any language)
        attr_pattern = re.compile(
            r'```(\w*)\s+(?:filename|file|path)=["\']?([^"\'`\n]+'
            + file_ext_pattern
            + r')["\']?\s*\n'
            r"(.*?)"
            r"```",
            re.DOTALL,
        )

        # Pattern 3: Standard code blocks with preceding path comment (any extension)
        block_pattern = re.compile(
            r"(?:^|\n)([a-zA-Z0-9_/\\.-]+" + file_ext_pattern + r")\s*[:\-]?\s*\n"
            r"```(?:\w*)?\s*\n"
            r"(.*?)"
            r"```",
            re.DOTALL,
        )

        # Pattern 4: YAML/JSON/TOML/Markup blocks with file header
        config_pattern = re.compile(
            r"(?:^|\n)(?:#|//|<!--)?\s*(?:File|file|FILE):\s*([^\n]+"
            + file_ext_pattern
            + r")\s*(?:-->)?\s*\n"
            r"```(?:yaml|yml|json|toml|xml|html|css|javascript|typescript|markdown|md)?\s*\n"
            r"(.*?)"
            r"```",
            re.DOTALL,
        )

        # Collect all matches
        matches: List[tuple[str, str]] = []
        seen_paths: set[str] = set()  # Avoid duplicates

        for match in file_pattern.finditer(response):
            path, content = match.groups()
            path = path.strip()
            if content.strip() and path not in seen_paths:
                matches.append((path, content))
                seen_paths.add(path)

        for match in attr_pattern.finditer(response):
            lang, path, ext, content = match.groups()
            path = path.strip()
            if content.strip() and path not in seen_paths:
                matches.append((path, content))
                seen_paths.add(path)

        for match in block_pattern.finditer(response):
            path, ext, content = match.groups()
            path = path.strip()
            if content.strip() and path not in seen_paths:
                if "/" in path or "\\" in path:  # Must look like a path
                    matches.append((path, content))
                    seen_paths.add(path)

        for match in config_pattern.finditer(response):
            path, ext, content = match.groups()
            path = path.strip()
            if content.strip() and path not in seen_paths:
                matches.append((path, content))
                seen_paths.add(path)

        # If no structured matches, try to extract code blocks and infer type
        if not matches:
            # Try Python blocks first
            code_blocks = re.findall(r"```python\s*\n(.*?)\n```", response, re.DOTALL)
            for i, code in enumerate(code_blocks):
                if code.strip():
                    class_match = re.search(r"class\s+(\w+)", code)
                    func_match = re.search(r"def\s+(\w+)", code)
                    if class_match:
                        name = class_match.group(1).lower()
                    elif func_match:
                        name = func_match.group(1).lower()
                    else:
                        name = f"{task_id.lower().replace('-', '_')}_{i}"
                    matches.append((f"src/agentic_v2/{name}.py", code))

            # Try YAML blocks
            yaml_blocks = re.findall(
                r"```(?:yaml|yml)\s*\n(.*?)\n```", response, re.DOTALL
            )
            for i, content in enumerate(yaml_blocks):
                if content.strip():
                    matches.append(
                        (
                            f"config/{task_id.lower().replace('-', '_')}_{i}.yaml",
                            content,
                        )
                    )

            # Try JSON blocks
            json_blocks = re.findall(r"```json\s*\n(.*?)\n```", response, re.DOTALL)
            for i, content in enumerate(json_blocks):
                if content.strip():
                    matches.append(
                        (
                            f"config/{task_id.lower().replace('-', '_')}_{i}.json",
                            content,
                        )
                    )

            # Try C# blocks
            csharp_blocks = re.findall(
                r"```(?:csharp|cs)\s*\n(.*?)\n```", response, re.DOTALL
            )
            for i, code in enumerate(csharp_blocks):
                if code.strip():
                    matches.append(
                        (f"dotnet/{task_id.lower().replace('-', '_')}_{i}.cs", code)
                    )

            # Try Java blocks
            java_blocks = re.findall(r"```java\s*\n(.*?)\n```", response, re.DOTALL)
            for i, code in enumerate(java_blocks):
                if code.strip():
                    matches.append(
                        (f"java/{task_id.lower().replace('-', '_')}_{i}.java", code)
                    )

        # Write files
        for rel_path, content in matches:
            # Normalize path
            rel_path = rel_path.replace("\\", "/").lstrip("./")

            # Determine default location based on file type
            ext = Path(rel_path).suffix.lower()
            if not any(
                rel_path.startswith(prefix)
                for prefix in ["src/", "config/", "tests/", "docs/", "ui/", "schemas/"]
            ):
                if ext == ".py":
                    rel_path = f"src/agentic_v2/{rel_path}"
                elif ext == ".cs":
                    rel_path = f"dotnet/{rel_path}"
                elif ext == ".java":
                    rel_path = f"java/{rel_path}"
                elif ext in (".yaml", ".yml", ".json", ".toml"):
                    rel_path = f"config/{rel_path}"
                elif ext in (".md", ".txt", ".rst"):
                    rel_path = f"docs/{rel_path}"
                elif ext in (".html", ".css", ".js", ".ts", ".tsx", ".jsx"):
                    rel_path = f"ui/src/{rel_path}"
                elif ext == ".schema.json":
                    rel_path = f"schemas/{rel_path}"
                # else: keep path as-is

            file_path = self.target_dir / rel_path

            try:
                # Create directories
                file_path.parent.mkdir(parents=True, exist_ok=True)

                # Clean content (remove leading/trailing whitespace, ensure newline at end)
                clean_content = content.strip() + "\n"

                # Write file
                file_path.write_text(clean_content, encoding="utf-8")
                written_files.append(str(rel_path))
                logger.info(f"  ✓ Wrote: {rel_path}")

            except Exception as e:
                logger.error(f"  ✗ Failed to write {rel_path}: {e}")

        return written_files

    async def _setup_mcp(self) -> None:
        """Initialize MCP servers (memory + filesystem) for this run."""
        if not self.enable_mcp:
            return

        # Keep memory scoped to the target directory by default.
        memory_path = self.mcp_memory_path
        if memory_path is None:
            memory_path = str((self.target_dir / "mcp_memory.json").resolve())

        # Allow filesystem tools to operate only under repo root.
        repo_root = Path.cwd().resolve()

        self._mcp_registry = await setup_default_mcp_servers(
            allowed_directories=[str(repo_root)],
            github_token=os.environ.get("GITHUB_TOKEN"),
            enable_memory=True,
            memory_path=memory_path,
        )

    async def _memory_upsert(
        self, key: str, value: object, tags: Optional[List[str]] = None
    ) -> None:
        if not self.enable_mcp or not self._mcp_registry:
            return
        try:
            await self._mcp_registry.invoke_tool(
                "memory", "upsert", {"key": key, "value": value, "tags": tags or []}
            )
        except Exception as e:
            logger.debug(f"Memory upsert failed for {key}: {e}")

    async def _memory_get(self, key: str) -> Optional[Dict]:
        if not self.enable_mcp or not self._mcp_registry:
            return None
        try:
            resp = await self._mcp_registry.invoke_tool("memory", "get", {"key": key})
            if not resp.success:
                return None
            return resp.result
        except Exception:
            return None

    async def _memory_snapshot(self, prefix: str, limit: int = 25) -> str:
        """Build a small, safe memory snapshot string for prompt context."""
        if not self.enable_mcp or not self._mcp_registry:
            return ""
        try:
            resp = await self._mcp_registry.invoke_tool(
                "memory", "list", {"prefix": prefix, "limit": limit}
            )
            if not resp.success:
                return ""
            keys = resp.result.get("keys", [])
            if not keys:
                return ""
            return "MCP Memory Keys:\n" + "\n".join(f"- {k}" for k in keys)
        except Exception:
            return ""

    def _read_documents(self) -> str:
        """Read all input documents."""
        docs = []

        # Read plan
        if self.plan_path.exists():
            docs.append(
                f"=== IMPLEMENTATION PLAN ===\n{self.plan_path.read_text(encoding='utf-8')}"
            )

        # Read architecture docs
        for doc_path in self.architecture_docs:
            if doc_path.exists():
                docs.append(
                    f"=== {doc_path.name} ===\n{doc_path.read_text(encoding='utf-8')}"
                )

        return "\n\n".join(docs)

    def _read_document_parts(self) -> List[tuple[str, str]]:
        """Read input documents as (title, text) pairs for per-doc
        summarization."""
        parts: List[tuple[str, str]] = []

        if self.plan_path.exists():
            parts.append(
                ("IMPLEMENTATION PLAN", self.plan_path.read_text(encoding="utf-8"))
            )

        for doc_path in self.architecture_docs:
            if doc_path.exists():
                parts.append((doc_path.name, doc_path.read_text(encoding="utf-8")))

        return parts

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Very rough token estimate to decide when to compress.

        Rule of thumb: ~4 chars/token for English-ish text.
        """
        if not text:
            return 0
        return max(1, len(text) // 4)

    async def _call_agent(
        self,
        prompt: str,
        tier: int,
        agent_name: str,
    ) -> str:
        """Call an agent with the smart router."""
        logger.info(f"Calling {agent_name} (tier {tier})...")

        if self.dry_run:
            return f"[DRY RUN] {agent_name} would process with tier {tier} model"

        try:
            # If use_cloud is set and tier >= 2, use GitHub Models (CLI-based)
            if self.use_cloud and tier >= 2:
                # Debug: show prompt size
                logger.debug(f"Prompt size: {len(prompt)} chars")
                est_tokens = self._estimate_tokens(prompt)
                logger.debug(f"Estimated prompt size: ~{est_tokens} tokens")

                # If we're likely to exceed the provider budget, hard-trim. We prefer trimming
                # to immediate 413 failures.
                if est_tokens > self.cloud_prompt_token_budget:
                    logger.warning(
                        f"Prompt likely too large (~{est_tokens} tokens). Trimming to fit budget {self.cloud_prompt_token_budget}."
                    )
                    # Keep the tail trimmed as well; models usually need the instructions + a slice of context.
                    target_chars = self.cloud_prompt_token_budget * 4
                    if len(prompt) > target_chars:
                        prompt = (
                            prompt[:target_chars]
                            + "\n\n[... truncated to fit token budget ...]"
                        )

                if self.max_prompt_chars and len(prompt) > self.max_prompt_chars:
                    logger.warning(
                        f"Prompt too long ({len(prompt)} chars), truncating to {self.max_prompt_chars} chars"
                    )
                    prompt = (
                        prompt[: self.max_prompt_chars]
                        + "\n\n[... truncated for length ...]"
                    )
                # Lower temperature for agents that must emit strict structured output
                temperature = (
                    0.2
                    if agent_name in {"Requirements Analyst", "Orchestrator", "Judge"}
                    else 0.7
                )

                # GitHub Models endpoint often enforces small total token budgets; keep max_tokens modest.
                if agent_name in {"Requirements Analyst", "Orchestrator", "Judge"}:
                    max_tokens = 2048
                else:
                    max_tokens = 4096

                for model in self.cloud_models:
                    try:
                        logger.info(f"Using model: {model}")
                        result = LLMClient.generate_text(
                            model,
                            prompt,
                            max_tokens=max_tokens,
                            temperature=temperature,
                        )
                        if (
                            result
                            and not result.startswith("Error")
                            and not result.startswith("gh models error")
                        ):
                            logger.info(f"{agent_name} completed using {model}")
                            return result
                        logger.warning(
                            f"Model {model} returned error: {result[:200] if result else 'empty'}"
                        )
                    except Exception as e:
                        logger.warning(f"Model {model} failed: {e}, trying next...")
                        continue
                raise RuntimeError("All models failed")

            # Otherwise use the smart router
            result, model_used = await self.router.call_with_fallback(
                tier=tier,
                prompt=prompt,
                max_tokens=8192,
                temperature=0.7,
                llm_client=LLMClient,
            )
            logger.info(f"{agent_name} completed using {model_used}")
            return result
        except Exception as e:
            logger.error(f"{agent_name} failed: {e}")
            raise

    async def _summarize_large_text(
        self,
        title: str,
        text: str,
        *,
        chunk_chars: int = 9000,
    ) -> str:
        """Summarize large text into a compact brief using chunked passes.

        This is used to avoid GitHub Models request token limits.
        """
        if self.dry_run:
            return f"[DRY RUN] Summary for {title} (original {len(text)} chars)"

        def chunks(s: str, size: int) -> List[str]:
            return [s[i : i + size] for i in range(0, len(s), size)]

        summarizer_prompt_tpl = (
            "You are summarizing an architecture/planning document for engineering implementation.\n\n"
            "Document: {title}\n"
            "Chunk {idx}/{total}\n\n"
            "Extract ONLY what helps implementation. Include:\n"
            "- Key deliverables/components\n"
            "- Interfaces/contracts (inputs/outputs)\n"
            "- Constraints/assumptions\n"
            "- Acceptance/verification notes\n\n"
            "Return a concise bullet list.\n\n"
            "CHUNK:\n{text}"
        )

        chunk_summaries: List[str] = []
        parts = chunks(text, chunk_chars)
        for i, part in enumerate(parts, start=1):
            prompt = summarizer_prompt_tpl.format(
                title=title, idx=i, total=len(parts), text=part
            )
            if self.use_cloud:
                # Use the most lightweight cloud model first; keep output small.
                for model in self.cloud_summarizer_models:
                    try:
                        out = LLMClient.generate_text(
                            model, prompt, max_tokens=1024, temperature=0.2
                        )
                        if (
                            out
                            and not out.startswith("Error")
                            and not out.startswith("gh models error")
                        ):
                            chunk_summaries.append(out.strip())
                            break
                    except Exception:
                        continue
                else:
                    chunk_summaries.append("[Summary failed for chunk]")
            else:
                # Local path: reuse the router so this works without GitHub Models.
                out, _ = await self.router.call_with_fallback(
                    tier=1,
                    prompt=prompt,
                    max_tokens=1024,
                    temperature=0.2,
                    llm_client=LLMClient,
                )
                chunk_summaries.append(out.strip())

        combined = "\n\n".join(chunk_summaries)
        if len(combined) <= chunk_chars:
            return combined

        # Final compression pass
        final_prompt = (
            "You are consolidating chunk summaries into a single implementation brief.\n\n"
            "Combine and deduplicate. Produce:\n"
            "- Components\n- Dependencies\n- Key requirements\n- Risks\n- Verification\n\n"
            f"SUMMARIES:\n{combined}"
        )
        for model in self.cloud_summarizer_models:
            try:
                out = LLMClient.generate_text(
                    model, final_prompt, max_tokens=1536, temperature=0.2
                )
                if (
                    out
                    and not out.startswith("Error")
                    and not out.startswith("gh models error")
                ):
                    return out.strip()
            except Exception:
                continue

        if not self.use_cloud:
            out, _ = await self.router.call_with_fallback(
                tier=1,
                prompt=final_prompt,
                max_tokens=1536,
                temperature=0.2,
                llm_client=LLMClient,
            )
            return out.strip()

        return combined[:chunk_chars]

    def _parse_json_response(self, response: str) -> Dict:
        """Extract JSON from response."""
        import re

        decoder = json.JSONDecoder()

        # Try to find JSON in code block
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", response)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Heuristic: some models emit reasoning wrappers like <think>...</think> (or <analysis>...</analysis>)
        # followed by the actual JSON. Try parsing the tail after the last closing tag.
        tail = response
        if "</think>" in tail:
            tail = tail.rsplit("</think>", 1)[-1]
        if "</analysis>" in tail:
            tail = tail.rsplit("</analysis>", 1)[-1]
        tail = tail.strip()
        if tail:
            try:
                parsed = json.loads(tail)
                if isinstance(parsed, dict):
                    return parsed
                return {"raw_json": parsed}
            except json.JSONDecodeError:
                pass

        # Try raw JSON (response might include leading/trailing whitespace)
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            pass

        # Robust salvage: scan from the end for the last decodable JSON object/array.
        # This handles outputs like: reasoning text + JSON, or multiple JSON snippets.
        # We prefer the *last* valid JSON since many models provide examples first.
        starts = [m.start() for m in re.finditer(r"[\[{]", response)]
        for start in reversed(starts[-500:]):
            try:
                parsed, _end = decoder.raw_decode(response[start:].lstrip())
            except json.JSONDecodeError:
                continue

            # Most call sites expect a dict. Preserve non-dict JSON for debugging.
            if isinstance(parsed, dict):
                return parsed
            return {"raw_json": parsed}

        # Return as text
        return {"raw": response}

    async def analyze_requirements(self) -> Dict:
        """Phase 1: Requirements Analyst processes documents."""
        logger.info("=" * 60)
        logger.info("PHASE 1: Requirements Analysis")
        logger.info("=" * 60)

        # Build a compact per-document brief first. This is the most effective way to stay under
        # GitHub Models request-size limits.
        raw_parts = self._read_document_parts()
        raw_total_chars = sum(len(t) for _, t in raw_parts)

        doc_briefs: List[str] = []
        for title, text in raw_parts:
            # Always summarize in cloud mode; otherwise we risk 413 even for "medium" sized docs.
            if self.use_cloud:
                brief = await self._summarize_large_text(title, text, chunk_chars=6000)
            else:
                # Local mode: keep more raw content (still capped).
                if self.max_doc_chars and len(text) > self.max_doc_chars:
                    brief = text[: self.max_doc_chars] + "\n\n[... truncated ...]"
                else:
                    brief = text
            doc_briefs.append(f"=== {title} (BRIEF) ===\n{brief}")

        documents = "\n\n".join(doc_briefs)
        await self._memory_upsert(
            key="agentic-workflows-v2/documents_brief",
            value={
                "brief": documents,
                "original_total_chars": raw_total_chars,
                "sources": [t for t, _ in raw_parts],
            },
            tags=["summary"],
        )

        # Use a shorter requirements prompt for cloud to reduce token overhead.
        if self.use_cloud:
            prompt = (
                "You are the Requirements Analyst.\n"
                "Given the document briefs below, produce a JSON object with:\n"
                "- summary: short paragraph\n"
                "- key_requirements: list of strings\n"
                "- constraints: list of strings\n"
                "- milestones: list of {name, deliverables[]}\n"
                "- risks: list of strings\n"
                "Return ONLY valid JSON.\n\n"
                f"DOCUMENT BRIEFS:\n{documents}"
            )
        else:
            prompt = REQUIREMENTS_ANALYST_PROMPT.format(documents=documents)

        response = await self._call_agent(
            prompt, tier=3, agent_name="Requirements Analyst"
        )
        self.requirements = self._parse_json_response(response)

        await self._memory_upsert(
            key="agentic-workflows-v2/requirements_analysis",
            value=self.requirements,
            tags=["requirements"],
        )

        # Save raw response for debugging
        raw_path = self.target_dir / "requirements_analysis.raw.txt"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(response, encoding="utf-8")

        # Save requirements
        req_path = self.target_dir / "requirements_analysis.json"
        req_path.parent.mkdir(parents=True, exist_ok=True)
        req_path.write_text(json.dumps(self.requirements, indent=2), encoding="utf-8")
        logger.info(f"Saved requirements to {req_path}")

        return self.requirements

    async def create_tasks(self, iteration: int) -> List[Task]:
        """Orchestrator breaks requirements into tasks."""
        logger.info("=" * 60)
        logger.info(f"PHASE 2: Task Planning (Iteration {iteration})")
        logger.info("=" * 60)

        completed = [t.id for t in self.tasks if t.status == "completed"]
        failed = [t.id for t in self.tasks if t.status == "failed"]

        # Use compact JSON to reduce prompt size without losing content.
        requirements_json = json.dumps(
            self.requirements, ensure_ascii=False, separators=(",", ":")
        )

        memory_snapshot = await self._memory_snapshot(prefix="agentic-workflows-v2/")
        if memory_snapshot:
            requirements_json = requirements_json + "\n\n" + memory_snapshot

        prompt = ORCHESTRATOR_PROMPT.format(
            requirements=requirements_json,
            iteration=iteration,
            max_iterations=self.max_iterations,
            completed=completed,
            failed=failed,
        )

        response = await self._call_agent(prompt, tier=3, agent_name="Orchestrator")
        task_data = self._parse_json_response(response)

        await self._memory_upsert(
            key=f"agentic-workflows-v2/orchestrator/iter_{iteration}",
            value=task_data,
            tags=["orchestrator", f"iter:{iteration}"],
        )

        # Save orchestrator output for debugging/repro
        out_dir = self.target_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"orchestrator_iter_{iteration}.raw.txt").write_text(
            response, encoding="utf-8"
        )
        (out_dir / f"orchestrator_iter_{iteration}.parsed.json").write_text(
            json.dumps(task_data, indent=2), encoding="utf-8"
        )

        new_tasks = []
        for t in task_data.get("tasks", []):
            task = Task(
                id=t.get("id", f"TASK-{len(self.tasks)+1}"),
                title=t.get("title", "Unnamed task"),
                description=t.get("description", ""),
                phase=t.get("phase", 1),
                tier=t.get("tier", 2),
                assigned_to=t.get("assigned_to", "developer"),
                dependencies=t.get("dependencies", []),
            )
            new_tasks.append(task)

        if not new_tasks:
            logger.warning(
                "Orchestrator produced 0 tasks. Saved raw/parsed outputs to target directory for inspection."
            )

        self.tasks.extend(new_tasks)
        logger.info(f"Created {len(new_tasks)} new tasks")

        return new_tasks

    def _ensure_package_scaffold(self) -> List[str]:
        """Create the basic package scaffold if it doesn't exist.

        Returns list of files created.
        """
        files_created = []

        # pyproject.toml
        pyproject_path = self.target_dir / "pyproject.toml"
        if not pyproject_path.exists():
            pyproject_content = """[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "agentic-workflows-v2"
version = "0.1.0"
description = "Tier-based multi-model AI workflow orchestration"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.25",
    "jinja2>=3.0",
    "jmespath>=1.0",
    "pyyaml>=6.0",
    "aiofiles>=23.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
]
server = [
    "fastapi>=0.100",
    "uvicorn>=0.23",
]

[tool.hatch.build.targets.wheel]
packages = ["src/agentic_v2"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
"""
            pyproject_path.parent.mkdir(parents=True, exist_ok=True)
            pyproject_path.write_text(pyproject_content, encoding="utf-8")
            files_created.append("pyproject.toml")
            logger.info("  ✓ Created pyproject.toml")

        # README.md
        readme_path = self.target_dir / "README.md"
        if not readme_path.exists():
            readme_content = """# agentic-workflows-v2

Tier-based multi-model AI workflow orchestration.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from agentic_v2 import Orchestrator, Task

# Create orchestrator
orch = Orchestrator()

# Define a task
task = Task(
    name="analyze_code",
    tier=2,  # Medium complexity
    input={"code": "def hello(): pass"}
)

# Run
result = await orch.run(task)
```

## Features

- **Tier-based routing**: Route tasks to appropriate model sizes
- **Smart fallback**: Automatic retry with different models
- **Pydantic contracts**: Type-safe inputs/outputs
- **Async-first**: Built for concurrent execution
"""
            readme_path.write_text(readme_content, encoding="utf-8")
            files_created.append("README.md")
            logger.info("  ✓ Created README.md")

        # src/agentic_v2/__init__.py
        init_path = self.target_dir / "src" / "agentic_v2" / "__init__.py"
        if not init_path.exists():
            init_content = '''"""Agentic Workflows V2 - Tier-based multi-model orchestration."""
from __future__ import annotations

__version__ = "0.1.0"
__all__ = ["__version__"]
'''
            init_path.parent.mkdir(parents=True, exist_ok=True)
            init_path.write_text(init_content, encoding="utf-8")
            files_created.append("src/agentic_v2/__init__.py")
            logger.info("  ✓ Created src/agentic_v2/__init__.py")

        # tests/__init__.py
        tests_init = self.target_dir / "tests" / "__init__.py"
        if not tests_init.exists():
            tests_init.parent.mkdir(parents=True, exist_ok=True)
            tests_init.write_text(
                '"""Test suite for agentic-workflows-v2."""\n', encoding="utf-8"
            )
            files_created.append("tests/__init__.py")
            logger.info("  ✓ Created tests/__init__.py")

        return files_created

    def _detect_language_from_task(self, task: Task) -> str:
        """Detect the primary language for a task based on its description and
        output files.

        Following GitHub Copilot best practices: detect context, then inject relevant rules.
        """
        description_lower = (task.title + " " + task.description).lower()

        # Check for explicit language mentions
        if any(
            word in description_lower
            for word in ["python", "pydantic", ".py", "pytest"]
        ):
            return "python"
        if any(word in description_lower for word in ["c#", "csharp", ".cs", "dotnet"]):
            return "csharp"
        if any(word in description_lower for word in ["java", ".java", "spring"]):
            return "java"
        if any(
            word in description_lower for word in ["typescript", ".ts", ".tsx", "react"]
        ):
            return "typescript"
        if any(
            word in description_lower for word in ["javascript", ".js", ".jsx", "node"]
        ):
            return "javascript"
        if any(
            word in description_lower for word in ["yaml", ".yaml", ".yml", "config"]
        ):
            return "yaml"
        if any(word in description_lower for word in ["json", ".json", "package.json"]):
            return "json"

        # Default to Python for this project (agentic-workflows-v2 is Python-based)
        return "python"

    def _build_language_specific_rules(self, language: str) -> str:
        """Build language-specific rules section for DEVELOPER_PROMPT.

        Industry best practice: inject ONLY relevant rules, avoid language bias.
        """
        if language not in LANGUAGE_STANDARDS:
            return ""

        std = LANGUAGE_STANDARDS[language]
        rules_section = f"""LANGUAGE: {language.upper()} {std['version']}

STANDARDS:
"""
        for rule in std["rules"]:
            rules_section += f"- {rule}\n"

        if std["imports_example"]:
            rules_section += f"\nTYPICAL IMPORTS:\n{std['imports_example']}\n"

        return rules_section

    async def execute_task(self, task: Task) -> Task:
        """Execute a single task."""
        logger.info(f"Executing task: {task.id} - {task.title}")
        task.status = "in_progress"

        # Build context from dependencies
        context_parts = []
        for dep_id in task.dependencies:
            dep_task = next((t for t in self.tasks if t.id == dep_id), None)
            if dep_task and dep_task.output:
                context_parts.append(
                    f"=== {dep_id} output ===\n{dep_task.output[:5000]}"
                )

        # Code-producing agent types use DEVELOPER_PROMPT
        code_agents = {
            "developer",
            "PackageArchitect",
            "APIDesigner",
            "ToolBuilder",
            "AgentBuilder",
            "RouterDeveloper",
            "TestWriter",
        }

        memory_snapshot = await self._memory_snapshot(prefix="agentic-workflows-v2/")
        if memory_snapshot:
            context_parts.append("=== MCP MEMORY SNAPSHOT ===\n" + memory_snapshot)

        if task.assigned_to in code_agents:
            # Detect language and inject ONLY relevant rules (industry best practice)
            detected_language = self._detect_language_from_task(task)
            language_rules = self._build_language_specific_rules(detected_language)

            prompt = DEVELOPER_PROMPT.format(
                language_specific_rules=language_rules,
                task_title=task.title,
                task_description=task.description,
                context=(
                    "\n".join(context_parts) if context_parts else "No prior context"
                ),
            )
        else:
            # Generic prompt for non-code agents
            prompt = f"""Task: {task.title}
Description: {task.description}
Context: {context_parts}

Complete this task and provide the output."""

        try:
            response = await self._call_agent(
                prompt, tier=task.tier, agent_name=task.assigned_to
            )
            task.output = response
            task.status = "completed"

            await self._memory_upsert(
                key=f"agentic-workflows-v2/tasks/{task.id}",
                value={
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "assigned_to": task.assigned_to,
                    "files_created": task.files_created,
                    "output": (task.output[:20000] if task.output else None),
                },
                tags=["task", task.status, f"assigned:{task.assigned_to}"],
            )

            # Extract and WRITE files if code was generated
            task.files_created = self._extract_and_write_files(response, task.id)

            logger.info(
                f"Task {task.id} completed - wrote {len(task.files_created)} files"
            )

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            logger.error(f"Task {task.id} failed: {e}")

            await self._memory_upsert(
                key=f"agentic-workflows-v2/tasks/{task.id}",
                value={
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "assigned_to": task.assigned_to,
                    "error": task.error,
                },
                tags=["task", "failed", f"assigned:{task.assigned_to}"],
            )

        return task

    async def execute_tasks_chunked(self, tasks: List[Task], chunk_size: int = 3):
        """Execute tasks in chunks, respecting dependencies."""
        # Group by dependencies
        ready = [
            t
            for t in tasks
            if all(
                any(d.id == dep and d.status == "completed" for d in self.tasks)
                for dep in t.dependencies
            )
            or not t.dependencies
        ]

        while ready:
            chunk = ready[:chunk_size]
            logger.info(f"Executing chunk of {len(chunk)} tasks...")

            # Execute chunk (could be parallel with asyncio.gather if desired)
            for task in chunk:
                await self.execute_task(task)

            # Update ready list
            completed_ids = {t.id for t in self.tasks if t.status == "completed"}
            ready = [
                t
                for t in tasks
                if t.status == "pending"
                and all(dep in completed_ids for dep in t.dependencies)
            ]

    async def judge_iteration(self, iteration: int) -> Dict:
        """Judge evaluates the iteration."""
        logger.info("=" * 60)
        logger.info(f"PHASE 5: Judge Evaluation (Iteration {iteration})")
        logger.info("=" * 60)

        completed = [t for t in self.tasks if t.status == "completed"]
        failed = [t for t in self.tasks if t.status == "failed"]

        prompt = JUDGE_PROMPT.format(
            iteration=iteration,
            max_iterations=self.max_iterations,
            plan_summary="Implementing agentic-workflows-v2 module",
            completed_tasks=json.dumps(
                [{"id": t.id, "title": t.title} for t in completed]
            ),
            failed_tasks=json.dumps([{"id": t.id, "error": t.error} for t in failed]),
            test_results="[Tests not yet implemented]",
            containment_report="[Containment check pending]",
        )

        response = await self._call_agent(prompt, tier=3, agent_name="Judge")
        decision = self._parse_json_response(response)

        logger.info(f"Judge decision: {decision.get('decision', 'unknown')}")
        logger.info(f"Score: {decision.get('score', 0)}")

        return decision

    async def run(self):
        """Run the complete implementation workflow."""
        logger.info("=" * 60)
        logger.info("STARTING IMPLEMENTATION WORKFLOW")
        logger.info("=" * 60)

        start_time = time.time()

        try:
            # Ensure target directory exists
            self.target_dir.mkdir(parents=True, exist_ok=True)

            # Create package scaffold (pyproject.toml, README, __init__.py)
            if not self.dry_run:
                scaffold_files = self._ensure_package_scaffold()
                if scaffold_files:
                    logger.info(
                        f"Created package scaffold: {len(scaffold_files)} files"
                    )

            # Optional: MCP setup (memory + filesystem)
            await self._setup_mcp()

            # Phase 1: Analyze requirements
            await self.analyze_requirements()

            # Iteration loop
            for iteration in range(1, self.max_iterations + 1):
                logger.info(f"\n{'='*60}")
                logger.info(f"ITERATION {iteration}/{self.max_iterations}")
                logger.info(f"{'='*60}\n")

                # Phase 2: Create/update tasks
                new_tasks = await self.create_tasks(iteration)

                if not new_tasks:
                    logger.info("No new tasks created, checking completion...")
                    if not self.tasks:
                        # We have no tasks at all; continuing would just spin.
                        logger.warning(
                            "No tasks were produced and no tasks exist yet. Running judge for evaluation and exiting early."
                        )

                # Phase 3: Execute tasks in chunks
                pending_tasks = [t for t in self.tasks if t.status == "pending"]
                if pending_tasks:
                    await self.execute_tasks_chunked(pending_tasks)

                # Phase 4: Judge
                decision = await self.judge_iteration(iteration)

                # If we still have zero tasks after judging, exit regardless of the judge's decision.
                if not self.tasks:
                    logger.warning(
                        "Exiting: no tasks were ever created, so the workflow cannot make progress."
                    )
                    # Normalize final decision so reports are unambiguous.
                    decision = dict(decision)
                    decision.setdefault("decision", "NO_TASKS_EXIT")
                    break

                # Record iteration
                state = IterationState(
                    iteration=iteration,
                    tasks=self.tasks.copy(),
                    completed_tasks=[
                        t.id for t in self.tasks if t.status == "completed"
                    ],
                    failed_tasks=[t.id for t in self.tasks if t.status == "failed"],
                    score=decision.get("score", 0),
                    judge_decision=decision.get("decision", "unknown"),
                    feedback=decision.get("iteration_feedback", ""),
                )
                self.iteration_history.append(state)

                # Check exit condition
                if decision.get("decision") == "PASS":
                    logger.info("🎉 IMPLEMENTATION COMPLETE!")
                    break
                elif decision.get("decision") == "FAIL":
                    logger.error("❌ Implementation failed - stopping")
                    break
                else:
                    logger.info(f"Continuing to iteration {iteration + 1}...")

            # Final report
            elapsed = time.time() - start_time
            logger.info(f"\n{'='*60}")
            logger.info("FINAL REPORT")
            logger.info(f"{'='*60}")
            logger.info(f"Total time: {elapsed:.1f}s")
            logger.info(f"Iterations: {len(self.iteration_history)}")
            logger.info(
                f"Tasks completed: {len([t for t in self.tasks if t.status == 'completed'])}"
            )
            logger.info(
                f"Tasks failed: {len([t for t in self.tasks if t.status == 'failed'])}"
            )

            # Save final state
            final_state = {
                "timestamp": datetime.now().isoformat(),
                "elapsed_seconds": elapsed,
                "iterations": len(self.iteration_history),
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "status": t.status,
                        "files": t.files_created,
                    }
                    for t in self.tasks
                ],
                "final_decision": (
                    self.iteration_history[-1].judge_decision
                    if self.iteration_history
                    else "none"
                ),
            }

            state_path = self.target_dir / "implementation_state.json"
            state_path.write_text(json.dumps(final_state, indent=2), encoding="utf-8")
            logger.info(f"Saved state to {state_path}")

        except Exception as e:
            logger.exception(f"Workflow failed: {e}")
            raise


async def main():
    parser = argparse.ArgumentParser(
        description="Run agentic-workflows-v2 implementation"
    )
    parser.add_argument(
        "--plan", default="docs/planning/agentic-workflows-v2-phased-implementation.md"
    )
    parser.add_argument(
        "--arch",
        nargs="+",
        default=[
            "docs/planning/agentic-workflows-v2-architecture.md",
            "docs/planning/agentic-workflows-v2-implementation-patterns.md",
        ],
    )
    parser.add_argument("--target", default="agentic-workflows-v2")
    parser.add_argument("--max-iterations", type=int, default=5)
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't make actual LLM calls"
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument(
        "--use-cloud",
        action="store_true",
        help="Prefer cloud models for planning tasks",
    )
    parser.add_argument(
        "--scaffold-only",
        action="store_true",
        help="Only create the package scaffold (pyproject/README/src/agentic_v2/tests) and exit.",
    )
    parser.add_argument(
        "--enable-mcp",
        action="store_true",
        help="Enable MCP memory/filesystem integration",
    )
    parser.add_argument(
        "--mcp-memory-path", default=None, help="Optional path for MCP memory JSON file"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Change to repo root (multiagent-workflows/scripts -> prompts repo root)
    repo_root = Path(__file__).parents[2]  # scripts -> multiagent-workflows -> prompts
    os.chdir(repo_root)
    logger.info(f"Working directory: {os.getcwd()}")

    runner = ImplementationRunner(
        plan_path=args.plan,
        architecture_docs=args.arch,
        target_dir=args.target,
        max_iterations=args.max_iterations,
        dry_run=args.dry_run,
        use_cloud=args.use_cloud,
        enable_mcp=args.enable_mcp,
        mcp_memory_path=args.mcp_memory_path,
    )

    if args.scaffold_only:
        logger.info("Creating scaffold only (no LLM calls will be made)...")
        runner.target_dir.mkdir(parents=True, exist_ok=True)
        scaffold_files = runner._ensure_package_scaffold()
        logger.info(f"Scaffold complete: {len(scaffold_files)} file(s) created")
        return

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())
