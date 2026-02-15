# Buyer's Playbook — Project Ocean

_The operating manual for buyer relationships, offer management, lead routing, and cap tracking._
_Updated: Feb 15, 2026 — with live Everflow data_

---

## Our Buyer Stack (Live in Everflow/RevvMind)

We operate as a **Partner/Affiliate** on RevvMind's Everflow instance. All offers are pre-approved, all US-only. Account manager: Zakir Khan (zakir@zappian.com).

### Debt Relief Offers (Our Core Business)

| ID | Buyer | Offer | CPA | Channel | Days | States Excl. | Cap Status |
|---|---|---|---|---|---|---|---|
| 4930 | **FDR** | Freedom Debt Relief - Email only M-F | **$60** | Email | M-F | ❓ | Ask for Cap |
| 4905 | **NDR** | National Debt Relief - W | **$50** | Web | ❓ | ❓ | ❓ |
| 4836 | **NDR** | NDR (Mon-Fri) Private-CPL (Budgeted) | **$45** | Email | M-F | ❓ | Budgeted |
| 4907 | **Cliqsilver** | Credit Card Debt Cpl-sq | **$30** | Web | ❓ | ❓ | ❓ |
| 4906 | **JGW** | JG Wentworth (nc-21805786) | **$25** | Web | ❓ | ❓ | ❓ |
| 4783 | **NDR** | NDR -SQ | **$24** | Email | ❓ | ❓ | ❓ |
| 4718 | **JGW** | JGW Debt Settlement [MKP] | **$24** | Email | ❓ | ❓ | ❓ |
| 4633 | **JGW** | JGW CPL weekends (NO CA) | **$24** | Email | 7 days | **CA** | ❓ |
| 4737 | **JGW** | JGW Debt Settlement M-F {US} | **$22** | Email | M-F | ❓ | ❓ |
| 4740 | **NDR** | NDR Email Only (Budgeted) | **$16** | Email | ❓ | ❓ | Budgeted |

### Loan Offers (Zappian Legacy — CPS 100% Rev Share)

| ID | Name | Category | Payout | Channel |
|---|---|---|---|---|
| 3228 | Maxloanusa.com_ZM_025_PUB | Personal Loan | CPS 100% | Email+SMS |
| 2884 | Rapidfundonline.com | Payday Loan | CPS 100% | Email |
| 2256 | 1stlendingusa.com_ZM_025 | Personal Loan | CPS 100% | Email |
| 1901 | eloantoday.com_ZM_025 | Personal Loan | CPS 100% | Email+SMS |
| 176 | Brighterloan.com_ZM_025 | Personal Loan | CPS 100% | Email |

---

## How We Make Money — The Lead Flow

```
Lead Source (RevPie / FB / Own Sites)
        ↓
  Our Website / Landing Page
        ↓
  FastDebt API (enrich: debt type, amount, composition)
        ↓
  Quality Filter (unsecured debt? CC primary? $10K+?)
        ↓
  Route to Best Offer (highest CPA where lead qualifies)
        ↓
  Scout Form Filler (fill buyer's form with qualified lead)
        ↓
  Advertiser checks (dedup + quality on THEIR end)
        ↓
  Everflow pixel fires → POSTBACK → Revenue confirmed
```

---

## ⚠️ Cap Management — THE Critical Business Logic

### Submissions vs Conversions

**A form fill is NOT revenue. A postback is.**

```
Form Fill (Submission) → Buyer checks → Accept/Reject → Pixel fires (Conversion)
```

- **Submission** = we filled their form (our count)
- **Conversion** = Everflow postback received (buyer accepted, counts toward cap, generates revenue)
- **Not every submission converts** — buyers check for duplicates, quality, state eligibility
- **Postbacks can be delayed** — sometimes hours, sometimes next business day

### Cap Rules

| Rule | Detail |
|---|---|
| Cap counts | **Confirmed conversions** (postbacks), NOT submissions |
| Safety buffer | Stop submitting at **1.5x cap** (prevents overfilling while postbacks pending) |
| Daily reset | Midnight ET |
| Weekly reset | Monday midnight ET |
| Weekly update | **AK provides caps every Monday** (cron reminder at 9AM IST) |
| Over-cap | If conversions hit cap → immediately pause submissions for that offer |

### Cap Check Before Every Fill

Before Scout fills ANY form, check `can_submit_to_offer()`:
1. Is offer status = 'active'?
2. Is today an allowed day for this offer?
3. Are daily conversions < daily cap?
4. Are daily submissions < daily cap × 1.5?
5. Are weekly conversions < weekly cap?
6. Is lead's state NOT in excluded_states?
7. Does lead meet min_debt_amount?
8. Is lead within freshness window?
9. Has this lead been sent to this buyer within dedup_window_days?

