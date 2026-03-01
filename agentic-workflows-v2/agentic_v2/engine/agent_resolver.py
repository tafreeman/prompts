"""Agent resolver — maps YAML agent names to executable step functions.

This is the bridge between the declarative YAML workflow definitions and
the executable runtime.  Each step in a YAML workflow declares an ``agent``
field (e.g. ``tier2_coder``).  The resolver:

1. **Infers the model tier** from the agent name prefix (``tier{N}_``).
2. **Selects an implementation**:
   - Tier 0 agents → deterministic Python function from ``TIER0_REGISTRY``.
   - Tier 1+ agents → auto-generated LLM-backed step via :func:`_make_llm_step`.
3. **Assembles the prompt** from persona Markdown files (``prompts/<role>.md``),
   task description, available context, tool contracts, and the universal
   sentinel output format instructions.
4. **Executes multi-turn tool loops** — LLM steps can call registered tools
   (up to 8 rounds, 12 calls/round) with truncated results.
5. **Parses LLM output** via sentinel artifacts (``<<<ARTIFACT>>>``), JSON
   extraction, and robust review-report normalization for gating conditions.

Key constants:
- ``_TIER_MAX_TOKENS``: Conservative per-tier output token limits.
- ``_MAX_TOOL_ROUNDS`` / ``_MAX_TOOL_CALLS_PER_ROUND``: Tool loop bounds.
- ``_MAX_TOOL_RESULT_CHARS``: Truncation limit for tool results.
"""

from __future__ import annotations

import ast
import json
import logging
import re
import time
from pathlib import Path
from typing import Any

from ..models.router import ModelTier
from .context import ExecutionContext
from .step import StepDefinition, StepFunction

logger = logging.getLogger(__name__)

# Maximum output tokens per model tier.  These are conservative values that
# work across all providers at each tier.  Tier 2+ use capable models that
# support at least 8 192 output tokens; tier 3+ supports 16 384.
_TIER_MAX_TOKENS: dict[ModelTier, int] = {
    ModelTier.TIER_0: 0,       # deterministic, no LLM
    ModelTier.TIER_1: 4096,
    ModelTier.TIER_2: 8192,
    ModelTier.TIER_3: 16384,
    ModelTier.TIER_4: 16384,
    ModelTier.TIER_5: 32768,
}


def _extract_json_candidates(text: str) -> list[str]:
    """Return increasingly permissive JSON candidates from model output.

    Tries, in order: raw text, markdown-fence-stripped text, bracket-span
    extraction for objects (``{…}``), and bracket-span for arrays (``[…]``).
    Duplicates are removed while preserving priority order.
    """
    candidates: list[str] = []
    raw = text.strip()
    if raw:
        candidates.append(raw)

    # Remove markdown fences when present
    if raw.startswith("```"):
        lines = [ln for ln in raw.splitlines() if not ln.strip().startswith("```")]
        fenced = "\n".join(lines).strip()
        if fenced:
            candidates.append(fenced)

    # Extract first likely JSON object/array by bracket span
    first_obj = raw.find("{")
    last_obj = raw.rfind("}")
    if first_obj != -1 and last_obj > first_obj:
        snippet = raw[first_obj:last_obj + 1].strip()
        if snippet:
            candidates.append(snippet)

    first_arr = raw.find("[")
    last_arr = raw.rfind("]")
    if first_arr != -1 and last_arr > first_arr:
        snippet = raw[first_arr:last_arr + 1].strip()
        if snippet:
            candidates.append(snippet)

    # Deduplicate while preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


