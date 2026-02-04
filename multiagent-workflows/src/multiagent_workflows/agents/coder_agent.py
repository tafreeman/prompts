"""Coder Agent.

Generates production-quality code based on specifications. Supports
multiple languages and frameworks.
"""

from __future__ import annotations

from typing import Any, Dict

from multiagent_workflows.core.agent_base import AgentBase

# Language-specific standards (dynamic injection based on industry best practices)
LANGUAGE_STANDARDS = {
    "python": {
        "features": "Modern Python 3.11+ features, type hints, async/await",
        "docs": "Google-style docstrings",
        "imports": "Absolute imports, group by stdlib/third-party/local",
    },
    "typescript": {
        "features": "TypeScript 5+, strict mode, ESM imports",
        "docs": "JSDoc comments for public APIs",
        "imports": "ESM import/export syntax",
    },
    "javascript": {
        "features": "ES2023+, async/await, destructuring",
        "docs": "JSDoc comments for public APIs",
        "imports": "ESM import/export syntax",
    },
    "java": {
        "features": "Java 17+, records, var for local inference",
        "docs": "Javadoc comments",
        "imports": "Organized imports (java.*, javax.*, then third-party)",
    },
    "csharp": {
        "features": "C# 11+, nullable reference types, records",
        "docs": "XML documentation comments",
        "imports": "Using directives at top, system first",
    },
}

SYSTEM_PROMPT = """You are an expert software developer generating production-quality code.

Follow these universal principles:
1. Clean code principles (SOLID, DRY, KISS)
2. Proper error handling and validation
3. Comprehensive type annotations/hints
4. Meaningful variable and function names
5. Appropriate comments for complex logic
6. Security best practices (input validation, escape outputs)

Generate complete, runnable code, not snippets.
"""


class CoderAgent(AgentBase):
    """Agent that generates production-quality code.

    Takes specifications and produces:
    - Complete source files
    - Proper structure and organization
    - Documentation and comments
    """

    async def _process(
        self,
        task: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Generate code based on specifications.

        Args:
            task: Contains 'specification', 'language', 'framework'
            context: Execution context with tech stack info

        Returns:
            Generated code files
        """
        specification = task.get("specification", "")
        language = task.get("language", "python")
        framework = task.get("framework", "")
        output_type = task.get("output_type", "backend")  # backend, frontend, fullstack

        # Get architecture context if available
        architecture = context.get("artifacts", {}).get("architecture_design", {})
        api_spec = context.get("artifacts", {}).get("api_design", {})

        prompt = self._build_prompt(
            specification=specification,
            language=language,
            framework=framework,
            output_type=output_type,
            architecture=architecture,
            api_spec=api_spec,
        )

        result = await self.call_model(
            prompt=prompt,
            temperature=0.2,  # Low temperature for consistent code
            max_tokens=8000,  # Allow longer outputs for complete code
        )

        # Parse generated code into files
        files = self._parse_code_files(result.text, language)

        return {
            "code": result.text,
            "files": files,
            "language": language,
            "framework": framework,
        }

    def _build_prompt(
        self,
        specification: str,
        language: str,
        framework: str,
        output_type: str,
        architecture: Dict[str, Any],
        api_spec: Dict[str, Any],
    ) -> str:
        """Build code generation prompt with dynamic language injection.

        Follows industry best practices: inject ONLY relevant language rules.
        """
        prompt_parts = [
            f"## Task: Generate {output_type} code",
            "",
            f"**Language**: {language}",
        ]

        # Inject language-specific standards (if available)
        if language.lower() in LANGUAGE_STANDARDS:
            std = LANGUAGE_STANDARDS[language.lower()]
            prompt_parts.extend(
                [
                    "",
                    "**Language Standards**:",
                    f"- Features: {std['features']}",
                    f"- Documentation: {std['docs']}",
                    f"- Imports: {std['imports']}",
                    "",
                ]
            )

        if framework:
            prompt_parts.append(f"**Framework**: {framework}")
            prompt_parts.append("")

        prompt_parts.extend(
            [
                "## Specification",
                "",
                specification,
                "",
            ]
        )

        if architecture:
            prompt_parts.extend(
                [
                    "## Architecture Context",
                    "",
                    str(architecture.get("tech_stack", "")),
                    "",
                ]
            )

        if api_spec:
            prompt_parts.extend(
                [
                    "## API Specification",
                    "",
                    str(api_spec),
                    "",
                ]
            )

        prompt_parts.extend(
            [
                "## Requirements",
                "",
                "Generate complete, production-ready code:",
                "- All necessary files with proper structure",
                "- Complete imports and dependencies",
                "- Type annotations/hints",
                "- Error handling",
                "- Documentation comments",
                "",
                "**Output Format**:",
                "```filename.ext",
                "// complete file contents",
                "```",
                "",
                "Generate multiple files if needed.",
            ]
        )

        return "\n".join(prompt_parts)

    def _parse_code_files(
        self,
        response: str,
        language: str,
    ) -> Dict[str, str]:
        """Parse code files from model response."""
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

            # First line might be filename or language
            first_line = lines[0].strip()
            content = lines[1] if len(lines) > 1 else ""

            # Check if first line is a filename
            if "." in first_line and "/" not in first_line and len(first_line) < 100:
                filename = first_line
            elif first_line in ("python", "typescript", "javascript", "tsx", "jsx"):
                # Generate filename based on content
                filename = self._infer_filename(content, first_line)
            else:
                # Use first line as content too
                content = block
                filename = self._infer_filename(content, language)

            files[filename] = content.strip()

        return files

    def _infer_filename(self, content: str, language: str) -> str:
        """Infer filename from content."""
        extension_map = {
            "python": ".py",
            "typescript": ".ts",
            "javascript": ".js",
            "tsx": ".tsx",
            "jsx": ".jsx",
        }

        ext = extension_map.get(language, ".txt")

        # Try to find class or function name
        if "class " in content:
            import re

            match = re.search(r"class\s+(\w+)", content)
            if match:
                return f"{match.group(1).lower()}{ext}"

        if "def " in content or "function " in content:
            import re

            match = re.search(r"(?:def|function)\s+(\w+)", content)
            if match:
                return f"{match.group(1).lower()}{ext}"

        return f"generated{ext}"
