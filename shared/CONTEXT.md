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
- **NDR Form Map revalidated (2026-02-18 01:49 GST):** `docs/NDR_FORM_MAP.md` updated from 2-step to confirmed 3-step flow: `/apply` → `/details` → `/personalizesavings`. Phone field auto-format confirmed (`(XXX) XXX-XXXX`), Step 2 submit confirmed as `POST /details?...` with redirect carrying `prospectId` + `ndrUID`.
- **NDR safe-submit guard shipped (2026-02-18 01:57 GST):** `scripts/fdr-ndr-fill.py` now supports `--safe-submit-probe` (NDR-only) with network-level interception that blocks live `POST /details` requests before prospect creation; regression matcher tests added in `tests/test_fdr_ndr_submit_guard.py`.
- **NDR safe-submit guard live-verified (2026-02-18 02:07 GST):** Runtime probe succeeded via direct NDR entry with proxy env vars blanked; command output captured blocked request `POST https://start.nationaldebtrelief.com/details?...` and returned safe success with screenshot `tmp/ndr-safeprobe-1771366020.png`.
- **NDR verification caveat (2026-02-18 02:07 GST):** Everflow+proxy verification path remained unstable in this run window (timeouts/variant rendering), so guard proof was established in deterministic direct-entry mode first.
- **Content Loop implementation shipped (2026-02-18 01:53 GST):** Dual-track content operations implemented in repo: `workflows/content-growth-loop.yaml`, `scripts/content-preflight-lint.py`, DB migration `db/migrations/003_content_growth_loop_tables.sql`, schema parity in `db/schema.sql`, and full skill pack under `skills/ocean-content-loop/`.
- **Dynamic HTML email templates shipped (2026-02-18 02:01 GST):** Added non-fixed, variable-driven templates (`templates/email-system/debt-relief-v2.dynamic.html`, `templates/email-system/personal-loan-cross-sell-v2.dynamic.html`) plus renderer script `scripts/render-email-template.py` and variable contract `templates/email-system/dynamic-template-vars.md`.
- **Model routing update (2026-02-17 00:36 GMT+4):** Fury switched from `openai-codex/gpt-5.3-codex-spark` to `openai-codex/gpt-5.3-codex` in live runtime config (`~/.openclaw/openclaw.json`) and template config (`config/openclaw.yaml`). Gateway restart executed via `openclaw gateway restart`.
- **Agent alignment hardening (2026-02-17):** Canonical agent IDs standardized (`fury/scout/shield/hawk/forge/watchtower/peter/ocean`) across repo configs and identity docs, stale `captain/signal` template references removed, and drift guard added at `scripts/validate_agent_alignment.sh` (runtime-aware `main` → `fury` normalization).
- **Budget Spent:** $0 / $5,000
- **Leads in DB:** 2 (1 dry run, 1 submitted to JGW) — unchanged since last sync
- **Revenue:** $0 — unchanged since last sync
- **Latest sync note (2026-02-19 11:30 GST):** Daily all-agent sync complete. No numeric data changes detected (leads acquired/delivered, revenue, spend all unchanged at 0/0/$0/$0).
- **Operating mode update (2026-02-19 22:32 GST):** AK directive enforced — Ocean runs in agency-first Chief of Staff mode (execute by default; ask only for spend, legal/compliance, irreversible external actions, or major priority tradeoffs).
- **Execution protocol update (2026-02-18 01:41 GST):** Immediate Execution Protocol activated. Significant tasks now require Task Packet in handoff queue + Execution Receipt in `shared/ACTION_LOG.md` (5-minute ack SLA, 30-minute first artifact SLA, proof-required closure).
- **SLA enforcement sweep (2026-02-18 01:49 GST):** Auto-reopen check run for task packets. No tasks had crossed `first_artifact_due` yet, so no reopen actions triggered in this sweep.

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
- **Tables staged (content loop):** content_assets, content_reviews, content_performance, content_learning_events — migration file committed, Supabase apply pending
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
- Content loop DB migration pending execution in Supabase (`003_content_growth_loop_tables.sql`), so workflow metrics queries are staged but not live yet.

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

## Task Packet Standard (Mandatory for Significant Tasks)

Use this packet format in the Handoff Queue. No significant task is "assigned" unless all fields are filled.

```
task_id:
from:
to:
task:
priority:
deadline:
first_artifact_due:
definition_of_done:
required_evidence:
escalate_if_blocked_by:
status: queued | active | blocked | done
```

