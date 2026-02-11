import { useState, useEffect, useCallback } from "react";
import { Settings2, Cpu, FlaskConical } from "lucide-react";
import type {
  WorkflowInputSchema,
  ExecutionProfileRequest,
} from "../../api/types";

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
}

export interface RunConfigFormProps {
  /** Workflow input schema (from DAG response). */
  inputs: WorkflowInputSchema[];
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
export default function RunConfigForm({ inputs, onChange }: RunConfigFormProps) {
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

  // -- Collapsible sections --------------------------------------------------
  const [showAdvanced, setShowAdvanced] = useState(false);

  // -- Propagate changes upward ----------------------------------------------
  const emitChange = useCallback(() => {
    const profile: ExecutionProfileRequest = { runtime };
    if (maxAttempts) profile.max_attempts = Number(maxAttempts);
    if (maxDuration) profile.max_duration_minutes = Number(maxDuration);
    if (runtime === "docker" && containerImage)
      profile.container_image = containerImage;

    onChange({ inputValues, executionProfile: profile, rubricId });
  }, [inputValues, runtime, maxAttempts, maxDuration, containerImage, rubricId, onChange]);

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
