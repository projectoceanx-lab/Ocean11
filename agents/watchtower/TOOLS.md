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

## Notes
- Cheapest agent — check often, report concisely
- Escalate critical alerts directly to AK
