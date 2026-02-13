import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.llm.llm_client import LLMClient

RANKED_MODELS_DEFAULT = [
    "gh:openai/gpt-4.1",
    "ollama:deepseek-v3.2:cloud",
    "gh:openai/gpt-4o",
    "gh:claude-3.5-sonnet",
    "ollama:gpt-oss:120b-cloud",
    "ollama:qwen3-coder:480b-cloud",
    "ollama:gpt-oss:20b-cloud",
    "gemini:gemini-2.5-pro",
    "gemini:gemini-2.5-flash",
    "gemini:gemini-2.0-flash",
    "gh:openai/gpt-4o-mini",
    "gh:openai/o3-mini",
    "gemini:gemini-2.0-flash-lite",
    "gh:openai/gpt-5-mini",
]
RANKED_MODELS_RAW = os.getenv("WAVE2_RANKED_MODELS", "").strip()

MODEL = os.getenv("WAVE2_SUBAGENT_MODEL", "gh:openai/gpt-4o")
EVAL_MODEL = os.getenv("WAVE2_EVAL_MODEL", "gh:openai/gpt-4o")
REFINEMENT_ROUNDS = max(int(os.getenv('WAVE2_REFINEMENT_ROUNDS', '2')), 1)
TARGET_SCORE = float(os.getenv('WAVE2_TARGET_SCORE', '8.0'))
VERBOSE = os.getenv('WAVE2_VERBOSE', '1').strip().lower() not in {'0', 'false', 'no', 'off'}
WRITE_LOG_FILE = os.getenv('WAVE2_WRITE_LOG', '1').strip().lower() not in {'0', 'false', 'no', 'off'}
MODEL_ATTEMPTS = max(int(os.getenv('WAVE2_MODEL_ATTEMPTS', '2')), 1)
RETRY_BACKOFF_SECONDS = float(os.getenv('WAVE2_RETRY_BACKOFF_SECONDS', '1.5'))
FALLBACK_MODELS_RAW = os.getenv("WAVE2_FALLBACK_MODELS", "")
OPENAI_FALLBACK_MODEL = os.getenv("WAVE2_OPENAI_MODEL", "gh:openai/gpt-4o")
GEMINI_FALLBACK_MODEL = os.getenv("WAVE2_GEMINI_MODEL", "gemini:gemini-2.5-pro")
CLAUDE_FALLBACK_MODEL = os.getenv("WAVE2_CLAUDE_MODEL", "gh:claude-3.5-sonnet")

# Role-aware defaults (can be overridden via env vars below)
ROLE_MODEL_DEFAULTS = {
    "scoring_engineer": "ollama:deepseek-v3.2:cloud",
    "ui_engineer": "gh:openai/gpt-4o",
    "adapter_engineer": "ollama:deepseek-v3.2:cloud",
    "integration_architect": "ollama:deepseek-v3.2:cloud",
    "qa_reviewer": "ollama:deepseek-v3.2:cloud",
    "adversarial_reviewer": "ollama:deepseek-v3.2:cloud",
}

ROLE_EVAL_MODEL_DEFAULTS = {
    "scoring_engineer": "ollama:deepseek-v3.2:cloud",
    "ui_engineer": "gh:openai/o3-mini",
    "adapter_engineer": "ollama:deepseek-v3.2:cloud",
    "integration_architect": "ollama:deepseek-v3.2:cloud",
    "qa_reviewer": "ollama:deepseek-v3.2:cloud",
    "adversarial_reviewer": "ollama:deepseek-v3.2:cloud",
}

# Optional override format:
# WAVE2_AGENT_MODELS="ui_engineer=gh:openai/gpt-4.1,scoring_engineer=gh:openai/o3-mini"
AGENT_MODEL_OVERRIDES = os.getenv("WAVE2_AGENT_MODELS", "")
_PROVIDER_KEY_INDEX = {"openai": 0, "gemini": 0, "claude": 0}
_KEY_POOLS_CACHE: dict[str, list[str]] | None = None
OLLAMA_CLOUD_ONLY = os.getenv("WAVE2_OLLAMA_CLOUD_ONLY", "1").strip().lower() not in {
    "0",
    "false",
    "no",
    "off",
}

