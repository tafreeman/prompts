import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Radio } from "lucide-react";
import { useWorkflowStream } from "../hooks/useWorkflowStream";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import StepLogPanel from "../components/live/StepLogPanel";
import TokenCounter from "../components/live/TokenCounter";
import StatusBadge from "../components/common/StatusBadge";

export default function LivePage() {
  const { runId } = useParams<{ runId: string }>();
  const navigate = useNavigate();
  const { stepStates, events, workflowStatus, error } = useWorkflowStream(
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
          <StepLogPanel events={events} />
        </div>
      </div>
    </div>
  );
}
