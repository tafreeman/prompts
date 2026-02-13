"""Agent routes."""

from __future__ import annotations

from fastapi import APIRouter

from ...storage import get_catalog_store
from ..models import AgentInfo, ListAgentsResponse

router = APIRouter(tags=["agents"])


@router.get("/agents", response_model=ListAgentsResponse)
async def list_agents():
    """List available agents."""
    agents: list[AgentInfo] = [
        AgentInfo(
            name="CoderAgent", description="Code generation and modification", tier="2"
        ),
        AgentInfo(
            name="ReviewerAgent",
            description="Code review and quality analysis",
            tier="2",
        ),
        AgentInfo(
            name="OrchestratorAgent", description="Dynamic workflow planning", tier="3"
        ),
        AgentInfo(
            name="ArchitectAgent",
            description="System design and architecture",
            tier="2",
        ),
        AgentInfo(
            name="TestAgent", description="Test generation and verification", tier="2"
        ),
    ]

    try:
        store = get_catalog_store()
        store.sync_agents_config()
        catalog_agents = store.list_agents()
        existing_names = {agent.name for agent in agents}

        for agent in catalog_agents:
            class_name = str(agent.get("class_name") or "")
            if not class_name or class_name in existing_names:
                continue
            description = str(agent.get("description") or agent.get("role") or "")
            agents.append(
                AgentInfo(
                    name=class_name,
                    description=description or f"{agent['agent_id']} agent",
                    tier=str(agent.get("tier") or "2"),
                )
            )
            existing_names.add(class_name)
    except Exception:
        # Keep API stable even if catalog sync fails.
        pass

    return ListAgentsResponse(agents=agents)
