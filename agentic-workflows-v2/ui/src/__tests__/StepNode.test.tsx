import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ReactFlowProvider, type NodeProps } from "@xyflow/react";
import StepNode, { type StepNodeData } from "../components/dag/StepNode";
import type { StepStatus } from "../api/types";

/** Minimal wrapper that mounts StepNode inside the ReactFlow context. */
function renderStepNode(
  data: Partial<StepNodeData> & { disconnected?: boolean },
  id = "step-a",
) {
  const fullData: StepNodeData & { disconnected?: boolean } = {
    label: data.label ?? id,
    agent: data.agent ?? null,
    description: data.description ?? "",
    tier: data.tier ?? null,
    status: (data.status ?? "pending") as StepStatus,
    startTime: data.startTime,
    durationMs: data.durationMs,
    modelUsed: data.modelUsed,
    tokensUsed: data.tokensUsed,
    modelInferred: data.modelInferred,
    error: data.error ?? null,
    disconnected: data.disconnected,
  };
  const props = {
    id,
    type: "step",
    data: fullData as unknown as Record<string, unknown>,
    selected: false,
    dragging: false,
    draggable: true,
    selectable: true,
    deletable: true,
    zIndex: 0,
    isConnectable: false,
    positionAbsoluteX: 0,
    positionAbsoluteY: 0,
  } as unknown as NodeProps;
  return render(
    <ReactFlowProvider>
      <StepNode {...props} />
    </ReactFlowProvider>,
  );
}

describe("StepNode — live animation (Story 2.5)", () => {
  it("applies clay glow class when running", () => {
    const { container } = renderStepNode({ status: "running" });
    expect(container.querySelector(".step-node--running")).not.toBeNull();
  });

  it("removes glow class when succeeded", () => {
    const { container } = renderStepNode({ status: "success" });
    expect(container.querySelector(".step-node--running")).toBeNull();
  });

  it("removes glow class when disconnected (animation paused)", () => {
    const { container } = renderStepNode({
      status: "running",
      disconnected: true,
    });
    expect(container.querySelector(".step-node--running")).toBeNull();
  });

  it("preserves data-testid on the root element across states", () => {
    const { container } = renderStepNode({ status: "running" }, "parse_code");
    expect(
      container.querySelector('[data-testid="dag-node-parse_code"]'),
    ).not.toBeNull();
  });
});
