// PAID. Fetch a page as markdown through the cheapest provider, falling back on a miss.
// Usage: LOOOT_TOKEN=... node page-to-markdown.ts https://www.example.com > page.md
import { Looot } from "looot-js";

const url = process.argv[2];
if (!url) throw new Error("usage: node page-to-markdown.ts <url>");

const run = await new Looot().runJob({
  job: "web.scrape.markdown",
  input: { url },
  prefer: "cheapest",
  fallback: { maxAttempts: 3, maxCostUsd: 0.02 },
  wait: 60,
});

if (run.status !== "completed") {
  console.error(run.status, run.error);
  process.exit(1);
}
console.error(`served by ${run.route?.servedBy ?? run.endpointId}, $${run.actualCost}`);
// Providers differ: some return markdown as a string, some wrap it. Print strings as-is.
const r = run.result as unknown;
process.stdout.write(typeof r === "string" ? r : JSON.stringify(r, null, 2));
