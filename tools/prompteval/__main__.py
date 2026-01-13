#!/usr/bin/env python3
"""
PromptEval CLI - Easy, Robust Prompt Evaluation
=================================================

A unified CLI that runs evaluations across multiple models and methods.

Simple Usage:
    prompteval prompts/advanced/              # Evaluate with sensible defaults
    prompteval prompt.md                      # Single file
    prompteval prompts/ --tier 3              # Cross-model validation
    
Multi-Model:
    prompteval prompts/ --models phi4,mistral,gpt-4o-mini
    prompteval prompts/ --all-local           # All local ONNX models
    prompteval prompts/ --all-cloud           # GitHub Models

Output:
    prompteval prompts/ -o results.json       # JSON
    prompteval prompts/ -o report.md          # Markdown
    prompteval prompts/ --ci                  # Exit code for CI/CD
"""

import sys
import io
import json
import argparse
import time
import os
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


# =============================================================================
# WINDOWS CONSOLE ENCODING FIX
# =============================================================================
# Fix emoji/unicode encoding issues on Windows console (cp1252 -> utf-8)
def _is_pytest_running() -> bool:
    """Check if we're running under pytest (avoid breaking capture)."""
    return "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ


def _is_already_wrapped(stream) -> bool:
    """Check if stream is already a TextIOWrapper with UTF-8."""
    return (
        isinstance(stream, io.TextIOWrapper)
        and getattr(stream, 'encoding', '').lower() == 'utf-8'
    )


if sys.platform == "win32" and not _is_pytest_running():
    # Set environment variable for subprocesses
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    # Reconfigure stdout/stderr to use UTF-8
    try:
        if not _is_already_wrapped(sys.stdout):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if not _is_already_wrapped(sys.stderr):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, IOError):
        pass  # Already wrapped or not available


# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================

class JSONParseError(Exception):
    """Raised when JSON parsing fails with the raw response for debugging."""
    def __init__(self, message: str, raw_response: str, model_name: str):
        super().__init__(message)
        self.raw_response = raw_response
        self.model_name = model_name
        self.truncated_response = raw_response[:500] if raw_response else ""


# =============================================================================
# FAILED FILES TRACKING
# =============================================================================

FAILED_FILES_PATH = Path(__file__).parent.parent.parent / "results" / "failed-prompts.json"

def load_failed_files() -> Dict[str, Any]:
    """Load previously failed files for retry."""
    if FAILED_FILES_PATH.exists():
        try:
            with open(FAILED_FILES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"failed": [], "timestamp": None}

def save_failed_files(failed_list: List[Dict[str, Any]]):
    """Save failed files for later retry."""
    FAILED_FILES_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "failed": failed_list,
        "timestamp": datetime.now().isoformat(),
        "count": len(failed_list),
    }
    with open(FAILED_FILES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"\n📁 Saved {len(failed_list)} failed prompt(s) to: {FAILED_FILES_PATH}")

def clear_failed_files():
    """Clear the failed files list after successful retry."""
    if FAILED_FILES_PATH.exists():
        FAILED_FILES_PATH.unlink()


# =============================================================================
# SAFETY DEFAULTS
# =============================================================================

# Safe-by-default provider allowlist.
# NOTE: GitHub Models are remote, but explicitly allowed by default in this repo.
_DEFAULT_ALLOWED_PREFIXES = (
    "local:",
    "gh:",
    "windows-ai:",
    "ollama:",
    "aitk:",
    "ai-toolkit:",
)


def _env_truthy(name: str) -> bool:
    v = (os.getenv(name) or "").strip().lower()
    return v in {"1", "true", "yes", "y", "on"}


def _is_model_allowed(model_full: str, allow_remote: bool) -> bool:
    m = (model_full or "").lower()
    if m.startswith(_DEFAULT_ALLOWED_PREFIXES):
        return True
    return bool(allow_remote)


def _require_model_allowed(model_full: str, allow_remote: bool):
    if _is_model_allowed(model_full, allow_remote):
        return
    raise RuntimeError(
        f"Remote provider disabled by default: '{model_full}'. "
        "Only local:* and gh:* models are allowed unless you opt in. "
        "Re-run with --allow-remote or set PROMPTEVAL_ALLOW_REMOTE=1."
    )


# Add repo root + tools directory to path
# This allows imports like `tools.errors` regardless of current working directory.
TOOLS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = TOOLS_DIR.parent
for p in (str(REPO_ROOT), str(TOOLS_DIR)):
    if p and p not in sys.path:
        sys.path.insert(0, p)

# =============================================================================
# LOGGING
# =============================================================================

# Global counter for unique keys per model per session
_eval_counters = defaultdict(int)

def get_log_path() -> Path:
    """Get the evaluation log file path."""
    log_dir = Path(__file__).parent.parent.parent / "results" / "eval-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "evaluations.jsonl"

def log_evaluation_result(
    date: str,
    origin: str,
    model: str,
    prompt_file: str,
    result: "ModelResult",
):
    """Log evaluation result immediately to file with unique key."""
    # Increment counter for this model
    _eval_counters[model] += 1
    count = _eval_counters[model]
    
    # Generate unique key: date.origin.model.count
    # e.g., 2026-01-04.advanced.deepseek-v3.2.001
    unique_key = f"{date}.{origin}.{model.replace(':', '-')}.{count:03d}"
    
    # Extract priority fixes and summary from improvements
    improvements = result.improvements or {}
    priority_fixes = improvements.get('_priority_fixes', [])
    summary = improvements.get('_summary', '')
    example_improvement = improvements.get('_example_improvement', '')
    
    # Extract per-criterion fixes
    criterion_fixes = {}
    for k, v in improvements.items():
        if k.startswith('_'):
            continue
        if isinstance(v, dict):
            criterion_fixes[k] = {
                'evidence': v.get('evidence', ''),
                'issue': v.get('issue', ''),
                'fix': v.get('fix', ''),
            }
        elif isinstance(v, str):
            criterion_fixes[k] = v
    
    # Create enriched log entry
    log_entry = {
        "key": unique_key,
        "timestamp": datetime.now().isoformat(),
        "date": date,
        "origin": origin,
        "model": model,
        "prompt_file": prompt_file,
        "run": result.run,
        "score": result.score,
        "criteria": result.criteria,
        "improvements": {
            "summary": summary,
            "priority_fixes": priority_fixes,
            "example_improvement": example_improvement,
            "by_criterion": criterion_fixes,
        },
        "duration": result.duration,
        "error": result.error,
    }
    
    # Append to log file (JSON Lines format)
    log_file = get_log_path()
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

# =============================================================================
# MODEL PRESETS
# =============================================================================

# Available local ONNX models (from local_model.py)
LOCAL_ONNX_MODELS = {
    "phi4": "local:phi4mini",
    "phi4mini": "local:phi4mini",
    "phi3": "local:phi3",
    "phi3.5": "local:phi3.5",
    "mistral": "local:mistral",
    "mistral-7b": "local:mistral",
}

# Ollama models (require Ollama server running locally - FREE, FAST)
OLLAMA_MODELS = {
    # Reasoning models (best for evaluation)
    "phi4-reasoning": "ollama:phi4-reasoning",
    "deepseek-r1": "ollama:deepseek-r1:14b",
    "deepseek-r1-14b": "ollama:deepseek-r1:14b",
    "qwen-coder": "ollama:qwen2.5-coder:14b",
    "qwen2.5-coder": "ollama:qwen2.5-coder:14b",
    # General models
    "llama3.3": "ollama:llama3.3",
    "llama3.1": "ollama:llama3.1",
    "qwen2.5": "ollama:qwen2.5",
    "deepseek-v3": "ollama:deepseek-v3",
    "gemma2": "ollama:gemma2",
    "mistral-ollama": "ollama:mistral",
}

# Combined local models (ONNX + Ollama)
LOCAL_MODELS = {**LOCAL_ONNX_MODELS, **OLLAMA_MODELS}

# GitHub Models (require GITHUB_TOKEN)
CLOUD_MODELS = {
    "gpt-4o-mini": "gh:gpt-4o-mini",
    "gpt-4.1": "gh:gpt-4.1",
    "gpt-4o": "gh:gpt-4o",
    "llama-70b": "gh:llama-3.3-70b-instruct",
    "mistral-small": "gh:mistral-small-2503",
    "deepseek-r1-cloud": "gh:deepseek/deepseek-r1",
}

