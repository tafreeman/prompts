"""
Reviewer Agent

Reviews code for security, quality, and best practices.
Identifies issues and provides recommendations.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from multiagent_workflows.core.agent_base import AgentBase


SYSTEM_PROMPT = """You are a senior security engineer and code quality expert.

Review code for:
1. Security vulnerabilities (injection, XSS, CSRF, etc.)
2. Performance issues and bottlenecks
3. Code quality and maintainability
4. Best practices violations
5. Error handling gaps
6. Type safety issues

For each issue found, provide:
- Severity level (critical/high/medium/low)
- Location in code (file and line if possible)
- Description of the issue
- Recommended fix

Output your response as JSON:
{
    "summary": "...",
    "issues": [
        {
            "severity": "critical|high|medium|low",
            "category": "security|performance|quality|best_practice",
            "location": "file:line",
            "description": "...",
            "recommendation": "..."
        }
    ],
    "metrics": {
        "security_score": 0-100,
        "quality_score": 0-100,
        "maintainability_score": 0-100
    },
    "passed": true|false
}
"""


class ReviewerAgent(AgentBase):
    """
    Agent that reviews code for security and quality.
    
    Analyzes code and produces:
    - List of issues with severity
    - Security findings
    - Quality recommendations
    - Overall scores
    """
    
    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Review code for issues.
        
        Args:
            task: Contains 'code' to review
            context: Execution context
            
        Returns:
            Review results with issues and scores
        """
        code = task.get("code", "")
        files = task.get("files", {})
        review_type = task.get("review_type", "full")  # full, security, quality
        
        # Combine code from files if provided
        if files and not code:
            code = self._combine_files(files)
        
        prompt = self._build_prompt(code, review_type)
        
        result = await self.call_model(
            prompt=prompt,
            temperature=0.1,  # Low temperature for consistent reviews
            max_tokens=4096,
        )
        
        # Parse review results
        review = self._parse_review(result.text)
        
        return {
            "review": review,
            "issues": review.get("issues", []),
            "passed": review.get("passed", True),
            "security_score": review.get("metrics", {}).get("security_score", 0),
            "quality_score": review.get("metrics", {}).get("quality_score", 0),
        }
    
    def _combine_files(self, files: Dict[str, str]) -> str:
        """Combine multiple files into a single review string."""
        parts = []
        for filename, content in files.items():
            parts.append(f"## File: {filename}")
            parts.append("")
            parts.append("```")
            parts.append(content)
            parts.append("```")
            parts.append("")
        return "\n".join(parts)
    
    def _build_prompt(self, code: str, review_type: str) -> str:
        """Build review prompt."""
        focus = {
            "full": "all aspects (security, quality, performance, best practices)",
            "security": "security vulnerabilities and risks",
            "quality": "code quality and maintainability",
        }.get(review_type, "all aspects")
        
        return f"""## Code Review Request

Review the following code, focusing on {focus}.

## Code to Review

{code}

## Instructions

1. Identify all issues with severity levels
2. Calculate scores for security, quality, and maintainability
3. Determine if the code passes review (no critical or high issues)
4. Provide your response as valid JSON

Be thorough but fair. Not every minor style issue needs to be reported.
Focus on issues that would matter in production."""
    
    def _parse_review(self, response: str) -> Dict[str, Any]:
        """Parse review results from model response."""
        try:
            # Extract JSON from response
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
            # Return structured error
            return {
                "summary": "Failed to parse review results",
                "issues": [],
                "metrics": {
                    "security_score": 50,
                    "quality_score": 50,
                    "maintainability_score": 50,
                },
                "passed": True,
                "raw_response": response,
            }
