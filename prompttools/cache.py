"""
Response caching for LLM calls.

Simple, file-based caching with TTL support.
"""

import os
import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any, Dict
from dataclasses import dataclass, asdict

from .config import get_cache_dir, CACHE_TTL_HOURS, is_cache_enabled


# Thread lock for cache operations
_cache_lock = threading.Lock()


# =============================================================================
# CACHE KEY GENERATION
# =============================================================================

def _compute_key(model: str, prompt: str, system: str = "") -> str:
    """Generate a unique cache key from inputs."""
    content = f"{model}|{system}|{prompt}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _get_cache_file(key: str) -> Path:
    """Get the file path for a cache entry."""
    return get_cache_dir() / f"{key}.json"


# =============================================================================
# CACHE ENTRY
# =============================================================================

@dataclass
class CacheEntry:
    """A single cache entry."""
    key: str
    model: str
    response: str
    created_at: str
    prompt_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CacheEntry":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})
    
    def is_expired(self, ttl_hours: float = CACHE_TTL_HOURS) -> bool:
        """Check if this entry has expired."""
        created = datetime.fromisoformat(self.created_at)
        return datetime.now() - created > timedelta(hours=ttl_hours)


# =============================================================================
# PUBLIC API
# =============================================================================

def get_cached(
    prompt: str,
    model: str,
    system: str = "",
    ttl_hours: float = CACHE_TTL_HOURS,
) -> Optional[str]:
    """
    Get a cached response if available.
    
    Args:
        prompt: The prompt that was sent
        model: The model used
        system: System prompt (if any)
        ttl_hours: Maximum age in hours
        
    Returns:
        Cached response string, or None if not cached/expired
    """
    if not is_cache_enabled():
        return None
    
    key = _compute_key(model, prompt, system)
    cache_file = _get_cache_file(key)
    
    with _cache_lock:
        if not cache_file.exists():
            return None
        
        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))
            entry = CacheEntry.from_dict(data)
            
            if entry.is_expired(ttl_hours):
                cache_file.unlink(missing_ok=True)
                return None
            
            return entry.response
            
        except (json.JSONDecodeError, KeyError, ValueError):
            cache_file.unlink(missing_ok=True)
            return None


def set_cached(
    prompt: str,
    model: str,
    response: str,
    system: str = "",
) -> None:
    """
    Store a response in the cache.
    
    Args:
        prompt: The prompt that was sent
        model: The model used
        response: The response to cache
        system: System prompt (if any)
    """
    if not is_cache_enabled():
        return
    
    key = _compute_key(model, prompt, system)
    cache_file = _get_cache_file(key)
    
    entry = CacheEntry(
        key=key,
        model=model,
        response=response,
        created_at=datetime.now().isoformat(),
        prompt_hash=hashlib.sha256(prompt.encode()).hexdigest()[:8],
    )
    
    with _cache_lock:
        cache_file.write_text(
            json.dumps(entry.to_dict(), indent=2),
            encoding="utf-8"
        )


def clear_cache(older_than_hours: Optional[float] = None) -> int:
    """
    Clear cached responses.
    
    Args:
        older_than_hours: If set, only clear entries older than this
        
    Returns:
        Number of entries cleared
    """
    cache_dir = get_cache_dir()
    cleared = 0
    
    with _cache_lock:
        for cache_file in cache_dir.glob("*.json"):
            try:
                if older_than_hours:
                    data = json.loads(cache_file.read_text(encoding="utf-8"))
                    entry = CacheEntry.from_dict(data)
                    if not entry.is_expired(older_than_hours):
                        continue
                
                cache_file.unlink()
                cleared += 1
            except Exception:
                # Corrupted file, delete it
                cache_file.unlink(missing_ok=True)
                cleared += 1
    
    return cleared


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics.
    
    Returns:
        Dict with entry counts, sizes, etc.
    """
    cache_dir = get_cache_dir()
    files = list(cache_dir.glob("*.json"))
    
    total_size = sum(f.stat().st_size for f in files)
    
    return {
        "entries": len(files),
        "size_bytes": total_size,
        "size_mb": round(total_size / (1024 * 1024), 2),
        "cache_dir": str(cache_dir),
        "enabled": is_cache_enabled(),
    }