# Tier presets (updated to prefer Ollama models when available)
TIER_CONFIGS = {
    0: {"name": "Structural", "models": [], "runs": 1, "cost": "$0", "time": "<1s"},
    1: {"name": "Local Quick", "models": ["phi4"], "runs": 1, "cost": "$0", "time": "~30s"},
    2: {"name": "Local G-Eval", "models": ["mistral"], "runs": 1, "cost": "$0", "time": "~60s"},
    3: {"name": "Local Cross", "models": ["phi4", "mistral", "phi3.5"], "runs": 2, "cost": "$0", "time": "~5min"},
    4: {"name": "Cloud Quick", "models": ["deepseek-r1"], "runs": 1, "cost": "~$0.01", "time": "~5s"},
    5: {"name": "Cloud Cross", "models": ["gpt-4o-mini", "deepseek-r1", "llama-70b"], "runs": 2, "cost": "~$0.10", "time": "~30s"},
    6: {"name": "Premium", "models": ["phi4", "mistral", "deepseek-r1", "gpt-4.1", "llama-70b"], "runs": 3, "cost": "~$0.30", "time": "~2min"},
    7: {"name": "Enterprise", "models": ["phi4", "mistral", "deepseek-r1", "gpt-4.1", "llama-70b"], "runs": 4, "cost": "~$0.50", "time": "~5min"},
}

# Rubric versioning
RUBRIC_VERSION = "1.0"

# Calibration settings
# Local models tend to score higher than cloud models.
# These offsets can be applied for cross-model comparisons.
CALIBRATION = {
    "enabled": False,  # Set to True to apply calibration
    "offsets": {
        # Negative offset = model scores high, adjust down
        "local:phi4": -5,
        "local:phi4mini": -5,
        "local:phi3.5": -3,
        "local:phi3": -3,
        "local:mistral": -2,
        # Cloud models are the anchor (0 offset)
        "gh:gpt-4o-mini": 0,
        "gh:gpt-4.1": 0,
        "gh:gpt-4o": 0,
        "gh:llama-3.3-70b-instruct": 0,
        "gh:deepseek/deepseek-r1": 0,
    },
    "notes": "Local ONNX models tend to score 3-5 points higher than cloud models. Use triage tier (local) for quick checks, cloud tier for final scores.",
}


# =============================================================================
# RESULT CLASSES
# =============================================================================

@dataclass
class ModelResult:
    """Result from a single model evaluation."""
    model: str
    run: int
    score: float
    criteria: Dict[str, float]
    duration: float
    error: Optional[str] = None
    improvements: Optional[Dict[str, str]] = None  # Suggested improvements per criterion


@dataclass
class PromptResult:
    """Aggregated result for a single prompt across all models."""
    file: str
    title: str
    category: str
    
    # Aggregated scores
    avg_score: float
    min_score: float
    max_score: float
    std_dev: float  # Standard deviation
    variance: float  # Range (max - min) for backward compatibility
    
    # Per-model results
    model_results: List[ModelResult]
    
    # Consensus
    passed: bool
    grade: str
    agreement: float  # % of models that agree on pass/fail
    
    # Stability indicators
    is_stable: bool = True  # True if std_dev < 10
    outlier_count: int = 0  # Runs > 2σ from mean
    
    # Metadata
    threshold: float = 70.0
    rubric_version: str = "1.0"


@dataclass
class EvalRun:
    """Complete evaluation run results."""
    timestamp: str
    tier: int
    tier_name: str
    threshold: float
    models_used: List[str]
    runs_per_model: int
    
    # Summary
    total_prompts: int
    passed: int
    failed: int
    avg_score: float
    
    # Details
    results: List[PromptResult]
    
    # Execution
    duration_seconds: float
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_grade(score: float) -> str:
    """Convert score to grade."""
    if score >= 90: return "Exceptional ⭐⭐⭐⭐⭐"
    if score >= 80: return "Proficient ⭐⭐⭐⭐"
    if score >= 70: return "Competent ⭐⭐⭐"
    if score >= 60: return "Developing ⭐⭐"
    return "Inadequate ⭐"


def find_prompts(path: Path, exclude: List[str] = None) -> List[Path]:
    """Find all prompt files in a path."""
    exclude = exclude or ["README.md", "index.md"]
    
    if path.is_file():
        if path.suffix == ".md":
            return [path]
        if path.suffix == ".yml" or path.suffix == ".yaml":
            # Check if it's a prompt test file (has .prompt.yml or is in evals dir)
            if ".prompt." in path.name or "evals" in str(path):
                return [path]
        return []
    
    prompts = []
    # Find markdown prompts
    for f in sorted(path.rglob("*.md")):
        if any(e in f.name for e in exclude):
            continue
        if "archive" in str(f).lower():
            continue
        prompts.append(f)
    
    # Find YAML prompt tests
    for f in sorted(path.rglob("*.prompt.yml")):
        if any(e in f.name for e in exclude):
            continue
        prompts.append(f)
        
    return prompts


def resolve_model(name: str) -> str:
    """Resolve model shortname to full provider:model format."""
    name = name.lower().strip()
    
    if name in LOCAL_MODELS:
        return LOCAL_MODELS[name]
    if name in CLOUD_MODELS:
        return CLOUD_MODELS[name]
    if ":" in name:
        return name  # Already in provider:model format
    
    # Try prefixing with local:
    return f"local:{name}"


def extract_json_robust(response: str, model_name: str = "unknown") -> Dict[str, Any]:
    """
    Robustly extract JSON from an LLM response with multiple fallback strategies.
    
    Strategies (in order):
    1. Find JSON with proper brace matching
    2. Extract from markdown code blocks
    3. Try to fix truncated JSON by completing braces
    4. Parse raw response
    5. Raise JSONParseError with full context
    
    Args:
        response: Raw LLM response text
        model_name: Name of the model (for error reporting)
        
    Returns:
        Parsed JSON as dict
        
    Raises:
        JSONParseError: If all parsing strategies fail
    """
    import re
    
    if not response or not response.strip():
        raise JSONParseError("Empty response from model", response or "", model_name)
    
    # Strategy 1: Find outermost JSON object with proper brace matching
    try:
        start_idx = response.find('{')
        if start_idx >= 0:
            brace_count = 0
            end_idx = start_idx
            in_string = False
            escape_next = False
            
            for i, char in enumerate(response[start_idx:], start_idx):
                if escape_next:
                    escape_next = False
                    continue
                if char == '\\':
                    escape_next = True
                    continue
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            json_str = response[start_idx:end_idx]
            if json_str:
                data = json.loads(json_str)
                return data
    except json.JSONDecodeError:
        pass  # Try next strategy
    
    # Strategy 2: Look for JSON in markdown code blocks
    code_patterns = [
        r'```json\s*\n?([\s\S]*?)\n?```',
        r'```\s*\n?([\s\S]*?)\n?```',
    ]
    for pattern in code_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            try:
                json_str = match.group(1).strip()
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError:
                pass
    
    # Strategy 3: Try to fix truncated JSON (incomplete due to token limits)
    try:
        start_idx = response.find('{')
        if start_idx >= 0:
            json_candidate = response[start_idx:]
            
            # Count open braces and brackets
            open_braces = json_candidate.count('{') - json_candidate.count('}')
            open_brackets = json_candidate.count('[') - json_candidate.count(']')
            
            # Try completing truncated JSON
            if open_braces > 0 or open_brackets > 0:
                # Remove trailing incomplete values (after last complete key-value)
                # Look for patterns like ',"key": ' at the end (incomplete)
                truncated = re.sub(r',\s*"[^"]*"\s*:\s*[^,}\]]*$', '', json_candidate)
                truncated = re.sub(r',\s*"[^"]*"\s*:\s*\{[^}]*$', '', truncated)
                truncated = re.sub(r',\s*"[^"]*"\s*$', '', truncated)
                
                # Close remaining braces/brackets
                completion = ']' * open_brackets + '}' * open_braces
                repaired = truncated.rstrip() + completion
                
                try:
                    data = json.loads(repaired)
                    print(f"    ⚠️  Repaired truncated JSON from {model_name}")
                    return data
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    
    # Strategy 4: Simple raw parse
    try:
        data = json.loads(response.strip())
        return data
    except json.JSONDecodeError:
        pass
    
    # Strategy 5: All strategies failed - raise descriptive error
    raise JSONParseError(
        f"All JSON extraction strategies failed for {model_name}",
        response,
        model_name
    )


