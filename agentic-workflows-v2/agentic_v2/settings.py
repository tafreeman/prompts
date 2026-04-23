"""Centralised application settings.

All environment variable reads for agentic_v2 core modules go through this
module.  Uses pydantic-settings so the app fails fast at startup when a
required variable is missing, and so that precedence is documented in one
place.

Precedence (highest to lowest):
1. Actual environment variables (``os.environ``)
2. ``.env`` file at the repo root (loaded by pydantic-settings automatically)
3. Defaults defined on the ``Settings`` class

Usage::

    from agentic_v2.settings import get_settings

    settings = get_settings()
    if settings.agentic_tracing:
        ...
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings sourced from environment variables.

    Precedence: env vars > .env file > field defaults.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- OTEL / tracing ---
    agentic_tracing: bool = Field(default=False, description="Enable OTLP tracing")
    agentic_trace_sensitive: bool = Field(
        default=False, description="Include prompt/response content in traces"
    )
    otel_exporter_otlp_endpoint: str = Field(
        default="http://localhost:4317", description="OTLP exporter endpoint"
    )
    otel_exporter_otlp_protocol: str = Field(
        default="grpc", description="OTLP protocol: grpc or http/protobuf"
    )
    otel_service_name: str = Field(
        default="agentic-workflows-v2", description="Service name for traces"
    )

    # --- Agent loader ---
    agentic_external_agents_dir: str | None = Field(
        default=None, description="Directory containing external agent definitions"
    )

    # --- Runtime ---
    shell: str = Field(default="/bin/bash", description="Shell for subprocess execution")

    # --- LLM placeholder mode ---
    agentic_no_llm: bool = Field(
        default=False,
        description=(
            "When true, get_client() and get_chat_model() both install a "
            "deterministic placeholder so demos and CI can run without API "
            "keys. The native-engine path (get_client()) has no extra "
            "dependencies. The LangChain-adapter path (get_chat_model()) "
            "still requires the [langchain] install extra — without it, "
            "get_chat_model() raises ImportError even under the flag. See "
            "docs/NO_LLM_MODE.md."
        ),
    )

    # --- Tool: file operations ---
    agentic_file_base_dir: str | None = Field(
        default=None, description="Base directory for file operations (sandbox root)"
    )

    # --- Tool: HTTP operations ---
    agentic_block_private_ips: bool = Field(
        default=False, description="Block HTTP requests to private/loopback IPs"
    )

    # --- Tool: memory operations ---
    agentic_memory_path: str | None = Field(
        default=None, description="Path to persistent memory store"
    )

    # --- MCP ---
    max_mcp_output_tokens: int | None = Field(
        default=None, description="Token budget cap for MCP tool output"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the cached application settings singleton."""
    return Settings()
