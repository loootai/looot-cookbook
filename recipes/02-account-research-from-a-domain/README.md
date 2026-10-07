# Account research from a domain

Input: one company domain. Output: a short account brief with the company record, its tech
stack and the email addresses known at the domain.

## Jobs used

| Job | Input sent | Providers that accept it, price |
| --- | --- | --- |
| `company.enrich` | `domain` | `hunter-companies-find` $0.0049 / call, `tomba-companies-find` $0.0089 / call, `fullenrich-api-company-lookup` $0.016 / result, `findymail-api-search-company` $0.0198 / call |
| `company.technographics` | `domain` | `tomba-technology` $0.0089 / call |
| `people.domain.search` | `domain` | `hunter-domain-search-get` $0.00245 / result, `tomba-domain-search` $0.0089 / call |

Prices from the public catalog on 2026-09-28. Other providers in these jobs take different
inputs: `builtwith-free1-api-json` (free) takes `LOOKUP`, not `domain`, which is why the recipe
names `tomba-technology` directly.

## How it works

Three runs in parallel, each with its own idempotency key:

- `job:company.enrich` with `{ domain }` and `fallback: { prefer: "cheapest" }`.
- `tomba-technology` with `{ domain }` (a named endpoint, no job pick needed).
- `job:people.domain.search` with `{ domain }`, fallback on.

Then print each `result`. Provider shapes differ, so the script prints them as they come;
`inspect` any endpoint to see its output summary first.

## Run it

```bash
npm install --ignore-scripts=false   # builds looot-js from GitHub
export LOOOT_TOKEN=cs_ms_...
node account-research.ts example.com
```

PAID: three runs, about $0.02 to $0.05 in total depending on which providers answer.

## With the MCP server

> Research the account example.com with looot. Run job:company.enrich and
> job:people.domain.search with {"domain": "example.com"} and fallback prefer cheapest, and
> run tomba-technology with the same input. Summarise the company, its stack and the three
> most senior contacts. Tell me what each run cost.
