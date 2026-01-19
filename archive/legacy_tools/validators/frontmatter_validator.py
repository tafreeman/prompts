#!/usr/bin/env python3
"""
Frontmatter Validator for Prompt Library
Validates YAML frontmatter against the unified schema defined in UNIFIED_REFACTOR_GUIDE_REACT.md

This validator distinguishes between:
1. DOCUMENTATION/CONTENT files - require full frontmatter schema
2. FUNCTIONAL CONFIG files - have their own minimal schemas:
   - *.agent.md files: name, description, tools (GitHub Copilot custom agents)
   - *.instructions.md files: applyTo, description, name (Copilot instructions)
   - .github/copilot-instructions.md: no frontmatter required

Usage:
    python tools/validators/frontmatter_validator.py --all
    python tools/validators/frontmatter_validator.py path/to/file.md
    python tools/validators/frontmatter_validator.py --folder prompts/developers/
"""

import argparse
import sys
import yaml
import re
import fnmatch
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class FileType(Enum):
    """Types of files with different validation schemas."""
    DOCUMENTATION = "documentation"  # Full frontmatter schema
    AGENT = "agent"                  # Minimal: name, description, tools
    INSTRUCTIONS = "instructions"    # Minimal: applyTo, description, name
    EXCLUDED = "excluded"            # Skip validation entirely


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    severity: Severity
    field: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    file_path: str
    is_valid: bool
    issues: List[Issue] = field(default_factory=list)
    
    def add_error(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.ERROR, field_name, message, suggestion))
        self.is_valid = False
    
    def add_warning(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.WARNING, field_name, message, suggestion))
    
    def add_info(self, field_name: str, message: str, suggestion: Optional[str] = None):
        self.issues.append(Issue(Severity.INFO, field_name, message, suggestion))


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEMA DEFINITION (from UNIFIED_REFACTOR_GUIDE_REACT.md)
# ═══════════════════════════════════════════════════════════════════════════════

VALID_TYPES = ["conceptual", "quickstart", "how_to", "tutorial", "reference", "troubleshooting"]

VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]

VALID_AUDIENCES = [
    "junior-engineer",
    "senior-engineer", 
    "solution-architect",
    "qa-engineer",
    "business-analyst",
    "project-manager",
    "functional-team"
]

VALID_PLATFORMS = [
    "github-copilot",
    "claude",
    "chatgpt",
    "azure-openai",
    "m365-copilot"
]

VALID_TECHNIQUES = [
    "chain-of-thought",
    "react",
    "tree-of-thought",
    "few-shot",
    "zero-shot",
    "reflection",
    "rag"
]

VALID_GOVERNANCE_TAGS = [
    # Core governance tags (original)
    "PII-safe",
    "client-approved",
    "internal-only",
    "requires-human-review",
    "audit-required",
    # General usage tags
    "general-use",
    "internal-use-only",
    # Human review variants
    "requires-human-review-for-critical-decisions",
    "requires-human-review-for-sensitive-docs",
    "requires-human-review-for-external-tools",
    "human-review-recommended",
    "requires-review",
    "requires-executive-review",
    # Architecture & technical decision tags
    "architecture-decision",
    "architecture-decision-record",
    "adr-required",
    "architectural-change",
    "system-architecture",
    "technical-documentation",
    "strategic-decision",
    # Code quality & security tags
    "secure-coding",
    "security-critical",
    "quality-assurance",
    "quality-control",
    # Data & governance tags
    "data-governance",
    "data-privacy",
    "quality-metrics",
    "tenant-boundaries",
    "compliance",
    "compliance-reporting",
    # Risk & audit tags
    "risk-assessment",
    "audit-trail",
    "restricted-access",
    "sensitive",
    # Approval tags
    "attorney-approval-required",
    "CISO-approval-required",
    # Change & production tags
    "change-management",
    "production-impact",
    # Analysis & automation tags
    "safe-for-automated-analysis",
    "research",
    "knowledge-synthesis",
    # Meta & process tags
    "meta-prompt",
    "continuous-improvement",
]

VALID_DATA_CLASSIFICATIONS = ["public", "internal", "confidential"]