def _normalize_expected_structure(
    parsed: dict[str, Any],
    expected_output_keys: list[str] | None,
) -> dict[str, Any]:
    """Normalize parsed LLM output to match expected workflow output keys.

    Primary focus is ``review_report`` normalization: LLM reviewer outputs
    arrive in many variant shapes (``review``, ``raw_response``, nested
    JSON, ``approved`` boolean, etc.).  This function coerces all variants
    into a canonical ``{"review_report": {"overall_status": "<STATUS>"}}``
    structure using :meth:`ReviewStatus.normalize` so that downstream
    ``when``-conditions can reliably gate on approval status.
    """
    from ..contracts import ReviewStatus

    if not expected_output_keys:
        return parsed

    # Normalize legacy/variant reviewer output into review_report.
    if "review_report" in expected_output_keys:
        rr = parsed.get("review_report")
        if not isinstance(rr, dict) and isinstance(parsed.get("review"), dict):
            rr = parsed.get("review")
            parsed["review_report"] = rr

        # Some model responses come wrapped as:
        # {"raw_response": "```json { \"review_report\": {...} } ```"}
        # Recover nested reviewer payload so when-conditions can resolve.
        if not isinstance(rr, dict) and isinstance(parsed.get("raw_response"), str):
            nested_raw = str(parsed.get("raw_response"))
            nested_report: dict[str, Any] | None = None
            for candidate in _extract_json_candidates(nested_raw):
                try:
                    nested_parsed = json.loads(candidate)
                    if isinstance(nested_parsed, dict):
                        if isinstance(nested_parsed.get("review_report"), dict):
                            nested_report = nested_parsed["review_report"]
                            break
                        if isinstance(nested_parsed.get("review"), dict):
                            nested_report = nested_parsed["review"]
                            break
                        if isinstance(nested_parsed.get("overall_status"), str):
                            nested_report = {
                                "overall_status": nested_parsed["overall_status"]
                            }
                            break
                except json.JSONDecodeError:
                    continue

            if nested_report is not None:
                rr = nested_report
                parsed["review_report"] = rr

        if not isinstance(rr, dict):
            raw_text = str(parsed.get("raw_response", ""))
            status_match = re.search(
                r'"?overall_status"?\s*[:=]\s*"?([A-Za-z_ -]+)"?',
                raw_text,
                flags=re.IGNORECASE,
            )
            approved_match = re.search(
                r'"?approved"?\s*[:=]\s*(true|false)',
                raw_text,
                flags=re.IGNORECASE,
            )

            if status_match:
                raw_status = status_match.group(1).strip()
            elif approved_match:
                raw_status = (
                    "APPROVED"
                    if approved_match.group(1).lower() == "true"
                    else "NEEDS_FIXES"
                )
            else:
                raw_status = None  # normalize() defaults to NEEDS_FIXES

            rr = {"overall_status": ReviewStatus.normalize(raw_status).value}
            parsed["review_report"] = rr

        if isinstance(rr, dict):
            top_level_status = parsed.get("overall_status")
            if isinstance(top_level_status, str) and "overall_status" not in rr:
                rr["overall_status"] = top_level_status

            if "overall_status" not in rr:
                approved = rr.get("approved")
                raw_status = "APPROVED" if approved is True else None
                rr["overall_status"] = ReviewStatus.normalize(raw_status).value
            else:
                # Normalize whatever value is already present
                rr["overall_status"] = ReviewStatus.normalize(
                    rr["overall_status"]
                ).value

            parsed["review_report"] = rr

    return parsed


