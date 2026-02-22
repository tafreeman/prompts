import { useState } from "react";
import { Link } from "react-router-dom";
import { Workflow, ChevronRight, Search } from "lucide-react";
import { useWorkflows } from "../hooks/useWorkflows";

export default function WorkflowsPage() {
  const { data: workflows, isLoading } = useWorkflows();
  const [searchQuery, setSearchQuery] = useState("");

  const filteredWorkflows = workflows?.filter((name) =>
    name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-4xl space-y-6 p-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-xl font-semibold">Workflows</h1>
            <p className="mt-1 text-sm text-gray-500">
              Available workflow definitions
            </p>
          </div>
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search workflows..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-md border border-white/10 bg-surface-2 py-2 pl-9 pr-4 text-sm text-gray-200 placeholder-gray-500 focus:border-accent-blue focus:outline-none focus:ring-1 focus:ring-accent-blue"
            />
          </div>
        </div>

        {isLoading && (
          <div className="space-y-2">
            {Array.from({ length: 3 }).map((_, i) => (
              <div key={i} className="card animate-pulse h-20" />
            ))}
          </div>
        )}

        <div className="space-y-2">
          {filteredWorkflows?.map((name) => (
            <Link
              key={name}
              to={`/workflows/${name}`}
              className="card-hover flex items-center gap-4"
            >
              <Workflow className="h-5 w-5 text-accent-blue" />
              <div className="flex-1">
                <div className="font-medium text-gray-200">{name}</div>
                <div className="text-xs text-gray-600">
                  {name.replace(/_/g, " ")}
                </div>
              </div>
              <ChevronRight className="h-4 w-4 text-gray-600" />
            </Link>
          ))}

          {filteredWorkflows?.length === 0 && !isLoading && (
            <div className="text-center text-gray-600 py-12">
              No workflows found matching "{searchQuery}".
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
