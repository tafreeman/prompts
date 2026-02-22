import { memo, useEffect, useState } from "react";
import { Handle, Position, type NodeProps } from "@xyflow/react";
import {
  CheckCircle2,
  XCircle,
  Clock,
  Loader2,
  SkipForward,
  Timer,
  Cpu,
  Bot,
  Sparkles,
} from "lucide-react";
import type { StepStatus } from "../../api/types";

export interface StepNodeData {
  label: string;
  agent: string | null;
  description: string;
  tier: string | null;
  status: StepStatus;
  startTime?: string;
  durationMs?: number;
  modelUsed?: string;
  tokensUsed?: number;
  modelInferred?: boolean;
}

const statusConfig: Record<
  StepStatus,
  { border: string; icon: typeof Clock; iconClass: string }
> = {
  pending: {
    border: "border-gray-200",
    icon: Clock,
    iconClass: "text-gray-400",
  },
  running: {
    border: "border-blue-500 shadow-[0_0_15px_rgba(59,130,246,0.15)]",
    icon: Loader2,
    iconClass: "text-blue-500 animate-spin",
  },
  success: {
    border: "border-green-500/40",
    icon: CheckCircle2,
    iconClass: "text-green-500",
  },
  failed: {
    border: "border-red-500/40",
    icon: XCircle,
    iconClass: "text-red-500",
  },
  skipped: {
    border: "border-amber-500/40",
    icon: SkipForward,
    iconClass: "text-amber-500",
  },
  cancelled: {
    border: "border-gray-300",
    icon: Clock,
    iconClass: "text-gray-400",
  },
};

function StepNodeComponent({ data }: NodeProps) {
  const nodeData = data as unknown as StepNodeData;
  const cfg = statusConfig[nodeData.status] ?? statusConfig.pending;
  const Icon = cfg.icon;

  let bgClass = "bg-white shadow-sm";
  if (nodeData.status === "pending") bgClass = "bg-gray-50/80";

  return (
    <>
      <Handle type="target" position={Position.Top} className="!bg-gray-300 !border-white !border-2 !w-3 !h-3" />

      <div
        className={`
          rounded-xl border ${cfg.border} ${bgClass}
          px-4 py-3 min-w-[200px] max-w-[260px]
          transition-all duration-300 ease-out
          ${nodeData.status === "running" ? "ring-1 ring-blue-500/20" : ""}
        `}
      >
        {/* Header: status icon + name */}
        <div className="flex items-center gap-2">
          <Icon className={`h-4 w-4 flex-shrink-0 ${cfg.iconClass} transition-colors duration-300`} />
          <span className="truncate text-sm font-semibold text-gray-800 tracking-tight">
            {nodeData.label}
          </span>
        </div>

        {/* Agent name */}
        {nodeData.agent && (
          <div className="mt-1 truncate text-xs font-medium text-gray-500">{nodeData.agent}</div>
        )}

        {/* Metrics row — only show when there's data */}
        {(nodeData.status === "running" || nodeData.durationMs != null || nodeData.tokensUsed != null) && (
          <div className="mt-3 flex flex-wrap items-center gap-2 text-xs">
            <StepTimer
              status={nodeData.status}
              startTime={nodeData.startTime}
              durationMs={nodeData.durationMs}
            />
            {nodeData.tokensUsed != null && (
              <span className="flex items-center gap-1 rounded-md bg-gray-50 border border-gray-200 px-2 py-0.5 font-medium text-gray-600 shadow-sm">
                <Cpu className="h-3 w-3 text-blue-500/70" />
                {nodeData.tokensUsed.toLocaleString()}
              </span>
            )}
          </div>
        )}

        {/* Model + tier — compact single line */}
        {(nodeData.modelUsed || nodeData.tier) && (
          <div className="mt-2.5 flex flex-wrap items-center gap-2">
            {nodeData.modelUsed && (
              <span
                className={`flex items-center gap-1 truncate text-[11px] px-2 py-0.5 rounded-md border shadow-sm font-medium ${
                  nodeData.modelInferred
                    ? "bg-amber-50 border-amber-200 text-amber-700 border-dashed"
                    : "bg-gray-50 border-gray-200 text-gray-600"
                }`}
                title={nodeData.modelInferred ? "Model inferred from configuration" : "Model explicitly recorded"}
              >
                {nodeData.modelInferred ? (
                  <Sparkles className="h-3 w-3 text-amber-500" />
                ) : (
                  <Bot className="h-3 w-3 text-gray-400" />
                )}
                <span className="truncate max-w-[130px]">{nodeData.modelUsed}</span>
              </span>
            )}
            {nodeData.tier && (
              <span className="rounded-md bg-purple-50 border border-purple-200 px-1.5 py-0.5 text-[10px] text-purple-700 uppercase flex-shrink-0 tracking-wider font-bold shadow-sm">
                {nodeData.tier}
              </span>
            )}
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-gray-300 !border-white !border-2 !w-3 !h-3" />
    </>
  );
}

/* ── StepTimer: live elapsed or final duration ── */
function StepTimer({
  status,
  startTime,
  durationMs,
}: Readonly<{
  status: StepStatus;
  startTime?: string;
  durationMs?: number;
}>) {
  const [elapsed, setElapsed] = useState<number | null>(null);

  useEffect(() => {
    if (status !== "running" || !startTime) {
      setElapsed(null);
      return;
    }
    const origin = new Date(startTime).getTime();
    setElapsed(Date.now() - origin);
    const id = setInterval(() => setElapsed(Date.now() - origin), 250);
    return () => clearInterval(id);
  }, [status, startTime]);

  const ms =
    status === "running" && elapsed != null
      ? elapsed
      : durationMs ?? null;

  if (ms == null) return null;

  return (
    <span className="flex items-center gap-1 rounded-md bg-gray-50 border border-gray-200 px-2 py-0.5 font-medium text-gray-600 shadow-sm tabular-nums">
      <Timer className="h-3 w-3 text-gray-400" />
      {formatMs(ms)}
    </span>
  );
}

function formatMs(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  const totalSec = ms / 1000;
  if (totalSec < 60) return `${totalSec.toFixed(1)}s`;
  const m = Math.floor(totalSec / 60);
  const s = Math.floor(totalSec % 60);
  return `${m}m ${s.toString().padStart(2, "0")}s`;
}

export default memo(StepNodeComponent);
