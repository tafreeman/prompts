"""
LLM Response Cache
==================

Caches LLM responses to avoid redundant API calls during development/evaluation.
This significantly speeds up re-runs and reduces API costs.

Usage:
    from tools.cache import get_cached_response, cache_response, clear_cache
    
    # Check for cached response first
    cached = get_cached_response("gh:gpt-4o-mini", "Hello world")
    if cached:
        return cached
    
    # Generate and cache
    response = LLMClient.generate_text(model, prompt)
    cache_response(model, prompt, response)
    
    # Clear cache
    clear_cache()  # All
    clear_cache(max_age_hours=24)  # Older than 24 hours

Author: Prompts Library Team
Version: 1.0.0
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

# Cache directory
CACHE_DIR = Path.home() / ".cache" / "prompts-tools" / "llm-responses"


def _get_cache_key(model: str, prompt: str, system_instruction: Optional[str] = None, **kwargs) -> str:
    """Generate a unique cache key for the request."""
    # Include all parameters that affect the response
    content = json.dumps({
        "model": model,
        "prompt": prompt,
        "system": system_instruction or "",
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 4096),
    }, sort_keys=True)
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _get_cache_file(key: str) -> Path:
    """Get the cache file path for a key."""
    return CACHE_DIR / f"{key}.json"


def get_cached_response(
    model: str,
    prompt: str,
    system_instruction: Optional[str] = None,
    max_age_hours: float = 24.0,
    **kwargs
) -> Optional[str]:
    """
    Get a cached response if available and not expired.
    
    Args:
        model: Model identifier (e.g., "gh:gpt-4o-mini")
        prompt: The user prompt
        system_instruction: Optional system prompt
        max_age_hours: Maximum age of cached response in hours
        **kwargs: Additional parameters (temperature, max_tokens)
    
    Returns:
        Cached response string, or None if not cached/expired
    """
    key = _get_cache_key(model, prompt, system_instruction, **kwargs)
    cache_file = _get_cache_file(key)
    
    if not cache_file.exists():
        return None
    
    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        cached_time = datetime.fromisoformat(data["timestamp"])
        
        # Check if expired
        if datetime.now() - cached_time > timedelta(hours=max_age_hours):
            return None
        
        return data["response"]
    except (json.JSONDecodeError, KeyError, ValueError):
        # Corrupted cache file
        cache_file.unlink(missing_ok=True)
        return None


def cache_response(
    model: str,
    prompt: str,
    response: str,
    system_instruction: Optional[str] = None,
    **kwargs
) -> None:
    """
    Cache an LLM response.
    
    Args:
        model: Model identifier
        prompt: The user prompt
        response: The LLM response to cache
        system_instruction: Optional system prompt
        **kwargs: Additional parameters
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    key = _get_cache_key(model, prompt, system_instruction, **kwargs)
    cache_file = _get_cache_file(key)
    
    data = {
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "response": response,
        "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
    }
    
    cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def clear_cache(max_age_hours: Optional[float] = None) -> int:
    """
    Clear cached responses.
    
    Args:
        max_age_hours: If provided, only clear entries older than this.
                       If None, clear all entries.
    
    Returns:
        Number of entries cleared
    """
    if not CACHE_DIR.exists():
        return 0
    
    cleared = 0
    cutoff = datetime.now() - timedelta(hours=max_age_hours) if max_age_hours else None
    
    for cache_file in CACHE_DIR.glob("*.json"):
        try:
            if cutoff:
                data = json.loads(cache_file.read_text(encoding="utf-8"))
                cached_time = datetime.fromisoformat(data["timestamp"])
                if cached_time >= cutoff:
                    continue
            
            cache_file.unlink()
            cleared += 1
        except Exception:
            # If we can't read it, delete it
            cache_file.unlink(missing_ok=True)
            cleared += 1
    
    return cleared


def get_cache_stats() -> Dict[str, Any]:
    """Get statistics about the cache."""
    if not CACHE_DIR.exists():
        return {"entries": 0, "size_mb": 0, "oldest": None, "newest": None}
    
    entries = list(CACHE_DIR.glob("*.json"))
    total_size = sum(f.stat().st_size for f in entries)
    
    timestamps = []
    for f in entries:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            timestamps.append(datetime.fromisoformat(data["timestamp"]))
        except Exception:
            pass
    
    return {
        "entries": len(entries),
        "size_mb": round(total_size / 1024 / 1024, 2),
        "oldest": min(timestamps).isoformat() if timestamps else None,
        "newest": max(timestamps).isoformat() if timestamps else None,
    }


# Environment variable to disable caching (useful for testing)
CACHE_ENABLED = os.environ.get("PROMPTS_CACHE_ENABLED", "1").lower() in ("1", "true", "yes")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage LLM response cache")
    parser.add_argument("--stats", action="store_true", help="Show cache statistics")
    parser.add_argument("--clear", action="store_true", help="Clear all cache entries")
    parser.add_argument("--clear-old", type=float, metavar="HOURS", 
                        help="Clear entries older than HOURS")
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_cache_stats()
        print(f"Cache entries: {stats['entries']}")
        print(f"Total size: {stats['size_mb']} MB")
        print(f"Oldest: {stats['oldest']}")
        print(f"Newest: {stats['newest']}")
    elif args.clear:
        cleared = clear_cache()
        print(f"Cleared {cleared} cache entries")
    elif args.clear_old:
        cleared = clear_cache(max_age_hours=args.clear_old)
        print(f"Cleared {cleared} cache entries older than {args.clear_old} hours")
    else:
        parser.print_help()
