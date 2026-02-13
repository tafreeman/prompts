import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import IterationTimeline from "../components/runs/IterationTimeline";

describe("IterationTimeline", () => {
  it("test_empty_attempts_returns_null", () => {
    const { container } = render(<IterationTimeline attempts={[]} />);
    expect(container.firstChild).toBeNull();
  });

  it("test_timeline_renders_attempts", () => {
    const attempts = [
      { attempt_number: 1, status: "failed", duration_ms: 1200, failed_steps: ["a"] },
      { attempt_number: 2, status: "failed", duration_ms: 900, failed_steps: ["b"] },
      { attempt_number: 3, status: "success", duration_ms: 700, failed_steps: [] },
    ];

    render(<IterationTimeline attempts={attempts} />);

    const nodes = screen.getAllByTestId("iteration-node");
    expect(nodes).toHaveLength(3);
    expect(screen.getByText("Attempt 1")).toBeInTheDocument();
    expect(screen.getByText("Attempt 2")).toBeInTheDocument();
    expect(screen.getByText("Attempt 3")).toBeInTheDocument();
  });

  it("test_timeline_final_highlighted", () => {
    const attempts = [
      { attempt_number: 1, status: "failed", duration_ms: 1200, failed_steps: ["a"] },
      { attempt_number: 2, status: "success", duration_ms: 600, failed_steps: [] },
    ];

    render(<IterationTimeline attempts={attempts} />);

    const nodes = screen.getAllByTestId("iteration-node");
    const lastNode = nodes[nodes.length - 1];
    expect(lastNode).toBeDefined();
    expect(lastNode!.className).toContain("ring-2");
    expect(lastNode!.className).toContain("ring-blue-500");
  });

  it("test_timeline_status_colors", () => {
    const attempts = [
      { attempt_number: 1, status: "failed", duration_ms: 500, failed_steps: ["a"] },
      { attempt_number: 2, status: "success", duration_ms: 300, failed_steps: [] },
    ];

    render(<IterationTimeline attempts={attempts} />);

    const failedBadge = screen.getByText("failed");
    const successBadge = screen.getByText("success");
    expect(failedBadge.className).toContain("bg-red-500/20");
    expect(successBadge.className).toContain("bg-green-500/20");
  });
});
