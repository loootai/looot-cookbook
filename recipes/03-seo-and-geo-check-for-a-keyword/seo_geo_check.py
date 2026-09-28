"""PAID. Google rank, search volume and ChatGPT/Perplexity mentions for one keyword.

Usage: LOOOT_TOKEN=... python seo_geo_check.py "<keyword>" <domain> [--no-volume]
       [--location "United States"] [--language en]
"""

from __future__ import annotations

import argparse
import json
from datetime import date

from looot import Looot


def urls_in_order(result) -> list[str]:
    """Every string that looks like a URL, in document order."""
    found: list[str] = []

    def walk(value):
        if isinstance(value, str) and value.startswith("http"):
            found.append(value)
        elif isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(result)
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("keyword")
    ap.add_argument("domain")
    ap.add_argument("--no-volume", action="store_true")
    ap.add_argument("--location", default="United States")
    ap.add_argument("--language", default="en")
    args = ap.parse_args()
    key = lambda step: f"cookbook-seo-{step}-{args.keyword}-{date.today()}"  # noqa: E731

    with Looot() as looot:
        serp = looot.run("scrapecreators-google-search", {"query": args.keyword}, wait=45, idempotency_key=key("serp"))
        urls = [u for u in dict.fromkeys(urls_in_order(serp.get("result")))]
        rank = next((i + 1 for i, u in enumerate(urls) if args.domain in u), None)
        print(f"Google: {args.domain} first seen at link #{rank}" if rank else f"Google: {args.domain} not in the result")

        if not args.no_volume:
            vol = looot.run(
                "dataforseo-keywords-data-google-ads-search-volume-live-ai",
                {"keywords": [args.keyword], "language_code": args.language, "location_name": args.location},
                wait=45,
                idempotency_key=key("volume"),
            )
            print("Volume result:", json.dumps(vol.get("result"))[:600])

        for label, endpoint in (("ChatGPT", "searchapi-io-chatgpt"), ("Perplexity", "searchapi-io-perplexity")):
            run = looot.run(endpoint, {"q": args.keyword}, wait=45, idempotency_key=key(endpoint))
            text = json.dumps(run.get("result")).lower()
            print(f"{label}: {text.count(args.domain.lower())} mention(s) of {args.domain}, cost ${run.get('actualCost')}")


if __name__ == "__main__":
    main()