ALL must pass. If any fail → route to next eligible offer.

### Database

- **Schema:** `db/offer_caps_schema.sql`
- **Tables:** `offer_caps` (per-offer caps + counters), `offer_submissions` (every fill + postback)
- **Functions:** `can_submit_to_offer()`, `record_submission()`, `record_postback()`

---

## Lead Routing Logic

### Priority Order (highest value first)

1. **FDR $60** (email, M-F, ask for cap) — if qualified and under cap
2. **NDR $50** (web) — if web-sourced and under cap
3. **NDR $45** (email, M-F, budgeted) — if email-sourced and under cap
4. **Cliqsilver $30** (web) — if web-sourced and under cap
5. **JGW $25** (web) — if web-sourced and under cap
6. **NDR $24** (email) — fallback email tier
7. **JGW $24 MKP** (email) — marketplace fallback
8. **JGW $24 weekends** (email, no CA) — weekend + non-CA leads
9. **JGW $22** (email, M-F) — lowest JGW tier
10. **NDR $16** (email, budgeted) — absolute last resort

### Routing Rules

- **Channel match required:** Email-sourced leads → email offers only. Web-sourced → web offers only.
- **State check:** Never send a CA lead to offer 4633 (NO CA).
- **Day check:** Don't submit to M-F offers on weekends.
- **Dedup:** Check `offer_submissions` — has this lead (by email+phone) been sent to this buyer in the last 90 days?
- **Cascade:** If top offer is capped/restricted, try next. If ALL offers exhausted → queue for next day.
- **Queue aging:** Lead undelivered > 48h → flag for Captain review.

### Quality Matching (Post-FastDebt Enrichment)

| Lead Profile | Best Offer | Why |
|---|---|---|
| $30K+ CC debt, verified | FDR $60 | Highest CPA, strict quality |
| $15-30K CC debt | NDR $50 or $45 | Good mid-tier match |
| $10-15K CC debt | JGW $25 or Cliqsilver $30 | Lower threshold buyers |
| Mixed debt (some secured) | NDR $24 or JGW $22 | Lenient on composition |
| Under $10K unsecured | Likely reject — don't submit | Below most buyer minimums |

---

## RevPie ↔ Everflow Traffic Optimization Loop

When buying traffic from RevPie to generate web leads:

```
RevPie Source ID → sends traffic → our landing page → Everflow tracks
                                                           ↓
                                              Performance per Source ID
                                                           ↓
                        Back to RevPie: whitelist winners, blacklist losers, adjust bids
```

### RevPie Account
- **Login:** vishal@revvmind.com
- **Balance:** $481.57
- **7 campaigns** (all paused, Zappian era)
- **Key campaign:** Debt_Campaign ($220/day budget, NDR + Cliqsilver ads)
- **Bid range:** $0.10 - $7.00 CPC
- **Controls:** Whitelist/Blacklist per campaign+ad, custom bid per Source ID

### Optimization Workflow (Hawk's job in Phase 3)
1. Enable campaign with conservative budget ($20-50/day)
2. Let it run 3-5 days, collect Source ID data
3. Pull Everflow report: which Source IDs generated conversions?
4. In RevPie: whitelist top Source IDs, raise bids. Blacklist zero-converters.
5. Repeat weekly. Kill sources with CPA > 2x target.

---

## Everflow Platform Reference

- **URL:** revvmind.everflowclient.io
- **Login:** arif@revvmind.com (Partner/Affiliate view)
- **Account Manager:** Zakir Khan (zakir@zappian.com)

### Navigation
| Icon | Section | URL |
|---|---|---|
| 🖥️ | Dashboard (My Stats) | / |
| 🔍 | Search (offers, transactions) | - |
| 🔗 | Tracking & Asset Generator | - |
| 📦 | Offers → Manage | /offers |
| 🔔 | Notifications | - |
| 👤 | Profile / My Account | - |

### Key Dashboard Metrics
- **Last Month (Jan 2026):** 310 clicks, 6 conversions, $24 revenue, 1.94% CVR
- **This Month (Feb 2026):** 0 (no active campaigns)
- **Last confirmed conversion:** FDR offer 4930 on Jan 28, 2026

### Offer Detail Page Contains
- General (ID, name, category)
- Caps (daily/weekly/monthly/global — usually empty, managed externally)
- Email Instructions (from-lines, subject lines, suppression URL, unsub URL)
- Payout (base CPA, tiers if any)
- Targeting (country inclusions/exclusions)
- Creatives (HTML email templates, downloadable)
- URLs (offer landing pages)
- Stats + View Report link

