import { Link } from "react-router-dom";
import { Workflow, ChevronRight } from "lucide-react";
import { useWorkflows } from "../hooks/useWorkflows";

export default function WorkflowsPage() {
  const { data: workflows, isLoading } = useWorkflows();

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-xl font-semibold">Workflows</h1>
        <p className="mt-1 text-sm text-gray-500">
          Available workflow definitions
        </p>
      </div>

      {isLoading && (
        <div className="space-y-2">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="card animate-pulse h-20" />
          ))}
        </div>
      )}

      <div className="space-y-2">
        {workflows?.map((name) => (
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

        {workflows?.length === 0 && (
          <div className="text-center text-gray-600 py-12">
            No workflows found. Add YAML definitions to the workflows/definitions/ directory.
          </div>
        )}
      </div>
    </div>
  );
}
