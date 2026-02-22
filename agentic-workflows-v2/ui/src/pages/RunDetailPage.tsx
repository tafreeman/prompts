import { useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Clock, Percent, Trophy } from "lucide-react";
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

  const runSteps = run?.steps ?? [];

  // Build step states from completed run data
  const stepStates = useMemo(
    () =>
      new Map(
        runSteps.map((s) => [
          s.step_name,
          {
            status: s.status,
            durationMs: s.duration_ms,
            modelUsed: s.model_used ?? undefined,
            tokensUsed: s.tokens_used ?? undefined,
            modelInferred: s.metadata?.model_inferred === true,
          },
        ])
      ),
    [runSteps]
  );

  const edgeCounts = useMemo(() => {
    if (!dag) return new Map<string, number>();

    const counts = new Map<string, number>();
    for (const edge of dag.edges) {
      const source = runSteps.find((s) => s.step_name === edge.source);
      const target = runSteps.find((s) => s.step_name === edge.target);
      if (!source || !target) continue;
      if (source.status !== "success") continue;
      if (target.status === "pending") continue;

      counts.set(`${edge.source}->${edge.target}`, 1);
    }
    return counts;
  }, [dag, runSteps]);

  const kickbackEdges = useMemo(() => {
    if (!dag) return new Set<string>();
    const isReviewOrTest = (name: string) => /(review|test)/i.test(name);
    const isDevRework = (name: string) => /(rework|developer|generate|fix)/i.test(name);

    return new Set(
      dag.edges
        .filter((edge) => isReviewOrTest(edge.source) && isDevRework(edge.target))
        .map((edge) => `${edge.source}->${edge.target}`)
    );
  }, [dag]);

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

  const successPercent = run.success_rate <= 1 ? run.success_rate * 100 : run.success_rate;

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center gap-4 border-b border-white/5 px-6 py-4">
        <button onClick={() => navigate(-1)} className="btn-ghost p-1" title="Go back">
          <ArrowLeft className="h-4 w-4" />
        </button>
        <div className="flex-1">
          <h1 className="text-lg font-semibold">{run.workflow_name}</h1>
          <p className="text-xs text-gray-600">{run.run_id}</p>
        </div>
        <div className="flex items-center gap-4 text-sm text-gray-400">
          {run.extra?.evaluation && (
            <span className="flex items-center gap-1 text-amber-300">
              <Trophy className="h-4 w-4" />
              {run.extra.evaluation.weighted_score.toFixed(1)}
            </span>
          )}
          <span className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            <DurationDisplay ms={run.total_duration_ms} />
          </span>
          <span className="flex items-center gap-1">
            <Percent className="h-4 w-4" />
            {successPercent.toFixed(0)}%
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
              edgeCounts={edgeCounts}
              kickbackEdges={kickbackEdges}
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
          {run.extra?.evaluation && (
            <div className="mb-3 rounded-lg border border-white/10 bg-surface-1 p-3">
              <div className="mb-2 text-xs uppercase tracking-wide text-gray-500">
                Evaluation Result
              </div>
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-2xl font-semibold text-gray-100">
                    {run.extra.evaluation.weighted_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-500">Weighted / 100</div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium text-gray-300">
                    Grade {run.extra.evaluation.grade}
                  </div>
                  <div
                    className={`text-xs ${
                      run.extra.evaluation.passed
                        ? "text-green-400"
                        : "text-red-400"
                    }`}
                  >
                    {run.extra.evaluation.passed ? "Passed" : "Did not pass"}
                  </div>
                </div>
              </div>
            </div>
          )}
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
