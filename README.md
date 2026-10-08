# looot cookbook

Short, runnable recipes for [looot](https://looot.ai): one gateway to about 2,500 data provider
operations with one token and one prepaid balance. Each recipe names the real job ids, endpoint
ids and input names it uses, as the public catalog lists them. `tests/check_recipes.py` checks
every one of those names against the live catalog, so a recipe cannot quietly drift.

## Install for agents

```bash
git clone https://github.com/loootai/looot-cookbook
claude mcp add --transport http looot https://api.looot.ai/mcp
```

See also: [awesome-looot-use-cases](https://github.com/loootai/awesome-looot-use-cases) (copy-paste recipes) and [awesome-gtm](https://github.com/loootai/awesome-gtm) (open-source GTM tools).

> Status: public, MIT. Recipes install `looot-js` and `looot` (Python) from GitHub until both are
> on npm and PyPI.

| # | Recipe | Jobs | Cost per run | Code |
| --- | --- | --- | --- | --- |
| 01 | [Enrich a lead list](recipes/01-enrich-a-lead-list/) | `people.email.find`, `people.email.verify` | from about $0.011 per row | Python |
| 02 | [Account research from a domain](recipes/02-account-research-from-a-domain/) | `company.enrich`, `company.technographics`, `people.domain.search` | about $0.02 to $0.05 | TypeScript |
| 03 | [SEO plus GEO check for a keyword](recipes/03-seo-and-geo-check-for-a-keyword/) | `google.serp.organic`, `google.keywords.volume`, `search.chatgpt`, `search.perplexity` | about $0.10, or $0.01 without volume | Python |
| 04 | [Web page to markdown](recipes/04-web-page-to-markdown/) | `web.scrape.markdown` | from $0.0002 | TypeScript |
| 05 | [Social profile lookup](recipes/05-social-profile-lookup/) | `linkedin.person.profile`, `tiktok.user.profile` | about $0.002 | Python |
| 06 | [Reading receipts](recipes/06-reading-receipts/) | none, reads runs and balance | free | TypeScript |

Every recipe also has a plain-English prompt for the MCP server, for agents that use looot
through Claude Code, Cursor, Codex or any other MCP client.

## Install

```bash
# TypeScript recipes
npm install --ignore-scripts=false            # builds looot-js from GitHub

# Python recipes
python3 -m venv .venv && .venv/bin/pip install git+https://github.com/loootai/looot-python
```

## 60-second quickstart

1. Browse for free, no token: `curl "https://api.looot.ai/v1/catalog/overview?topic=email"`.
2. Create an agent token at looot.ai (Settings, Agent tokens) and `export LOOOT_TOKEN=cs_ms_...`.
3. Top up; a new workspace starts at $0. `node recipes/06-reading-receipts/receipts.ts` prints
   the balance for free.
4. Run the cheapest recipe:
   `node recipes/04-web-page-to-markdown/page-to-markdown.ts https://www.example.com`.

## Rules every recipe follows

- Only real names. Every job, endpoint and input is in `recipes.json` and checked live.
- Idempotency keys are stable per logical step, so a re-run never pays twice for the same row.
- Fallback carries a `maxCostUsd`, so a walk through providers has a ceiling.
- A run's `status` is read before its `result`: a 201 can still be `failed`.

## Test

```bash
python3 tests/check_recipes.py      # free public routes only, standard library
bash scripts/leak-scan.sh .
```

## Links

- Catalog overview (free): https://api.looot.ai/v1/catalog/overview
- Agent guide: https://api.looot.ai/llms.txt
- OpenAPI: https://api.looot.ai/openapi.json
- Docs: https://looot.ai/docs

## License

MIT. See [LICENSE](LICENSE).
