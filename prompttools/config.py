"""
Configuration for prompttools.

This module provides handles for both local and package-level paths,
default model configurations, and provider settings managed through
environment variables or standard defaults.
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List

# =============================================================================
# PATHS
# =============================================================================

def get_package_dir() -> Path:
    """Get the prompttools package directory."""
    return Path(__file__).parent


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to the root of the repository.
    """
    return get_package_dir().parent


def get_cache_dir() -> Path:
    """Get the cache directory."""
    cache_dir = Path(os.environ.get(
        "PROMPTTOOLS_CACHE_DIR",
        get_project_root() / ".cache" / "prompttools"
    ))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_rubrics_dir() -> Path:
    """Get the rubrics directory."""
    return get_package_dir() / "rubrics"


# =============================================================================
# DEFAULTS
# =============================================================================

# Default model preference order
DEFAULT_MODELS = [
    "local:phi4mini",
    "ollama:phi4-reasoning",
    "ollama:llama3.3",
    "gh:gpt-4o-mini",
]

# Required frontmatter fields (at least one of these must be present)
REQUIRED_FRONTMATTER = ["name"]  # 'name' is our standard; 'title' also accepted

# Preferred frontmatter fields (warning if missing)
PREFERRED_FRONTMATTER = ["description", "type"]

# Optional execution/evaluation frontmatter fields
OPTIONAL_FRONTMATTER = [
    "pattern",           # react | cove | reflexion | rag
    "model",             # Recommended model (e.g., openai/gpt-4o)
    "model_parameters",  # {temperature, max_tokens, top_p}
    "response_format",   # text | json_object | json_schema
    "difficulty",        # beginner | intermediate | advanced
    "test_data",         # List of input/expected pairs for evaluation
]

# Valid values for enumerated frontmatter fields
VALID_PATTERNS = ["react", "cove", "reflexion", "rag"]
VALID_RESPONSE_FORMATS = ["text", "json_object", "json_schema"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
VALID_TYPES = ["how_to", "reference", "template", "guide"]

# Required sections in prompt files
REQUIRED_SECTIONS = ["Description", "Prompt"]

# Preferred sections (warning if missing)
PREFERRED_SECTIONS = ["Variables", "Example"]

# Optional sections
OPTIONAL_SECTIONS = ["Test Data"]

# Files/patterns to skip during validation
SKIP_PATTERNS = [
    "README.md",
    "index.md",
    "LICENSE*",
    "**/archive/**",
    "**/templates/**",
]

# Evaluation pass threshold (0-100)
PASS_THRESHOLD = 70.0

# Cache TTL in hours
CACHE_TTL_HOURS = 24.0


# =============================================================================
# PROVIDER CONFIGURATION
# =============================================================================

@dataclass
class ProviderConfig:
    """Configuration for LLM providers."""
    
    # Ollama
    ollama_host: str = field(
        default_factory=lambda: os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    )
    
    # GitHub Models
    github_token: Optional[str] = field(
        default_factory=lambda: os.environ.get("GITHUB_TOKEN")
    )
    github_endpoint: str = "https://models.github.ai/inference"
    
    # Azure OpenAI
    azure_openai_endpoint: Optional[str] = field(
        default_factory=lambda: os.environ.get("AZURE_OPENAI_ENDPOINT")
    )
    azure_openai_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("AZURE_OPENAI_API_KEY")
    )
    
    # OpenAI
    openai_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("OPENAI_API_KEY")
    )
    
    # Google Gemini
    gemini_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY") or 
                                os.environ.get("GOOGLE_API_KEY")
    )
    
    # Anthropic Claude
    anthropic_key: Optional[str] = field(
        default_factory=lambda: os.environ.get("ANTHROPIC_API_KEY")
    )


# Global config instance
_config: Optional[ProviderConfig] = None


def get_config() -> ProviderConfig:
    """Get or create the global config."""
    global _config
    if _config is None:
        _config = ProviderConfig()
    return _config


# =============================================================================
# ENVIRONMENT HELPERS
# =============================================================================

def is_cache_enabled() -> bool:
    """
    Check if the global response cache is enabled.
    
    Controlled by PROMPTTOOLS_CACHE_ENABLED environment variable.
    
    Returns:
        True if enabled (default), False otherwise.
    """
    return os.environ.get("PROMPTTOOLS_CACHE_ENABLED", "1").lower() in ("1", "true", "yes")


def is_verbose() -> bool:
    """Check if verbose mode is enabled."""
    return os.environ.get("PROMPTTOOLS_VERBOSE", "0").lower() in ("1", "true", "yes")
