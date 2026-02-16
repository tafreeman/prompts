import { useEffect, useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Radio, Trophy, ChevronDown, ChevronRight } from "lucide-react";
import { useWorkflowStream } from "../hooks/useWorkflowStream";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import StepLogPanel from "../components/live/StepLogPanel";
import LiveStepDetails from "../components/live/LiveStepDetails";
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
  const [selectedStep, setSelectedStep] = useState<string | null>(null);
  const { stepStates, events, workflowStatus, evaluation, error } = useWorkflowStream(
    runId ?? null
  );

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

  // Step progress counter
  const completedCount = useMemo(() => {
    let count = 0;
    if (stepStates) {
      for (const [, state] of stepStates) {
        if (state.status === "success" || state.status === "failed" || state.status === "skipped") count++;
      }
    }
    return count;
  }, [stepStates]);

  const totalSteps = dag?.nodes.length ?? 0;

  const runningStep = useMemo(() => {
    if (!stepStates || stepStates.size === 0) return null;
    for (const [name, state] of stepStates) {
      if (state.status === "running") return name;
    }
    return null;
  }, [stepStates]);

  useEffect(() => {
    if (!runningStep) return;
    setSelectedStep((prev) => (prev === runningStep ? prev : runningStep));
  }, [runningStep]);

  const statusMap: Record<string, string> = {
    connecting: "pending",
    running: "running",
    evaluating: "running",
    completed: "success",
    error: "failed",
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header — compact single row */}
      <div className="flex items-center gap-3 border-b border-white/5 px-4 py-2.5">
        <button type="button" onClick={() => navigate(-1)} className="btn-ghost p-1" title="Go back">
          <ArrowLeft className="h-4 w-4" />
        </button>
        <Radio className="h-3.5 w-3.5 text-red-400 animate-pulse" />
        <div className="min-w-0 flex-1">
          <h1 className="truncate text-sm font-semibold">
            {wfName ?? "Live Execution"}
          </h1>
        </div>

        {/* Progress pill */}
        {totalSteps > 0 && (
          <div className="flex items-center gap-1.5 rounded-full bg-surface-2 px-2.5 py-1 text-[11px] text-gray-400">
            <span className="tabular-nums">{completedCount}/{totalSteps}</span>
            <span className="text-gray-600">steps</span>
          </div>
        )}

        <TokenCounter events={events} />
        <StatusBadge
          status={statusMap[workflowStatus] ?? "pending"}
          size="md"
        />
      </div>

      {/* Evaluating / error banners — slimmer */}
      {workflowStatus === "evaluating" && (
        <div className="border-b border-accent-blue/20 bg-accent-blue/5 px-4 py-1.5 text-[11px] text-accent-blue">
          Evaluating workflow output...
        </div>
      )}
      {error && (
        <div className="border-b border-red-500/20 bg-red-500/5 px-4 py-2 text-xs text-red-400">
          {error}
        </div>
      )}

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* DAG — takes as much room as possible */}
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
            <div className="flex h-full items-center justify-center text-gray-600 text-sm">
              {workflowStatus === "connecting"
                ? "Connecting..."
                : "Waiting for DAG..."}
            </div>
          )}
        </div>

        {/* Sidebar — narrower, collapsible-ready */}
        <div className="w-[430px] flex flex-col overflow-hidden border-l border-white/5">
          {evaluation && (
            <div className="flex-shrink-0 p-3 border-b border-white/5">
              <EvaluationCard evaluation={evaluation} />
            </div>
          )}
          <div className="flex-1 overflow-y-auto p-3">
            <div className="mb-2 text-xs font-medium uppercase tracking-wide text-gray-500">
              Step details
            </div>
            <LiveStepDetails
              stepStates={stepStates}
              stepOrder={dag?.nodes.map((n) => n.id)}
              selectedStep={selectedStep}
              onSelectStep={setSelectedStep}
            />
          </div>
          <div className="flex-shrink-0 p-3 pt-0">
            <StepLogPanel events={events} />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Criterion row ── */
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
      <div className="flex items-center justify-between text-[11px]">
        <span className="truncate text-gray-300">{c.criterion}</span>
        <span className="ml-2 flex-shrink-0 tabular-nums text-gray-500">
          {c.score}/{c.max_score}
          {c.weight !== 1 && (
            <span className="ml-0.5 text-gray-600">&times;{c.weight}</span>
          )}
        </span>
      </div>
      <div className="mt-0.5 h-0.5 w-full rounded-full bg-white/5">
        <div className={`h-full rounded-full ${barColor} ${widthClass} transition-all duration-500`} />
      </div>
    </div>
  );
}

/* ── Evaluation card — compact ── */
function EvaluationCard({ evaluation }: Readonly<{ evaluation: EvaluationResult }>) {
  const [expanded, setExpanded] = useState(false);
  const hasCriteria = evaluation.criteria.length > 0;

  return (
    <div className="rounded-lg border border-white/5 bg-surface-1 p-2.5">
      <div className="flex items-center gap-1.5 text-[10px] uppercase tracking-wide text-gray-600 mb-1.5">
        <Trophy className="h-3 w-3 text-amber-400" />
        Evaluation
      </div>
      <div className="flex items-end justify-between">
        <div>
          <div className="text-xl font-semibold tabular-nums text-gray-100">
            {evaluation.weighted_score.toFixed(1)}
          </div>
          <div className="text-[10px] text-gray-600">/ 100</div>
        </div>
        <div className="text-right">
          <div className="text-xs font-medium text-gray-300">
            {evaluation.grade}
          </div>
          <div
            className={`text-[10px] ${evaluation.passed ? "text-green-400" : "text-red-400"}`}
          >
            {evaluation.passed ? "Passed" : "Needs work"}
          </div>
        </div>
      </div>

      {hasCriteria && (
        <>
          <button
            type="button"
            onClick={() => setExpanded((prev) => !prev)}
            className="mt-2 flex w-full items-center gap-1 text-[11px] text-gray-500 hover:text-gray-300 transition-colors"
          >
            {expanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
            {evaluation.criteria.length} criteria
          </button>

          {expanded && (
            <div className="mt-1.5 space-y-1.5">
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