VALID_REVIEW_STATUSES = ["draft", "reviewed", "approved"]

VALID_LEARNING_TRACKS = ["engineer-quickstart", "architect-depth", "functional-productivity"]

VALID_TOPICS = [
    "code-generation",
    "debugging",
    "refactoring",
    "testing",
    "documentation",
    "analysis",
    "governance"
]

# Required fields for all content
REQUIRED_FIELDS_ALL = [
    "title",
    "shortTitle", 
    "intro",
    "type",
    "difficulty",
    "author",
    "version",
    "date",
    "governance_tags",
    "dataClassification",
    "reviewStatus"
]

# Required fields for prompts (not index.md)
REQUIRED_FIELDS_PROMPTS = [
    "audience",
    "platforms"
]

# Navigation fields (index.md only)
INDEX_FIELDS = ["children", "featuredLinks", "layout"]

# ═══════════════════════════════════════════════════════════════════════════════
# FILE TYPE DETECTION
# Determines which validation schema to apply based on file path/name
# ═══════════════════════════════════════════════════════════════════════════════

# Files to EXCLUDE from validation entirely (no frontmatter expected)
EXCLUDED_PATTERNS = [
    '.github/copilot-instructions.md',  # Workspace instructions (no frontmatter)
    '.github/instructions/copilot-instructions.md',  # Alt location
    '.github/agents/README.md',   # Human-readable docs in functional directory
    '.github/agents/AGENTS_GUIDE.md',  # Human-readable docs in functional directory
    'SECURITY.md',                # Root-level standard file (no frontmatter)
    'LICENSE',                    # License file
    'docs/archive/*',             # Archived planning docs (no frontmatter validation)
    'docs/archive/**/*',          # Nested archived files
]

# Cursor IDE config files - different format, exclude from VS Code schema validation
CURSOR_PATTERNS = [
    '.agent/rules/*.md',      # Cursor rule files (use trigger, glob fields)
    '.agent/workflows/*.md',  # Cursor workflow files (step-by-step format)
    '.cursorrules',           # Cursor project rules file
]

# Files to validate with AGENT schema (name, description, tools)
AGENT_PATTERNS = [
    '*.agent.md',           # Any file ending in .agent.md
    '.github/agents/*.agent.md',  # Only .agent.md files in .github/agents
]

# Documentation files in agent directories (use full documentation schema)
# These are content files that happen to be in agent folders
AGENT_DOCS_PATTERNS = [
    'agents/README.md',
    'agents/AGENTS_GUIDE.md',
]

# Files to validate with INSTRUCTIONS schema (applyTo, description, name)
INSTRUCTIONS_PATTERNS = [
    '*.instructions.md',           # Any file ending in .instructions.md
    '.github/instructions/*.md',   # Instruction files (but not copilot-instructions.md)
]

# Template files that should keep minimal format (they are meant to be copied)
TEMPLATE_PATTERNS = [
    'agents/agent-template.md',
    '.github/agents/agent-template.md',
]


def get_file_type(file_path: Path, repo_root: Path) -> FileType:
    """
    Determine the validation schema to use based on file path.
    
    Args:
        file_path: Absolute path to the file
        repo_root: Repository root path
        
    Returns:
        FileType indicating which validation schema to apply
    """
    # Get relative path for pattern matching
    try:
        rel_path = file_path.relative_to(repo_root)
    except ValueError:
        rel_path = file_path
    
    rel_path_str = str(rel_path).replace('\\', '/')  # Normalize for cross-platform
    file_name = file_path.name
    
    # Check exclusions first
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(rel_path_str, pattern) or rel_path_str == pattern:
            return FileType.EXCLUDED
    
    # Check Cursor patterns (different format, exclude from validation)
    for pattern in CURSOR_PATTERNS:
        if fnmatch.fnmatch(rel_path_str, pattern) or rel_path_str == pattern:
            return FileType.EXCLUDED
    
    # Check if it's a template that should be treated as agent format
    for pattern in TEMPLATE_PATTERNS:
        if fnmatch.fnmatch(rel_path_str, pattern) or rel_path_str == pattern:
            return FileType.AGENT
    
    # Check for documentation files in agent directories (treat as docs, not agents)
    for pattern in AGENT_DOCS_PATTERNS:
        if fnmatch.fnmatch(rel_path_str, pattern) or rel_path_str == pattern:
            return FileType.DOCUMENTATION
    
    # Check agent patterns
    for pattern in AGENT_PATTERNS:
        if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(rel_path_str, pattern):
            return FileType.AGENT
    
    # Check instructions patterns  
    for pattern in INSTRUCTIONS_PATTERNS:
        if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(rel_path_str, pattern):
            return FileType.INSTRUCTIONS
    
    # Default: full documentation schema
    return FileType.DOCUMENTATION


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDATOR
# ═══════════════════════════════════════════════════════════════════════════════

