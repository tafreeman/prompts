import { useMemo, useCallback, useEffect, useRef } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  type NodeTypes,

  MarkerType,
  BackgroundVariant,
  useReactFlow,
  ReactFlowProvider,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import StepNode, { type StepNodeData } from "./StepNode";
import { layoutDAG } from "./dagLayout";
import type { DAGNode, DAGEdge, StepStatus } from "../../api/types";

const nodeTypes: NodeTypes = {
  step: StepNode,
};

interface StepLiveState {
  status: StepStatus;
  startTime?: string;
  durationMs?: number;
  modelUsed?: string;
  tokensUsed?: number;
  modelInferred?: boolean;
}

interface Props {
  dagNodes: DAGNode[];
  dagEdges: DAGEdge[];
  /** Live state overrides per step name. */
  stepStates?: Map<string, StepLiveState>;
  /** Optional traversal counts keyed by "source->target". */
  edgeCounts?: Map<string, number>;
  /** Optional set of kickback/rework edges keyed by "source->target". */
  kickbackEdges?: Set<string>;
  /** Callback when a node is clicked. */
  onNodeClick?: (stepName: string) => void;
  className?: string;
}

/* ── Inner component (has access to useReactFlow) ── */
function WorkflowDAGInner({
  dagNodes,
  dagEdges,
  stepStates,
  edgeCounts,
  kickbackEdges,
  onNodeClick,
  className = "",
}: Readonly<Props>) {
  const { fitView, setCenter } = useReactFlow();
  const prevRunningRef = useRef<string | null>(null);
  const userInteractedRef = useRef(false);
  const interactionTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const positions = useMemo(
    () => layoutDAG(dagNodes, dagEdges),
    [dagNodes, dagEdges]
  );

  // Find the currently-running step
  const runningStepId = useMemo(() => {
    if (!stepStates) return null;
    for (const [id, state] of stepStates) {
      if (state.status === "running") return id;
    }
    return null;
  }, [stepStates]);

  // Auto-pan to the running node when it changes
  useEffect(() => {
    if (!runningStepId || runningStepId === prevRunningRef.current) return;
    if (userInteractedRef.current) return; // respect manual navigation

    prevRunningRef.current = runningStepId;
    const pos = positions.find((p) => p.id === runningStepId);
    if (!pos) return;

    // Center on the running node with a smooth animation
    setCenter(pos.x + 120, pos.y + 60, { zoom: 1.1, duration: 700 });
  }, [runningStepId, positions, setCenter]);

  // When workflow completes (no running step and we had one before), zoom to fit all
  const allDone = useMemo(() => {
    if (!stepStates || stepStates.size === 0) return false;
    for (const [, state] of stepStates) {
      if (state.status === "running" || state.status === "pending") return false;
    }
    return true;
  }, [stepStates]);

  useEffect(() => {
    if (allDone && prevRunningRef.current) {
      prevRunningRef.current = null;
      userInteractedRef.current = false;
      fitView({ padding: 0.15, duration: 800 });
    }
  }, [allDone, fitView]);

  // Track user interaction — pause auto-pan for 8s after manual move
  const handleMoveEnd = useCallback(() => {
    userInteractedRef.current = true;
    if (interactionTimerRef.current) clearTimeout(interactionTimerRef.current);
    interactionTimerRef.current = setTimeout(() => {
      userInteractedRef.current = false;
    }, 8000);
  }, []);

  // Clear any pending interaction timeout on unmount
  useEffect(() => {
    return () => {
      if (interactionTimerRef.current) {
        clearTimeout(interactionTimerRef.current);
        interactionTimerRef.current = null;
      }
    };
  }, []);

  const nodes = useMemo(() => {
    return dagNodes.map((dn) => {
      const pos = positions.find((p) => p.id === dn.id);
      const live = stepStates?.get(dn.id);

      const data: StepNodeData = {
        label: dn.id,
        agent: dn.agent,
        description: dn.description,
        tier: dn.tier,
        status: live?.status ?? "pending",
        startTime: live?.startTime,
        durationMs: live?.durationMs,
        modelUsed: live?.modelUsed,
        tokensUsed: live?.tokensUsed,
        modelInferred: live?.modelInferred,
      };

      return {
        id: dn.id,
        type: "step" as const,
        position: { x: pos?.x ?? 0, y: pos?.y ?? 0 },
        data: data as unknown as Record<string, unknown>,
      };
    });
  }, [dagNodes, positions, stepStates]);

  const edges: Edge[] = useMemo(() => {
    return dagEdges.map((de) => {
      const edgeId = `${de.source}->${de.target}`;
      const sourceState = stepStates?.get(de.source);
      const targetState = stepStates?.get(de.target);
      const traversalCount = edgeCounts?.get(edgeId) ?? 0;
      const isKickback = kickbackEdges?.has(edgeId) ?? false;

      let strokeColor = "#374151"; // gray-700
      let animated = false;

      if (isKickback && traversalCount > 0) {
        strokeColor = "#a855f7"; // violet
      } else if (sourceState?.status === "success" && targetState?.status === "running") {
        strokeColor = "#3b82f6"; // blue
        animated = true;
      } else if (sourceState?.status === "success") {
        strokeColor = "#22c55e40"; // green/faint
      } else if (sourceState?.status === "failed") {
        strokeColor = "#ef444440"; // red/faint
      }

      return {
        id: edgeId,
        source: de.source,
        target: de.target,
        animated,
        label: traversalCount > 0 ? String(traversalCount) : undefined,
        labelStyle: {
          fill: isKickback ? "#e9d5ff" : "#d1d5db",
          fontSize: 11,
          fontWeight: 600,
        },
        labelBgStyle: {
          fill: isKickback ? "rgba(88, 28, 135, 0.75)" : "rgba(17, 24, 39, 0.75)",
          fillOpacity: 1,
        },
        labelBgPadding: [6, 2],
        labelBgBorderRadius: 4,
        style: { stroke: strokeColor, strokeWidth: 2 },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: strokeColor,
          width: 16,
          height: 16,
        },
      };
    });
  }, [dagEdges, edgeCounts, kickbackEdges, stepStates]);

  const handleNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      onNodeClick?.(node.id);
    },
    [onNodeClick]
  );

  return (
    <div className={`h-full w-full ${className}`}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={handleNodeClick}
        onMoveEnd={handleMoveEnd}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        proOptions={{ hideAttribution: true }}
        minZoom={0.2}
        maxZoom={2.0}
      >
        <Background variant={BackgroundVariant.Dots} gap={20} size={1} color="#1f1f2e" />
        <Controls showInteractive={false} className="dag-controls" />
        <MiniMap
          nodeColor={(node) => {
            const status = (node.data as unknown as StepNodeData | undefined)?.status;
            switch (status) {
              case "running": return "#3b82f6";
              case "success": return "#22c55e";
              case "failed":  return "#ef4444";
              case "skipped": return "#f59e0b";
              default:        return "#374151";
            }
          }}
          maskColor="rgba(0, 0, 0, 0.7)"
          pannable
          zoomable
        />
      </ReactFlow>
    </div>
  );
}

/* ── Wrapper providing ReactFlowProvider ── */
export default function WorkflowDAG(props: Readonly<Props>) {
  return (
    <ReactFlowProvider>
      <WorkflowDAGInner {...props} />
    </ReactFlowProvider>
  );
}