## Agent Status Board
| Agent | Status | Last Active | Current Task |
|---|---|---|---|
| Fury 🎖️ | 🟢 Active | 2026-02-19 11:30 GST | Daily all-agent data sync (responsiveness/fallback scan complete; overdue owner actions re-issued) |
| Peter 🛠️ | 🟢 Active | 2026-02-17 00:36 GST | Keep postback infra fallback path hot; execute fresh main session reset support if needed |
| Cap 🛡️ | 🟢 Active | 2026-02-16 15:48 GST | Execute compliance audit on 2 stored leads and publish pass/fail evidence |
| Hawkeye 🦅 | 🟢 Active | 2026-02-16 15:48 GST | Keep Copy Pack V1 launch-ready; prep channel variants pending Phase 3 gate |
| Widow 🔍 | 🟡 Standby | 2026-02-17 01:30 GST | NDR map done; next = post-submit behavior + phone-mask test protocol (no real lead burn) |
| Banner 🔥 | 🟡 Standby | 2026-02-16 15:48 GST | Finalize implementation-ready landing/offer-wall execution plan (no build pre-gate) |
| Vision 🗼 | 🟢 Active | 2026-02-16 23:55 GST | Execute Everflow global postback setup + E2E validation against Ocean endpoint |
| Ocean 🌊 | 🟢 Active | 2026-02-18 02:07 GST | Live-verified NDR safe-submit guard in browser runtime; next step = apply migration 003 in Supabase |

## Handoff Queue
_Daily sync note (2026-02-19 11:30 GST): no new execution receipts logged after 2026-02-18 02:07 GST. Remaining queued items are past first-artifact SLA and require immediate owner recommit + fresh receipts or explicit blocker evidence._

| task_id | from | to | task | priority | deadline (GST) | first_artifact_due (GST) | definition_of_done | required_evidence | escalate_if_blocked_by (GST) | status |
|---|---|---|---|---|---|---|---|---|---|---|
| TP-20260218-000 | AK | OCEAN | Implement immediate execution protocol across shared operating docs | high | 2026-02-18 02:00 | 2026-02-18 01:55 | protocol codified in playbook/context/action-log/metrics with live pilot packet | docs diff bundle + context activation note + KPI panel | 2026-02-18 01:55 | done |
| TP-20260218-010 | OCEAN | OCEAN | Run SLA sweep and auto-reopen overdue tasks without blocker evidence | high | 2026-02-18 01:50 | 2026-02-18 01:49 | sweep completed and overdue tasks reopened if any | timestamped sweep note in context + queue status check | 2026-02-18 01:49 | done (no overdue tasks found) |
| TP-20260218-011 | AK | OCEAN | Implement Ocean dual-track content loop plan (workflow, schema, skill, guardrails) | high | 2026-02-18 03:00 | 2026-02-18 02:00 | repo includes executable workflow + lint + migration + interfaces docs + skill package | git diff bundle across `workflows/`, `scripts/`, `db/`, `skills/`, `docs/` + syntax smoke tests | 2026-02-18 02:00 | done (Supabase apply pending) |
| TP-20260218-013 | AK | OCEAN | Add non-fixed dynamic HTML email templates with reusable blocks and renderer utility | high | 2026-02-18 02:30 | 2026-02-18 02:10 | v2 HTML templates + variable contract + render script validated with strict smoke tests | template files + renderer script + render outputs with strict mode | 2026-02-18 02:10 | done |
| TP-20260218-001 | OCEAN | PETER | Pilot: validate NDR post-submit behavior + phone input mask handling without burning real lead | high | 2026-02-18 12:00 | 2026-02-18 02:10 | behavior map + mask rules added and linked in context | Playwright snapshot + network trace (`tmp_ndr_network.txt`) + `docs/NDR_FORM_MAP.md` update | 2026-02-18 02:10 | done (guard incident closed via TP-20260218-012) |
| TP-20260218-012 | AK | PETER | Implement route-level NDR test-safe submit guard in filler script to prevent prospect creation during submit-path validation | high | 2026-02-18 02:15 | 2026-02-18 02:00 | NDR test mode blocks `POST /details` at network layer and exposes explicit CLI flag with regression tests | script diff + guard matcher tests + local verification output | 2026-02-18 02:00 | done (live probe verified at 02:07 GST) |
| TP-20260218-002 | FURY | VISION | Configure Everflow global postback to Ocean endpoint and run signed test | high | 2026-02-18 13:00 | 2026-02-18 02:10 | signed postback reaches endpoint and DB log confirms | URL used, signed request sample, DB row proof | 2026-02-18 02:10 | queued |
| TP-20260218-003 | FURY | PETER | Maintain backup ownership for postback endpoint and execute fallback if Vision blocked | high | 2026-02-18 13:00 | 2026-02-18 02:10 | fallback path verified and deploy/debug support ready | health response + deployment/run output reference | 2026-02-18 02:10 | queued |
| TP-20260218-004 | FURY | CAP | Complete compliance audit on 2 stored leads (TSR/TCPA/consent fields) | high | 2026-02-18 15:00 | 2026-02-18 02:10 | both leads dispositioned pass/fail with remediation for failures | audit checklist output + lead-level disposition log | 2026-02-18 02:10 | queued |
| TP-20260218-005 | FURY | WIDOW | Extend NDR map with safe test data protocol and anti-detection behavior notes | high | 2026-02-18 14:00 | 2026-02-18 02:10 | NDR mapping doc updated with test-safe execution protocol | doc diff + section link + field/mask evidence | 2026-02-18 02:10 | queued |
| TP-20260218-006 | FURY | HAWKEYE | Refresh channel copy variants and compliance-safe creative matrix (hold launch gate) | medium | 2026-02-18 18:00 | 2026-02-18 02:10 | revised copy pack ready for Shield precheck | copy matrix doc + compliance notes | 2026-02-18 02:10 | queued |
| TP-20260218-007 | FURY | BANNER | Deliver implementation-ready page-block plan for high-converting site + offer wall | medium | 2026-02-18 18:00 | 2026-02-18 02:10 | page-block spec mapped to routing logic and handoff-ready | spec doc + block-level acceptance criteria | 2026-02-18 02:10 | queued |
| TP-20260218-008 | PETER | FURY | Start/confirm fresh `main` session key to clear spark overflow metadata risk | high | 2026-02-18 11:00 | 2026-02-18 02:10 | fresh session confirmed and old overflow risk explicitly closed or monitored | sessions output + explicit status note in context | 2026-02-18 02:10 | queued |
| TP-20260218-009 | FURY | FURY | Publish daily sync status with explicit "no numeric movement" unless evidence changes | high | 2026-02-18 12:00 | 2026-02-18 02:10 | sync note published in context with evidence source timestamp | sync note + evidence timestamp reference | 2026-02-18 02:10 | queued |

