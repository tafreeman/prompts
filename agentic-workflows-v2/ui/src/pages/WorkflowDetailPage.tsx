import { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Play, ArrowLeft } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { useEvaluationDatasets, useWorkflowDAG } from "../hooks/useWorkflows";
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
  const { data: evaluationDatasets } = useEvaluationDatasets();
  const { data: runs, isLoading: runsLoading } = useRuns(name);

  // Run config form values (inputs + runtime + rubric)
  const configRef = useRef<RunConfigValues>({
    inputValues: {},
    executionProfile: { runtime: "subprocess" },
    rubricId: "",
  });

  const [evaluationEnabled, setEvaluationEnabled] = useState(false);
  const [datasetSource, setDatasetSource] = useState<"none" | "repository" | "local">(
    "repository"
  );
  const [datasetId, setDatasetId] = useState("");
  const [sampleIndex, setSampleIndex] = useState("0");

  const repositoryDatasets = evaluationDatasets?.repository ?? [];
  const localDatasets = evaluationDatasets?.local ?? [];
  const activeDatasets =
    datasetSource === "local" ? localDatasets : repositoryDatasets;

  useEffect(() => {
    if (!evaluationEnabled || datasetSource === "none") return;
    if (activeDatasets.length === 0) {
      setDatasetId("");
      return;
    }
    const firstDataset = activeDatasets[0];
    if (!activeDatasets.some((dataset) => dataset.id === datasetId)) {
      setDatasetId(firstDataset?.id ?? "");
    }
  }, [activeDatasets, datasetId, datasetSource, evaluationEnabled]);

  useEffect(() => {
    if (!evaluationEnabled) return;
    if (datasetSource === "repository" && repositoryDatasets.length === 0) {
      if (localDatasets.length > 0) {
        setDatasetSource("local");
      } else {
        setDatasetSource("none");
      }
    }
  }, [datasetSource, evaluationEnabled, localDatasets.length, repositoryDatasets.length]);

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

  const runMutation = useMutation({
    mutationFn: () => {
      const { executionProfile, rubricId } = configRef.current;
      const evalRequest = evaluationEnabled
        ? {
            enabled: true as const,
            dataset_source: datasetSource,
            dataset_id: datasetSource === "none" ? undefined : datasetId || undefined,
            sample_index: Number.parseInt(sampleIndex, 10) || 0,
            rubric_id: rubricId || undefined,
          }
        : undefined;

      return runWorkflow({
        workflow: name!,
        input_data: buildInputData(),
        evaluation: evalRequest,
        execution_profile: executionProfile,
      });
    },
    onSuccess: (data) => {
      navigate(`/live/${data.run_id}`);
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
            <Play className="h-3.5 w-3.5" />
            {runMutation.isPending
              ? "Starting..."
              : evaluationEnabled
              ? "Run + Evaluate"
              : "Run Workflow"}
          </button>
        </div>

        {/* Schema-driven run configuration form */}
        {hasInputs && (
          <div className="mt-4">
            <RunConfigForm
              inputs={dag.inputs!}
              onChange={(values) => {
                configRef.current = values;
              }}
            />
          </div>
        )}

        {/* Evaluation controls */}
        <div className="mt-4 rounded-lg border border-white/10 bg-surface-1/60 p-3">
          <div className="flex flex-wrap items-center gap-4">
            <label className="flex items-center gap-2 text-xs font-medium text-gray-300">
              <input
                type="checkbox"
                checked={evaluationEnabled}
                onChange={(e) => setEvaluationEnabled(e.target.checked)}
                className="h-3.5 w-3.5 rounded border-white/20 bg-surface-2 text-accent-blue focus:ring-accent-blue/50"
              />
              Enable evaluation scoring
            </label>

            {evaluationEnabled && (
              <>
                <label className="text-xs text-gray-400">
                  Dataset source
                  <select
                    value={datasetSource}
                    onChange={(e) =>
                      setDatasetSource(
                        e.target.value as "none" | "repository" | "local"
                      )
                    }
                    className="ml-2 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                  >
                    <option value="repository">Repository set</option>
                    <option value="local">Local JSON</option>
                    <option value="none">No dataset</option>
                  </select>
                </label>

                {datasetSource !== "none" && (
                  <label className="text-xs text-gray-400">
                    Dataset
                    <select
                      value={datasetId}
                      onChange={(e) => setDatasetId(e.target.value)}
                      className="ml-2 max-w-[280px] rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                    >
                      {activeDatasets.length === 0 ? (
                        <option value="">
                          No datasets available
                        </option>
                      ) : (
                        activeDatasets.map((dataset) => (
                          <option key={dataset.id} value={dataset.id}>
                            {dataset.name}
                            {dataset.sample_count != null
                              ? ` (${dataset.sample_count})`
                              : ""}
                          </option>
                        ))
                      )}
                    </select>
                  </label>
                )}

                <label className="text-xs text-gray-400">
                  Sample #
                  <input
                    type="number"
                    min={0}
                    value={sampleIndex}
                    onChange={(e) => setSampleIndex(e.target.value)}
                    className="ml-2 w-16 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                  />
                </label>
              </>
            )}
          </div>
          {evaluationEnabled && datasetSource !== "none" && (
            <p className="mt-2 text-xs text-gray-600">
              Run progress streams live as usual; evaluation score is computed after workflow completion and shown in the live panel.
            </p>
          )}
        </div>
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
