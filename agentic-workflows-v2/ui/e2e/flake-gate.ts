import { readFileSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';
import { resolve } from 'path';

interface FlakeRecord {
  timestamp: string;
  fails: number;
  total: number;
  rate: number;
}

interface FlakeFile {
  version?: number;
  records: FlakeRecord[];
}

function resolveFlakePath(relative = 'agentic-workflows-v2/tests/slo/flake-rate.json'): string {
  const repoRoot = execSync('git rev-parse --show-toplevel').toString().trim();
  return resolve(repoRoot, relative);
}

const TOTAL = 50;
const BUDGET = 0.005;
const ROLLING_DAYS = 7;
const MAX_RECORDS = 30;

function main(): void {
  const fails = Number(process.argv[2] ?? 0);
  const filePath = resolveFlakePath();

  const data: FlakeFile = JSON.parse(readFileSync(filePath, { encoding: 'utf8' }));
  if (!Array.isArray(data.records)) {
    data.records = [];
  }

  data.records.push({
    timestamp: new Date().toISOString(),
    fails,
    total: TOTAL,
    rate: fails / TOTAL,
  });
  if (data.records.length > MAX_RECORDS) {
    data.records.splice(0, data.records.length - MAX_RECORDS);
  }
  writeFileSync(filePath, JSON.stringify(data, null, 2), { encoding: 'utf8' });

  const cutoff = Date.now() - ROLLING_DAYS * 86400 * 1000;
  const recent = data.records.filter((r) => Date.parse(r.timestamp) >= cutoff);
  const totalFails = recent.reduce((s, r) => s + r.fails, 0);
  const totalRuns = recent.reduce((s, r) => s + r.total, 0);
  const rate = totalRuns === 0 ? 0 : totalFails / totalRuns;

  console.log(
    `Rolling ${ROLLING_DAYS}d flake rate: ${(rate * 100).toFixed(2)}% (${totalFails}/${totalRuns})`,
  );
  if (rate > BUDGET) {
    console.error(`FAIL: rate ${(rate * 100).toFixed(2)}% > ${(BUDGET * 100).toFixed(1)}% budget`);
    process.exit(1);
  }
}

main();
