interface Attempt {
  attempt_number: number;
  status: string;
  duration_ms: number;
  failed_steps: string[];
}

interface IterationTimelineProps {
  attempts: Attempt[];
}

export default function IterationTimeline({ attempts }: IterationTimelineProps) {
  if (attempts.length === 0) {
    return null;
  }

  const lastIndex = attempts.length - 1;

  return (
    <div className="rounded-lg border border-white/10 bg-surface-1 p-3">
      <div className="mb-2 text-xs uppercase tracking-wide text-gray-500">
        Iteration Timeline
      </div>
      <div className="space-y-3">
        {attempts.map((attempt, index) => {
          const isSuccess = attempt.status.toLowerCase() === "success";
          const isLast = index === lastIndex;
          const statusClass = isSuccess
            ? "bg-green-500/20 text-green-300"
            : "bg-red-500/20 text-red-300";

          return (
            <div key={attempt.attempt_number} className="flex items-start gap-3">
              <div className="mt-1 flex flex-col items-center">
                <div
                  data-testid="iteration-node"
                  className={`h-3.5 w-3.5 rounded-full border border-white/30 bg-surface-2 ${
                    isLast ? "ring-2 ring-blue-500" : ""
                  }`}
                />
                {index < lastIndex && <div className="mt-1 h-6 w-px bg-white/20" />}
              </div>

              <div className="min-w-0 flex-1 rounded bg-surface-2/60 px-3 py-2">
                <div className="flex items-center justify-between gap-2">
                  <div className="text-sm font-medium text-gray-200">
                    Attempt {attempt.attempt_number}
                  </div>
                  <span
                    className={`rounded px-2 py-0.5 text-xs font-medium capitalize ${statusClass}`}
                  >
                    {attempt.status}
                  </span>
                </div>
                <div className="mt-1 text-xs text-gray-400">
                  Duration: {attempt.duration_ms}ms
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export type { Attempt, IterationTimelineProps };
