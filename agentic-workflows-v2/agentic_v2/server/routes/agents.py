"""Agent routes."""

from __future__ import annotations

from fastapi import APIRouter

from ..models import AgentInfo, ListAgentsResponse

router = APIRouter(tags=["agents"])


@router.get("/agents", response_model=ListAgentsResponse)
async def list_agents():
    """List available agents."""
    # Hardcoded for now based on current implementation
    # In a full implementation, this should use discovery
    agents = [
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
    return ListAgentsResponse(agents=agents)
