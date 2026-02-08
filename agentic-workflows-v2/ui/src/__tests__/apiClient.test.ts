import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  getWorkflowDAG,
  listEvaluationDatasets,
  listRuns,
  listWorkflows,
} from "../api/client";

describe("API client", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("listWorkflows fetches /api/workflows", async () => {
    const mockResponse = { workflows: ["code_review", "fullstack_generation"] };
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    } as Response);

    const result = await listWorkflows();
    expect(result.workflows).toEqual(["code_review", "fullstack_generation"]);
    expect(fetch).toHaveBeenCalledWith("/api/workflows", undefined);
  });

  it("getWorkflowDAG fetches /api/workflows/{name}/dag", async () => {
    const mockDAG = { name: "test", description: "", nodes: [], edges: [] };
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockDAG),
    } as Response);

    const result = await getWorkflowDAG("test");
    expect(result.name).toBe("test");
    expect(fetch).toHaveBeenCalledWith("/api/workflows/test/dag", undefined);
  });

  it("listRuns fetches /api/runs with params", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve([]),
    } as Response);

    await listRuns("code_review", 10);
    const url = (fetch as ReturnType<typeof vi.fn>).mock.calls[0]?.[0] as string;
    expect(url).toContain("workflow=code_review");
    expect(url).toContain("limit=10");
  });

  it("listEvaluationDatasets fetches /api/eval/datasets", async () => {
    const mockResponse = { repository: [], local: [] };
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    } as Response);

    const result = await listEvaluationDatasets();
    expect(result).toEqual(mockResponse);
    expect(fetch).toHaveBeenCalledWith("/api/eval/datasets", undefined);
  });

  it("throws on non-OK response", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue({
      ok: false,
      status: 404,
      text: () => Promise.resolve("Not Found"),
    } as Response);

    await expect(listWorkflows()).rejects.toThrow("API 404");
  });
});
