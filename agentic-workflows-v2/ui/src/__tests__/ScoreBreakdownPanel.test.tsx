import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ScoreBreakdownPanel from "../components/runs/ScoreBreakdownPanel";
import type { EvaluationResult } from "../api/types";

describe("ScoreBreakdownPanel", () => {
  it("renders criteria and failure sections", () => {
    const evaluation: EvaluationResult = {
      enabled: true,
      rubric: "workflow_default",
      criteria: [
        { criterion: "correctness", score: 0.8, weight: 0.6, max_score: 1.0 },
      ],
      overall_score: 80,
      weighted_score: 82,
      grade: "B",
      passed: false,
      pass_threshold: 85,
      generated_at: "2026-02-09T00:00:00Z",
      hard_gate_failures: ["required_outputs_present"],
      floor_violations: [{ criterion: "validation", floor: 0.8, normalized_score: 0.6 }],
    };

    render(<ScoreBreakdownPanel evaluation={evaluation} />);

    expect(screen.getByText("Score Breakdown")).toBeInTheDocument();
    expect(screen.getByText("correctness")).toBeInTheDocument();
    expect(screen.getByText("Hard Gate Failures")).toBeInTheDocument();
    expect(screen.getByText("required_outputs_present")).toBeInTheDocument();
    expect(screen.getByText("Floor Violations")).toBeInTheDocument();
  });
});
