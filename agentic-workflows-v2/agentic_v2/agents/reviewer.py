"""Reviewer agent for code review tasks.

Aggressive design improvements:
- Multi-pass review (style, bugs, security)
- Severity-based issue categorization
- Actionable suggestions with diffs
- Review checklist customization
"""

from __future__ import annotations

import json
import re
from typing import Any, Optional

from ..contracts import (CodeIssue, CodeReviewInput, CodeReviewOutput,
                         IssueCategory, Severity)
from ..models import ModelTier
from .base import AgentConfig, BaseAgent
from .capabilities import CodeReviewMixin

REVIEW_SYSTEM_PROMPT = """You are an expert code reviewer with deep knowledge of software engineering best practices.

When reviewing code, analyze:
1. **Correctness**: Logic errors, edge cases, potential bugs
2. **Security**: Vulnerabilities, injection risks, unsafe practices  
3. **Performance**: Inefficiencies, unnecessary allocations, complexity
4. **Style**: Naming, formatting, documentation, readability
5. **Maintainability**: Code organization, duplication, coupling

For each issue found, provide:
- Severity: critical, high, medium, low, info
- Category: correctness, security, performance, style, maintainability
- Line number (if applicable)
- Clear explanation of the problem
- Suggested fix with code example

Format your response as JSON with this structure:
{
    "summary": "Brief overall assessment",
    "issues": [
        {
            "severity": "high",
            "category": "correctness",
            "line": 10,
            "description": "Problem description",
            "suggestion": "How to fix it",
            "code_suggestion": "fixed code snippet"
        }
    ],
    "positive_aspects": ["list of things done well"],
    "overall_score": 7.5
}"""


