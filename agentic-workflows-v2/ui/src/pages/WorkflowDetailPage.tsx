import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Play, ArrowLeft } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { useWorkflowDAG } from "../hooks/useWorkflows";
import { useRuns } from "../hooks/useRuns";
import { runWorkflow } from "../api/client";
import WorkflowDAG from "../components/dag/WorkflowDAG";
import RunList from "../components/runs/RunList";
import type { WorkflowInputSchema } from "../api/types";

export default function WorkflowDetailPage() {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const { data: dag, isLoading: dagLoading } = useWorkflowDAG(name);
  const { data: runs, isLoading: runsLoading } = useRuns(name);
  const [inputValues, setInputValues] = useState<Record<string, string>>({});

  // Initialize defaults from schema when DAG loads
  useEffect(() => {
    if (dag?.inputs) {
      const defaults: Record<string, string> = {};
      for (const inp of dag.inputs) {
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
    }
  }, [dag]);

  const buildInputData = (): Record<string, unknown> => {
    const data: Record<string, unknown> = {};
    if (!dag?.inputs) return data;
    for (const inp of dag.inputs) {
      const val = inputValues[inp.name] ?? "";
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
    mutationFn: () =>
      runWorkflow({
        workflow: name!,
        input_data: buildInputData(),
      }),
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
            {runMutation.isPending ? "Starting..." : "Run Workflow"}
          </button>
        </div>

        {/* Input form */}
        {hasInputs && (
          <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {dag.inputs!.map((inp: WorkflowInputSchema) => (
              <InputField
                key={inp.name}
                schema={inp}
                value={inputValues[inp.name] ?? ""}
                onChange={(val) =>
                  setInputValues((prev) => ({ ...prev, [inp.name]: val }))
                }
              />
            ))}
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

/** Renders a single input field based on its schema. */
function InputField({
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

  // Object/array -> textarea
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
        className="w-full rounded-md border border-white/10 bg-surface-2 px-3 py-1.5 text-sm text-gray-200 placeholder-gray-600 focus:border-accent-blue/50 focus:outline-none"
      />
      {schema.description && (
        <p className="mt-0.5 text-xs text-gray-600">{schema.description}</p>
      )}
    </div>
  );
}
