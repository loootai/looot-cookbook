# Reading receipts

Every run carries what it cost and why. This recipe reads it back. Nothing here is paid:
`getRun`, `runAttempts`, `listRuns` and `balance` are free (they need `runs.read` and
`usage.read`).

## Where the money shows

| Field | Where | Meaning |
| --- | --- | --- |
| `estimatedCost` | the run, while queued | the hold placed before the run |
| `actualCost` | the run, once settled | what you paid |
| `route.attempts[]` | a fallback run | each provider tried: `outcome`, `status`, `chargedUsd`, `ms`, `reason` |
| `route.skipped[]` | a fallback run | providers passed over and why (`code`, `reason`) |
| `route.chargedUsd`, `route.capped` | a fallback run | the route total, and whether `maxCostUsd` cut it short |
| attempts list | `GET /v1/runs/{id}/attempts` | each attempt with its receipt and cost |
| `available`, `reserved` | `GET /v1/balance` | money free to spend, money held by runs in flight |

Rules worth knowing, from the public guide (api.looot.ai/llms-full.txt):

- A refusal before admission holds and charges nothing.
- A definitive failure releases the hold and settles at $0 or the provider's evidenced cost.
- An uncertain outcome parks as `reconciliation_pending` and keeps the hold until a person
  settles it.
- With fallback, only attempts that ran are charged. Errors, 402s and rejected calls never are.
  A provider that bills a "not found" is charged and listed.

## Run it

```bash
npm install
export LOOOT_TOKEN=cs_ms_...        # runs.read + usage.read
node receipts.ts                     # the last 10 runs
node receipts.ts run_000028          # one run in detail
```

## With the MCP server

> Show my looot balance, then list my last 10 runs with runs_list. For the most expensive one,
> call runs_get and runs_evidence and explain each attempt and what it cost.
