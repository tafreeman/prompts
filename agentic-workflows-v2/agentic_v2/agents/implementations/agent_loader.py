"""Load agent definitions from .md files with YAML frontmatter.

Reads files like::

    ---
    name: code-reviewer
    description: Expert code review specialist...
    tools: ["Read", "Grep", "Glob", "Bash"]
    model: sonnet
    ---

    You are a senior code reviewer...

Returns a dict mapping agent name → AgentDefinition ready for use in
ClaudeSDKAgent(subagents=...) or any other consumer.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
import os

import yaml

try:
    from claude_agent_sdk import AgentDefinition
except ImportError as e:
    raise ImportError(
        "claude-agent-sdk is required: pip install 'agentic-workflows-v2[claude]'"
    ) from e

# Map short model names used in .md files to full Claude model IDs
_MODEL_MAP = {
    "opus": "claude-opus-4-6",
    "sonnet": "claude-sonnet-4-6",
    "haiku": "claude-haiku-4-5",
}

# Default directory containing .md agent definitions shipped with the project
_DEFAULT_AGENTS_DIR = Path(__file__).parent / "definitions"

# Optional external directory for local agent packs.
# Keep this configurable to avoid machine-specific absolute paths in source.
_EXTERNAL_AGENTS_DIR = (
    Path(os.environ["AGENTIC_EXTERNAL_AGENTS_DIR"])
    if os.environ.get("AGENTIC_EXTERNAL_AGENTS_DIR")
    else None
)

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_agent_file(path: Path) -> tuple[dict[str, Any], str]:
    """Parse a .md file into (frontmatter_dict, body_text)."""
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"No YAML frontmatter found in {path}")
    meta = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():].strip()
    return meta, body


def load_agents(directory: Path | str | None = None) -> dict[str, AgentDefinition]:
    """Load all .md agent definitions from *directory*.

    Args:
        directory: Path containing ``*.md`` agent files.  Defaults to the
                   bundled definitions directory, falling back to the external
                   ``D:\\source\\everything-claude-code\\agents`` location.

    Returns:
        Dict mapping agent ``name`` → :class:`AgentDefinition`.
    """
    if directory is not None:
        dirs = [Path(directory)]
    else:
        # Prefer bundled definitions; then optional external path (if configured).
        dirs = [_DEFAULT_AGENTS_DIR]
        if _EXTERNAL_AGENTS_DIR is not None:
            dirs.append(_EXTERNAL_AGENTS_DIR)

    agents: dict[str, AgentDefinition] = {}

    for d in dirs:
        if not d.exists():
            continue
        for md_file in sorted(d.glob("*.md")):
            try:
                meta, body = _parse_agent_file(md_file)
            except Exception:
                continue  # skip malformed files

            name = meta.get("name") or md_file.stem
            description = meta.get("description", "")
            tools_raw = meta.get("tools", ["Read", "Glob", "Grep"])
            # tools may be stored as a JSON-like list string or a real list
            if isinstance(tools_raw, str):
                import json
                tools_raw = json.loads(tools_raw)
            model_short = meta.get("model", "sonnet")
            model_id = _MODEL_MAP.get(str(model_short).lower(), "claude-sonnet-4-6")

            agents[name] = AgentDefinition(
                description=description,
                prompt=body,
                tools=list(tools_raw),
            )

        if agents:
            break  # stop once we found files in the first valid directory

    return agents


# Pre-loaded registry of agents from the external location
agents: dict[str, AgentDefinition] = load_agents()
