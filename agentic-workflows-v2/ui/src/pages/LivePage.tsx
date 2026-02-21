import { useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Radio, Trophy, ChevronDown, ChevronRight } from "lucide-react";
import { useWorkflowStream } from "../hooks/useWorkflowStream";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import StepLogPanel from "../components/live/StepLogPanel";
import TokenCounter from "../components/live/TokenCounter";
import StatusBadge from "../components/common/StatusBadge";
import type { EvaluationResult } from "../api/types";

const WIDTH_CLASS_BY_DECILE: Record<number, string> = {
  0: "w-0",
  10: "w-[10%]",
  20: "w-[20%]",
  30: "w-[30%]",
  40: "w-[40%]",
  50: "w-[50%]",
  60: "w-[60%]",
  70: "w-[70%]",
  80: "w-[80%]",
  90: "w-[90%]",
  100: "w-full",
};

function scoreWidthClass(percent: number): string {
  const clamped = Math.max(0, Math.min(100, percent));
  const decile = Math.floor(clamped / 10) * 10;
  return WIDTH_CLASS_BY_DECILE[decile] ?? "w-0";
}

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

  const edgeCounts = useMemo(() => {
    if (!dag) return new Map<string, number>();

    const counts = new Map<string, number>();
    const incoming = new Map<string, string[]>();
    for (const edge of dag.edges) {
      const key = `${edge.source}->${edge.target}`;
      incoming.set(edge.target, [...(incoming.get(edge.target) ?? []), edge.source]);
      counts.set(key, 0);
    }

    const completedSuccess = new Set<string>();
    for (const event of events) {
      if (event.type === "step_end" && event.status === "success") {
        completedSuccess.add(event.step);
      }

      if (event.type === "step_start") {
        for (const source of incoming.get(event.step) ?? []) {
          if (!completedSuccess.has(source)) continue;
          const edgeId = `${source}->${event.step}`;
          counts.set(edgeId, (counts.get(edgeId) ?? 0) + 1);
        }
      }
    }

    return counts;
  }, [dag, events]);

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
        <button onClick={() => navigate(-1)} className="btn-ghost p-1" title="Go back">
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
              edgeCounts={edgeCounts}
              kickbackEdges={kickbackEdges}
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
            <EvaluationCard evaluation={evaluation} />
          )}
          <StepLogPanel events={events} />
        </div>
      </div>
    </div>
  );
}

/* ── Single criterion row with score bar ── */
function CriterionRow({
  criterion: c,
}: Readonly<{ criterion: EvaluationResult["criteria"][number] }>) {
  const pct = c.max_score > 0 ? (c.score / c.max_score) * 100 : 0;
  const clampedPct = Math.min(pct, 100);
  const widthClass = scoreWidthClass(clampedPct);

  let barColor = "bg-red-500";
  if (pct >= 80) barColor = "bg-green-500";
  else if (pct >= 50) barColor = "bg-amber-500";

  return (
    <div>
      <div className="flex items-center justify-between text-xs">
        <span className="truncate text-gray-300">{c.criterion}</span>
        <span className="ml-2 flex-shrink-0 tabular-nums text-gray-400">
          {c.score}/{c.max_score}
          {c.weight !== 1 && (
            <span className="ml-1 text-gray-600">&times;{c.weight}</span>
          )}
        </span>
      </div>
      <div className="mt-0.5 h-1 w-full rounded-full bg-white/5">
        <div className={`h-full rounded-full ${barColor} ${widthClass} transition-all`} />
      </div>
    </div>
  );
}

/* ── Evaluation score card with expandable criteria breakdown ── */
function EvaluationCard({ evaluation }: Readonly<{ evaluation: EvaluationResult }>) {
  const [expanded, setExpanded] = useState(false);
  const hasCriteria = evaluation.criteria.length > 0;

  return (
    <div className="mb-3 rounded-lg border border-white/5 bg-surface-1 p-3">
      {/* Summary row */}
      <div className="mb-2 flex items-center gap-2 text-xs uppercase tracking-wide text-gray-500">
        <Trophy className="h-3.5 w-3.5 text-amber-400" />
        Evaluation Score
      </div>
      <div className="flex items-end justify-between">
        <div>
          <div className="text-2xl font-semibold text-gray-100">
            {evaluation.weighted_score.toFixed(1)}
          </div>
          <div className="text-xs text-gray-500">Weighted / 100</div>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium text-gray-300">
            Grade {evaluation.grade}
          </div>
          <div
            className={`text-xs ${evaluation.passed ? "text-green-400" : "text-red-400"}`}
          >
            {evaluation.passed ? "Passed" : "Needs improvement"}
          </div>
        </div>
      </div>

      {/* Threshold + rubric info */}
      <div className="mt-2 flex items-center justify-between text-[10px] text-gray-600">
        <span>Threshold: {evaluation.pass_threshold}</span>
        <span className="truncate ml-2">{evaluation.rubric}</span>
      </div>

      {/* Toggle for criteria breakdown */}
      {hasCriteria && (
        <>
          <button
            onClick={() => setExpanded((prev) => !prev)}
            className="mt-3 flex w-full items-center gap-1 text-xs text-gray-400 hover:text-gray-200 transition-colors"
          >
            {expanded ? (
              <ChevronDown className="h-3.5 w-3.5" />
            ) : (
              <ChevronRight className="h-3.5 w-3.5" />
            )}
            <span>{expanded ? "Hide" : "Show"} criteria breakdown ({evaluation.criteria.length})</span>
          </button>

          {expanded && (
            <div className="mt-2 space-y-2">
              {evaluation.criteria.map((c) => (
                <CriterionRow key={c.criterion} criterion={c} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
