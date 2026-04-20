import { Database, FileJson, Link2 } from "lucide-react";
import { useEvaluationDatasets } from "../hooks/useWorkflows";
import BTopBar from "../components/layout/BTopBar";
import BBox from "../components/common/BBox";
import BPill from "../components/common/BPill";

export default function DatasetsPage() {
  const { data: datasets, isLoading, error } = useEvaluationDatasets();

  const repoCount = datasets?.repository.length ?? 0;
  const localCount = datasets?.local.length ?? 0;
  const evalSetCount = datasets?.eval_sets.length ?? 0;

  return (
    <div className="flex h-full flex-col">
      <BTopBar path="datasets" />

      <div className="h-full overflow-y-auto">
        <div className="mx-auto max-w-6xl space-y-4 p-6">
          <div>
            <h1
              className="text-[24px] font-semibold text-b-text"
              style={{ letterSpacing: "-0.5px" }}
            >
              Datasets
            </h1>
            <div className="mt-1 font-mono text-[11px] text-b-text-dim">
              $ {repoCount} repo · {localCount} local · {evalSetCount} eval sets
            </div>
          </div>

          {isLoading ? (
            <div className="flex h-32 items-center justify-center font-mono text-[11px] text-b-text-dim">
              $ loading datasets…
            </div>
          ) : error ? (
            <div className="rounded-sm border border-b-red bg-b-red/10 p-4 font-mono text-[11px] text-b-red">
              [!] failed to load datasets
            </div>
          ) : !datasets ? (
            <BBox>
              <div className="p-6 text-center font-mono text-[11px] text-b-text-dim">
                no datasets available
              </div>
            </BBox>
          ) : (
            <div className="space-y-4">
              {/* Repository */}
              <BBox title="▥ repository · public">
                {datasets.repository.length === 0 ? (
                  <div className="p-4 font-mono text-[11px] italic text-b-text-dim">
                    no repository datasets
                  </div>
                ) : (
                  <div className="grid gap-px bg-b-line-soft sm:grid-cols-2 lg:grid-cols-3">
                    {datasets.repository.map((ds) => (
                      <div
                        key={ds.id}
                        className="bg-b-bg1 p-3 transition-colors hover:bg-b-bg2"
                      >
                        <div className="flex items-start gap-2">
                          <Database className="mt-0.5 h-3.5 w-3.5 shrink-0 text-b-blue" />
                          <div className="min-w-0 flex-1">
                            <div className="truncate font-mono text-[12px] font-semibold text-b-text">
                              {ds.name}
                            </div>
                            <div className="mt-0.5 flex items-center gap-2 font-mono text-[10px] text-b-text-dim">
                              <span>#{ds.id}</span>
                              {ds.sample_count != null && (
                                <BPill tone="dim">
                                  {ds.sample_count} samples
                                </BPill>
                              )}
                            </div>
                          </div>
                        </div>
                        <p className="mt-2 line-clamp-3 font-mono text-[10px] leading-relaxed text-b-text-mid">
                          {ds.description || "no description"}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </BBox>

              {/* Local */}
              <BBox title="▨ local · project">
                {datasets.local.length === 0 ? (
                  <div className="p-4 font-mono text-[11px] italic text-b-text-dim">
                    no local datasets
                  </div>
                ) : (
                  <div className="grid gap-px bg-b-line-soft sm:grid-cols-2 lg:grid-cols-3">
                    {datasets.local.map((ds) => (
                      <div
                        key={ds.id}
                        className="bg-b-bg1 p-3 transition-colors hover:bg-b-bg2"
                      >
                        <div className="flex items-start gap-2">
                          <FileJson className="mt-0.5 h-3.5 w-3.5 shrink-0 text-b-amber" />
                          <div className="min-w-0 flex-1">
                            <div className="truncate font-mono text-[12px] font-semibold text-b-text">
                              {ds.name}
                            </div>
                            <div className="mt-0.5 flex items-center gap-2 font-mono text-[10px] text-b-text-dim">
                              <span>#{ds.id}</span>
                              {ds.sample_count != null && (
                                <BPill tone="dim">
                                  {ds.sample_count} samples
                                </BPill>
                              )}
                            </div>
                          </div>
                        </div>
                        <p className="mt-2 line-clamp-3 font-mono text-[10px] leading-relaxed text-b-text-mid">
                          {ds.description || "no description"}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </BBox>

              {/* Eval sets */}
              <BBox title="◇ evaluation sets">
                {datasets.eval_sets.length === 0 ? (
                  <div className="p-4 font-mono text-[11px] italic text-b-text-dim">
                    no evaluation sets
                  </div>
                ) : (
                  <div className="grid gap-px bg-b-line-soft sm:grid-cols-2 lg:grid-cols-3">
                    {datasets.eval_sets.map((es) => (
                      <div
                        key={es.id}
                        className="bg-b-bg1 p-3 transition-colors hover:bg-b-bg2"
                      >
                        <div className="flex items-start gap-2">
                          <Link2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-b-purple" />
                          <div className="min-w-0 flex-1">
                            <div className="truncate font-mono text-[12px] font-semibold text-b-text">
                              {es.name}
                            </div>
                            <div className="mt-0.5 font-mono text-[10px] text-b-text-dim">
                              #{es.id} · {es.datasets.length} linked
                            </div>
                          </div>
                        </div>
                        <p className="mt-2 line-clamp-3 font-mono text-[10px] leading-relaxed text-b-text-mid">
                          {es.description || "no description"}
                        </p>
                        {es.datasets.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {es.datasets.map((d) => (
                              <span
                                key={d}
                                className="rounded-sm bg-b-bg3 px-1.5 py-0.5 font-mono text-[9px] text-b-text-mid"
                              >
                                {d}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </BBox>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
