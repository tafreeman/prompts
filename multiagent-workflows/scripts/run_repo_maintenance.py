"""
Repository Maintenance Workflow - LangChain Implementation

A multi-agent LangChain workflow with a Librarian orchestrator that coordinates:
- Explorer: Maps repository structure
- Tester: Validates tool functionality
- Documenter: Audits and updates documentation
- Cleanup: Identifies duplicates and orphaned files
- Engineering Expert: Analyzes code quality and best practices

Usage:
    python run_repo_maintenance.py --repo-path /path/to/repo [--dry-run]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# Standardized Contracts for Inter-Agent Communication
# ============================================================================

class ItemStatus(str, Enum):
    """Status of an item after agent analysis."""
    HEALTHY = "healthy"           # No issues found
    WARNING = "warning"           # Minor issues
    NEEDS_REVIEW = "needs_review"  # Requires human attention
    DEPRECATED = "deprecated"     # Should be archived/removed
    CRITICAL = "critical"         # Immediate action required
    UNKNOWN = "unknown"           # Could not determine status
    PASSING = "passing"           # Test passed
    FAILING = "failing"           # Test failed
    SKIPPED = "skipped"           # Test skipped
    ERROR = "error"               # Error during analysis


class ItemPriority(str, Enum):
    """Priority level for recommendations."""
    CRITICAL = "critical"  # P0 - Fix immediately
    HIGH = "high"          # P1 - Fix soon
    MEDIUM = "medium"      # P2 - Fix when convenient
    LOW = "low"            # P3 - Nice to have
    INFO = "info"          # Informational only


class ItemAction(str, Enum):
    """Recommended action for an item."""
    PRESERVE = "preserve"          # Keep as-is
    ARCHIVE = "archive"            # Move to archive
    DELETE = "delete"              # Safe to remove
    REFACTOR = "refactor"          # Needs code changes
    DOCUMENT = "document"          # Needs documentation
    TEST = "test"                  # Needs test coverage
    REVIEW = "review"              # Needs human review
    MERGE = "merge"                # Consolidate with another file
    FIX_SECURITY = "fix_security"  # Security issue to address
    UPDATE = "update"              # Needs update/refresh
    SKIP = "skip"                  # No action needed


class IssueCategory(str, Enum):
    """Category of issues found."""
    SECURITY = "security"
    QUALITY = "quality"
    BEST_PRACTICES = "best_practices"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    TECHNICAL_DEBT = "technical_debt"
    DUPLICATE = "duplicate"
    ORPHAN = "orphan"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"


class FileType(str, Enum):
    """Type of file being analyzed."""
    PYTHON = "python"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    CONFIG = "config"
    TEST = "test"
    TOOL = "tool"
    SCRIPT = "script"
    DOCUMENTATION = "documentation"
    OTHER = "other"


class TestStatus(str, Enum):
    """Status of a test execution."""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"
    NOT_RUN = "not_run"


class DocStatus(str, Enum):
    """Status of documentation."""
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    OUTDATED = "outdated"
    MISSING = "missing"
    BROKEN_LINKS = "broken_links"


@dataclass
class MaintenanceItem:
    """Standardized item for inter-agent communication."""
    path: str
    status: ItemStatus
    priority: ItemPriority
    action: ItemAction
    category: IssueCategory
    message: str
    agent: str  # Which agent identified this
    confidence: float = 0.8  # 0-1 confidence score
    line_number: Optional[int] = None  # Line number if applicable
    notes: List[str] = field(default_factory=list)  # Additional notes
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": self.path,
            "status": self.status.value,
            "priority": self.priority.value,
            "action": self.action.value,
            "category": self.category.value,
            "message": self.message,
            "agent": self.agent,
            "confidence": self.confidence,
            "line_number": self.line_number,
            "notes": self.notes,
            "details": self.details
        }


@dataclass
class FileAnalysisItem:
    """Result from file analysis (Explorer, Engineering)."""
    path: str
    file_type: FileType
    status: ItemStatus
    size_bytes: int = 0
    line_count: int = 0
    issues: List[MaintenanceItem] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "file_type": self.file_type.value,
            "status": self.status.value,
            "size_bytes": self.size_bytes,
            "line_count": self.line_count,
            "issues": [i.to_dict() for i in self.issues],
            "notes": self.notes
        }


@dataclass
class TestResultItem:
    """Result from test execution."""
    path: str
    test_status: TestStatus
    execution_time_ms: float = 0
    error_message: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "test_status": self.test_status.value,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
            "notes": self.notes
        }


@dataclass
class DocAuditItem:
    """Result from documentation audit."""
    path: str
    doc_status: DocStatus
    broken_links: List[str] = field(default_factory=list)
    missing_sections: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "doc_status": self.doc_status.value,
            "broken_links": self.broken_links,
            "missing_sections": self.missing_sections,
            "notes": self.notes
        }


@dataclass
class CleanupItem:
    """Recommendation for file cleanup."""
    path: str
    action: ItemAction
    priority: ItemPriority
    reason: str
    related_files: List[str] = field(default_factory=list)  # Duplicates, etc.
    risk_level: str = "low"  # low, medium, high
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "action": self.action.value,
            "priority": self.priority.value,
            "reason": self.reason,
            "related_files": self.related_files,
            "risk_level": self.risk_level,
            "notes": self.notes
        }


@dataclass
class AgentResult:
    """Standardized result from any agent."""
    agent_name: str
    success: bool
    items: List[MaintenanceItem] = field(default_factory=list)
    file_analyses: List[FileAnalysisItem] = field(default_factory=list)
    test_results: List[TestResultItem] = field(default_factory=list)
    doc_audits: List[DocAuditItem] = field(default_factory=list)
    cleanup_items: List[CleanupItem] = field(default_factory=list)
    summary: str = ""
    raw_llm_response: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "success": self.success,
            "items": [item.to_dict() for item in self.items],
            "file_analyses": [f.to_dict() for f in self.file_analyses],
            "test_results": [t.to_dict() for t in self.test_results],
            "doc_audits": [d.to_dict() for d in self.doc_audits],
            "cleanup_items": [c.to_dict() for c in self.cleanup_items],
            "summary": self.summary,
            "error": self.error
        }


# ============================================================================
# Tool Definitions for Agent Use
# ============================================================================

@dataclass
class ToolResult:
    """Result from a tool execution."""
    tool_name: str
    success: bool
    output: Any = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tool_name": self.tool_name,
            "success": self.success,
            "output": str(self.output)[:1000] if self.output else None,
            "error": self.error
        }


class AgentToolkit:
    """Tools available to agents for file operations and execution."""

    def __init__(self, repo_path: Path, dry_run: bool = True):
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.actions_log: List[Dict[str, Any]] = []

    def _log_action(self, tool: str, params: Dict, result: ToolResult):
        """Log all tool actions for audit."""
        self.actions_log.append({
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "params": params,
            "success": result.success,
            "dry_run": self.dry_run
        })

    def read_file(self, path: str, max_chars: int = 5000) -> ToolResult:
        """Read file contents."""
        try:
            full_path = self.repo_path / path
            if not full_path.exists():
                return ToolResult("read_file", False, error=f"File not found: {path}")
            if not full_path.is_file():
                return ToolResult("read_file", False, error=f"Not a file: {path}")

            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_chars)

            result = ToolResult("read_file", True, output=content)
            self._log_action("read_file", {"path": path}, result)
            return result
        except Exception as e:
            return ToolResult("read_file", False, error=str(e))

    def write_file(self, path: str, content: str) -> ToolResult:
        """Write content to a file."""
        try:
            full_path = self.repo_path / path

            if self.dry_run:
                result = ToolResult("write_file", True,
                                    output=f"[DRY RUN] Would write {len(content)} chars to {path}")
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                result = ToolResult("write_file", True, output=f"Wrote {len(content)} chars to {path}")

            self._log_action("write_file", {"path": path, "size": len(content)}, result)
            return result
        except Exception as e:
            return ToolResult("write_file", False, error=str(e))

    def move_file(self, src: str, dest: str) -> ToolResult:
        """Move/rename a file."""
        import shutil
        try:
            src_path = self.repo_path / src
            dest_path = self.repo_path / dest

            if not src_path.exists():
                return ToolResult("move_file", False, error=f"Source not found: {src}")

            if self.dry_run:
                result = ToolResult("move_file", True,
                                    output=f"[DRY RUN] Would move {src} -> {dest}")
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src_path), str(dest_path))
                result = ToolResult("move_file", True, output=f"Moved {src} -> {dest}")

            self._log_action("move_file", {"src": src, "dest": dest}, result)
            return result
        except Exception as e:
            return ToolResult("move_file", False, error=str(e))

    def delete_file(self, path: str) -> ToolResult:
        """Delete a file (moves to .trash by default in dry_run)."""
        try:
            full_path = self.repo_path / path

            if not full_path.exists():
                return ToolResult("delete_file", False, error=f"File not found: {path}")

            if self.dry_run:
                result = ToolResult("delete_file", True,
                                    output=f"[DRY RUN] Would delete {path}")
            else:
                # Safety: move to .trash instead of actual delete
                trash_path = self.repo_path / ".trash" / path
                trash_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.rename(trash_path)
                result = ToolResult("delete_file", True,
                                    output=f"Moved to trash: {path}")

            self._log_action("delete_file", {"path": path}, result)
            return result
        except Exception as e:
            return ToolResult("delete_file", False, error=str(e))

    def list_dir(self, path: str = ".") -> ToolResult:
        """List directory contents."""
        try:
            full_path = self.repo_path / path
            if not full_path.exists():
                return ToolResult("list_dir", False, error=f"Directory not found: {path}")

            entries = []
            for entry in full_path.iterdir():
                entries.append({
                    "name": entry.name,
                    "type": "dir" if entry.is_dir() else "file",
                    "size": entry.stat().st_size if entry.is_file() else 0
                })

            result = ToolResult("list_dir", True, output=entries)
            self._log_action("list_dir", {"path": path}, result)
            return result
        except Exception as e:
            return ToolResult("list_dir", False, error=str(e))

    def web_search(self, query: str, max_results: int = 5) -> ToolResult:
        """Search the web using DuckDuckGo."""
        try:
            import urllib.request
            import urllib.parse
            import json as _json
            
            # Use DuckDuckGo Instant Answer API (free, no auth required)
            encoded_query = urllib.parse.quote(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
            
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = _json.loads(response.read().decode('utf-8'))
            
            results = []
            
            # Abstract (main result)
            if data.get("Abstract"):
                results.append({
                    "title": data.get("Heading", "Result"),
                    "snippet": data["Abstract"],
                    "url": data.get("AbstractURL", "")
                })
            
            # Related topics
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if isinstance(topic, dict) and topic.get("Text"):
                    results.append({
                        "title": topic.get("Text", "")[:100],
                        "snippet": topic.get("Text", ""),
                        "url": topic.get("FirstURL", "")
                    })
            
            result = ToolResult("web_search", True, output=results[:max_results])
            self._log_action("web_search", {"query": query}, result)
            return result
        except Exception as e:
            return ToolResult("web_search", False, error=str(e))

    def remove_file_permanently(self, path: str, confirm: bool = False) -> ToolResult:
        """Permanently remove a file (requires confirm=True)."""
        try:
            full_path = self.repo_path / path

            if not full_path.exists():
                return ToolResult("remove_file_permanently", False, error=f"File not found: {path}")

            if not confirm:
                return ToolResult("remove_file_permanently", False, 
                                  error="Must set confirm=True to permanently delete")

            if self.dry_run:
                result = ToolResult("remove_file_permanently", True,
                                    output=f"[DRY RUN] Would permanently delete {path}")
            else:
                full_path.unlink()
                result = ToolResult("remove_file_permanently", True,
                                    output=f"Permanently deleted: {path}")

            self._log_action("remove_file_permanently", {"path": path, "confirm": confirm}, result)
            return result
        except Exception as e:
            return ToolResult("remove_file_permanently", False, error=str(e))

    def get_tool_descriptions(self) -> str:
        """Get description of available tools for LLM prompt."""
        return """Available Tools:
- read_file(path, max_chars=5000): Read file contents
- write_file(path, content): Write content to file
- move_file(src, dest): Move/rename file (use for archiving)
- delete_file(path): Delete file (moves to .trash for safety)
- remove_file_permanently(path, confirm=True): PERMANENTLY delete file (no recovery)
- list_dir(path="."): List directory contents
- web_search(query, max_results=5): Search the web for information

To use a tool, respond with:
ACTION: tool_name
PARAMS: {"param1": "value1", ...}

Wait for OBSERVATION before continuing."""


# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Try to use ModelManager (GitHub Models, Ollama, etc.)
try:
    from multiagent_workflows.core.model_manager import ModelManager
    MODEL_MANAGER_AVAILABLE = True
except ImportError:
    MODEL_MANAGER_AVAILABLE = False
    print("Warning: ModelManager not available. Run from multiagent-workflows directory.")

# Global model manager instance
_model_manager = None

def get_model_manager() -> "ModelManager":
    """Get or create the global ModelManager instance."""
    global _model_manager
    if _model_manager is None and MODEL_MANAGER_AVAILABLE:
        _model_manager = ModelManager()
    return _model_manager


class RepoMaintenanceAgent:
    """Base class for maintenance agents."""

    def __init__(self, name: str, role: str, model: str = "gh:openai/gpt-4o-mini"):
        self.name = name
        self.role = role
        self.model = model  # Now uses gh: prefix for GitHub Models
        self._manager = None

    @property
    def manager(self) -> "ModelManager":
        if self._manager is None:
            self._manager = get_model_manager()
        return self._manager
    
    async def call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """Call the LLM using ModelManager."""
        if self.manager:
            result = await self.manager.generate(
                model_id=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.0,
                max_tokens=4096,
            )
            return result.text
        return ""

    async def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute a task and return results."""
        raise NotImplementedError


