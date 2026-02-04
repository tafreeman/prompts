#!/usr/bin/env python3
"""
Test Tasks for Multi-Agent Orchestrator
========================================

A curated collection of software engineering tasks for testing multi-agent
workflows. These tasks are designed to exercise different agent capabilities:
- Analyst: requirements analysis, pattern recognition
- Researcher: best practices, technology choices
- Strategist: architecture, design decisions
- Implementer: code generation, specifications

Gold standards are stored externally and fetched on demand from:
- GitHub repositories (reference implementations)
- SWE-bench dataset (standard benchmarks)
- Local cache (for offline/fast access)

Usage:
    # Run a single task
    python -m tools.agents.test_tasks --task 1

    # Run all tasks
    python -m tools.agents.test_tasks --all

    # List available tasks
    python -m tools.agents.test_tasks --list

    # Run with specific model
    python -m tools.agents.test_tasks --task 1 --model local:phi4

    # Fetch gold standards from source
    python -m tools.agents.test_tasks --fetch-gold 1

Author: Prompts Library Team
Version: 1.1
"""

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent directory to path for imports
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.agents.multi_agent_orchestrator import MultiAgentOrchestrator

# =============================================================================
# GOLD STANDARD REFERENCE SYSTEM
# =============================================================================


@dataclass
class GoldStandardRef:
    """Reference to a gold standard stored externally."""

    source_type: str  # "github", "swe-bench", "local", "url"
    source_url: str  # URL or path to fetch from
    commit_hash: Optional[str] = None  # Git commit for reproducibility
    file_path: Optional[str] = None  # Path within repo/archive
    benchmark_id: Optional[str] = None  # ID in standard benchmark (e.g., SWE-bench)
    version: str = "1.0"  # Version of the gold standard
    last_verified: Optional[str] = None  # ISO date when last verified
    checksum: Optional[str] = None  # SHA256 of expected content


# Cache directory for gold standards
GOLD_STANDARD_CACHE_DIR = Path(__file__).parent / ".gold_standard_cache"


def get_cache_path(ref: GoldStandardRef) -> Path:
    """Get local cache path for a gold standard reference."""
    # Create unique cache key from source
    key = f"{ref.source_type}:{ref.source_url}:{ref.commit_hash or 'latest'}"
    cache_key = hashlib.sha256(key.encode()).hexdigest()[:16]
    return GOLD_STANDARD_CACHE_DIR / f"{cache_key}.json"


def fetch_gold_standard(
    ref: GoldStandardRef, force_refresh: bool = False
) -> Optional[Dict[str, Any]]:
    """Fetch gold standard from source or cache.

    Args:
        ref: Reference to the gold standard
        force_refresh: If True, bypass cache and fetch from source

    Returns:
        Gold standard dict or None if fetch fails
    """
    cache_path = get_cache_path(ref)

    # Check cache first (unless force refresh)
    if not force_refresh and cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
                # Verify checksum if provided
                if ref.checksum:
                    content_hash = hashlib.sha256(
                        json.dumps(cached["data"], sort_keys=True).encode()
                    ).hexdigest()
                    if content_hash != ref.checksum:
                        print("  ⚠ Cache checksum mismatch, refetching...")
                    else:
                        return cached["data"]
                else:
                    return cached["data"]
        except (json.JSONDecodeError, KeyError):
            pass  # Cache corrupted, will refetch

    # Fetch from source
    print(f"  📥 Fetching gold standard from {ref.source_type}...")
    data = None

    try:
        if ref.source_type == "github":
            data = _fetch_from_github(ref)
        elif ref.source_type == "swe-bench":
            data = _fetch_from_swe_bench(ref)
        elif ref.source_type == "url":
            data = _fetch_from_url(ref)
        elif ref.source_type == "local":
            data = _fetch_from_local(ref)
        else:
            print(f"  ⚠ Unknown source type: {ref.source_type}")
            return None
    except Exception as e:
        print(f"  ⚠ Failed to fetch: {e}")
        return None

    # Cache the result
    if data:
        GOLD_STANDARD_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "ref": {
                        "source_type": ref.source_type,
                        "source_url": ref.source_url,
                        "commit_hash": ref.commit_hash,
                        "version": ref.version,
                    },
                    "fetched_at": datetime.now().isoformat(),
                    "data": data,
                },
                f,
                indent=2,
            )
        print(f"  ✓ Cached to {cache_path.name}")

    return data