def _parse_llm_json_output(
    response: str,
    expected_output_keys: list[str] | None,
) -> dict[str, Any]:
    """Parse model text output into a JSON dict with robust fallbacks.

    Attempts each candidate from :func:`_extract_json_candidates`.  If all
    fail, returns ``{"raw_response": response}`` with a best-effort
    ``review_report`` salvaged from raw text (if expected).
    """
    for candidate in _extract_json_candidates(response):
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return _normalize_expected_structure(parsed, expected_output_keys)
        except json.JSONDecodeError:
            continue

    fallback: dict[str, Any] = {"raw_response": response}

    # If this step expects review_report but the model returned malformed JSON,
    # salvage status from raw text so when-conditions still work.
    if expected_output_keys and "review_report" in expected_output_keys:
        status_match = re.search(
            r'"?overall_status"?\s*[:=]\s*"?([A-Za-z_ -]+)"?',
            response,
            flags=re.IGNORECASE,
        )
        approved_match = re.search(
            r'"?approved"?\s*[:=]\s*(true|false)',
            response,
            flags=re.IGNORECASE,
        )

        if status_match:
            raw_status = status_match.group(1).strip()
            normalized = raw_status.upper().replace(" ", "_")
            fallback["review_report"] = {"overall_status": normalized}
        elif approved_match:
            is_approved = approved_match.group(1).lower() == "true"
            fallback["review_report"] = {
                "overall_status": "APPROVED" if is_approved else "NEEDS_FIXES"
            }
        else:
            # Conservative default: if we cannot prove approval, force rework path.
            fallback["review_report"] = {"overall_status": "NEEDS_FIXES"}

    return fallback


# ---------------------------------------------------------------------------
# Sentinel-format parser
# ---------------------------------------------------------------------------

_ARTIFACT_RE = re.compile(
    r"<<<ARTIFACT\s+(\w+)>>>(.*?)<<<ENDARTIFACT>>>",
    re.DOTALL,
)
_FILE_BLOCK_RE = re.compile(
    r"^FILE:\s*(.+?)\n(.*?)^ENDFILE\s*$",
    re.DOTALL | re.MULTILINE,
)


def _extract_files_from_artifact(content: str) -> dict[str, str]:
    """Return ``{path: content}`` for every FILE/ENDFILE block in *content*.

    This supports R4's one-file-per-path model: callers can iterate over
    individual files rather than treating the artifact as a single blob.
    Returns an empty dict when no FILE blocks are present.
    """
    return {
        match.group(1).strip(): match.group(2)
        for match in _FILE_BLOCK_RE.finditer(content)
    }


def _parse_sentinel_output(
    text: str,
    expected_output_keys: list[str] | None,
) -> dict[str, Any] | None:
    """Parse the sentinel artifact format produced by coder.md prompts.

    Looks for blocks of the form::

        <<<ARTIFACT key>>>
        FILE: path/to/file.py
        content
        ENDFILE
        <<<ENDARTIFACT>>>

    JSON-shaped artifact content (starting with ``{`` or ``[``) is parsed
    as JSON; all other content is kept as a raw string.

    For code artifacts that contain FILE/ENDFILE blocks, an additional
    ``<key>_files`` entry is added to the result dict mapping each file
    path to its content — this lets downstream steps iterate individual
    files (R4 pattern) without changing the primary ``<key>`` value.

    Returns ``None`` when no sentinel blocks are found so callers can fall
    back to JSON parsing.
    """
    matches = _ARTIFACT_RE.findall(text)
    if not matches:
        return None

    result: dict[str, Any] = {}
    for key, raw_content in matches:
        content = raw_content.strip()
        stripped = content.lstrip()
        if stripped.startswith(("{", "[")):
            try:
                result[key] = json.loads(content)
                continue
            except json.JSONDecodeError:
                pass
        # Keep raw string for backward compatibility
        result[key] = content
        # Also expose per-file dict for R4 consumers
        files = _extract_files_from_artifact(content)
        if files:
            result[f"{key}_files"] = files

    if expected_output_keys and "review_report" in expected_output_keys:
        result = _normalize_expected_structure(result, expected_output_keys)
    return result


# ---------------------------------------------------------------------------
# Tier-0 deterministic step implementations
# ---------------------------------------------------------------------------

