import { useEffect, useState, useCallback, useRef } from "react";
import { connectExecutionStream } from "../api/websocket";
import type { EvaluationResult, ExecutionEvent, StepStatus } from "../api/types";

export interface StepState {
  status: StepStatus;
  startTime?: string;
  durationMs?: number;
  modelUsed?: string;
  tokensUsed?: number;
  tier?: string | null;
  input?: Record<string, unknown>;
  output?: Record<string, unknown>;
  error?: string | null;
}

export interface WorkflowStreamState {
  stepStates: Map<string, StepState>;
  events: ExecutionEvent[];
  workflowStatus: "connecting" | "running" | "evaluating" | "completed" | "error";
  evaluation: EvaluationResult | null;
  error: string | null;
}

export function useWorkflowStream(runId: string | null): WorkflowStreamState {
  const [stepStates, setStepStates] = useState<Map<string, StepState>>(
    new Map()
  );
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [workflowStatus, setWorkflowStatus] =
    useState<WorkflowStreamState["workflowStatus"]>("connecting");
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
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
            modelUsed: event.model_used ?? undefined,
            tokensUsed: event.tokens_used ?? undefined,
            tier: event.tier,
            input: event.input,
            output: event.output,
            error: event.error,
          });
          return next;
        });
        break;

      case "workflow_end":
        setWorkflowStatus("completed");
        break;

      case "evaluation_start":
        setWorkflowStatus("evaluating");
        break;

      case "evaluation_complete":
        setEvaluation({
          enabled: true,
          rubric: event.rubric,
          criteria: event.criteria,
          overall_score: event.overall_score,
          weighted_score: event.weighted_score,
          grade: event.grade,
          passed: event.passed,
          pass_threshold: event.pass_threshold,
          generated_at: event.timestamp,
        });
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
    setEvaluation(null);
    setWorkflowStatus("connecting");
    setError(null);

    connectionRef.current = connectExecutionStream(runId, handleEvent);

    return () => {
      connectionRef.current?.close();
    };
  }, [runId, handleEvent]);

  return { stepStates, events, workflowStatus, evaluation, error };
}
