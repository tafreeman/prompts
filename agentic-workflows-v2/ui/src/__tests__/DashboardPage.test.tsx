import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DashboardPage from "../pages/DashboardPage";

const mockUseRunsSummary = vi.fn();
const mockUseRuns = vi.fn();
const mockUseWorkflows = vi.fn();

vi.mock("../hooks/useRuns", () => ({
  useRunsSummary: () => mockUseRunsSummary(),
  useRuns: () => mockUseRuns(),
}));

vi.mock("../hooks/useWorkflows", () => ({
  useWorkflows: () => mockUseWorkflows(),
}));

vi.mock("../components/runs/RunSummaryCards", () => ({
  default: ({ summary }: { summary: { total_runs?: number } | undefined }) => (
    <div>Summary {summary?.total_runs ?? 0}</div>
  ),
}));

vi.mock("../components/runs/RunList", () => ({
  default: ({ runs }: { runs?: Array<{ workflow_name: string | null }> }) => (
    <div>Run List {runs?.length ?? 0}</div>
  ),
}));

describe("DashboardPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders available workflows and recent runs", () => {
    mockUseRunsSummary.mockReturnValue({ data: { total_runs: 2 }, isLoading: false });
    mockUseRuns.mockReturnValue({
      data: [{ workflow_name: "triage" }, { workflow_name: "review" }],
      isLoading: false,
    });
    mockUseWorkflows.mockReturnValue({ data: ["triage", "review"] });

    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>
    );

    expect(screen.getByText("Summary 2")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /triage/i })).toHaveAttribute("href", "/workflows/triage");
    expect(screen.getByRole("link", { name: /review/i })).toHaveAttribute("href", "/workflows/review");
    expect(screen.getByText("Run List 2")).toBeInTheDocument();
  });

  it("renders the empty state when there are no runs", () => {
    mockUseRunsSummary.mockReturnValue({ data: { total_runs: 0 }, isLoading: false });
    mockUseRuns.mockReturnValue({ data: [], isLoading: false });
    mockUseWorkflows.mockReturnValue({ data: ["triage"] });

    render(
      <MemoryRouter>
        <DashboardPage />
      </MemoryRouter>
    );

    expect(screen.getByText("No runs yet")).toBeInTheDocument();
    expect(screen.queryByText("Run List 0")).not.toBeInTheDocument();
  });
});
