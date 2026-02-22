"""Model provider registry for the LangChain workflow engine.

Supported providers:
- GitHub Models          (prefix ``gh:``)            via OpenAI-compatible API
- Ollama                 (prefix ``ollama:``)        local or remote Ollama
- OpenAI                 (prefix ``openai:``)        direct OpenAI API
- Anthropic              (prefix ``anthropic:`` / ``claude:``)
- Gemini                 (prefix ``gemini:``)
- NotebookLM alias       (prefix ``notebooklm:``)    routes to Gemini model
- Local ONNX             (prefix ``local:``)         via repo ``LLMClient``
- LM Studio              (prefix ``lmstudio:``)      via OpenAI-compatible API
- Local API              (prefix ``local-api:``)     via OpenAI-compatible API

Environment variables
---------------------
GITHUB_TOKEN
    Personal access token for GitHub Models API.
OLLAMA_BASE_URL
    Override Ollama server URL (default: ``http://localhost:11434``).
OPENAI_API_KEY
    API key for OpenAI provider.
ANTHROPIC_API_KEY
    API key for Anthropic provider.
GOOGLE_API_KEY / GEMINI_API_KEY
    API key for Gemini provider.
NOTEBOOKLM_MODEL / NOTEBOOKLM_GEMINI_MODEL
    Optional default Gemini model used by ``notebooklm:`` alias.
AGENTIC_MODEL_TIER_{N}
    Force a specific model ID for tier N (e.g. ``AGENTIC_MODEL_TIER_2=gh:openai/gpt-4o``).
DEEP_RESEARCH_* (optional)
    Can be used with ``env:VAR|fallback`` per-step overrides in workflow YAML.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Load .env so API keys are available when invoked via uvicorn directly
# (the CLI entry point already does this, but server startup may bypass it)
# ---------------------------------------------------------------------------

try:
    from dotenv import load_dotenv as _load_dotenv

    for _p in Path(__file__).resolve().parents:
        _env = _p / ".env"
        if _env.is_file():
            _load_dotenv(_env, override=False)
            break
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Provider availability probe
# ---------------------------------------------------------------------------

# Env-var keys that gate each provider (any one present = provider available)
_PROVIDER_ENV_KEYS: dict[str, list[str]] = {
    "gemini": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "gh": ["GITHUB_TOKEN"],
    "ollama": [],  # always available (local)
    "local": [],   # always available (ONNX)
    "lmstudio": [], # always available (local server)
    "local_api": [], # always available (local server)
}

# ---------------------------------------------------------------------------
# Tier defaults (updated dynamically by probe_and_update_tier_defaults)
# ---------------------------------------------------------------------------

_TIER_DEFAULTS: dict[int, str] = {
    1: "gemini:gemini-2.0-flash-lite",
    2: "gemini:gemini-2.0-flash",
    3: "gemini:gemini-2.5-flash",
    4: "gemini:gemini-2.5-flash",
    5: "gemini:gemini-2.5-flash",
}

# Models ranked by reasoning capability per tier.
# First available provider wins during probe.
_TIER_FALLBACK_CHAINS: dict[int, list[str]] = {
    # Tier 1: fast / cheap -- summarisation, extraction, simple tasks
    1: [
        "gemini:gemini-2.0-flash-lite",
        "gh:openai/gpt-4o-mini",
        "openai:gpt-4o-mini",
        "anthropic:claude-haiku-4-5-20251001",
        "ollama:gemma3:4b",
    ],
    # Tier 2: balanced -- code review, moderate reasoning
    2: [
        "gemini:gemini-2.0-flash",
        "gh:openai/gpt-4o",
        "openai:gpt-4o",
        "anthropic:claude-sonnet-4-6-20260219",
        "ollama:qwen3:8b",
    ],
    # Tier 3: strong reasoning -- architecture, complex code gen
    3: [
        "gemini:gemini-2.5-flash",
        "anthropic:claude-sonnet-4-6-20260219",
        "openai:gpt-4o",
        "gh:openai/gpt-4o",
        "ollama:qwen3-coder:30b",
    ],
    # Tier 4: top-tier -- hard problems, multi-step planning
    4: [
        "gemini:gemini-2.5-flash",
        "anthropic:claude-sonnet-4-6-20260219",
        "openai:gpt-4o",
        "gh:openai/gpt-4o",
        "ollama:qwen3-coder:30b",
    ],
    # Tier 5: best available -- research, deep analysis
    5: [
        "gemini:gemini-2.5-flash",
        "anthropic:claude-sonnet-4-6-20260219",
        "openai:gpt-4o",
        "gh:openai/gpt-4o",
        "ollama:qwen3-coder:30b",
    ],
}

# GitHub Models base URL
_GH_BASE_URL = "https://models.inference.ai.azure.com"
_TRANSIENT_HTTP_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
_GH_BACKUP_MODELS: tuple[str, ...] = (
    "gh:openai/gpt-4o-mini",
    "gh:openai/gpt-4o",
)


def _provider_prefix(model_id: str) -> str:
    """Extract the provider prefix from a model ID."""
    return model_id.split(":")[0] if ":" in model_id else "ollama"


def _is_provider_available(provider: str) -> bool:
    """Check if a provider's required env vars are present."""
    keys = _PROVIDER_ENV_KEYS.get(provider, [])
    if not keys:
        return True  # ollama / local -- no key required
    return any(os.environ.get(k) for k in keys)


