---
title: "Everflow Postback Pipeline Setup"
date: 2026-02-17
tags: [everflow, postback, conversion-tracking, supabase, vercel]
category: integration-issues
severity: critical
status: resolved
related_files:
  - db/offer_caps_schema.sql
  - api/postback.js
  - config/everflow_urls.json
  - scripts/fdr-ndr-fill.py
---

# Everflow Postback Pipeline Setup

## Problem

No infrastructure existed to receive Everflow conversion postbacks. When a form submission converted (buyer accepted the lead), Everflow had nowhere to fire its postback — meaning we couldn't track conversions, measure ROI, or enforce offer caps. Without this, the entire lead pipeline was flying blind.

## Investigation

Mapped out the full conversion lifecycle:

1. **Form fill** — Script submits lead to buyer's form via Everflow tracking URL
2. **Click registered** — Everflow logs the click with an `aff_click_id`
3. **Buyer converts** — Buyer accepts the lead, Everflow fires a postback to our endpoint
4. **We record** — Match postback to submission, update payout, mark lead delivered

Missing pieces: no endpoint to receive step 3, no tables to store offers/submissions/postbacks, no cap logic to prevent over-delivery.

## Root Cause

Greenfield gap — the initial `db/schema.sql` covered leads, buyers, campaigns, and deliveries, but had no concept of Everflow offers, form submissions, or postback tracking. The system was designed for direct buyer delivery, not affiliate network flows.

## Solution

### 1. Database Schema (`db/offer_caps_schema.sql`)

Three new tables + four RPC functions:

**`everflow_offers`** — Offer catalog with cap management:
- `offer_id` (Everflow's integer ID), buyer info, CPA, channel
- `weekly_cap` / `daily_cap` with running counters (`weekly_submissions`, `daily_submissions`, etc.)
- `cap_safety_pct` (default 0.80) — stops submitting at 80% of cap to prevent over-delivery while postbacks are pending
- `excluded_states`, `schedule`, `min/max_debt_amount` for targeting

**`offer_submissions`** — Every form fill attempt:
- Links `offer_id` to `lead_id`, tracks `everflow_click_id`
- Status: `submitted` → `converted` / `rejected` / `duplicate` / `expired`
- Stores postback data: `conversion_id`, `converted_at`, `payout`
- Dedup index: `UNIQUE(offer_id, lead_id) WHERE lead_id IS NOT NULL`

**`postback_log`** — Raw audit trail of every postback received:
- `source_ip`, `query_params`, `click_id`, `payout`
- `processed` boolean + `processed_at` timestamp

**RPC Functions:**

```sql
-- Check if we can submit (respects safety margin)
check_offer_cap(p_offer_id INTEGER)
  → RETURNS TABLE(can_submit BOOLEAN, reason TEXT, daily_remaining INTEGER, weekly_remaining INTEGER)

-- Increment submission counters after form fill
increment_submission(p_offer_id INTEGER)

-- Record conversion when postback fires (matches by click_id)
record_conversion(p_click_id TEXT, p_payout NUMERIC, p_conversion_id TEXT)

-- Cron functions
reset_daily_caps()   -- midnight EST
reset_weekly_caps()  -- Monday midnight EST
```

### 2. Vercel Endpoint (`api/postback.js`)

Serverless function that Everflow hits on conversion:

```
GET /api/postback?click_id=<aff_click_id>&offer_id=<id>&payout=<amount>&txn_id=<txn>&secret=<secret>
```

Flow:
1. Validate `POSTBACK_SECRET` (rejects unauthorized calls)
2. Log raw postback to `postback_log` (audit trail, even if matching fails)
3. Find submission by `everflow_click_id` where `status = 'submitted'`
4. Mark submission `converted` with payout and timestamp
5. Increment `daily_conversions` / `weekly_conversions` on `everflow_offers`
6. Mark lead status → `delivered`
7. Mark `postback_log` entry as `processed`

Health check: `GET /api/postback?health=1` returns `200 OK`.

### 3. Everflow Tracking URLs (`config/everflow_urls.json`)

10 offers seeded with tracking URLs:

| Offer ID | Buyer | CPA | Channel |
|----------|-------|-----|---------|
| 4930 | FDR | $60 | email |
| 4905 | NDR | $50 | web |
| 4836 | NDR | $45 | email |
| 4907 | CLIQ | $30 | web |
| 4906 | JGW | $25 | web |
| 4783 | NDR | $24 | web |
| 4633 | JGW | $24 | web |
| 4718 | JGW | $24 | call |
| 4737 | JGW | $22 | email |
| 4740 | NDR | $16 | email |

All URLs route through Everflow's redirect domain (`zkds923.com`) with our affiliate ID (`2MZN3ZS`).

### 4. Cap Management

Weekly caps set to 5 (testing phase). Safety margin at 80% means we stop at 4 submissions per offer per week. The `check_offer_cap()` RPC is called before every form fill in `scripts/fdr-ndr-fill.py`.

## Prevention

- All new offers get added to both `everflow_offers` table AND `config/everflow_urls.json`
- Form fill scripts always call `check_offer_cap()` before submitting
- Postback endpoint validates secret — no unauthenticated writes
- Raw `postback_log` provides audit trail even if matching logic changes

## Related

- [FDR/NDR Form Fill Automation](./fdr-ndr-form-fill-automation.md) — the script that generates submissions
- [Offer Submissions lead_id Nullable](../database-issues/offer-submissions-lead-id-nullable.md) — schema fix for test submissions
