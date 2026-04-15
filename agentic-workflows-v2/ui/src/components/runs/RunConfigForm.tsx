import { useState, useEffect, useCallback } from "react";
import {
  Settings2,
  Cpu,
  FlaskConical,
  Database,
  ChevronDown,
  ChevronRight,
  Sparkles,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";
import type {
  WorkflowInputSchema,
  ExecutionProfileRequest,
  EvaluationDatasetsResponse,
} from "../../api/types";
import { listEvaluationDatasets, previewDatasetInputs } from "../../api/client";

// ---------------------------------------------------------------------------
// Public types
// ---------------------------------------------------------------------------

export interface RunConfigValues {
  inputValues: Record<string, string>;
  executionProfile: ExecutionProfileRequest;
  rubricId: string;
  evaluationReadiness: {
    status: DatasetPreviewState["status"];
    message: string;
  };
  evaluation: {
    enabled: boolean;
    datasetSource: "none" | "repository" | "local";
    datasetId: string;
    selectedSamples: number[];
    runsPerRecord: number;
  };
}

interface DatasetPreviewState {
  status: "idle" | "loading" | "ready" | "error";
  message: string;
  reasons: string[];
}

export interface RunConfigFormProps {
  inputs: WorkflowInputSchema[];
  workflowName: string;
  onChange: (values: RunConfigValues) => void;
}

// ---------------------------------------------------------------------------
// RunConfigForm — compact layout
// ---------------------------------------------------------------------------

export default function RunConfigForm({ inputs, workflowName, onChange }: RunConfigFormProps) {
  const [inputValues, setInputValues] = useState<Record<string, string>>({});
  const [showInputs, setShowInputs] = useState(true);

  useEffect(() => {
    const defaults: Record<string, string> = {};
    for (const inp of inputs) {
      if (inp.default != null) {
        defaults[inp.name] =
          typeof inp.default === "string"
            ? inp.default
            : JSON.stringify(inp.default);
      } else {
        defaults[inp.name] = "";
      }
    }
    setInputValues(defaults);
  }, [inputs]);

  // -- Runtime config --------------------------------------------------------
  const [runtime, setRuntime] = useState<"subprocess" | "docker">("subprocess");
  const [maxAttempts, setMaxAttempts] = useState<string>("");
  const [maxDuration, setMaxDuration] = useState<string>("");
  const [containerImage, setContainerImage] = useState<string>("");

  // -- Rubric override -------------------------------------------------------
  const [rubricId, setRubricId] = useState<string>("");

  // -- Evaluation config -----------------------------------------------------
  const [evalEnabled, setEvalEnabled] = useState<boolean>(false);
  const [evalDatasetSource, setEvalDatasetSource] = useState<"none" | "repository" | "local">("none");
  const [evalDatasetId, setEvalDatasetId] = useState<string>("");
  const [evalSelectedSamples, setEvalSelectedSamples] = useState<number[]>([0]);
  const [evalRunsPerRecord, setEvalRunsPerRecord] = useState<number>(1);
  const [datasets, setDatasets] = useState<EvaluationDatasetsResponse | null>(null);
  const [datasetsError, setDatasetsError] = useState<string | null>(null);
  const [isDatasetsLoading, setIsDatasetsLoading] = useState(false);
  const [previewState, setPreviewState] = useState<DatasetPreviewState>({
    status: "idle",
    message: "Choose a workflow-compatible dataset to auto-fill inputs.",
    reasons: [],
  });

  useEffect(() => {
    let isActive = true;
    setIsDatasetsLoading(true);
    setDatasetsError(null);

    listEvaluationDatasets(workflowName)
      .then((response) => {
        if (!isActive) return;
        setDatasets(response);
      })
      .catch((err) => {
        if (!isActive) return;
        setDatasetsError(
          err instanceof Error ? err.message : "Failed to load evaluation datasets."
        );
      })
      .finally(() => {
        if (!isActive) return;
        setIsDatasetsLoading(false);
      });

    return () => {
      isActive = false;
    };
  }, [workflowName]);

  useEffect(() => {
    if (!evalEnabled) {
      setPreviewState({
        status: "idle",
        message: "Turn on evaluation to score the run after it completes.",
        reasons: [],
      });
      return;
    }

    if (datasetsError) {
      setPreviewState({
        status: "error",
        message: "Evaluation datasets could not be loaded for this workflow.",
        reasons: [datasetsError],
      });
      return;
    }

    if (evalDatasetSource === "none") {
      setPreviewState({
        status: "idle",
        message: "Select a repository or local dataset to run a scored evaluation.",
        reasons: [],
      });
      return;
    }

    if (!evalDatasetId) {
      setPreviewState({
        status: "idle",
        message: "Select a dataset to preview how it maps onto this workflow's inputs.",
        reasons: [],
      });
      return;
    }

    setPreviewState({
      status: "loading",
      message: "Checking dataset compatibility and preparing sample inputs…",
      reasons: [],
    });
  }, [evalEnabled, evalDatasetSource, evalDatasetId, datasetsError]);

  useEffect(() => {
    if (
      !evalEnabled ||
      evalDatasetSource === "none" ||
      !evalDatasetId
    ) {
      return;
    }

    let isCurrent = true;
    const previewIndex = evalSelectedSamples[0] ?? 0;
    previewDatasetInputs(workflowName, evalDatasetSource, evalDatasetId, previewIndex)
      .then((preview) => {
        if (!isCurrent) {
          return;
        }
        if (preview.compatible && preview.adapted_inputs) {
          setInputValues((prev) => {
            const updated = { ...prev };
            for (const [key, value] of Object.entries(preview.adapted_inputs)) {
              if (value !== null && value !== undefined) {
                updated[key] =
                  typeof value === "string" ? value : JSON.stringify(value);
              }
            }
            return updated;
          });
        }

        setPreviewState(
          preview.compatible
            ? {
                status: "ready",
                message: "Dataset is compatible. Sample inputs were prefilled for you.",
                reasons: [],
              }
            : {
                status: "error",
                message: "Dataset does not match this workflow's required inputs.",
                reasons: preview.reasons,
              }
        );
      })
      .catch((err) => {
        if (!isCurrent) {
          return;
        }
        const reason = err instanceof Error ? err.message : "Failed to preview dataset inputs.";
        setPreviewState({
          status: "error",
          message: "Dataset preview failed.",
          reasons: [reason],
        });
      });

    return () => {
      isCurrent = false;
    };
  }, [workflowName, evalEnabled, evalDatasetSource, evalDatasetId, evalSelectedSamples]);

  const [showAdvanced, setShowAdvanced] = useState(false);

  const emitChange = useCallback(() => {
    const profile: ExecutionProfileRequest = { runtime };
    if (maxAttempts) profile.max_attempts = Number(maxAttempts);
    if (maxDuration) profile.max_duration_minutes = Number(maxDuration);
    if (runtime === "docker" && containerImage)
      profile.container_image = containerImage;

    onChange({
      inputValues,
      executionProfile: profile,
      rubricId,
      evaluationReadiness: {
        status: previewState.status,
        message: previewState.message,
      },
      evaluation: {
        enabled: evalEnabled,
        datasetSource: evalDatasetSource,
        datasetId: evalDatasetId,
        selectedSamples: evalSelectedSamples,
        runsPerRecord: evalRunsPerRecord,
      }
    });
  }, [inputValues, runtime, maxAttempts, maxDuration, containerImage, rubricId,
      previewState.status, previewState.message, evalEnabled, evalDatasetSource, evalDatasetId,
      evalSelectedSamples, evalRunsPerRecord, onChange]);

  useEffect(() => {
    emitChange();
  }, [emitChange]);

  const handleInputChange = (name: string, value: string) => {
    setInputValues((prev) => ({ ...prev, [name]: value }));
  };

  // Separate large inputs (object/array) from compact ones
  const compactInputs = inputs.filter(
    (inp) => inp.type !== "object" && inp.type !== "array" && !(inp.name === "tech_stack" && inp.type === "object")
  );
  const largeInputs = inputs.filter(
    (inp) => inp.type === "object" || inp.type === "array"
  );

  const selectedDataset =
    evalDatasetSource === "repository"
      ? datasets?.repository.find((dataset) => dataset.id === evalDatasetId)
      : datasets?.local.find((dataset) => dataset.id === evalDatasetId);

  const previewTone =
    previewState.status === "error"
      ? "border-red-500/20 bg-red-500/5 text-red-200"
      : previewState.status === "ready"
      ? "border-emerald-500/20 bg-emerald-500/5 text-emerald-100"
      : "border-white/10 bg-surface-1/70 text-gray-300";

  const previewIcon =
    previewState.status === "error" ? (
      <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-300" />
    ) : previewState.status === "ready" ? (
      <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-300" />
    ) : (
      <Sparkles className="mt-0.5 h-4 w-4 shrink-0 text-accent-blue" />
    );

  return (
    <div data-testid="run-config-form" className="space-y-2">
      {/* ---- Collapsible inputs header ---- */}
      {inputs.length > 0 && (
        <button
          type="button"
          onClick={() => setShowInputs((v) => !v)}
          className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-200 transition-colors"
        >
          {showInputs ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
          Inputs ({inputs.length})
        </button>
      )}

      {inputs.length > 0 && showInputs && (
        <div className="space-y-2" data-testid="workflow-inputs">
          {/* Compact inputs — inline row */}
          {compactInputs.length > 0 && (
            <div className="flex flex-wrap items-end gap-2">
              {compactInputs.map((inp) => (
                <CompactInputField
                  key={inp.name}
                  schema={inp}
                  value={inputValues[inp.name] ?? ""}
                  onChange={(val) => handleInputChange(inp.name, val)}
                />
              ))}
            </div>
          )}

          {/* Large inputs — each on own row but shorter */}
          {largeInputs.map((inp) =>
            inp.name === "tech_stack" && inp.type === "object" ? (
              <TechStackField
                key={inp.name}
                value={inputValues[inp.name] ?? ""}
                onChange={(val) => handleInputChange(inp.name, val)}
                required={inp.required}
              />
            ) : (
              <div key={inp.name}>
                <label className="mb-0.5 block text-[11px] font-medium text-gray-500">
                  {inp.name.replace(/_/g, " ")}
                  {inp.required && <span className="ml-0.5 text-red-400">*</span>}
                </label>
                <textarea
                  value={inputValues[inp.name] ?? ""}
                  onChange={(e) => handleInputChange(inp.name, e.target.value)}
                  rows={2}
                  placeholder={inp.description || "JSON value"}
                  required={inp.required}
                  data-testid={`input-${inp.name}`}
                  className="w-full rounded border border-white/10 bg-surface-2 px-2 py-1 font-mono text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none resize-y"
                />
              </div>
            )
          )}
        </div>
      )}

      <div
        data-testid="evaluation-config"
        className="space-y-3 rounded-xl border border-white/10 bg-surface-1/60 p-3 text-xs"
      >
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="space-y-1">
            <div className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-[0.18em] text-gray-400">
              <Database className="h-3.5 w-3.5" />
              Evaluation
            </div>
            <p className="max-w-xl text-xs text-gray-500">
              Score this run against a workflow-compatible dataset. Evaluation sets remain visible on the
              datasets page, but this runner executes one concrete dataset at a time for predictable results.
            </p>
          </div>
          <label className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-surface-2 px-3 py-1.5 text-gray-200">
            <input
              type="checkbox"
              checked={evalEnabled}
              onChange={(e) => setEvalEnabled(e.target.checked)}
              className="rounded border-white/10 bg-surface-2 text-accent-blue focus:ring-accent-blue/50"
            />
            Enable evaluation
          </label>
        </div>

        {evalEnabled && (
          <>
            <div className="flex flex-wrap items-end gap-2">
              <label className="text-gray-400">
                Source
                <select
                  value={evalDatasetSource}
                  onChange={(e) => {
                    setEvalDatasetSource(e.target.value as typeof evalDatasetSource);
                    setEvalDatasetId("");
                    setEvalSelectedSamples([0]);
                  }}
                  className="ml-1 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                >
                  <option value="none">None</option>
                  <option value="repository">Repository</option>
                  <option value="local">Local</option>
                </select>
              </label>

              {evalDatasetSource === "repository" && datasets?.repository && (
                <label className="text-gray-400">
                  Dataset
                  <select
                    value={evalDatasetId}
                    onChange={(e) => setEvalDatasetId(e.target.value)}
                    className="ml-1 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                  >
                    <option value="">Select...</option>
                    {datasets.repository.map((ds) => (
                      <option key={ds.id} value={ds.id}>
                        {ds.name} {ds.sample_count ? `(${ds.sample_count})` : ""}
                      </option>
                    ))}
                  </select>
                </label>
              )}

              {evalDatasetSource === "local" && datasets?.local && (
                <label className="text-gray-400">
                  Dataset
                  <select
                    value={evalDatasetId}
                    onChange={(e) => setEvalDatasetId(e.target.value)}
                    className="ml-1 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                  >
                    <option value="">Select...</option>
                    {datasets.local.map((ds) => (
                      <option key={ds.id} value={ds.id}>
                        {ds.name} {ds.sample_count ? `(${ds.sample_count})` : ""}
                      </option>
                    ))}
                  </select>
                </label>
              )}
            </div>

            {(evalDatasetSource === "repository" || evalDatasetSource === "local") && evalDatasetId && (
              <SampleSelector
                datasetSource={evalDatasetSource}
                datasetId={evalDatasetId}
                datasets={datasets}
                selectedSamples={evalSelectedSamples}
                runsPerRecord={evalRunsPerRecord}
                onSelectedSamplesChange={setEvalSelectedSamples}
                onRunsPerRecordChange={setEvalRunsPerRecord}
              />
            )}

            <div className={`rounded-lg border px-3 py-2 ${previewTone}`}>
              <div className="flex items-start gap-2">
                {previewIcon}
                <div className="min-w-0 space-y-1">
                  <p className="font-medium">{previewState.message}</p>
                  {selectedDataset && (
                    <p className="text-[11px] text-inherit/80">
                      {selectedDataset.name}
                      {selectedDataset.sample_count != null ? ` · ${selectedDataset.sample_count} samples` : ""}
                    </p>
                  )}
                  {previewState.reasons.length > 0 && (
                    <ul className="list-disc space-y-0.5 pl-4 text-[11px] text-inherit/80">
                      {previewState.reasons.map((reason) => (
                        <li key={reason}>{reason}</li>
                      ))}
                    </ul>
                  )}
                  {isDatasetsLoading && (
                    <p className="text-[11px] text-inherit/80">Loading workflow-compatible datasets…</p>
                  )}
                  {datasetsError && !isDatasetsLoading && (
                    <p className="text-[11px] text-inherit/80">{datasetsError}</p>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* ---- Advanced toggle ---- */}
      <button
        type="button"
        onClick={() => setShowAdvanced((v) => !v)}
        className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-200 transition-colors"
        data-testid="advanced-toggle"
      >
        <Settings2 className="h-3 w-3" />
        {showAdvanced ? "Hide advanced" : "Advanced runtime"}
      </button>

      {showAdvanced && (
        <div className="space-y-2 rounded border border-white/10 bg-surface-1/60 p-2 text-xs">
          {/* ---- Rubric + Runtime in a single row ---- */}
          <div className="flex flex-wrap items-end gap-3 pt-1 border-t border-white/5">
            <fieldset data-testid="rubric-config" className="flex items-end gap-1">
              <label className="text-[11px] text-gray-400 flex items-center gap-1">
                <FlaskConical className="h-3 w-3" />
                Rubric
              </label>
              <input
                type="text"
                value={rubricId}
                onChange={(e) => setRubricId(e.target.value)}
                placeholder="default"
                aria-label="Rubric ID"
                className="w-28 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
              />
            </fieldset>

            <fieldset data-testid="runtime-config" className="flex items-end gap-2">
              <label className="text-[11px] text-gray-400 flex items-center gap-1">
                <Cpu className="h-3 w-3" />
                Engine
              </label>
              <select
                value={runtime}
                onChange={(e) =>
                  setRuntime(e.target.value as "subprocess" | "docker")
                }
                aria-label="Runtime engine"
                className="rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
              >
                <option value="subprocess">Subprocess</option>
                <option value="docker">Docker</option>
              </select>

              <label className="text-[11px] text-gray-400">
                Retries
                <input
                  type="number"
                  min={1}
                  value={maxAttempts}
                  onChange={(e) => setMaxAttempts(e.target.value)}
                  placeholder="–"
                  aria-label="Max attempts"
                  className="ml-1 w-12 rounded border border-white/10 bg-surface-2 px-1.5 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                />
              </label>

              <label className="text-[11px] text-gray-400">
                Timeout
                <input
                  type="number"
                  min={1}
                  value={maxDuration}
                  onChange={(e) => setMaxDuration(e.target.value)}
                  placeholder="–"
                  aria-label="Max duration minutes"
                  className="ml-1 w-12 rounded border border-white/10 bg-surface-2 px-1.5 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                />
                <span className="ml-0.5 text-gray-600">min</span>
              </label>

              {runtime === "docker" && (
                <label className="text-[11px] text-gray-400">
                  Image
                  <input
                    type="text"
                    value={containerImage}
                    onChange={(e) => setContainerImage(e.target.value)}
                    placeholder="python:3.12-slim"
                    aria-label="Container image"
                    className="ml-1 w-36 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
                  />
                </label>
              )}
            </fieldset>
          </div>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// CompactInputField — inline input for simple types (string, enum)
// ---------------------------------------------------------------------------

function CompactInputField({
  schema,
  value,
  onChange,
}: {
  schema: WorkflowInputSchema;
  value: string;
  onChange: (val: string) => void;
}) {
  const label = schema.name.replace(/_/g, " ");

  if (schema.enum) {
    return (
      <label className="text-[11px] text-gray-500">
        {label}
        {schema.required && <span className="ml-0.5 text-red-400">*</span>}
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          aria-label={label}
          required={schema.required}
          data-testid={`input-${schema.name}`}
          className="ml-1 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
        >
          {!value && <option value="">Select...</option>}
          {schema.enum.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </label>
    );
  }

  return (
    <label className="text-[11px] text-gray-500">
      {label}
      {schema.required && <span className="ml-0.5 text-red-400">*</span>}
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={schema.description || schema.name}
        required={schema.required}
        data-testid={`input-${schema.name}`}
        className="ml-1 w-40 rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
      />
    </label>
  );
}

// ---------------------------------------------------------------------------
// SampleSelector — compact multi-select for dataset samples
// ---------------------------------------------------------------------------

function SampleSelector({
  datasetSource,
  datasetId,
  datasets,
  selectedSamples,
  runsPerRecord,
  onSelectedSamplesChange,
  onRunsPerRecordChange,
}: Readonly<{
  datasetSource: "repository" | "local";
  datasetId: string;
  datasets: EvaluationDatasetsResponse | null;
  selectedSamples: number[];
  runsPerRecord: number;
  onSelectedSamplesChange: (samples: number[]) => void;
  onRunsPerRecordChange: (count: number) => void;
}>) {
  const list = datasetSource === "repository" ? datasets?.repository : datasets?.local;
  const dataset = list?.find((d) => d.id === datasetId);
  const sampleCount = dataset?.sample_count ?? null;

  const toggleSample = (index: number) => {
    if (selectedSamples.includes(index)) {
      onSelectedSamplesChange(selectedSamples.filter((i) => i !== index));
    } else {
      onSelectedSamplesChange([...selectedSamples, index].sort((a, b) => a - b));
    }
  };

  const selectAll = () => {
    if (sampleCount !== null) {
      onSelectedSamplesChange(Array.from({ length: sampleCount }, (_, i) => i));
    }
  };

  const totalRuns = selectedSamples.length * runsPerRecord;

  return (
    <div className="w-full space-y-1 pt-1 border-t border-white/5">
      <div className="flex items-center justify-between">
        <span className="text-gray-400">
          Records{sampleCount !== null && ` (${sampleCount})`}
        </span>
        <div className="flex items-center gap-2">
          {sampleCount !== null && sampleCount <= 50 && (
            <button type="button" onClick={selectAll} className="text-accent-blue hover:underline">
              All
            </button>
          )}
          {selectedSamples.length > 0 && (
            <button
              type="button"
              onClick={() => onSelectedSamplesChange([])}
              className="text-gray-500 hover:text-gray-300"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {sampleCount === null ? (
        <div className="flex items-center gap-2">
          <input
            type="number"
            min={0}
            placeholder="Index"
            className="w-16 rounded border border-white/10 bg-surface-2 px-1.5 py-0.5 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                const val = Number((e.target as HTMLInputElement).value);
                if (selectedSamples.includes(val)) return;
                onSelectedSamplesChange([...selectedSamples, val].sort((a, b) => a - b));
                (e.target as HTMLInputElement).value = "";
              }
            }}
          />
          <span className="text-gray-600">Enter to add</span>
          {selectedSamples.length > 0 && (
            <span className="text-gray-400">
              [{selectedSamples.join(", ")}]
            </span>
          )}
        </div>
      ) : (
        <div className="max-h-20 overflow-y-auto rounded border border-white/10 bg-surface-2 p-1">
          <div className="flex flex-wrap gap-0.5">
            {Array.from({ length: Math.min(sampleCount, 50) }, (_, i) => (
              <button
                key={i}
                type="button"
                onClick={() => toggleSample(i)}
                className={`rounded px-1.5 py-0.5 text-[10px] transition-colors ${
                  selectedSamples.includes(i)
                    ? "bg-accent-blue/20 text-accent-blue"
                    : "text-gray-500 hover:bg-white/5 hover:text-gray-300"
                }`}
              >
                {i}
              </button>
            ))}
            {sampleCount > 50 && (
              <span className="px-1 text-[10px] text-gray-600">+{sampleCount - 50} more</span>
            )}
          </div>
        </div>
      )}

      <div className="flex items-center gap-3">
        <label className="flex items-center gap-1 text-gray-400">
          Runs/record
          <input
            type="number"
            min={1}
            max={100}
            value={runsPerRecord}
            onChange={(e) => onRunsPerRecordChange(Math.max(1, Number(e.target.value)))}
            className="w-12 rounded border border-white/10 bg-surface-2 px-1.5 py-0.5 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
          />
        </label>
        {selectedSamples.length > 0 && (
          <span className="text-gray-500">
            = {totalRuns} run{totalRuns !== 1 && "s"}
          </span>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// TechStackField — compact inline tech stack picker
// ---------------------------------------------------------------------------

const FRONTEND_OPTIONS = [
  { value: "react",   label: "React" },
  { value: "nextjs",  label: "Next.js" },
  { value: "vue",     label: "Vue 3" },
  { value: "angular", label: "Angular" },
  { value: "svelte",  label: "Svelte" },
];

const BACKEND_OPTIONS = [
  { value: "fastapi",    label: "FastAPI" },
  { value: "aspnetcore", label: "ASP.NET Core" },
  { value: "express",    label: "Express" },
  { value: "django",     label: "Django REST" },
  { value: "nestjs",     label: "NestJS" },
];

const DATABASE_OPTIONS = [
  { value: "postgresql", label: "PostgreSQL" },
  { value: "mysql",      label: "MySQL" },
  { value: "sqlserver",  label: "SQL Server" },
  { value: "sqlite",     label: "SQLite" },
  { value: "mongodb",    label: "MongoDB" },
];

function TechStackField({
  value,
  onChange,
  required,
}: Readonly<{
  value: string;
  onChange: (val: string) => void;
  required: boolean;
}>) {
  let parsed: { frontend: string; backend: string; database: string } = {
    frontend: "react",
    backend: "fastapi",
    database: "postgresql",
  };
  try {
    const candidate = JSON.parse(value);
    if (candidate && typeof candidate === "object") parsed = { ...parsed, ...candidate };
  } catch {
    /* use defaults */
  }

  const update = (key: "frontend" | "backend" | "database", val: string) => {
    onChange(JSON.stringify({ ...parsed, [key]: val }));
  };

  const cls =
    "rounded border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none";

  return (
    <div className="flex flex-wrap items-end gap-2" data-testid="input-tech_stack">
      <span className="text-[11px] text-gray-500">
        Stack{required && <span className="ml-0.5 text-red-400">*</span>}
      </span>
      <label className="text-[10px] text-gray-600">
        FE
        <select value={parsed.frontend} onChange={(e) => update("frontend", e.target.value)} aria-label="Frontend framework" className={`ml-0.5 ${cls}`}>
          {FRONTEND_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      </label>
      <label className="text-[10px] text-gray-600">
        BE
        <select value={parsed.backend} onChange={(e) => update("backend", e.target.value)} aria-label="Backend framework" className={`ml-0.5 ${cls}`}>
          {BACKEND_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      </label>
      <label className="text-[10px] text-gray-600">
        DB
        <select value={parsed.database} onChange={(e) => update("database", e.target.value)} aria-label="Database" className={`ml-0.5 ${cls}`}>
          {DATABASE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      </label>
    </div>
  );
}