def _model_is_usable(model_name: str, inventory: Dict[str, Any]) -> bool:
    """Best-effort determination of whether a requested model is usable."""
    try:
        resolved = resolve_model(model_name)
    except Exception:
        resolved = model_name

    providers = inventory.get("providers", {}) if isinstance(inventory, dict) else {}

    def _p(name: str) -> Dict[str, Any]:
        v = providers.get(name, {})
        return v if isinstance(v, dict) else {}

    if resolved.startswith("gh:"):
        return bool(_p("github_models").get("can_attempt"))
    if resolved.startswith("azure-foundry:"):
        return bool(_p("azure_foundry").get("configured"))
    if resolved.startswith("azure-openai:"):
        return bool(_p("azure_openai").get("configured"))
    if resolved.startswith("ollama:"):
        oll = _p("ollama")
        # If we didn't actively probe, reachable may be None.
        return bool(oll.get("configured", True)) and oll.get("reachable") is not False
    if resolved.startswith("openai:") or ("gpt" in resolved and not resolved.startswith("gh:")):
        return bool(_p("openai").get("configured"))
    if resolved.startswith("gemini:") or "gemini" in resolved:
        return bool(_p("gemini").get("configured"))
    if resolved.startswith("claude:") or "claude" in resolved:
        return bool(_p("claude").get("configured"))
    if resolved.startswith("aitk:") or resolved.startswith("ai-toolkit:"):
        # AI Toolkit models are local ONNX models, always attempt if installed
        return True

    # local:* and everything else: let the evaluator attempt it.
    return True


# =============================================================================
# EVALUATORS
# =============================================================================

