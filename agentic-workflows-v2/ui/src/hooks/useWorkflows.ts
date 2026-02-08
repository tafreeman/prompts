import { useQuery } from "@tanstack/react-query";
import { listWorkflows, getWorkflowDAG } from "../api/client";

export function useWorkflows() {
  return useQuery({
    queryKey: ["workflows"],
    queryFn: () => listWorkflows().then((r) => r.workflows),
  });
}

export function useWorkflowDAG(name: string | undefined) {
  return useQuery({
    queryKey: ["workflow-dag", name],
    queryFn: () => getWorkflowDAG(name!),
    enabled: !!name,
  });
}
