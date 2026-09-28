---
name: looot-cookbook
description: Write or update a recipe in looot-cookbook, the runnable examples for the looot API and MCP server. Use when adding a recipe, when a catalog change breaks tests/check_recipes.py, or when prices in a recipe need refreshing.
---

# looot-cookbook

## What this repo is

Short recipes, one folder each under `recipes/`: a README (jobs table, how it works, how to run,
an MCP prompt) and one script using `looot-js` or `looot-python`. `recipes.json` lists every job
id, endpoint id and input name the recipes use.

## Build and test

```bash
python3 tests/check_recipes.py      # free public routes only, stdlib
bash scripts/leak-scan.sh .
git config core.hooksPath .githooks
```

Running a recipe script is PAID (except 06). Never run one from a test or from CI.

## Adding a recipe

1. Find the job: `GET https://api.looot.ai/v1/catalog/overview?topic=<word>` (free).
2. List its providers and their inputs:
   `GET https://api.looot.ai/v1/public-catalog?capability=<job with dots as underscores>&limit=100`.
   Read an agent card at `https://api.looot.ai/catalog/<endpointId>.md` for examples.
3. Pick input names that the providers you name actually take. Never invent a field. If a
   field is not in the public catalog or a card, leave it out and say "inspect first".
4. Add the recipe to `recipes.json` and run `tests/check_recipes.py` until it passes.
5. Write prices as the catalog shows them, with the date.

## Release later (only after the owner says yes)

Swap `file:../looot-js` and `pip install ../looot-python` for the published package names and
exact versions, then tag.

## Public looot surface this repo may use

`https://api.looot.ai/v1/catalog/overview`, `/v1/public-catalog`, `/catalog/*.md`,
`/llms.txt`, `/llms-full.txt`, `/openapi.json`, the MCP server at `https://api.looot.ai/mcp`,
and `https://looot.ai/docs`.

## Never

- Copy code or text from the private gateway repo, or read its catalog seed files.
- Commit a token, key, `.env` file, or a real person's email, name or profile URL. Use
  `example.com` and `example` placeholders.
- Write internal hosts, local machine paths, workspace or customer ids.
- Name private repos or private branches.