async def _parse_code_step(ctx: ExecutionContext) -> dict[str, Any]:
    """Tier-0: Parse a code file and return basic structure info."""
    file_path = None
    # Try multiple ways to get the file path from context
    for key in ("file_path", "code_file"):
        try:
            file_path = await ctx.get(key)
            if file_path:
                break
        except Exception:
            pass

    # Also check parent context
    if not file_path:
        try:
            all_vars = ctx.all_variables()
            file_path = all_vars.get("file_path") or all_vars.get("code_file")
        except Exception:
            pass

    source = ""
    if file_path:
        p = Path(file_path)
        if p.exists():
            source = p.read_text(encoding="utf-8", errors="replace")
        else:
            source = str(file_path)  # Might be inline code
    
    # Basic AST analysis for Python files
    parsed_ast: dict[str, Any] = {"raw_source": source[:500]}
    metrics: dict[str, Any] = {"lines": len(source.splitlines()), "chars": len(source)}

    try:
        tree = ast.parse(source)
        functions = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        imports = [
            n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
        ] + [
            alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names
        ]
        parsed_ast.update({
            "language": "python",
            "functions": functions,
            "classes": classes,
            "imports": imports,
        })
        metrics.update({
            "function_count": len(functions),
            "class_count": len(classes),
            "import_count": len(imports),
        })
    except SyntaxError:
        parsed_ast["language"] = "unknown"
        parsed_ast["parse_error"] = "Could not parse as Python"

    return {"parsed_ast": parsed_ast, "code_metrics": metrics}


async def _noop_step(ctx: ExecutionContext) -> dict[str, Any]:
    """Tier-0 fallback: return empty outputs."""
    return {}


# Registry of known tier-0 deterministic step implementations
TIER0_REGISTRY: dict[str, StepFunction] = {
    "tier0_parser": _parse_code_step,
}

# Directory containing agent-specific system prompt Markdown files
_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

# Universal output format instructions appended to EVERY LLM step prompt.
# Prompt files describe agent expertise/persona; this block enforces the
# output contract so it never depends on individual prompt file contents.
_SENTINEL_OUTPUT_INSTRUCTIONS = """
## Output Format (REQUIRED — engine contract)

Your response MUST use sentinel artifact blocks:

<<<ARTIFACT key>>>
FILE: path/to/file.ext
<full file content — no truncation>
ENDFILE
<<<ENDARTIFACT>>>

For structured data (JSON) use:

<<<ARTIFACT key>>>
{"field": "value", ...}
<<<ENDARTIFACT>>>

Rules:
- One <<<ARTIFACT key>>> block per logical output (e.g. backend_code, review_report)
- FILE/ENDFILE inside code artifacts; raw JSON inside data artifacts
- ENDFILE on its own line; <<<ENDARTIFACT>>> on its own line
- Complete files only — no truncation, no TODO stubs
""".strip()

_MAX_TOOL_ROUNDS = 8
_MAX_TOOL_CALLS_PER_ROUND = 12
_MAX_TOOL_RESULT_CHARS = 12000


def _load_agent_system_prompt(
    agent_name: str,
    prompt_file_override: str | None = None,
) -> str | None:
    """Return the Markdown persona prompt for *agent_name*, or None.

    Resolution order:
    1. Explicit ``prompt_file_override`` from the YAML step definition.
    2. ``prompts/<role>.md`` where ``<role>`` is the suffix after the tier
       prefix (e.g. ``tier2_coder`` → ``coder.md``).
    3. ``prompts/default.md`` fallback.

    Note: Output format instructions are injected separately by
    ``_make_llm_step`` via ``_SENTINEL_OUTPUT_INSTRUCTIONS`` — prompt files
    only need to describe the agent's persona/expertise.
    """
    # 1. Explicit override
    if prompt_file_override:
        override_path = _PROMPTS_DIR / prompt_file_override
        if override_path.exists():
            return override_path.read_text(encoding="utf-8")
        logger.warning(
            f"prompt_file '{prompt_file_override}' for agent '{agent_name}' not found "
            f"in {_PROMPTS_DIR}; falling back to role-based lookup."
        )

    # 2. Role-based lookup
    if "_" in agent_name:
        role = agent_name.split("_", 1)[1]  # "tier2_coder" → "coder"
        role_path = _PROMPTS_DIR / f"{role}.md"
        if role_path.exists():
            return role_path.read_text(encoding="utf-8")

    # 3. Default fallback
    default_path = _PROMPTS_DIR / "default.md"
    if default_path.exists():
        return default_path.read_text(encoding="utf-8")

    logger.debug(
        f"No system prompt found for agent '{agent_name}'; "
        "using inline output instructions only."
    )
    return None


