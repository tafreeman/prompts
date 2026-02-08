import { memo } from "react";
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
  durationMs?: number;
  modelUsed?: string;
  tokensUsed?: number;
}

const statusConfig: Record<
  StepStatus,
  { border: string; icon: typeof Clock; iconClass: string }
> = {
  pending: {
    border: "border-gray-600",
    icon: Clock,
    iconClass: "text-gray-500",
  },
  running: {
    border: "border-blue-500 shadow-blue-500/20 shadow-lg",
    icon: Loader2,
    iconClass: "text-blue-400 animate-spin",
  },
  success: {
    border: "border-green-500/60",
    icon: CheckCircle2,
    iconClass: "text-green-400",
  },
  failed: {
    border: "border-red-500/60",
    icon: XCircle,
    iconClass: "text-red-400",
  },
  skipped: {
    border: "border-amber-500/40",
    icon: SkipForward,
    iconClass: "text-amber-400",
  },
  cancelled: {
    border: "border-gray-600",
    icon: Clock,
    iconClass: "text-gray-500",
  },
};

function StepNodeComponent({ data }: NodeProps) {
  const nodeData = data as unknown as StepNodeData;
  const cfg = statusConfig[nodeData.status] ?? statusConfig.pending;
  const Icon = cfg.icon;

  const bgClass =
    nodeData.status === "running"
      ? "bg-surface-2 animate-pulse-slow"
      : nodeData.status === "pending"
        ? "bg-surface-1/80"
        : "bg-surface-2";

  return (
    <>
      <Handle type="target" position={Position.Top} className="!bg-gray-600 !border-0 !w-2 !h-2" />

      <div
        className={`rounded-lg border-2 ${cfg.border} ${bgClass} px-4 py-3 min-w-[200px] max-w-[280px] transition-all`}
      >
        {/* Header: status icon + name */}
        <div className="flex items-center gap-2">
          <Icon className={`h-4 w-4 flex-shrink-0 ${cfg.iconClass}`} />
          <span className="truncate text-sm font-medium text-gray-100">
            {nodeData.label}
          </span>
        </div>

        {/* Agent name */}
        {nodeData.agent && (
          <div className="mt-1 text-xs text-gray-500">{nodeData.agent}</div>
        )}

        {/* Metrics row */}
        <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
          {nodeData.durationMs != null && (
            <span className="flex items-center gap-1">
              <Timer className="h-3 w-3" />
              {nodeData.durationMs < 1000
                ? `${Math.round(nodeData.durationMs)}ms`
                : `${(nodeData.durationMs / 1000).toFixed(1)}s`}
            </span>
          )}
          {nodeData.tokensUsed != null && (
            <span className="flex items-center gap-1">
              <Cpu className="h-3 w-3" />
              {nodeData.tokensUsed.toLocaleString()} tok
            </span>
          )}
        </div>

        {/* Model used */}
        {nodeData.modelUsed && (
          <div className="mt-1 truncate text-xs text-gray-600">
            {nodeData.modelUsed}
          </div>
        )}

        {/* Tier badge */}
        {nodeData.tier && (
          <div className="mt-1">
            <span className="rounded bg-white/5 px-1.5 py-0.5 text-[10px] text-gray-500 uppercase">
              {nodeData.tier}
            </span>
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} className="!bg-gray-600 !border-0 !w-2 !h-2" />
    </>
  );
}

export default memo(StepNodeComponent);