WAVE2_CONTEXT = """
Wave 2 status from docs/planning/workflow-eval-consolidated-plan.md:
- Completed baseline:
  - W2-ST-001: ExecutionStrategy abstraction
  - W2-ST-002: Iterative repair strategy
- Remaining target tickets for this run:
  - W2-AG-001: server/evaluation.py + contracts/messages.py, add agent_scores payload, reliability adjustment, reporting bundle stats, tests (8)
  - W2-UI-001: dataset selector filters/disabled by workflow compatibility via GET /api/eval/datasets?workflow=..., tests (2)
  - W2-UI-002: score breakdown panel with criteria/weights/grade/hard-gate failures, tests (3)
  - W2-AD-001: integrations/microsoft_agent_framework.py, optional import behavior, canonical event mapping, tests test_microsoft_adapter.py(3)
Constraints:
- Preserve existing behavior and test stability
- Add/extend tests for each ticket
- Keep APIs backward compatible where possible
- Prefer additive schema evolution over breaking payload changes
Prior run quality gaps to close:
- Improve edge-case and backward-compat test coverage
- Replace vague mitigation language with concrete checks
- Be explicit about optional dependency fallback behavior
Execution mode:
- This run supports iterative refinement loops per subagent.
- If evaluator score is below target, revise once or more using evaluator feedback.
""".strip()

SUBAGENTS = [
    {
        "id": "scoring_engineer",
        "title": "W2-AG Scoring Engineer",
        "focus": "W2-AG-001",
        "system": (
            "You are a scoring/evaluation systems engineer. "
            "Design per-agent scoring schemas and statistically sound reporting bundles. "
            "Prioritize deterministic outputs, payload backward compatibility, and explicit edge-case tests. "
            "You must specify exact response fields for server payloads and SSE emission."
        ),
    },
    {
        "id": "ui_engineer",
        "title": "W2-UI Engineer",
        "focus": "W2-UI-001 and W2-UI-002",
        "system": (
            "You are a frontend engineer for React+TypeScript dashboards. "
            "Design compatibility-aware UI states and transparent score breakdown UX tied to backend payloads. "
            "Include explicit disabled/empty/error states and test assertions for hard gate visibility."
        ),
    },
    {
        "id": "adapter_engineer",
        "title": "W2-AD Adapter Engineer",
        "focus": "W2-AD-001",
        "system": (
            "You are an integration adapter engineer. "
            "Design framework adapters with strict contract conformance and graceful optional dependencies. "
            "Explicitly define fallback behavior when the Microsoft SDK is unavailable."
        ),
    },
    {
        "id": "integration_architect",
        "title": "Wave2 Integration Architect",
        "focus": "Cross-ticket backend+SSE+UI contract integration for W2-AG-001/W2-UI-001/W2-UI-002/W2-AD-001",
        "system": (
            "You are a cross-layer integration architect. "
            "Align backend evaluation payloads, streaming contracts, and UI rendering types. "
            "Prevent schema drift and call out required API/type updates."
        ),
    },
    {
        "id": "qa_reviewer",
        "title": "Wave2 QA Reviewer",
        "focus": "Wave 2 end-to-end regression and test coverage",
        "system": (
            "You are a principal QA reviewer. "
            "Identify regression risks, missing tests, and release gates for Wave 2 integration. "
            "Require explicit backward-compatibility checks and failure-mode tests."
        ),
    },
    {
        "id": "adversarial_reviewer",
        "title": "Wave2 Adversarial Reviewer",
        "focus": "Negative-path and adversarial failure-mode analysis for W2-AG-001/W2-UI-001/W2-UI-002/W2-AD-001",
        "system": (
            "You are a red-team reliability reviewer for software delivery plans. "
            "Focus on breakpoints, malformed payloads, missing optional dependencies, and schema mismatch regressions. "
            "Demand concrete negative-path tests."
        ),
    },
]

EVAL_SYSTEM = (
    "You are a strict technical reviewer scoring subagent implementation plans. "
    "Use a 0-10 scale where 10 means production-ready guidance. "
    "Focus on correctness to Wave2 tickets, implementation depth, testability, backward compatibility, "
    "repo alignment, and risk handling. Penalize vague statements, missing file paths, missing edge-case tests, "
    "or absent mitigation validation."
)

