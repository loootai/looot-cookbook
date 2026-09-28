"""PAID. Find and verify a work email for every row of a CSV (first_name,last_name,domain).

Usage: LOOOT_TOKEN=... python enrich_leads.py leads.csv > enriched.csv
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys

from looot import Looot, LoootError

FALLBACK = {"prefer": "cheapest", "maxAttempts": 3, "maxCostUsd": 0.1}


def row_key(step: str, row: dict) -> str:
    digest = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()[:16]
    return f"cookbook-{step}-{digest}"


def find_email(result) -> str | None:
    """Returns the first string that looks like an email anywhere in a provider result."""
    if isinstance(result, str):
        return result if "@" in result and " " not in result else None
    if isinstance(result, dict):
        for key in ("email", "value"):
            if isinstance(result.get(key), str) and "@" in result[key]:
                return result[key]
        values = result.values()
    elif isinstance(result, list):
        values = result
    else:
        return None
    for value in values:
        found = find_email(value)
        if found:
            return found
    return None


def main(path: str) -> None:
    out = csv.DictWriter(sys.stdout, ["first_name", "last_name", "domain", "email", "status", "served_by", "cost_usd"])
    out.writeheader()
    with Looot() as looot, open(path, newline="") as f:
        for row in csv.DictReader(f):
            lead = {k: row[k].strip() for k in ("first_name", "last_name", "domain")}
            try:
                found = looot.run_job(
                    "people.email.find", lead, fallback=FALLBACK, wait=45, idempotency_key=row_key("find", lead)
                )
            except LoootError as e:
                sys.exit(f"stopped: {e.code}: {e.message}")
            cost = found.get("actualCost") or 0
            email = find_email((found.get("normalized") or {}).get("fields")) or find_email(found.get("result"))
            status = "not_found"
            if email:
                checked = looot.run_job(
                    "people.email.verify",
                    {"email": email},
                    fallback=FALLBACK,
                    wait=45,
                    idempotency_key=row_key("verify", {"email": email}),
                )
                cost += checked.get("actualCost") or 0
                # normalized.verdict is documented in llms-full.txt; outcome is on every run.
                status = (checked.get("normalized") or {}).get("verdict") or checked.get("outcome") or checked["status"]
            out.writerow({**lead, "email": email or "", "status": status,
                          "served_by": (found.get("route") or {}).get("servedBy", found.get("endpointId")),
                          "cost_usd": round(cost, 6)})


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "leads.example.csv")
