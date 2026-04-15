import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import RunConfigForm from "../components/runs/RunConfigForm";
import type { WorkflowInputSchema } from "../api/types";

vi.mock("../api/client", () => ({
  listEvaluationDatasets: vi.fn().mockResolvedValue({
    repository: [
      {
        id: "repo-dataset",
        name: "Repository Dataset",
        source: "repository",
        description: "A mocked repository dataset",
        sample_count: 3,
      },
    ],
    local: [
      {
        id: "local-dataset",
        name: "Local Dataset",
        source: "local",
        description: "A mocked local dataset",
        sample_count: 2,
      },
    ],
    eval_sets: [
      {
        id: "quick_test",
        name: "Quick Test",
        description: "Displayed elsewhere",
        datasets: ["repo-dataset"],
      },
    ],
  }),
  previewDatasetInputs: vi.fn().mockResolvedValue({
    compatible: true,
    reasons: [],
    adapted_inputs: { prompt: "prefilled" },
    dataset_meta: {},
  }),
}));

/** Helper to build a minimal input schema. */
function makeInput(
  overrides: Partial<WorkflowInputSchema> & { name: string }
): WorkflowInputSchema {
  return {
    type: "string",
    description: "",
    default: null,
    required: true,
    enum: null,
    ...overrides,
  };
}

async function renderForm(
  inputs: WorkflowInputSchema[],
  onChange = vi.fn(),
  workflowName = "test"
) {
  render(<RunConfigForm inputs={inputs} workflowName={workflowName} onChange={onChange} />);
  await waitFor(() => {
    expect(onChange).toHaveBeenCalled();
  });
  return { onChange };
}

describe("RunConfigForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the correct number of input fields from schema", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "repo_url", description: "GitHub repository URL" }),
      makeInput({ name: "issue_text", description: "Issue description" }),
    ];

    await renderForm(inputs);

    // Both fields should be rendered
    expect(screen.getByTestId("input-repo_url")).toBeInTheDocument();
    expect(screen.getByTestId("input-issue_text")).toBeInTheDocument();

    // Verify the containing grid exists
    expect(screen.getByTestId("workflow-inputs")).toBeInTheDocument();
  });

  it("renders a select dropdown for enum inputs", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({
        name: "language",
        enum: ["python", "typescript", "go"],
        description: "Programming language",
      }),
    ];
    await renderForm(inputs);

    const select = screen.getByTestId("input-language") as HTMLSelectElement;
    expect(select.tagName).toBe("SELECT");

    // Enum options should be present
    const options = select.querySelectorAll("option");
    const optionValues = Array.from(options).map((o) => o.value);
    expect(optionValues).toContain("python");
    expect(optionValues).toContain("typescript");
    expect(optionValues).toContain("go");
  });

  it("does not mark optional fields as required", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "optional_field", required: false }),
      makeInput({ name: "required_field", required: true }),
    ];
    await renderForm(inputs);

    const optionalInput = screen.getByTestId(
      "input-optional_field"
    ) as HTMLInputElement;
    const requiredInput = screen.getByTestId(
      "input-required_field"
    ) as HTMLInputElement;

    expect(optionalInput.required).toBe(false);
    expect(requiredInput.required).toBe(true);
  });

  it("populates default values from schema", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "model", default: "gpt-4o" }),
    ];
    await renderForm(inputs);

    const input = screen.getByTestId("input-model") as HTMLInputElement;
    expect(input.value).toBe("gpt-4o");
  });

  it("shows advanced runtime panel with rubric and runtime options when toggled", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "task" }),
    ];
    await renderForm(inputs);

    // Advanced panel should not be visible initially
    expect(screen.queryByTestId("rubric-config")).not.toBeInTheDocument();
    expect(screen.queryByTestId("runtime-config")).not.toBeInTheDocument();

    expect(screen.getByTestId("evaluation-config")).toBeInTheDocument();
    expect(screen.getByText(/score this run against a workflow-compatible dataset/i)).toBeInTheDocument();

    // Click toggle
    fireEvent.click(screen.getByTestId("advanced-toggle"));

    // Now both config sections should be visible
    expect(screen.getByTestId("rubric-config")).toBeInTheDocument();
    expect(screen.getByTestId("runtime-config")).toBeInTheDocument();
  });

  it("calls onChange with execution profile and rubric values", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "prompt", default: "hello" }),
    ];
    const { onChange } = await renderForm(inputs);

    // The form should emit onChange on initial render with defaults
    expect(onChange).toHaveBeenCalled();

    const lastCall = onChange.mock.calls.at(-1)?.[0];
    expect(lastCall).toBeDefined();
    expect(lastCall!.inputValues).toHaveProperty("prompt", "hello");
    expect(lastCall!.executionProfile).toHaveProperty("runtime", "subprocess");
    expect(lastCall!.rubricId).toBe("");
  });

  it("renders textarea for object-type inputs", async () => {
    const inputs: WorkflowInputSchema[] = [
      makeInput({ name: "config", type: "object", description: "JSON config" }),
    ];
    await renderForm(inputs);

    const textarea = screen.getByTestId("input-config") as HTMLTextAreaElement;
    expect(textarea.tagName).toBe("TEXTAREA");
  });

  it("renders no input grid when inputs array is empty", async () => {
    await renderForm([]);

    expect(screen.queryByTestId("workflow-inputs")).not.toBeInTheDocument();
    // Form wrapper should still exist
    expect(screen.getByTestId("run-config-form")).toBeInTheDocument();
  });

  it("loads workflow-specific datasets and does not offer eval-set execution", async () => {
    const inputs: WorkflowInputSchema[] = [makeInput({ name: "prompt", required: false })];
    await renderForm(inputs, vi.fn(), "code_review");

    fireEvent.click(screen.getByLabelText(/enable evaluation/i));

    const sourceSelect = screen.getByRole("combobox", { name: /source/i });
    fireEvent.change(sourceSelect, { target: { value: "repository" } });

    await waitFor(() => {
      expect(screen.getByRole("option", { name: /repository dataset/i })).toBeInTheDocument();
    });

    expect(screen.queryByRole("option", { name: /quick test/i })).not.toBeInTheDocument();
  });
});