PLAN_SCHEMA = """
{
  "summary": "short",
  "ticket_scope": ["ticket ids"],
  "code_changes": [
    {
      "file": "agentic-workflows-v2/...",
      "purpose": "what/why",
      "operations": ["concrete edit 1 naming class/function/field", "concrete edit 2"],
      "compatibility_notes": "how existing behavior stays stable"
    }
  ],
  "tests": [
    {
      "name": "test_name",
      "file": "agentic-workflows-v2/tests/...",
      "type": "unit|integration|ui",
      "asserts": "main assertion",
      "edge_case": true
    }
  ],
  "integration_dependencies": ["module or payload dependency"],
  "risk_register": [
    {
      "risk": "specific risk",
      "impact": "low|medium|high",
      "mitigation": "specific mitigation",
      "validation": "how to verify mitigation"
    }
  ],
  "acceptance_checks": ["verifiable gate"]
}
""".strip()


def _load_dotenv(dotenv_path: Path) -> None:
    """Best-effort .env loader without external dependencies."""
    if not dotenv_path.exists() or not dotenv_path.is_file():
        return
    try:
        text = dotenv_path.read_text(encoding="utf-8")
    except Exception:
        return

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        key = k.strip()
        value = v.strip()
        if not key:
            continue
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        # Keep explicit shell exports authoritative.
        if key in os.environ and (os.getenv(key) or "").strip():
            continue
        os.environ[key] = value


def _http_ok(url: str, timeout_s: float = 2.0) -> bool:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return False


def _default_gateway_ip() -> str | None:
    try:
        cp = subprocess.run(
            ["ip", "route"],
            capture_output=True,
            text=True,
            check=False,
        )
        if cp.returncode != 0:
            return None
        for line in cp.stdout.splitlines():
            parts = line.split()
            if parts and parts[0] == "default" and "via" in parts:
                idx = parts.index("via")
                if idx + 1 < len(parts):
                    return parts[idx + 1]
    except Exception:
        return None
    return None


def _ensure_ollama_host() -> tuple[str, bool]:
    current = (os.getenv("OLLAMA_HOST") or "http://localhost:11434").strip()
    candidates = [current]
    lowered = current.lower()
    if "localhost" in lowered or "127.0.0.1" in lowered:
        gw = _default_gateway_ip()
        if gw:
            candidates.append(f"http://{gw}:11434")
        candidates.append("http://host.docker.internal:11434")

    seen: set[str] = set()
    for host in candidates:
        if host in seen:
            continue
        seen.add(host)
        if _http_ok(f"{host.rstrip('/')}/api/tags"):
            switched = host != current
            os.environ["OLLAMA_HOST"] = host
            return host, switched
    return current, False


def _wsl_to_windows_path(path: Path) -> Path | None:
    """Convert /mnt/<drive>/... to <DRIVE>:\\... when needed."""
    raw = str(path).replace("\\", "/")
    m = re.match(r"^/mnt/([a-zA-Z])/(.+)$", raw)
    if not m:
        return None
    drive = m.group(1).upper()
    rest = m.group(2).replace("/", "\\")
    return Path(f"{drive}:\\{rest}")


def _resolve_dotenv_path(override: str) -> Path:
    candidates: list[Path] = []
    seen: set[str] = set()

    def add_candidate(p: Path):
        key = str(p)
        if key in seen:
            return
        seen.add(key)
        candidates.append(p)

    if override:
        add_candidate(Path(override))
    default_dotenv = Path(__file__).resolve().parent / ".env"
    add_candidate(default_dotenv)
    add_candidate(Path.cwd() / ".env")

    # Add Windows-path variants for WSL-style paths.
    for p in list(candidates):
        converted = _wsl_to_windows_path(p)
        if converted is not None:
            add_candidate(converted)

    for p in candidates:
        try:
            if p.exists() and p.is_file():
                return p
        except Exception:
            continue
    return candidates[0]


def _env_keys_case_insensitive(name: str) -> list[str]:
    target = name.strip().upper()
    return [k for k in os.environ.keys() if k.upper() == target]


