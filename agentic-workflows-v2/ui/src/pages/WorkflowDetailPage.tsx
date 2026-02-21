import { useRef, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Play, ArrowLeft, Loader2 } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import { useRuns } from "../hooks/useRuns";
import { runWorkflow } from "../api/client";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import RunList from "../components/runs/RunList";
import RunConfigForm, {
  type RunConfigValues,
} from "../components/runs/RunConfigForm";

export default function WorkflowDetailPage() {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const { data: dag, isLoading: dagLoading } = useWorkflowDAG(name);
  const { data: runs, isLoading: runsLoading } = useRuns(name);

  const configRef = useRef<RunConfigValues>({
    inputValues: {},
    executionProfile: { runtime: "subprocess" },
    rubricId: "",
    evaluation: {
      enabled: false,
      datasetSource: "none",
      datasetId: "",
      evalSetId: "",
      selectedSamples: [0],
      runsPerRecord: 1,
    },
  });

  const buildInputData = (): Record<string, unknown> => {
    const data: Record<string, unknown> = {};
    if (!dag?.inputs) return data;
    const vals = configRef.current.inputValues;
    for (const inp of dag.inputs) {
      const val = vals[inp.name] ?? "";
      if (!val && !inp.required) continue;
      if (inp.type === "object" || inp.type === "array") {
        try {
          data[inp.name] = JSON.parse(val);
        } catch {
          data[inp.name] = val;
        }
      } else {
        data[inp.name] = val;
      }
    }
    return data;
  };

  const [batchProgress, setBatchProgress] = useState<{ done: number; total: number } | null>(null);

  const runMutation = useMutation({
    mutationFn: async () => {
      const { executionProfile, rubricId, evaluation } = configRef.current;

      const buildEvalRequest = (sampleIndex: number) => {
        if (!evaluation.enabled) return undefined;
        if (evaluation.datasetSource === "eval_set" && evaluation.evalSetId) {
          return {
            enabled: true as const,
            dataset_source: "repository" as const,
            dataset_id: evaluation.evalSetId,
            sample_index: sampleIndex,
            rubric_id: rubricId || undefined,
          };
        }
        if (evaluation.datasetSource !== "none" && evaluation.datasetId) {
          return {
            enabled: true as const,
            dataset_source: evaluation.datasetSource as "repository" | "local",
            dataset_id: evaluation.datasetId,
            sample_index: sampleIndex,
            rubric_id: rubricId || undefined,
          };
        }
        return {
          enabled: true as const,
          dataset_source: "none" as const,
          sample_index: sampleIndex,
          rubric_id: rubricId || undefined,
        };
      };

      const samples = evaluation.enabled && evaluation.selectedSamples.length > 0
        ? evaluation.selectedSamples
        : [0];
      const runsPerRecord = evaluation.enabled ? (evaluation.runsPerRecord ?? 1) : 1;
      const isBatch = samples.length > 1 || runsPerRecord > 1;

      const jobs: Array<{ sampleIndex: number }> = [];
      for (const s of samples) {
        for (let r = 0; r < runsPerRecord; r++) {
          jobs.push({ sampleIndex: s });
        }
      }

      if (!isBatch) {
        return runWorkflow({
          workflow: name!,
          input_data: buildInputData(),
          evaluation: buildEvalRequest(jobs[0] ? jobs[0].sampleIndex : 0),
          execution_profile: executionProfile,
        });
      }

      setBatchProgress({ done: 0, total: jobs.length });
      for (let i = 0; i < jobs.length; i++) {
        await runWorkflow({
          workflow: name!,
          input_data: buildInputData(),
          evaluation: buildEvalRequest(jobs[i]?.sampleIndex ?? 0),
          execution_profile: executionProfile,
        });
        setBatchProgress({ done: i + 1, total: jobs.length });
      }
      return null;
    },
    onSuccess: (data) => {
      setBatchProgress(null);
      if (data) {
        navigate(`/live/${data.run_id}`);
      } else {
        navigate(`/workflows/${encodeURIComponent(name!)}`);
      }
    },
    onError: () => {
      setBatchProgress(null);
    },
  });

  const hasInputs = dag?.inputs && dag.inputs.length > 0;

  return (
    <div className="flex h-full flex-col">
      {/* Header — compact with inline run button */}
      <div className="border-b border-white/5 px-4 py-2.5">
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => navigate("/workflows")}
            className="btn-ghost p-1"
            aria-label="Back to workflows"
          >
            <ArrowLeft className="h-4 w-4" />
          </button>
          <div className="min-w-0 flex-1">
            <h1 className="truncate text-sm font-semibold">{name}</h1>
            {dag?.description && (
              <p className="truncate text-xs text-gray-600">{dag.description}</p>
            )}
          </div>
          <button
            type="button"
            onClick={() => runMutation.mutate()}
            disabled={runMutation.isPending}
            className="btn-primary text-xs py-1.5 px-3"
          >
            {runMutation.isPending
              ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
              : <Play className="h-3.5 w-3.5" />}
            {batchProgress
              ? `${batchProgress.done}/${batchProgress.total}`
              : runMutation.isPending
              ? "Starting..."
              : configRef.current.evaluation.enabled
              ? "Run + Eval"
              : "Run"}
          </button>
        </div>

        {/* Config form — directly under header, compact */}
        {hasInputs && (
          <div className="mt-2">
            <RunConfigForm
              inputs={dag.inputs!}
              workflowName={name!}
              onChange={(values) => {
                configRef.current = values;
              }}
            />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* DAG Preview */}
        <div className="flex-1 border-r border-white/5">
          {dagLoading ? (
            <div className="flex h-full items-center justify-center text-gray-600 text-sm">
              Loading DAG...
            </div>
          ) : dag ? (
            <WorkflowDAG dagNodes={dag.nodes} dagEdges={dag.edges} />
          ) : (
            <div className="flex h-full items-center justify-center text-gray-600 text-sm">
              Failed to load DAG
            </div>
          )}
        </div>

        {/* Run history sidebar — narrower */}
        <div className="w-[320px] overflow-y-auto p-3">
          <h2 className="mb-2 text-xs font-medium text-gray-500 uppercase tracking-wide">
            History
          </h2>
          <RunList runs={runs} isLoading={runsLoading} />
        </div>
      </div>

      {/* Error banner */}
      {runMutation.isError && (
        <div className="border-t border-red-500/20 bg-red-500/5 px-4 py-2 text-xs text-red-400">
          Failed: {(runMutation.error as Error).message}
        </div>
      )}
    </div>
  );
}
