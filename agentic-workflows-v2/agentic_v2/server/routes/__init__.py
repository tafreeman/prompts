"""API route modules for the Agentic server.

Submodules:
    :mod:`~agentic_v2.server.routes.health` -- ``GET /api/health`` liveness probe.
    :mod:`~agentic_v2.server.routes.agents` -- ``GET /api/agents`` agent discovery.
    :mod:`~agentic_v2.server.routes.workflows` -- Workflow execution, DAG
        visualization, run history, evaluation datasets, and SSE streaming.
"""

from __future__ import annotations