def _collect_key_pool(*base_names: str) -> list[str]:
    """Collect key values from BASE and BASE_<n>, case-insensitive."""
    matches: list[tuple[int, str]] = []
    for env_name, value in os.environ.items():
        key_upper = env_name.upper()
        for base in base_names:
            base_upper = base.upper()
            if key_upper == base_upper:
                matches.append((-1, value))
                continue
            prefix = f"{base_upper}_"
            if key_upper.startswith(prefix):
                suffix = key_upper[len(prefix):]
                if suffix.isdigit():
                    matches.append((int(suffix), value))

    # Stable sort: base (-1) first, then numeric suffix ascending.
    matches.sort(key=lambda item: item[0])
    out: list[str] = []
    seen: set[str] = set()
    for _, raw_value in matches:
        value = (raw_value or "").strip()
        if not value or value in seen:
            continue
        out.append(value)
        seen.add(value)
    return out


def _compute_provider_key_pools() -> dict[str, list[str]]:
    return {
        "openai": _collect_key_pool("OPENAI_API_KEY"),
        "gemini": _collect_key_pool("GEMINI_API_KEY", "GOOGLE_API_KEY"),
        "claude": _collect_key_pool("ANTHROPIC_API_KEY", "CLAUDE_API_KEY"),
    }


def _provider_key_pools(*, force_refresh: bool = False) -> dict[str, list[str]]:
    global _KEY_POOLS_CACHE
    if force_refresh or _KEY_POOLS_CACHE is None:
        _KEY_POOLS_CACHE = _compute_provider_key_pools()
    # return a shallow copy to avoid external mutation
    return {
        "openai": list(_KEY_POOLS_CACHE.get("openai", [])),
        "gemini": list(_KEY_POOLS_CACHE.get("gemini", [])),
        "claude": list(_KEY_POOLS_CACHE.get("claude", [])),
    }


def _provider_for_model(model_name: str) -> str | None:
    m = (model_name or "").strip().lower()
    if not m:
        return None
    if m.startswith("gh:") or m.startswith("ollama:") or m.startswith("local:"):
        return None
    if m.startswith("openai:") or m.startswith("gpt"):
        return "openai"
    if m.startswith("gemini:") or m.startswith("google:"):
        return "gemini"
    if m.startswith("claude:") or m.startswith("anthropic:"):
        return "claude"
    if "gemini" in m:
        return "gemini"
    if "claude" in m or "anthropic" in m:
        return "claude"
    if "gpt" in m or "openai" in m:
        return "openai"
    return None


def _activate_provider_key(provider: str) -> tuple[bool, str]:
    pools = _provider_key_pools()
    pool = pools.get(provider) or []
    if not pool:
        return False, "missing"

    idx = _PROVIDER_KEY_INDEX.get(provider, 0) % len(pool)
    selected = pool[idx]
    _PROVIDER_KEY_INDEX[provider] = idx + 1

    # Mirror across accepted aliases for provider-specific client calls.
    if provider == "openai":
        os.environ["OPENAI_API_KEY"] = selected
        active_name = _env_keys_case_insensitive("OPENAI_API_KEY")
        key_label = active_name[0] if active_name else "OPENAI_API_KEY"
    elif provider == "gemini":
        os.environ["GEMINI_API_KEY"] = selected
        os.environ["GOOGLE_API_KEY"] = selected
        active_name = _env_keys_case_insensitive("GEMINI_API_KEY")
        key_label = active_name[0] if active_name else "GEMINI_API_KEY"
    elif provider == "claude":
        os.environ["ANTHROPIC_API_KEY"] = selected
        os.environ["CLAUDE_API_KEY"] = selected
        active_name = _env_keys_case_insensitive("ANTHROPIC_API_KEY")
        key_label = active_name[0] if active_name else "ANTHROPIC_API_KEY"
    else:
        return False, "unsupported"

    return True, f"{key_label}[slot={idx + 1}/{len(pool)}]"


def _prepare_provider_auth_for_model(model_name: str) -> tuple[str | None, bool, str]:
    provider = _provider_for_model(model_name)
    if provider is None:
        return None, True, "n/a"
    ok, detail = _activate_provider_key(provider)
    return provider, ok, detail


