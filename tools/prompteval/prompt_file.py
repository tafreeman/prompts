"""
Prompt File Format - Compatible with gh-models .prompt.yml

This module provides a Python implementation of the .prompt.yml format
used by gh-models for storing prompts with test data and evaluators.

The format supports:
- Model configuration (model, parameters)
- Message templates with {{variable}} placeholders
- Test data with input/expected pairs
- Evaluators (string-based and LLM-based)

Source pattern: https://github.com/github/gh-models (MIT License)
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class ModelParameters:
    """Model configuration parameters."""

    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None


@dataclass
class Message:
    """A conversation message."""

    role: str  # "system", "user", "assistant"
    content: str


@dataclass
class StringEvaluatorConfig:
    """String-based evaluator configuration."""

    contains: Optional[str] = None
    equals: Optional[str] = None
    starts_with: Optional[str] = None
    ends_with: Optional[str] = None


@dataclass
class LLMEvaluatorConfig:
    """LLM-based evaluator configuration."""

    model_id: str
    prompt: str
    choices: List[Dict[str, Any]]  # [{"choice": "1", "score": 0.0}, ...]
    system_prompt: Optional[str] = None


@dataclass
class Evaluator:
    """Evaluator definition."""

    name: str
    string: Optional[StringEvaluatorConfig] = None
    llm: Optional[LLMEvaluatorConfig] = None
    uses: Optional[str] = None  # e.g., "github/similarity"


@dataclass
class PromptFile:
    """Represents a .prompt.yml file structure.

    Compatible with gh-models format for evaluation and execution. Also
    supports loading from Markdown prompt files with YAML frontmatter.
    """

    name: str
    description: str = ""
    model: str = "openai/gpt-4o"
    model_parameters: ModelParameters = field(default_factory=ModelParameters)
    response_format: Optional[str] = None  # "text", "json_object", "json_schema"
    json_schema: Optional[Dict[str, Any]] = None
    messages: List[Message] = field(default_factory=list)
    test_data: List[Dict[str, Any]] = field(default_factory=list)
    evaluators: List[Evaluator] = field(default_factory=list)
    # Extended fields for pattern evaluation
    pattern: Optional[str] = None  # "react", "cove", "reflexion", "rag"
    difficulty: Optional[str] = None  # "beginner", "intermediate", "advanced"
    prompt_type: Optional[str] = None  # "how_to", "reference", "template", "guide"

    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> "PromptFile":
        """Load a prompt file from YAML or Markdown."""
        file_path = Path(file_path)

        # Handle Markdown files with YAML frontmatter
        if file_path.suffix.lower() == ".md":
            return cls._from_markdown(file_path)

        # Handle YAML files
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls._from_dict(data)

    @classmethod
    def _from_markdown(cls, file_path: Path) -> "PromptFile":
        """Create PromptFile from Markdown file with YAML frontmatter."""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract frontmatter
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
        if not fm_match:
            # No frontmatter, use filename as name
            return cls(
                name=file_path.stem.replace("-", " ").title(),
                description="",
                messages=[Message(role="user", content=content)],
            )

        fm_text, body = fm_match.group(1), fm_match.group(2)
        try:
            fm = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            fm = {}

        # Extract model parameters
        model_params_data = fm.get("model_parameters", {})
        model_params = ModelParameters(
            max_tokens=model_params_data.get("max_tokens"),
            temperature=model_params_data.get("temperature"),
            top_p=model_params_data.get("top_p"),
        )

        # Extract messages from markdown body
        messages = cls._extract_messages_from_markdown(body)

        # Extract test data from frontmatter or markdown table
        test_data = fm.get("test_data", [])
        if not test_data:
            test_data = cls._extract_test_data_from_markdown(body)

        return cls(
            name=fm.get("name", file_path.stem.replace("-", " ").title()),
            description=fm.get("description", ""),
            model=fm.get("model", "openai/gpt-4o"),
            model_parameters=model_params,
            response_format=fm.get("response_format"),
            json_schema=fm.get("json_schema"),
            messages=messages,
            test_data=test_data,
            evaluators=[],
            pattern=fm.get("pattern"),
            difficulty=fm.get("difficulty"),
            prompt_type=fm.get("type"),
        )

    @classmethod
    def _extract_messages_from_markdown(cls, body: str) -> List[Message]:
        """Extract system and user messages from markdown prompt sections."""
        messages = []

        # Look for ### System Prompt section
        system_match = re.search(
            r"###\s*System\s*Prompt\s*\n+```(?:text)?\n(.*?)```",
            body,
            re.DOTALL | re.IGNORECASE,
        )
        if system_match:
            messages.append(
                Message(role="system", content=system_match.group(1).strip())
            )

        # Look for ### User Prompt section
        user_match = re.search(
            r"###\s*User\s*Prompt\s*\n+```(?:text)?\n(.*?)```",
            body,
            re.DOTALL | re.IGNORECASE,
        )
        if user_match:
            messages.append(Message(role="user", content=user_match.group(1).strip()))

        # Fallback: Look for ## Prompt section with single code block
        if not messages:
            prompt_match = re.search(
                r"##\s*Prompt\s*\n+```(?:text)?\n(.*?)```",
                body,
                re.DOTALL | re.IGNORECASE,
            )
            if prompt_match:
                messages.append(
                    Message(role="user", content=prompt_match.group(1).strip())
                )

        # Last resort: use entire body as user message
        if not messages:
            messages.append(Message(role="user", content=body.strip()))

        return messages

    @classmethod
    def _extract_test_data_from_markdown(cls, body: str) -> List[Dict[str, Any]]:
        """Extract test data from ## Test Data markdown table."""
        test_data = []

        # Find Test Data section
        test_section_match = re.search(
            r"##\s*Test\s*Data.*?\n\|.*?\|.*?\|.*?\|\n\|[-\s|]+\|\n(.*?)(?:\n##|\n$|\Z)",
            body,
            re.DOTALL | re.IGNORECASE,
        )
        if not test_section_match:
            return test_data

        # Parse table rows
        table_content = test_section_match.group(1)
        for line in table_content.strip().split("\n"):
            if not line.strip() or line.strip().startswith("|--"):
                continue
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 3:
                # Format: | Scenario | Input Variables | Expected Contains |
                test_data.append(
                    {
                        "scenario": cols[0],
                        "input": cols[1],
                        "expected_contains": cols[2],
                    }
                )

        return test_data

    @classmethod
    def _from_dict(cls, data: Dict[str, Any]) -> "PromptFile":
        """Create PromptFile from dictionary."""
        # Parse model parameters
        params_data = data.get("modelParameters", {})
        model_params = ModelParameters(
            max_tokens=params_data.get("maxTokens"),
            temperature=params_data.get("temperature"),
            top_p=params_data.get("topP"),
        )

        # Parse messages
        messages = []
        for msg in data.get("messages", []):
            messages.append(
                Message(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                )
            )

        # Parse evaluators
        evaluators = []
        for eval_data in data.get("evaluators", []):
            string_config = None
            llm_config = None

            if "string" in eval_data:
                s = eval_data["string"]
                string_config = StringEvaluatorConfig(
                    contains=s.get("contains"),
                    equals=s.get("equals"),
                    starts_with=s.get("startsWith"),
                    ends_with=s.get("endsWith"),
                )

            if "llm" in eval_data:
                l = eval_data["llm"]
                llm_config = LLMEvaluatorConfig(
                    model_id=l.get("modelId", "openai/gpt-4o"),
                    prompt=l.get("prompt", ""),
                    choices=l.get("choices", []),
                    system_prompt=l.get("systemPrompt"),
                )

            evaluators.append(
                Evaluator(
                    name=eval_data.get("name", "unnamed"),
                    string=string_config,
                    llm=llm_config,
                    uses=eval_data.get("uses"),
                )
            )

        # Parse JSON schema if present
        json_schema = None
        if "jsonSchema" in data:
            raw_schema = data["jsonSchema"]
            if isinstance(raw_schema, str):
                json_schema = json.loads(raw_schema)
            else:
                json_schema = raw_schema

        return cls(
            name=data.get("name", "Unnamed Prompt"),
            description=data.get("description", ""),
            model=data.get("model", "openai/gpt-4o"),
            model_parameters=model_params,
            response_format=data.get("responseFormat"),
            json_schema=json_schema,
            messages=messages,
            test_data=data.get("testData", []),
            evaluators=evaluators,
        )

    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """Save prompt file to YAML."""
        file_path = Path(file_path)

        data = self._to_dict()

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
            )

    def _to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = {
            "name": self.name,
            "description": self.description,
            "model": self.model,
        }

        # Model parameters (only include if set)
        params = {}
        if self.model_parameters.max_tokens:
            params["maxTokens"] = self.model_parameters.max_tokens
        if self.model_parameters.temperature is not None:
            params["temperature"] = self.model_parameters.temperature
        if self.model_parameters.top_p is not None:
            params["topP"] = self.model_parameters.top_p
        if params:
            data["modelParameters"] = params

        # Response format
        if self.response_format:
            data["responseFormat"] = self.response_format
        if self.json_schema:
            data["jsonSchema"] = json.dumps(self.json_schema)

        # Messages
        data["messages"] = [
            {"role": msg.role, "content": msg.content} for msg in self.messages
        ]

        # Test data
        if self.test_data:
            data["testData"] = self.test_data

        # Evaluators
        if self.evaluators:
            evals = []
            for ev in self.evaluators:
                ev_data = {"name": ev.name}

                if ev.string:
                    s_data = {}
                    if ev.string.contains:
                        s_data["contains"] = ev.string.contains
                    if ev.string.equals:
                        s_data["equals"] = ev.string.equals
                    if ev.string.starts_with:
                        s_data["startsWith"] = ev.string.starts_with
                    if ev.string.ends_with:
                        s_data["endsWith"] = ev.string.ends_with
                    if s_data:
                        ev_data["string"] = s_data

                if ev.llm:
                    ev_data["llm"] = {
                        "modelId": ev.llm.model_id,
                        "prompt": ev.llm.prompt,
                        "choices": ev.llm.choices,
                    }
                    if ev.llm.system_prompt:
                        ev_data["llm"]["systemPrompt"] = ev.llm.system_prompt

                if ev.uses:
                    ev_data["uses"] = ev.uses

                evals.append(ev_data)
            data["evaluators"] = evals

        return data

    def template_messages(self, test_data: Dict[str, Any]) -> List[Message]:
        """Template messages with test data variables.

        Uses {{variable}} syntax compatible with gh-models.
        """
        templated = []

        for msg in self.messages:
            content = msg.content
            for key, value in test_data.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            templated.append(Message(role=msg.role, content=content))

        return templated

    def validate(self) -> List[str]:
        """Validate the prompt file structure.

        Returns list of validation errors (empty if valid).
        """
        errors = []

        if not self.name:
            errors.append("name is required")

        if not self.model:
            errors.append("model is required")

        if not self.messages:
            errors.append("at least one message is required")

        # Validate response format
        if self.response_format:
            valid_formats = ["text", "json_object", "json_schema"]
            if self.response_format not in valid_formats:
                errors.append(f"invalid responseFormat: {self.response_format}")

            if self.response_format == "json_schema" and not self.json_schema:
                errors.append(
                    "jsonSchema is required when responseFormat is 'json_schema'"
                )

        # Validate evaluators reference valid built-ins
        from tools.prompteval.builtin_evaluators import list_evaluators

        valid_builtins = [f"github/{e}" for e in list_evaluators()]

        for ev in self.evaluators:
            if ev.uses and ev.uses not in valid_builtins:
                # Check if it's a github/* pattern
                if ev.uses.startswith("github/"):
                    builtin_name = ev.uses.replace("github/", "")
                    if builtin_name not in list_evaluators():
                        errors.append(f"unknown built-in evaluator: {ev.uses}")

        return errors


