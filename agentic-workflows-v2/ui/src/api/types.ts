/** Mirrors server StepStatus enum. */
export type StepStatus =
  | "pending"
  | "running"
  | "success"
  | "failed"
  | "skipped"
  | "cancelled";

/** A node in the DAG visualization (from GET /api/workflows/{name}/dag). */
export interface DAGNode {
  id: string;
  agent: string | null;
  description: string;
  depends_on: string[];
  tier: string | null;
}

export interface DAGEdge {
  source: string;
  target: string;
}

/** Input parameter schema for a workflow. */
export interface WorkflowInputSchema {
  name: string;
  type: string;
  description: string;
  default: unknown;
  required: boolean;
  enum: string[] | null;
}

export interface DAGResponse {
  name: string;
  description: string;
  nodes: DAGNode[];
  edges: DAGEdge[];
  inputs?: WorkflowInputSchema[];
}

/** Summary of a single run (from GET /api/runs). */
export interface RunSummary {
  filename: string;
  run_id: string | null;
  workflow_name: string | null;
  status: string | null;
  success_rate: number | null;
  total_duration_ms: number | null;
  step_count: number | null;
  failed_step_count: number | null;
  start_time: string | null;
  end_time: string | null;
}

/** Full run detail (from GET /api/runs/{filename}). */
export interface RunDetail {
  run_id: string;
  workflow_name: string;
  status: string;
  success_rate: number;
  total_duration_ms: number;
  step_count: number;
  failed_step_count: number;
  start_time: string;
  end_time: string;
  steps: StepResult[];
}

export interface StepResult {
  step_name: string;
  status: StepStatus;
  duration_ms: number;
  model_used: string | null;
  tokens_used: number | null;
  tier: string | null;
  input: Record<string, unknown>;
  output: Record<string, unknown>;
  error: string | null;
}

/** Aggregate stats (from GET /api/runs/summary). */
export interface RunsSummary {
  total_runs: number;
  success: number;
  failed: number;
  avg_duration_ms: number | null;
  workflows: string[];
}

/** POST /api/run request. */
export interface WorkflowRunRequest {
  workflow: string;
  input_data: Record<string, unknown>;
  run_id?: string;
}

/** POST /api/run response. */
export interface WorkflowRunResponse {
  run_id: string;
  status: StepStatus;
}

/** WebSocket execution events. */
export type ExecutionEvent =
  | { type: "workflow_start"; run_id: string; workflow_name: string; timestamp: string }
  | { type: "step_start"; run_id: string; step: string; timestamp: string }
  | {
      type: "step_end";
      run_id: string;
      step: string;
      status: StepStatus;
      duration_ms: number;
      model_used?: string;
      tokens_used?: number;
      timestamp: string;
    }
  | { type: "workflow_end"; run_id: string; status: string; timestamp: string }
  | { type: "error"; run_id: string; error: string }
  | { type: "keepalive" }
  | { type: "connection_established"; run_id: string; message: string };

/** Agent info (from GET /api/agents). */
export interface AgentInfo {
  name: string;
  description: string;
  tier: string;
}
