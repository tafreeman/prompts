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
}

const statusConfig: Record<
  StepStatus,
  { border: string; icon: typeof Clock; iconClass: string }
> = {
  pending: {
    border: "border-gray-700/50",
    icon: Clock,
    iconClass: "text-gray-600",
  },
  running: {
    border: "border-blue-500 shadow-blue-500/25 shadow-lg",
    icon: Loader2,
    iconClass: "text-blue-400 animate-spin",
  },
  success: {
    border: "border-green-500/50",
    icon: CheckCircle2,
    iconClass: "text-green-400",
  },
  failed: {
    border: "border-red-500/50",
    icon: XCircle,
    iconClass: "text-red-400",
  },
  skipped: {
    border: "border-amber-500/30",
    icon: SkipForward,
    iconClass: "text-amber-400/70",
  },
  cancelled: {
    border: "border-gray-700/50",
    icon: Clock,
    iconClass: "text-gray-600",
  },
};

function StepNodeComponent({ data }: NodeProps) {
  const nodeData = data as unknown as StepNodeData;
  const cfg = statusConfig[nodeData.status] ?? statusConfig.pending;
  const Icon = cfg.icon;

  let bgClass = "bg-surface-2";
  if (nodeData.status === "pending") bgClass = "bg-surface-1/60";

  return (
    <>
      <Handle type="target" position={Position.Top} className="!bg-gray-600 !border-0 !w-2 !h-2" />

      <div
        className={`
          rounded-lg border ${cfg.border} ${bgClass}
          px-3 py-2.5 min-w-[180px] max-w-[240px]
          transition-all duration-500 ease-out
          ${nodeData.status === "running" ? "ring-1 ring-blue-500/20" : ""}
        `}
      >
        {/* Header: status icon + name */}
        <div className="flex items-center gap-1.5">
          <Icon className={`h-3.5 w-3.5 flex-shrink-0 ${cfg.iconClass} transition-colors duration-300`} />
          <span className="truncate text-xs font-medium text-gray-200">
            {nodeData.label}
          </span>
        </div>

        {/* Agent name */}
        {nodeData.agent && (
          <div className="mt-0.5 truncate text-[10px] text-gray-600">{nodeData.agent}</div>
        )}

        {/* Metrics row — only show when there's data */}
        {(nodeData.status === "running" || nodeData.durationMs != null || nodeData.tokensUsed != null) && (
          <div className="mt-1.5 flex items-center gap-2 text-[10px] text-gray-500">
            <StepTimer
              status={nodeData.status}
              startTime={nodeData.startTime}
              durationMs={nodeData.durationMs}
            />
            {nodeData.tokensUsed != null && (
              <span className="flex items-center gap-0.5">
                <Cpu className="h-2.5 w-2.5" />
                {nodeData.tokensUsed.toLocaleString()}
              </span>
            )}
          </div>
        )}

        {/* Model + tier — compact single line */}
        {(nodeData.modelUsed || nodeData.tier) && (
          <div className="mt-1 flex items-center gap-1.5">
            {nodeData.modelUsed && (
              <span className="truncate text-[10px] text-gray-600">
                {nodeData.modelUsed}
              </span>
            )}
            {nodeData.tier && (
              <span className="rounded bg-white/5 px-1 py-px text-[9px] text-gray-600 uppercase flex-shrink-0">
                {nodeData.tier}
              </span>
            )}
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-gray-600 !border-0 !w-2 !h-2" />
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
    <span className="flex items-center gap-0.5 tabular-nums">
      <Timer className="h-2.5 w-2.5" />
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