def probe_available_providers() -> dict[str, bool]:
    """Probe which LLM providers have credentials configured."""
    return {prov: _is_provider_available(prov) for prov in _PROVIDER_ENV_KEYS}


def probe_and_update_tier_defaults() -> dict[str, Any]:
    """Probe providers and update ``_TIER_DEFAULTS`` to the best available model per tier.

    Called on module import and can be re-called at server startup to pick up
    env changes.  Also installs a health-checker on the native ``ModelRouter``
    so both engines benefit from the same availability data.

    Returns a summary dict with provider availability and resolved tier defaults.
    """
    availability = probe_available_providers()

    available_providers = [p for p, ok in availability.items() if ok]
    unavailable_providers = [p for p, ok in availability.items() if not ok]

    resolved: dict[int, str] = {}
    for tier, chain in _TIER_FALLBACK_CHAINS.items():
        for model_id in chain:
            provider = _provider_prefix(model_id)
            if _is_provider_available(provider):
                resolved[tier] = model_id
                break
        else:
            resolved[tier] = _TIER_DEFAULTS.get(tier, chain[-1])

    _TIER_DEFAULTS.update(resolved)

    # Also configure the native engine router with the same env-var checker
    _configure_native_router(availability)

    summary = {
        "available_providers": available_providers,
        "unavailable_providers": unavailable_providers,
        "tier_defaults": dict(_TIER_DEFAULTS),
    }

    logger.info(
        "Model probe complete: available=%s, unavailable=%s",
        available_providers,
        unavailable_providers,
    )
    for tier, model_id in sorted(_TIER_DEFAULTS.items()):
        logger.info("  Tier %d -> %s", tier, model_id)

    return summary


def _configure_native_router(availability: dict[str, bool]) -> None:
    """Set a health-checker on the native ModelRouter so it skips unavailable providers."""
    try:
        from ..models.router import get_router
    except ImportError:
        return

    router = get_router()

    def _env_health_checker(model_id: str) -> bool:
        provider = _provider_prefix(model_id)
        return availability.get(provider, _is_provider_available(provider))

    router.set_health_checker(_env_health_checker)

    # Pre-mark unavailable models so the router doesn't try them
    try:
        from ..models.router import DEFAULT_CHAINS, ModelTier
    except ImportError:
        return

    for provider, available in availability.items():
        if not available:
            for tier_enum in ModelTier:
                if tier_enum == ModelTier.TIER_0:
                    continue
                chain = DEFAULT_CHAINS.get(tier_enum)
                if chain:
                    for m in chain:
                        if _provider_prefix(m) == provider:
                            router.mark_unavailable(m)

    logger.debug("Native ModelRouter configured with env-var health checker")


