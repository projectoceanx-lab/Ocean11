# Metrics Dashboard — Source of Truth

_Updated by Watchtower every heartbeat cycle. All agents reference this for decision-making._

## Daily Snapshot
| Metric | Today | Yesterday | 7-Day Avg | Target |
|---|---|---|---|---|
| Leads Acquired | 0 | — | — | 50/day |
| Leads Scored A/B | 0 | — | — | 60% A+B |
| Compliance Pass Rate | — | — | — | >95% |
| Leads Delivered | 0 | — | — | 40/day |
| Revenue | $0 | — | — | $800/day |
| Total Spend | $0 | — | — | <$400/day |
| CPL | — | — | — | <$12 |
| Gross Margin | — | — | — | >20% |
| AI Cost | $0 | — | — | <$5/day |

## Execution Discipline (Protocol KPIs)
_Protocol activated: 2026-02-18 01:41 GST_

| Metric | Today | Yesterday | 7-Day Avg | Target |
|---|---|---|---|---|
| Ack SLA Pass Rate (<=5m) | N/A (ack timestamp not instrumented) | — | — | >=95% |
| First Artifact SLA Pass Rate (<=30m) | 100% (4/4) | — | — | >=90% |
| Evidence-Complete Closure Rate | 100% (4/4) | — | — | >=90% |
| Reopen Rate | 0% (0/4) | — | — | <=10% |
| False-Complete Incidents | 0 | — | — | 0 |

_Execution KPI source: `shared/ACTION_LOG.md` entries `OCN-PROT-001`, `OCN-NDR-001`, `OCN-SLA-001`, and `OCN-NDR-002`, checked 2026-02-18 01:58 GST._

## By Source
| Source | Leads | CPL | Quality Avg | Status |
|---|---|---|---|---|
| Facebook | 0 | — | — | Not started |
| RevPie | 0 | — | — | Not started |
| Email | 0 | — | — | Not started |
| Organic | 0 | — | — | Not started |

## By Buyer
| Buyer | Delivered | Accepted | Returned | Payout | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## System Health
_Last checked: 2026-02-14 23:53 GMT+4 by Watchtower_

| Metric | Value |
|---|---|
| Total files in repo | 106 |
| Last commit | `96d888a` — Document Max subscriptions |
| Git status | Clean (1 tracked modification: shared/CONTEXT.md) |
| Agent files (SOUL/config/MISSIONS) | 18/18 ✅ |
| Docs files | 7 ✅ |
| Shared files | 7 ✅ |
| DB files | 3 ✅ |
| Missing files | None |
| Infrastructure status | Pre-launch — Supabase, Ringba, FastDebt all pending |

## Alerts
<!-- Watchtower flags anomalies here -->
