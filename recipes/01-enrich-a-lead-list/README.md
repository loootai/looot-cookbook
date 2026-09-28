# Enrich a lead list: find and verify work emails

Input: a CSV of `first_name,last_name,domain`. Output: the same rows with a verified email.

## Jobs used

| Step | Job | Input sent | Providers that accept it, price per call |
| --- | --- | --- | --- |
| Find | `people.email.find` | `first_name`, `last_name`, `domain` | `tomba-email-finder` $0.0089, `leadmagic-people-email-finder` $0.0198, `hunter-email-finder` $0.0245 |
| Verify | `people.email.verify` | `email` | `icypeas-email-verify` $0.0019, `leadmagic-email-verify` $0.00495, `tomba-email-verifier` $0.0089, `zerobounce-validate` $0.01, `hunter-email-verifier` $0.01225, `findymail-api-verify` $0.0198 |

Prices from the public catalog (`GET /v1/public-catalog?capability=people_email_find`) on
2026-09-28. Check again before a big batch.

Some providers in `people.email.find` want other inputs (`icypeas-email-find` wants
`domainOrCompany`, `findymail-api-search-name` wants `name`). Sending `job:people.email.find`
lets looot pick the first provider whose schema accepts what you sent, so those are skipped.

## How it works

1. `run` with `endpointId: "job:people.email.find"` and `fallback: { prefer: "cheapest", maxAttempts: 3 }`.
   On a miss looot tries the next provider inside one hold; only attempts that ran are charged.
2. Read the found address from the provider's `result` (or `normalized.fields` when the gateway
   adds it). Every provider shapes `result` its own way, so inspect one first.
3. `run` `job:people.email.verify` on that address. When the gateway adds `normalized`, its
   `verdict` gives the answer and the email status is one of `valid`, `invalid`, `catch_all`,
   `risky` or `unknown`. Every run also carries `outcome` (`hit`, `miss` and so on).
4. Use a stable `idempotencyKey` per row (`cookbook-find-<row hash>`), so a crashed batch can be re-run
   without paying twice.

## Run it

```bash
pip install ../looot-python          # or the published package, once there is one
export LOOOT_TOKEN=cs_ms_...         # runs.execute + runs.read
python enrich_leads.py leads.example.csv > enriched.csv
```

PAID: two lookups per row, at most `maxCostUsd` each. Start with three rows.

## With the MCP server

> Read leads.csv. For each row, run looot `job:people.email.find` with first_name, last_name
> and domain, fallback prefer cheapest, max 3 attempts. Then run `job:people.email.verify` on
> the address found. Use one idempotencyKey per row and step. Show me the cost of each row.
