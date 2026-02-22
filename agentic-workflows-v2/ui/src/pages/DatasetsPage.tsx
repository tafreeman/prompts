import { Database, FileJson, Link2 } from "lucide-react";
import { useEvaluationDatasets } from "../hooks/useWorkflows";

export default function DatasetsPage() {
  const { data: datasets, isLoading, error } = useEvaluationDatasets();

  return (
    <div className="h-full overflow-y-auto">
      <div className="mx-auto max-w-6xl space-y-6 p-6">
        <div>
          <h1 className="text-xl font-semibold">Datasets</h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage your evaluation datasets.
          </p>
        </div>

        {isLoading ? (
          <div className="flex h-32 items-center justify-center text-gray-500">
            Loading datasets...
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-500">
            Failed to load datasets.
          </div>
        ) : !datasets ? (
          <div className="rounded-lg border border-white/10 bg-surface-1 p-6 text-center text-gray-500">
            No datasets available.
          </div>
        ) : (
          <div className="space-y-8">
            {/* Repository Datasets */}
            <section>
              <h2 className="mb-4 text-lg font-medium text-gray-200">Repository Datasets</h2>
              {datasets.repository.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No repository datasets found.</p>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {datasets.repository.map((ds) => (
                    <div key={ds.id} className="rounded-lg border border-white/5 bg-surface-1 p-4 shadow-sm">
                      <div className="flex items-start gap-3">
                        <Database className="mt-0.5 h-5 w-5 text-blue-500 opacity-80" />
                        <div>
                          <h3 className="text-sm font-semibold text-gray-200">{ds.name}</h3>
                          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
                            <span className="font-mono">{ds.id}</span>
                            {ds.sample_count != null && (
                              <>
                                <span>&bull;</span>
                                <span>{ds.sample_count} samples</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                      <p className="mt-3 text-xs text-gray-400 leading-relaxed line-clamp-3">
                        {ds.description || "No description provided."}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Local Datasets */}
            <section>
              <h2 className="mb-4 text-lg font-medium text-gray-200">Local Datasets</h2>
              {datasets.local.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No local datasets found.</p>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {datasets.local.map((ds) => (
                    <div key={ds.id} className="rounded-lg border border-white/5 bg-surface-1 p-4 shadow-sm">
                      <div className="flex items-start gap-3">
                        <FileJson className="mt-0.5 h-5 w-5 text-amber-500 opacity-80" />
                        <div>
                          <h3 className="text-sm font-semibold text-gray-200">{ds.name}</h3>
                          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
                            <span className="font-mono">{ds.id}</span>
                            {ds.sample_count != null && (
                              <>
                                <span>&bull;</span>
                                <span>{ds.sample_count} samples</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>
                      <p className="mt-3 text-xs text-gray-400 leading-relaxed line-clamp-3">
                        {ds.description || "No description provided."}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </section>

            {/* Evaluation Sets */}
            <section>
              <h2 className="mb-4 text-lg font-medium text-gray-200">Evaluation Sets</h2>
              {datasets.eval_sets.length === 0 ? (
                <p className="text-sm text-gray-500 italic">No evaluation sets found.</p>
              ) : (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {datasets.eval_sets.map((es) => (
                    <div key={es.id} className="rounded-lg border border-white/5 bg-surface-1 p-4 shadow-sm">
                      <div className="flex items-start gap-3">
                        <Link2 className="mt-0.5 h-5 w-5 text-purple-500 opacity-80" />
                        <div>
                          <h3 className="text-sm font-semibold text-gray-200">{es.name}</h3>
                          <div className="mt-1 flex items-center gap-2 text-xs text-gray-500">
                            <span className="font-mono">{es.id}</span>
                            <span>&bull;</span>
                            <span>{es.datasets.length} linked datasets</span>
                          </div>
                        </div>
                      </div>
                      <p className="mt-3 text-xs text-gray-400 leading-relaxed line-clamp-3">
                        {es.description || "No description provided."}
                      </p>
                      {es.datasets.length > 0 && (
                        <div className="mt-3 flex flex-wrap gap-1">
                          {es.datasets.map(d => (
                            <span key={d} className="rounded bg-white/5 px-1.5 py-0.5 text-[10px] text-gray-400 font-mono">
                              {d}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </section>
          </div>
        )}
      </div>
    </div>
  );
}
