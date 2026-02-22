import { Trophy, Clock, CheckCircle2, XCircle, Search } from "lucide-react";
import { useRuns } from "../hooks/useRuns";
import { Link } from "react-router-dom";

export default function EvaluationsPage() {
  const { data: runs, isLoading } = useRuns();

  const evaluatedRuns = runs?.filter(r => r.evaluation_score != null) ?? [];

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl space-y-6 p-6">
        <div>
          <h1 className="text-xl font-semibold">Evaluations</h1>
          <p className="mt-1 text-sm text-gray-500">
            Automated grading and performance benchmarks across runs.
          </p>
        </div>

        {isLoading ? (
          <div className="flex justify-center p-12 text-sm text-gray-500">
            Loading evaluations...
          </div>
        ) : evaluatedRuns.length === 0 ? (
          <div className="rounded-lg border border-dashed border-white/10 p-8 text-center bg-surface-1">
            <Search className="mx-auto h-8 w-8 text-gray-600 mb-3" />
            <h3 className="text-sm font-medium text-gray-300">No evaluations found</h3>
            <p className="mt-1 text-xs text-gray-500">
              Run a workflow with evaluation enabled to see metrics and scores appear here.
            </p>
          </div>
        ) : (
          <div className="overflow-hidden rounded-lg border border-white/5 bg-surface-1 shadow-sm">
            <table className="w-full text-left text-sm text-gray-400">
              <thead className="bg-[#1f1f2e] text-xs font-semibold uppercase tracking-wider text-gray-300">
                <tr>
                  <th className="px-5 py-3">Workflow</th>
                  <th className="px-5 py-3">Score</th>
                  <th className="px-5 py-3">Grade</th>
                  <th className="px-5 py-3">Steps</th>
                  <th className="px-5 py-3">Date</th>
                  <th className="px-5 py-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {evaluatedRuns.map((run) => (
                  <tr key={run.run_id ?? run.filename} className="hover:bg-white/[0.02] transition-colors">
                    <td className="px-5 py-4 font-medium text-gray-200">
                      {run.workflow_name}
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        <Trophy className="h-3.5 w-3.5 text-amber-500" />
                        <span className="font-mono text-gray-300">
                          {run.evaluation_score?.toFixed(1) ?? "N/A"}
                        </span>
                      </div>
                    </td>
                    <td className="px-5 py-4">
                      <span className="inline-flex items-center rounded-full bg-surface-hover px-2.5 py-0.5 text-xs font-medium text-gray-300 ring-1 ring-inset ring-white/10">
                        {run.evaluation_grade || "N/A"}
                      </span>
                    </td>
                    <td className="px-5 py-4">
                      {run.status === "success" ? (
                        <span className="flex items-center gap-1 text-green-400">
                          <CheckCircle2 className="h-4 w-4" />
                          {run.step_count}
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-red-400">
                          <XCircle className="h-4 w-4" />
                          {run.step_count}
                        </span>
                      )}
                    </td>
                    <td className="px-5 py-4 text-xs">
                      <div className="flex items-center gap-1 tabular-nums">
                        <Clock className="h-3.5 w-3.5 text-gray-600" />
                        {run.start_time
                          ? new Date(run.start_time).toLocaleString(undefined, {
                              month: "short",
                              day: "numeric",
                              hour: "numeric",
                              minute: "2-digit",
                            })
                          : "Unknown"}
                      </div>
                    </td>
                    <td className="px-5 py-4 text-right">
                      <Link
                        to={`/runs/${run.filename}`}
                        className="text-xs font-semibold text-blue-500 hover:text-blue-400"
                      >
                        View &rarr;
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
