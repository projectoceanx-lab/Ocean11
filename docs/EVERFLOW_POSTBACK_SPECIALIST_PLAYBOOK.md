# EVERFLOW POSTBACK SPECIALIST PLAYBOOK (Vision)

_Last verified: 2026-02-16 (GMT+4), inside `revvmind.everflowclient.io` with current Partner/Affiliate credentials._

## Evidence Basis (what was actually observed)

This playbook is based on direct UI navigation and page-content extraction from the logged-in account. Key verified pages:

- `/` → Dashboard (“My Stats”)
- `/offers` → Manage Offers (15 offers visible)
- `/offers/4906` → Offer Details (sample debt offer)
- `/smartlinks` → Manage Smart Links (0 records)
- `/postbacks?tab=conversions` / `?tab=events` / `?tab=cpc` → Manage Postbacks
- `/postbacks/add?type=conversion` → Add Postback form
- `/reporting/offers` → Offer Report
- `/analytics/dimensional` → Dimensional Report
- Invalid/admin-like routes tested (`/affiliates`, `/advertisers`, `/company-settings`) redirected to `/404`

---

## 1) Navigation Map (step-by-step)

## A. Primary left nav (expanded menu)
From any page, open the left hamburger to reveal labeled sections:

1. **Dashboard** (`/`)
2. **Manage**
   - **Offers** (`/offers`)
   - **Smart Links** (`/smartlinks`)
   - **Postbacks** (`/postbacks`)
3. **Analyze**
   - **Reporting** (`/reporting/offers` default)
   - **Analytics** (`/analytics/dimensional` default)
4. **Tools**
   - **Tracking & Asset Generator** (embedded tool panel + menu entry)
5. **More**
   - **Company Settings** (flyout panel, not direct route)

## B. Postbacks flow (core)

1. Go to **Manage → Postbacks** (`/postbacks`)
2. Tabs available at top:
   - **Conversions** (`?tab=conversions`)
   - **Events** (`?tab=events`)
   - **CPC** (`?tab=cpc`)
3. Click **Postback** button to create one
4. Lands on: `/postbacks/add?type=conversion` (or respective type)
5. Required fields shown:
   - Status (Active/Inactive)
   - Postback Type (Conversion/Event/CPC)
   - Postback Level (Global/Specific)
   - If Specific selected: **Offer*** selector appears
   - Delivery Method (required)
6. Submit via **Add**

## C. Offer-level flow

1. Go to **Manage → Offers** (`/offers`)
2. Click any offer row/name (e.g., `4906`) → `/offers/{id}`
3. On offer details page:
   - General details, caps, payout, targeting, creatives, URLs
   - **Offer Tracking Links** button
4. Open **Offer Tracking Links** tool panel
5. Generate tracking link(s) and copy final URL

Example observed generated link (Offer 4906):

- `https://www.zkds923.com/2MZN3ZS/9N9X3MM/`

---

## 2) Postback Setup Matrix (availability by scope)

| Scope | In current affiliate account? | Where found | What can be done | Limitation observed |
|---|---|---|---|---|
| Global postback | **Yes** | `/postbacks/add?type=conversion` with Level=Global | Create active/inactive postback for Conversion/Event/CPC | No network-wide admin controls exposed |
| Per-offer postback | **Yes** | same add form with Level=Specific → Offer selector | Target postback to a specific offer | Offer selector only; no advertiser/affiliate object selector shown |
| Per-affiliate postback (as network admin assigning to partners) | **No evidence of access** | Not present in add form or menus | N/A | No `/affiliates` area; direct route tests go 404 |
| Network-level defaults/policies (admin settings) | **No evidence of access** | No admin settings area visible | N/A | Company Settings appears partner-side account panel only |
| Offer tracking links (click-side setup) | **Yes** | Offer Details → Offer Tracking Links | Generate/copy click URL for traffic source | No deep admin override controls shown |
| Smart Link postback mapping | **Partially** | `/smartlinks` exists but no records currently | Could configure if Smart Links exist | No active smart links in account now |

### Practical conclusion
With current credentials, Vision/AK can configure **global** and **offer-specific** postbacks for this affiliate account, but cannot access network-admin entities (affiliates/advertisers/global platform controls).

---

## 3) Exact Implementation Checklist for AK

## Pre-check (2 minutes)
- [ ] Confirm Ocean receiver endpoint is live (e.g., `https://ocean11-postback.vercel.app` health OK)
- [ ] Confirm endpoint supports GET (query params) and logs raw payload
- [ ] Confirm dedup key strategy in DB (recommend: `transaction_id` or `sub1+offer_id+timestamp window` fallback)

## Step 1 — Build canonical click links (offer-side)
- [ ] Open `/offers`
- [ ] Open target offer (e.g., 4905/4906/4930)
- [ ] Click **Offer Tracking Links**
- [ ] Generate link and copy
- [ ] Add your tracking params at source side (RevPie/ad URLs) consistently

