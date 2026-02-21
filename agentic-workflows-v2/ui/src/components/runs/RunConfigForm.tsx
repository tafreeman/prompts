import { useState, useEffect, useCallback } from "react";
import { Settings2, Cpu, FlaskConical, Database } from "lucide-react";
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
  /** Workflow input parameter values keyed by input name. */
  inputValues: Record<string, string>;
  /** Runtime execution profile (subprocess / docker, max_attempts …). */
  executionProfile: ExecutionProfileRequest;
  /** Rubric override id (empty string = use workflow default). */
  rubricId: string;
  /** Evaluation configuration. */
  evaluation: {
    enabled: boolean;
    datasetSource: "none" | "repository" | "local" | "eval_set";
    datasetId: string;
    evalSetId: string;
    /** Selected sample indices to run (multi-select). */
    selectedSamples: number[];
    /** How many times to run each selected record. */
    runsPerRecord: number;
  };
}

export interface RunConfigFormProps {
  /** Workflow input schema (from DAG response). */
  inputs: WorkflowInputSchema[];
  /** Workflow name, used to preview dataset-to-input mapping. */
  workflowName: string;
  /** Called whenever any configuration value changes. */
  onChange: (values: RunConfigValues) => void;
}

// ---------------------------------------------------------------------------
// RunConfigForm component
// ---------------------------------------------------------------------------

/**
 * Schema-driven run configuration form.
 *
 * Dynamically renders workflow input fields from the schema, and exposes
 * rubric + runtime configuration panels.
 */
