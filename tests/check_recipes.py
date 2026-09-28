"""Checks that every job, endpoint and input name in recipes.json exists in the live catalog.

Uses only free public routes (no token, no cost):
  GET https://api.looot.ai/v1/public-catalog?capability=<job with dots as underscores>
  GET https://api.looot.ai/v1/catalog/overview?topic=<word>   (job ids)

Standard library only. Run: python3 tests/check_recipes.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.looot.ai"
ROOT = Path(__file__).resolve().parent.parent


def get(path: str) -> dict:
    req = urllib.request.Request(API + path, headers={"accept": "application/json", "user-agent": "looot-cookbook-check"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def items_for_job(job: str) -> dict:
    cap = urllib.parse.quote(job.replace(".", "_"))
    page = get(f"/v1/public-catalog?limit=100&capability={cap}")
    return {item["catalogItemId"]: item for item in page["items"]}


def main() -> int:
    manifest = json.loads((ROOT / "recipes.json").read_text())
    failures: list[str] = []
    checked = 0
    for recipe in manifest["recipes"]:
        rid = recipe["id"]
        if not (ROOT / "recipes" / rid / "README.md").exists():
            failures.append(f"{rid}: recipes/{rid}/README.md is missing")
        for job, spec in recipe["jobs"].items():
            items = items_for_job(job)
            if not items:
                failures.append(f"{rid}: job {job} has no public endpoints")
                continue
            for endpoint in spec["endpoints"]:
                item = items.get(endpoint)
                if item is None:
                    failures.append(f"{rid}: {endpoint} is not listed under job {job}")
                    continue
                names = {p["name"] for p in item["parameters"]}
                required = {p["name"] for p in item["parameters"] if p["required"]}
                used = set(spec["input"])
                # The recipe's input must fit the endpoint: every required field is sent,
                # and at least one field we send is one it takes.
                if not required <= used:
                    failures.append(f"{rid}: {endpoint} requires {sorted(required - used)} which the recipe does not send")
                if not used & names:
                    failures.append(f"{rid}: {endpoint} takes none of {sorted(used)}")
                checked += 1
    status = "FAIL" if failures else "OK"
    print(f"check_recipes: {status}, {checked} endpoint(s) checked across {len(manifest['recipes'])} recipes")
    for f in failures:
        print("  -", f)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