def evaluate_structural(file_path: Path) -> Dict[str, Any]:
    """Fast structural analysis without LLM."""
    import yaml
    
    # Handle YAML files
    if file_path.suffix.lower() in ['.yml', '.yaml'] or file_path.name.endswith('.prompt.yml'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            scores = {}
            # 1. Structure (40%)
            required = ["testData", "messages"]
            present = sum(1 for f in required if f in data)
            scores["structure"] = (present / len(required)) * 100
            
            # 2. Test Data (30%)
            test_data = data.get("testData", [])
            scores["test_data"] = 100 if len(test_data) > 0 else 0
            
            # 3. Messages (30%)
            messages = data.get("messages", [])
            scores["messages"] = 100 if len(messages) > 0 else 0
            
            overall = sum(s * w for s, w in zip(scores.values(), [0.4, 0.3, 0.3]))
            
            return {
                "score": round(overall, 1),
                "criteria": scores,
                "title": data.get("description", file_path.stem),
                "category": "evaluation",
            }
        except:
            return {
                "score": 0,
                "criteria": {"error": 0},
                "title": file_path.stem,
                "category": "error",
            }

    content = file_path.read_text(encoding="utf-8")
    content_stripped = content.lstrip()
    
    # Parse frontmatter
    frontmatter = {}
    if content_stripped.startswith("---"):
        try:
            end = content_stripped.find("---", 3)
            if end > 0:
                frontmatter = yaml.safe_load(content_stripped[3:end]) or {}
        except:
            pass
    
    body = content_stripped.lower()
    
    # Score components
    scores = {}
    
    # 1. Frontmatter (25%)
    # Align with reference/frontmatter-schema.md
    required = ["title", "intro", "type"]
    present = sum(1 for f in required if f in frontmatter)
    scores["frontmatter"] = (present / len(required)) * 100
    
    # 2. Sections (25%)
    # Keep Tier 0 lightweight: these are the most common prompt sections.
    sections = ["description", "prompt", "variables", "example"]
    found = sum(1 for s in sections if f"## {s}" in body or f"# {s}" in body)
    scores["sections"] = (found / len(sections)) * 100
    
    # 3. Examples (20%)
    scores["examples"] = 100 if "```" in content else 50
    
    # 4. Documentation (15%)
    scores["docs"] = 100 if len(content) > 500 else 60
    
    # 5. Governance (15%)
    scores["governance"] = 100 if frontmatter.get("governance_tags") else 60
    
    overall = sum(s * w for s, w in zip(scores.values(), [0.25, 0.25, 0.20, 0.15, 0.15]))
    
    return {
        "score": round(overall, 1),
        "criteria": scores,
        "title": frontmatter.get("title", file_path.stem),
        "category": frontmatter.get("type", "unknown"),
    }


def evaluate_yaml_prompt(file_path: Path, model_full: str, run_num: int, start_time: float) -> ModelResult:
    """Evaluate a `.prompt.yml` file.

    Supports two modes:
      1) GitHub Models-style `evaluators:` (string checks) when present.
      2) Legacy "JSON scoring" mode (ask the model to return numeric JSON) when no evaluators exist.

    The goal is to avoid brittle parsing and provide honest failures.
    """

    def _substitute(template: str, variables: Dict[str, Any]) -> str:
        # Support {{var}} and {{ var }} (common in YAML templates).
        import re

        def repl(match: re.Match) -> str:
            key = match.group(1).strip()
            return str(variables.get(key, match.group(0)))

        return re.sub(r"\{\{\s*([^}]+?)\s*\}\}", repl, template)

    def _extract_json_dict(text: str) -> Optional[Dict[str, Any]]:
        """Best-effort extraction of a JSON object from model output."""
        import re

        if not isinstance(text, str):
            return None

        s = text.strip()
        # Strip fenced code blocks.
        m = re.search(r"```json\s*([\s\S]*?)\s*```", s, re.IGNORECASE)
        if m:
            s = m.group(1).strip()
        else:
            m = re.search(r"```\s*([\s\S]*?)\s*```", s)
            if m:
                s = m.group(1).strip()

        # Find the outermost JSON object.
        first = s.find("{")
        last = s.rfind("}")
        if first == -1 or last <= first:
            return None

        candidate = s[first:last + 1]
        # Small cleanup attempts.
        attempts = [
            candidate,
            re.sub(r",\s*([}\]])", r"\1", candidate),  # trailing commas
            candidate.replace("'", '"'),
        ]
        for c in attempts:
            try:
                obj = json.loads(c)
                return obj if isinstance(obj, dict) else None
            except Exception:
                continue
        return None

    def _eval_string_rule(text: str, rule: Dict[str, Any]) -> bool:
        import re

        if not isinstance(text, str):
            text = str(text)

        if not isinstance(rule, dict):
            return False

        # Common GitHub Models evaluator operators.
        if "contains" in rule:
            return str(rule["contains"]) in text
        if "notContains" in rule:
            return str(rule["notContains"]) not in text
        if "startsWith" in rule:
            return text.startswith(str(rule["startsWith"]))
        if "endsWith" in rule:
            return text.endswith(str(rule["endsWith"]))
        if "equals" in rule:
            return text.strip() == str(rule["equals"]).strip()
        if "regex" in rule:
            try:
                return re.search(str(rule["regex"]), text) is not None
            except re.error:
                return False
        return False

    def _score_from_evaluators(response_text: str, evaluators: List[Dict[str, Any]]) -> (float, Dict[str, float]):
        if not evaluators:
            return 0.0, {}
        passed = 0
        per_eval: Dict[str, float] = {}
        for ev in evaluators:
            name = ev.get("name") or "unnamed"
            rule = ev.get("string")
            ok = _eval_string_rule(response_text, rule)
            per_eval[name] = 100.0 if ok else 0.0
            passed += 1 if ok else 0
        return (passed / len(evaluators)) * 100.0, per_eval

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return ModelResult(
            model=model_full,
            run=run_num,
            score=0,
            criteria={},
            duration=round(time.time() - start_time, 1),
            error=f"YAML Error: {str(e)}",
        )

    test_data = data.get("testData", [])
    messages_template = data.get("messages", [])
    evaluators = data.get("evaluators") or []
    model_params = data.get("modelParameters") or {}

    if not test_data or not messages_template:
        return ModelResult(
            model=model_full,
            run=run_num,
            score=0,
            criteria={},
            duration=round(time.time() - start_time, 1),
            error="Missing testData or messages in YAML",
        )

    from llm_client import LLMClient

    total_score = 0.0
    case_count = 0
    aggregated_criteria: Dict[str, float] = {}
    errors: List[str] = []

    # Use optional modelParameters when present (best-effort; not all providers support these).
    temperature = float(model_params.get("temperature", 0.3)) if isinstance(model_params, dict) else 0.3
    max_tokens = int(model_params.get("max_tokens", 500)) if isinstance(model_params, dict) else 500

    for item in test_data:
        if not isinstance(item, dict):
            continue

        system_instruction: Optional[str] = None
        turns: List[str] = []
        non_system_contents: List[str] = []

        for msg in messages_template:
            if not isinstance(msg, dict):
                continue
            role = str(msg.get("role", "user")).lower()
            content = str(msg.get("content", ""))
            content = _substitute(content, item)

            if role == "system":
                system_instruction = content
                continue

            non_system_contents.append(content)
            # Preserve roles for multi-turn templates.
            turns.append(f"{role.capitalize()}: {content}")

        # If there's only one non-system message, don't add "User:" prefix.
        if len(non_system_contents) == 1:
            full_prompt = non_system_contents[0]
        else:
            full_prompt = "\n\n".join(turns)

        try:
            response_text = LLMClient.generate_text(
                model_full,
                full_prompt,
                system_instruction=system_instruction,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            errors.append(str(e))
            # Honest failure: this test case contributes 0.
            case_count += 1
            continue

        if isinstance(response_text, str) and response_text.strip().lower().startswith("error calling"):
            errors.append(response_text.strip()[:200])
            case_count += 1
            continue

        # Mode 1: evaluators (string checks)
        if evaluators:
            score, per_eval = _score_from_evaluators(response_text, evaluators)
            total_score += score
            case_count += 1
            for k, v in per_eval.items():
                aggregated_criteria[k] = aggregated_criteria.get(k, 0.0) + v
            continue

        # Mode 2: legacy JSON scoring
        obj = _extract_json_dict(response_text)
        if not obj:
            errors.append("Non-JSON model response")
            case_count += 1
            continue

        overall = obj.get("overall")
        if overall is None:
            nums = [v for v in obj.values() if isinstance(v, (int, float))]
            overall = (sum(nums) / len(nums)) if nums else 0

        try:
            overall_f = float(overall)
        except Exception:
            overall_f = 0.0

        # Normalize 1-10 to 0-100 if it looks like a 1-10 rubric.
        normalized = (overall_f - 1.0) / 9.0 * 100.0 if 0 < overall_f <= 10 else overall_f
        normalized = max(0.0, min(100.0, normalized))

        total_score += normalized
        case_count += 1

        for k, v in obj.items():
            if k == "overall":
                continue
            if isinstance(v, (int, float)):
                vv = float(v)
                vv = (vv - 1.0) / 9.0 * 100.0 if 0 < vv <= 10 else vv
                aggregated_criteria[k] = aggregated_criteria.get(k, 0.0) + vv

    if case_count == 0:
        return ModelResult(
            model=model_full,
            run=run_num,
            score=0,
            criteria={},
            duration=round(time.time() - start_time, 1),
            error="No test cases executed (empty testData?)",
        )

    avg_score = total_score / case_count
    avg_criteria = {k: (v / case_count) for k, v in aggregated_criteria.items()}

    err = None
    if errors and avg_score == 0:
        err = errors[0]
    elif errors:
        # Non-fatal issues happened; keep a short note for visibility.
        err = f"{len(errors)}/{case_count} test case(s) had errors"

    return ModelResult(
        model=model_full,
        run=run_num,
        score=round(avg_score, 1),
        criteria={k: round(v, 1) for k, v in avg_criteria.items()},
        duration=round(time.time() - start_time, 1),
        error=err,
    )


def evaluate_with_model(
    file_path: Path,
    model_name: str,
    run_num: int = 1,
    max_retries: int = 2,
    allow_remote: bool = False,
) -> ModelResult:
    """
    Evaluate a prompt with a specific model.
    
    Includes retry logic with exponential backoff for transient errors.
    """
    start = time.time()
    
    # Import error classification from canonical source
    try:
        from tools.errors import classify_error, ErrorCode
    except ImportError:
        # Fallback if errors module not available
        def classify_error(msg, rc=None):
            return ("internal_error", False)
        # No error code registry available; continue without it.
    
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            model_full = resolve_model(model_name)
            _require_model_allowed(model_full, allow_remote)
            
            # Check for YAML evaluation
            if file_path.suffix.lower() in ['.yml', '.yaml'] or file_path.name.endswith('.prompt.yml'):
                return evaluate_yaml_prompt(file_path, model_full, run_num, start)
            
            if model_full.startswith("local:"):
                # Use local_model.py (no retries needed for local)
                from local_model import LocalModel

                content = file_path.read_text(encoding="utf-8")
                model_key = model_full.split(":", 1)[1] if ":" in model_full else None
                model = LocalModel(model_key=model_key, verbose=False)
                result = model.evaluate_prompt_geval(content)
                
                # Parse result
                overall = result.get("overall", 0)
                scores = result.get("scores", {})
                
                # Normalize 1-10 to 0-100
                normalized = (overall - 1) / 9 * 100 if overall > 0 else 0
                criteria = {k: (v - 1) / 9 * 100 for k, v in scores.items()}
                
                return ModelResult(
                    model=model_name,
                    run=run_num,
                    score=round(normalized, 1),
                    criteria=criteria,
                    duration=round(time.time() - start, 1),
                )
            
            else:
                # Use llm_client for anything non-local (gh:, openai:, gemini:, claude:, azure-*)
                from llm_client import LLMClient

                content = file_path.read_text(encoding="utf-8")

                # Enhanced G-Eval prompt with detailed rubric and actionable feedback
                eval_prompt = f"""You are an expert prompt engineer evaluating prompt templates.

PROMPT TO EVALUATE:
---
{content[:4000]}
---

## EVALUATION RUBRIC (Score 1-10 for each)

### 1. CLARITY (Weight: 25%)
Assess how clear, unambiguous, and understandable the prompt is.
- 9-10: Crystal clear purpose, zero ambiguity, perfect structure, self-explanatory variables
- 7-8: Clear purpose, minimal ambiguity, good structure, mostly clear variables
- 5-6: Understandable but some interpretation needed, decent structure
- 3-4: Confusing in places, unclear variables, needs improvement
- 1-2: Very difficult to understand, major rewrites needed

### 2. EFFECTIVENESS (Weight: 30%)
Assess how well this prompt will produce quality outputs consistently.
- 9-10: Will produce excellent results 95%+ of time, handles edge cases, works across platforms
- 7-8: Good results 85%+ of time, decent edge case handling
- 5-6: Acceptable results 70%+ of time, some inconsistency
- 3-4: Mixed results 50-70%, often unpredictable
- 1-2: Frequently fails or produces poor results

### 3. STRUCTURE (Weight: 20%)
Assess the prompt's organization, formatting, and professional quality.
- 9-10: Perfect markdown, clear sections, excellent use of headers/lists, professional
- 7-8: Good formatting, well-organized sections, minor improvements possible
- 5-6: Adequate structure but could be better organized
- 3-4: Poorly organized, inconsistent formatting
- 1-2: No structure, wall of text, unprofessional

### 4. SPECIFICITY (Weight: 15%)
Assess how specific and actionable the instructions are.
- 9-10: Highly specific instructions, clear success criteria, defined constraints
- 7-8: Good specificity, reasonable constraints, clear expectations
- 5-6: Somewhat vague, could be more specific
- 3-4: Too vague or too restrictive, unclear expectations
- 1-2: Extremely vague or unusable constraints

### 5. COMPLETENESS (Weight: 10%)
Assess whether the prompt has all necessary components.
- 9-10: Has context, instructions, examples, output format, error handling guidance
- 7-8: Has most key elements, minor additions needed
- 5-6: Missing some important elements
- 3-4: Missing multiple key components
- 1-2: Severely incomplete, missing critical information

## REQUIRED OUTPUT

Provide a detailed JSON response with:
1. Scores for each criterion (1-10)
2. Specific evidence/quotes from the prompt supporting each score
3. Actionable improvements with EXAMPLE rewrites for any score below 8
4. Overall assessment and priority fixes

{{
  "clarity": {{
    "score": N,
    "evidence": "specific quote or observation from prompt",
    "issue": "what's wrong (if score < 8)",
    "fix": "specific rewrite or addition to improve this"
  }},
  "effectiveness": {{
    "score": N,
    "evidence": "specific observation",
    "issue": "what's wrong (if score < 8)",
    "fix": "specific improvement suggestion"
  }},
  "structure": {{
    "score": N,
    "evidence": "specific observation",
    "issue": "what's wrong (if score < 8)",
    "fix": "specific improvement suggestion"
  }},
  "specificity": {{
    "score": N,
    "evidence": "specific observation",
    "issue": "what's wrong (if score < 8)",
    "fix": "specific improvement suggestion"
  }},
  "completeness": {{
    "score": N,
    "evidence": "specific observation",
    "issue": "what's wrong (if score < 8)",
    "fix": "specific improvement suggestion"
  }},
  "overall": N,
  "weighted_score": N,
  "summary": "one sentence overall assessment",
  "priority_fixes": ["most important fix first", "second priority", "third priority"],
  "example_improvement": "show a specific rewrite of the weakest section"
}}
"""

                # Check cache first
                response = None
                try:
                    from response_cache import get_cache
                    cache = get_cache()
                    if cache.enabled:
                        cached_response = cache.get(content, model_full, eval_prompt[:500])
                        if cached_response:
                            response = cached_response
                except ImportError:
                    pass  # Cache not available
                
                # Make LLM call if not cached
                if response is None:
                    response = LLMClient.generate_text(model_full, eval_prompt, max_tokens=2000)
                    
                    # Store in cache
                    try:
                        from response_cache import get_cache
                        cache = get_cache()
                        if cache.enabled:
                            cache.set(content, model_full, eval_prompt[:500], response)
                    except ImportError:
                        pass

                # Parse response using robust JSON extraction
                try:
                    data = extract_json_robust(response, model_name)
                except JSONParseError as e:
                    # Log the parsing failure with context
                    print(f"\n    ⚠️  JSON Parse Error from {model_name}")
                    print(f"    Error: {str(e)}")
                    print(f"    Response preview (first 300 chars):")
                    print(f"    {e.truncated_response[:300]}")
                    print(f"    ---")
                    
                    # Re-raise to be caught by outer exception handler
                    raise
                
                if data:
                    # Extract scores from nested or flat structure
                    criteria = {}
                    improvements = {}
                    
                    for key in ['clarity', 'effectiveness', 'structure', 'specificity', 'completeness']:
                        val = data.get(key)
                        if isinstance(val, dict):
                            # Nested structure with detailed feedback
                            score = val.get('score', 5)
                            criteria[key] = (score - 1) / 9 * 100
                            # Combine issue and fix into improvement
                            if val.get('issue') or val.get('fix'):
                                improvements[key] = {
                                    'evidence': val.get('evidence', ''),
                                    'issue': val.get('issue', ''),
                                    'fix': val.get('fix', ''),
                                }
                        elif isinstance(val, (int, float)):
                            # Flat structure (backward compat)
                            criteria[key] = (val - 1) / 9 * 100
                    
                    # Extract additional high-value fields
                    summary = data.get('summary', '')
                    priority_fixes = data.get('priority_fixes', [])
                    example_improvement = data.get('example_improvement', '')
                    
                    # Add to improvements dict
                    if summary:
                        improvements['_summary'] = summary
                    if priority_fixes:
                        improvements['_priority_fixes'] = priority_fixes
                    if example_improvement:
                        improvements['_example_improvement'] = example_improvement
                    
                    overall = data.get("overall", data.get("weighted_score", 5))
                    normalized = (overall - 1) / 9 * 100 if overall else 50

                return ModelResult(
                    model=model_name,
                    run=run_num,
                    score=round(normalized, 1),
                    criteria=criteria,
                    improvements=improvements if improvements else None,
                    duration=round(time.time() - start, 1),
                )
        
        except Exception as e:
            last_error = str(e)
            error_code, should_retry = classify_error(last_error)
            
            # Only retry transient errors
            if should_retry and attempt < max_retries:
                # Exponential backoff with jitter
                import random
                delay = min(1.0 * (2 ** attempt), 30.0) * (0.8 + random.random() * 0.4)
                time.sleep(delay)
                continue
            
            # Return error result
            return ModelResult(
                model=model_name,
                run=run_num,
                score=0,
                criteria={},
                duration=round(time.time() - start, 1),
                error=f"{error_code.value if hasattr(error_code, 'value') else error_code}: {last_error}",
            )
    
    # Should not reach here
    return ModelResult(
        model=model_name,
        run=run_num,
        score=0,
        criteria={},
        duration=round(time.time() - start, 1),
        error=last_error,
    )


# =============================================================================
# SINGLE PROMPT EVALUATOR (for parallel execution)
# =============================================================================

# Thread-safe lock for console output
_print_lock = threading.Lock()


def _evaluate_single_prompt(
    prompt_path: Path,
    prompt_index: int,
    total_prompts: int,
    tier: int,
    models: List[str],
    runs: int,
    threshold: float,
    allow_remote: bool,
    delay: float,
    verbose: bool,
) -> Tuple[PromptResult, Optional[Dict]]:
    """
    Evaluate a single prompt file (thread-safe).
    
    Returns:
        Tuple of (PromptResult, optional failure dict for --retry-failed)
    """
    with _print_lock:
        if verbose:
            print(f"[{prompt_index}/{total_prompts}] {prompt_path.name}")
    
    # Structural analysis first
    structural = evaluate_structural(prompt_path)
    
    model_results = []
    
    if tier == 0 or not models:
        # Structural only
        model_results.append(ModelResult(
            model="structural",
            run=1,
            score=structural["score"],
            criteria=structural["criteria"],
            duration=0,
        ))
    else:
        # Run each model
        eval_count = 0
        for model in models:
            for run in range(1, runs + 1):
                # Add delay between evaluations to avoid rate limiting
                if delay > 0 and eval_count > 0:
                    time.sleep(delay)
                eval_count += 1
                
                with _print_lock:
                    if verbose:
                        print(f"  > {model} (run {run}/{runs})", end=" ", flush=True)
                
                try:
                    result = evaluate_with_model(prompt_path, model, run, allow_remote=allow_remote)
                    model_results.append(result)
                    
                except JSONParseError as e:
                    # Continue with error result
                    result = ModelResult(
                        model=model,
                        run=run,
                        score=0,
                        criteria={},
                        duration=0,
                        error=f"JSONParseError: {str(e)[:100]}",
                    )
                    model_results.append(result)
                
                # Log result immediately to file
                date_str = datetime.now().strftime("%Y-%m-%d")
                origin = prompt_path.parent.name  # e.g., "advanced", "business"
                log_evaluation_result(date_str, origin, model, prompt_path.name, result)
                
                with _print_lock:
                    if verbose:
                        if result.error:
                            print(f"❌ {result.error[:30]}")
                        else:
                            print(f"✓ {result.score:.0f}%")
                            # Show per-criterion breakdown if available
                            if result.criteria:
                                weak_criteria = [(k, v) for k, v in result.criteria.items() if v < 70]
                                if weak_criteria:
                                    print(f"    ⚠️  Weak: {', '.join(f'{k}={v:.0f}%' for k, v in weak_criteria)}")
    
    # Aggregate results with proper statistics
    valid_scores = [r.score for r in model_results if not r.error and r.score > 0]
    
    if valid_scores:
        n = len(valid_scores)
        avg_score = sum(valid_scores) / n
        min_score = min(valid_scores)
        max_score = max(valid_scores)
        variance = max_score - min_score  # Range for backward compat
        
        # Standard deviation
        if n > 1:
            sum_sq_diff = sum((x - avg_score) ** 2 for x in valid_scores)
            std_dev = (sum_sq_diff / (n - 1)) ** 0.5  # Sample std dev
        else:
            std_dev = 0.0
        
        # Stability: stable if std_dev < 10 points
        is_stable = std_dev < 10.0
        
        # Outlier detection: count scores > 2σ from mean
        if std_dev > 0:
            outlier_count = sum(1 for s in valid_scores if abs(s - avg_score) > 2 * std_dev)
        else:
            outlier_count = 0
        
        passed = avg_score >= threshold
        passes = sum(1 for s in valid_scores if s >= threshold)
        agreement = passes / n * 100
    else:
        avg_score = structural["score"]
        min_score = max_score = avg_score
        variance = 0
        std_dev = 0.0
        is_stable = True
        outlier_count = 0
        passed = avg_score >= threshold
        agreement = 100
    
    prompt_result = PromptResult(
        file=str(prompt_path),
        title=structural["title"],
        category=structural["category"],
        avg_score=round(avg_score, 1),
        min_score=round(min_score, 1),
        max_score=round(max_score, 1),
        std_dev=round(std_dev, 2),
        variance=round(variance, 1),
        model_results=model_results,
        passed=passed,
        grade=get_grade(avg_score),
        agreement=round(agreement, 1),
        is_stable=is_stable,
        outlier_count=outlier_count,
        threshold=threshold,
        rubric_version=RUBRIC_VERSION,
    )
    
    # Track failures for --retry-failed
    failure_info = None
    if not passed:
        failure_info = {
            "file": str(prompt_path),
            "score": avg_score,
            "threshold": threshold,
            "models": [m.model for m in model_results],
            "timestamp": datetime.now().isoformat(),
        }
    
    with _print_lock:
        if verbose:
            status = "PASS" if passed else "FAIL"
            stability = "stable" if is_stable else f"UNSTABLE (sd={std_dev:.1f})"
            print(f"  {status} -> {avg_score:.1f}% +/-{std_dev:.1f} ({stability})\n")
    
    return prompt_result, failure_info


# =============================================================================
# MAIN EVALUATOR
# =============================================================================

def run_evaluation(
    path: Path,
    tier: int = 2,
    threshold: float = 70.0,
    models: List[str] = None,
    runs: int = None,
    parallel: int = 1,
    verbose: bool = False,
    skip_probe: bool = False,
    allow_remote: bool = False,
    delay: float = 0.0,
    fail_fast: bool = False,
    retry_failed: bool = False,
) -> EvalRun:
    """
    Run a complete evaluation.
    
    Args:
        path: File or directory to evaluate
        tier: Evaluation tier (0-7) - sets default models/runs
        threshold: Pass/fail threshold
        models: Override models to use
        runs: Override runs per model
        parallel: Number of parallel evaluations
        verbose: Print progress
        skip_probe: Skip model availability probing
        delay: Seconds to wait between evaluations (prevents rate limiting)
    """
    start_time = time.time()
    
    # Get tier config
    tier_config = TIER_CONFIGS.get(tier, TIER_CONFIGS[2])
    requested_models = models or tier_config["models"]
    runs = runs or tier_config["runs"]
    
    # Auto-discover Ollama models and add to LOCAL_MODELS if available
    try:
        import urllib.request
        import urllib.error
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        req = urllib.request.Request(
            f"{ollama_host}/api/tags",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            ollama_models = []
            for m in data.get("models", []):
                full_name = m.get("name", "")
                if not full_name:
                    continue
                # Keep full name with tag (e.g., deepseek-v3.2:cloud)
                # Also create a short alias without tag for convenience
                short_name = full_name.split(":")[0]
                ollama_models.append(full_name)
                
                # Add both full name and short name to LOCAL_MODELS
                if full_name not in LOCAL_MODELS:
                    LOCAL_MODELS[full_name] = f"ollama:{full_name}"
                if short_name not in LOCAL_MODELS:
                    LOCAL_MODELS[short_name] = f"ollama:{full_name}"  # Short name points to full name
            
            if verbose and ollama_models:
                print(f"🦙 Discovered {len(ollama_models)} Ollama models: {', '.join(ollama_models[:5])}")
    except:
        pass  # Ollama not running, continue with ONNX models
    
    # Probe models for availability (Phase 2 reliability)
    skipped_models = []
    if requested_models and not skip_probe:
        try:
            from model_probe import ModelProbe
            probe = ModelProbe(verbose=verbose)
            
            # Resolve model names and probe
            resolved_models = []
            for m in requested_models:
                resolved = resolve_model(m)
                # Enforce safe defaults early so we don't probe disallowed providers.
                if not _is_model_allowed(resolved, allow_remote):
                    skipped_models.append({
                        "model": m,
                        "resolved": resolved,
                        "error_code": "remote_disabled",
                        "error": "Remote provider disabled by default",
                    })
                    if verbose:
                        print(f"⚠️  Skipping {m}: remote providers disabled")
                    continue
                result = probe.check_model(resolved)
                if result.usable:
                    resolved_models.append(m)
                else:
                    skipped_models.append({
                        "model": m,
                        "resolved": resolved,
                        "error_code": result.error_code,
                        "error": result.error_message,
                    })
                    if verbose:
                        print(f"⚠️  Skipping {m}: {result.error_code} - {result.error_message[:50] if result.error_message else 'unavailable'}")
            
            models = resolved_models
        except ImportError:
            # model_probe not available, proceed without probing
            # model_probe not available, proceed (but still enforce safe default allowlist)
            models = [m for m in requested_models if _is_model_allowed(resolve_model(m), allow_remote)]
    else:
        models = [m for m in requested_models if _is_model_allowed(resolve_model(m), allow_remote)]
    
    # Find prompts
    prompts = find_prompts(path)
    if not prompts:
        print(f"No prompts found in: {path}")
        return None
    
    # Handle --retry-failed mode
    if retry_failed:
        failed_data = load_failed_files()
        if not failed_data.get("failed"):
            print("No previously failed prompts found. Run a normal evaluation first.")
            return None
        
        failed_paths = [Path(f["file"]) for f in failed_data["failed"]]
        prompts = [p for p in prompts if p in failed_paths]
        
        if not prompts:
            print("None of the previously failed prompts were found in the current path.")
            return None
        
        print(f"\n🔄 Retry mode: Evaluating {len(prompts)} previously failed prompt(s)")
        print(f"Last failure timestamp: {failed_data.get('timestamp', 'unknown')}")
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"PromptEval - Tier {tier}: {tier_config['name']}")
        print(f"{'='*60}")
        print(f"Path: {path}")
        print(f"Prompts: {len(prompts)}")
        print(f"Models: {', '.join(models) if models else 'Structural only'}")
        if skipped_models:
            print(f"Skipped: {len(skipped_models)} unavailable model(s)")
        print(f"Runs per model: {runs}")
        print(f"Est. cost: {tier_config['cost']}")
        if fail_fast:
            print(f"Mode: Fail-fast (stop on first error)")
        if retry_failed:
            print(f"Mode: Retry failed prompts only")
        if parallel > 1:
            print(f"Mode: Parallel evaluation ({parallel} workers)")
        print(f"{'='*60}\n")
    
    results = []
    failed_list = []  # Track failed prompts for saving
    
    # Choose sequential or parallel execution
    if parallel > 1 and len(prompts) > 1 and not fail_fast:
        # Parallel execution using ThreadPoolExecutor
        # Note: fail_fast is incompatible with parallel mode
        if verbose:
            print(f"🚀 Starting parallel evaluation with {parallel} workers...\n")
        
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            # Submit all tasks
            future_to_prompt = {
                executor.submit(
                    _evaluate_single_prompt,
                    prompt_path=prompt_path,
                    prompt_index=i,
                    total_prompts=len(prompts),
                    tier=tier,
                    models=models,
                    runs=runs,
                    threshold=threshold,
                    allow_remote=allow_remote,
                    delay=delay,
                    verbose=verbose,
                ): prompt_path
                for i, prompt_path in enumerate(prompts, 1)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_prompt):
                prompt_path = future_to_prompt[future]
                try:
                    prompt_result, failure_info = future.result()
                    results.append(prompt_result)
                    if failure_info:
                        failed_list.append(failure_info)
                except Exception as e:
                    # Handle unexpected errors
                    with _print_lock:
                        print(f"❌ Error evaluating {prompt_path.name}: {e}")
                    # Create a failed result
                    results.append(PromptResult(
                        file=str(prompt_path),
                        title=prompt_path.stem,
                        category="unknown",
                        avg_score=0,
                        min_score=0,
                        max_score=0,
                        std_dev=0,
                        variance=0,
                        model_results=[],
                        passed=False,
                        grade="F",
                        agreement=0,
                        is_stable=False,
                        outlier_count=0,
                        threshold=threshold,
                        rubric_version=RUBRIC_VERSION,
                    ))
                    failed_list.append({
                        "file": str(prompt_path),
                        "error": str(e),
                        "timestamp": datetime.now().isoformat(),
                    })
    else:
        # Sequential execution (original behavior, supports fail-fast)
        for i, prompt_path in enumerate(prompts, 1):
            if verbose:
                print(f"[{i}/{len(prompts)}] {prompt_path.name}")
            
            # Structural analysis first
            structural = evaluate_structural(prompt_path)
            
            model_results = []
            
            if tier == 0 or not models:
                # Structural only
                model_results.append(ModelResult(
                    model="structural",
                    run=1,
                    score=structural["score"],
                    criteria=structural["criteria"],
                    duration=0,
                ))
            else:
                # Run each model
                eval_count = 0
                for model in models:
                    for run in range(1, runs + 1):
                        # Add delay between evaluations to avoid rate limiting
                        if delay > 0 and eval_count > 0:
                            time.sleep(delay)
                        eval_count += 1
                        
                        if verbose:
                            print(f"  > {model} (run {run}/{runs})", end=" ", flush=True)
                        
                        try:
                            result = evaluate_with_model(prompt_path, model, run, allow_remote=allow_remote)
                            model_results.append(result)
                            
                            # Check for JSON parse errors (raised as exceptions now)
                            if result.error and "JSONParseError" in result.error:
                                if fail_fast:
                                    print(f"\n\n🛑 FAIL-FAST: JSON parsing failed for {prompt_path.name}")
                                    print(f"   Error: {result.error}")
                                    print(f"\n   Stopping evaluation. Fix the issue and retry with --retry-failed")
                                    
                                    # Save this failed prompt
                                    failed_list.append({
                                        "file": str(prompt_path),
                                        "model": model,
                                        "error": result.error,
                                        "timestamp": datetime.now().isoformat(),
                                    })
                                    save_failed_files(failed_list)
                                    raise SystemExit(1)
                        
                        except JSONParseError as e:
                            # JSON parsing failed completely
                            if fail_fast:
                                print(f"\n\n🛑 FAIL-FAST: JSON parsing failed for {prompt_path.name}")
                                print(f"   Model: {model}")
                                print(f"   Error: {str(e)}")
                                print(f"   Response preview: {e.truncated_response[:200]}...")
                                print(f"\n   Stopping evaluation. Fix the issue and retry with --retry-failed")
                                
                                # Save this failed prompt
                                failed_list.append({
                                    "file": str(prompt_path),
                                    "model": model,
                                    "error": str(e),
                                    "timestamp": datetime.now().isoformat(),
                                })
                                save_failed_files(failed_list)
                                raise SystemExit(1)
                            
                            # Continue with error result
                            result = ModelResult(
                                model=model,
                                run=run,
                                score=0,
                                criteria={},
                                duration=0,
                                error=f"JSONParseError: {str(e)[:100]}",
                            )
                            model_results.append(result)
                        
                        # Log result immediately to file
                        date_str = datetime.now().strftime("%Y-%m-%d")
                        origin = prompt_path.parent.name  # e.g., "advanced", "business"
                        log_evaluation_result(date_str, origin, model, prompt_path.name, result)
                        
                        if verbose:
                            if result.error:
                                print(f"❌ {result.error[:30]}")
                            else:
                                print(f"✓ {result.score:.0f}%")
                                # Show per-criterion breakdown if available
                                if result.criteria:
                                    weak_criteria = [(k, v) for k, v in result.criteria.items() if v < 70]
                                    if weak_criteria:
                                        print(f"    ⚠️  Weak: {', '.join(f'{k}={v:.0f}%' for k, v in weak_criteria)}")
                                        # Show detailed improvement suggestions
                                        if result.improvements:
                                            for criterion, info in result.improvements.items():
                                                if criterion.startswith('_'):
                                                    continue  # Skip meta fields
                                                if isinstance(info, dict) and criterion in [k for k, v in weak_criteria]:
                                                    if info.get('fix'):
                                                        print(f"    💡 {criterion}: {info['fix'][:70]}...")
                                                        if info.get('evidence'):
                                                            print(f"       Evidence: \"{info['evidence'][:50]}...\"")
                                                elif isinstance(info, str) and criterion in [k for k, v in weak_criteria]:
                                                    print(f"    💡 {criterion}: {info[:70]}...")
                                            # Show priority fixes if available
                                            if result.improvements.get('_priority_fixes'):
                                                print(f"    🎯 Priority: {', '.join(result.improvements['_priority_fixes'][:2])}")
            
            # Aggregate results with proper statistics
            valid_scores = [r.score for r in model_results if not r.error and r.score > 0]
            
            if valid_scores:
                n = len(valid_scores)
                avg_score = sum(valid_scores) / n
                min_score = min(valid_scores)
                max_score = max(valid_scores)
                variance = max_score - min_score  # Range for backward compat
                
                # Standard deviation
                if n > 1:
                    sum_sq_diff = sum((x - avg_score) ** 2 for x in valid_scores)
                    std_dev = (sum_sq_diff / (n - 1)) ** 0.5  # Sample std dev
                else:
                    std_dev = 0.0
                
                # Stability: stable if std_dev < 10 points
                is_stable = std_dev < 10.0
                
                # Outlier detection: count scores > 2σ from mean
                if std_dev > 0:
                    outlier_count = sum(1 for s in valid_scores if abs(s - avg_score) > 2 * std_dev)
                else:
                    outlier_count = 0
                
                passed = avg_score >= threshold
                passes = sum(1 for s in valid_scores if s >= threshold)
                agreement = passes / n * 100
            else:
                avg_score = structural["score"]
                min_score = max_score = avg_score
                variance = 0
                std_dev = 0.0
                is_stable = True
                outlier_count = 0
                passed = avg_score >= threshold
                agreement = 100
            
            prompt_result = PromptResult(
                file=str(prompt_path),
                title=structural["title"],
                category=structural["category"],
                avg_score=round(avg_score, 1),
                min_score=round(min_score, 1),
                max_score=round(max_score, 1),
                std_dev=round(std_dev, 2),
                variance=round(variance, 1),
                model_results=model_results,
                passed=passed,
                grade=get_grade(avg_score),
                agreement=round(agreement, 1),
                is_stable=is_stable,
                outlier_count=outlier_count,
                threshold=threshold,
                rubric_version=RUBRIC_VERSION,
            )
            
            results.append(prompt_result)
            
            # Track failures for --retry-failed
            if not passed:
                failed_list.append({
                    "file": str(prompt_path),
                    "score": avg_score,
                    "threshold": threshold,
                    "models": [m.model for m in model_results],
                    "timestamp": datetime.now().isoformat(),
                })
            
            if verbose:
                status = "PASS" if passed else "FAIL"
                stability = "stable" if is_stable else f"UNSTABLE (sd={std_dev:.1f})"
                print(f"  {status} -> {avg_score:.1f}% +/-{std_dev:.1f} ({stability})\n")
    
    # Save failed prompts list for --retry-failed
    if failed_list and not retry_failed:
        save_failed_files(failed_list)
    elif retry_failed and not failed_list:
        # All retries passed! Clear the failed list
        clear_failed_files()
        print("\n✅ All previously failed prompts now pass!")
    
    # Build summary
    passed_count = sum(1 for r in results if r.passed)
    avg_overall = sum(r.avg_score for r in results) / len(results) if results else 0
    
    return EvalRun(
        timestamp=datetime.now().isoformat(),
        tier=tier,
        tier_name=tier_config["name"],
        threshold=threshold,
        models_used=models,
        runs_per_model=runs,
        total_prompts=len(results),
        passed=passed_count,
        failed=len(results) - passed_count,
        avg_score=round(avg_overall, 1),
        results=results,
        duration_seconds=round(time.time() - start_time, 1),
    )


# =============================================================================
# OUTPUT FORMATTERS
# =============================================================================

def print_summary(run: EvalRun):
    """Print evaluation summary to console."""
    print(f"\n{'='*60}")
    print(f"EVALUATION COMPLETE - {run.tier_name}")
    print(f"{'='*60}")
    print(f"Prompts: {run.total_prompts} | Passed: {run.passed} | Failed: {run.failed}")
    print(f"Average Score: {run.avg_score}%")
    print(f"Threshold: {run.threshold}%")
    print(f"Duration: {run.duration_seconds}s")
    print(f"{'='*60}")
    
    # Top performers
    sorted_results = sorted(run.results, key=lambda r: r.avg_score, reverse=True)
    
    print(f"\n🏆 Top 5:")
    for r in sorted_results[:5]:
        status = "✓" if r.passed else "✗"
        print(f"  {status} {r.avg_score:5.1f}% | {r.title[:40]}")
    
    # Needs improvement
    if run.failed > 0:
        print(f"\n⚠️  Needs Improvement:")
        for r in sorted_results[-min(5, run.failed):]:
            if not r.passed:
                print(f"  ✗ {r.avg_score:5.1f}% | {r.title[:40]}")
                # Show weakest criteria for actionable insight
                if r.model_results and r.model_results[0].criteria:
                    criteria = r.model_results[0].criteria
                    weak = [(k, v) for k, v in criteria.items() if v < 60]
                    if weak:
                        weak_str = ', '.join(f"{k} ({v:.0f}%)" for k, v in sorted(weak, key=lambda x: x[1]))
                        print(f"      → Focus on: {weak_str}")
                    # Show detailed improvement suggestions
                    if r.model_results[0].improvements:
                        impr = r.model_results[0].improvements
                        # Show priority fixes first
                        if impr.get('_priority_fixes'):
                            for i, fix in enumerate(impr['_priority_fixes'][:3], 1):
                                print(f"      {i}. {fix[:70]}")
                        # Show example improvement if available
                        if impr.get('_example_improvement'):
                            print(f"      📝 Example fix:")
                            example = impr['_example_improvement']
                            for line in example.split('\\n')[:3]:
                                print(f"         {line[:60]}")
                        # Fallback to per-criterion fixes
                        elif not impr.get('_priority_fixes'):
                            for criterion, info in impr.items():
                                if criterion.startswith('_'):
                                    continue
                                if isinstance(info, dict) and info.get('fix'):
                                    print(f"      💡 {criterion}: {info['fix'][:70]}")
                                elif isinstance(info, str):
                                    print(f"      💡 {criterion}: {info[:70]}")
    
    print(f"\n{'='*60}\n")


def save_json(run: EvalRun, path: Path):
    """Save results to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(run.to_dict(), f, indent=2, default=str, ensure_ascii=False)
    print(f"Saved: {path}")


def save_markdown(run: EvalRun, path: Path):
    """Save results to Markdown."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Prompt Evaluation Report\n\n")
        f.write(f"**Date:** {run.timestamp}\n")
        f.write(f"**Tier:** {run.tier} ({run.tier_name})\n")
        f.write(f"**Models:** {', '.join(run.models_used)}\n\n")
        
        f.write(f"## Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Total Prompts | {run.total_prompts} |\n")
        f.write(f"| Passed | {run.passed} |\n")
        f.write(f"| Failed | {run.failed} |\n")
        f.write(f"| Average Score | {run.avg_score}% |\n")
        f.write(f"| Duration | {run.duration_seconds}s |\n\n")
        
        f.write(f"## Results\n\n")
        f.write(f"| Status | Score | Title | Category |\n")
        f.write(f"|--------|-------|-------|----------|\n")
        
        for r in sorted(run.results, key=lambda x: x.avg_score, reverse=True):
            status = "✓" if r.passed else "✗"
            f.write(f"| {status} | {r.avg_score}% | {r.title[:40]} | {r.category} |\n")
    
    print(f"Saved: {path}")


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PromptEval - Easy, robust prompt evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  prompteval prompts/advanced/           # Evaluate with defaults (Tier 2)
  prompteval prompt.md                   # Single file
  prompteval prompts/ --tier 0           # Structural only (no LLM, instant)
  prompteval prompts/ --tier 3           # Cross-model validation
  prompteval prompts/ -p 4               # Parallel (4 workers)
  prompteval prompts/ --cache            # Enable response caching
  prompteval prompts/ --models phi4,gpt-4o-mini  # Specific models
  prompteval prompts/ -o results.json    # Save JSON report
  prompteval prompts/ --ci               # CI mode (exit code)

Other Entry Points:
  python prompt.py                       # Interactive toolkit (menu-driven)
  prompt-tools                           # Code generation wizard
  python -c "from cli_help import print_quick_reference; print_quick_reference()"
        """,
    )
    
    parser.add_argument("path", nargs="?", help="Prompt file or directory")
    parser.add_argument("-t", "--tier", type=int, default=2, choices=range(8),
                        help="Evaluation tier 0-7 (default: 2)")
    parser.add_argument("-m", "--models", help="Comma-separated models (e.g., phi4,mistral)")
    parser.add_argument("-r", "--runs", type=int, help="Runs per model")
    parser.add_argument("--threshold", type=float, default=70.0, help="Pass threshold (default: 70)")
    parser.add_argument("-o", "--output", help="Output file (.json or .md)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--ci", action="store_true", help="CI mode: exit 1 if any failed")
    parser.add_argument("--all-local", action="store_true", help="Use all local models")
    parser.add_argument("--all-cloud", action="store_true", help="Use all cloud models")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--list-tiers", action="store_true", help="List tier configurations")
    parser.add_argument("--inventory", action="store_true",
                        help="Print a JSON capability inventory and exit")
    parser.add_argument("--no-inventory", action="store_true",
                        help="Skip startup capability inventory")
    parser.add_argument("--active-probe", action="store_true",
                        help="Perform active probes (network calls) when building the inventory")
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help=(
            "Allow non-local/non-GitHub providers (OpenAI/Azure/Gemini/Claude). "
            "Disabled by default to prevent accidental remote usage."
        ),
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Seconds to wait between evaluations (prevents rate limiting, default: 0)",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop immediately on first JSON parsing or evaluation error",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Only evaluate prompts that previously failed (reads from failed-prompts.json)",
    )
    parser.add_argument(
        "-p", "--parallel",
        type=int,
        default=1,
        help="Number of parallel workers for batch evaluation (default: 1, sequential). "
             "Incompatible with --fail-fast.",
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Enable response caching to avoid redundant LLM calls. "
             "Cached responses are stored in ~/.cache/prompts-eval/responses/",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the response cache and exit.",
    )
    
    args = parser.parse_args()

    allow_remote = bool(args.allow_remote) or _env_truthy("PROMPTEVAL_ALLOW_REMOTE")

    # Handle --clear-cache
    if args.clear_cache:
        try:
            from response_cache import ResponseCache
            cache = ResponseCache(enabled=True)
            count = cache.clear()
            print(f"Cleared {count} cache entries")
            return 0
        except Exception as e:
            print(f"Failed to clear cache: {e}")
            return 1

    # Initialize response cache if enabled
    if args.cache:
        try:
            from response_cache import enable_cache
            enable_cache(verbose=args.verbose)
            if args.verbose:
                print("📦 Response cache enabled")
        except ImportError:
            print("Warning: response_cache module not found, caching disabled")

    # Startup capability inventory (skip by default in CI to reduce noise and surprise network calls)
    inventory: Optional[Dict[str, Any]] = None
    if args.inventory:
        from model_inventory import build_inventory

        inventory = build_inventory(active_probes=args.active_probe)
        print(json.dumps(inventory, indent=2, default=str))
        return 0 if inventory.get("ok") else 1

    if not args.no_inventory and not args.ci:
        try:
            from model_inventory import build_inventory, format_inventory_summary

            inventory = build_inventory(active_probes=args.active_probe)
            # Keep this line short; full details are available via --inventory.
            print(format_inventory_summary(inventory))
        except Exception as e:
            if args.verbose:
                print(f"[WARN] Inventory failed: {e}")
    
    # Handle info commands
    if args.list_models:
        # Check for Ollama models
        ollama_discovered = []
        try:
            import urllib.request
            import urllib.error
            ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            req = urllib.request.Request(
                f"{ollama_host}/api/tags",
                headers={"Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                ollama_discovered = [m.get("name", "").split(":")[0] for m in data.get("models", []) if m.get("name")]
        except:
            pass
        
        print("\nLocal Models (ONNX - Always Available, FREE):")
        for k, v in LOCAL_MODELS.items():
            if not v.startswith("ollama:"):
                print(f"  {k:15} -> {v}")
        
        print("\nLocal Models (Ollama - Requires Ollama Running, FREE):")
        if ollama_discovered:
            for model in ollama_discovered:
                print(f"  {model:15} -> ollama:{model} ✅ AVAILABLE")
        else:
            print("  (Start Ollama to use local Llama, DeepSeek, etc.)")
        
        print("\nCloud Models (require GITHUB_TOKEN):")
        for k, v in CLOUD_MODELS.items():
            print(f"  {k:15} -> {v}")
        print("\nWindows AI (local NPU, may be gated):")
        print("  phi-silica       -> windows-ai:phi-silica")
        if inventory is not None:
            print("\nTip: use --inventory to see your detected providers/models.")
        return 0
    
    if args.list_tiers:
        print("\nEvaluation Tiers:")
        for t, c in TIER_CONFIGS.items():
            models = ", ".join(c["models"]) if c["models"] else "None (structural)"
            print(f"  Tier {t}: {c['name']:15} | {c['cost']:8} | {c['time']:8} | {models}")
        return 0
    
    # Resolve models
    models = None
    if args.models:
        models = [m.strip() for m in args.models.split(",")]
    elif args.all_local:
        models = list(LOCAL_MODELS.keys())
    elif args.all_cloud:
        models = list(CLOUD_MODELS.keys())

    # Filter out models we already know are unusable (based on the inventory)
    if models and inventory is not None:
        usable = [m for m in models if _model_is_usable(m, inventory)]
        skipped = [m for m in models if m not in usable]
        if skipped and (args.verbose or not args.ci):
            print(f"[WARN] Skipping unavailable models: {', '.join(skipped)}")
        models = usable
    
    # Run evaluation
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path not found: {path}")
        return 1
    
    # Warn if --parallel and --fail-fast are both set
    if args.parallel > 1 and args.fail_fast:
        print("Warning: --parallel and --fail-fast are incompatible. Using sequential mode.")
    
    run = run_evaluation(
        path=path,
        tier=args.tier,
        threshold=args.threshold,
        models=models,
        runs=args.runs,
        parallel=args.parallel,
        verbose=args.verbose or not args.ci,
        allow_remote=allow_remote,
        delay=args.delay,
        fail_fast=args.fail_fast,
        retry_failed=args.retry_failed,
    )
    
    if run is None:
        return 1
    
    # Output
    if not args.ci:
        print_summary(run)
    
    if args.output:
        output_path = Path(args.output)
        if output_path.suffix == ".json":
            save_json(run, output_path)
        elif output_path.suffix == ".md":
            save_markdown(run, output_path)
        else:
            save_json(run, output_path)
    
    # CI exit code
    if args.ci:
        if run.failed > 0:
            print(f"FAILED: {run.failed}/{run.total_prompts} prompts below threshold")
            return 1
        print(f"PASSED: {run.passed}/{run.total_prompts} prompts")
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