**Recommended pass-through params** (keep naming consistent across stack):
- `sub1` = internal lead/session id
- `sub2` = source id / placement id
- `sub3` = campaign id
- `sub4` = adset/adgroup id
- `sub5` = creative id

## Step 2 — Configure global conversion postback
- [ ] Open `/postbacks?tab=conversions`
- [ ] Click **Postback**
- [ ] Set:
  - Status = Active
  - Type = Conversion
  - Level = Global
  - Delivery Method = URL/S2S (choose URL callback mode)
- [ ] Enter Ocean endpoint URL with expected tokens/params
- [ ] Save (**Add**)

## Step 3 — Configure offer-specific overrides (only where needed)
Use only when one buyer/offer needs custom mapping.
- [ ] In same screen, new postback
- [ ] Level = Specific
- [ ] Select offer
- [ ] Keep mapping compatible with global schema
- [ ] Save

## Step 4 — Configure Events/CPC if operationally required
- [ ] `/postbacks?tab=events` add event postback (optional)
- [ ] `/postbacks?tab=cpc` add cpc postback (optional)
- [ ] Only enable if downstream system can process them cleanly

## Step 5 — End-to-end validation (must do)
- [ ] Fire test click through generated tracking link
- [ ] Trigger a conversion/event test path (or wait for first live)
- [ ] Verify Everflow postback row appears active and no errors
- [ ] Verify Ocean endpoint logs hit with expected params
- [ ] Verify Supabase row inserted/updated exactly once
- [ ] Verify revenue attribution and offer mapping in internal dashboard

## Step 6 — Lock-in operations
- [ ] Document exact live postback URL(s) in `shared/CONTEXT.md`
- [ ] Keep one source-of-truth mapping table for param names
- [ ] Add alerting for postback drop-off (>30 min no hits during active traffic)

---

## 4) Troubleshooting Playbook

## A. No postbacks arriving at Ocean endpoint
1. Check Everflow postback exists and is **Active**
2. Confirm correct tab/type (Conversion vs Event vs CPC)
3. Confirm scope conflict:
   - If specific offer postback exists, ensure it is not misconfigured vs global
4. Check endpoint URL typo / HTTPS cert / 4xx/5xx
5. Inspect endpoint server logs for blocked requests/timeouts

## B. Clicks present but zero conversions in reporting
1. Validate tracking link used in traffic source is the newest generated one
2. Confirm offer is approved/active and country/rules match traffic
3. Check offer restrictions (e.g., email-only, weekday-only notes in offer name/details)
4. Inspect conversion delay expectation (some buyers approve later)

## C. Duplicate conversion handling issues
1. Ensure dedup key uses network transaction/click identifier where possible
2. Enforce idempotent write at API layer
3. Store raw payload for replay/debug

## D. Wrong offer attribution
1. Ensure postback payload includes offer ID/name params
2. Ensure click link uses consistent sub param convention
3. Compare Everflow Offer Report (`/reporting/offers`) against DB records

## E. Can’t find admin controls others mention
Expected with current role. Evidence:
- Menu is Partner Platform (offers/smartlinks/postbacks/reporting/analytics)
- Direct admin-ish routes (`/affiliates`, `/advertisers`) returned 404

Escalate to network admin for:
- Affiliate management
- Advertiser management
- Network-wide permission/policy changes

---

## 5) 10-Question Self-Test (Vision) + Answers

1. **Q:** Where do you create conversion postbacks?
   **A:** `Manage → Postbacks → Conversions`, then click **Postback**.

2. **Q:** What two scope levels are visible for postbacks in this account?
   **A:** **Global** and **Specific (Offer)**.

3. **Q:** What appears when Postback Level = Specific?
   **A:** Mandatory **Offer** selector.

4. **Q:** Can this account configure partner-wide affiliate objects like `/affiliates`?
   **A:** No evidence; tested routes return `/404`.

5. **Q:** Where do you get an offer tracking link to place in RevPie/ad URLs?
   **A:** Offer detail page (`/offers/{id}`) → **Offer Tracking Links**.

6. **Q:** Name three postback types visible.
   **A:** Conversion, Event, CPC.

7. **Q:** Which two reporting pages help diagnose missing conversions?
   **A:** `/reporting/offers` and `/analytics/dimensional`.

8. **Q:** If global postback exists but one offer needs custom mapping, what do you do?
   **A:** Add a **Specific** postback for that offer and keep mapping schema compatible.

9. **Q:** What is the minimum reliable E2E validation?
   **A:** Click test + conversion trigger + endpoint hit + deduped DB write + report cross-check.

10. **Q:** What is the fastest indicator that role is partner/affiliate not network admin?
    **A:** Left nav scope (Offers/Smart Links/Postbacks/Reporting/Analytics) plus admin routes not accessible.

---

## Operational Notes for AK

- Start with **one global conversion S2S postback** to reduce complexity.
- Add offer-specific postbacks only for exceptions.
- Keep a strict parameter contract between Everflow payload and Ocean ingest schema.
- Treat Events/CPC as optional until conversion pipeline is stable.

