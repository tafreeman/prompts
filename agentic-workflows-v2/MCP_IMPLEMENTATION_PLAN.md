# MCP Client Implementation Plan for agentic-workflows-v2

> **Consolidated**: This plan has been completed. All implementation details, architecture overview,
> file manifest, and integration guide are now in [MCP_IMPLEMENTATION_COMPLETE.md](./MCP_IMPLEMENTATION_COMPLETE.md).
>
> The in-package guide is at [agentic_v2/integrations/mcp/README.md](./agentic_v2/integrations/mcp/README.md).

## Original Architecture Principles (preserved for reference)

1. **Strict Transport/Protocol Separation**: Transport layer (WebSocket/stdio) completely decoupled from JSON-RPC protocol
2. **Capability-Driven Discovery**: Fetch tools/resources/prompts only after successful capability negotiation
3. **Defensive Error Handling**: All external server calls wrapped with timeouts, never crash the orchestrator
4. **LRU Caching with Invalidation**: Cache expensive operations, invalidate on server notifications
5. **Schema Passthrough**: Preserve remote JSON Schema verbatim, don't attempt lossy Zod/Pydantic reconstruction

## Phase Summary (all complete)

| Phase | Description | LOC |
|-------|-------------|-----|
| 1 | Transport Layer (stdio, WebSocket) | 739 |
| 2 | Protocol Client (JSON-RPC) | 528 |
| 3 | Connection Manager (lifecycle, backoff) | 457 |
| 4 | Discovery Services (tools, resources, prompts) | 451 |
| 5 | LLM Adapters (tool, prompt, resource) | 601 |
| 6 | Output Safety (budget, storage) | 607 |
| 7 | Configuration (loader, expansion) | 998 |
| 8 | Testing (4 test modules + fixtures) | 1,631 |
| **Total** | | **6,012** |