class LibrarianAgent(RepoMaintenanceAgent):
    """
    The Librarian - Central Orchestrator

    Like a head librarian managing a library, this agent:
    - Knows the entire "collection" (repository structure)
    - Directs specialist agents to specific tasks
    - Maintains the catalog (inventory) of all items
    - Synthesizes reports from all departments
    - Makes final decisions on what to keep, archive, or discard
    """

    SYSTEM_PROMPT = """You are the Head Librarian of a code repository.

Your role is to:
1. CATALOG: Maintain a comprehensive inventory of all code, tools, and documentation
2. DIRECT: Assign specialist agents to their appropriate tasks
3. CURATE: Decide what belongs in the collection and what should be archived/removed
4. SYNTHESIZE: Combine reports from all specialists into coherent recommendations
5. PRESERVE: Ensure nothing valuable is lost during maintenance

You work with these specialist agents:
- Explorer: Maps the repository structure (your "catalog assistant")
- Tester: Validates tools work correctly (your "quality control")
- Documenter: Audits and updates documentation (your "reference librarian")
- Cleanup: Identifies duplicates and orphans (your "collection manager")
- Engineering Expert: Analyzes code quality and best practices (your "technical advisor")

Always prioritize preservation over deletion. When in doubt, archive don't delete."""

    def __init__(self):
        super().__init__(
            name="Librarian",
            role="Head Repository Librarian & Orchestrator",
            model="gh:openai/gpt-4o-mini"  # Fast orchestration model
        )
        self.catalog = {}
        self.task_queue = []
        self.completed_tasks = []
        self.specialists = {}

    def register_specialist(self, name: str, agent: RepoMaintenanceAgent):
        """Register a specialist agent with the librarian."""
        self.specialists[name] = agent
        print(f"   📚 Librarian registered specialist: {name} ({agent.role})")

    async def analyze_collection(self, repo_path: str) -> Dict[str, Any]:
        """Initial analysis of the repository collection."""
        print("\n📚 Librarian: Analyzing the collection...")
        if "explorer" in self.specialists:
            explorer_results = await self.specialists["explorer"].execute(repo_path)
            self.catalog["structure"] = explorer_results
            return explorer_results
        return {}

    async def delegate_task(self, specialist_name: str, task: str, *args, **kwargs) -> Dict[str, Any]:
        """Delegate a task to a specialist agent."""
        if specialist_name not in self.specialists:
            return {"error": f"Unknown specialist: {specialist_name}"}

        print(f"   📚 Librarian delegating to {specialist_name}: {task[:50]}...")
        result = await self.specialists[specialist_name].execute(*args, **kwargs)

        self.completed_tasks.append({
            "specialist": specialist_name,
            "task": task,
            "result_summary": self._summarize_result(result)
        })
        return result

    def _summarize_result(self, result: Dict[str, Any]) -> str:
        """Create a brief summary of a result."""
        if isinstance(result, dict):
            keys = list(result.keys())[:3]
            return f"Keys: {keys}"
        return str(result)[:100]

    async def curate_recommendations(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Curate final recommendations based on all specialist reports using LLM."""
        print("\n📚 Librarian: Curating final recommendations...")

        recommendations = {
            "preserve": [],
            "archive": [],
            "discard": [],
            "review": [],
            "improve": [],  # Items needing code quality improvements
            "llm_analysis": None,  # LLM-generated analysis
        }

        # First, do rule-based categorization
        cleanup = all_results.get("cleanup", {}).get("cleanup_plan", {})

        for item in cleanup.get("phase1_safe", []):
            recommendations["discard"].append({
                "path": item.get("path"),
                "reason": item.get("reason"),
                "confidence": "high"
            })

        for item in cleanup.get("phase2_medium", []):
            recommendations["archive"].append({
                "path": item.get("path"),
                "reason": item.get("reason"),
                "confidence": "medium"
            })

        for item in cleanup.get("phase3_manual", []):
            recommendations["review"].append({
                "item": item,
                "reason": "Multiple copies or complex decision",
                "confidence": "low"
            })

        # Working tools must be preserved
        testing = all_results.get("testing", {}).get("test_results", {})
        for tool in testing.get("working", [])[:10]:  # Limit to first 10
            recommendations["preserve"].append({
                "path": tool.get("path"),
                "reason": "Working tool - validated",
                "confidence": "high"
            })

        # Add engineering expert recommendations
        engineering = all_results.get("engineering", {})
        for issue in engineering.get("quality_issues", []):
            recommendations["improve"].append({
                "path": issue.get("path"),
                "issue": issue.get("issue"),
                "priority": issue.get("priority", "medium")
            })

        # Now use LLM to provide executive summary
        if self.manager:
            print("   🤖 Calling LLM for executive analysis...")
            summary_data = {
                "tools_found": all_results.get("exploration", {}).get("tool_count", 0),
                "docs_found": all_results.get("exploration", {}).get("doc_count", 0),
                "working_tools": len(testing.get("working", [])),
                "broken_tools": len(testing.get("broken", [])),
                "security_concerns": len(engineering.get("security_concerns", [])),
                "quality_issues": len(engineering.get("quality_issues", [])),
                "duplicates_for_review": len(cleanup.get("phase3_manual", [])),
                "safe_to_delete": len(cleanup.get("phase1_safe", [])),
            }
            
            prompt = f"""As a Repository Librarian AI, analyze this maintenance scan summary and provide a brief executive analysis (3-5 sentences):

Repository Scan Results:
- Tools discovered: {summary_data['tools_found']}
- Documentation files: {summary_data['docs_found']}
- Working tools: {summary_data['working_tools']}
- Broken tools: {summary_data['broken_tools']}
- Security concerns: {summary_data['security_concerns']}
- Code quality issues: {summary_data['quality_issues']}
- Duplicate files needing review: {summary_data['duplicates_for_review']}
- Files safe to delete: {summary_data['safe_to_delete']}

Provide a concise executive summary focusing on the health of the repository and top priorities."""

            try:
                analysis = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)
                recommendations["llm_analysis"] = analysis
                print(f"   ✅ LLM analysis complete ({len(analysis)} chars)")
            except Exception as e:
                print(f"   ⚠️ LLM call failed: {e}")
                recommendations["llm_analysis"] = f"[LLM analysis unavailable: {e}]"

        return recommendations

    def generate_catalog_report(self) -> str:
        """Generate the librarian's catalog report."""
        report = """
# 📚 Librarian's Catalog Report

## Collection Overview
"""
        if "structure" in self.catalog:
            struct = self.catalog["structure"]
            report += f"""
- **Total Tools:** {struct.get('tool_count', 'N/A')}
- **Documentation Files:** {struct.get('doc_count', 'N/A')}
- **Potential Duplicates:** {struct.get('duplicate_candidates', 'N/A')}
"""

        report += """
## Tasks Completed
"""
        for task in self.completed_tasks:
            report += f"- ✅ {task['specialist']}: {task['task'][:50]}...\n"

        return report


class ExplorerAgent(RepoMaintenanceAgent):
    """Explores and maps repository structure."""

    def __init__(self):
        super().__init__(
            name="Explorer",
            role="Repository Structure Analyst",
            model="gh:openai/gpt-4o-mini"  # Fast scanning
        )

    async def execute(self, repo_path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Map the repository structure."""
        repo_path = Path(repo_path)

        inventory = {
            "directories": [],
            "python_files": [],
            "documentation": [],
            "tools": [],
            "potential_duplicates": [],
        }

        skip_dirs = {'.git', '__pycache__', '.venv', 'node_modules', '.vs', '.vscode', '.pytest_cache', 'archive'}

        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]

            rel_path = Path(root).relative_to(repo_path)

            for f in files:
                rel_file_path = str(rel_path / f) if rel_path != Path('.') else f

                # Skip files with 'archive' in path
                if 'archive' in rel_file_path.lower():
                    continue

                if f.endswith('.py'):
                    inventory["python_files"].append(rel_file_path)
                    if 'tools' in str(rel_path) or f.startswith('run_') or f.startswith('cli'):
                        inventory["tools"].append(rel_file_path)

                if f.lower().endswith('.md') or f.lower() in ['readme.txt', 'readme.rst']:
                    inventory["documentation"].append(rel_file_path)

            if rel_path != Path('.'):
                inventory["directories"].append(str(rel_path))

        # Find potential duplicates
        from collections import defaultdict
        name_paths = defaultdict(list)
        for py_file in inventory["python_files"]:
            name = Path(py_file).name
            name_paths[name].append(py_file)

        for name, paths in name_paths.items():
            if len(paths) > 1:
                inventory["potential_duplicates"].append({
                    "filename": name,
                    "locations": paths
                })

        return {
            "repo_inventory": inventory,
            "tool_count": len(inventory["tools"]),
            "doc_count": len(inventory["documentation"]),
            "duplicate_candidates": len(inventory["potential_duplicates"])
        }


class EngineeringExpertAgent(RepoMaintenanceAgent):
    """
    AI & Software Engineering Expert

    Analyzes code for:
    - Correctness and functionality
    - Best practices adherence
    - Code quality metrics
    - Security considerations
    - Performance patterns
    - Technical debt indicators
    """

    SYSTEM_PROMPT = """You are a Senior AI & Software Engineering Expert.

Your role is to analyze code repositories for:
1. CORRECTNESS: Does the code work as intended?
2. BEST PRACTICES: Does it follow Python/industry standards?
3. QUALITY: Code readability, maintainability, documentation
4. SECURITY: Common vulnerabilities and unsafe patterns
5. PERFORMANCE: Efficiency issues and optimization opportunities
6. TECHNICAL DEBT: Areas needing refactoring or modernization

You provide actionable, specific feedback with priority ratings."""

    def __init__(self):
        super().__init__(
            name="EngineeringExpert",
            role="AI & Software Engineering Expert",
            model="ollama:deepseek-r1:14b"  # Local reasoning model for code analysis
        )

    async def execute(self, tools: List[str], repo_path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze tools for code quality and best practices using LLM."""
        repo_path = Path(repo_path)

        analysis = {
            "analyzed": [],
            "quality_issues": [],
            "best_practices_violations": [],
            "security_concerns": [],
            "technical_debt": [],
            "recommendations": [],
        }

        # Sample files for LLM analysis (limit to avoid token overload)
        sample_files = []
        for tool_path in tools[:10]:  # Analyze up to 10 files with LLM
            file_path = repo_path / tool_path
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()[:3000]  # First 3000 chars
                    sample_files.append({"path": tool_path, "content": content})
                except Exception:
                    pass

        # Call LLM for analysis
        if self.manager and sample_files:
            print("   🤖 Engineering Expert calling LLM for code analysis...")
            
            file_summaries = "\n\n".join([
                f"### {f['path']}\n```python\n{f['content'][:1500]}\n```"
                for f in sample_files[:5]  # Show 5 files to LLM
            ])
            
            prompt = f"""Analyze these Python files for code quality issues.

{file_summaries}

For each file, identify:
1. SECURITY issues (hardcoded secrets, SQL injection, etc.)
2. QUALITY issues (no docstrings, large files, poor structure)
3. BEST PRACTICES violations (no type hints, broad exceptions)

Respond in this exact format:
SECURITY:
- [filepath]: [issue description]

QUALITY:
- [filepath]: [issue description]

BEST_PRACTICES:
- [filepath]: [issue description]

Be specific about actual issues found. If no issues, say "None found"."""

            try:
                llm_response = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)
                print(f"   ✅ LLM analysis complete ({len(llm_response)} chars)")
                
                # Parse LLM response into structured issues
                current_category = None
                for line in llm_response.split('\n'):
                    line = line.strip()
                    if line.startswith('SECURITY:'):
                        current_category = 'security'
                    elif line.startswith('QUALITY:'):
                        current_category = 'quality'
                    elif line.startswith('BEST_PRACTICES:'):
                        current_category = 'best_practices'
                    elif line.startswith('- ') and current_category:
                        issue_text = line[2:]
                        if ':' in issue_text:
                            path, issue = issue_text.split(':', 1)
                            path = path.strip()
                            issue = issue.strip()
                        else:
                            path = "general"
                            issue = issue_text
                        
                        if 'none found' not in issue.lower():
                            issue_obj = {
                                "path": path,
                                "issue": issue,
                                "category": current_category,
                                "priority": "high" if current_category == "security" else "medium"
                            }
                            if current_category == 'security':
                                analysis["security_concerns"].append(issue_obj)
                            elif current_category == 'quality':
                                analysis["quality_issues"].append(issue_obj)
                            elif current_category == 'best_practices':
                                analysis["best_practices_violations"].append(issue_obj)
                
            except Exception as e:
                print(f"   ⚠️ LLM analysis failed: {e}")
                # Fall back to heuristic analysis
                for f in sample_files:
                    file_analysis = self._analyze_file(f["path"], f["content"])
                    analysis["analyzed"].append(file_analysis)
        else:
            # Fallback: heuristic analysis for remaining files
            for tool_path in tools[:30]:
                file_path = repo_path / tool_path
                if file_path.exists():
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        file_analysis = self._analyze_file(tool_path, content)
                        analysis["analyzed"].append(file_analysis)
                        for issue in file_analysis.get("issues", []):
                            issue["path"] = tool_path
                            if issue["category"] == "quality":
                                analysis["quality_issues"].append(issue)
                            elif issue["category"] == "security":
                                analysis["security_concerns"].append(issue)
                    except Exception:
                        pass

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)

        return {
            "engineering_analysis": analysis,
            "total_analyzed": len(sample_files) if sample_files else len(analysis["analyzed"]),
            "quality_issues_count": len(analysis["quality_issues"]),
            "security_concerns_count": len(analysis["security_concerns"]),
            "best_practices_violations_count": len(analysis["best_practices_violations"])
        }

    def _analyze_file(self, path: str, content: str) -> Dict[str, Any]:
        """Analyze a single file for quality issues."""
        issues = []
        lines = content.split('\n')

        # Check for docstrings
        if not ('"""' in content or "'''" in content):
            issues.append({
                "category": "quality",
                "issue": "Missing docstrings",
                "priority": "medium",
                "suggestion": "Add module and function docstrings"
            })

        # Check for type hints
        func_pattern = r'def \w+\([^)]*\):'
        funcs_without_hints = re.findall(func_pattern, content)
        if funcs_without_hints and '->' not in content:
            issues.append({
                "category": "best_practices",
                "issue": "Missing type hints",
                "priority": "low",
                "suggestion": "Add return type annotations to functions"
            })

        # Check for bare excepts
        if 'except:' in content or 'except Exception:' in content:
            issues.append({
                "category": "best_practices",
                "issue": "Broad exception handling",
                "priority": "medium",
                "suggestion": "Use specific exception types"
            })

        # Check for hardcoded credentials patterns
        cred_patterns = ['password=', 'api_key=', 'secret=', 'token=']
        for pattern in cred_patterns:
            if pattern in content.lower() and '=' in content:
                # Check if it's not just a parameter name
                for line in lines:
                    if pattern in line.lower() and ('=' in line) and ('"' in line or "'" in line):
                        issues.append({
                            "category": "security",
                            "issue": f"Potential hardcoded credential: {pattern}",
                            "priority": "high",
                            "suggestion": "Use environment variables for secrets"
                        })
                        break

        # Check for TODO/FIXME comments (technical debt)
        todo_count = content.lower().count('todo') + content.lower().count('fixme')
        if todo_count > 0:
            issues.append({
                "category": "technical_debt",
                "issue": f"Found {todo_count} TODO/FIXME comments",
                "priority": "low",
                "suggestion": "Address or track these items"
            })

        # Check file length (complexity indicator)
        if len(lines) > 500:
            issues.append({
                "category": "quality",
                "issue": f"Large file ({len(lines)} lines)",
                "priority": "medium",
                "suggestion": "Consider splitting into smaller modules"
            })

        # Check for main guard
        if 'if __name__' not in content and 'def main' in content:
            issues.append({
                "category": "best_practices",
                "issue": "Missing __name__ guard",
                "priority": "low",
                "suggestion": "Add if __name__ == '__main__': guard"
            })

        return {
            "path": path,
            "lines": len(lines),
            "issues": issues,
            "quality_score": max(0, 100 - len(issues) * 10)
        }

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate prioritized recommendations."""
        recommendations = []

        # High priority: Security
        if analysis["security_concerns"]:
            recommendations.append({
                "priority": "HIGH",
                "category": "Security",
                "action": "Address security concerns immediately",
                "files": [c["path"] for c in analysis["security_concerns"][:5]]
            })

        # Medium priority: Quality
        if len(analysis["quality_issues"]) > 5:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Code Quality",
                "action": "Improve documentation and reduce file sizes",
                "files": list(set(i["path"] for i in analysis["quality_issues"]))[:5]
            })

        # Low priority: Best practices
        if analysis["best_practices_violations"]:
            recommendations.append({
                "priority": "LOW",
                "category": "Best Practices",
                "action": "Add type hints and improve exception handling",
                "files": list(set(i["path"] for i in analysis["best_practices_violations"]))[:5]
            })

        return recommendations


class ToolTesterAgent(RepoMaintenanceAgent):
    """Tests repository tools."""

    def __init__(self):
        super().__init__(
            name="Tester",
            role="Tool Testing Specialist",
            model="gh:openai/gpt-4o-mini"  # Fast testing
        )

    async def execute(self, tools: List[str], repo_path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Test tools for import errors and basic functionality."""
        results = {
            "tested": [],
            "working": [],
            "broken": [],
            "skipped": []
        }

        repo_path = Path(repo_path)

        for tool_path in tools[:50]:
            tool_file = repo_path / tool_path
            tool_name = Path(tool_path).stem

            result = {
                "path": tool_path,
                "name": tool_name,
                "status": "unknown",
                "details": ""
            }

            try:
                if not tool_file.exists():
                    result["status"] = "missing"
                    result["details"] = "File not found"
                    results["broken"].append(result)
                    continue

                with open(tool_file, 'r', encoding='utf-8', errors='ignore') as f:
                    source = f.read()

                try:
                    compile(source, tool_path, 'exec')
                    result["status"] = "syntax_ok"
                    result["details"] = "Syntax valid"
                    results["working"].append(result)
                except SyntaxError as e:
                    result["status"] = "syntax_error"
                    result["details"] = str(e)
                    results["broken"].append(result)

            except Exception as e:
                result["status"] = "error"
                result["details"] = str(e)
                results["broken"].append(result)

            results["tested"].append(result)

        return {
            "test_results": results,
            "total_tested": len(results["tested"]),
            "working_count": len(results["working"]),
            "broken_count": len(results["broken"])
        }