# NOTE: probe_and_update_tier_defaults() is intentionally NOT called here.
# It is called once from the FastAPI lifespan handler in server/app.py so that
# it runs at server startup only — not on every test import, which would mutate
# global _TIER_DEFAULTS and cause test-order dependencies.

# ---------------------------------------------------------------------------
# Provider dispatch
# ---------------------------------------------------------------------------


def get_chat_model(model_id: str, temperature: float = 0.0) -> Any:
    """Resolve a model ID string to a LangChain ``BaseChatModel`` instance.

    Parameters
    ----------
    model_id:
        A prefixed model ID such as ``gh:openai/gpt-4o`` or
        ``ollama:qwen2.5-coder``.
    temperature:
        Sampling temperature passed to the model.

    Returns
    -------
    A LangChain ``BaseChatModel`` instance.

    Raises
    ------
    ValueError
        If the provider prefix is not supported.
    ImportError
        If the required LangChain integration package is not installed.
    """
    model_id = (model_id or "").strip()
    if not model_id:
        raise ValueError("Model ID must be a non-empty string.")

    if model_id.startswith("gh:"):
        return _build_github_model(model_id[3:], temperature)

    if model_id.startswith("ollama:"):
        return _build_ollama_model(model_id[7:], temperature)

    if model_id.startswith("openai:"):
        return _build_openai_model(model_id[7:], temperature)

    if model_id.startswith("anthropic:"):
        return _build_anthropic_model(model_id[10:], temperature)

    if model_id.startswith("claude:"):
        return _build_anthropic_model(model_id[7:], temperature)

    if model_id.startswith("gemini:"):
        return _build_gemini_model(model_id[7:], temperature)

    if model_id == "notebooklm":
        return _build_notebooklm_model("", temperature)

    if model_id.startswith("notebooklm:"):
        return _build_notebooklm_model(model_id[11:], temperature)

    if model_id.startswith("local:"):
        return _build_local_onnx_model(model_id[6:], temperature)

    if model_id.startswith("lmstudio:"):
        return _build_lmstudio_model(model_id[9:], temperature)

    if model_id.startswith("local-api:"):
        return _build_local_api_model(model_id[10:], temperature)

    # Bare name without prefix -- treat as Ollama local model
    if not any(
        model_id.startswith(p)
        for p in (
            "openai:",
            "azure:",
            "local:",
            "windows-ai:",
            "anthropic:",
            "claude:",
            "gemini:",
            "notebooklm:",
            "lmstudio:",
            "local-api:",
        )
    ):
        return _build_ollama_model(model_id, temperature)

    raise ValueError(
        f"Unsupported model provider in '{model_id}'. "
        "Supported prefixes: gh:, ollama:, openai:, anthropic:/claude:, "
        "gemini:, notebooklm:, local:, lmstudio:, local-api:."
    )


def get_model_for_tier(tier: int, model_override: str | None = None) -> Any:
    """Return a chat model for the given agent tier.

    Resolution order:
    1. ``model_override`` argument
    2. Env var ``AGENTIC_MODEL_TIER_{tier}``
    3. Tier default from ``_TIER_DEFAULTS`` (set by probe)
    4. Walk the fallback chain trying each available provider
    """
    chain = get_model_candidates_for_tier(
        tier,
        model_override,
        include_unavailable=False,
        include_gh_backup=True,
    )
    last_err: Exception | None = None
    for model_id in chain:
        try:
            return get_chat_model(model_id)
        except (ValueError, ImportError) as exc:
            last_err = exc
            logger.debug("Fallback %s failed: %s", model_id, exc)
            continue

    raise ValueError(
        f"No available model for tier {tier}. "
        f"Checked: {chain}. "
        f"Last error: {last_err}"
    )


