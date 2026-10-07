# SEO plus GEO check for a keyword

Input: a keyword and your domain. Output: where the domain ranks on Google, the keyword's
monthly volume, and whether ChatGPT and Perplexity mention the domain when asked about it.

## Jobs used

| Check | Job | Endpoint | Input sent | Price |
| --- | --- | --- | --- | --- |
| Google rank | `google.serp.organic` | `scrapecreators-google-search` | `query` | $0.00188 / call |
| Search volume | `google.keywords.volume` | `dataforseo-keywords-data-google-ads-search-volume-live-ai` | `keywords` (array), `language_code`, `location_name` | $0.09 / call |
| ChatGPT answer | `search.chatgpt` | `searchapi-io-chatgpt` | `q` | $0.004 / call |
| Perplexity answer | `search.perplexity` | `searchapi-io-perplexity` | `q` | $0.004 / call |

Prices from the public catalog on 2026-09-28. Volume is the expensive step; skip it with
`--no-volume`. `google.serp.ai-mode` (Google's AI Mode) is another GEO source, but its
`tasks` input has no documented example yet, so `inspect` it before adding it.

## How it works

1. Google SERP for the keyword, then find the first result whose URL contains your domain.
2. Volume for `[keyword]` in `United States`, `en` (change both with flags).
3. Ask ChatGPT and Perplexity the keyword as a question. Count mentions of your domain in the
   answer text. That count is the GEO signal.

Each provider returns its own shape, so the script searches the result JSON as text for the
domain instead of reading one fixed field.

## Run it

```bash
pip install git+https://github.com/loootai/looot-python
export LOOOT_TOKEN=cs_ms_...
python seo_geo_check.py "email verification api" example.com
python seo_geo_check.py "email verification api" example.com --no-volume
```

PAID: about $0.10 with volume, about $0.01 without.

## With the MCP server

> For the keyword "email verification api" and the domain example.com: run looot
> scrapecreators-google-search with {"query": ...} and tell me the domain's position; run
> searchapi-io-chatgpt and searchapi-io-perplexity with {"q": ...} and tell me whether each
> answer mentions example.com. Report the cost of each run.