# ---------------------------------------------------------------------------
# LLM-backed step factory
# ---------------------------------------------------------------------------

def _parameter_spec_to_json_schema(spec: Any) -> dict[str, Any]:
    """Convert internal tool parameter spec to JSON schema object."""
    if not isinstance(spec, dict):
        return {"type": "string"}

    normalized: dict[str, Any] = {}
    for key, value in spec.items():
        if key == "required":
            continue
        normalized[key] = value

    normalized.setdefault("type", "string")
    return normalized


def _build_tool_contracts(
    tier: ModelTier,
    requested_tools: list[str] | None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Return OpenAI-compatible tool schemas and bound tool instances."""
    from ..tools import get_registry

    registry = get_registry()
    available = {tool.name: tool for tool in registry.list_tools()}

    selected: list[Any] = []
    if requested_tools is None:
        selected = [tool for tool in available.values() if tool.tier <= tier.value]
    else:
        for tool_name in requested_tools:
            tool = available.get(tool_name)
            if tool is None:
                logger.warning("Unknown tool '%s' requested; skipping.", tool_name)
                continue
            if tool.tier > tier.value:
                logger.warning(
                    "Tool '%s' (tier %s) exceeds step tier %s; skipping.",
                    tool_name,
                    tool.tier,
                    tier.value,
                )
                continue
            selected.append(tool)

    selected.sort(key=lambda t: t.name)

    tool_schemas: list[dict[str, Any]] = []
    bound_tools: dict[str, Any] = {}
    for tool in selected:
        schema = tool.get_schema()
        params = schema.parameters if schema else {}
        required_fields = [
            name
            for name, spec in params.items()
            if isinstance(spec, dict) and bool(spec.get("required"))
        ]

        tool_schemas.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            name: _parameter_spec_to_json_schema(spec)
                            for name, spec in params.items()
                        },
                        "required": required_fields,
                    },
                },
            }
        )
        bound_tools[tool.name] = tool

    return tool_schemas, bound_tools


def _extract_usage_tokens(usage: Any) -> int:
    """Best-effort extraction of total token usage across providers."""
    if not isinstance(usage, dict):
        return 0

    direct_keys = ("total_tokens", "totalTokenCount", "total")
    for key in direct_keys:
        value = usage.get(key)
        if isinstance(value, (int, float)):
            return max(0, int(value))

    prompt = usage.get("prompt_tokens", usage.get("input_tokens"))
    completion = usage.get("completion_tokens", usage.get("output_tokens"))
    if isinstance(prompt, (int, float)) and isinstance(completion, (int, float)):
        return max(0, int(prompt) + int(completion))

    return 0


def _messages_to_text(messages: list[dict[str, Any]]) -> str:
    """Flatten chat messages for fallback token estimation."""
    parts: list[str] = []
    for msg in messages:
        role = str(msg.get("role", ""))
        content = msg.get("content", "")
        if isinstance(content, str):
            parts.append(f"{role}:{content}")
        else:
            parts.append(f"{role}:{json.dumps(content, default=str)}")
    return "\n".join(parts)


def _parse_tool_args(raw_args: Any) -> dict[str, Any]:
    """Normalize tool-call arguments into a dict."""
    if isinstance(raw_args, dict):
        return raw_args

    if isinstance(raw_args, str):
        stripped = raw_args.strip()
        if not stripped:
            return {}
        try:
            parsed = json.loads(stripped)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}

    return {}


def _normalize_tool_call(call: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    """Normalize provider-specific tool call shape."""
    fn = call.get("function")
    if isinstance(fn, dict):
        name = str(fn.get("name", "")).strip()
        args = _parse_tool_args(fn.get("arguments"))
        call_id = str(call.get("id", "")).strip()
    else:
        # Anthropic-style blocks: {"type":"tool_use","name":"...","input":{...}}
        name = str(call.get("name", "")).strip()
        args = _parse_tool_args(call.get("input"))
        call_id = str(call.get("id", "")).strip()

    if not call_id:
        call_id = (
            f"tool-{abs(hash((name, json.dumps(args, sort_keys=True, default=str)))):x}"
        )

    return call_id, name, args


def _truncate_tool_result(text: str) -> str:
    """Bound tool payload size to avoid runaway context growth."""
    if len(text) <= _MAX_TOOL_RESULT_CHARS:
        return text
    return (
        text[:_MAX_TOOL_RESULT_CHARS]
        + "\n[truncated]"
    )


def _serialize_tool_result(tool_result: Any) -> str:
    """Serialize a ToolResult-like object as compact JSON."""
    payload = {
        "success": bool(getattr(tool_result, "success", False)),
        "data": getattr(tool_result, "data", None),
        "error": getattr(tool_result, "error", None),
        "metadata": getattr(tool_result, "metadata", {}),
        "execution_time_ms": getattr(tool_result, "execution_time_ms", 0.0),
        "tool_name": getattr(tool_result, "tool_name", ""),
    }
    return _truncate_tool_result(json.dumps(payload, default=str))


async def _complete_chat_with_fallback(
    client: Any,
    tier: ModelTier,
    messages: list[dict[str, Any]],
    max_tokens: int,
    tools: list[dict[str, Any]] | None,
) -> tuple[dict[str, Any], str, int]:
    """Call backend.complete_chat with router-based fallback."""
    if client.backend is None:
        raise RuntimeError("No LLM backend configured")

    tried: list[str] = []
    last_error: Exception | None = None

    for _ in range(6):
        model = client.router.get_model_for_tier(tier)
        if model is None or model in tried:
            break
        tried.append(model)

        start = time.perf_counter()
        try:
            response = await client.backend.complete_chat(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                tools=tools,
            )

            latency_ms = (time.perf_counter() - start) * 1000
            client.router.record_success(model, latency_ms)

            tokens_used = _extract_usage_tokens(response.get("usage"))
            if tokens_used <= 0:
                tokens_used = client.backend.count_tokens(
                    _messages_to_text(messages) + str(response.get("content", "")),
                    model,
                )
            if getattr(client, "budget", None):
                client.budget.consume(tokens_used)

            return response, model, int(tokens_used)

        except Exception as exc:
            last_error = exc
            error_str = str(exc).lower()
            if "rate limit" in error_str or "429" in error_str:
                client.router.record_rate_limit(model)
            elif "timeout" in error_str:
                client.router.record_timeout(model)
            elif "not found" in error_str or "no access" in error_str:
                client.router.record_failure(model, "permanent", is_permanent=True)
            else:
                client.router.record_failure(model, type(exc).__name__)
            logger.warning("Model %s failed during chat completion: %s", model, exc)

    raise RuntimeError(
        f"All chat models failed. Tried: {tried}. Last error: {last_error}"
    )


async def _run_tool_calls(
    tool_calls: list[dict[str, Any]],
    bound_tools: dict[str, Any],
    messages: list[dict[str, Any]],
) -> int:
    """Execute tool calls and append tool results to messages."""
    executed = 0
    for call in tool_calls[:_MAX_TOOL_CALLS_PER_ROUND]:
        if not isinstance(call, dict):
            continue
        call_id, tool_name, tool_args = _normalize_tool_call(call)
        if not tool_name:
            continue

        tool = bound_tools.get(tool_name)
        if tool is None:
            tool_result_text = json.dumps(
                {"success": False, "error": f"Unknown tool: {tool_name}"}
            )
        else:
            is_valid, validation_error = tool.validate_parameters(**tool_args)
            if not is_valid:
                tool_result_text = json.dumps(
                    {
                        "success": False,
                        "error": f"Invalid parameters for {tool_name}: {validation_error}",
                    }
                )
            else:
                try:
                    tool_result = await tool.execute(**tool_args)
                    tool_result_text = _serialize_tool_result(tool_result)
                except Exception as exc:
                    tool_result_text = json.dumps(
                        {
                            "success": False,
                            "error": f"Tool execution error for {tool_name}: {exc}",
                        }
                    )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": call_id,
                "name": tool_name,
                "content": _truncate_tool_result(tool_result_text),
            }
        )
        executed += 1

    return executed


def _make_llm_step(
    agent_name: str,
    description: str,
    tier: ModelTier,
    expected_output_keys: list[str] | None = None,
    prompt_file_override: str | None = None,
    enabled_tools: list[str] | None = None,
) -> StepFunction:
    """Create an async step function that calls an LLM for its output.

    Prompt assembly (in order):
    1. Agent persona from ``prompts/<role>.md`` (or ``prompt_file_override``)
    2. Task description and available context
    3. Required artifact key list (if ``expected_output_keys`` provided)
    4. ``_SENTINEL_OUTPUT_INSTRUCTIONS`` — always appended so the output
       contract is enforced regardless of which persona prompt is loaded.

    Args:
        expected_output_keys: Keys that MUST appear as <<<ARTIFACT>>> blocks.
        prompt_file_override: Optional filename (relative to prompts/) to use
            instead of the role-based lookup.
        enabled_tools: Optional explicit tool allowlist. ``None`` means all
            tools available for the step's tier.
    """
    persona_prompt = _load_agent_system_prompt(agent_name, prompt_file_override)

    async def _llm_step(ctx: ExecutionContext) -> dict[str, Any]:
        # Gather available context as step input
        all_vars = ctx.all_variables()

        prompt_parts: list[str] = []

        # 1. Agent persona
        if persona_prompt:
            prompt_parts += [persona_prompt, "", "---", ""]

        # 2. Task + context
        prompt_parts += [
            f"You are acting as agent '{agent_name}'.",
            f"Task: {description}",
            "",
            "Available context:",
            json.dumps(all_vars, indent=2, default=str),
            "",
        ]

        # 3. Required artifact keys
        if expected_output_keys:
            prompt_parts += [
                "Your response MUST include <<<ARTIFACT key>>> blocks for: "
                + ", ".join(expected_output_keys)
                + ".",
                "",
            ]

        # 4. Tooling contract
        tool_schemas, bound_tools = _build_tool_contracts(tier, enabled_tools)
        if bound_tools:
            prompt_parts += [
                "Tooling access is enabled for this step.",
                "Use tools to fetch facts or inspect artifacts instead of guessing.",
                "Available tools: " + ", ".join(sorted(bound_tools.keys())) + ".",
                "",
            ]

        # 4. Universal output format contract (always appended)
        prompt_parts += [_SENTINEL_OUTPUT_INSTRUCTIONS, ""]

        prompt = "\n".join(prompt_parts)

        # Try to get a model client from the service container
        try:
            from ..models.client import get_client
            client = get_client(auto_configure=True)
            max_tokens = _TIER_MAX_TOKENS.get(tier, 8192)
            messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
            response = ""
            model_used = ""
            tokens_used = 0
            tool_call_count = 0

            for iteration in range(_MAX_TOOL_ROUNDS + 1):
                chat_response, model_used, turn_tokens = await _complete_chat_with_fallback(
                    client=client,
                    tier=tier,
                    messages=messages,
                    max_tokens=max_tokens,
                    tools=tool_schemas if bound_tools else None,
                )
                tokens_used += turn_tokens

                response = str(chat_response.get("content", "") or "")
                tool_calls = chat_response.get("tool_calls") or []

                assistant_message: dict[str, Any] = {
                    "role": "assistant",
                    "content": response,
                }
                if tool_calls:
                    assistant_message["tool_calls"] = tool_calls
                messages.append(assistant_message)

                if not tool_calls:
                    break

                if iteration >= _MAX_TOOL_ROUNDS:
                    logger.warning(
                        "Tool loop maxed out for agent '%s' after %s rounds.",
                        agent_name,
                        _MAX_TOOL_ROUNDS,
                    )
                    break

                executed = await _run_tool_calls(tool_calls, bound_tools, messages)
                tool_call_count += executed
                if executed == 0:
                    break
        except Exception as e:
            logger.warning(
                f"LLM call failed for agent '{agent_name}' (tier {tier.name}): {e}. "
                "Returning placeholder output."
            )
            return {
                "agent": agent_name,
                "status": "llm_unavailable",
                "description": description,
                "note": str(e),
            }

        parsed = (
            _parse_sentinel_output(response, expected_output_keys)
            or _parse_llm_json_output(response, expected_output_keys)
        )

        # Attach metadata so StepExecutor can populate StepResult.model_used
        parsed["_meta"] = {
            "model_used": model_used,
            "tokens_used": tokens_used,
            "tool_calls": tool_call_count,
        }
        return parsed

    _llm_step.__qualname__ = f"llm_step[{agent_name}]"
    return _llm_step


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------

def _infer_tier(agent_name: str) -> ModelTier:
    """Infer model tier from agent name convention: tier{N}_{role}."""
    if agent_name.startswith("tier0_"):
        return ModelTier.TIER_0
    elif agent_name.startswith("tier1_"):
        return ModelTier.TIER_1
    elif agent_name.startswith("tier2_"):
        return ModelTier.TIER_2
    elif agent_name.startswith("tier3_"):
        return ModelTier.TIER_3
    elif agent_name.startswith("tier4_"):
        return ModelTier.TIER_4
    elif agent_name.startswith("tier5_"):
        return ModelTier.TIER_5
    else:
        return ModelTier.TIER_2  # Default to balanced tier


def resolve_agent(step_def: StepDefinition) -> StepDefinition:
    """Resolve a step definition's agent metadata into an executable function.

    If `step_def.func` is already set, this is a no-op.
    Otherwise, looks up the agent name from metadata and either:
      - Uses a registered Tier-0 deterministic implementation, or
      - Generates an LLM-backed step function for higher tiers.

    The step's `tier` field is also updated based on the agent name.

    Returns the mutated StepDefinition (same object).
    """
    if step_def.func is not None:
        return step_def  # Already has a function

    agent_name = step_def.metadata.get("agent")
    if not agent_name:
        raise ValueError(
            f"Step '{step_def.name}' has no agent and no func — "
            f"check YAML 'agent:' field or provide a 'func:' reference"
        )

    tier = _infer_tier(agent_name)
    step_def.tier = tier

    # Check tier-0 registry first
    if tier == ModelTier.TIER_0 and agent_name in TIER0_REGISTRY:
        step_def.func = TIER0_REGISTRY[agent_name]
        logger.debug(f"Resolved step '{step_def.name}' -> deterministic {agent_name}")
    else:
        # Generate an LLM-backed step
        step_def.func = _make_llm_step(
            agent_name=agent_name,
            description=step_def.description,
            tier=tier,
            expected_output_keys=list(step_def.output_mapping.keys()) or None,
            prompt_file_override=step_def.metadata.get("prompt_file"),
            enabled_tools=step_def.metadata.get("tools"),
        )
        logger.debug(f"Resolved step '{step_def.name}' -> LLM agent {agent_name} (tier {tier.name})")

    return step_def
