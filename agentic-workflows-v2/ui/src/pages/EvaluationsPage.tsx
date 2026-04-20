import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useRuns } from "../hooks/useRuns";
import BTopBar from "../components/layout/BTopBar";
import BBox from "../components/common/BBox";
import BPill from "../components/common/BPill";
import BAsciiBar from "../components/common/BAsciiBar";

export default function EvaluationsPage() {
  const { data: runs, isLoading } = useRuns();

  const evaluatedRuns = useMemo(
    () => (runs ?? []).filter((r) => r.evaluation_score != null),
    [runs],
  );

  // Score histogram — 20 buckets 0..100
  const histogram = useMemo(() => {
    const buckets = Array(20).fill(0);
    evaluatedRuns.forEach((r) => {
      const score = r.evaluation_score ?? 0;
      const normalized = score <= 1 ? score * 100 : score;
      const idx = Math.min(19, Math.max(0, Math.floor(normalized / 5)));
      buckets[idx] += 1;
    });
    return buckets;
  }, [evaluatedRuns]);
  const maxBucket = Math.max(1, ...histogram);

  // Pass rate by workflow
  const workflowPassRate = useMemo(() => {
    const map = new Map<string, { total: number; pass: number }>();
    evaluatedRuns.forEach((r) => {
      const key = r.workflow_name ?? "unknown";
      const entry = map.get(key) ?? { total: 0, pass: 0 };
      entry.total += 1;
      const score = r.evaluation_score ?? 0;
      const normalized = score <= 1 ? score * 100 : score;
      if (normalized >= 75) entry.pass += 1;
      map.set(key, entry);
    });
    return Array.from(map.entries()).map(([name, v]) => ({
      name,
      rate: v.pass / v.total,
      total: v.total,
    }));
  }, [evaluatedRuns]);

  return (
    <div className="flex h-full flex-col">
      <BTopBar path="evaluations" />

      <div className="h-full overflow-y-auto">
        <div className="mx-auto max-w-6xl space-y-3 p-6">
          <div>
            <h1
              className="text-[24px] font-semibold text-b-text"
              style={{ letterSpacing: "-0.5px" }}
            >
              Evaluations
            </h1>
            <div className="mt-1 font-mono text-[11px] text-b-text-dim">
              $ {evaluatedRuns.length} runs scored · automated grading across
              workflows
            </div>
          </div>

          {isLoading ? (
            <div className="flex justify-center p-12 font-mono text-[11px] text-b-text-dim">
              $ loading evaluations…
            </div>
          ) : evaluatedRuns.length === 0 ? (
            <BBox>
              <div className="p-8 text-center font-mono text-[11px] text-b-text-dim">
                no evaluations yet · run a workflow with eval enabled
              </div>
            </BBox>
          ) : (
            <>
              {/* Top row: histogram + workflow pass rates */}
              <div className="grid grid-cols-1 gap-2.5 lg:grid-cols-5">
                <div className="lg:col-span-3">
                  <BBox title="score distribution · 20 buckets">
                    <div className="p-4">
                      <div className="flex h-[120px] items-end gap-[3px]">
                        {histogram.map((c, i) => {
                          const h = (c / maxBucket) * 100;
                          const mid = i * 5 + 2.5;
                          const color =
                            mid < 50
                              ? "bg-b-red"
                              : mid < 75
                                ? "bg-b-clay"
                                : "bg-b-green";
                          return (
                            <div
                              key={i}
                              className="flex flex-1 flex-col justify-end"
                              title={`${i * 5}–${i * 5 + 5}: ${c} run${c === 1 ? "" : "s"}`}
                            >
                              {c > 0 ? (
                                <div
                                  className={color}
                                  style={{ height: `${h}%` }}
                                />
                              ) : (
                                <div className="h-[2px] bg-b-line-soft" />
                              )}
                            </div>
                          );
                        })}
                      </div>
                      <div className="mt-2 flex justify-between font-mono text-[10px] text-b-text-faint">
                        <span>0</span>
                        <span>50</span>
                        <span>100</span>
                      </div>
                    </div>
                  </BBox>
                </div>
                <div className="lg:col-span-2">
                  <BBox title="pass rate by workflow">
                    <div className="space-y-2 p-3">
                      {workflowPassRate.length === 0 && (
                        <div className="font-mono text-[11px] text-b-text-dim">
                          no data
                        </div>
                      )}
                      {workflowPassRate.map((w) => (
                        <div key={w.name}>
                          <div className="flex items-center justify-between font-mono text-[11px]">
                            <span className="truncate text-b-text-mid">
                              {w.name}
                            </span>
                            <span className="tabular-nums text-b-text-dim">
                              {(w.rate * 100).toFixed(0)}% · {w.total}
                            </span>
                          </div>
                          <div className="mt-0.5">
                            <BAsciiBar
                              value={w.rate}
                              width={22}
                              color={
                                w.rate >= 0.75
                                  ? "b-green"
                                  : w.rate >= 0.5
                                    ? "b-amber"
                                    : "b-red"
                              }
                            />
                          </div>
                        </div>
                      ))}
                    </div>
                  </BBox>
                </div>
              </div>

              {/* Eval runs table */}
              <BBox title="eval runs">
                <div className="overflow-x-auto">
                  <table className="w-full font-mono text-[11px]">
                    <thead>
                      <tr className="border-b border-b-line text-left text-[10px] uppercase tracking-[0.5px] text-b-text-faint">
                        <th className="px-3 py-2">WORKFLOW</th>
                        <th className="w-[60px] px-3 py-2 text-right">
                          SCORE
                        </th>
                        <th className="w-[180px] px-3 py-2">PROGRESS</th>
                        <th className="w-[60px] px-3 py-2">GRADE</th>
                        <th className="w-[60px] px-3 py-2">PASS</th>
                        <th className="w-[110px] px-3 py-2">WHEN</th>
                        <th className="w-[60px] px-3 py-2 text-right">—</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evaluatedRuns.map((run) => {
                        const raw = run.evaluation_score ?? 0;
                        const pct = raw <= 1 ? raw * 100 : raw;
                        const passed = pct >= 75;
                        return (
                          <tr
                            key={run.run_id ?? run.filename}
                            className="border-b border-b-line-soft transition-colors hover:bg-b-bg2"
                          >
                            <td className="truncate px-3 py-2 text-b-text">
                              {run.workflow_name}
                            </td>
                            <td className="px-3 py-2 text-right tabular-nums text-b-text">
                              {pct.toFixed(1)}
                            </td>
                            <td className="px-3 py-2">
                              <BAsciiBar
                                value={Math.max(0, Math.min(1, pct / 100))}
                                width={20}
                                color={
                                  pct >= 75
                                    ? "b-green"
                                    : pct >= 50
                                      ? "b-amber"
                                      : "b-red"
                                }
                              />
                            </td>
                            <td className="px-3 py-2 text-b-text-mid">
                              {run.evaluation_grade || "—"}
                            </td>
                            <td className="px-3 py-2">
                              <BPill tone={passed ? "ok" : "err"}>
                                {passed ? "pass" : "fail"}
                              </BPill>
                            </td>
                            <td className="px-3 py-2 text-b-text-dim">
                              {run.start_time
                                ? new Date(run.start_time).toLocaleString(
                                    undefined,
                                    {
                                      month: "short",
                                      day: "numeric",
                                      hour: "numeric",
                                      minute: "2-digit",
                                    },
                                  )
                                : "—"}
                            </td>
                            <td className="px-3 py-2 text-right">
                              <Link
                                to={`/runs/${run.filename}`}
                                className="font-semibold text-b-clay hover:underline"
                              >
                                [↗]
                              </Link>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </BBox>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
