import { Link } from "react-router-dom";
import { Workflow, Play, ArrowRight } from "lucide-react";
import { useRuns, useRunsSummary } from "../hooks/useRuns";
import { useWorkflows } from "../hooks/useWorkflows";
import RunSummaryCards from "../components/runs/RunSummaryCards";
import RunList from "../components/runs/RunList";

export default function DashboardPage() {
  const { data: summary, isLoading: summaryLoading } = useRunsSummary();
  const { data: runs, isLoading: runsLoading } = useRuns();
  const { data: workflows } = useWorkflows();

  const hasRuns = (runs?.length ?? 0) > 0;

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl space-y-6 p-6">
        <div>
          <h1 className="text-xl font-semibold">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-500">
            Overview of workflow executions
          </p>
        </div>

        <RunSummaryCards summary={summary} isLoading={summaryLoading} />

        {/* Available workflows - always show */}
        {workflows && workflows.length > 0 && (
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-medium text-gray-400">
                Available Workflows
              </h2>
              <Link
                to="/workflows"
                className="flex items-center gap-1 text-xs text-gray-500 hover:text-accent-blue"
              >
                View all <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {workflows.map((name) => (
                <Link
                  key={name}
                  to={`/workflows/${name}`}
                  className="card-hover flex items-center gap-3"
                >
                  <div className="flex h-9 w-9 items-center justify-center rounded-md bg-accent-blue/10">
                    <Workflow className="h-4 w-4 text-accent-blue" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="truncate text-sm font-medium text-gray-200">
                      {name}
                    </div>
                    <div className="text-xs text-gray-600">
                      {name.replace(/_/g, " ")}
                    </div>
                  </div>
                  <Play className="h-4 w-4 flex-shrink-0 text-gray-600" />
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Empty state */}
        {!hasRuns && !runsLoading && (
          <div className="rounded-lg border border-dashed border-white/10 p-8 text-center">
            <Workflow className="mx-auto h-8 w-8 text-gray-600" />
            <h3 className="mt-3 text-sm font-medium text-gray-400">
              No runs yet
            </h3>
            <p className="mt-1 text-xs text-gray-600">
              Select a workflow above to start your first execution
            </p>
          </div>
        )}

        {/* Recent runs */}
        {hasRuns && (
          <div>
            <h2 className="mb-3 text-sm font-medium text-gray-400">
              Recent Runs
            </h2>
            <RunList runs={runs} isLoading={runsLoading} />
          </div>
        )}
      </div>
    </div>
  );
}