def get_model_candidates_for_tier(
    tier: int,
    model_override: str | None = None,
    *,
    include_unavailable: bool = False,
    include_gh_backup: bool = True,
) -> list[str]:
    """Return ordered candidate model IDs for a tier, including fallbacks.

    Resolution order:
    1. Per-step ``model_override`` (resolved, supports ``env:VAR|fallback``)
    2. Env var ``AGENTIC_MODEL_TIER_{tier}``
    3. Probed tier default from ``_TIER_DEFAULTS``
    4. Tier fallback chain from ``_TIER_FALLBACK_CHAINS``
    5. GitHub backup models (when ``GITHUB_TOKEN`` is configured)
    """
    pinned: list[str] = []

    if model_override:
        pinned.append(_resolve_model_override(model_override))

    env_key = f"AGENTIC_MODEL_TIER_{tier}"
    env_val = (os.environ.get(env_key) or "").strip()
    if env_val:
        pinned.append(env_val)

    default_id = _TIER_DEFAULTS.get(tier, _TIER_DEFAULTS.get(2, "ollama:qwen3:8b"))
    if default_id:
        pinned.append(default_id)

    fallback = list(_TIER_FALLBACK_CHAINS.get(tier, _TIER_FALLBACK_CHAINS.get(2, [])))

    if include_gh_backup and os.environ.get("GITHUB_TOKEN"):
        fallback.extend(_GH_BACKUP_MODELS)

    ordered_pinned = _dedupe_keep_order(pinned)
    ordered_fallback = _dedupe_keep_order(fallback)
    if include_unavailable:
        return _dedupe_keep_order(ordered_pinned + ordered_fallback)

    filtered_fallback = [
        m for m in ordered_fallback if _is_provider_available(_provider_prefix(m))
    ]
    return _dedupe_keep_order(ordered_pinned + filtered_fallback)


def is_retryable_model_error(exc: Exception) -> bool:
    """Heuristic classification for transient model/provider failures."""
    status_code = getattr(exc, "status_code", None)
    if status_code is None:
        response = getattr(exc, "response", None)
        status_code = getattr(response, "status_code", None)
    try:
        if int(status_code) in _TRANSIENT_HTTP_STATUS_CODES:
            return True
    except (TypeError, ValueError):
        pass

    cls = exc.__class__.__name__.lower()
    msg = str(exc).lower()

    if any(
        token in cls
        for token in (
            "ratelimit",
            "timeout",
            "apiconnection",
            "serviceunavailable",
            "temporar",
        )
    ):
        return True

    return any(
        token in msg
        for token in (
            "429",
            "too many requests",
            "rate limit",
            "quota exceeded",
            "resource exhausted",
            "temporarily unavailable",
            "service unavailable",
            "overloaded",
            "timeout",
            "timed out",
            "connection reset",
            "connection error",
            "upstream error",
            "try again later",
        )
    )


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Return deduplicated list preserving first-seen order."""
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        val = (item or "").strip()
        if not val or val in seen:
            continue
        seen.add(val)
        out.append(val)
    return out


def _resolve_model_override(model_override: str) -> str:
    """Resolve a model override string.

    Supported forms:
    - ``gh:openai/gpt-4o`` (direct model id)
    - ``ollama:deepseek-r1`` (direct model id)
    - ``env:VAR_NAME`` (required environment variable)
    - ``env:VAR_NAME|gh:openai/gpt-4o-mini`` (env with fallback)
    """
    if not model_override.startswith("env:"):
        return model_override

    raw = model_override[4:].strip()
    if not raw:
        raise ValueError("Invalid model override 'env:' (missing variable name).")

    if "|" in raw:
        env_key, fallback = raw.split("|", 1)
        env_key = env_key.strip()
        fallback = fallback.strip()
    else:
        env_key, fallback = raw, ""

    if not env_key:
        raise ValueError("Invalid model override: missing env var name.")

    env_val = os.environ.get(env_key, "").strip()
    if env_val:
        return env_val
    if fallback:
        return fallback

    raise ValueError(
        f"Model override requires environment variable '{env_key}', "
        "but it is not set."
    )


# ---------------------------------------------------------------------------
# Provider builders
# ---------------------------------------------------------------------------


def _build_github_model(model_name: str, temperature: float) -> Any:
    """Build a ChatOpenAI instance pointed at GitHub Models."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for GitHub Models. "
            "Install with: pip install langchain-openai"
        ) from exc

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError(
            "GITHUB_TOKEN environment variable is required for GitHub Models. "
            "Set it to a GitHub personal access token with 'models:read' scope."
        )

    logger.debug("Using GitHub Models: %s", model_name)
    return ChatOpenAI(
        model=model_name,
        base_url=_GH_BASE_URL,
        api_key=token,
        temperature=temperature,
    )


