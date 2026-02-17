# Shared Context — All Agents Read This

_This file is the shared brain. Every agent reads it at session start. Update it when state changes._

## Current Phase: PHASE 1 — Scout + Shield Loop
_Phase 0 ✅ COMPLETE (Feb 15, 2026). First form filled, first lead stored._

## Current State
- **Phase:** Phase 1 (acquire → comply → score → route to buyer)
- **Primary Goal (AK directive):** Website conversion acceleration as top priority — optimize EBC immediately while building a new high-converting site in parallel.
- **Active Agents:** All agents gearing up under parallel-track execution (no passive standby posture on critical tracks)
- **Infra update (2026-02-16 23:15 GMT+4):** Ocean postback endpoint deployed on Vercel at `https://ocean11-postback.vercel.app` (health OK). Vision = primary owner, Peter = backup owner.
- **Vision navigation drill update (2026-02-16 23:55 GMT+4):** Completed deep Everflow postback/navigation drill and published evidence-based runbook at `docs/EVERFLOW_POSTBACK_SPECIALIST_PLAYBOOK.md` (menus, routes, role limitations, implementation checklist, troubleshooting, self-test).
- **NDR Form Map complete (2026-02-17 01:30 GMT+4):** Full form mapping published at `docs/NDR_FORM_MAP.md`. 2-step form: (1) debt amount dropdown on `/apply`, (2) contact info (first name, last name, email, phone) on `/details`. **No CAPTCHA.** Primary anti-bot: TrustedForm (records mouse/keystrokes for TCPA cert). Also has Datadog RUM, Hotjar session recording, 118 tracking scripts. Hidden fields: TrustedForm cert URL + token + ping URL. Gravity Forms-style field naming. Key blocker: need to test post-submission behavior + phone mask without creating real leads.
- **Model routing update (2026-02-17 00:36 GMT+4):** Fury switched from `openai-codex/gpt-5.3-codex-spark` to `openai-codex/gpt-5.3-codex` in live runtime config (`~/.openclaw/openclaw.json`) and template config (`config/openclaw.yaml`). Gateway restart executed via `openclaw gateway restart`.
- **Agent alignment hardening (2026-02-17):** Canonical agent IDs standardized (`fury/scout/shield/hawk/forge/watchtower/peter/ocean`) across repo configs and identity docs, stale `captain/signal` template references removed, and drift guard added at `scripts/validate_agent_alignment.sh` (runtime-aware `main` → `fury` normalization).
- **Budget Spent:** $0 / $5,000
- **Leads in DB:** 2 (1 dry run, 1 submitted to JGW) — unchanged since last sync
- **Revenue:** $0 — unchanged since last sync
- **Latest sync note (2026-02-17 11:44 GST):** Daily all-agent sync complete. No numeric data changes detected (leads/revenue/spend/deliveries unchanged).

## 📋 MANDATORY READING — All Agents

Every agent MUST read these before acting:

| File | What | Why |
|---|---|---|
| `docs/BUYERS_PLAYBOOK.md` | Full buyer stack, routing logic, cap rules | Defines how leads flow to revenue |
| `docs/OFFER_CAPS.md` | Per-offer caps, restrictions, state exclusions | Prevents overfilling, compliance |
| `docs/COMPLIANCE_RULES.md` | FTC, TSR, TCPA, CAN-SPAM, state rules | Non-negotiable — Shield enforces |
| `shared/PLAYBOOK_RULES.md` | Hard rules — violate = escalation | Everyone reads, no exceptions |
| `shared/KNOWLEDGE_HUB.md` | Learned patterns, form filling playbook, platform intel | Don't repeat mistakes |

## ⚠️ CRITICAL BUSINESS LOGIC — Caps & Conversions

**Read `docs/BUYERS_PLAYBOOK.md` for full details. Summary:**

1. **Submission ≠ Revenue.** We fill a form (submission). Buyer checks quality/dedup. If accepted → Everflow pixel fires (conversion). CONVERSION = revenue.
2. **Cap = max confirmed conversions**, not submissions. Postbacks can be delayed hours.
3. **Safety buffer:** Stop submitting at 1.5x cap to prevent overfilling.
4. **AK provides caps weekly** (Monday 9AM IST cron). Fury updates `offer_caps` table + OFFER_CAPS.md.
5. **Before every fill:** Check `can_submit_to_offer()` — day allowed? State ok? Under cap? Dedup clear?

