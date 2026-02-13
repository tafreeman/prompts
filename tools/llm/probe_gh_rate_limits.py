#!/usr/bin/env python3
"""
Probe GH models exposed in the toolkit and report GitHub account rate limits.
Also attempt to probe each gh model for context-window / max-tokens information using the toolkit's LLMClient (best-effort).
Usage: python -m tools.llm.probe_gh_rate_limits
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Try to auto-load a .env file so GITHUB_TOKEN placed there is available to os.environ
try:
    from dotenv import load_dotenv, find_dotenv
    env_path = find_dotenv(usecwd=True)
    if env_path:
        load_dotenv(env_path)
    else:
        # fallback: search upward from this file for a .env
        p = Path(__file__).resolve().parent
        for _ in range(6):
            candidate = p / ".env"
            if candidate.exists():
                load_dotenv(candidate)
                break
            p = p.parent
except Exception:
    # dotenv not installed or other error; continue without failing
    pass

try:
    import requests
except Exception:
    print("The 'requests' package is required. Install with: pip install requests", file=sys.stderr)
    raise


def run_discovery(out_path: str = "discovery.json") -> str:
    cmd = [sys.executable, "-m", "tools.llm.model_probe", "--discover", "--force", "-o", out_path]
    subprocess.check_call(cmd)
    return out_path


def load_discovery(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_gh_models(discovery: dict) -> list:
    models = discovery.get("models") or []
    gh = []
    for m in models:
        if isinstance(m, dict):
            mid = m.get("id") or m.get("model") or m.get("name")
        else:
            mid = str(m)
        if mid and mid.startswith("gh:"):
            gh.append(mid)
    return gh


def get_github_rate_limit(token: str):
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is required to query GitHub rate limits")
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    resp = requests.get("https://api.github.com/rate_limit", headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json(), resp.headers


def probe_model_context(model_id: str) -> dict:
    """Best-effort probe to extract context window / max tokens info for a model using LLMClient.
    Returns a dict with raw info and a parsed 'context' value if found.
    """
    result = {"model": model_id, "info": None, "parsed_context": None, "error": None}
    try:
        from tools.llm.llm_client import LLMClient
    except Exception as e:
        result["error"] = f"LLMClient import failed: {e}"
        return result

    try:
        client = LLMClient.from_model(model_id)
    except Exception as e:
        result["error"] = f"LLMClient.from_model failed: {e}"
        return result

    info = None
    # Try several common method/attr names for metadata
    candidates = ["model_info", "metadata", "get_model_info", "get_metadata", "info", "describe", "request_metadata"]
    for name in candidates:
        try:
            if hasattr(client, name):
                fn = getattr(client, name)
                if callable(fn):
                    info = fn()
                else:
                    info = fn
                break
        except Exception:
            continue

    # Last resort: try a generic inspect of client
    if info is None:
        try:
            # some clients expose a .model or .config attribute
            for attr in ("model", "config", "_model", "_info"):
                if hasattr(client, attr):
                    info = getattr(client, attr)
                    break
        except Exception:
            pass

    result["info"] = info

    # Parse common keys for context window / max tokens
    parsed = {}
    if isinstance(info, dict):
        for key in ("context_window", "context_window_size", "max_tokens", "context_size", "context_length", "max_context"):
            if key in info:
                parsed["value"] = info[key]
                parsed["key"] = key
                break
        # search nested dicts
        if "value" not in parsed:
            for v in info.values():
                if isinstance(v, dict):
                    for key in ("context_window", "max_tokens"):
                        if key in v:
                            parsed["value"] = v[key]
                            parsed["key"] = key
                            break
                    if "value" in parsed:
                        break

    # If info is an object with attributes
    if "value" not in parsed and info is not None:
        try:
            for attr in ("context_window", "max_tokens", "context_size", "context_length"):
                if hasattr(info, attr):
                    parsed["value"] = getattr(info, attr)
                    parsed["key"] = attr
                    break
        except Exception:
            pass

    if parsed:
        result["parsed_context"] = parsed

    return result


def main():
    out = Path("discovery.json")
    try:
        run_discovery(str(out))
    except subprocess.CalledProcessError as e:
        print("Model discovery failed:", e, file=sys.stderr)
        sys.exit(1)

    discovery = load_discovery(str(out))
    gh_models = extract_gh_models(discovery)
    print("Discovered gh models:", gh_models)

    # Probe each model for context window info
    print("\nProbing models for context-window info (best-effort):")
    results = []
    for m in gh_models:
        try:
            r = probe_model_context(m)
        except Exception as e:
            r = {"model": m, "error": str(e)}
        results.append(r)

    print(json.dumps(results, indent=2, default=str))

    token = os.environ.get("GITHUB_TOKEN")
    try:
        data, headers = get_github_rate_limit(token)
    except Exception as e:
        print("Failed to fetch GitHub rate limit:", e, file=sys.stderr)
        sys.exit(1)

    print("\nGitHub account rate limit (from /rate_limit):")
    print(json.dumps(data, indent=2))

    print("\nImportant headers:")
    for k in ("X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"):
        if k in headers:
            print(f"{k}: {headers[k]}")


if __name__ == "__main__":
    main()