# Watchtower — Active Missions

## 🎯 Phase 1 Objectives

### Database Management (Supabase)
- [x] Baseline DB is live and verified (`leads`, `buyers`, `campaigns`, `deliveries`, `pnl_daily`, `compliance_log`, `agent_activity`, `offer_fields`)
- [x] Offer-cap schema is applied (`everflow_offers`, `offer_submissions`, `postback_log`) with helper functions
- [ ] Keep free-tier limits under watch (storage + row count) and alert before thresholds
- [ ] Run weekly dedup checks (`leads.email` + `leads.phone`) and report drift
- [ ] Monitor slow queries and recommend index/migration fixes
- [ ] Enforce and review agent access matrix by role

### Vercel & Postback Reliability
- [x] Postback receiver deployment is live and health-checkable
- [ ] Keep endpoint uptime checks active and alert on any downtime >1 minute
- [ ] Validate production env var presence after each deploy/redeploy
- [ ] Track Everflow global postback setup status until end-to-end proof lands

### System Monitoring
- [ ] Monitor all agent heartbeats — critical alert if any agent is silent >1h
- [ ] Track daily AI spend — warning >$10, critical >$15
- [ ] Monitor pipeline health (acquired vs delivered vs confirmed conversions)
- [ ] Watch for fallback/model-routing anomalies and log recurrence
- [ ] Track compliance failure rates (Shield block rate) and escalate outliers
- [ ] Log all alerts and system events in shared context with owner and timestamp

### Memory System Maintenance
- [ ] Daily cron: run `scripts/memory-maintain.sh` (ref → decay → promote)
- [ ] Monitor vault sizes across agents
- [ ] Alert if `shared/observations` grows >50 files (cleanup review needed)

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
| Landing page/postback down | > 1 min | > 5 min |
| Email bounce rate | > 3% | > 5% |

## 🚧 Blockers
- Everflow global postback is not yet configured to Ocean receiver endpoint (proof pending)
- Runtime fallback reliability incident remains open (intermittent model/provider path instability)
- Memory maintenance fallback policy needs hardening after model-access failure incident

## 📝 Notes
- Watchtower is a monitoring role: concise, evidence-based reporting over narrative
- Watchtower does not own spend/campaign execution; it owns anomaly detection and escalation
- Escalate critical alerts to Fury → Ocean (Ocean routes to AK when needed)
- DB access matrix enforcement: use AGENTS.md + PLAYBOOK rules as policy source

## Standing Order (Every Session)
Before closing: update shared/CONTEXT.md, memory/YYYY-MM-DD.md, and shared/KNOWLEDGE_HUB.md per shared/PLAYBOOK_RULES.md § MANDATORY CHECKPOINTS. No exceptions.
