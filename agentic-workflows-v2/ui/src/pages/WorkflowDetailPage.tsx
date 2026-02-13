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

  // Run config form values (inputs + runtime + rubric + evaluation)
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
        return undefined;
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

      // Batch mode — fire all jobs sequentially and report progress
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
        // Single run — go to live view
        navigate(`/live/${data.run_id}`);
      } else {
        // Batch complete — stay on workflow page so run history refreshes
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
      {/* Header */}
      <div className="border-b border-white/5 px-6 py-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate("/workflows")}
            className="btn-ghost p-1"
            aria-label="Back to workflows"
          >
            <ArrowLeft className="h-4 w-4" />
          </button>
          <div className="flex-1">
            <h1 className="text-lg font-semibold">{name}</h1>
            {dag?.description && (
              <p className="text-sm text-gray-500">{dag.description}</p>
            )}
          </div>
          <button
            onClick={() => runMutation.mutate()}
            disabled={runMutation.isPending}
            className="btn-primary text-xs"
          >
            {runMutation.isPending
              ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
              : <Play className="h-3.5 w-3.5" />}
            {batchProgress
              ? `Running ${batchProgress.done}/${batchProgress.total}…`
              : runMutation.isPending
              ? "Starting…"
              : configRef.current.evaluation.enabled
              ? "Run + Evaluate"
              : "Run Workflow"}
          </button>
        </div>

        {/* Schema-driven run configuration form */}
        {hasInputs && (
          <div className="mt-4">
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
            <div className="flex h-full items-center justify-center text-gray-600">
              Loading DAG...
            </div>
          ) : dag ? (
            <WorkflowDAG dagNodes={dag.nodes} dagEdges={dag.edges} />
          ) : (
            <div className="flex h-full items-center justify-center text-gray-600">
              Failed to load DAG
            </div>
          )}
        </div>

        {/* Run history sidebar */}
        <div className="w-[400px] overflow-y-auto p-4">
          <h2 className="mb-3 text-sm font-medium text-gray-400">
            Run History
          </h2>
          <RunList runs={runs} isLoading={runsLoading} />
        </div>
      </div>

      {/* Error */}
      {runMutation.isError && (
        <div className="border-t border-red-500/20 bg-red-500/10 px-6 py-3 text-sm text-red-400">
          Failed to start workflow: {(runMutation.error as Error).message}
        </div>
      )}
    </div>
  );
}
