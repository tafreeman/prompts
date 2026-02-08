import { useEffect, useState, useCallback, useRef } from "react";
import { connectExecutionStream } from "../api/websocket";
import type { ExecutionEvent, StepStatus } from "../api/types";

export interface StepState {
  status: StepStatus;
  startTime?: string;
  durationMs?: number;
  modelUsed?: string;
  tokensUsed?: number;
}

export interface WorkflowStreamState {
  stepStates: Map<string, StepState>;
  events: ExecutionEvent[];
  workflowStatus: "connecting" | "running" | "completed" | "error";
  error: string | null;
}

export function useWorkflowStream(runId: string | null): WorkflowStreamState {
  const [stepStates, setStepStates] = useState<Map<string, StepState>>(
    new Map()
  );
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [workflowStatus, setWorkflowStatus] =
    useState<WorkflowStreamState["workflowStatus"]>("connecting");
  const [error, setError] = useState<string | null>(null);
  const connectionRef = useRef<{ close: () => void } | null>(null);

  const handleEvent = useCallback((event: ExecutionEvent) => {
    setEvents((prev) => [...prev, event]);

    switch (event.type) {
      case "workflow_start":
        setWorkflowStatus("running");
        break;

      case "step_start":
        setStepStates((prev) => {
          const next = new Map(prev);
          next.set(event.step, {
            status: "running",
            startTime: event.timestamp,
          });
          return next;
        });
        break;

      case "step_end":
        setStepStates((prev) => {
          const next = new Map(prev);
          next.set(event.step, {
            status: event.status,
            durationMs: event.duration_ms,
            modelUsed: event.model_used,
            tokensUsed: event.tokens_used,
          });
          return next;
        });
        break;

      case "workflow_end":
        setWorkflowStatus("completed");
        break;

      case "error":
        setError(event.error);
        setWorkflowStatus("error");
        break;
    }
  }, []);

  useEffect(() => {
    if (!runId) return;

    setStepStates(new Map());
    setEvents([]);
    setWorkflowStatus("connecting");
    setError(null);

    connectionRef.current = connectExecutionStream(runId, handleEvent);

    return () => {
      connectionRef.current?.close();
    };
  }, [runId, handleEvent]);

  return { stepStates, events, workflowStatus, error };
}