def _fetch_from_github(ref: GoldStandardRef) -> Optional[Dict[str, Any]]:
    """Fetch gold standard from GitHub repository."""
    # Parse GitHub URL to construct raw content URL
    # Expected format: https://github.com/owner/repo/blob/commit/path
    # Or: owner/repo (with file_path and commit_hash in ref)

    if ref.source_url.startswith("https://github.com/"):
        # Full URL provided
        url = ref.source_url.replace("github.com", "raw.githubusercontent.com").replace(
            "/blob/", "/"
        )
    else:
        # Short format: owner/repo
        commit = ref.commit_hash or "main"
        path = ref.file_path or "gold_standard.json"
        url = f"https://raw.githubusercontent.com/{ref.source_url}/{commit}/{path}"

    print(f"    → {url}")

    req = urllib.request.Request(url, headers={"User-Agent": "prompts-library/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode("utf-8")
        return json.loads(content)


def _fetch_from_swe_bench(ref: GoldStandardRef) -> Optional[Dict[str, Any]]:
    """Fetch gold standard from SWE-bench dataset."""
    # SWE-bench instances are stored in HuggingFace datasets
    # https://huggingface.co/datasets/princeton-nlp/SWE-bench

    if not ref.benchmark_id:
        print("  ⚠ No benchmark_id provided for SWE-bench reference")
        return None

    # For now, return a placeholder structure
    # In production, would use HuggingFace datasets API
    print(f"    → SWE-bench instance: {ref.benchmark_id}")
    print("    ⚠ SWE-bench fetch requires huggingface_hub package")
    print("    → Install with: pip install huggingface_hub datasets")

    # Return expected structure for SWE-bench
    return {
        "benchmark": "swe-bench",
        "instance_id": ref.benchmark_id,
        "note": "Install huggingface_hub to fetch actual data",
        "docs_url": "https://www.swebench.com/",
        "dataset_url": "https://huggingface.co/datasets/princeton-nlp/SWE-bench",
    }


def _fetch_from_url(ref: GoldStandardRef) -> Optional[Dict[str, Any]]:
    """Fetch gold standard from arbitrary URL."""
    print(f"    → {ref.source_url}")

    req = urllib.request.Request(
        ref.source_url, headers={"User-Agent": "prompts-library/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode("utf-8")
        return json.loads(content)


def _fetch_from_local(ref: GoldStandardRef) -> Optional[Dict[str, Any]]:
    """Fetch gold standard from local file."""
    path = Path(ref.source_url)
    if not path.is_absolute():
        # Relative to this file's directory
        path = Path(__file__).parent / ref.source_url

    print(f"    → {path}")

    if not path.exists():
        print(f"  ⚠ Local file not found: {path}")
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# TEST TASK DEFINITIONS
# =============================================================================


class TaskCategory(Enum):
    """Categories of test tasks."""

    API_DESIGN = "api_design"
    CLI_TOOL = "cli_tool"
    DATA_PIPELINE = "data_pipeline"
    MICROSERVICES = "microservices"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DEVOPS = "devops"
    SECURITY = "security"


class TaskDifficulty(Enum):
    """Task difficulty levels."""

    EASY = "easy"  # Single-domain, clear requirements
    MEDIUM = "medium"  # Multi-domain, some ambiguity
    HARD = "hard"  # Complex, requires deep analysis
    EXPERT = "expert"  # Enterprise-scale, many constraints


@dataclass
class TestTask:
    """A test task for the multi-agent orchestrator."""

    id: int
    name: str
    description: str
    category: TaskCategory
    difficulty: TaskDifficulty
    expected_agents: List[str]  # Which agents should be involved
    evaluation_criteria: List[str]  # What to check in output
    tags: List[str] = field(default_factory=list)
    context: Optional[str] = None  # Additional context/constraints
    gold_standard_ref: Optional[GoldStandardRef] = (
        None  # Reference to fetch gold standard
    )
    _gold_standard_cache: Optional[Dict[str, Any]] = field(default=None, repr=False)

    def get_gold_standard(
        self, force_refresh: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Fetch gold standard on demand."""
        if not self.gold_standard_ref:
            return None

        if self._gold_standard_cache and not force_refresh:
            return self._gold_standard_cache

        self._gold_standard_cache = fetch_gold_standard(
            self.gold_standard_ref, force_refresh
        )
        return self._gold_standard_cache


@dataclass
class GoldStandard:
    """Gold standard output structure (fetched from source)."""

    required_components: List[str]  # Must be present (class names, functions, etc.)
    required_patterns: List[str]  # Regex patterns that must match
    code_structure: Optional[Dict[str, List[str]]] = (
        None  # {filename: [required_elements]}
    )
    api_endpoints: Optional[List[Dict[str, str]]] = (
        None  # [{method, path, description}]
    )
    database_tables: Optional[List[str]] = None  # Table names
    key_decisions: Optional[List[str]] = (
        None  # Architecture decisions that should appear
    )


# =============================================================================
# GOLD STANDARD FILE PATH
# =============================================================================

GOLD_STANDARDS_DIR = Path(__file__).parent / "gold_standards"


# =============================================================================
# CURATED TEST TASKS (with references to external gold standards)
# =============================================================================

TEST_TASKS: List[TestTask] = [
    # -------------------------------------------------------------------------
    # EASY TASKS - Good for basic testing
    # -------------------------------------------------------------------------
    TestTask(
        id=1,
        name="Simple REST API",
        description="""Design a REST API for a bookmark manager application.

Requirements:
- Users can save, list, update, and delete bookmarks
- Each bookmark has: URL, title, description, tags, created_at
- Support filtering by tags
- Support pagination for listing

Provide the API specification, database schema, and basic implementation approach.""",
        category=TaskCategory.API_DESIGN,
        difficulty=TaskDifficulty.EASY,
        expected_agents=["analyst", "researcher", "implementer"],
        evaluation_criteria=[
            "Defines CRUD endpoints",
            "Includes database schema",
            "Specifies request/response formats",
            "Addresses pagination",
            "Mentions authentication (optional)",
        ],
        tags=["rest", "api", "crud", "beginner"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_001_rest_api.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=2,
        name="Configuration File Parser",
        description="""Create a Python library for parsing configuration files.

Requirements:
- Support YAML, JSON, and TOML formats
- Provide a unified API regardless of format
- Support environment variable substitution (e.g., ${VAR_NAME})
- Support default values
- Type validation (optional)

Provide the class design, key methods, and usage examples.""",
        category=TaskCategory.CLI_TOOL,
        difficulty=TaskDifficulty.EASY,
        expected_agents=["analyst", "implementer"],
        evaluation_criteria=[
            "Unified interface for all formats",
            "Environment variable handling",
            "Default value support",
            "Clear usage examples",
            "Error handling approach",
        ],
        tags=["python", "config", "parsing", "library"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_002_config_parser.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    # -------------------------------------------------------------------------
    # MEDIUM TASKS - Multi-domain, some complexity
    # -------------------------------------------------------------------------
    TestTask(
        id=3,
        name="Event-Driven Notification System",
        description="""Design an event-driven notification system for a SaaS application.

Requirements:
- Support multiple channels: email, SMS, push notifications, Slack
- Event types: user_signup, password_reset, payment_success, payment_failed
- User preferences for notification channels
- Template system for message formatting
- Rate limiting and retry logic
- Audit logging

Provide the architecture, key components, and implementation strategy.""",
        category=TaskCategory.MICROSERVICES,
        difficulty=TaskDifficulty.MEDIUM,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Event-driven architecture",
            "Channel abstraction",
            "Template system design",
            "Rate limiting strategy",
            "Retry/failure handling",
            "Scalability considerations",
        ],
        tags=["events", "notifications", "microservices", "architecture"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_003_notification_system.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=4,
        name="Data Validation Pipeline",
        description="""Design a data validation pipeline for processing CSV uploads.

Requirements:
- Validate file format (encoding, delimiters, headers)
- Schema validation (column types, required fields)
- Business rule validation (ranges, patterns, relationships)
- Generate detailed validation reports
- Support for custom validation rules
- Handle files up to 100MB efficiently

Provide the pipeline architecture, validation stages, and error handling approach.""",
        category=TaskCategory.DATA_PIPELINE,
        difficulty=TaskDifficulty.MEDIUM,
        expected_agents=["analyst", "strategist", "implementer"],
        evaluation_criteria=[
            "Staged validation approach",
            "Schema definition format",
            "Custom rule extensibility",
            "Large file handling",
            "Report generation",
            "Performance considerations",
        ],
        tags=["data", "validation", "pipeline", "csv"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_004_data_pipeline.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=5,
        name="Feature Flag System",
        description="""Design a feature flag system for controlled feature rollouts.

Requirements:
- Toggle features on/off per environment
- Percentage-based rollouts
- User targeting (by ID, attributes, segments)
- A/B testing support
- Real-time updates without deployment
- SDK for Python and JavaScript
- Admin dashboard for flag management

Provide the system architecture, SDK design, and evaluation logic.""",
        category=TaskCategory.DEVOPS,
        difficulty=TaskDifficulty.MEDIUM,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Flag evaluation logic",
            "Targeting rules engine",
            "Real-time sync mechanism",
            "SDK interface design",
            "Dashboard features",
            "Performance (latency requirements)",
        ],
        tags=["feature-flags", "devops", "a-b-testing", "sdk"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_005_feature_flags.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    # -------------------------------------------------------------------------
    # HARD TASKS - Complex, requires deep analysis
    # -------------------------------------------------------------------------
    TestTask(
        id=6,
        name="Code Review Automation",
        description="""Design an automated code review system that integrates with GitHub.

Requirements:
- Analyze pull requests for common issues
- Support multiple languages (Python, JavaScript, TypeScript)
- Configurable rule sets
- Auto-comment on specific lines
- Track review history and patterns
- Learn from accepted/rejected suggestions

Provide the architecture, analysis pipeline, and GitHub integration approach.""",
        category=TaskCategory.DEVOPS,
        difficulty=TaskDifficulty.HARD,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Analysis pipeline design",
            "Multi-language support approach",
            "Rule configuration system",
            "GitHub API integration",
            "Learning/feedback loop",
            "Performance at scale",
        ],
        tags=["code-review", "github", "automation", "ml"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_006_code_review.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=7,
        name="Multi-Tenant SaaS Architecture",
        description="""Design a multi-tenant architecture for a B2B SaaS application.

Requirements:
- Support 1000+ tenants with varying sizes
- Data isolation strategies
- Per-tenant customization (branding, features)
- Tenant provisioning and onboarding
- Usage metering and billing integration
- Cross-tenant reporting (for admin)
- Tenant self-service admin portal

Provide the architecture, data model, and isolation strategy.""",
        category=TaskCategory.MICROSERVICES,
        difficulty=TaskDifficulty.HARD,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Tenant isolation approach",
            "Database strategy (shared vs dedicated)",
            "Customization architecture",
            "Provisioning workflow",
            "Billing integration",
            "Security boundaries",
            "Scalability considerations",
        ],
        tags=["multi-tenant", "saas", "architecture", "enterprise"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_007_multi_tenant.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=8,
        name="API Rate Limiter",
        description="""Design a distributed rate limiting system for a high-traffic API.

Requirements:
- Support multiple algorithms: fixed window, sliding window, token bucket
- Distributed across multiple nodes
- Per-user and per-API-key limits
- Tiered limits based on subscription level
- Real-time metrics and alerting
- Graceful degradation under load
- Sub-millisecond latency requirement

Provide the architecture, algorithm implementations, and distributed coordination approach.""",
        category=TaskCategory.API_DESIGN,
        difficulty=TaskDifficulty.HARD,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Algorithm implementations",
            "Distributed coordination",
            "Storage backend selection",
            "Latency optimization",
            "Tiered limit configuration",
            "Metrics and monitoring",
            "Failure handling",
        ],
        tags=["rate-limiting", "distributed", "api", "performance"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_008_rate_limiter.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    # -------------------------------------------------------------------------
    # EXPERT TASKS - Enterprise-scale, many constraints
    # -------------------------------------------------------------------------
    TestTask(
        id=9,
        name="Legacy System Migration",
        description="""Plan a migration from a 15-year-old monolithic system to microservices.

Current State:
- Java EE monolith with 2M lines of code
- Oracle database with 500+ tables
- 50+ integrations with external systems
- 200 active users, 10k daily transactions
- Poor test coverage (<20%)

Constraints:
- No downtime during business hours
- Maintain all integrations
- Complete within 18 months
- Budget: $2M

Provide the migration strategy, risk analysis, and team organization.""",
        category=TaskCategory.REFACTORING,
        difficulty=TaskDifficulty.EXPERT,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Strangler fig implementation",
            "Domain decomposition approach",
            "Data migration strategy",
            "Integration handling",
            "Risk identification and mitigation",
            "Team organization",
            "Timeline and milestones",
            "Success metrics",
        ],
        tags=["migration", "monolith", "microservices", "enterprise"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_009_legacy_migration.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
    TestTask(
        id=10,
        name="Security Incident Response Platform",
        description="""Design a security incident response platform for a SOC team.

Requirements:
- Ingest alerts from multiple sources (SIEM, EDR, cloud, network)
- Automated alert correlation and prioritization
- Playbook automation for common incidents
- Case management with SLA tracking
- Integration with threat intelligence feeds
- Compliance reporting (SOC 2, GDPR)
- Real-time dashboards and metrics
- Team collaboration features

Provide the architecture, data model, and automation framework.""",
        category=TaskCategory.SECURITY,
        difficulty=TaskDifficulty.EXPERT,
        expected_agents=["analyst", "researcher", "strategist", "implementer"],
        evaluation_criteria=[
            "Alert ingestion architecture",
            "Correlation engine design",
            "Playbook execution framework",
            "Case management workflow",
            "Threat intel integration",
            "Compliance reporting",
            "Dashboard design",
            "Scalability (alerts/second)",
        ],
        tags=["security", "soc", "incident-response", "enterprise"],
        gold_standard_ref=GoldStandardRef(
            source_type="local",
            source_url="gold_standards/task_010_security_incident.json",
            version="1.0",
            last_verified="2026-01-23",
        ),
    ),
]

# =============================================================================
# GOLD STANDARD EVALUATION
# =============================================================================


def evaluate_against_gold_standard(
    output: str, gold_standard: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate output against gold standard requirements.

    Returns detailed scoring with:
    - Component coverage (required elements found)
    - Pattern matching (regex patterns matched)
    - Key decision coverage
    - Overall score (0-100)
    """
    results = {
        "components": {"matched": [], "missing": [], "score": 0.0},
        "patterns": {"matched": [], "missing": [], "score": 0.0},
        "decisions": {"matched": [], "missing": [], "score": 0.0},
        "endpoints": {"matched": [], "missing": [], "score": 0.0},
        "tables": {"matched": [], "missing": [], "score": 0.0},
        "overall_score": 0.0,
        "grade": "F",
    }

    output_lower = output.lower()
    scores = []

    # Check required components
    if "required_components" in gold_standard:
        components = gold_standard["required_components"]
        for comp in components:
            if comp.lower() in output_lower:
                results["components"]["matched"].append(comp)
            else:
                results["components"]["missing"].append(comp)
        if components:
            results["components"]["score"] = (
                len(results["components"]["matched"]) / len(components) * 100
            )
            scores.append(results["components"]["score"])

    # Check required patterns (regex)
    if "required_patterns" in gold_standard:
        patterns = gold_standard["required_patterns"]
        for pattern in patterns:
            try:
                if re.search(pattern, output, re.IGNORECASE):
                    results["patterns"]["matched"].append(pattern)
                else:
                    results["patterns"]["missing"].append(pattern)
            except re.error:
                # Invalid regex, skip
                pass
        if patterns:
            results["patterns"]["score"] = (
                len(results["patterns"]["matched"]) / len(patterns) * 100
            )
            scores.append(results["patterns"]["score"])

    # Check key decisions
    if "key_decisions" in gold_standard:
        decisions = gold_standard["key_decisions"]
        for decision in decisions:
            # Check if key terms from decision appear in output
            key_terms = decision.lower().split()
            # Require at least 50% of key terms to match
            matches = sum(
                1 for term in key_terms if len(term) > 3 and term in output_lower
            )
            if matches >= len([t for t in key_terms if len(t) > 3]) * 0.4:
                results["decisions"]["matched"].append(decision)
            else:
                results["decisions"]["missing"].append(decision)
        if decisions:
            results["decisions"]["score"] = (
                len(results["decisions"]["matched"]) / len(decisions) * 100
            )
            scores.append(results["decisions"]["score"])

    # Check API endpoints
    if "api_endpoints" in gold_standard:
        endpoints = gold_standard["api_endpoints"]
        for ep in endpoints:
            method = ep.get("method", "").lower()
            path = ep.get("path", "").lower()
            # Check if both method and path pattern appear
            if (
                method in output_lower
                and path.replace("{id}", "").replace("/", " ").strip() in output_lower
            ):
                results["endpoints"]["matched"].append(f"{ep['method']} {ep['path']}")
            else:
                results["endpoints"]["missing"].append(f"{ep['method']} {ep['path']}")
        if endpoints:
            results["endpoints"]["score"] = (
                len(results["endpoints"]["matched"]) / len(endpoints) * 100
            )
            scores.append(results["endpoints"]["score"])

    # Check database tables
    if "database_tables" in gold_standard:
        tables = gold_standard["database_tables"]
        for table in tables:
            if table.lower() in output_lower:
                results["tables"]["matched"].append(table)
            else:
                results["tables"]["missing"].append(table)
        if tables:
            results["tables"]["score"] = (
                len(results["tables"]["matched"]) / len(tables) * 100
            )
            scores.append(results["tables"]["score"])

    # Calculate overall score
    if scores:
        results["overall_score"] = sum(scores) / len(scores)

    # Assign grade
    score = results["overall_score"]
    if score >= 90:
        results["grade"] = "A"
    elif score >= 80:
        results["grade"] = "B"
    elif score >= 70:
        results["grade"] = "C"
    elif score >= 60:
        results["grade"] = "D"
    else:
        results["grade"] = "F"

    return results


def print_gold_standard_report(eval_results: Dict[str, Any], verbose: bool = True):
    """Print a formatted gold standard evaluation report."""
    print("\n" + "-" * 80)
    print("GOLD STANDARD COMPARISON")
    print("-" * 80)

    print(
        f"\n📊 Overall Score: {eval_results['overall_score']:.1f}/100 (Grade: {eval_results['grade']})"
    )

    # Components
    if eval_results["components"]["matched"] or eval_results["components"]["missing"]:
        comp = eval_results["components"]
        print(f"\n🧩 Components: {comp['score']:.0f}%")
        if verbose:
            for c in comp["matched"]:
                print(f"   ✓ {c}")
            for c in comp["missing"]:
                print(f"   ✗ {c}")

    # Patterns
    if eval_results["patterns"]["matched"] or eval_results["patterns"]["missing"]:
        pat = eval_results["patterns"]
        print(f"\n🔍 Pattern Matching: {pat['score']:.0f}%")
        if verbose:
            print(
                f"   Matched: {len(pat['matched'])}/{len(pat['matched']) + len(pat['missing'])}"
            )

    # Key Decisions
    if eval_results["decisions"]["matched"] or eval_results["decisions"]["missing"]:
        dec = eval_results["decisions"]
        print(f"\n💡 Key Decisions: {dec['score']:.0f}%")
        if verbose:
            for d in dec["matched"]:
                print(f"   ✓ {d}")
            for d in dec["missing"]:
                print(f"   ✗ {d}")

    # API Endpoints
    if eval_results["endpoints"]["matched"] or eval_results["endpoints"]["missing"]:
        ep = eval_results["endpoints"]
        print(f"\n🌐 API Endpoints: {ep['score']:.0f}%")
        if verbose:
            for e in ep["matched"]:
                print(f"   ✓ {e}")
            for e in ep["missing"]:
                print(f"   ✗ {e}")

    # Database Tables
    if eval_results["tables"]["matched"] or eval_results["tables"]["missing"]:
        tbl = eval_results["tables"]
        print(f"\n🗄️ Database Tables: {tbl['score']:.0f}%")
        if verbose:
            for t in tbl["matched"]:
                print(f"   ✓ {t}")
            for t in tbl["missing"]:
                print(f"   ✗ {t}")


# =============================================================================
# RUNNER
# =============================================================================


def list_tasks():
    """Print all available test tasks."""
    print("\n" + "=" * 80)
    print("AVAILABLE TEST TASKS")
    print("=" * 80)

    for task in TEST_TASKS:
        print(f"\n[{task.id}] {task.name}")
        print(f"    Category: {task.category.value}")
        print(f"    Difficulty: {task.difficulty.value}")
        print(f"    Expected agents: {', '.join(task.expected_agents)}")
        print(f"    Tags: {', '.join(task.tags)}")

        # Check gold standard reference
        if task.gold_standard_ref:
            src = task.gold_standard_ref.source_type
            url = task.gold_standard_ref.source_url
            ver = task.gold_standard_ref.version
            print(f"    Gold standard: ✓ [{src}] {url} (v{ver})")
        else:
            print("    Gold standard: ✗ (none)")

    print("\n" + "=" * 80)
    print(f"Total: {len(TEST_TASKS)} tasks")
    print("=" * 80)


def run_task(
    task: TestTask,
    model: str = "gh:gpt-4o-mini",
    verbose: bool = True,
) -> Dict[str, Any]:
    """Run a single test task and return results."""
    print(f"\n{'=' * 80}")
    print(f"RUNNING TASK {task.id}: {task.name}")
    print(f"Difficulty: {task.difficulty.value} | Category: {task.category.value}")
    print(f"{'=' * 80}\n")

    orchestrator = MultiAgentOrchestrator(
        model=model,
        verbose=verbose,
    )

    start_time = datetime.now()
    result = orchestrator.run(task.description)
    end_time = datetime.now()

    # Evaluate results
    evaluation = {
        "task_id": task.id,
        "task_name": task.name,
        "model": model,
        "duration_seconds": result.total_duration_seconds,
        "successful_tasks": result.metadata.get("successful_tasks", 0),
        "total_tasks": result.metadata.get("num_tasks", 0),
        "criteria_checked": [],
        "gold_standard_eval": None,
    }

    # Check evaluation criteria (simple keyword matching)
    output_lower = result.final_output.lower()
    for criterion in task.evaluation_criteria:
        # Simple heuristic: check if key terms from criterion appear in output
        key_terms = criterion.lower().split()
        found = sum(1 for term in key_terms if term in output_lower)
        evaluation["criteria_checked"].append(
            {
                "criterion": criterion,
                "likely_covered": found >= len(key_terms) * 0.5,
            }
        )

    # Gold standard evaluation (fetch on demand)
    gold_standard = task.get_gold_standard()
    if gold_standard:
        gold_eval = evaluate_against_gold_standard(result.final_output, gold_standard)
        evaluation["gold_standard_eval"] = gold_eval

    return {
        "evaluation": evaluation,
        "result": result,
    }


def run_all_tasks(
    model: str = "gh:gpt-4o-mini",
    verbose: bool = False,
    max_tasks: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """Run all test tasks and return aggregated results."""
    results = []
    tasks_to_run = TEST_TASKS[:max_tasks] if max_tasks else TEST_TASKS

    for task in tasks_to_run:
        try:
            result = run_task(task, model=model, verbose=verbose)
            results.append(result)
        except Exception as e:
            print(f"ERROR running task {task.id}: {e}")
            results.append(
                {
                    "evaluation": {
                        "task_id": task.id,
                        "task_name": task.name,
                        "error": str(e),
                    },
                    "result": None,
                }
            )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run test tasks for the Multi-Agent Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--task",
        "-t",
        type=int,
        help="Run a specific task by ID",
    )
    parser.add_argument(
        "--all",
        "-a",
        action="store_true",
        help="Run all tasks",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available tasks",
    )
    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="gh:gpt-4o-mini",
        help="Model to use (default: gh:gpt-4o-mini)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--max-tasks",
        type=int,
        help="Maximum number of tasks to run (with --all)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file for results (JSON)",
    )
    parser.add_argument(
        "--fetch-gold",
        type=int,
        metavar="TASK_ID",
        help="Fetch and display gold standard for a task",
    )
    parser.add_argument(
        "--refresh-gold",
        action="store_true",
        help="Force refresh gold standard from source (with --fetch-gold or --task)",
    )

    args = parser.parse_args()

    # Handle fetch-gold command
    if args.fetch_gold:
        task = next((t for t in TEST_TASKS if t.id == args.fetch_gold), None)
        if not task:
            print(f"Error: Task {args.fetch_gold} not found")
            sys.exit(1)

        if not task.gold_standard_ref:
            print(f"Task {task.id} has no gold standard reference")
            sys.exit(1)

        print(f"\n{'=' * 80}")
        print(f"GOLD STANDARD: Task {task.id} - {task.name}")
        print(f"{'=' * 80}")
        print(f"\nSource: {task.gold_standard_ref.source_type}")
        print(f"URL: {task.gold_standard_ref.source_url}")
        print(f"Version: {task.gold_standard_ref.version}")
        if task.gold_standard_ref.commit_hash:
            print(f"Commit: {task.gold_standard_ref.commit_hash}")
        if task.gold_standard_ref.last_verified:
            print(f"Last Verified: {task.gold_standard_ref.last_verified}")

        print("\nFetching...")
        gold = task.get_gold_standard(force_refresh=args.refresh_gold)

        if gold:
            print(f"\n{'=' * 80}")
            print("GOLD STANDARD CONTENT")
            print("=" * 80)
            print(json.dumps(gold, indent=2))
        else:
            print("\n⚠ Failed to fetch gold standard")
            sys.exit(1)
        return

    if args.list:
        list_tasks()
        return

    if args.task:
        # Find task by ID
        task = next((t for t in TEST_TASKS if t.id == args.task), None)
        if not task:
            print(f"Error: Task {args.task} not found")
            sys.exit(1)

        result = run_task(task, model=args.model, verbose=args.verbose)

        print("\n" + "=" * 80)
        print("FINAL OUTPUT")
        print("=" * 80)
        print(result["result"].final_output)

        print("\n" + "=" * 80)
        print("EVALUATION")
        print("=" * 80)
        eval_data = result["evaluation"]
        print(f"Duration: {eval_data['duration_seconds']:.1f}s")
        print(
            f"Tasks: {eval_data['successful_tasks']}/{eval_data['total_tasks']} successful"
        )
        print("\nCriteria Coverage:")
        for check in eval_data["criteria_checked"]:
            status = "✓" if check["likely_covered"] else "?"
            print(f"  [{status}] {check['criterion']}")

        # Print gold standard evaluation if available
        if eval_data.get("gold_standard_eval"):
            print_gold_standard_report(
                eval_data["gold_standard_eval"], verbose=args.verbose
            )

        if args.output:
            # Can't serialize the full result, just save evaluation
            with open(args.output, "w") as f:
                json.dump(eval_data, f, indent=2)
            print(f"\nResults saved to {args.output}")

    elif args.all:
        results = run_all_tasks(
            model=args.model,
            verbose=args.verbose,
            max_tasks=args.max_tasks,
        )

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        for r in results:
            eval_data = r["evaluation"]
            if "error" in eval_data:
                print(
                    f"[{eval_data['task_id']}] {eval_data['task_name']}: ERROR - {eval_data['error']}"
                )
            else:
                success_rate = eval_data["successful_tasks"] / max(
                    eval_data["total_tasks"], 1
                )
                gold_grade = ""
                if eval_data.get("gold_standard_eval"):
                    gold_grade = f" | Gold: {eval_data['gold_standard_eval']['grade']} ({eval_data['gold_standard_eval']['overall_score']:.0f}%)"
                print(
                    f"[{eval_data['task_id']}] {eval_data['task_name']}: "
                    f"{eval_data['duration_seconds']:.1f}s, "
                    f"{success_rate:.0%} task success{gold_grade}"
                )

        if args.output:
            with open(args.output, "w") as f:
                json.dump([r["evaluation"] for r in results], f, indent=2)
            print(f"\nResults saved to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
