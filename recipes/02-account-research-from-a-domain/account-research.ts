// PAID. Company record, tech stack and known emails for one domain, in parallel.
// Usage: LOOOT_TOKEN=... node account-research.ts example.com
import { Looot } from "looot-js";

const domain = process.argv[2];
if (!domain) throw new Error("usage: node account-research.ts <domain>");

const looot = new Looot();
const day = new Date().toISOString().slice(0, 10);
const key = (step: string) => `cookbook-account-${step}-${domain}-${day}`;

const [company, stack, people] = await Promise.all([
  looot.runJob({ job: "company.enrich", input: { domain }, prefer: "cheapest", wait: 45, idempotencyKey: key("company") }),
  looot.run({ endpointId: "tomba-technology", input: { domain }, wait: 45, idempotencyKey: key("stack") }),
  looot.runJob({ job: "people.domain.search", input: { domain }, prefer: "cheapest", wait: 45, idempotencyKey: key("people") }),
]);

for (const [label, run] of [["Company", company], ["Tech stack", stack], ["People", people]] as const) {
  console.log(`\n## ${label}: ${run.status}, ${run.outcome ?? ""}, served by ${run.route?.servedBy ?? run.endpointId}, $${run.actualCost ?? 0}`);
  console.log(JSON.stringify(run.status === "completed" ? run.result : run.error, null, 2).slice(0, 4000));
}