class ReviewerAgent(BaseAgent[CodeReviewInput, CodeReviewOutput], CodeReviewMixin):
    """Agent specialized for code review.

    Aggressive improvements:
    - Multi-pass review (configurable focus areas)
    - Structured JSON output
    - Severity scoring
    - Positive feedback inclusion
    - Review customization
    """

    def __init__(
        self,
        config: Optional[AgentConfig] = None,
        focus_areas: Optional[list[str]] = None,
        **kwargs,
    ):
        if config is None:
            config = AgentConfig(
                name="reviewer",
                description="Code review agent",
                system_prompt=REVIEW_SYSTEM_PROMPT,
                default_tier=ModelTier.TIER_2,
                max_iterations=3,
            )

        super().__init__(config=config, **kwargs)

        # Configurable focus areas
        self.focus_areas = focus_areas or [
            "correctness",
            "security",
            "performance",
            "style",
            "maintainability",
        ]

    def _format_task_message(self, task: CodeReviewInput) -> str:
        """Format code review task."""
        parts = [
            f"Please review the following {task.language} code:\n",
            "```" + task.language,
            task.code,
            "```",
        ]

        if task.context:
            parts.append(f"\nContext: {task.context}")

        if task.focus_areas:
            parts.append(f"\nFocus particularly on: {', '.join(task.focus_areas)}")
        else:
            parts.append(f"\nFocus areas: {', '.join(self.focus_areas)}")

        parts.append("\n\nProvide your review in the JSON format specified.")

        return "\n".join(parts)

    async def _is_task_complete(self, task: CodeReviewInput, response: str) -> bool:
        """Check if response contains valid review."""
        try:
            data = self._extract_json(response)
            return "issues" in data or "summary" in data
        except Exception:
            return False

    async def _parse_output(
        self, task: CodeReviewInput, response: str
    ) -> CodeReviewOutput:
        """Parse response into CodeReviewOutput."""
        try:
            data = self._extract_json(response)
        except Exception:
            # Fallback: create minimal output
            return CodeReviewOutput(
                success=True, summary=response[:500], issues=[], confidence=0.5
            )

        # Parse issues
        issues = []
        for issue_data in data.get("issues", []):
            try:
                severity = self._parse_severity(issue_data.get("severity", "info"))
                category = self._parse_category(issue_data.get("category", "style"))

                issue = CodeIssue(
                    severity=severity,
                    category=category,
                    line_number=issue_data.get("line"),
                    description=issue_data.get("description", ""),
                    suggestion=issue_data.get("suggestion"),
                    code_suggestion=issue_data.get("code_suggestion"),
                )
                issues.append(issue)
            except Exception:
                continue

        # Calculate approval based on issues
        critical_count = sum(1 for i in issues if i.severity == Severity.CRITICAL)
        high_count = sum(1 for i in issues if i.severity == Severity.HIGH)
        approved = critical_count == 0 and high_count <= 2

        # Calculate confidence based on response quality
        confidence = 0.9 if data.get("issues") is not None else 0.6

        return CodeReviewOutput(
            success=True,
            summary=data.get("summary", "Review complete"),
            issues=issues,
            approved=approved,
            overall_score=data.get("overall_score"),
            positive_aspects=data.get("positive_aspects", []),
            confidence=confidence,
        )

    async def _call_model(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        """Call LLM for code review."""
        # Default implementation for testing
        return {
            "content": json.dumps(
                {
                    "summary": "Code review complete",
                    "issues": [
                        {
                            "severity": "medium",
                            "category": "style",
                            "line": 1,
                            "description": "Consider adding type hints",
                            "suggestion": "Add type annotations for better clarity",
                        }
                    ],
                    "positive_aspects": ["Clear variable naming"],
                    "overall_score": 7.5,
                }
            )
        }

    def _extract_json(self, text: str) -> dict[str, Any]:
        """Extract JSON from response."""
        # Try to find JSON block
        json_match = re.search(r"```json\s*(.*?)```", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        # Try to find raw JSON
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))

        raise ValueError("No JSON found in response")

    def _parse_severity(self, value: str) -> Severity:
        """Parse severity string to enum."""
        value = value.lower()
        mapping = {
            "critical": Severity.CRITICAL,
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
            "info": Severity.INFO,
        }
        return mapping.get(value, Severity.INFO)

    def _parse_category(self, value: str) -> IssueCategory:
        """Parse category string to enum."""
        value = value.lower()
        mapping = {
            "correctness": IssueCategory.CORRECTNESS,
            "bug": IssueCategory.CORRECTNESS,
            "security": IssueCategory.SECURITY,
            "performance": IssueCategory.PERFORMANCE,
            "style": IssueCategory.STYLE,
            "maintainability": IssueCategory.MAINTAINABILITY,
            "documentation": IssueCategory.DOCUMENTATION,
        }
        return mapping.get(value, IssueCategory.STYLE)

    # -------------------------------------------------------------------------
    # CodeReviewMixin implementation
    # -------------------------------------------------------------------------

    async def review_code(
        self,
        code: str,
        language: str = "python",
        focus_areas: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """Review code and return issues."""
        task = CodeReviewInput(
            code=code, language=language, focus_areas=focus_areas or self.focus_areas
        )

        result = await self.run(task)

        return {
            "summary": result.summary,
            "issues": [
                {
                    "severity": i.severity.value,
                    "category": i.category.value,
                    "line": i.line_number,
                    "description": i.description,
                    "suggestion": i.suggestion,
                }
                for i in result.issues
            ],
            "approved": result.approved,
            "score": result.overall_score,
        }

    # -------------------------------------------------------------------------
    # Advanced features
    # -------------------------------------------------------------------------

    async def multi_pass_review(
        self, task: CodeReviewInput, passes: Optional[list[str]] = None
    ) -> CodeReviewOutput:
        """Perform multi-pass review with different focus areas.

        Each pass focuses on specific aspects, results are merged.
        """
        passes = passes or ["correctness", "security", "style"]
        all_issues = []
        summaries = []

        for focus in passes:
            # Create focused task
            focused_task = CodeReviewInput(
                code=task.code,
                language=task.language,
                context=task.context,
                focus_areas=[focus],
            )

            result = await self.run(focused_task)
            all_issues.extend(result.issues)
            summaries.append(f"{focus}: {result.summary}")

        # Deduplicate issues by line+description
        seen = set()
        unique_issues = []
        for issue in all_issues:
            key = (issue.line_number, issue.description[:50])
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)

        # Recalculate approval
        critical_count = sum(
            1 for i in unique_issues if i.severity == Severity.CRITICAL
        )
        high_count = sum(1 for i in unique_issues if i.severity == Severity.HIGH)

        return CodeReviewOutput(
            success=True,
            summary="\n".join(summaries),
            issues=unique_issues,
            approved=critical_count == 0 and high_count <= 2,
            confidence=0.95,
        )

    async def review_diff(
        self, original: str, modified: str, language: str = "python"
    ) -> CodeReviewOutput:
        """Review changes between original and modified code.

        Focuses on the diff rather than full code review.
        """
        import difflib

        # Generate diff
        diff = difflib.unified_diff(
            original.splitlines(),
            modified.splitlines(),
            lineterm="",
            fromfile="original",
            tofile="modified",
        )
        diff_text = "\n".join(diff)

        task = CodeReviewInput(
            code=modified,
            language=language,
            context=f"Review these changes:\n```diff\n{diff_text}\n```\n\nFocus on the modified lines.",
            focus_areas=["correctness", "security"],
        )

        return await self.run(task)
