import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Clock, Percent } from "lucide-react";
import { useRunDetail } from "../hooks/useRuns";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import RunDetailSteps from "../components/runs/RunDetail";
import StatusBadge from "../components/common/StatusBadge";
import DurationDisplay from "../components/common/DurationDisplay";
import type { StepStatus } from "../api/types";

export default function RunDetailPage() {
  const { filename } = useParams<{ filename: string }>();
  const navigate = useNavigate();
  const { data: run, isLoading } = useRunDetail(filename);
  const { data: dag } = useWorkflowDAG(run?.workflow_name);
  const [selectedStep, setSelectedStep] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center text-gray-600">
        Loading run...
      </div>
    );
  }

  if (!run) {
    return (
      <div className="flex h-full items-center justify-center text-gray-600">
        Run not found
      </div>
    );
  }

  // Build step states from completed run data
  const stepStates = new Map(
    run.steps.map((s) => [
      s.step_name,
      {
        status: s.status,
        durationMs: s.duration_ms,
        modelUsed: s.model_used ?? undefined,
        tokensUsed: s.tokens_used ?? undefined,
      },
    ])
  );

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 border-b border-white/5 px-6 py-4">
        <button onClick={() => navigate(-1)} className="btn-ghost p-1">
          <ArrowLeft className="h-4 w-4" />
        </button>
        <div className="flex-1">
          <h1 className="text-lg font-semibold">{run.workflow_name}</h1>
          <p className="text-xs text-gray-600">{run.run_id}</p>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-400">
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            <DurationDisplay ms={run.total_duration_ms} />
          </span>
          <span className="flex items-center gap-1">
            <Percent className="h-4 w-4" />
            {(run.success_rate * 100).toFixed(0)}%
          </span>
          <StatusBadge status={run.status as StepStatus} size="md" />
        </div>
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* DAG */}
        <div className="flex-1">
          {dag ? (
            <WorkflowDAG
              dagNodes={dag.nodes}
              dagEdges={dag.edges}
              stepStates={stepStates}
              onNodeClick={setSelectedStep}
            />
          ) : (
            <div className="flex h-full items-center justify-center text-gray-600">
              DAG unavailable
            </div>
          )}
        </div>

        {/* Step panels */}
        <div className="w-[450px] overflow-y-auto border-l border-white/5 p-4">
          <h2 className="mb-3 text-sm font-medium text-gray-400">
            Steps ({run.steps.length})
          </h2>
          <RunDetailSteps
            steps={run.steps}
            selectedStep={selectedStep}
            onSelectStep={setSelectedStep}
          />
        </div>
      </div>
    </div>
  );
}