# =============================================================================
# EVALUATION RUNNER
# =============================================================================


@dataclass
class EvaluationResult:
    """Result from a single evaluator."""

    evaluator_name: str
    score: float
    passed: bool
    details: str = ""


@dataclass
class TestResult:
    """Result from running a single test case."""

    test_case: Dict[str, Any]
    model_response: str
    evaluation_results: List[EvaluationResult]

    @property
    def passed(self) -> bool:
        """Did all evaluators pass?"""
        return all(r.passed for r in self.evaluation_results)


@dataclass
class EvaluationSummary:
    """Summary of prompt evaluation."""

    name: str
    description: str
    model: str
    test_results: List[TestResult]
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "testResults": [
                {
                    "testCase": r.test_case,
                    "modelResponse": r.model_response,
                    "evaluationResults": [
                        {
                            "evaluatorName": e.evaluator_name,
                            "score": e.score,
                            "passed": e.passed,
                            "details": e.details,
                        }
                        for e in r.evaluation_results
                    ],
                }
                for r in self.test_results
            ],
            "summary": {
                "totalTests": self.total_tests,
                "passedTests": self.passed_tests,
                "failedTests": self.failed_tests,
                "passRate": self.pass_rate,
            },
        }


class PromptEvaluator:
    """Evaluates prompts using the gh-models pattern.

    1. Load prompt file
    2. For each test case:
       a. Template messages with test data
       b. Call model to get completion
       c. Run evaluators on completion
    3. Aggregate results
    """

    def __init__(self, llm_client=None):
        """Initialize evaluator.

        Args:
            llm_client: Client with generate_text(model_name, prompt, temperature) method
        """
        self.llm_client = llm_client

    def evaluate(
        self, prompt_file: PromptFile, verbose: bool = False
    ) -> EvaluationSummary:
        """Run full evaluation on a prompt file.

        Args:
            prompt_file: Loaded PromptFile
            verbose: Print progress

        Returns:
            EvaluationSummary with all results
        """
        from tools.prompteval.builtin_evaluators import (
            EvaluatorRunner,
        )
        from tools.prompteval.builtin_evaluators import (
            StringEvaluator as BuiltinStringEvaluator,
        )

        runner = EvaluatorRunner(self.llm_client)
        test_results = []

        for i, test_case in enumerate(prompt_file.test_data):
            if verbose:
                print(f"Running test case {i + 1}/{len(prompt_file.test_data)}...")

            # Template messages
            messages = prompt_file.template_messages(test_case)

            # Build prompt for model
            full_prompt = ""
            for msg in messages:
                if msg.role == "system":
                    full_prompt += f"System: {msg.content}\n\n"
                elif msg.role == "assistant":
                    full_prompt += f"Assistant: {msg.content}\n\n"
                else:
                    full_prompt += f"{msg.content}\n"

            # Call model
            model_name = prompt_file.model
            if model_name.startswith("openai/"):
                model_name = f"gh:{model_name.split('/')[-1]}"

            try:
                response = self.llm_client.generate_text(
                    model_name=model_name,
                    prompt=full_prompt,
                    temperature=prompt_file.model_parameters.temperature or 0.7,
                )
            except Exception as e:
                response = f"[Error: {e}]"

            # Run evaluators
            eval_results = []
            for evaluator in prompt_file.evaluators:
                if evaluator.uses:
                    # Built-in evaluator (e.g., "github/similarity")
                    name = evaluator.uses.replace("github/", "")
                    result = runner.run_evaluator(
                        name,
                        test_case,
                        response,
                    )
                    eval_results.append(
                        EvaluationResult(
                            evaluator_name=evaluator.name,
                            score=result["score"],
                            passed=result["passed"],
                            details=result["details"],
                        )
                    )

                elif evaluator.string:
                    # String evaluator
                    str_eval = BuiltinStringEvaluator(
                        contains=evaluator.string.contains,
                        equals=evaluator.string.equals,
                        starts_with=evaluator.string.starts_with,
                        ends_with=evaluator.string.ends_with,
                    )
                    passed, score, details = str_eval.evaluate(response, test_case)
                    eval_results.append(
                        EvaluationResult(
                            evaluator_name=evaluator.name,
                            score=score,
                            passed=passed,
                            details=details,
                        )
                    )

                elif evaluator.llm:
                    # Custom LLM evaluator
                    # This would need implementation similar to runner.run_evaluator
                    eval_results.append(
                        EvaluationResult(
                            evaluator_name=evaluator.name,
                            score=0.0,
                            passed=False,
                            details="Custom LLM evaluators not yet implemented",
                        )
                    )

            test_results.append(
                TestResult(
                    test_case=test_case,
                    model_response=response,
                    evaluation_results=eval_results,
                )
            )

        # Aggregate
        passed_tests = sum(1 for r in test_results if r.passed)
        total_tests = len(test_results)

        return EvaluationSummary(
            name=prompt_file.name,
            description=prompt_file.description,
            model=prompt_file.model,
            test_results=test_results,
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=total_tests - passed_tests,
            pass_rate=(passed_tests / total_tests * 100) if total_tests > 0 else 0.0,
        )


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt File Handler")
    parser.add_argument("file", help="Path to .prompt.yml file")
    parser.add_argument("--validate", action="store_true", help="Validate the file")
    parser.add_argument("--show", action="store_true", help="Show file contents")

    args = parser.parse_args()

    prompt_file = PromptFile.load_from_file(args.file)

    if args.validate:
        errors = prompt_file.validate()
        if errors:
            print("Validation errors:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("✓ Valid prompt file")

    if args.show:
        print(f"Name: {prompt_file.name}")
        print(f"Description: {prompt_file.description}")
        print(f"Model: {prompt_file.model}")
        print(f"Messages: {len(prompt_file.messages)}")
        print(f"Test cases: {len(prompt_file.test_data)}")
        print(f"Evaluators: {len(prompt_file.evaluators)}")
        for ev in prompt_file.evaluators:
            ev_type = "string" if ev.string else ("llm" if ev.llm else "builtin")
            print(f"  - {ev.name} ({ev_type})")