def extract_json(text: str):
    text = (text or "").strip()
    if not text:
        return None
    fenced = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    candidates = fenced + [text]
    for c in candidates:
        c = c.strip()
        m = re.search(r"\{[\s\S]*\}", c)
        if m:
            c = m.group(0)
        try:
            return json.loads(c)
        except Exception:
            continue
    return None


def _score_of(evaluation: dict[str, Any] | None) -> float | None:
    if not isinstance(evaluation, dict):
        return None
    value = evaluation.get("overall_score")
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def _parse_model_overrides(raw: str) -> dict[str, str]:
    """Parse key=value,key2=value2 model override strings."""
    overrides: dict[str, str] = {}
    for chunk in (raw or "").split(","):
        part = chunk.strip()
        if not part or "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            overrides[key] = value
    return overrides


def _parse_ranked_models(raw: str) -> list[str]:
    if not raw.strip():
        return list(RANKED_MODELS_DEFAULT)
    return [part.strip() for part in raw.split(",") if part.strip()]


RANKED_MODELS = _parse_ranked_models(RANKED_MODELS_RAW)


def _resolve_agent_model(agent_id: str, overrides: dict[str, str]) -> str:
    env_key = f"WAVE2_MODEL_{agent_id.upper()}"
    env_specific = os.getenv(env_key)
    if env_specific:
        return env_specific.strip()
    if agent_id in overrides:
        return overrides[agent_id]
    return ROLE_MODEL_DEFAULTS.get(agent_id, MODEL)


def _has_openai_key() -> bool:
    return bool(_provider_key_pools().get("openai"))


def _has_gemini_key() -> bool:
    return bool(_provider_key_pools().get("gemini"))


def _has_claude_key() -> bool:
    return bool(_provider_key_pools().get("claude"))


