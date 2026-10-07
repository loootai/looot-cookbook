# Social profile lookup

Input: a LinkedIn profile URL or a TikTok handle. Output: the public profile.

## Jobs used

| Job | Input sent | Providers that accept it, price |
| --- | --- | --- |
| `linkedin.person.profile` | `url` | `scrapecreators-linkedin-profile` $0.00188 / call, `icypeas-scrape-profile` $0.0285 / result, `tikhub-api-linkedin-web-v2-get-user-profile` $0.05 / call |
| `tiktok.user.profile` | `handle` | `scrapecreators-tiktok-profile`, `scrapecreators-tiktok-user-profile`, `scrapecreators-tiktok-profile-region`, each $0.00188 / call |

Other providers in these jobs take different names: `anysite-api-linkedin-user` wants `user`,
`leadmagic-people-profile-search` wants `profile_url`, TikHub's TikTok endpoints want
`uniqueId`, and `searchapi-io-tiktok-profile` wants `username`. The job pick skips them when you
send `url` or `handle`; name one directly to use it.

## Run it

```bash
pip install git+https://github.com/loootai/looot-python
export LOOOT_TOKEN=cs_ms_...
python social_lookup.py linkedin https://www.linkedin.com/in/example
python social_lookup.py tiktok example
```

PAID: about $0.002 per lookup with the cheapest provider.

## With the MCP server

> Look up the TikTok account "example" with looot job:tiktok.user.profile and
> {"handle": "example"}, fallback on. Give me followers, likes and bio.
