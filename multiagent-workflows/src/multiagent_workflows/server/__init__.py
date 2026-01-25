"""Local UI + API server for Multi-Agent Workflows.

This server exists to support the HTML UI in `multiagent-workflows/ui/`.
It exposes a tiny JSON API for browsing benchmark datasets and fetching tasks
from online sources (HuggingFace datasets) when available.

Design goals:
- No heavy web framework dependency (uses aiohttp which is already in deps)
- Same-origin serving of UI to avoid CORS issues
- Graceful fallback if optional benchmark tooling isn't importable
"""