## Owner Actions — 2026-02-19 (Execution-Focused)
- **Fury:** Run overdue-task triage now; reissue TP-002..TP-009 with new first-artifact SLAs and escalate non-responders within 30 minutes.
- **Peter:** Post fallback readiness proof for postback path + update on fresh `main` session reset closure (TP-003, TP-008).
- **Cap:** Deliver compliance audit evidence for the 2 stored leads or file blocker with timestamped dependency.
- **Widow:** Publish NDR safe-test protocol extension (mask + anti-detection notes) into `docs/NDR_FORM_MAP.md` with proof links.
- **Hawkeye:** Submit refreshed compliant copy matrix and route to Shield precheck queue.
- **Banner:** Deliver implementation-ready page-block spec for high-converting site + offer wall handoff.
- **Vision:** Complete Everflow global postback config + signed E2E test to Ocean endpoint with DB-row proof.

- Security update (2026-02-16): POSTBACK_SECRET rotated. Fingerprint: 9Kn168...F6aE

## Handoff Note — AK (2026-02-21 15:03 +04) — Overnight Launch Kit
- Productized digital asset completed at `products/overnight-launch-kit/` with offer doc, usage README, license, hero SVG, and 3 operator-ready templates/checklists.
- Sales storefront completed at `storefront/overnight-launch-kit/` (static HTML/CSS/JS) with concise copy, features, FAQ, and CTA.
- Deployment attempt executed via `npx vercel --prod storefront/overnight-launch-kit --yes`; blocked by Vercel **402 overdue billing** on team `arifs-projects-aacf12b1`.
- True blockers + exact recovery commands documented in `LAUNCH_ACTION_ITEMS.md`.
- Morning execution path documented in `LAUNCH_CHECKLIST.md` (<20 min flow).
- Recommended pricing: **$79 intro / $129 standard** (also logged in `STATUS_SUMMARY.md`).
