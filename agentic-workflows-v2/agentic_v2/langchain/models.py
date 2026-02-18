"""Model provider registry for the LangChain workflow engine.

Supported providers:
- GitHub Models          (prefix ``gh:``)            via OpenAI-compatible API
- Ollama                 (prefix ``ollama:``)        local or remote Ollama
- OpenAI                 (prefix ``openai:``)        direct OpenAI API
- Anthropic              (prefix ``anthropic:`` / ``claude:``)
- Gemini                 (prefix ``gemini:``)
- NotebookLM alias       (prefix ``notebooklm:``)    routes to Gemini model
- Local ONNX             (prefix ``local:``)         via repo ``LLMClient``

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
# Tier defaults (used when agents.yaml has no match)
# ---------------------------------------------------------------------------

_DEFAULT_HIGH_TIER_MODEL = "gemini:gemini-2.5-flash"

_TIER_DEFAULTS: dict[int, str] = {
    1: "gemini:gemini-2.0-flash-lite",
    2: "gemini:gemini-2.0-flash",
    3: _DEFAULT_HIGH_TIER_MODEL,
    4: _DEFAULT_HIGH_TIER_MODEL,
    5: _DEFAULT_HIGH_TIER_MODEL,
}

# GitHub Models base URL
_GH_BASE_URL = "https://models.inference.ai.azure.com"


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

    # Bare name without prefix — treat as Ollama local model
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
        )
    ):
        return _build_ollama_model(model_id, temperature)

    raise ValueError(
        f"Unsupported model provider in '{model_id}'. "
        "Supported prefixes: gh:, ollama:, openai:, anthropic:/claude:, "
        "gemini:, notebooklm:, local:."
    )


def get_model_for_tier(tier: int, model_override: str | None = None) -> Any:
    """Return a chat model for the given agent tier.

    Resolution order:
    1. ``model_override`` argument
    2. Env var ``AGENTIC_MODEL_TIER_{tier}``
    3. Tier default from ``_TIER_DEFAULTS``
    """
    if model_override:
        return get_chat_model(_resolve_model_override(model_override))

    env_key = f"AGENTIC_MODEL_TIER_{tier}"
    env_val = os.environ.get(env_key)
    if env_val:
        return get_chat_model(env_val)

    default_id = _TIER_DEFAULTS.get(tier, _TIER_DEFAULTS[2])
    return get_chat_model(default_id)


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
    """NotebookLM alias routed through Gemini models.

    NotebookLM itself is a product surface, not a direct model API in this
    runtime. We route to Gemini so users can keep a semantic ``notebooklm:``
    selector in workflow configuration.
    """
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

    # Default conservative fallback.
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


def _build_local_onnx_model(model_name: str, temperature: float) -> Any:
    """Build a minimal chat wrapper over repo-local ONNX via ``LLMClient``.

    This wrapper is intended for prompt-only steps. It does not implement
    provider-native tool-calling semantics.
    """
    try:
        from langchain_core.language_models.chat_models import BaseChatModel
        from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
        from langchain_core.outputs import ChatGeneration, ChatResult
    except ImportError as exc:
        raise ImportError(
            "langchain-core is required for local ONNX chat wrapper. "
            "Install with: pip install langchain-core"
        ) from exc

    LLMClient = _import_repo_llm_client()
    key = (model_name or "phi4mini").strip()

    class LocalOnnxChatModel(BaseChatModel):
        model_key: str = key
        default_temperature: float = temperature

        @property
        def _llm_type(self) -> str:
            return "local-onnx"

        def bind_tools(self, tools: Any, **kwargs: Any) -> Any:
            # ReAct agent can still run, but local ONNX path is prompt-only.
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
            response = LLMClient.generate_text(
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
