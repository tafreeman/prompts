"""
Verbose Hierarchical Logging System

Captures all multi-agent workflow execution details at 5 levels:
1. Workflow Execution
2. Step Execution
3. Agent Execution
4. Model Calls
5. Tool Invocations

Supports export to JSON and Markdown formats.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Configure module logger
logger = logging.getLogger(__name__)


def _utc_now() -> str:
    """Return current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _generate_id() -> str:
    """Generate a unique identifier."""
    import uuid
    return str(uuid.uuid4())[:8]


@dataclass
class LogEvent:
    """A single log event with hierarchical relationships."""
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    event_id: str
    parent_id: Optional[str] = None
    duration_ms: Optional[float] = None


@dataclass
class VerboseLogger:
    """
    Hierarchical logging system for multi-agent workflows.
    
    Captures all execution details for analysis and evaluation:
    - Workflow start/complete with metadata
    - Step execution within workflows
    - Agent execution within steps
    - Model calls with prompts and responses
    - Tool invocations with parameters and results
    
    Example:
        logger = VerboseLogger(workflow_id="wf-001", config={"level": "DEBUG"})
        wf_id = logger.log_workflow_start("fullstack_generation", {"input": "..."})
        step_id = logger.log_step_start(wf_id, "architecture_design")
        agent_id = logger.log_agent_start(step_id, "architect_agent", "gh:gpt-4o")
        call_id = logger.log_model_call(agent_id, "Design the architecture...", {})
        logger.log_model_response(call_id, "Here is the architecture...", {"tokens": 500})
        logger.log_agent_output(agent_id, {"architecture": "..."})
        logger.log_step_complete(step_id, "success", {"artifacts": [...]})
        logger.log_workflow_complete(wf_id, True, {"total_steps": 11})
    """
    
    workflow_id: str
    config: Dict[str, Any] = field(default_factory=dict)
    events: List[LogEvent] = field(default_factory=list)
    metrics: Dict[str, List[float]] = field(default_factory=lambda: defaultdict(list))
    _timers: Dict[str, float] = field(default_factory=dict)
    
    # Workflow metadata
    workflow_name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    success: bool = False
    
    # Full text storage for prompts/responses (for JSON export)
    _full_prompts: Dict[str, str] = field(default_factory=dict)
    _full_responses: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize logging configuration."""
        self.log_level = self.config.get("level", "DEBUG")
        # Enable full text storage for detailed JSON exports
        self.store_full_text = self.config.get("store_full_text", True)
        self._setup_console_logging()
    
    def _setup_console_logging(self) -> None:
        """Configure console logging based on config level."""
        level = getattr(logging, self.log_level.upper(), logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    
    def _emit(
        self,
        event_type: str,
        data: Dict[str, Any],
        parent_id: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> str:
        """Emit a log event and return its ID."""
        event_id = _generate_id()
        event = LogEvent(
            event_type=event_type,
            timestamp=_utc_now(),
            data=data,
            event_id=event_id,
            parent_id=parent_id,
            duration_ms=duration_ms,
        )
        self.events.append(event)
        
        # Console logging
        prefix = f"[WORKFLOW:{self.workflow_id}]"
        if "." in event_type:
            parts = event_type.split(".")
            prefix += f"[{parts[0].upper()}:{event_id}]"
        
        log_msg = f"{prefix} {event_type}: {self._summarize(data)}"
        
        if event_type.endswith(".error"):
            logger.error(log_msg)
        elif event_type.endswith(".complete"):
            logger.info(log_msg)
        elif event_type.endswith(".start"):
            logger.info(log_msg)
        else:
            logger.debug(log_msg)
        
        return event_id
    
    def _summarize(self, data: Dict[str, Any], max_len: int = 200) -> str:
        """Create a short summary of data for console logging."""
        summary_parts = []
        for key, value in data.items():
            if key in ("prompt", "response", "output", "system_prompt"):
                # Truncate long text fields
                if isinstance(value, str) and len(value) > 50:
                    value = value[:50] + "..."
            summary_parts.append(f"{key}={value}")
        summary = ", ".join(summary_parts)
        if len(summary) > max_len:
            summary = summary[:max_len] + "..."
        return summary
    
    def _start_timer(self, timer_id: str) -> None:
        """Start a timer for duration tracking."""
        self._timers[timer_id] = time.perf_counter()
    
    def _stop_timer(self, timer_id: str) -> float:
        """Stop a timer and return elapsed milliseconds."""
        if timer_id in self._timers:
            elapsed = (time.perf_counter() - self._timers[timer_id]) * 1000
            del self._timers[timer_id]
            return elapsed
        return 0.0
    
    # =========================================================================
    # Level 1: Workflow Execution
    # =========================================================================
    
    def log_workflow_start(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log workflow initiation."""
        self.workflow_name = workflow_name
        self.start_time = _utc_now()
        self._start_timer("workflow")
        
        data = {
            "name": workflow_name,
            "inputs": self._sanitize(inputs),
            "metadata": metadata or {},
        }
        return self._emit("workflow.start", data)
    
    def log_workflow_complete(
        self,
        workflow_id: str,
        success: bool,
        summary: Dict[str, Any],
    ) -> None:
        """Log workflow completion with metrics."""
        self.end_time = _utc_now()
        self.success = success
        duration_ms = self._stop_timer("workflow")
        
        # Calculate aggregate metrics
        total_tokens = sum(self.metrics.get("tokens", []))
        total_cost = sum(self.metrics.get("cost", []))
        
        data = {
            "success": success,
            "summary": summary,
            "total_duration_ms": duration_ms,
            "total_tokens": total_tokens,
            "estimated_cost_usd": total_cost,
        }
        self._emit("workflow.complete", data, parent_id=workflow_id, duration_ms=duration_ms)
    
    def log_workflow_error(self, workflow_id: str, error: Exception) -> None:
        """Log workflow-level error."""
        data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        self._emit("workflow.error", data, parent_id=workflow_id)
    
    # =========================================================================
    # Level 2: Step Execution
    # =========================================================================
    
    def log_step_start(
        self,
        workflow_id: str,
        step_name: str,
        step_id: Optional[str] = None,
        inputs: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Log workflow step start with inputs."""
        self._start_timer(f"step_{step_id or step_name}")
        
        data = {
            "name": step_name,
            "step_id": step_id,
            "inputs": self._sanitize(inputs) if inputs else {},
            "context": context or {},
        }
        return self._emit("step.start", data, parent_id=workflow_id)
    
    def log_step_complete(
        self,
        step_id: str,
        success: bool,
        outputs: Dict[str, Any],
    ) -> None:
        """Log step completion."""
        duration_ms = self._stop_timer(f"step_{step_id}")
        
        data = {
            "success": success,
            "outputs": self._sanitize(outputs) if outputs else {},
            "output_keys": list(outputs.keys()) if outputs else [],
            "artifact_count": len(outputs) if outputs else 0,
        }
        self._emit("step.complete", data, parent_id=step_id, duration_ms=duration_ms)
    
    def log_step_error(self, step_id: str, error: Exception) -> None:
        """Log step-level error."""
        data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        self._emit("step.error", data, parent_id=step_id)
    
    # =========================================================================
    # Level 3: Agent Execution
    # =========================================================================
    
    def log_agent_start(
        self,
        step_id: str,
        agent_name: str,
        model_id: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Log agent execution start."""
        self._start_timer(f"agent_{agent_name}")
        
        data = {
            "agent": agent_name,
            "model": model_id,
            "system_prompt": system_prompt[:200] + "..." if system_prompt and len(system_prompt) > 200 else system_prompt,
        }
        return self._emit("agent.start", data, parent_id=step_id)
    
    def log_agent_output(
        self,
        agent_id: str,
        output: Union[str, Dict[str, Any]],
        metrics: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log agent completion with output."""
        duration_ms = self._stop_timer(f"agent_{agent_id}")
        
        data = {
            "output_type": type(output).__name__,
            "output_size": len(str(output)),
            "metrics": metrics or {},
        }
        self._emit("agent.output", data, parent_id=agent_id, duration_ms=duration_ms)
    
    def log_agent_error(self, agent_id: str, error: Exception) -> None:
        """Log agent-level error."""
        data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        self._emit("agent.error", data, parent_id=agent_id)
    
    # =========================================================================
    # Level 4: Model Calls
    # =========================================================================
    
    def log_model_call(
        self,
        agent_id: str,
        model_id: str,
        prompt: str,
        params: Dict[str, Any],
    ) -> str:
        """Log model API call with full prompt storage."""
        self._start_timer(f"model_{agent_id}")
        
        data = {
            "model_id": model_id,
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "parameters": params,
        }
        call_id = self._emit("model.call", data, parent_id=agent_id)
        
        # Store full prompt for JSON export
        if self.store_full_text:
            self._full_prompts[call_id] = prompt
        
        return call_id
    
    def log_model_response(
        self,
        call_id: str,
        response: str,
        timing_ms: float,
        tokens: int,
        cost: float = 0.0,
    ) -> None:
        """Log model response with full response storage."""
        duration_ms = self._stop_timer(f"model_{call_id}")
        
        # Track metrics
        self.metrics["tokens"].append(tokens)
        self.metrics["cost"].append(cost)
        self.metrics["response_time_ms"].append(timing_ms)
        
        data = {
            "response_length": len(response),
            "response_preview": response[:100] + "..." if len(response) > 100 else response,
            "timing_ms": timing_ms,
            "tokens": tokens,
            "cost_usd": cost,
        }
        
        # Store full response for JSON export
        if self.store_full_text:
            self._full_responses[call_id] = response
        
        self._emit("model.response", data, parent_id=call_id, duration_ms=duration_ms)
    
    def log_model_error(self, call_id: str, error: Exception) -> None:
        """Log model call error."""
        data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        self._emit("model.error", data, parent_id=call_id)
    
    # =========================================================================
    # Level 5: Tool Invocations
    # =========================================================================
    
    def log_tool_invocation(
        self,
        agent_id: str,
        tool_name: str,
        params: Dict[str, Any],
    ) -> str:
        """Log tool usage."""
        self._start_timer(f"tool_{tool_name}")
        
        data = {
            "tool": tool_name,
            "parameters": params,
        }
        return self._emit("tool.call", data, parent_id=agent_id)
    
    def log_tool_result(
        self,
        tool_call_id: str,
        result: Any,
        success: bool = True,
    ) -> None:
        """Log tool result."""
        duration_ms = self._stop_timer(f"tool_{tool_call_id}")
        
        data = {
            "success": success,
            "result_type": type(result).__name__,
            "result_size": len(str(result)) if result else 0,
        }
        self._emit("tool.result", data, parent_id=tool_call_id, duration_ms=duration_ms)
    
    # =========================================================================
    # Utility Methods
    # =========================================================================
    
    def _sanitize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data by removing sensitive fields."""
        sensitive_keys = {"api_key", "token", "password", "secret", "credential"}
        sanitized = {}
        for key, value in data.items():
            if any(s in key.lower() for s in sensitive_keys):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize(value)
            else:
                sanitized[key] = value
        return sanitized
    
    def get_structured_log(self) -> Dict[str, Any]:
        """Return complete structured log for evaluation with full prompt/response records."""
        # Build model calls with full prompts and responses
        model_calls = []
        for e in self.events:
            if e.event_type == "model.call":
                call_record = {
                    "call_id": e.event_id,
                    "timestamp": e.timestamp,
                    "model_id": e.data.get("model_id"),
                    "prompt": self._full_prompts.get(e.event_id, e.data.get("prompt_preview")),
                    "parameters": e.data.get("parameters"),
                }
                # Find matching response
                for r in self.events:
                    if r.event_type == "model.response" and r.parent_id == e.event_id:
                        call_record["response"] = self._full_responses.get(
                            e.event_id, r.data.get("response_preview")
                        )
                        call_record["tokens"] = r.data.get("tokens")
                        call_record["timing_ms"] = r.data.get("timing_ms")
                        call_record["cost_usd"] = r.data.get("cost_usd")
                        break
                model_calls.append(call_record)

        return {
            "workflow_id": self.workflow_id,
            "workflow_name": self.workflow_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "success": self.success,
            "events": [
                {
                    "id": e.event_id,
                    "type": e.event_type,
                    "timestamp": e.timestamp,
                    "parent_id": e.parent_id,
                    "duration_ms": e.duration_ms,
                    "data": e.data,
                }
                for e in self.events
            ],
            # Full prompt/response records per model call
            "model_calls": model_calls,
            "metrics": {
                "total_tokens": sum(self.metrics.get("tokens", [])),
                "total_cost_usd": sum(self.metrics.get("cost", [])),
                "avg_response_time_ms": (
                    sum(self.metrics.get("response_time_ms", [])) /
                    len(self.metrics.get("response_time_ms", [1]))
                ),
                "event_count": len(self.events),
                "model_call_count": len(model_calls),
            },
        }
    
    def export_to_json(self, filepath: Union[str, Path]) -> None:
        """Export structured logs to JSON file."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_structured_log(), f, indent=2, default=str)
        
        logger.info(f"Exported logs to {path}")

    def save_logs(self, filepath: Union[str, Path]) -> None:
        """Alias for export_to_json for backward compatibility."""
        self.export_to_json(filepath)
    
    def export_to_markdown(self, filepath: Union[str, Path]) -> None:
        """Export human-readable log to Markdown."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        lines = [
            f"# Workflow Log: {self.workflow_name}",
            "",
            f"**Workflow ID**: {self.workflow_id}",
            f"**Start Time**: {self.start_time}",
            f"**End Time**: {self.end_time}",
            f"**Status**: {'✅ Success' if self.success else '❌ Failed'}",
            "",
            "## Summary Metrics",
            "",
            f"- Total Tokens: {sum(self.metrics.get('tokens', []))}",
            f"- Estimated Cost: ${sum(self.metrics.get('cost', [])):.4f}",
            f"- Total Events: {len(self.events)}",
            "",
            "## Event Timeline",
            "",
        ]
        
        for event in self.events:
            icon = "🔵" if event.event_type.endswith(".start") else (
                "✅" if event.event_type.endswith(".complete") else (
                    "❌" if event.event_type.endswith(".error") else "📝"
                )
            )
            duration = f" ({event.duration_ms:.0f}ms)" if event.duration_ms else ""
            lines.append(f"### {icon} {event.event_type}{duration}")
            lines.append(f"- **Time**: {event.timestamp}")
            lines.append(f"- **ID**: {event.event_id}")
            if event.parent_id:
                lines.append(f"- **Parent**: {event.parent_id}")
            for key, value in event.data.items():
                if key == "inputs" or key == "outputs":
                    lines.append(f"- **{key}**: (Detailed JSON in log file)")
                    continue
                if isinstance(value, str) and len(value) > 100:
                    value = value[:100] + "..."
                lines.append(f"- **{key}**: {value}")
            lines.append("")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        
        logger.info(f"Exported markdown log to {path}")
