"""
Contracts module - Message and schema definitions.

Exports:
- Message types: AgentMessage, StepResult, WorkflowResult
- Enums: MessageType, StepStatus
- Task schemas: TaskInput, TaskOutput, CodeGeneration*, CodeReview*, TestGeneration*
- Issue types: CodeIssue, Severity, IssueCategory, TestType, TestCase
"""

from .messages import AgentMessage, MessageType, StepResult, StepStatus, WorkflowResult
from .schemas import (  # Enums; Base classes; Code generation; Code review; Test generation
    CodeGenerationInput,
    CodeGenerationOutput,
    CodeIssue,
    CodeReviewInput,
    CodeReviewOutput,
    IssueCategory,
    Severity,
    TaskInput,
    TaskOutput,
    TestCase,
    TestGenerationInput,
    TestGenerationOutput,
    TestType,
)

__all__ = [
    # Messages
    "MessageType",
    "StepStatus",
    "AgentMessage",
    "StepResult",
    "WorkflowResult",
    # Schemas - enums
    "Severity",
    "IssueCategory",
    "TestType",
    # Schemas - base
    "TaskInput",
    "TaskOutput",
    # Schemas - code generation
    "CodeGenerationInput",
    "CodeGenerationOutput",
    # Schemas - code review
    "CodeIssue",
    "CodeReviewInput",
    "CodeReviewOutput",
    # Schemas - test generation
    "TestCase",
    "TestGenerationInput",
    "TestGenerationOutput",
]
