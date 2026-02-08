"""Agent resolver for YAML-defined workflow steps.

Maps agent names from workflow YAML definitions to executable step functions.
Agent names follow a convention: tier{N}_{role}, e.g., tier0_parser, tier2_reviewer.

For Tier 0 (deterministic), steps use Python-only logic (no LLM).
For Tier 1+, steps generate an LLM prompt from the step's description and inputs,
then call the model router to get a response.
"""

from __future__ import annotations

import ast
import json
import logging
from pathlib import Path
from typing import Any, Optional

from ..models.router import ModelTier
from .context import ExecutionContext
from .step import StepDefinition, StepFunction

logger = logging.getLogger(__name__)


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


# ---------------------------------------------------------------------------
# LLM-backed step factory
# ---------------------------------------------------------------------------

def _make_llm_step(
    agent_name: str,
    description: str,
    tier: ModelTier,
    expected_output_keys: list[str] | None = None,
) -> StepFunction:
    """Create an async step function that calls an LLM for its output.

    The step gathers all context variables as input, sends them along with the
    step description to the LLM, and returns the response as a JSON dict.

    Args:
        expected_output_keys: If provided, the prompt will instruct the LLM to
            include these keys in the output JSON so downstream steps can
            resolve ``${steps.<name>.outputs.<key>}`` references.
    """

    async def _llm_step(ctx: ExecutionContext) -> dict[str, Any]:
        # Gather available context as step input
        all_vars = ctx.all_variables()

        prompt_parts = [
            f"You are acting as agent '{agent_name}'.",
            f"Task: {description}",
            "",
            "Available context:",
            json.dumps(all_vars, indent=2, default=str),
            "",
        ]

        # Tell the LLM exactly which keys to include so downstream steps
        # and when-conditions can reference them.
        if expected_output_keys:
            prompt_parts.append(
                "Your JSON response MUST include these top-level keys: "
                + ", ".join(f'"{k}"' for k in expected_output_keys)
                + "."
            )
            prompt_parts.append("")

        prompt_parts.append(
            "Produce your analysis as a JSON object. "
            "Return ONLY valid JSON, no markdown fences.",
        )
        prompt = "\n".join(prompt_parts)

        # Try to get a model client from the service container
        try:
            from ..models.client import get_client
            client = get_client(auto_configure=True)
            response, model_used, tokens_used = await client.complete(
                prompt, tier=tier, max_retries=6,
            )
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

        # Strip markdown fences (LLMs often wrap JSON in ```json blocks)
        text = response.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            # Remove first and last lines (fences)
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines).strip()

        # Try to parse JSON from response
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = {"raw_response": response}

        # Attach metadata so StepExecutor can populate StepResult.model_used
        parsed["_meta"] = {"model_used": model_used, "tokens_used": tokens_used}
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
        )
        logger.debug(f"Resolved step '{step_def.name}' -> LLM agent {agent_name} (tier {tier.name})")

    return step_def
