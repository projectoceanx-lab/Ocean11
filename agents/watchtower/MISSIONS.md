# Watchtower — Active Missions

## 🎯 Phase 1 Objectives

### Database Management (Supabase)
- [ ] Run schema.sql + seed.sql on Supabase project
- [ ] Verify all 7 tables created correctly with indexes
- [ ] Set up pg_cron: daily buyer cap reset at midnight EST
- [ ] Monitor free tier limits (500MB, 50K rows)
- [ ] Run dedup checks weekly (leads.email + leads.phone)
- [ ] Monitor query performance, flag slow queries
- [ ] Manage schema migrations (`db/migrations/`)
- [ ] Enforce agent access matrix (who can read/write which tables)

### Vercel Deployment
- [ ] Connect repo to Vercel project (Forge's Next.js site)
- [ ] Configure environment variables (Supabase keys, FastDebt API, etc.)
- [ ] Monitor build status, deploy previews on PR
- [ ] Alert if landing pages go down (uptime check)
- [ ] Manage production vs preview environments

### System Monitoring
- [ ] Monitor all agent heartbeats — alert if any agent goes silent > 1h
- [ ] Track daily AI spend across all agents — alert if > $15/day
- [ ] Monitor lead pipeline health (intake vs delivery rate)
- [ ] Watch for compliance failures (Shield block rate > 20% = alert)
- [ ] Track infrastructure costs (Supabase, Vercel, proxies, APIs)
- [ ] Log all alerts and system events

### Memory System Maintenance
- [ ] Daily cron: run `scripts/memory-maintain.sh` (ref → decay → promote)
- [ ] Monitor vault sizes across agents
- [ ] Alert if shared/observations grows >50 files (review needed)

## 📋 Alert Thresholds
| Metric | Warning | Critical |
|--------|---------|----------|
| Agent silent | > 30 min | > 1 hour |
| Daily AI cost | > $10 | > $15 |
| Shield block rate | > 15% | > 25% |
| Delivery failure rate | > 10% | > 20% |
| DB row count | > 40K | > 48K (free tier limit) |
| DB storage | > 400MB | > 475MB |
| Vercel build fail | 1 failure | 2+ consecutive |
| Landing page down | > 1 min | > 5 min |
| Email bounce rate | > 3% | > 5% |

## 🚧 Blockers
- Supabase project not created yet (waiting on Arif)
- Vercel project not linked yet

## 📝 Notes
- Watchtower is the cheapest agent (GPT-5-nano) — run often, report concisely
- Watchtower does NOT write business data — manages infrastructure that holds it
- Escalate critical alerts directly to Arif via OpenClaw notification
- DB access matrix enforcement: read AGENTS.md for who can access what
