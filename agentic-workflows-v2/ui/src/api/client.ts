import type {
  AgentInfo,
  DAGResponse,
  EvaluationDatasetsResponse,
  RunDetail,
  RunSummary,
  RunsSummary,
  WorkflowRunRequest,
  WorkflowRunResponse,
} from "./types";

const BASE = "/api";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

/** List available workflow names. */
export function listWorkflows(): Promise<{ workflows: string[] }> {
  return fetchJSON(`${BASE}/workflows`);
}

/** Get DAG structure for a workflow. */
export function getWorkflowDAG(name: string): Promise<DAGResponse> {
  return fetchJSON(`${BASE}/workflows/${encodeURIComponent(name)}/dag`);
}

/** List past runs. */
export function listRuns(workflow?: string, limit = 50): Promise<RunSummary[]> {
  const params = new URLSearchParams();
  if (workflow) params.set("workflow", workflow);
  params.set("limit", String(limit));
  return fetchJSON(`${BASE}/runs?${params}`);
}

/** Get full run detail. */
export function getRunDetail(filename: string): Promise<RunDetail> {
  return fetchJSON(`${BASE}/runs/${encodeURIComponent(filename)}`);
}

/** Get aggregate run stats. */
export function getRunsSummary(workflow?: string): Promise<RunsSummary> {
  const params = workflow ? `?workflow=${encodeURIComponent(workflow)}` : "";
  return fetchJSON(`${BASE}/runs/summary${params}`);
}

/** Trigger a workflow run. */
export function runWorkflow(
  request: WorkflowRunRequest
): Promise<WorkflowRunResponse> {
  return fetchJSON(`${BASE}/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}

/** List repository and local datasets for evaluation mode. */
export function listEvaluationDatasets(): Promise<EvaluationDatasetsResponse> {
  return fetchJSON(`${BASE}/eval/datasets`);
}

/** List available agents. */
export function listAgents(): Promise<{ agents: AgentInfo[] }> {
  return fetchJSON(`${BASE}/agents`);
}

/** Health check. */
export function healthCheck(): Promise<{ status: string; version: string }> {
  return fetchJSON(`${BASE}/health`);
}