## Live Platforms

### Everflow (RevvMind) — Offer Tracking & Attribution
- **URL:** revvmind.everflowclient.io
- **Login:** arif@revvmind.com
- **Role:** Partner/Affiliate
- **10 debt relief offers** (FDR $60, NDR $16-50, JGW $22-25, Cliqsilver $30)
- **5 loan offers** (Zappian legacy, CPS 100%)
- **Jan 2026:** 310 clicks, 6 conversions, $24 revenue, 1.94% CVR
- **Account Manager:** Zakir Khan (zakir@zappian.com)

### RevPie — Native Ad Traffic Source
- **URL:** revpie.com
- **Login:** vishal@revvmind.com
- **Role:** Advertiser
- **Balance:** $481.57 | Lifetime spend: $15,518.43
- **7 campaigns** (all paused, Zappian era)
- **Key control:** Whitelist/Blacklist Source IDs + custom CPC bids
- **RevPie → Everflow:** Tracking links in ad URLs pass clicks to Everflow for attribution

### Supabase — Database
- **URL:** https://xpbbdmosyrhkoczhcgpt.supabase.co
- **Tables live:** leads, buyers, campaigns, deliveries, pnl_daily, compliance_log, agent_activity, offer_fields
- **Tables live (offer caps):** everflow_offers (10 rows, seeded), offer_submissions (0 rows), postback_log (2 rows) — schema applied & verified 2026-02-17 01:30 GMT+4
- **Functions live:** check_offer_cap(), increment_submission(), record_conversion(), reset_daily_caps(), reset_weekly_caps() — all verified via RPC
- **RLS enabled** on all 3 new tables (service_role policy)

## Offer Routing Priority (Highest CPA First)

| Priority | Offer | Buyer | CPA | Channel | Key Restriction |
|---|---|---|---|---|---|
| 1 | 4930 | FDR | $60 | Email | M-F only, ask for cap |
| 2 | 4905 | NDR | $50 | Web | TBD |
| 3 | 4836 | NDR | $45 | Email | M-F, budgeted |
| 4 | 4907 | Cliqsilver | $30 | Web | TBD |
| 5 | 4906 | JGW | $25 | Web | TBD |
| 6 | 4783 | NDR | $24 | Email | TBD |
| 7 | 4718 | JGW | $24 | Email | Marketplace |
| 8 | 4633 | JGW | $24 | Email | 7 days, NO CA |
| 9 | 4737 | JGW | $22 | Email | M-F |
| 10 | 4740 | NDR | $16 | Email | Budgeted, last resort |

_Caps (❓) to be filled by AK. See `docs/OFFER_CAPS.md` for full details._

## Phase 1 Milestones

- [x] Database live (Supabase)
- [x] First form mapped + filled (JGW)
- [x] First lead stored in DB
- [x] Everflow explored — all 15 offers mapped
- [x] RevPie explored — 7 campaigns, Source ID optimization documented
- [x] Cap management system designed (schema + cron)
- [x] Buyers Playbook rewritten with live data
- [x] **AK provides first round of caps** — weekly cap set to 5 conversions/offer (2026-02-16)
- [x] **Run offer_caps_schema.sql in Supabase** ✅ (2026-02-17 01:30 GMT+4, Vision)
- [ ] Shield compliance check on stored leads
- [x] Map second form target (**NDR priority set by AK on 2026-02-16**) — `docs/NDR_FORM_MAP.md` published (2026-02-17)
- [ ] Proxy setup for scaled form filling
- [ ] Quality scoring logic implemented
- [ ] Everflow global postback configured to Ocean receiver + end-to-end test proof
- [ ] First CONFIRMED conversion (Everflow postback)

