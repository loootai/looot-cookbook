# Web page to markdown

Input: a URL. Output: the page as markdown, ready to put in a prompt.

## Job used

| Job | Input sent | Providers (all take `url`), price per call |
| --- | --- | --- |
| `web.scrape.markdown` | `url` | `jina-reader` $0.0002, `hyperbrowser-api-web-fetch` $0.001, `context-dev-web-scrape-markdown` $0.0025, `steel-scrape` $0.005 |

All four providers take the same input, so `job:web.scrape.markdown` with fallback walks from
the cheapest to the next one if a page blocks the first.

## Run it

```bash
npm install
export LOOOT_TOKEN=cs_ms_...
node page-to-markdown.ts https://www.example.com > page.md
```

PAID: usually $0.0002, at most `maxCostUsd` (0.02 in the script).

## With the MCP server

> Use looot job:web.scrape.markdown on https://www.example.com with fallback prefer cheapest
> and give me the markdown.
