"""PAID. Look up a LinkedIn profile (by URL) or a TikTok profile (by handle).

Usage: LOOOT_TOKEN=... python social_lookup.py linkedin <profile url>
       LOOOT_TOKEN=... python social_lookup.py tiktok <handle>
"""

import json
import sys

from looot import Looot

JOBS = {
    "linkedin": ("linkedin.person.profile", "url"),
    "tiktok": ("tiktok.user.profile", "handle"),
}

if len(sys.argv) != 3 or sys.argv[1] not in JOBS:
    sys.exit(__doc__)

job, field = JOBS[sys.argv[1]]
with Looot() as looot:
    run = looot.run_job(job, {field: sys.argv[2]}, prefer="cheapest", fallback={"maxAttempts": 2}, wait=45)
    print(f"{run['status']} via {(run.get('route') or {}).get('servedBy', run.get('endpointId'))}, ${run.get('actualCost')}", file=sys.stderr)
    print(json.dumps(run.get("result") if run["status"] == "completed" else run.get("error"), indent=2))