export default function RunConfigForm({ inputs, workflowName, onChange }: RunConfigFormProps) {
  // -- Input values ----------------------------------------------------------
  const [inputValues, setInputValues] = useState<Record<string, string>>({});

  // Initialise defaults from schema
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
  const [evalDatasetSource, setEvalDatasetSource] = useState<"none" | "repository" | "local" | "eval_set">("none");
  const [evalDatasetId, setEvalDatasetId] = useState<string>("");
  const [evalSetId, setEvalSetId] = useState<string>("");
  const [evalSelectedSamples, setEvalSelectedSamples] = useState<number[]>([0]);
  const [evalRunsPerRecord, setEvalRunsPerRecord] = useState<number>(1);
  const [datasets, setDatasets] = useState<EvaluationDatasetsResponse | null>(null);

  // Load available datasets
  useEffect(() => {
    listEvaluationDatasets()
      .then(setDatasets)
      .catch((err) => console.error("Failed to load datasets:", err));
  }, []);

  // Auto-populate workflow inputs when dataset/sample selection changes
  useEffect(() => {
    if (
      !evalEnabled ||
      evalDatasetSource === "none" ||
      evalDatasetSource === "eval_set" ||
      !evalDatasetId
    ) {
      return;
    }

    // Preview using the first selected sample for input auto-population
    const previewIndex = evalSelectedSamples[0] ?? 0;
    previewDatasetInputs(workflowName, evalDatasetSource, evalDatasetId, previewIndex)
      .then((preview) => {
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
      })
      .catch((err) => {
        console.warn("Failed to preview dataset inputs:", err);
      });
  }, [workflowName, evalEnabled, evalDatasetSource, evalDatasetId, evalSelectedSamples]);

  // -- Collapsible sections --------------------------------------------------
  const [showAdvanced, setShowAdvanced] = useState(false);

  // -- Propagate changes upward ----------------------------------------------
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
      evaluation: {
        enabled: evalEnabled,
        datasetSource: evalDatasetSource,
        datasetId: evalDatasetId,
        evalSetId: evalSetId,
        selectedSamples: evalSelectedSamples,
        runsPerRecord: evalRunsPerRecord,
      }
    });
  }, [inputValues, runtime, maxAttempts, maxDuration, containerImage, rubricId,
      evalEnabled, evalDatasetSource, evalDatasetId, evalSetId, evalSelectedSamples, evalRunsPerRecord, onChange]);

  useEffect(() => {
    emitChange();
  }, [emitChange]);

  // -- Helpers ---------------------------------------------------------------
  const handleInputChange = (name: string, value: string) => {
    setInputValues((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div data-testid="run-config-form" className="space-y-4">
      {/* ---- Workflow inputs ---- */}
      {inputs.length > 0 && (
        <div
          className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3"
          data-testid="workflow-inputs"
        >
          {inputs.map((inp) => (
            <SchemaInputField
              key={inp.name}
              schema={inp}
              value={inputValues[inp.name] ?? ""}
              onChange={(val) => handleInputChange(inp.name, val)}
            />
          ))}
        </div>
      )}

      {/* ---- Advanced toggle ---- */}
      <button
        type="button"
        onClick={() => setShowAdvanced((v) => !v)}
        className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-200 transition-colors"
        data-testid="advanced-toggle"
      >
        <Settings2 className="h-3.5 w-3.5" />
        {showAdvanced ? "Hide advanced options" : "Show advanced options"}
      </button>

      {showAdvanced && (
        <div className="space-y-3 rounded-lg border border-white/10 bg-surface-1/60 p-3">
          {/* ---- Evaluation config ---- */}
          <fieldset data-testid="evaluation-config">
            <legend className="mb-2 flex items-center gap-1.5 text-xs font-medium text-gray-300">
              <Database className="h-3.5 w-3.5" />
              Evaluation Dataset
            </legend>

            <div className="space-y-2">
              <label className="flex items-center gap-2 text-xs text-gray-400">
                <input
                  type="checkbox"
                  checked={evalEnabled}
                  onChange={(e) => setEvalEnabled(e.target.checked)}
                  className="rounded border-white/10 bg-surface-2 text-accent-blue focus:ring-accent-blue/50"
                />
                Enable evaluation mode
              </label>

              {evalEnabled && (
                <>
                  <label className="block text-xs text-gray-400">
                    Dataset Source
                    <select
                      value={evalDatasetSource}
                      onChange={(e) => setEvalDatasetSource(e.target.value as any)}
                      className="mt-1 w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                    >
                      <option value="none">None</option>
                      <option value="eval_set">Evaluation Set</option>
                      <option value="repository">Repository Dataset</option>
                      <option value="local">Local Dataset</option>
                    </select>
                  </label>

                  {evalDatasetSource === "eval_set" && datasets?.eval_sets && (
                    <label className="block text-xs text-gray-400">
                      Eval Set
                      <select
                        value={evalSetId}
                        onChange={(e) => setEvalSetId(e.target.value)}
                        className="mt-1 w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                      >
                        <option value="">Select eval set...</option>
                        {datasets.eval_sets.map((set) => (
                          <option key={set.id} value={set.id}>
                            {set.name} ({set.datasets.length} datasets)
                          </option>
                        ))}
                      </select>
                      {evalSetId && datasets.eval_sets.find(s => s.id === evalSetId) && (
                        <p className="mt-1 text-xs text-gray-600">
                          {datasets.eval_sets.find(s => s.id === evalSetId)?.description}
                        </p>
                      )}
                    </label>
                  )}

                  {evalDatasetSource === "repository" && datasets?.repository && (
                    <label className="block text-xs text-gray-400">
                      Repository Dataset
                      <select
                        value={evalDatasetId}
                        onChange={(e) => setEvalDatasetId(e.target.value)}
                        className="mt-1 w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                      >
                        <option value="">Select dataset...</option>
                        {datasets.repository.map((ds) => (
                          <option key={ds.id} value={ds.id}>
                            {ds.name} {ds.sample_count ? `(${ds.sample_count} samples)` : ""}
                          </option>
                        ))}
                      </select>
                    </label>
                  )}

                  {evalDatasetSource === "local" && datasets?.local && (
                    <label className="block text-xs text-gray-400">
                      Local Dataset
                      <select
                        value={evalDatasetId}
                        onChange={(e) => setEvalDatasetId(e.target.value)}
                        className="mt-1 w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                      >
                        <option value="">Select dataset...</option>
                        {datasets.local.map((ds) => (
                          <option key={ds.id} value={ds.id}>
                            {ds.name} {ds.sample_count ? `(${ds.sample_count} samples)` : ""}
                          </option>
                        ))}
                      </select>
                    </label>
                  )}

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
                </>
              )}
            </div>
          </fieldset>

          {/* ---- Rubric config ---- */}
          <fieldset data-testid="rubric-config">
            <legend className="mb-1 flex items-center gap-1.5 text-xs font-medium text-gray-300">
              <FlaskConical className="h-3.5 w-3.5" />
              Rubric override
            </legend>
            <input
              type="text"
              value={rubricId}
              onChange={(e) => setRubricId(e.target.value)}
              placeholder="Leave blank for workflow default"
              aria-label="Rubric ID"
              className="w-full max-w-sm rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
            />
            <p className="mt-0.5 text-xs text-gray-600">
              Optionally override the workflow&apos;s default rubric for scoring.
            </p>
          </fieldset>

          {/* ---- Runtime config ---- */}
          <fieldset data-testid="runtime-config">
            <legend className="mb-1 flex items-center gap-1.5 text-xs font-medium text-gray-300">
              <Cpu className="h-3.5 w-3.5" />
              Runtime
            </legend>
            <div className="flex flex-wrap items-center gap-4">
              <label className="text-xs text-gray-400">
                Engine
                <select
                  value={runtime}
                  onChange={(e) =>
                    setRuntime(e.target.value as "subprocess" | "docker")
                  }
                  aria-label="Runtime engine"
                  className="ml-2 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                >
                  <option value="subprocess">Subprocess (default)</option>
                  <option value="docker">Docker</option>
                </select>
              </label>

              <label className="text-xs text-gray-400">
                Max attempts
                <input
                  type="number"
                  min={1}
                  value={maxAttempts}
                  onChange={(e) => setMaxAttempts(e.target.value)}
                  placeholder="–"
                  aria-label="Max attempts"
                  className="ml-2 w-16 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                />
              </label>

              <label className="text-xs text-gray-400">
                Max duration (min)
                <input
                  type="number"
                  min={1}
                  value={maxDuration}
                  onChange={(e) => setMaxDuration(e.target.value)}
                  placeholder="–"
                  aria-label="Max duration minutes"
                  className="ml-2 w-16 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
                />
              </label>

              {runtime === "docker" && (
                <label className="text-xs text-gray-400">
                  Container image
                  <input
                    type="text"
                    value={containerImage}
                    onChange={(e) => setContainerImage(e.target.value)}
                    placeholder="e.g. python:3.12-slim"
                    aria-label="Container image"
                    className="ml-2 w-48 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
                  />
                </label>
              )}
            </div>
          </fieldset>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// SampleSelector — multi-select checkboxes for dataset samples + repeat count
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
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400">
          Records
          {sampleCount !== null && ` (${sampleCount} available)`}
        </span>
        <div className="flex items-center gap-3">
          {sampleCount !== null && sampleCount <= 50 && (
            <button
              type="button"
              onClick={selectAll}
              className="text-xs text-accent-blue hover:underline"
            >
              Select all
            </button>
          )}
          {selectedSamples.length > 0 && (
            <button
              type="button"
              onClick={() => onSelectedSamplesChange([])}
              className="text-xs text-gray-500 hover:text-gray-300"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Checkbox grid — show up to 50 samples */}
      {sampleCount === null ? (
        /* No sample count known — show a manual index input */
        <div className="flex items-center gap-2">
          <input
            type="number"
            min={0}
            placeholder="Index"
            className="w-24 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                const val = Number((e.target as HTMLInputElement).value);
                if (selectedSamples.includes(val)) return;
                onSelectedSamplesChange([...selectedSamples, val].sort((a, b) => a - b));
                (e.target as HTMLInputElement).value = "";
              }
            }}
          />
          <span className="text-xs text-gray-600">Press Enter to add</span>
          {selectedSamples.length > 0 && (
            <span className="text-xs text-gray-400">
              Selected: {selectedSamples.join(", ")}
            </span>
          )}
        </div>
      ) : (
        <div className="max-h-40 overflow-y-auto rounded-md border border-white/10 bg-surface-2 p-2">
          <div className="grid grid-cols-5 gap-1 sm:grid-cols-8 lg:grid-cols-10">
            {Array.from({ length: Math.min(sampleCount, 50) }, (_, i) => (
              <label
                key={i}
                className={`flex cursor-pointer items-center justify-center rounded px-1.5 py-1 text-xs transition-colors ${
                  selectedSamples.includes(i)
                    ? "bg-accent-blue/20 text-accent-blue"
                    : "text-gray-500 hover:bg-white/5 hover:text-gray-300"
                }`}
              >
                <input
                  type="checkbox"
                  className="sr-only"
                  checked={selectedSamples.includes(i)}
                  onChange={() => toggleSample(i)}
                />
                {i}
              </label>
            ))}
            {sampleCount > 50 && (
              <span className="col-span-full text-center text-xs text-gray-600">
                Showing first 50 of {sampleCount}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Runs per record + summary */}
      <div className="flex items-center gap-4">
        <label className="flex items-center gap-2 text-xs text-gray-400">
          {"Runs per record"}
          <input
            type="number"
            min={1}
            max={100}
            value={runsPerRecord}
            onChange={(e) => onRunsPerRecordChange(Math.max(1, Number(e.target.value)))}
            className="w-16 rounded-md border border-white/10 bg-surface-2 px-2 py-1 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none"
          />
        </label>
        {selectedSamples.length > 0 && (
          <span className="text-xs text-gray-500">
            {totalRuns} total {totalRuns === 1 ? "run" : "runs"}
            {" "}({selectedSamples.length} {selectedSamples.length === 1 ? "record" : "records"} × {runsPerRecord})
          </span>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// TechStackField — structured dropdowns for the tech_stack object input
// ---------------------------------------------------------------------------

const FRONTEND_OPTIONS = [
  { value: "react",   label: "React" },
  { value: "nextjs",  label: "Next.js" },
  { value: "vue",     label: "Vue 3" },
  { value: "angular", label: "Angular" },
  { value: "svelte",  label: "Svelte" },
];

const BACKEND_OPTIONS = [
  { value: "fastapi",    label: "FastAPI (Python)" },
  { value: "aspnetcore", label: "ASP.NET Core 8 (.NET)" },
  { value: "express",    label: "Express (Node.js)" },
  { value: "django",     label: "Django REST (Python)" },
  { value: "nestjs",     label: "NestJS (Node.js)" },
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
  // Parse the current JSON value (or fall back to defaults)
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

  const selectClass =
    "w-full rounded-md border border-white/10 bg-surface-2 px-2 py-1.5 text-xs text-gray-200 focus:border-accent-blue/50 focus:outline-none";

  return (
    <div className="sm:col-span-2 lg:col-span-3" data-testid="input-tech_stack">
      <span className="mb-1.5 block text-xs font-medium text-gray-400">
        Tech Stack{required && <span className="ml-0.5 text-red-400">*</span>}
      </span>
      <div className="grid grid-cols-3 gap-2">
        <label className="space-y-0.5">
          <span className="text-xs text-gray-500">Frontend</span>
          <select
            value={parsed.frontend}
            onChange={(e) => update("frontend", e.target.value)}
            aria-label="Frontend framework"
            className={selectClass}
          >
            {FRONTEND_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </label>
        <label className="space-y-0.5">
          <span className="text-xs text-gray-500">Backend</span>
          <select
            value={parsed.backend}
            onChange={(e) => update("backend", e.target.value)}
            aria-label="Backend framework"
            className={selectClass}
          >
            {BACKEND_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </label>
        <label className="space-y-0.5">
          <span className="text-xs text-gray-500">Database</span>
          <select
            value={parsed.database}
            onChange={(e) => update("database", e.target.value)}
            aria-label="Database"
            className={selectClass}
          >
            {DATABASE_OPTIONS.map((o) => (
              <option key={o.value} value={o.value}>{o.label}</option>
            ))}
          </select>
        </label>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SchemaInputField — renders a single input based on its schema
// ---------------------------------------------------------------------------

function SchemaInputField({
  schema,
  value,
  onChange,
}: {
  schema: WorkflowInputSchema;
  value: string;
  onChange: (val: string) => void;
}) {
  const label = schema.name.replace(/_/g, " ");

  // Enum -> dropdown
  if (schema.enum) {
    return (
      <div>
        <label className="mb-1 block text-xs font-medium text-gray-400">
          {label}
          {schema.required && <span className="ml-0.5 text-red-400">*</span>}
        </label>
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          aria-label={label}
          required={schema.required}
          data-testid={`input-${schema.name}`}
          className="w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 focus:border-accent-blue/50 focus:outline-none"
        >
          {!value && <option value="">Select...</option>}
          {schema.enum.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
        {schema.description && (
          <p className="mt-0.5 text-xs text-gray-600">{schema.description}</p>
        )}
      </div>
    );
  }

  // tech_stack object -> structured stack picker
  if (schema.name === "tech_stack" && schema.type === "object") {
    return (
      <TechStackField
        value={value}
        onChange={onChange}
        required={schema.required}
      />
    );
  }

  // Object / array -> textarea
  if (schema.type === "object" || schema.type === "array") {
    return (
      <div className="sm:col-span-2 lg:col-span-3">
        <label className="mb-1 block text-xs font-medium text-gray-400">
          {label}
          {schema.required && <span className="ml-0.5 text-red-400">*</span>}
        </label>
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          rows={3}
          placeholder={schema.description || "JSON value"}
          required={schema.required}
          data-testid={`input-${schema.name}`}
          className="w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 font-mono text-xs text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
        />
        {schema.description && (
          <p className="mt-0.5 text-xs text-gray-600">{schema.description}</p>
        )}
      </div>
    );
  }

  // Default -> text input
  return (
    <div>
      <label className="mb-1 block text-xs font-medium text-gray-400">
        {label}
        {schema.required && <span className="ml-0.5 text-red-400">*</span>}
      </label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={schema.description || schema.name}
        required={schema.required}
        data-testid={`input-${schema.name}`}
        className="w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
      />
      {schema.description && (
        <p className="mt-0.5 text-xs text-gray-600">{schema.description}</p>
      )}
    </div>
  );
}
