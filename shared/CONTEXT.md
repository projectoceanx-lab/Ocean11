# Shared Context — All Agents Read This

_This file is the shared brain. Every agent reads it at session start. Update it when decisions change._

## Current Phase: PHASE 0 — Database + First Lead
_Nothing else matters until this is done._

## Current State
- **Phase:** Phase 0 (no database, no leads, no revenue)
- **Active Agents:** None yet (configuring)
- **Budget Spent:** $0 / $5,000
- **Leads Generated:** 0
- **Revenue:** $0

## Active Decisions

### Captain's Brief — 2026-02-14 23:57 GST
**State of play:** Three agents completed recon. We have solid intel on 3 form targets (Scout), a clear compliance threat map (Shield), and a verified repo baseline (Watchtower). No money spent. No infrastructure live. We're in the "know before you go" phase and it's going well.

**Key findings:**
1. All 3 debt relief targets require headless browser (Playwright) — no shortcuts
2. Pacific Debt is our easiest first target (button-based step 1, low complexity)
3. Advance fee ban is the #1 compliance landmine — every buyer must be vetted on this before first delivery
4. FTC "common enterprise" doctrine means bad buyers = our liability. Buyer vetting is not optional, it's existential.
5. Infrastructure (Supabase, Ringba, FastDebt) is all pending — this is the actual bottleneck now

**Recommended next steps for Arif:**
1. **Supabase setup** — We need a database before Scout can store anything. Schema exists in `db/schema.sql`. Priority #1.
2. **Scout: deep-map Pacific Debt full funnel** — Easiest target, get full field schema, validate against DB schema
3. **Shield: map state licensing requirements** — Which states require licensing for debt relief lead gen?
4. **Start buyer outreach list** — I need to know who we're selling to. Arif: any existing contacts from Zappian, or cold start?
5. **Hawk + Signal stay offline** — No traffic to buy, no leads to deliver. They activate when infrastructure is ready.

## Blockers
<!-- Any agent can flag a blocker here — Captain triages -->

## Today's Priority
_Set by Captain 🎖️ — 2026-02-14_
1. **Arif decision needed:** Supabase setup + buyer contact list (existing or cold start?)
2. Scout: deep-map Pacific Debt full funnel (all steps, all fields, hidden fields, honeypots)
3. Shield: state licensing requirements for debt relief lead gen
4. Watchtower: verify infrastructure endpoint reachability (Supabase, any configured APIs)

## Agent Status Board
| Agent | Status | Last Active | Current Task |
|---|---|---|---|
| Captain | 🟡 Idle | 2026-02-14 23:57 GST | First review complete — scored Scout/Shield/Watchtower recon, set priorities |
| Scout | 🟡 Idle | 2026-02-14 | Recon complete — 3 targets mapped in KNOWLEDGE_HUB.md |
| Shield | 🟡 Idle | 2026-02-14 23:54 GST | Completed: FTC enforcement review. 3 pre-launch gates defined. |
| Hawk | 🟡 Idle | 2026-02-15 00:00 GST | Complete: FB Ads debt relief CPL benchmarks → KNOWLEDGE_HUB.md |
| Signal | 🟡 Idle | 2026-02-14 23:58 GST | Completed: Buyer landscape research. Intel in KNOWLEDGE_HUB.md. Needs live verification via Everflow/network logins. |
| Watchtower | 🟡 Idle | 2026-02-14 | Health check complete — all systems nominal |

## Handoff Queue
<!-- When one agent needs another to pick up work -->
<!-- Format: [FROM] → [TO]: description (priority: high/medium/low) -->