class FrontmatterValidator:
    
    def __init__(self, strict: bool = False, repo_root: Optional[Path] = None):
        """
        Initialize validator.
        
        Args:
            strict: If True, warnings become errors
            repo_root: Repository root path for file type detection
        """
        self.strict = strict
        self.repo_root = repo_root or Path.cwd()
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single markdown file based on its type."""
        result = ValidationResult(file_path=str(file_path), is_valid=True)
        
        # Determine file type
        file_type = get_file_type(file_path, self.repo_root)
        
        # Skip excluded files
        if file_type == FileType.EXCLUDED:
            result.add_info("file_type", "Excluded from validation (functional config file)")
            return result
        
        # Read file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            result.add_error("file", f"Could not read file: {e}")
            return result
        
        # Extract frontmatter
        frontmatter = self._extract_frontmatter(content)
        
        # Route to appropriate validation based on file type
        if file_type == FileType.AGENT:
            return self._validate_agent_file(frontmatter, result)
        elif file_type == FileType.INSTRUCTIONS:
            return self._validate_instructions_file(frontmatter, result)
        else:
            return self._validate_documentation_file(frontmatter, file_path, result)
    
    def _validate_agent_file(self, frontmatter: Optional[Dict], result: ValidationResult) -> ValidationResult:
        """Validate agent file with minimal schema: name, description, tools."""
        if frontmatter is None:
            result.add_error("frontmatter", "No valid YAML frontmatter found",
                           "Add YAML frontmatter with name, description, tools fields")
            return result
        
        # Required: name and description
        if "name" not in frontmatter:
            result.add_error("name", "Missing required field: name")
        if "description" not in frontmatter:
            result.add_error("description", "Missing required field: description")
        
        # Optional but recommended: tools
        if "tools" not in frontmatter:
            result.add_warning("tools", "Missing tools field",
                             "Add tools array to specify agent capabilities")
        elif not isinstance(frontmatter["tools"], list):
            result.add_error("tools", "tools must be an array")
        
        # Warn if documentation fields are present (they shouldn't be in agent files)
        doc_fields = ["title", "shortTitle", "intro", "type", "difficulty", 
                      "audience", "platforms", "governance_tags", "dataClassification", "reviewStatus"]
        present_doc_fields = [f for f in doc_fields if f in frontmatter]
        if present_doc_fields:
            result.add_warning("schema", 
                             f"Agent files should only have name, description, tools. Found extra fields: {', '.join(present_doc_fields)}",
                             "Remove documentation-style frontmatter from agent configuration files")
        
        return result
    
    def _validate_instructions_file(self, frontmatter: Optional[Dict], result: ValidationResult) -> ValidationResult:
        """Validate instructions file with minimal schema: applyTo, description, name."""
        # Instructions files can have no frontmatter (body-only instructions)
        if frontmatter is None:
            result.add_info("frontmatter", "No frontmatter found (body-only instructions file)")
            return result
        
        # All fields are optional for instructions files
        # Just check that if present, they're valid types
        if "applyTo" in frontmatter and not isinstance(frontmatter["applyTo"], str):
            result.add_error("applyTo", "applyTo must be a string (glob pattern)")
        
        if "name" in frontmatter and not isinstance(frontmatter["name"], str):
            result.add_error("name", "name must be a string")
        
        if "description" in frontmatter and not isinstance(frontmatter["description"], str):
            result.add_error("description", "description must be a string")
        
        # Warn if documentation fields are present
        doc_fields = ["title", "shortTitle", "intro", "type", "difficulty", 
                      "audience", "platforms", "governance_tags", "dataClassification", "reviewStatus"]
        present_doc_fields = [f for f in doc_fields if f in frontmatter]
        if present_doc_fields:
            result.add_warning("schema",
                             f"Instruction files should only have applyTo, description, name. Found extra fields: {', '.join(present_doc_fields)}",
                             "Remove documentation-style frontmatter from instruction files")
        
        return result
    
    def _validate_documentation_file(self, frontmatter: Optional[Dict], file_path: Path, result: ValidationResult) -> ValidationResult:
        """Validate documentation/content file with full schema."""
        if frontmatter is None:
            result.add_error("frontmatter", "No valid YAML frontmatter found", 
                           "Add YAML frontmatter between --- delimiters")
            return result
        
        # Determine if this is an index file
        is_index = file_path.name == "index.md"
        
        # Validate required fields
        self._validate_required_fields(frontmatter, is_index, result)
        
        # Validate field values
        self._validate_field_values(frontmatter, result)
        
        # Validate constraints
        self._validate_constraints(frontmatter, result)
        
        # Validate index-specific fields
        if is_index:
            self._validate_index_fields(frontmatter, result)
        
        return result
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """Extract YAML frontmatter from markdown content."""
        if not content.strip().startswith('---'):
            return None
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        try:
            return yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            return None
    
    def _validate_required_fields(self, fm: Dict, is_index: bool, result: ValidationResult):
        """Check that all required fields are present."""
        
        # All content requires these
        for field_name in REQUIRED_FIELDS_ALL:
            if field_name not in fm:
                result.add_error(field_name, f"Missing required field: {field_name}")
        
        # Prompts (non-index) require these additional fields
        if not is_index:
            for field_name in REQUIRED_FIELDS_PROMPTS:
                if field_name not in fm:
                    result.add_error(field_name, f"Missing required field: {field_name}")
    
    def _validate_field_values(self, fm: Dict, result: ValidationResult):
        """Validate that field values are from allowed sets."""
        
        # type
        if "type" in fm and fm["type"] not in VALID_TYPES:
            result.add_error("type", f"Invalid type: '{fm['type']}'",
                           f"Use one of: {', '.join(VALID_TYPES)}")
        
        # difficulty
        if "difficulty" in fm and fm["difficulty"] not in VALID_DIFFICULTIES:
            result.add_error("difficulty", f"Invalid difficulty: '{fm['difficulty']}'",
                           f"Use one of: {', '.join(VALID_DIFFICULTIES)}")
        
        # audience (array)
        if "audience" in fm:
            if not isinstance(fm["audience"], list):
                result.add_error("audience", "audience must be an array")
            else:
                for aud in fm["audience"]:
                    if aud not in VALID_AUDIENCES:
                        result.add_error("audience", f"Invalid audience value: '{aud}'",
                                       f"Use one of: {', '.join(VALID_AUDIENCES)}")
        
        # platforms (array)
        if "platforms" in fm:
            if not isinstance(fm["platforms"], list):
                result.add_error("platforms", "platforms must be an array")
            else:
                for plat in fm["platforms"]:
                    if plat not in VALID_PLATFORMS:
                        result.add_error("platforms", f"Invalid platform: '{plat}'",
                                       f"Use one of: {', '.join(VALID_PLATFORMS)}")
        
        # technique (optional)
        if "technique" in fm and fm["technique"] not in VALID_TECHNIQUES:
            result.add_warning("technique", f"Invalid technique: '{fm['technique']}'",
                             f"Use one of: {', '.join(VALID_TECHNIQUES)}")
        
        # governance_tags (array)
        if "governance_tags" in fm:
            if not isinstance(fm["governance_tags"], list):
                result.add_error("governance_tags", "governance_tags must be an array")
            else:
                for tag in fm["governance_tags"]:
                    if tag not in VALID_GOVERNANCE_TAGS:
                        result.add_warning("governance_tags", f"Unknown governance tag: '{tag}'",
                                         f"Standard tags are: {', '.join(VALID_GOVERNANCE_TAGS)}")
        
        # dataClassification
        if "dataClassification" in fm and fm["dataClassification"] not in VALID_DATA_CLASSIFICATIONS:
            result.add_error("dataClassification", f"Invalid dataClassification: '{fm['dataClassification']}'",
                           f"Use one of: {', '.join(VALID_DATA_CLASSIFICATIONS)}")
        
        # reviewStatus
        if "reviewStatus" in fm and fm["reviewStatus"] not in VALID_REVIEW_STATUSES:
            result.add_error("reviewStatus", f"Invalid reviewStatus: '{fm['reviewStatus']}'",
                           f"Use one of: {', '.join(VALID_REVIEW_STATUSES)}")
        
        # learningTrack (optional)
        if "learningTrack" in fm and fm["learningTrack"] not in VALID_LEARNING_TRACKS:
            result.add_warning("learningTrack", f"Invalid learningTrack: '{fm['learningTrack']}'",
                             f"Use one of: {', '.join(VALID_LEARNING_TRACKS)}")
        
        # topics (optional array)
        if "topics" in fm:
            if not isinstance(fm["topics"], list):
                result.add_warning("topics", "topics should be an array")
            else:
                for topic in fm["topics"]:
                    if topic not in VALID_TOPICS:
                        result.add_info("topics", f"Non-standard topic: '{topic}'",
                                      f"Standard topics are: {', '.join(VALID_TOPICS)}")
    
    def _validate_constraints(self, fm: Dict, result: ValidationResult):
        """Validate field constraints like length limits and formats."""
        
        # title: ≤60 chars
        if "title" in fm and isinstance(fm["title"], str):
            if len(fm["title"]) > 60:
                result.add_error("title", f"Title exceeds 60 characters ({len(fm['title'])} chars)",
                               "Shorten title to ≤60 characters")
        
        # shortTitle: ≤27 chars (GitHub Docs standard)
        if "shortTitle" in fm and isinstance(fm["shortTitle"], str):
            if len(fm["shortTitle"]) > 27:
                result.add_error("shortTitle", f"shortTitle exceeds 27 characters ({len(fm['shortTitle'])} chars)",
                               "Shorten to ≤27 characters (GitHub Docs standard)")
        
        # date: YYYY-MM-DD format
        if "date" in fm:
            date_str = str(fm["date"])
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                result.add_error("date", f"Invalid date format: '{date_str}'",
                               "Use YYYY-MM-DD format (e.g., 2025-11-29)")
            else:
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    result.add_error("date", f"Invalid date value: '{date_str}'")
        
        # version: should be semver-ish
        if "version" in fm:
            version_str = str(fm["version"])
            if not re.match(r'^\d+(\.\d+)*$', version_str):
                result.add_warning("version", f"Version '{version_str}' doesn't follow standard format",
                                 "Use format like '1.0' or '1.0.0'")
        
        # estimatedTime format
        if "estimatedTime" in fm:
            time_str = str(fm["estimatedTime"])
            if not re.match(r'^\d+\s*(min|hour|hr|h|m)s?$', time_str, re.IGNORECASE):
                result.add_info("estimatedTime", f"Non-standard time format: '{time_str}'",
                              "Use format like '15 min' or '2 hours'")
    
    def _validate_index_fields(self, fm: Dict, result: ValidationResult):
        """Validate index.md specific fields."""
        
        # children should be present
        if "children" not in fm:
            result.add_warning("children", "index.md missing children array",
                             "Add children array to define navigation order")
        elif not isinstance(fm["children"], list):
            result.add_error("children", "children must be an array of paths")
        
        # layout should be present
        if "layout" not in fm:
            result.add_info("layout", "No layout specified",
                          "Add layout: 'category-landing' for category pages")


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def find_markdown_files(root: Path, folder: Optional[str] = None) -> List[Path]:
    """Find all markdown files in the repository."""
    if folder:
        search_path = root / folder
    else:
        search_path = root
    
    # Exclude certain directories
    exclude_dirs = {'.git', 'node_modules', '__pycache__', 'bin', 'obj', '.venv', 'venv'}
    
    files = []
    for md_file in search_path.rglob('*.md'):
        # Skip excluded directories
        if any(exc in md_file.parts for exc in exclude_dirs):
            continue
        files.append(md_file)
    
    return sorted(files)


def print_result(result: ValidationResult, verbose: bool = False):
    """Print validation result for a single file."""
    
    errors = [i for i in result.issues if i.severity == Severity.ERROR]
    warnings = [i for i in result.issues if i.severity == Severity.WARNING]
    infos = [i for i in result.issues if i.severity == Severity.INFO]
    
    # Check if file was excluded
    is_excluded = any(i.field == "file_type" and "Excluded" in i.message for i in infos)
    
    # Status indicator (using ASCII-safe symbols for Windows compatibility)
    if is_excluded:
        status = "o"
        color = "\033[90m"  # Gray for excluded
    elif result.is_valid and not warnings:
        status = "+"
        color = "\033[92m"  # Green
    elif result.is_valid:
        status = "~"
        color = "\033[93m"  # Yellow (warnings only)
    else:
        status = "x"
        color = "\033[91m"  # Red
    
    reset = "\033[0m"
    
    # Use safe print for Windows
    try:
        print(f"{color}{status}{reset} {result.file_path}")
    except UnicodeEncodeError:
        print(f"{status} {result.file_path}")
    
    if verbose or errors:
        for issue in errors:
            try:
                print(f"  {color}ERROR{reset} [{issue.field}]: {issue.message}")
                if issue.suggestion:
                    print(f"         -> {issue.suggestion}")
            except UnicodeEncodeError:
                print(f"  ERROR [{issue.field}]: {issue.message}")
                if issue.suggestion:
                    print(f"         -> {issue.suggestion}")
    
    if verbose:
        for issue in warnings:
            try:
                print(f"  \033[93mWARN{reset}  [{issue.field}]: {issue.message}")
                if issue.suggestion:
                    print(f"         -> {issue.suggestion}")
            except UnicodeEncodeError:
                print(f"  WARN  [{issue.field}]: {issue.message}")
                if issue.suggestion:
                    print(f"         -> {issue.suggestion}")
        
        for issue in infos:
            try:
                print(f"  \033[94mINFO{reset}  [{issue.field}]: {issue.message}")
            except UnicodeEncodeError:
                print(f"  INFO  [{issue.field}]: {issue.message}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter against the unified schema"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Specific file to validate"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all markdown files in the repository"
    )
    parser.add_argument(
        "--folder",
        help="Validate all files in a specific folder"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all issues including warnings and info"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary statistics only"
    )
    
    args = parser.parse_args()
    
    # Determine repository root
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent.parent  # tools/validators/ -> repo root
    
    # Initialize validator
    validator = FrontmatterValidator(strict=args.strict, repo_root=repo_root)
    
    # Collect files to validate
    if args.file:
        files = [Path(args.file)]
    elif args.all or args.folder:
        files = find_markdown_files(repo_root, args.folder)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Validate files
    results = []
    for file_path in files:
        result = validator.validate_file(file_path)
        results.append(result)
        
        if not args.summary:
            print_result(result, args.verbose)
    
    # Print summary
    total = len(results)
    passed = sum(1 for r in results if r.is_valid)
    failed = total - passed
    
    total_errors = sum(len([i for i in r.issues if i.severity == Severity.ERROR]) for r in results)
    total_warnings = sum(len([i for i in r.issues if i.severity == Severity.WARNING]) for r in results)
    
    print()
    print("=" * 60)
    print(f"SUMMARY: {passed}/{total} files passed")
    print(f"  Errors:   {total_errors}")
    print(f"  Warnings: {total_warnings}")
    print("=" * 60)
    
    # Exit code
    if failed > 0:
        print(f"\n\033[91mValidation FAILED\033[0m - {failed} file(s) have errors")
        sys.exit(1)
    else:
        print(f"\n\033[92mValidation PASSED\033[0m")
        sys.exit(0)


if __name__ == "__main__":
    main()
