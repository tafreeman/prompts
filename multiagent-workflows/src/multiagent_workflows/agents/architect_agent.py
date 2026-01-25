"""
Architect Agent

Designs system architecture based on requirements.
Outputs tech stack recommendations, component diagrams, and API strategies.
"""

from __future__ import annotations

import json
from typing import Any, Dict

from multiagent_workflows.core.agent_base import AgentBase

SYSTEM_PROMPT = """You are a senior software architect with expertise in full-stack application design.

Your task is to design system architecture including:
1. Tech stack recommendation with justification
2. Component diagram (high-level architecture)
3. API strategy (REST/GraphQL, versioning)
4. Database choice and data flow
5. Authentication and authorization strategy
6. Deployment architecture
7. Scalability considerations

Follow these principles:
- Separation of concerns
- Domain-driven design where appropriate
- Security by design
- Performance optimization

Output your response as JSON with the following structure:
{
    "tech_stack": {
        "frontend": {"framework": "...", "justification": "..."},
        "backend": {"framework": "...", "justification": "..."},
        "database": {"type": "...", "justification": "..."},
        "infrastructure": {"platform": "...", "justification": "..."}
    },
    "component_diagram": "... (Mermaid diagram syntax)",
    "api_strategy": {
        "type": "REST|GraphQL",
        "versioning": "...",
        "authentication": "..."
    },
    "data_flow": "...",
    "deployment": {
        "strategy": "...",
        "environments": ["dev", "staging", "prod"]
    },
    "scalability": {
        "bottlenecks": [...],
        "recommendations": [...]
    }
}
"""


class ArchitectAgent(AgentBase):
    """
    Agent that designs system architecture.
    
    Takes requirements and produces:
    - Tech stack recommendations
    - Component diagrams
    - API strategy
    - Deployment architecture
    """
    
    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Design architecture based on requirements.
        
        Args:
            task: Contains 'requirements' and optional 'constraints'
            context: Execution context
            
        Returns:
            Architecture design as structured dict
        """
        requirements = task.get("requirements", "")
        constraints = task.get("constraints", "")
        user_stories = task.get("user_stories", "")
        
        prompt = self._build_prompt(requirements, constraints, user_stories)
        
        result = await self.call_model(
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more consistent output
            max_tokens=4096,
        )
        
        # Parse response
        architecture = self._parse_architecture(result.text)
        
        return {
            "architecture": architecture,
            "tech_stack": architecture.get("tech_stack", {}),
            "component_diagram": architecture.get("component_diagram", ""),
            "api_strategy": architecture.get("api_strategy", {}),
        }
    
    def _build_prompt(
        self,
        requirements: str,
        constraints: str,
        user_stories: str,
    ) -> str:
        """Build the architecture design prompt."""
        prompt_parts = ["## Requirements", "", requirements, ""]
        
        if user_stories:
            prompt_parts.extend([
                "## User Stories",
                "",
                user_stories,
                "",
            ])
        
        if constraints:
            prompt_parts.extend([
                "## Constraints",
                "",
                constraints,
                "",
            ])
        
        prompt_parts.extend([
            "## Task",
            "",
            "Design a comprehensive system architecture for the above requirements.",
            "Provide your response as valid JSON matching the specified structure.",
        ])
        
        return "\n".join(prompt_parts)
    
    def _parse_architecture(self, response: str) -> Dict[str, Any]:
        """Parse architecture from model response."""
        # Try to extract JSON from response
        try:
            # Look for JSON block
            if "```json" in response:
                start = response.index("```json") + 7
                end = response.index("```", start)
                json_str = response[start:end].strip()
            elif "```" in response:
                start = response.index("```") + 3
                end = response.index("```", start)
                json_str = response[start:end].strip()
            elif "{" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response
            
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            # Return raw response in structured format
            return {
                "raw_response": response,
                "tech_stack": {},
                "component_diagram": "",
                "api_strategy": {},
            }
