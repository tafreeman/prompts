import type { EvaluationResult } from "../../api/types";

interface Props {
  evaluation: EvaluationResult;
  className?: string;
}

export default function ScoreBreakdownPanel({
  evaluation,
  className = "",
}: Props) {
  return (
    <div className={`rounded-lg border border-white/10 bg-surface-1 p-3 ${className}`}>
      <div className="mb-2 text-xs uppercase tracking-wide text-gray-500">
        Score Breakdown
      </div>

      <div className="space-y-1 text-xs text-gray-300">
        {evaluation.criteria.map((criterion) => (
          <div
            key={criterion.criterion}
            className="flex items-center justify-between rounded bg-surface-2/60 px-2 py-1"
          >
            <span className="truncate text-gray-400">{criterion.criterion}</span>
            <span>
              {criterion.score.toFixed(2)} x {criterion.weight.toFixed(2)}
            </span>
          </div>
        ))}
      </div>

      {!!evaluation.hard_gate_failures?.length && (
        <div className="mt-3">
          <div className="text-xs font-medium text-red-400">Hard Gate Failures</div>
          <ul className="mt-1 space-y-1 text-xs text-red-300">
            {evaluation.hard_gate_failures.map((failure) => (
              <li key={failure} className="rounded bg-red-500/10 px-2 py-1">
                {failure}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!!evaluation.floor_violations?.length && (
        <div className="mt-3">
          <div className="text-xs font-medium text-amber-400">Floor Violations</div>
          <ul className="mt-1 space-y-1 text-xs text-amber-300">
            {evaluation.floor_violations.map((violation) => (
              <li
                key={`${violation.criterion}:${violation.floor}`}
                className="rounded bg-amber-500/10 px-2 py-1"
              >
                {violation.criterion}: {violation.normalized_score.toFixed(2)} &lt;{" "}
                {violation.floor.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
