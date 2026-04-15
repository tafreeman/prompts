import { useEffect } from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import type { RunConfigValues } from "../components/runs/RunConfigForm";
import WorkflowDetailPage from "../pages/WorkflowDetailPage";

const mockNavigate = vi.fn();
const mockRunWorkflow = vi.fn();
const mockRunConfigForm = vi.fn();

vi.mock("../hooks/useWorkflows", () => ({
  useWorkflowDAG: () => ({
    data: {
      name: "code_review",
      description: "Automated code review workflow",
      nodes: [],
      edges: [],
      inputs: [
        {
          name: "code_file",
          type: "string",
          description: "Path to code",
          default: null,
          required: true,
          enum: null,
        },
      ],
    },
    isLoading: false,
  }),
}));

vi.mock("../hooks/useRuns", () => ({
  useRuns: () => ({
    data: [],
    isLoading: false,
  }),
}));

vi.mock("../api/client", () => ({
  runWorkflow: (...args: unknown[]) => mockRunWorkflow(...args),
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual<typeof import("react-router-dom")>(
    "react-router-dom"
  );
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

vi.mock("../components/dag/WorkflowDAG", () => ({
  default: () => <div>DAG</div>,
}));

vi.mock("../components/runs/RunList", () => ({
  default: () => <div>Run List</div>,
}));

vi.mock("../components/runs/RunConfigForm", () => ({
  default: function MockRunConfigForm(props: {
    onChange: (values: RunConfigValues) => void;
  }) {
    const nextValues = mockRunConfigForm(props) as RunConfigValues | undefined;
    useEffect(() => {
      if (nextValues) {
        props.onChange(nextValues);
      }
    }, []);
    return <div>Run Config Form</div>;
  },
}));

function renderPage() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/workflows/code_review"]}>
        <Routes>
          <Route path="/workflows/:name" element={<WorkflowDetailPage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("WorkflowDetailPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockRunWorkflow.mockResolvedValue({ run_id: "run-123", status: "pending" });
  });

  it("updates the CTA to Run + Eval when evaluation is enabled", async () => {
    mockRunConfigForm.mockImplementation(
      () => {
        return {
          inputValues: { code_file: "src/example.py" },
          executionProfile: { runtime: "subprocess" },
          rubricId: "",
          evaluationReadiness: {
            status: "ready",
            message: "Dataset is compatible.",
          },
          evaluation: {
            enabled: true,
            datasetSource: "repository",
            datasetId: "repo-dataset",
            selectedSamples: [0],
            runsPerRecord: 1,
          },
        } satisfies RunConfigValues;
      }
    );

    renderPage();

    expect(
      await screen.findByRole("button", { name: /run \+ eval/i })
    ).toBeInTheDocument();
    expect(screen.getByText(/evaluation ready/i)).toBeInTheDocument();
  });

  it("blocks starting a scored eval until a dataset is selected", async () => {
    mockRunConfigForm.mockImplementation(
      () => {
        return {
          inputValues: { code_file: "src/example.py" },
          executionProfile: { runtime: "subprocess" },
          rubricId: "",
          evaluationReadiness: {
            status: "idle",
            message: "Choose a dataset before starting a scored evaluation.",
          },
          evaluation: {
            enabled: true,
            datasetSource: "repository",
            datasetId: "",
            selectedSamples: [0],
            runsPerRecord: 1,
          },
        } satisfies RunConfigValues;
      }
    );

    renderPage();

    expect(
      await screen.findByText(/choose a dataset before starting a scored evaluation/i)
    ).toBeInTheDocument();

    const button = screen.getByRole("button", { name: /run \+ eval/i });
    expect(button).toBeDisabled();

    fireEvent.click(button);

    await waitFor(() => {
      expect(mockRunWorkflow).not.toHaveBeenCalled();
    });
  });
});
