import {
  CheckCircle2,
  XCircle,
  Clock,
  Loader2,
  SkipForward,
  Ban,
} from "lucide-react";
import type { StepStatus } from "../../api/types";

const config: Record<
  StepStatus,
  { color: string; bg: string; icon: typeof Clock; label: string }
> = {
  pending: {
    color: "text-gray-400",
    bg: "bg-gray-400/10",
    icon: Clock,
    label: "Pending",
  },
  running: {
    color: "text-blue-400",
    bg: "bg-blue-400/10",
    icon: Loader2,
    label: "Running",
  },
  success: {
    color: "text-green-400",
    bg: "bg-green-400/10",
    icon: CheckCircle2,
    label: "Success",
  },
  failed: {
    color: "text-red-400",
    bg: "bg-red-400/10",
    icon: XCircle,
    label: "Failed",
  },
  skipped: {
    color: "text-amber-400",
    bg: "bg-amber-400/10",
    icon: SkipForward,
    label: "Skipped",
  },
  cancelled: {
    color: "text-gray-500",
    bg: "bg-gray-500/10",
    icon: Ban,
    label: "Cancelled",
  },
};

interface Props {
  status: StepStatus | string;
  size?: "sm" | "md";
}

export default function StatusBadge({ status, size = "sm" }: Props) {
  const cfg = config[status as StepStatus] ?? config.pending;
  const Icon = cfg.icon;
  const sizeClass = size === "sm" ? "text-xs px-2 py-0.5" : "text-sm px-3 py-1";

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full font-medium ${cfg.bg} ${cfg.color} ${sizeClass}`}
    >
      <Icon
        className={`${size === "sm" ? "h-3 w-3" : "h-4 w-4"} ${status === "running" ? "animate-spin" : ""}`}
      />
      {cfg.label}
    </span>
  );
}
