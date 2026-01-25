"""Verbose logging for multi-agent workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import json


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


@dataclass
class LogEvent:
    event_type: str
    timestamp: str
    data: Dict[str, Any]
    event_id: int
    parent_id: Optional[int] = None


@dataclass
class VerboseLogger:
    """Structured logger for workflows, steps, agents, and model calls."""

    events: List[LogEvent] = field(default_factory=list)
    _next_id: int = 1

    def _emit(self, event_type: str, data: Dict[str, Any], parent_id: Optional[int] = None) -> int:
        event_id = self._next_id
        self._next_id += 1
        self.events.append(LogEvent(event_type, _now(), data, event_id, parent_id))
        return event_id

    def log_workflow_start(self, name: str, meta: Optional[Dict[str, Any]] = None) -> int:
        return self._emit("workflow.start", {"name": name, "meta": meta or {}})

    def log_workflow_complete(self, workflow_id: int, status: str, summary: Dict[str, Any]) -> None:
        self._emit("workflow.complete", {"status": status, "summary": summary}, parent_id=workflow_id)

    def log_step_start(self, workflow_id: int, name: str, meta: Optional[Dict[str, Any]] = None) -> int:
        return self._emit("step.start", {"name": name, "meta": meta or {}}, parent_id=workflow_id)

    def log_step_complete(self, step_id: int, status: str, summary: Dict[str, Any]) -> None:
        self._emit("step.complete", {"status": status, "summary": summary}, parent_id=step_id)

    def log_agent_start(self, step_id: int, agent_name: str, model_id: str) -> int:
        return self._emit("agent.start", {"agent": agent_name, "model": model_id}, parent_id=step_id)

    def log_agent_output(self, agent_id: int, output: str, meta: Optional[Dict[str, Any]] = None) -> None:
        payload = {"output": output, "meta": meta or {}}
        self._emit("agent.output", payload, parent_id=agent_id)

    def log_model_call(self, agent_id: int, prompt: str, parameters: Dict[str, Any]) -> int:
        payload = {"prompt": prompt, "parameters": parameters}
        return self._emit("model.call", payload, parent_id=agent_id)

    def log_model_response(self, model_call_id: int, response: str, meta: Optional[Dict[str, Any]] = None) -> None:
        payload = {"response": response, "meta": meta or {}}
        self._emit("model.response", payload, parent_id=model_call_id)

    def log_tool_invocation(self, step_id: int, tool_name: str, args: Dict[str, Any], result: Any) -> None:
        payload = {"tool": tool_name, "args": args, "result": result}
        self._emit("tool.call", payload, parent_id=step_id)

    def get_structured_log(self) -> Dict[str, Any]:
        return {
            "events": [
                {
                    "id": e.event_id,
                    "type": e.event_type,
                    "timestamp": e.timestamp,
                    "parent_id": e.parent_id,
                    "data": e.data,
                }
                for e in self.events
            ]
        }

    def export_to_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.get_structured_log(), f, indent=2)

    def export_to_markdown(self, path: str) -> None:
        lines = ["# Workflow Log", ""]
        for event in self.events:
            lines.append(f"## {event.event_type} ({event.timestamp})")
            lines.append(f"- id: {event.event_id}")
            if event.parent_id:
                lines.append(f"- parent: {event.parent_id}")
            for key, value in event.data.items():
                lines.append(f"- {key}: {value}")
            lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