def _dedupe_keep_order(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        val = (item or "").strip()
        if not val or val in seen:
            continue
        out.append(val)
        seen.add(val)
    return out


def _filter_model_chain(items: list[str]) -> list[str]:
    if not OLLAMA_CLOUD_ONLY:
        return items
    out: list[str] = []
    for item in items:
        val = (item or "").strip()
        if not val:
            continue
        if val.lower().startswith("ollama:") and "cloud" not in val.lower():
            continue
        out.append(val)
    return out


def _looks_provider_error(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return True
    provider_error_markers = [
        "gh models error:",
        "rate limited",
        "too many requests",
        "429",
        "quota exceeded",
        "api key",
        "authentication",
        "openaierror",
        "anthropic",
        "gemini",
    ]
    if t.startswith("error:"):
        return True
    return any(marker in t for marker in provider_error_markers) and len(t) < 800


def _build_model_chain(primary_model: str, fallback_model: str) -> list[str]:
    explicit_fallbacks = [part.strip() for part in FALLBACK_MODELS_RAW.split(",") if part.strip()]
    chain = [primary_model, fallback_model, *explicit_fallbacks, *RANKED_MODELS]
    if _has_openai_key():
        chain.append(OPENAI_FALLBACK_MODEL)
    if _has_gemini_key():
        chain.append(GEMINI_FALLBACK_MODEL)
    if _has_claude_key():
        chain.append(CLAUDE_FALLBACK_MODEL)
    chain.append(MODEL)
    filtered = _filter_model_chain(chain)
    return _dedupe_keep_order(filtered)


def _generate_with_fallback(
    *,
    primary_model: str,
    fallback_model: str,
    prompt: str,
    system_instruction: str,
    temperature: float,
    max_tokens: int,
) -> tuple[str, str]:
    """Generate text with retry + model/provider failover."""
    model_chain = _build_model_chain(primary_model, fallback_model)
    last_error_text: str | None = None
    last_exception: Exception | None = None

    for model_name in model_chain:
        for attempt in range(1, MODEL_ATTEMPTS + 1):
            try:
                provider, auth_ok, auth_detail = _prepare_provider_auth_for_model(model_name)
                if VERBOSE and provider is not None:
                    print(
                        f"[{_ts()}] [auth] model={model_name} provider={provider} "
                        f"status={'ok' if auth_ok else 'missing'} detail={auth_detail}",
                        flush=True,
                    )
                text = LLMClient.generate_text(
                    model_name,
                    prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                if _looks_provider_error(text):
                    last_error_text = text
                    if VERBOSE:
                        print(
                            f"[{_ts()}] [model-failover] model={model_name} "
                            f"attempt={attempt}/{MODEL_ATTEMPTS} returned provider error text; retry/failover",
                            flush=True,
                        )
                    if attempt < MODEL_ATTEMPTS:
                        time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                        continue
                    break
                return text, model_name
            except Exception as exc:
                last_exception = exc
                if VERBOSE:
                    print(
                        f"[{_ts()}] [model-failover] model={model_name} "
                        f"attempt={attempt}/{MODEL_ATTEMPTS} exception={type(exc).__name__}: {exc}",
                        flush=True,
                    )
                if attempt < MODEL_ATTEMPTS:
                    time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                    continue
                break

        if VERBOSE:
            print(
                f"[{_ts()}] [model-failover] switching from model={model_name}",
                flush=True,
            )

    if last_error_text:
        return last_error_text, model_chain[-1] if model_chain else fallback_model
    if last_exception is not None:
        raise last_exception
    return "model generation failed: no response", fallback_model


def run_subagent(agent, *, model_name: str):
    prompt = f"""
{WAVE2_CONTEXT}

Your assignment focus: {agent['focus']}.

Return ONLY JSON with this exact shape:
{PLAN_SCHEMA}

Rules:
- Use concrete repo-relative file paths.
- Include at least 3 tests and at least 1 backward-compat or edge-case test.
- No markdown, no prose outside JSON.
""".strip()
    raw, used_model = _generate_with_fallback(
        primary_model=model_name,
        fallback_model=MODEL,
        prompt=prompt,
        system_instruction=agent["system"],
        temperature=0.2,
        max_tokens=1200,
    )
    parsed = extract_json(raw)
    return raw, parsed, used_model


def refine_subagent_output(agent, prior_output, eval_feedback, round_number, *, model_name: str):
    feedback_json = json.dumps(eval_feedback or {}, indent=2)
    prompt = f"""
{WAVE2_CONTEXT}

Your assignment focus: {agent['focus']}.
You are in refinement round {round_number}.

Previous output:
{prior_output}

Evaluator feedback to address:
{feedback_json}

Revise the plan to close gaps. Preserve good parts, improve weak parts.
Return ONLY JSON with this exact shape:
{PLAN_SCHEMA}

Rules:
- Address each blocking issue if present.
- Convert vague acceptance checks into measurable checks.
- Add at least 1 explicit negative-path test.
- Use concrete repo-relative file paths.
- No markdown, no prose outside JSON.
""".strip()
    raw, used_model = _generate_with_fallback(
        primary_model=model_name,
        fallback_model=MODEL,
        prompt=prompt,
        system_instruction=agent["system"],
        temperature=0.1,
        max_tokens=1400,
    )
    parsed = extract_json(raw)
    return raw, parsed, used_model


def evaluate_agent_output(agent, raw_output, *, model_name: str):
    prompt = f"""
Evaluate the following subagent output for {agent['focus']}.

Output to evaluate:
{raw_output}

Return ONLY JSON:
{{
  "criterion_scores": {{
    "ticket_alignment": 0,
    "implementation_depth": 0,
    "testability": 0,
    "backward_compatibility": 0,
    "repo_alignment": 0,
    "risk_management": 0,
    "specificity": 0
  }},
  "overall_score": 0,
  "verdict": "strong|adequate|weak",
  "key_findings": ["..."],
  "blocking_issues": ["..."],
  "next_actions": ["..."]
}}
""".strip()
    raw, used_model = _generate_with_fallback(
        primary_model=model_name,
        fallback_model=EVAL_MODEL,
        prompt=prompt,
        system_instruction=EVAL_SYSTEM,
        temperature=0.0,
        max_tokens=700,
    )
    parsed = extract_json(raw)
    return raw, parsed, used_model


def main():
    dotenv_override = (os.getenv("WAVE2_DOTENV") or "").strip()
    dotenv_path = _resolve_dotenv_path(dotenv_override)
    _load_dotenv(dotenv_path)
    ollama_host, ollama_switched = _ensure_ollama_host()
    _provider_key_pools(force_refresh=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path("runs") / "subagents"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"wave2_subagent_run_{ts}.log"

    log_fp = None
    if WRITE_LOG_FILE:
        log_fp = log_path.open("w", encoding="utf-8")

    def log(message: str, *, force_console: bool = False):
        line = f"[{_ts()}] {message}"
        if VERBOSE or force_console:
            print(line, flush=True)
        if log_fp is not None:
            log_fp.write(line + "\n")
            log_fp.flush()

    model_overrides = _parse_model_overrides(AGENT_MODEL_OVERRIDES)

    log(
        "Wave2 subagent run starting "
        f"(model={MODEL}, eval_model={EVAL_MODEL}, rounds={REFINEMENT_ROUNDS}, "
        f"target={TARGET_SCORE}, attempts={MODEL_ATTEMPTS}, backoff={RETRY_BACKOFF_SECONDS}s)",
        force_console=True,
    )
    log(
        "Provider availability: "
        f"openai={_has_openai_key()} gemini={_has_gemini_key()} claude={_has_claude_key()}",
        force_console=True,
    )
    pools = _provider_key_pools()
    log(
        "Provider key pool sizes: "
        f"openai={len(pools.get('openai', []))} "
        f"gemini={len(pools.get('gemini', []))} "
        f"claude={len(pools.get('claude', []))}",
        force_console=True,
    )
    log(f"dotenv path used: {dotenv_path}", force_console=True)
    log(
        f"ollama host: {ollama_host} (auto_switched={ollama_switched})",
        force_console=True,
    )
    if FALLBACK_MODELS_RAW.strip():
        log(f"Custom fallback chain: {FALLBACK_MODELS_RAW}", force_console=True)
    log(f"Ranked model order: {RANKED_MODELS}", force_console=True)
    if model_overrides:
        log(f"Agent model overrides: {model_overrides}", force_console=True)

    run = {
        "timestamp": ts,
        "model": MODEL,
        "eval_model": EVAL_MODEL,
        "wave": "Wave2",
        "config": {
            "refinement_rounds": REFINEMENT_ROUNDS,
            "target_score": TARGET_SCORE,
        },
        "subagents": [],
    }

    total_agents = len(SUBAGENTS)
    for index, agent in enumerate(SUBAGENTS, start=1):
        agent_model = _resolve_agent_model(agent["id"], model_overrides)
        eval_default = ROLE_EVAL_MODEL_DEFAULTS.get(agent["id"], EVAL_MODEL)
        agent_eval_model = os.getenv(
            f"WAVE2_EVAL_MODEL_{agent['id'].upper()}",
            eval_default,
        ).strip()
        log(
            f"[{index}/{total_agents}] subagent={agent['id']} focus='{agent['focus']}' "
            f"model={agent_model} eval_model={agent_eval_model} starting",
            force_console=True,
        )
        preview_chain = _build_model_chain(agent_model, MODEL)
        log(
            f"[{agent['id']}] model chain: {preview_chain}",
            force_console=True,
        )
        rounds: list[dict[str, Any]] = []

        log(f"[{agent['id']}] round=1 generating plan")
        raw, parsed, used_gen_model = run_subagent(agent, model_name=agent_model)
        log(
            f"[{agent['id']}] round=1 generation complete "
            f"(chars={len(raw or '')}, parsed_json={parsed is not None}, model_used={used_gen_model})"
        )

        log(f"[{agent['id']}] round=1 evaluating plan")
        eval_raw, eval_parsed, used_eval_model = evaluate_agent_output(
            agent,
            raw,
            model_name=agent_eval_model,
        )
        log(
            f"[{agent['id']}] round=1 evaluation complete "
            f"(score={_score_of(eval_parsed)}, parsed_json={eval_parsed is not None}, model_used={used_eval_model})"
        )
        rounds.append({
            "round": 1,
            "raw_output": raw,
            "parsed_output": parsed,
            "evaluation_raw": eval_raw,
            "evaluation": eval_parsed,
            "overall_score": _score_of(eval_parsed),
            "generation_model": used_gen_model,
            "evaluation_model": used_eval_model,
        })

        best_round = rounds[0]
        best_score = best_round["overall_score"]

        for round_number in range(2, REFINEMENT_ROUNDS + 1):
            if best_score is not None and best_score >= TARGET_SCORE:
                log(
                    f"[{agent['id']}] target reached (score={best_score}) after round={best_round['round']}; skipping remaining rounds"
                )
                break
            log(
                f"[{agent['id']}] round={round_number} refining from previous score={rounds[-1]['overall_score']}"
            )
            refine_raw, refine_parsed, refine_gen_model = refine_subagent_output(
                agent,
                prior_output=rounds[-1]["raw_output"],
                eval_feedback=rounds[-1]["evaluation"],
                round_number=round_number,
                model_name=agent_model,
            )
            log(
                f"[{agent['id']}] round={round_number} refinement complete "
                f"(chars={len(refine_raw or '')}, parsed_json={refine_parsed is not None}, model_used={refine_gen_model})"
            )
            log(f"[{agent['id']}] round={round_number} evaluating refined plan")
            refine_eval_raw, refine_eval_parsed, refine_eval_model = evaluate_agent_output(
                agent,
                refine_raw,
                model_name=agent_eval_model,
            )
            candidate = {
                "round": round_number,
                "raw_output": refine_raw,
                "parsed_output": refine_parsed,
                "evaluation_raw": refine_eval_raw,
                "evaluation": refine_eval_parsed,
                "overall_score": _score_of(refine_eval_parsed),
                "generation_model": refine_gen_model,
                "evaluation_model": refine_eval_model,
            }
            rounds.append(candidate)
            log(
                f"[{agent['id']}] round={round_number} evaluation complete "
                f"(score={candidate['overall_score']}, parsed_json={refine_eval_parsed is not None}, model_used={refine_eval_model})"
            )

            if best_score is None:
                if candidate["overall_score"] is not None:
                    best_round = candidate
                    best_score = candidate["overall_score"]
            elif (
                candidate["overall_score"] is not None
                and candidate["overall_score"] > best_score
            ):
                best_round = candidate
                best_score = candidate["overall_score"]
                log(
                    f"[{agent['id']}] new best round={best_round['round']} score={best_score}"
                )

        log(
            f"[{agent['id']}] finalized best_round={best_round['round']} "
            f"best_score={best_score} target_reached={bool(best_score is not None and best_score >= TARGET_SCORE)}",
            force_console=True,
        )

        run["subagents"].append({
            "id": agent["id"],
            "title": agent["title"],
            "focus": agent["focus"],
            "system_instruction": agent["system"],
            "raw_output": best_round["raw_output"],
            "parsed_output": best_round["parsed_output"],
            "evaluation_raw": best_round["evaluation_raw"],
            "evaluation": best_round["evaluation"],
            "best_round": best_round["round"],
            "target_reached": bool(best_score is not None and best_score >= TARGET_SCORE),
            "generation_model_selected": agent_model,
            "evaluation_model_selected": agent_eval_model,
            "generation_model_used": best_round.get("generation_model"),
            "evaluation_model_used": best_round.get("evaluation_model"),
            "rounds": rounds,
        })

    # Aggregate score
    scores = []
    for item in run["subagents"]:
        ev = item.get("evaluation") or {}
        sc = ev.get("overall_score")
        if isinstance(sc, (int, float)):
            scores.append(float(sc))
    run["aggregate"] = {
        "evaluated_agents": len(scores),
        "mean_overall_score": round(sum(scores) / len(scores), 3) if scores else None,
        "min_overall_score": min(scores) if scores else None,
        "max_overall_score": max(scores) if scores else None,
    }

    out_path = out_dir / f"wave2_subagent_run_{ts}.json"
    out_path.write_text(json.dumps(run, indent=2), encoding="utf-8")

    log(f"Saved subagent run: {out_path}", force_console=True)
    if log_fp is not None:
        log(f"Verbose log file: {log_path}", force_console=True)

    print("\nScore summary:", flush=True)
    for item in run["subagents"]:
        ev = item.get("evaluation") or {}
        print(
            f"- {item['id']}: {ev.get('overall_score')} ({ev.get('verdict')}) "
            f"[best_round={item.get('best_round')} target_reached={item.get('target_reached')}]",
            flush=True,
        )
    print(f"- mean: {run['aggregate']['mean_overall_score']}", flush=True)

    if log_fp is not None:
        log_fp.close()


if __name__ == "__main__":
    main()