def _build_openai_model(model_name: str, temperature: float) -> Any:
    """Build a ChatOpenAI instance for direct OpenAI API."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for OpenAI models. "
            "Install with: pip install langchain-openai"
        ) from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for OpenAI models."
        )

    kwargs: dict[str, Any] = {
        "model": model_name,
        "api_key": api_key,
        "temperature": temperature,
    }

    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("OPENAI_API_BASE")
    if base_url:
        kwargs["base_url"] = base_url

    org = os.environ.get("OPENAI_ORG_ID")
    if org:
        kwargs["organization"] = org

    logger.debug("Using OpenAI model: %s", model_name)
    return ChatOpenAI(**kwargs)


def _build_anthropic_model(model_name: str, temperature: float) -> Any:
    """Build a ChatAnthropic instance."""
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError as exc:
        raise ImportError(
            "langchain-anthropic is required for Anthropic models. "
            "Install with: pip install langchain-anthropic"
        ) from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic models."
        )

    logger.debug("Using Anthropic model: %s", model_name)
    return ChatAnthropic(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
    )


def _build_gemini_model(model_name: str, temperature: float) -> Any:
    """Build a ChatGoogleGenerativeAI instance."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as exc:
        raise ImportError(
            "langchain-google-genai is required for Gemini models. "
            "Install with: pip install langchain-google-genai"
        ) from exc

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY (or GEMINI_API_KEY) is required for Gemini models."
        )

    logger.debug("Using Gemini model: %s", model_name)
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
    )


def _build_notebooklm_model(model_name: str, temperature: float) -> Any:
    """NotebookLM alias routed through Gemini models."""
    resolved = _resolve_notebooklm_model_name(model_name)
    logger.debug("Using NotebookLM alias via Gemini model: %s", resolved)
    return _build_gemini_model(resolved, temperature)


def _resolve_notebooklm_model_name(model_name: str) -> str:
    """Resolve the Gemini model used for NotebookLM alias."""
    raw = (model_name or "").strip()
    if raw:
        return raw

    env_model = (
        os.environ.get("NOTEBOOKLM_MODEL")
        or os.environ.get("NOTEBOOKLM_GEMINI_MODEL")
        or ""
    ).strip()
    if env_model:
        return env_model

    return "gemini-2.5-pro"


def _build_ollama_model(model_name: str, temperature: float) -> Any:
    """Build a ChatOllama instance for local Ollama server."""
    try:
        from langchain_ollama import ChatOllama
    except ImportError as exc:
        raise ImportError(
            "langchain-ollama is required for Ollama models. "
            "Install with: pip install langchain-ollama"
        ) from exc

    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    logger.debug("Using Ollama: %s at %s", model_name, base_url)
    return ChatOllama(
        model=model_name,
        base_url=base_url,
        temperature=temperature,
    )


