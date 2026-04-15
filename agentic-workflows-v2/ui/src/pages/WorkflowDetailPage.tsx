import { useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Play, ArrowLeft, Loader2, Sparkles, AlertCircle } from "lucide-react";
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

  const [config, setConfig] = useState<RunConfigValues>({
    inputValues: {},
    executionProfile: { runtime: "subprocess" },
    rubricId: "",
    evaluationReadiness: {
      status: "idle",
      message: "Turn on evaluation to score the run after it completes.",
    },
    evaluation: {
      enabled: false,
      datasetSource: "none",
      datasetId: "",
      selectedSamples: [0],
      runsPerRecord: 1,
    },
  });

  const buildInputData = (): Record<string, unknown> => {
    const data: Record<string, unknown> = {};
    if (!dag?.inputs) return data;
    const vals = config.inputValues;
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

  const requiredInputNames = useMemo(
    () => dag?.inputs?.filter((input) => input.required).map((input) => input.name) ?? [],
    [dag?.inputs]
  );

  const validationMessage = useMemo(() => {
    if (!config.evaluation.enabled) {
      return null;
    }
    if (
      config.evaluation.datasetSource !== "none" &&
      !config.evaluation.datasetId
    ) {
      return "Choose a dataset before starting a scored evaluation.";
    }

    if (config.evaluation.datasetSource !== "none") {
      if (config.evaluationReadiness.status === "loading") {
        return "Wait for dataset preview to finish before starting the run.";
      }
      if (config.evaluationReadiness.status === "error") {
        return config.evaluationReadiness.message;
      }
    }

    const missingRequiredInputs = requiredInputNames.filter((name) => {
      const value = config.inputValues[name];
      if (typeof value === "string") {
        return value.trim() === "";
      }
      return value == null;
    });

    if (config.evaluation.datasetSource === "none" && missingRequiredInputs.length > 0) {
      return "Provide the required workflow inputs or choose a dataset that can prefill them.";
    }

    return null;
  }, [config, requiredInputNames]);

  const runMutation = useMutation({
    mutationFn: async () => {
      const { executionProfile, rubricId, evaluation } = config;

      if (validationMessage) {
        throw new Error(validationMessage);
      }

      const buildEvalRequest = (sampleIndex: number) => {
        if (!evaluation.enabled) return undefined;
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

  let runButtonLabel = "Run";
  if (batchProgress) {
    runButtonLabel = `${batchProgress.done}/${batchProgress.total}`;
  } else if (runMutation.isPending) {
    runButtonLabel = "Starting...";
  } else if (config.evaluation.enabled) {
    runButtonLabel = "Run + Eval";
  }

  let evalSummary = "Manual run";
  if (config.evaluation.enabled) {
    if (config.evaluation.datasetSource === "none") {
      evalSummary = "Evaluation enabled — using manual inputs only.";
    } else if (config.evaluation.datasetId) {
      evalSummary = `Evaluation ready · ${config.evaluation.datasetSource} dataset selected`;
    } else {
      evalSummary = "Evaluation enabled — choose a dataset to continue.";
    }
  }

  let dagContent = (
    <div className="flex h-full items-center justify-center text-gray-600 text-sm">
      Failed to load DAG
    </div>
  );

  if (dagLoading) {
    dagContent = (
      <div className="flex h-full items-center justify-center text-gray-600 text-sm">
        Loading DAG...
      </div>
    );
  } else if (dag) {
    dagContent = <WorkflowDAG dagNodes={dag.nodes} dagEdges={dag.edges} />;
  }

  const errorMessage = runMutation.error?.message ?? null;
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
            <div className="mt-1 flex items-center gap-1.5 text-[11px] text-gray-500">
              <Sparkles className="h-3 w-3 text-accent-blue" />
              <span>{evalSummary}</span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => runMutation.mutate()}
            disabled={runMutation.isPending || Boolean(validationMessage)}
            className="btn-primary text-xs py-1.5 px-3"
          >
            {runMutation.isPending
              ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
              : <Play className="h-3.5 w-3.5" />}
            {runButtonLabel}
          </button>
        </div>

        {validationMessage && (
          <div className="mt-2 inline-flex items-start gap-2 rounded-lg border border-amber-500/20 bg-amber-500/5 px-3 py-2 text-[11px] text-amber-100">
            <AlertCircle className="mt-0.5 h-3.5 w-3.5 shrink-0" />
            <span>{validationMessage}</span>
          </div>
        )}

        {/* Config form — directly under header, compact */}
        {hasInputs && (
          <div className="mt-2">
            <RunConfigForm
              inputs={dag.inputs!}
              workflowName={name!}
              onChange={setConfig}
            />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* DAG Preview */}
        <div className="flex-1 border-r border-white/5">
          {dagContent}
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
      {runMutation.isError && errorMessage && (
        <div className="border-t border-red-500/20 bg-red-500/5 px-4 py-2 text-xs text-red-400">
          Failed: {errorMessage}
        </div>
      )}
    </div>
  );
}
