import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import WorkflowsPage from "../pages/WorkflowsPage";

const mockUseWorkflows = vi.fn();

vi.mock("../hooks/useWorkflows", () => ({
  useWorkflows: () => mockUseWorkflows(),
}));

describe("WorkflowsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders loading placeholders", () => {
    mockUseWorkflows.mockReturnValue({ data: undefined, isLoading: true });

    const { container } = render(
      <MemoryRouter>
        <WorkflowsPage />
      </MemoryRouter>
    );

    expect(container.querySelectorAll(".animate-pulse")).toHaveLength(3);
  });

  it("filters workflows by search query", () => {
    mockUseWorkflows.mockReturnValue({
      data: ["code_review", "triage_workflow"],
      isLoading: false,
    });

    render(
      <MemoryRouter>
        <WorkflowsPage />
      </MemoryRouter>
    );

    expect(screen.getByText("code_review")).toBeInTheDocument();
    expect(screen.getByText("triage_workflow")).toBeInTheDocument();

    fireEvent.change(screen.getByPlaceholderText("Search workflows..."), {
      target: { value: "triage" },
    });

    expect(screen.queryByText("code_review")).not.toBeInTheDocument();
    expect(screen.getByText("triage_workflow")).toBeInTheDocument();
  });

  it("shows the empty search state", () => {
    mockUseWorkflows.mockReturnValue({
      data: ["code_review"],
      isLoading: false,
    });

    render(
      <MemoryRouter>
        <WorkflowsPage />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Search workflows..."), {
      target: { value: "missing" },
    });

    expect(screen.getByText('No workflows found matching "missing".')).toBeInTheDocument();
  });
});