def _build_lmstudio_model(model_name: str, temperature: float) -> Any:
    """Build a ChatOpenAI instance for local LM Studio server."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for LM Studio models. "
            "Install with: pip install langchain-openai"
        ) from exc

    base_url = os.environ.get("LMSTUDIO_HOST", "http://127.0.0.1:12340")
    if not base_url.endswith("/v1"):
        base_url = f"{base_url.rstrip('/')}/v1"

    logger.debug("Using LM Studio: %s at %s", model_name, base_url)
    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key="lm-studio",
        temperature=temperature,
    )


def _build_local_api_model(model_name: str, temperature: float) -> Any:
    """Build a ChatOpenAI instance for generic local OpenAI-compatible API."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise ImportError(
            "langchain-openai is required for local API models. "
            "Install with: pip install langchain-openai"
        ) from exc

    base_url = (
        os.getenv("OPENAI_BASE_URL")
        or os.getenv("OPENAI_API_BASE")
        or os.getenv("LOCAL_AI_API_BASE_URL")
        or os.getenv("LOCAL_OPENAI_BASE_URL")
        or "http://localhost:1234/v1"
    )
    if not base_url.endswith("/v1"):
        base_url = f"{base_url.rstrip('/')}/v1"

    logger.debug("Using Local API: %s at %s", model_name, base_url)
    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key="local-api",
        temperature=temperature,
    )


def _build_local_onnx_model(model_name: str, temperature: float) -> Any:
    """Build a minimal chat wrapper over repo-local ONNX via ``LLMClient``."""
    try:
        from langchain_core.language_models.chat_models import BaseChatModel
        from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
        from langchain_core.outputs import ChatGeneration, ChatResult
    except ImportError as exc:
        raise ImportError(
            "langchain-core is required for local ONNX chat wrapper. "
            "Install with: pip install langchain-core"
        ) from exc

    llm_client = _import_repo_llm_client()
    key = (model_name or "phi4mini").strip()

    class LocalOnnxChatModel(BaseChatModel):
        model_key: str = key
        default_temperature: float = temperature

        @property
        def _llm_type(self) -> str:
            return "local-onnx"

        def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
            return self

        def _messages_to_prompt(
            self,
            messages: list[BaseMessage],
        ) -> tuple[str, str | None]:
            system_text: str | None = None
            chunks: list[str] = []
            for msg in messages:
                if isinstance(msg, SystemMessage):
                    system_text = str(msg.content)
                elif isinstance(msg, HumanMessage):
                    chunks.append(f"User: {msg.content}")
                else:
                    chunks.append(f"Assistant: {msg.content}")
            prompt = "\n\n".join(chunks) if chunks else ""
            return prompt, system_text

        def _generate(
            self,
            messages: list[BaseMessage],
            stop: list[str] | None = None,
            run_manager: Any | None = None,
            **kwargs: Any,
        ) -> Any:
            prompt, system_text = self._messages_to_prompt(messages)
            response = llm_client.generate_text(
                model_name=f"local:{self.model_key}",
                prompt=prompt,
                system_instruction=system_text,
                temperature=float(kwargs.get("temperature", self.default_temperature)),
                max_tokens=int(kwargs.get("max_tokens", 4096)),
            )
            text = response
            if stop:
                for token in stop:
                    if token and token in text:
                        text = text.split(token, 1)[0]
                        break
            message = AIMessage(content=text)
            return ChatResult(generations=[ChatGeneration(message=message)])

    logger.warning(
        "Using local ONNX wrapper for 'local:%s'. This path is prompt-only and "
        "does not support structured tool-calling.",
        key,
    )
    return LocalOnnxChatModel()


def _import_repo_llm_client() -> Any:
    """Import repo ``tools.llm.llm_client`` with workspace fallback."""
    try:
        from tools.llm.llm_client import LLMClient

        return LLMClient
    except ImportError:
        repo_root = Path(__file__).resolve().parents[3]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        try:
            from tools.llm.llm_client import LLMClient

            return LLMClient
        except ImportError as exc:
            raise ImportError(
                "Local ONNX provider requires importing tools.llm.llm_client. "
                "Run from repo root or add the workspace root to PYTHONPATH."
            ) from exc