## Blockers
- Proxy provider not selected (~$20-50/mo)
- FastDebt API not yet integrated (enrichment gate still open)
- Vision/Kimi OpenRouter path intermittently falling back to Codex (connector reliability incident; mitigation active)
- Memory maintenance cron failed on Feb 16 with model access error (`gpt-5.3-codex` unavailable in that run) — retry policy and model fallback still pending
- Everflow global postback not yet configured to Ocean receiver endpoint (playbook completed; execution owner = Vision, AK execution assist required)
- Fury direct session key `agent:main:main` remains at historical `206,385` tokens on spark metadata; requires fresh/reset session key to eliminate overflow behavior risk
- Pipeline movement unchanged this sync (0 acquired / 0 delivered / $0 revenue / $0 spend)

## Latest Regulatory Intelligence (Fury)
- Run date: 2026-02-16 (manual trigger)
- Result: **No material regulatory change this week** for debt relief + personal loan cross-monetization scope (CFPB/FTC/FCC/CAN-SPAM + CA/NY/TX/FL scan)
- Action: Keep Copy Guardrails V1 active; no template or lexicon changes required today.

## Cron Jobs Active

| Job | Schedule | Purpose |
|---|---|---|
| Memory maintenance | 2:00 AM Dubai daily | Decay + promote memory observations |
| Weekly cap check | 9:00 AM IST Monday | Fury asks AK for offer caps |
| Regulatory intelligence weekly | Monday 10:30 Dubai | CFPB/FTC/FCC/CAN-SPAM/state update + Fury Action Pack |
| Regulatory follow-through | Monday 11:00 Dubai | Fury reviews, assigns owners, updates shared context |
| Login reliability heartbeat | Every 4h | Vision checks browser/auth health for Everflow/RevPie/FB + alerts |

## Agent Status Board
| Agent | Status | Last Active | Current Task |
|---|---|---|---|
| Fury 🎖️ | 🟢 Active | 2026-02-17 11:44 GST | Daily all-agent data sync (responsiveness/fallback scan + owner actions issued) |
| Peter 🛠️ | 🟢 Active | 2026-02-17 00:36 GST | Keep postback infra fallback path hot; execute fresh main session reset support if needed |
| Cap 🛡️ | 🟢 Active | 2026-02-16 15:48 GST | Execute compliance audit on 2 stored leads and publish pass/fail evidence |
| Hawkeye 🦅 | 🟢 Active | 2026-02-16 15:48 GST | Keep Copy Pack V1 launch-ready; prep channel variants pending Phase 3 gate |
| Widow 🔍 | 🟡 Standby | 2026-02-17 01:30 GST | NDR map done; next = post-submit behavior + phone-mask test protocol (no real lead burn) |
| Banner 🔥 | 🟡 Standby | 2026-02-16 15:48 GST | Finalize implementation-ready landing/offer-wall execution plan (no build pre-gate) |
| Vision 🗼 | 🟢 Active | 2026-02-16 23:55 GST | Execute Everflow global postback setup + E2E validation against Ocean endpoint |

## Handoff Queue
<!-- Format: [FROM] → [TO]: description (priority: high/medium/low) -->
- [FURY] → [VISION]: Configure Everflow global postback to Ocean endpoint, run signed test, and post proof bundle (URL used, request sample, DB row evidence) (priority: high)
- [FURY] → [PETER]: Maintain backup ownership for postback endpoint and run fallback deployment/debug immediately if Vision is blocked (priority: high)
- [FURY] → [CAP]: Complete compliance audit for 2 stored leads (TSR/TCPA/consent fields) and log disposition + remediation if any fail (priority: high)
- [FURY] → [WIDOW]: Add NDR post-submit behavior map + phone input mask constraints + safe test data plan (priority: high)
- [FURY] → [HAWKEYE]: Refresh channel-specific copy variants and compliance-safe creative matrix; hold launch until Phase 3 traffic gate (priority: medium)
- [FURY] → [BANNER]: Deliver page-block-level execution plan for high-converting site + offer wall linked to current buyer routing logic (priority: medium)
- [PETER] → [FURY]: Start/confirm fresh `main` session key to clear historical spark overflow metadata risk (priority: high)
- [FURY] → [FURY]: Publish daily sync status, explicitly noting no numeric movement unless new evidence lands today (priority: high)


- Security update (2026-02-16): POSTBACK_SECRET rotated. Fingerprint: 9Kn168...F6aE
