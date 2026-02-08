import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Radio, Trophy } from "lucide-react";
import { useWorkflowStream } from "../hooks/useWorkflowStream";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import StepLogPanel from "../components/live/StepLogPanel";
import TokenCounter from "../components/live/TokenCounter";
import StatusBadge from "../components/common/StatusBadge";

export default function LivePage() {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();
  const { stepStates, events, workflowStatus, evaluation, error } = useWorkflowStream(
    runId ?? null
  );

  // Try to extract workflow name from events
  const workflowName = events.find((e) => e.type === "workflow_start");
  const wfName =
    workflowName?.type === "workflow_start"
      ? workflowName.workflow_name
      : undefined;
  const { data: dag } = useWorkflowDAG(wfName);

  const statusMap: Record<string, string> = {
    connecting: "pending",
    running: "running",
    evaluating: "running",
    completed: "success",
    error: "failed",
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 border-b border-white/5 px-6 py-4">
        <button onClick={() => navigate(-1)} className="btn-ghost p-1">
          <ArrowLeft className="h-4 w-4" />
        </button>
        <Radio className="h-4 w-4 text-red-400 animate-pulse" />
        <div className="flex-1">
          <h1 className="text-lg font-semibold">
            {wfName ?? runId ?? "Live Execution"}
          </h1>
          <p className="text-xs text-gray-600">{runId}</p>
        </div>
        <TokenCounter events={events} />
        <StatusBadge
          status={statusMap[workflowStatus] ?? "pending"}
          size="md"
        />
      </div>

      {/* Evaluation progress banner */}
      {workflowStatus === "evaluating" && (
        <div className="border-b border-accent-blue/20 bg-accent-blue/10 px-6 py-2 text-xs text-accent-blue">
          Evaluating workflow output and computing criterion scores...
        </div>
      )}

      {/* Error banner */}
      {error && (
        <div className="border-b border-red-500/20 bg-red-500/10 px-6 py-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* DAG */}
        <div className="flex-1">
          {dag ? (
            <WorkflowDAG
              dagNodes={dag.nodes}
              dagEdges={dag.edges}
              stepStates={stepStates}
            />
          ) : (
            <div className="flex h-full items-center justify-center text-gray-600">
              {workflowStatus === "connecting"
                ? "Connecting to execution stream..."
                : "Waiting for workflow DAG data..."}
            </div>
          )}
        </div>

        {/* Event log */}
        <div className="w-[350px] overflow-y-auto border-l border-white/5 p-4">
          {evaluation && (
            <div className="mb-3 rounded-lg border border-white/5 bg-surface-1 p-3">
              <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-wide text-gray-500">
                <Trophy className="h-3.5 w-3.5 text-amber-400" />
                Evaluation Score
              </div>
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-2xl font-semibold text-gray-100">
                    {evaluation.weighted_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-500">
                    Weighted / 100
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-300">
                    Grade {evaluation.grade}
                  </div>
                  <div
                    className={`text-xs ${
                      evaluation.passed ? "text-green-400" : "text-red-400"
                    }`}
                  >
                    {evaluation.passed ? "Passed" : "Needs improvement"}
                  </div>
                </div>
              </div>
            </div>
          )}
          <StepLogPanel events={events} />
        </div>
      </div>
    </div>
  );
}
