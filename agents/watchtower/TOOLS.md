# TOOLS.md — Watchtower

## Active Tools
- **Database:** Supabase (pending setup) — read-only access to all tables

## Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Agent silent | > 30 min | > 1 hour |
| Daily AI cost | > $10 | > $15 |
| Shield block rate | > 15% | > 25% |
| Delivery failure | > 10% | > 20% |
| DB rows | > 8K | > 9K |

## Memory Vault
- **Search:** `python3 scripts/memory-search.py "query" --agent watchtower --limit 5`
- **Decay:** `python3 scripts/memory-decay.py` (daily cron)
- **Promote:** `python3 scripts/memory-promote.py` (auto-promote high-confidence observations)

## Google Services (gog CLI)
- `gog` CLI available for Google Drive — useful for uploading daily ops reports
- Example: `gog drive upload ./daily-report.md`

## Notes
- Cheapest agent — check often, report concisely
- Escalate critical alerts to Fury → Ocean (never directly to AK)
