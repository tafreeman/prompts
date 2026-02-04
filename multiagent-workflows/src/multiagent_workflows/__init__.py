"""Multi-Agent Workflows Package.

A comprehensive multi-agent development tool with evaluation framework
integration. Implements 4 pre-built software development workflows with
comprehensive logging and scoring rubrics.
"""

__version__ = "0.1.0"
__all__ = [
    "ModelManager",
    "WorkflowEngine",
    "VerboseLogger",
    "AgentBase",
    "WorkflowEvaluator",
]

from multiagent_workflows.core.agent_base import AgentBase
from multiagent_workflows.core.evaluator import WorkflowEvaluator
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.workflow_engine import WorkflowEngine
