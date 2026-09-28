// Free. Balance, recent runs, and one run's route and attempts.
// Usage: LOOOT_TOKEN=... node receipts.ts [runId]
import { Looot } from "looot-js";

const looot = new Looot();
const runId = process.argv[2];

const b = await looot.balance();
console.log(`balance: $${b.available} available, $${b.reserved} held by runs in flight`);

if (!runId) {
  const { runs = [] } = await looot.listRuns({ limit: 10 });
  for (const r of runs) {
    console.log(`${r.runId}  ${String(r.status).padEnd(10)} ${String(r.endpointId).padEnd(40)} $${r.actualCost ?? "-"}`);
  }
  process.exit(0);
}

const run = await looot.getRun(runId);
console.log(`${run.runId}: ${run.status}, outcome ${run.outcome ?? "-"}, paid $${run.actualCost ?? 0}`);
if (run.error) console.log("error:", run.error.code, run.error.whoseError, run.error.message);
if (run.route) {
  console.log(`route: served by ${run.route.servedBy ?? "nobody"}, total $${run.route.chargedUsd}, capped ${run.route.capped}`);
  for (const a of run.route.attempts ?? []) {
    console.log(`  #${a.n} ${a.endpointId} ${a.outcome} $${a.chargedUsd} ${a.ms} ms ${a.reason ?? ""}`);
  }
  for (const s of run.route.skipped ?? []) console.log(`  skipped ${s.endpointId}: ${s.code} ${s.reason}`);
}
const { attempts } = await looot.runAttempts(runId);
for (const a of attempts) console.log("attempt:", JSON.stringify(a));
