import { useQuery } from "@tanstack/react-query";
import { listRuns, getRunDetail, getRunsSummary } from "../api/client";

export function useRuns(workflow?: string) {
  return useQuery({
    queryKey: ["runs", workflow],
    queryFn: () => listRuns(workflow),
    refetchInterval: 5000,
  });
}

export function useRunDetail(filename: string | undefined) {
  return useQuery({
    queryKey: ["run", filename],
    queryFn: () => getRunDetail(filename!),
    enabled: !!filename,
  });
}

export function useRunsSummary(workflow?: string) {
  return useQuery({
    queryKey: ["runs-summary", workflow],
    queryFn: () => getRunsSummary(workflow),
  });
}
