import { useMemo, useState, type ReactNode } from "react";
import { ChevronDown, ChevronRight, Cpu, Timer } from "lucide-react";
import StatusBadge from "../common/StatusBadge";
import DurationDisplay from "../common/DurationDisplay";
import JsonViewer from "../common/JsonViewer";
import type { StepState } from "../../hooks/useWorkflowStream";

interface Props {
  stepStates: Map<string, StepState>;
  stepOrder?: string[];
  selectedStep: string | null;
  onSelectStep: (stepName: string | null) => void;
}

function orderedStepNames(stepStates: Map<string, StepState>, stepOrder?: string[]): string[] {
  const known = new Set(stepStates.keys());
  const ordered: string[] = [];
  const seen = new Set<string>();

  for (const name of stepOrder ?? []) {
    if (known.has(name) && !seen.has(name)) {
      ordered.push(name);
      seen.add(name);
    }
  }

  for (const name of stepStates.keys()) {
    if (!seen.has(name)) {
      ordered.push(name);
      seen.add(name);
    }
  }

  return ordered;
}

export default function LiveStepDetails({
  stepStates,
  stepOrder,
  selectedStep,
  onSelectStep,
}: Readonly<Props>) {
  const names = useMemo(
    () => orderedStepNames(stepStates, stepOrder),
    [stepStates, stepOrder]
  );

  if (names.length === 0) {
    return (
      <div className="rounded-lg border border-white/5 bg-surface-1 px-3 py-4 text-center text-xs text-gray-600">
        Waiting for step updates...
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {names.map((name) => {
        const step = stepStates.get(name);
        if (!step) return null;

        const isOpen = selectedStep === name;
        return (
          <StepPanel
            key={name}
            stepName={name}
            step={step}
            isOpen={isOpen}
            onToggle={() => onSelectStep(isOpen ? null : name)}
          />
        );
      })}
    </div>
  );
}

function StepPanel({
  stepName,
  step,
  isOpen,
  onToggle,
}: Readonly<{
  stepName: string;
  step: StepState;
  isOpen: boolean;
  onToggle: () => void;
}>) {
  const [tab, setTab] = useState<"output" | "input">("output");
  const hasInput = step.input !== undefined;
  const hasOutput = step.output !== undefined;
  let content: ReactNode;

  if (tab === "input") {
    content = hasInput ? (
      <JsonViewer data={step.input} defaultExpanded maxDepth={3} />
    ) : (
      <div className="text-xs text-gray-600">No input captured yet.</div>
    );
  } else {
    content = hasOutput ? (
      <JsonViewer data={step.output} defaultExpanded maxDepth={3} />
    ) : (
      <div className="text-xs text-gray-600">No output captured yet.</div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border border-white/5 bg-surface-1">
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full items-center gap-3 px-3 py-2.5 text-left transition-colors hover:bg-surface-2/30"
      >
        {isOpen ? (
          <ChevronDown className="h-4 w-4 text-gray-500" />
        ) : (
          <ChevronRight className="h-4 w-4 text-gray-500" />
        )}

        <span className="flex-1 truncate text-sm font-medium text-gray-200">{stepName}</span>

        <div className="flex items-center gap-2 text-[11px] text-gray-500">
          {step.durationMs != null && (
            <span className="flex items-center gap-1">
              <Timer className="h-3 w-3" />
              <DurationDisplay ms={step.durationMs} />
            </span>
          )}
          {step.tokensUsed != null && (
            <span className="flex items-center gap-1">
              <Cpu className="h-3 w-3" />
              {step.tokensUsed.toLocaleString()}
            </span>
          )}
        </div>

        <StatusBadge status={step.status} size="sm" />
      </button>

      {isOpen && (
        <div className="border-t border-white/5 px-3 py-3">
          {step.error && (
            <div className="mb-3 rounded-md border border-red-500/20 bg-red-500/10 px-3 py-2 text-xs text-red-400">
              {step.error}
            </div>
          )}

          <div className="mb-3 flex gap-1">
            {(["output", "input"] as const).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTab(t)}
                className={`rounded-md px-3 py-1 text-xs font-medium transition-colors ${
                  tab === t
                    ? "bg-white/10 text-gray-200"
                    : "text-gray-500 hover:text-gray-300"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>

          <div className="max-h-72 overflow-y-auto rounded-md bg-surface-0 p-3">
            {content}
          </div>

          <div className="mt-3 flex flex-wrap gap-3 text-xs text-gray-600">
            {step.tier && <span>Tier: {step.tier}</span>}
            {step.modelUsed && <span>Model: {step.modelUsed}</span>}
            {step.tokensUsed != null && <span>Tokens: {step.tokensUsed.toLocaleString()}</span>}
          </div>
        </div>
      )}
    </div>
  );
}
