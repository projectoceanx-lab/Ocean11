# Watchtower — Active Missions

## 🎯 Phase 1 Objectives
- [ ] Monitor all agent heartbeats — alert if any agent goes silent > 1h
- [ ] Track daily AI spend across all agents — alert if > $15/day
- [ ] Monitor lead pipeline health (intake vs delivery rate)
- [ ] Watch for compliance failures (Shield block rate > 20% = alert)
- [ ] Track Supabase usage (free tier limits)
- [ ] Log all alerts and system events

## 📋 Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Agent silent | > 30 min | > 1 hour |
| Daily AI cost | > $10 | > $15 |
| Shield block rate | > 15% | > 25% |
| Delivery failure rate | > 10% | > 20% |
| DB row count | > 8K | > 9K (free tier limit) |

## 🚧 Blockers
- None yet

## 📝 Notes
- Watchtower is the cheapest agent — check often, report concisely
- Escalate critical alerts directly to Arif via OpenClaw notification
- Keep monitoring logs for audit/debugging