### Important: SPA Navigation
- Everflow is an Angular SPA — direct URL navigation often shows blank "Network" page
- Must navigate via sidebar clicks from root
- Offer detail pages only load when clicked from /offers list

---

## FDR Offer Detail (Verified Feb 15, 2026)

**Offer 4930 — Freedom Debt Relief - Email only - M-F Drops Only - Ask for Cap**

- **CPA:** $60 (Base, no tiers)
- **Caps in Everflow:** None set (managed externally)
- **Targeting:** US only
- **Creatives:** 2 HTML email templates
  - Cr1: "A smart program to help Americans get rid of debt"
  - Cr3: "You could be eligible for this debt solution"
- **100+ Subject Lines** provided (debt relief themed, includes economic anxiety angles)
- **From Lines:** Multiple variations (Debt_Relief, Partner, Associate, Freedom Debt Relief_Ad, etc.)
- **Suppression + Unsub URLs:** Provided in Everflow
- **FDR Address:** Freedom Debt Relief, LLC | 1875 South Grant Street, Suite 400, San Mateo, CA 94402

---

## Finding New Buyers

### Where to Look
1. **Everflow marketplace** — check for new offers periodically
2. **Affiliate networks** — ClickDealer, MaxBounty, Perform[cb]
3. **Direct outreach** — debt relief companies, credit counseling agencies
4. **LinkedIn** — "debt relief buyer", "lead buyer debt settlement"
5. **Industry events** — LeadsCon, Affiliate Summit
6. **RevPie/LeadPoint** — marketplace platforms

### Ideal Buyer Profile
- Licensed debt relief / settlement company
- Active in 10+ states
- Daily cap of 25-100 leads
- Payout $40-100 per exclusive lead
- Net-15 or faster payment terms
- Responsive to delivery

---

## Onboarding a New Buyer

### Step 1: AK initiates relationship
- AK handles all external buyer communication
- Captain receives terms: cap, payout, states, restrictions

### Step 2: Captain configures
- Add to `offer_caps` table
- Set routing priority based on CPA
- Configure in OFFER_CAPS.md

### Step 3: Test Batch
- Start with 5-10 test leads
- Track submission → postback conversion rate
- Adjust quality criteria based on acceptance rate

### Step 4: Scale
- Increase volume gradually
- Monitor conversion rate (target: >50% of submissions convert)
- If conversion rate < 30%, review lead quality or pause offer

---

## Payout Negotiation (AK handles, Captain advises)

### What Affects Payout
| Factor | Higher Payout | Lower Payout |
|---|---|---|
| Lead freshness | Real-time | Aged (30+ days) |
| Exclusivity | Exclusive | Shared |
| Verification | Fully verified + enriched | Self-reported |
| Debt amount | $25K+ | Under $10K |
| Debt type | 80%+ credit card | Mixed/mortgage |
| State | CA, TX, FL, NY | Low-pop states |
| Delivery method | Live transfer (call) | Email/form only |

### Current Payout Range
- **Highest:** FDR $60 (email, M-F, capped)
- **Mid-tier:** NDR $45-50, Cliqsilver $30
- **Base:** JGW $22-25, NDR $16-24

---

## Handling Rejections

When a submission doesn't get a postback (no pixel fire):

### Common Rejection Reasons
- **Duplicate** — buyer already has this lead
- **Bad data** — phone disconnected, email invalid
- **Wrong state** — lead's state not covered by buyer
- **Below threshold** — debt amount too low
- **Wrong debt type** — secured debt, not credit card

### Monitoring
| Conversion Rate | Action |
|---|---|
| > 60% | Excellent — increase volume |
| 40-60% | Normal — monitor |
| 25-40% | Warning — review lead quality, check enrichment |
| < 25% | Problem — pause, investigate, may need to stop source |

### Process
1. Track submission → postback ratio per offer per week
2. If ratio drops below 40%, Captain investigates
3. Check: Is it a source quality issue? Enrichment gap? State mismatch?
4. Adjust routing or pause problematic source

---

## Weekly Operating Rhythm

### Monday (Cap Day)
- **9:00 AM IST:** Cron fires → Captain asks AK for this week's caps
- AK provides: daily caps, weekly caps, state changes, new offers
- Captain updates `offer_caps` table + OFFER_CAPS.md
- Captain reviews last week's conversion rates per offer

### Daily
- Check daily submission vs conversion counts per offer
- If any offer approaching cap → adjust routing priority
- If postbacks delayed > 24h → flag for AK

### Friday
- Week-end review: total submissions, conversions, revenue, conversion rate
- Prepare Monday cap request with data

---

_This playbook is the operating manual. Every agent who touches lead routing reads this. When in doubt, check here first._
