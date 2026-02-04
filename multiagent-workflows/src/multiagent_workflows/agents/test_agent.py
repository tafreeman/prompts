"""Test Agent.

Generates comprehensive test suites for code. Supports unit,
integration, and end-to-end tests.
"""

from __future__ import annotations

from typing import Any, Dict, List

from multiagent_workflows.core.agent_base import AgentBase

SYSTEM_PROMPT = """You are a test automation expert specializing in comprehensive test coverage.

Generate tests including:
1. Unit tests (>80% coverage target)
2. Integration tests for component interactions
3. End-to-end tests for critical user flows
4. Edge case and error scenario tests
5. Performance tests where applicable

Use:
- pytest for Python, Jest for JavaScript/TypeScript
- Descriptive test names that explain what is being tested
- Proper mocking and fixtures
- Arrange-Act-Assert pattern
- Parameterized tests for multiple inputs

Generate complete, runnable test files with all imports and fixtures.
"""


class TestAgent(AgentBase):
    """Agent that generates comprehensive test suites.

    Takes code and produces:
    - Unit tests
    - Integration tests
    - E2E tests
    - Test fixtures and mocks
    """

    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate tests for provided code.

        Args:
            task: Contains 'code', 'language', 'test_types'
            context: Execution context

        Returns:
            Generated test files
        """
        code = task.get("code", "")
        files = task.get("files", {})
        language = task.get("language", "python")
        test_types = task.get("test_types", ["unit", "integration"])

        # Combine code from files if provided
        if files and not code:
            code = self._combine_files(files)

        prompt = self._build_prompt(code, language, test_types)

        result = await self.call_model(
            prompt=prompt,
            temperature=0.2,
            max_tokens=8000,
        )

        # Parse test files
        test_files = self._parse_test_files(result.text, language)

        return {
            "tests": result.text,
            "test_files": test_files,
            "test_types": test_types,
        }

    def _combine_files(self, files: Dict[str, str]) -> str:
        """Combine multiple files for test generation."""
        parts = []
        for filename, content in files.items():
            parts.append(f"## File: {filename}")
            parts.append("")
            parts.append("```")
            parts.append(content)
            parts.append("```")
            parts.append("")
        return "\n".join(parts)

    def _build_prompt(
        self,
        code: str,
        language: str,
        test_types: List[str],
    ) -> str:
        """Build test generation prompt."""
        test_framework = "pytest" if language == "python" else "Jest"

        type_descriptions = []
        if "unit" in test_types:
            type_descriptions.append("- Unit tests for individual functions/methods")
        if "integration" in test_types:
            type_descriptions.append("- Integration tests for component interactions")
        if "e2e" in test_types:
            type_descriptions.append("- End-to-end tests for complete user flows")

        return f"""## Test Generation Request

Generate comprehensive tests for the following code using {test_framework}.

## Code to Test

{code}

## Test Types Required

{chr(10).join(type_descriptions)}

## Requirements

1. Aim for >80% code coverage
2. Test happy paths and error cases
3. Include edge cases and boundary conditions
4. Use descriptive test names
5. Include proper mocking for external dependencies
6. Add fixtures for common test data
7. Use parameterized tests where appropriate

Format each test file as:
```test_filename.{language == 'python' and 'py' or 'test.ts'}
// test contents
```"""

    def _parse_test_files(
        self,
        response: str,
        language: str,
    ) -> Dict[str, str]:
        """Parse test files from model response."""
        files: Dict[str, str] = {}

        # Split by code blocks
        parts = response.split("```")

        for i in range(1, len(parts), 2):
            if i >= len(parts):
                break

            block = parts[i]
            lines = block.split("\n", 1)

            if len(lines) < 2:
                continue

            first_line = lines[0].strip()
            content = lines[1] if len(lines) > 1 else ""

            # Determine filename
            if first_line.startswith("test_") or first_line.endswith(".test.ts"):
                filename = first_line
            elif first_line in ("python", "typescript", "javascript"):
                filename = (
                    f"test_generated.{'py' if first_line == 'python' else 'test.ts'}"
                )
            else:
                filename = (
                    f"test_generated.{'py' if language == 'python' else 'test.ts'}"
                )

            files[filename] = content.strip()

        return files
