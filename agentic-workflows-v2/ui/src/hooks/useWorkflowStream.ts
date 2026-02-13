import { useEffect, useState, useCallback, useRef } from "react";
import { connectExecutionStream } from "../api/websocket";
import { getRunDetail } from "../api/client";
import type { EvaluationResult, ExecutionEvent, StepStatus } from "../api/types";

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
            modelUsed: event.model_used,
            tokensUsed: event.tokens_used,
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
          hard_gates: event.hard_gates,
          hard_gate_failures: event.hard_gate_failures,
          floor_violations: event.floor_violations,
          grade_capped: event.grade_capped,
          step_scores: event.step_scores,
          agent_scores: event.agent_scores,
          reporting_bundle: event.reporting_bundle,
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

    // Attempt to recover state from REST API in case of reconnection
    // This helps restore missed events after a disconnect
    let isSubscribed = true;
    
    const recoverState = async () => {
      try {
        // Try to fetch run detail - if it exists, we can backfill state
        // Note: This assumes runId matches the filename pattern
        // In production, the backend should expose /api/runs/by-id/{runId}
        const detail = await getRunDetail(runId);
        
        if (!isSubscribed) return;
        
        // Restore step states from completed steps
        const recoveredStates = new Map<string, StepState>();
        for (const step of detail.steps) {
          recoveredStates.set(step.step_name, {
            status: step.status,
            durationMs: step.duration_ms,
            modelUsed: step.model_used ?? undefined,
            tokensUsed: step.tokens_used ?? undefined,
          });
        }
        
        setStepStates(recoveredStates);
        
        // Set workflow status based on run state
        if (detail.extra?.evaluation) {
          setEvaluation(detail.extra.evaluation);
          setWorkflowStatus("completed");
        } else if (detail.status === "completed" || detail.status === "failed") {
          setWorkflowStatus("completed");
        } else {
          setWorkflowStatus("running");
        }
      } catch (err) {
        // If REST fetch fails, just proceed with WebSocket only
        console.debug("State recovery failed, using WebSocket only:", err);
      }
    };

    // Start state recovery in parallel with WebSocket connection
    recoverState();

    connectionRef.current = connectExecutionStream(runId, handleEvent);

    return () => {
      isSubscribed = false;
      connectionRef.current?.close();
    };
  }, [runId, handleEvent]);

  return { stepStates, events, workflowStatus, evaluation, error };
}