class ResearcherAgent(RepoMaintenanceAgent):
    """
    Researcher Agent - Uses web search to find information.

    Can search for:
    - Best practices for code patterns
    - Documentation for libraries
    - Security vulnerability information
    - Alternative implementations
    """

    SYSTEM_PROMPT = """You are a Research Specialist with web search capabilities.

You can search the web to find:
1. Best practices and coding standards
2. Library documentation and examples
3. Security vulnerability databases
4. Community recommendations

Use the web_search tool to gather information.
Synthesize findings into actionable recommendations."""

    def __init__(self):
        super().__init__(
            name="Researcher",
            role="Web Research Specialist",
            model="gh:openai/gpt-4o-mini"
        )
        self.toolkit: Optional[AgentToolkit] = None

    def set_toolkit(self, toolkit: AgentToolkit):
        """Attach toolkit for tool access."""
        self.toolkit = toolkit

    async def execute(
        self,
        query: str,
        repo_path: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Search the web for information."""
        if not self.toolkit:
            self.toolkit = AgentToolkit(Path(repo_path), dry_run=True)

        results = {
            "query": query,
            "search_results": [],
            "synthesis": None,
            "recommendations": []
        }

        print(f"   🔍 Researcher: Searching for '{query[:50]}...'")

        # Perform web search
        search_result = self.toolkit.web_search(query, max_results=5)
        if search_result.success:
            results["search_results"] = search_result.output
            print(f"   ✅ Found {len(search_result.output)} results")

            # Use LLM to synthesize findings
            if self.manager and search_result.output:
                search_text = "\n".join([
                    f"- {r.get('title', 'N/A')}: {r.get('snippet', 'N/A')[:200]}"
                    for r in search_result.output
                ])

                prompt = f"""Based on these search results for \"{query}\":

{search_text}

Provide a brief synthesis (2-3 sentences) and any actionable recommendations."""

                try:
                    synthesis = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)
                    results["synthesis"] = synthesis
                    print(f"   ✅ Synthesis complete")
                except Exception as e:
                    print(f"   ⚠️ Synthesis failed: {e}")
        else:
            print(f"   ⚠️ Search failed: {search_result.error}")
            results["error"] = search_result.error

        return results


class DocumentationAgent(RepoMaintenanceAgent):
    """Audits and updates documentation."""

    SYSTEM_PROMPT = """You are a Documentation Specialist.
Analyze documentation for completeness, clarity, and accuracy.
Identify missing sections, outdated content, and broken references."""

    def __init__(self):
        super().__init__(
            name="Documenter",
            role="Documentation Specialist",
            model="gh:openai/gpt-4o-mini"
        )

    async def execute(self, docs: List[str], repo_path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Audit documentation files using LLM."""
        repo_path = Path(repo_path)

        audit_results = {
            "audited": [],
            "issues": [],
            "broken_links": [],
            "missing_sections": [],
            "llm_summary": None
        }

        # First pass: quick heuristic scan for broken links
        doc_samples = []
        for doc_path in docs[:20]:
            doc_file = repo_path / doc_path
            if not doc_file.exists():
                continue

            try:
                with open(doc_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                audit = {"path": doc_path, "size": len(content), "issues": []}

                # Check for broken internal links (quick)
                links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
                for text, url in links:
                    if url.startswith('/') or url.startswith('./'):
                        target = repo_path / url.lstrip('/')
                        if not target.exists():
                            audit_results["broken_links"].append({
                                "file": doc_path, "link": url, "text": text
                            })

                audit_results["audited"].append(audit)
                
                # Collect samples for LLM
                if len(content) > 200 and len(doc_samples) < 5:
                    doc_samples.append({
                        "path": doc_path,
                        "content": content[:2000]
                    })

            except Exception as e:
                audit_results["issues"].append({"path": doc_path, "error": str(e)})

        # Call LLM for deeper analysis
        if self.manager and doc_samples:
            print("   🤖 Documenter calling LLM for doc analysis...")
            
            doc_summaries = "\n\n".join([
                f"### {d['path']}\n{d['content'][:1000]}"
                for d in doc_samples[:3]
            ])
            
            prompt = f"""Analyze these documentation files for quality:

{doc_summaries}

Identify:
1. Missing required sections (Installation, Usage, Examples, API Reference)
2. Outdated or stale content indicators  
3. Documentation gaps
4. Overall quality assessment

Be brief and specific."""

            try:
                llm_response = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)
                audit_results["llm_summary"] = llm_response
                print(f"   ✅ Doc analysis complete ({len(llm_response)} chars)")
            except Exception as e:
                print(f"   ⚠️ LLM doc analysis failed: {e}")

        return {
            "audit_results": audit_results,
            "total_audited": len(audit_results["audited"]),
            "issues_found": len(audit_results["issues"]),
            "broken_links_count": len(audit_results["broken_links"])
        }


class CleanupAgent(RepoMaintenanceAgent):
    """Identifies duplicates and files for cleanup."""

    SYSTEM_PROMPT = """You are a Repository Cleanup Specialist.
Analyze duplicate files and decide which should be kept, archived, or deleted.
Consider file locations, naming, and context when making recommendations."""

    def __init__(self):
        super().__init__(
            name="Cleanup",
            role="Duplicate Detection Specialist",
            model="gh:openai/gpt-4o-mini"
        )

    async def execute(self, inventory: Dict[str, Any], repo_path: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Identify files for cleanup using LLM."""
        repo_path = Path(repo_path)

        cleanup_plan = {
            "phase1_safe": [],
            "phase2_medium": [],
            "phase3_manual": [],
            "llm_recommendations": None
        }

        # Quick heuristic scan for empty/stub files
        for py_file in inventory.get("python_files", [])[:100]:
            file_path = repo_path / py_file
            if file_path.exists():
                try:
                    size = file_path.stat().st_size
                    if size == 0:
                        cleanup_plan["phase1_safe"].append({
                            "path": py_file, "reason": "Empty file", "action": "DELETE"
                        })
                except Exception:
                    pass

        # Mark duplicates for review
        for dup in inventory.get("potential_duplicates", [])[:30]:
            cleanup_plan["phase3_manual"].append({
                "filename": dup["filename"],
                "locations": dup["locations"],
                "reason": "Same filename in multiple locations",
                "action": "REVIEW"
            })

        # Check archive duplicates
        archive_files = [f for f in inventory.get("python_files", []) if 'archive' in f.lower()]
        for archive_file in archive_files[:20]:
            filename = Path(archive_file).name
            active = [f for f in inventory.get("python_files", [])
                      if Path(f).name == filename and 'archive' not in f.lower()]
            if active:
                cleanup_plan["phase2_medium"].append({
                    "path": archive_file,
                    "reason": f"Archived copy with active version: {active[0]}",
                    "action": "VERIFY_AND_DELETE"
                })

        # Call LLM for duplicate analysis
        if self.manager and cleanup_plan["phase3_manual"]:
            print("   🤖 Cleanup agent calling LLM for duplicate analysis...")
            
            dup_summary = "\n".join([
                f"- {d['filename']}: found in {len(d['locations'])} locations"
                for d in cleanup_plan["phase3_manual"][:10]
            ])
            
            prompt = f"""Analyze these duplicate files and recommend actions:

{dup_summary}

For each, recommend: KEEP (which location), ARCHIVE, or DELETE.
Consider: is one in 'archive/' already? Is one in 'testing/'?

Be brief."""

            try:
                llm_response = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)
                cleanup_plan["llm_recommendations"] = llm_response
                print(f"   ✅ Cleanup analysis complete ({len(llm_response)} chars)")
            except Exception as e:
                print(f"   ⚠️ LLM cleanup analysis failed: {e}")

        return {
            "cleanup_plan": cleanup_plan,
            "safe_deletions": len(cleanup_plan["phase1_safe"]),
            "medium_risk": len(cleanup_plan["phase2_medium"]),
            "manual_review": len(cleanup_plan["phase3_manual"])
        }


class DeveloperAgent(RepoMaintenanceAgent):
    """
    Developer Engineer Agent - Implements approved changes.

    Uses tools to:
    - Move files to archive
    - Delete files
    - Create/update documentation
    - Refactor code based on recommendations
    """

    SYSTEM_PROMPT = """You are a Senior Developer Engineer.
You implement maintenance changes approved by the Librarian/LATS controller.

You have access to tools:
- read_file(path): Read file contents
- write_file(path, content): Write to file
- move_file(src, dest): Move file (use for archiving)
- delete_file(path): Delete file (moved to .trash)
- list_dir(path): List directory

For each task, plan your approach, then execute using tools.
Always verify changes before and after.
Respond with ACTION: tool_name and PARAMS: {...} to use tools."""

    def __init__(self):
        super().__init__(
            name="Developer",
            role="Developer Engineer",
            model="gh:openai/gpt-4o-mini"
        )
        self.toolkit: Optional[AgentToolkit] = None

    def set_toolkit(self, toolkit: AgentToolkit):
        """Attach toolkit for tool access."""
        self.toolkit = toolkit

    async def execute(
        self,
        approved_actions: List[Dict[str, Any]],
        repo_path: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute approved maintenance actions."""
        if not self.toolkit:
            self.toolkit = AgentToolkit(Path(repo_path), dry_run=True)

        results = {
            "executed": [],
            "skipped": [],
            "errors": [],
            "tool_calls": []
        }

        for action in approved_actions[:20]:  # Limit for safety
            action_type = action.get("action", "").upper()
            path = action.get("path", "")

            print(f"   🔧 Developer: {action_type} on {path}")

            try:
                if action_type == "ARCHIVE":
                    dest = f"archive/{Path(path).name}"
                    result = self.toolkit.move_file(path, dest)
                    results["tool_calls"].append(result.to_dict())
                    if result.success:
                        results["executed"].append({
                            "action": action_type, "path": path, "result": result.output
                        })
                    else:
                        results["errors"].append({
                            "action": action_type, "path": path, "error": result.error
                        })

                elif action_type == "DELETE":
                    result = self.toolkit.delete_file(path)
                    results["tool_calls"].append(result.to_dict())
                    if result.success:
                        results["executed"].append({
                            "action": action_type, "path": path, "result": result.output
                        })
                    else:
                        results["errors"].append({
                            "action": action_type, "path": path, "error": result.error
                        })

                elif action_type in ["REVIEW", "PRESERVE", "SKIP"]:
                    results["skipped"].append({
                        "action": action_type, "path": path, "reason": "No automated action"
                    })

                else:
                    results["skipped"].append({
                        "action": action_type, "path": path, "reason": f"Unknown action: {action_type}"
                    })

            except Exception as e:
                results["errors"].append({
                    "action": action_type, "path": path, "error": str(e)
                })

        return {
            "developer_results": results,
            "total_executed": len(results["executed"]),
            "total_skipped": len(results["skipped"]),
            "total_errors": len(results["errors"])
        }


class LATSQualityController(RepoMaintenanceAgent):
    """
    LATS (Language Agent Tree Search) Quality Controller.

    Takes ALL agent outputs as input and:
    1. Synthesizes findings across all agents
    2. Identifies conflicts and inconsistencies
    3. Iteratively verifies recommendations (up to max_iterations)
    4. Produces a final verified action plan

    Uses LATS pattern: Generate -> Evaluate -> Refine -> Verify
    """

    SYSTEM_PROMPT = """You are a LATS Quality Controller - the final verification step.

You receive the combined outputs from multiple specialist agents:
- Explorer: Repository inventory
- Tester: Tool test results
- Engineering: Code quality/security analysis
- Documenter: Documentation audit
- Cleanup: Duplicate/cleanup recommendations

Your job is to:
1. SYNTHESIZE: Combine insights from all agents
2. VERIFY: Check for conflicts or inconsistencies
3. PRIORITIZE: Rank recommendations by impact and risk
4. DECIDE: Produce a final action plan with confidence scores

Output Format:
```json
{
  "verified_actions": [
    {"path": "...", "action": "ARCHIVE|DELETE|PRESERVE|REVIEW", "priority": "HIGH|MEDIUM|LOW", "confidence": 0.95, "reason": "..."}
  ],
  "conflicts_resolved": [...],
  "items_needing_human_review": [...],
  "overall_confidence": 0.85
}
```

Be conservative - when uncertain, recommend REVIEW instead of DELETE."""

    def __init__(self):
        super().__init__(
            name="LATSController",
            role="LATS Quality Controller",
            model="ollama:qwen2.5-coder:14b"  # Local coder model for synthesis
        )
        self.max_iterations = 2  # LATS refinement iterations
        self.aggressive = False  # If True, be more willing to DELETE

    async def execute(
        self,
        all_agent_results: Dict[str, Any],
        repo_path: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Run LATS verification on all agent outputs."""
        print("   🔍 LATS Controller: Synthesizing all agent outputs...")

        # Build comprehensive context from all agents
        agent_summary = self._build_agent_summary(all_agent_results)

        verified_plan = {
            "verified_actions": [],
            "conflicts": [],
            "human_review": [],
            "iterations": 0,
            "overall_confidence": 0.0
        }

        # LATS Loop: Generate -> Evaluate -> Refine
        for iteration in range(self.max_iterations):
            print(f"   🔄 LATS Iteration {iteration + 1}/{self.max_iterations}...")

            aggressive_instruction = """
IMPORTANT: AGGRESSIVE MODE IS ENABLED.
- Prefer DELETE over REVIEW for empty files, duplicates, and obsolete code
- Prefer ARCHIVE over REVIEW for deprecated but potentially useful files
- Only use REVIEW for genuinely ambiguous cases
""" if self.aggressive else ""

            prompt = f"""## Agent Reports Summary

{agent_summary}
{aggressive_instruction}
## Your Task (Iteration {iteration + 1})

Analyze the above reports and produce a verified action plan.

{"This is your first pass. Focus on identifying all actionable items." if iteration == 0 else "This is a refinement pass. Review your previous analysis and improve confidence scores."}

For each file that needs action, specify:
- path: the file path
- action: ARCHIVE, DELETE, PRESERVE, or REVIEW
- priority: HIGH, MEDIUM, or LOW
- confidence: 0.0-1.0
- reason: brief explanation

Respond with a JSON object containing verified_actions, conflicts_resolved, and overall_confidence."""

            try:
                llm_response = await self.call_llm(prompt, system_prompt=self.SYSTEM_PROMPT)

                # Parse response
                parsed = self._parse_lats_response(llm_response)
                verified_plan["verified_actions"] = parsed.get("verified_actions", [])
                verified_plan["conflicts"] = parsed.get("conflicts_resolved", [])
                verified_plan["overall_confidence"] = parsed.get("overall_confidence", 0.7)
                verified_plan["iterations"] = iteration + 1
                verified_plan["raw_response"] = llm_response

                # If confidence is high enough, stop early
                if verified_plan["overall_confidence"] >= 0.85:
                    print(f"   ✅ High confidence ({verified_plan['overall_confidence']:.0%}), stopping early")
                    break

            except Exception as e:
                print(f"   ⚠️ LATS iteration {iteration + 1} failed: {e}")

        print(f"   ✅ LATS complete: {len(verified_plan['verified_actions'])} verified actions")

        return {
            "lats_results": verified_plan,
            "verified_count": len(verified_plan["verified_actions"]),
            "confidence": verified_plan["overall_confidence"],
            "iterations": verified_plan["iterations"]
        }

    def _build_agent_summary(self, results: Dict[str, Any]) -> str:
        """Build a summary of all agent outputs for LLM context."""
        sections = []

        # Explorer results
        if "exploration" in results:
            exp = results["exploration"]
            inv = exp.get("repo_inventory", {})
            sections.append(f"""### Explorer Agent
- Python files: {len(inv.get('python_files', []))}
- Documentation: {len(inv.get('documentation', []))}
- Potential duplicates: {len(inv.get('potential_duplicates', []))}""")

        # Engineering results
        if "engineering" in results:
            eng = results["engineering"]
            sections.append(f"""### Engineering Expert
- Security concerns: {eng.get('security_count', 0)}
- Quality issues: {eng.get('quality_count', 0)}
- LLM Analysis: {eng.get('llm_analysis', 'N/A')[:500]}...""")

        # Documentation results
        if "documentation" in results:
            doc = results["documentation"]
            sections.append(f"""### Documentation Agent
- Audited: {doc.get('total_audited', 0)}
- Broken links: {doc.get('broken_links_count', 0)}""")

        # Cleanup results
        if "cleanup" in results:
            clean = results["cleanup"]
            sections.append(f"""### Cleanup Agent
- Safe deletions (phase 1): {clean.get('safe_deletions', 0)}
- Medium risk (phase 2): {clean.get('medium_risk', 0)}
- Manual review (phase 3): {clean.get('manual_review', 0)}""")

        # Test results
        if "testing" in results:
            test = results["testing"]
            sections.append(f"""### Tester Agent
- Working tools: {test.get('working_count', 0)}
- Broken tools: {test.get('broken_count', 0)}""")

        return "\n\n".join(sections)

    def _parse_lats_response(self, response: str) -> Dict[str, Any]:
        """Parse LATS JSON response."""
        # Try to extract JSON from response
        try:
            # Look for JSON block
            if "```json" in response:
                start = response.find("```json") + 7
                end = response.find("```", start)
                json_str = response[start:end].strip()
            elif "{" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
            else:
                return {"verified_actions": [], "overall_confidence": 0.5}

            return json.loads(json_str)
        except json.JSONDecodeError:
            return {"verified_actions": [], "overall_confidence": 0.5}


class RepoMaintenanceWorkflow:
    """Orchestrates the multi-agent repository maintenance workflow."""

    def __init__(self, repo_path: str, dry_run: bool = True, aggressive: bool = False):
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.aggressive = aggressive  # If True, LATS will output DELETE actions more readily
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Initialize toolkit for tool access
        self.toolkit = AgentToolkit(self.repo_path, dry_run=dry_run)

        # Initialize the Librarian as orchestrator
        self.librarian = LibrarianAgent()

        # Register specialist agents
        self.librarian.register_specialist("explorer", ExplorerAgent())
        self.librarian.register_specialist("tester", ToolTesterAgent())
        self.librarian.register_specialist("documenter", DocumentationAgent())
        self.librarian.register_specialist("cleanup", CleanupAgent())
        self.librarian.register_specialist("engineering", EngineeringExpertAgent())
        
        # Researcher Agent with web search
        researcher = ResearcherAgent()
        researcher.set_toolkit(self.toolkit)
        self.librarian.register_specialist("researcher", researcher)

        # LATS Quality Controller (verifies all outputs)
        self.lats_controller = LATSQualityController()
        self.lats_controller.aggressive = aggressive  # Pass aggressive flag

        # Developer Agent (implements changes)
        self.developer = DeveloperAgent()
        self.developer.set_toolkit(self.toolkit)

    async def run(self) -> Dict[str, Any]:
        """Execute the full maintenance workflow."""
        print(f"\n{'='*60}")
        print("📚 Repository Maintenance Workflow")
        print("   Orchestrated by: The Librarian → LATS → Developer")
        print(f"{'='*60}")
        print(f"Target: {self.repo_path}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"{'='*60}\n")

        # ================================================================
        # PHASE 1: ANALYSIS (Specialist Agents)
        # ================================================================

        # Step 1: Librarian analyzes the collection
        print("📁 Step 1: Librarian analyzing collection...")
        self.results["exploration"] = await self.librarian.analyze_collection(
            str(self.repo_path)
        )
        print(f"   Found {self.results['exploration']['tool_count']} tools, "
              f"{self.results['exploration']['doc_count']} docs")

        # Step 2: Delegate tool testing
        print("\n🧪 Step 2: Delegating tool testing...")
        tools = self.results["exploration"]["repo_inventory"]["tools"]
        self.results["testing"] = await self.librarian.delegate_task(
            "tester", "Test all repository tools", tools, str(self.repo_path)
        )
        print(f"   {self.results['testing']['working_count']} working, "
              f"{self.results['testing']['broken_count']} broken")

        # Step 3: Engineering expert analysis
        print("\n🔬 Step 3: Engineering Expert analyzing code quality...")
        self.results["engineering"] = await self.librarian.delegate_task(
            "engineering", "Analyze code quality and best practices",
            tools, str(self.repo_path)
        )
        print(f"   {self.results['engineering']['quality_issues_count']} quality, "
              f"{self.results['engineering']['security_concerns_count']} security")

        # Step 4: Audit documentation
        print("\n📝 Step 4: Delegating documentation audit...")
        docs = self.results["exploration"]["repo_inventory"]["documentation"]
        self.results["documentation"] = await self.librarian.delegate_task(
            "documenter", "Audit all documentation", docs, str(self.repo_path)
        )
        print(f"   {self.results['documentation']['issues_found']} issues, "
              f"{self.results['documentation']['broken_links_count']} broken links")

        # Step 5: Plan cleanup
        print("\n🧹 Step 5: Delegating cleanup planning...")
        self.results["cleanup"] = await self.librarian.delegate_task(
            "cleanup", "Identify duplicates and cleanup candidates",
            self.results["exploration"]["repo_inventory"], str(self.repo_path)
        )
        print(f"   Phase 1: {self.results['cleanup']['safe_deletions']} safe, "
              f"Phase 2: {self.results['cleanup']['medium_risk']} medium, "
              f"Phase 3: {self.results['cleanup']['manual_review']} manual")

        # ================================================================
        # PHASE 2: VERIFICATION (LATS Quality Controller)
        # ================================================================

        print("\n🔍 Step 6: LATS Quality Controller verifying all outputs...")
        self.results["lats_verification"] = await self.lats_controller.execute(
            all_agent_results=self.results,
            repo_path=str(self.repo_path)
        )
        print(f"   Verified {self.results['lats_verification']['verified_count']} actions "
              f"with {self.results['lats_verification']['confidence']:.0%} confidence")

        # ================================================================
        # PHASE 3: IMPLEMENTATION (Developer Agent)
        # ================================================================

        # Only run developer if we have verified actions
        verified_actions = self.results["lats_verification"].get(
            "lats_results", {}
        ).get("verified_actions", [])

        if verified_actions:
            print(f"\n🔧 Step 7: Developer implementing {len(verified_actions)} verified actions...")
            self.results["developer_execution"] = await self.developer.execute(
                approved_actions=verified_actions,
                repo_path=str(self.repo_path)
            )
            print(f"   Executed: {self.results['developer_execution']['total_executed']}, "
                  f"Skipped: {self.results['developer_execution']['total_skipped']}, "
                  f"Errors: {self.results['developer_execution']['total_errors']}")
        else:
            print("\n🔧 Step 7: No verified actions to implement")
            self.results["developer_execution"] = {"total_executed": 0}

        # Step 8: Librarian curates final recommendations
        print("\n📚 Step 8: Librarian curating final recommendations...")
        self.results["recommendations"] = await self.librarian.curate_recommendations(
            self.results
        )

        # Generate report
        print("\n📊 Step 9: Generating comprehensive report...")
        report = self._generate_report()

        report_path = self.repo_path / f"maintenance_report_{self.timestamp}.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"   Report saved to: {report_path}")

        json_path = self.repo_path / f"maintenance_results_{self.timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"   JSON results saved to: {json_path}")

        # Save tool action log
        if self.toolkit.actions_log:
            log_path = self.repo_path / f"tool_actions_{self.timestamp}.json"
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(self.toolkit.actions_log, f, indent=2)
            print(f"   Tool action log saved to: {log_path}")

        print(f"\n{'='*60}")
        print("✅ Maintenance workflow complete!")
        print(f"{'='*60}\n")

        return self.results

    def _generate_report(self) -> str:
        """Generate a markdown maintenance report."""
        report = f"""# 📚 Repository Maintenance Report

**Repository:** `{self.repo_path}`
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Mode:** {'DRY RUN (no changes made)' if self.dry_run else 'LIVE'}
**Orchestrated by:** The Librarian Agent

---

## Executive Summary

| Metric | Count |
|--------|-------|
| Tools Discovered | {self.results['exploration']['tool_count']} |
| Documentation Files | {self.results['exploration']['doc_count']} |
| Tools Tested | {self.results['testing']['total_tested']} |
| Working Tools | {self.results['testing']['working_count']} |
| Broken Tools | {self.results['testing']['broken_count']} |
| Code Quality Issues | {self.results['engineering']['quality_issues_count']} |
| Security Concerns | {self.results['engineering']['security_concerns_count']} |
| Documentation Issues | {self.results['documentation']['issues_found']} |
| Safe Deletions | {self.results['cleanup']['safe_deletions']} |

---

## 🔬 Engineering Expert Analysis

### Security Concerns (Priority: HIGH)
"""
        for concern in self.results['engineering']['engineering_analysis'].get('security_concerns', [])[:10]:
            report += f"- `{concern.get('path')}`: {concern.get('issue')}\n"

        report += """
### Code Quality Issues
"""
        for issue in self.results['engineering']['engineering_analysis'].get('quality_issues', [])[:10]:
            report += f"- `{issue.get('path')}`: {issue.get('issue')} ({issue.get('priority')})\n"

        report += """
### Engineering Recommendations
"""
        for rec in self.results['engineering']['engineering_analysis'].get('recommendations', []):
            report += f"- **{rec['priority']}** [{rec['category']}]: {rec['action']}\n"

        report += """
---

## 📚 Librarian's Curated Recommendations

### ✅ Preserve (Working, Validated)
"""
        for item in self.results['recommendations'].get('preserve', [])[:10]:
            report += f"- `{item.get('path')}` - {item.get('reason')}\n"

        report += """
### 📦 Archive (Move to archive/)
"""
        for item in self.results['recommendations'].get('archive', [])[:10]:
            report += f"- `{item.get('path')}` - {item.get('reason')}\n"

        report += """
### 🗑️ Discard (Safe to Delete)
"""
        for item in self.results['recommendations'].get('discard', [])[:10]:
            report += f"- `{item.get('path')}` - {item.get('reason')}\n"

        report += """
### 👀 Human Review Required
"""
        for item in self.results['recommendations'].get('review', [])[:10]:
            if isinstance(item.get('item'), dict) and 'locations' in item['item']:
                report += f"- **{item['item'].get('filename')}** in {len(item['item']['locations'])} locations\n"
            else:
                report += f"- {item}\n"

        report += f"""
---

{self.librarian.generate_catalog_report()}

---

*Generated by Repository Maintenance Workflow with Librarian Orchestration*
"""
        return report


async def main():
    parser = argparse.ArgumentParser(description="Run repository maintenance workflow")
    parser.add_argument("--repo-path", type=str, default=".", help="Path to repository")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Report only")
    parser.add_argument("--live", action="store_true", help="Execute cleanup (caution)")
    parser.add_argument("--aggressive", action="store_true", help="Aggressive mode: DELETE instead of REVIEW")

    args = parser.parse_args()

    workflow = RepoMaintenanceWorkflow(
        repo_path=args.repo_path,
        dry_run=not args.live,
        aggressive=args.aggressive
    )

    await workflow.run()


if __name__ == "__main__":
    asyncio.run(main())
