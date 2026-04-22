import { readFileSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';
import { resolve } from 'path';

/**
 * Resolve the SLO data file path relative to the repo root, so this works
 * whether the caller is running from the ui/ directory (Playwright) or the
 * repo root (CI).
 */
function resolveSloPath(relative = 'agentic-workflows-v2/tests/slo/first-span-latency.json'): string {
  const repoRoot = execSync('git rev-parse --show-toplevel').toString().trim();
  return resolve(repoRoot, relative);
}

export interface LatencyRecord {
  timestamp: string;
  latency_ms: number;
  commit: string;
}

interface LatencyFile {
  version: number;
  max_records: number;
  records: LatencyRecord[];
}

export async function recordLatency(ms: number, pathOverride?: string): Promise<void> {
  const filePath = pathOverride ?? resolveSloPath();
  const data: LatencyFile = JSON.parse(readFileSync(filePath, { encoding: 'utf8' }));
  let commit = '';
  try {
    commit = execSync('git rev-parse HEAD').toString().trim();
  } catch {
    commit = 'unknown';
  }
  data.records.push({
    timestamp: new Date().toISOString(),
    latency_ms: ms,
    commit,
  });
  if (data.records.length > data.max_records) {
    data.records.splice(0, data.records.length - data.max_records);
  }
  writeFileSync(filePath, JSON.stringify(data, null, 2), { encoding: 'utf8' });
}

export async function readP95(
  options: { windowDays: number; pathOverride?: string },
): Promise<number> {
  const filePath = options.pathOverride ?? resolveSloPath();
  const data: LatencyFile = JSON.parse(readFileSync(filePath, { encoding: 'utf8' }));
  const cutoff = Date.now() - options.windowDays * 86400 * 1000;
  const recent = data.records
    .filter((r) => Date.parse(r.timestamp) >= cutoff)
    .map((r) => r.latency_ms)
    .sort((a, b) => a - b);
  if (recent.length === 0) return 0; // no data yet — don't fail
  // Canonical nearest-rank p95: ceil(0.95 * n) - 1. For n=100 yields index 94
  // (the 95th value in 1-based ordering), not index 95 which would be the 96th.
  const idx = Math.max(0, Math.ceil(recent.length * 0.95) - 1);
  return recent[idx] ?? 0;
}
