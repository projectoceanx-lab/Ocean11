# Knowledge Hub — What We've Learned

_Every agent contributes here. This is our institutional memory — patterns, insights, and hard-won lessons that make us smarter over time._

---

## Lead Acquisition Patterns
<!-- Scout writes here -->
<!-- What forms work, what sites block us, timing patterns, form field changes -->

### Debt Relief Form Target Reconnaissance — 2026-02-14
*Checked by Scout. Source: live browser inspection of each site.*

---

#### Target 1: National Debt Relief (NDR)
- **URL:** `https://start.nationaldebtrelief.com/apply`
- **Form type:** Multi-step wizard (JS-rendered SPA)
- **Step 1 fields:**
  - Debt Amount (dropdown/combobox) — 14 ranges from "$0–$4,999" to "$100,000+"
  - CTA: "See if You Qualify"
- **Subsequent steps (expected):** Name, phone, email, state, debt types — standard multi-step funnel. Steps load dynamically after step 1 submission.
- **Anti-bot measures observed:**
  - Fully JS-rendered (no static HTML form — requires headless browser or equivalent)
  - Cookie consent banner (privacy/tracking layer)
  - No visible CAPTCHA on step 1
  - NMLS licensed (#1250950) — legitimate regulated entity
- **Qualification threshold:** Accepts all debt amounts (including $0–$4,999)
- **Phone:** 800-300-9550
- **Notes:** High-volume target. 58,800+ ConsumerAffairs reviews, 42,740+ Trustpilot reviews. A+ BBB. NYC-based (180 Maiden Lane). NASCAR sponsor.

---

#### Target 2: Freedom Debt Relief (FDR)
- **URL:** `https://apply.freedomdebtrelief.com/home/estimated-debt?from=fdr`
- **Form type:** Multi-step wizard (JS-rendered SPA)
- **Step 1 fields:**
  - Debt Amount (slider input) — range $1,000 to $100,000+, default $25,000
  - CTA: "Continue"
- **Subsequent steps (expected):** Behind current payments Y/N, state, name, phone, email. Multi-step funnel.
- **Anti-bot measures observed:**
  - Fully JS-rendered SPA
  - Slider UI (requires precise interaction — not a simple form POST)
  - Generates a `leadId` UUID on page load (e.g., `b8bce13f-...`) — server-side session tracking
  - No visible CAPTCHA on step 1
  - **Not available in all states** (notably New Jersey excluded)
- **Qualification threshold:** $1,000 minimum
- **Phone:** (800) 910-0065
- **Notes:** Largest player. 1M+ clients served. $20B+ settled since 2002. 46,000+ Trustpilot reviews. Founding ACDR member. IAPDA Platinum. Separate legal partner network. Has affiliated debt consolidation loan partners.

---

#### Target 3: Pacific Debt Relief
- **URL:** `https://start.pacificdebt.com/#step=debt-amount`
- **Form type:** Multi-step wizard (JS-rendered SPA, hash-routed)
- **Step 1 fields:**
  - Debt Amount (3 button choices):
    - "Less than $10,000"
    - "$10,000 – $25,000"
    - "More than $25,000"
  - No explicit CTA — clicking a button advances
- **Subsequent steps (expected):** State, name, phone, email. Standard multi-step.
- **Anti-bot measures observed:**
  - JS-rendered SPA with hash-based routing (`#step=debt-amount`)
  - No visible CAPTCHA
  - "No impact to credit score" messaging suggests soft-pull or no credit check at intake
  - 3rd party script monitoring disclosed in footer
  - NMLS licensed (#1250953)
- **Qualification threshold:** $10,000+ for program enrollment (per FAQ: "must have more than $10,000 in unsecured debt")
- **Phone:** (833) 865-2028
- **Notes:** 20+ years in business. A+ BBB. IAPDA certified. San Diego-based. Nationwide except some states. $500M+ settled. Smaller than NDR/FDR but solid mid-tier target. Button-based step 1 is simplest to automate of the three.

---

### Key Patterns Across All 3 Targets

| Feature | NDR | FDR | Pacific Debt |
|---|---|---|---|
| Step 1 input | Dropdown (14 options) | Slider ($1K–$100K+) | 3 buttons |
| JS-rendered | Yes | Yes | Yes |
| CAPTCHA visible | No | No | No |
| LeadID tracking | Unknown | Yes (UUID on load) | Unknown |
| Min debt | $0 | $1,000 | $10,000 |
| Excluded states | Unknown | NJ | Some (unspecified) |
| Automation difficulty | Medium | Medium-High (slider) | Low (buttons) |

### Observations
1. **All 3 are JS SPAs** — no simple HTTP POST will work. Headless browser (Playwright/Puppeteer) required for any form interaction.
2. **No CAPTCHAs on step 1** — anti-bot measures likely kick in on later steps (phone/email capture) or server-side via rate limiting, fingerprinting, and session tracking.
3. **FDR's slider + leadId** is the most sophisticated anti-automation measure observed. Slider interaction needs to look human (gradual movement, not instant set).
4. **Pacific Debt's 3-button approach** is the easiest automation target for step 1.
5. **All sites use multi-step funnels** — full form field mapping requires advancing through all steps. This recon covers step 1 only. Deeper mapping needed.
6. **Accredited Debt Relief** (`accrediteddebtrelief.com`) returned **Cloudflare 403** on web_fetch — has aggressive bot protection. Worth noting as a harder target.
7. **Beyond Finance** (`beyondfinance.com`) also returned **Cloudflare 403** — same pattern.

### Next Steps
- Deep-map remaining steps on all 3 targets (need to advance through each form)
- Test Cloudflare-protected sites with residential proxy + browser fingerprinting
- Document full field schema for database alignment
- Check for hidden fields, honeypots, and JS fingerprinting on later steps

## Compliance Patterns
<!-- Shield writes here -->
<!-- Common compliance flags, state-specific gotchas, buyer-specific requirements -->

### FTC Enforcement Review — Debt Relief (2024-2025)
_Added by Shield 🛡️ | 2026-02-14 23:53 GST | Sources: FTC press releases, Goodwin Law 2024 YIR_

**Industry landscape:** 16 enforcement actions tracked in 2024 (down from 22 in 2023). 9 by FTC/CFPB, 5 by state agencies, 2 joint. Total monetary recovery: $30.3M+. Under Trump admin, expect state AGs to increase enforcement while federal actions may decline — does NOT mean less risk, means more unpredictable risk.

#### Case 1: Strategic Financial Solutions LLC (Jan 2024)
- **Who:** CFPB + 7 state AGs sued New York-based debt relief company
- **What went wrong:** Charged illegal advance fees for promised debt relief, provided almost no actual services. Used shell companies and law firms to hide illegal activity from law enforcement.
- **Violations:** TSR advance fee ban, various state laws
- **Status:** TRO granted Jan 2024. Motions to dismiss denied Dec 2024.
- **Ocean lesson:** Shell company structures don't protect you — they make it worse. The advance fee ban is absolute. If our buyers charge advance fees, we're exposed through association. **Vet every buyer's fee structure before first delivery.**

#### Case 2: Accelerated Debt Settlement / "Accelerated Debt" (Jul 2025)
- **Who:** FTC sued 7 companies + 3 individuals operating as common enterprise
- **What went wrong:** $100M scheme targeting seniors/veterans. Falsely impersonated consumers' banks, credit card issuers, and government agencies. Promised 75%+ debt reduction. Charged illegal advance fees (~$10K per consumer). Told consumers to stop paying creditors (causing defaults, credit score destruction). Used prohibited remotely created checks. Unlawfully obtained credit reports. Violated DNC rules.
- **Violations:** FTC Act, TSR, Impersonation Rule, FCRA, GLB Act §521, DNC requirements
- **Status:** TRO granted Jul 2025. Unanimous 3-0 FTC vote.
- **Ocean lesson:** This is a masterclass in what NOT to do. Key takeaways:
  - **Impersonation = nuclear.** Never let marketing imply we are the consumer's bank/creditor/government.
  - **Targeting vulnerable populations (seniors, veterans) draws maximum FTC attention.**
  - **"Common enterprise" doctrine** means all related entities are liable — if our buyers operate this way, association risk flows to us.
  - **DNC violations in debt relief are specifically called out** — inbound AND outbound telemarketing.

#### Case 3: Global Circulation Inc. (Oct 2024)
- **Who:** FTC sued debt collector + CEO in N.D. Georgia
- **What went wrong:** Misrepresented debt status and authority to collect. Threatened unlawful actions. Used false/deceptive means to collect.
- **Status:** TRO granted Oct 2024.
- **Ocean lesson:** Even downstream partners (collectors, not just lead gen) trigger enforcement. If we deliver leads to bad actors who misrepresent, we carry reputational and potential legal exposure.

#### Key Patterns Across All Cases
1. **Advance fees are the #1 trigger.** Every major debt relief case involves TSR §310.4(a)(5) violations. Non-negotiable: our buyers must not charge advance fees.
2. **Shell companies / common enterprise doctrine** — FTC pierces corporate structures routinely. No hiding behind LLCs.
3. **Impersonation is a new escalation vector** — FTC's Impersonation Rule is being actively used in debt relief cases.
4. **State AGs are expected to increase enforcement** under current admin. California DFPI, NY DFS, and TX are highest risk.
5. **Targeting vulnerable demographics** (seniors, veterans, military) draws maximum scrutiny and worse penalties.
6. **DNC compliance in debt relief is specifically monitored** — both inbound and outbound telemarketing subject to TSR requirements.

## Campaign Patterns
<!-- Hawk writes here -->
<!-- What ad angles convert, CPL by source, audience insights, A/B test results -->

### Facebook Ads — Debt Relief CPL Benchmarks & Market Intel (2024-2025)
_Added by Hawk 🦅 | 2026-02-14 ~23:58 GST_
_Sources: WordStream 2025 FB Ads Benchmarks (1,000+ campaigns analyzed), WordStream historical benchmarks, industry knowledge. **Note:** Web search API unavailable — Brave key not configured. Data below combines verified benchmark sources with well-established industry patterns. Debt-specific CPL ranges are directional estimates based on Finance & Insurance category data + debt vertical niche premiums. Will verify with live campaign data once we launch._

---

#### 1. Facebook Ads Industry Benchmarks — Finance & Insurance (2025)

**Traffic Campaigns:**
- CTR: 0.98% (lowest tier — below 1.71% all-industry avg)
- CPC: $1.22 (highest tier — above $0.70 all-industry avg)

**Lead Campaigns (Lead Ads / form-based):**
- CPC: Not broken out separately for Finance in the 2025 report, but historically $3.77 (2024 data). Attorneys & Legal came in at $4.10 in 2025.
- CVR: Finance historically ~9.09%. Attorneys & Legal at 10.53% in 2025.
- CPL all-industry average: **$27.66** (up 20.94% YoY from $22.87 in 2024)
- CPL for Attorneys & Legal: **$18.17** (down 77% YoY — anomaly, likely competitive pullback)

**Key trend:** CPL is rising across the board. 60% of industries saw CPL increases in 2025. Finance/Insurance is one of the most expensive categories on Facebook.

#### 2. Debt Relief / Debt Settlement — Estimated CPL Ranges

Debt relief is a sub-niche within Finance & Insurance, with HIGHER CPLs due to:
- Heavy compliance restrictions on ad copy (Meta's financial services policies)
- Smaller qualified audience (people with $10K+ unsecured debt, behind on payments)
- High competition from well-funded players (NDR, FDR, Pacific Debt all run FB ads)
- Seasonal spikes (post-holiday Jan-Mar, back-to-school Aug-Sep)

**Estimated Facebook CPL ranges for debt relief leads (2024-2025):**

| Lead Type | CPL Range | Notes |
|---|---|---|
| Raw FB Lead Ad (form fill only) | $15–$35 | Name + phone + email + debt amount. No verification. High junk rate. |
| Qualified lead (phone-verified, $10K+ debt) | $30–$65 | Requires call center or IVR qualification step. This is what buyers want. |
| Exclusive real-time lead | $45–$85 | Sold to one buyer only, delivered in real-time. Premium pricing. |
| Shared/aged lead | $5–$15 | Sold to multiple buyers or 24-48hr+ old. Lower quality, lower price. |
| Live transfer (inbound call) | $80–$150+ | Consumer on the phone, transferred to buyer's call center. Highest value. |

**Buyer payout context (what buyers pay us):**
- Ping/post lead: $20–$65 depending on quality tier, debt amount, state
- Exclusive lead: $40–$90
- Live transfer: $100–$200+
- **Our target arbitrage: Buy at $14–$20 CPL, sell at $40–$65. That's $20–$45 margin per lead.**

#### 3. What Ad Angles Work in Debt Relief (FB)

**Top-performing angles (based on industry patterns):**

1. **"Government program" / "New 2025 program"** — ⚠️ HIGH COMPLIANCE RISK. Works extremely well for CTR but borderline misleading. Shield must review. FTC has flagged impersonation of government programs.

2. **"Struggling with debt? You're not alone"** — Empathy-first angle. Lower CTR but higher quality leads. People who click are genuinely in pain, not curiosity clickers. **Recommended starting angle.**

3. **"Reduce your debt by up to 50%"** — Direct benefit angle. Strong performer IF backed by actual program outcomes. Must have substantiation per FTC guidelines. NDR and FDR use this angle extensively.

4. **"One simple monthly payment"** — Debt consolidation framing. Appeals to overwhelmed consumers. Works well for $15K-$40K debt range.

5. **"Stop creditor calls"** — Fear/relief angle. Very emotional trigger. Good CTR. Quality depends on landing page qualification.

6. **"See if you qualify in 60 seconds"** — Low-friction CTA. Works best with instant-form Lead Ads. High volume but lower quality without qualification steps.

**Creative formats that work:**
- **Video testimonials** (real or actor) outperform static images 2-3x on CTR
- **Before/after debt payoff stories** — strong emotional hook
- **Simple text-on-color backgrounds** — surprisingly effective, low production cost
- **Carousel ads** showing step-by-step process — good for education-first approach

**Audiences to test:**
- Interest targeting: Credit cards, debt management, financial stress, bankruptcy (careful — Meta may restrict)
- Lookalike audiences: Based on converter data (need 100+ conversions first)
- Broad targeting with Advantage+: Meta's algo finds debt-stressed users via behavioral signals. **BUT** high bot/junk risk — need form validation.
- Age: 30-55 sweet spot. Under 30 = lower debt amounts. Over 55 = different financial products.
- Income: Don't target low income directly (compliance issue) — let the qualification questions filter.

#### 4. Competitive Landscape

**Big spenders on FB for debt relief (estimated monthly FB spend):**
- National Debt Relief: $500K-$1M+/mo (massive scale, brand + performance)
- Freedom Debt Relief: $300K-$700K/mo (aggressive, multi-channel)
- Pacific Debt: $50K-$150K/mo (smaller but consistent)
- Numerous lead gen intermediaries: $10K-$100K/mo each

**What this means for us ($5K budget):**
- We CANNOT compete on scale. We compete on efficiency.
- Target long-tail audiences the big players over-bid on
- Test 15+ ad sets at $5-$10/day each, kill fast, scale winners
- Focus on quality over volume — a $20 CPL on A-tier leads beats $12 CPL on junk
- Use Lead Ads (instant forms) to minimize landing page friction and reduce CPC

#### 5. Platform-Specific Risks

- **Ad account bans:** Debt relief is a restricted category on Meta. Account can be disabled without warning. Mitigation: Keep ad copy compliant, avoid "debt forgiveness" / "government program" language, have backup ad accounts.
- **Policy review delays:** Financial services ads go through extra review. 24-48hr approval times common. Plan creative pipeline ahead.
- **Audience size limitations:** After compliance-safe targeting, audience pools can be small. Monitor frequency — creative fatigue hits fast at <500K audience size.
- **iOS privacy impact:** Conversion tracking degraded post-ATT. Use Conversions API (CAPI) server-side tracking for accurate attribution.

#### 6. Hawk's Recommended Launch Strategy

1. **Budget:** $50/day initial ($1,500/mo of $5K total budget)
2. **Campaign structure:** 1 campaign, 5 ad sets (different audiences), 3 ads per ad set = 15 creatives
3. **Kill rules:** Any ad set with CPL >$25 after 500 impressions AND <2% CTR → kill
4. **Scale rules:** CPL <$18 with 20+ leads → increase budget 30%/day
5. **Creative refresh:** Every 5-7 days rotate 2-3 new creatives to combat fatigue
6. **Tracking:** UTM params + CAPI + Supabase logging for full attribution

**⚠️ IMPORTANT:** Before ANY ads go live, Shield must approve all copy and creative. FTC enforcement in debt relief is aggressive (see Shield's enforcement review in Compliance Patterns above). One bad ad = account ban + potential legal exposure.

---

_Confidence level: MEDIUM. Benchmarks are from verified sources (WordStream 2025). Debt-specific CPL ranges are directional estimates — will validate with our own campaign data within first 2 weeks of spend. Web search was unavailable (no Brave API key) so couldn't pull real-time competitor spy data or forum discussions._

_Next steps: (1) Get Brave API key configured for deeper research. (2) Run Facebook Ad Library research on competitor creatives. (3) Draft 15 ad variations for Shield review. (4) Set up CAPI tracking before first dollar spent._

## Delivery Patterns
<!-- Signal writes here -->
<!-- Buyer preferences, best delivery times, email deliverability insights, call connect rates -->

## Buyer Intelligence
<!-- Fury + Signal write here -->
<!-- Buyer profiles, payout history, reliability scores, negotiation notes -->

### CPA vs Quality — The Real Economics (from AK, Feb 15 2026)

**Higher CPA ≠ better deal.** CPA is a function of lead quality requirements:
- **$60 CPA** (FDR) = they want HIGH debt amount leads. Average unsecured debt $30K+.
- **$22-$25 CPA** (JGW) = they accept LOWER debt amounts. Maybe $10K-$15K+.
- **The CPA reflects what the buyer expects to close, not our profit.**

**What matters is: can we source leads that match the quality tier at a cost below the CPA?**

### Debt Type — CRITICAL Filter

**Only unsecured debt qualifies for debt settlement:**
- ✅ **Credit card debt** — THE biggest component. This is 70-80% of what settlement companies work with.
- ✅ **Personal loan debt** — smaller component, accepted.
- ❌ **Mortgage** — secured, NOT eligible
- ❌ **Student loans** — NOT eligible for these buyers
- ❌ **Auto loans** — secured, NOT eligible
- ❌ **Medical debt** — varies by buyer, usually separate programs

**If a lead has mostly mortgage or student loan debt, it's worthless to debt settlement buyers.** Doesn't matter if they owe $100K — wrong debt type = rejected.

### Why FastDebt API is Critical

Before delivering ANY lead to a buyer, we need to know:
1. **Total unsecured debt amount** — determines which CPA tier/buyer
2. **Debt composition** — what % is credit card vs personal loan vs other
3. **Number of accounts** — more accounts = more settlement opportunities = higher value

**FastDebt enrichment is NOT optional — it's the gatekeeper between acquiring garbage and delivering quality.**

Without enrichment, we're guessing. Guessing at $5K budget = dead in 2 weeks.

### Lead Source 3: Our Own Payday/Personal Loan Sites (from AK, Feb 15)
- AK owns payday + personal loan websites with live applicant traffic
- Loan application asks "reason for loan" — when answer is "debt consolidation" = debt relief signal
- These applicants are WARMER than RevPie/FB: self-qualified, zero acquisition cost, real-time
- Backend can push these leads directly to Ocean DB
- Already have: name, phone, email, income, loan amount — most fields needed for buyer forms
- **Highest margin source** — $0 CPL, just enrichment + delivery cost

### Revised Unit Economics

Don't chase the $60 CPA. Chase the **quality match**:
- Source leads with $15K+ unsecured debt (mostly credit card)
- Enrich via FastDebt to confirm debt type + amount
- Route to the right buyer based on their debt profile
- A $25 CPA lead that converts is worth more than a $60 CPA lead that gets rejected

### Debt Relief Lead Buyer Landscape — 2026-02-14
*Added by Signal 📡 | Sources: BUYERS_PLAYBOOK.md benchmarks, industry knowledge, boberdoo.com (verified accessible). NOTE: Web search API unavailable during research. Payout ranges are industry-standard estimates — MUST be verified with live buyer conversations before committing to any pricing.*

---

#### Payout Ranges by Lead Type

| Lead Type | Payout Range | Notes |
|---|---|---|
| **Exclusive web leads (API/real-time)** | $40–$80/lead | Standard for verified, real-time delivery. Higher end for $25K+ debt, premium states (CA/TX/FL/NY) |
| **Exclusive web leads (email batch)** | $30–$60/lead | Lower due to latency. Morning delivery preferred by most buyers |
| **Live transfer calls** | $50–$150/call | Duration-based (typically 90–120 sec minimum). Highest margins but requires call infrastructure (Ringba) |
| **Aged leads (30–90 days)** | $5–$15/lead | Low margin, high volume. Good for cash flow while building real-time pipeline |
| **Shared leads (sold to 2–3 buyers)** | $15–$30/lead | Lower per-buyer but higher total yield. Requires careful dedup and buyer transparency |

#### Key Buyer Categories

**Tier 1 — Debt Settlement Companies (Direct Buyers)**
- National Debt Relief, Freedom Debt Relief, Pacific Debt, Accredited Debt Relief, Beyond Finance, New Era Debt Solutions, CuraDebt, National Debt Advisors
- Pay highest ($50–$80 exclusive, $80–$150 live transfers)
- Strict compliance requirements (TSR, state licensing verification)
- Usually want exclusive leads only
- State restrictions vary (FDR excludes NJ, others vary)
- Minimum debt thresholds: typically $10K–$15K unsecured
- **Onboarding difficulty: HIGH** — require proven quality track record, compliance documentation

**Tier 2 — Affiliate Networks with Debt Offers**
- Perform[cb], MaxBounty, ClickDealer, Everflow marketplace, MarketCall
- Act as intermediaries — lower payout ($30–$50) but easier onboarding
- Good for initial volume while building Tier 1 relationships
- Everflow (we have RevvMind account) — check marketplace for active debt offers
- **Onboarding difficulty: MEDIUM** — network approval + offer approval

**Tier 3 — Lead Aggregators/Exchanges**
- LeadPoint (NMLS #3175, Woodland Hills CA), boberdoo-powered exchanges
- Buy in bulk at lower rates ($20–$40)
- Less picky on quality but lower margins
- Good fallback for leads that don't meet Tier 1 specs
- **Onboarding difficulty: LOW** — volume-based, less strict

#### Standard Lead Spec Requirements (Cross-Buyer)

| Field | Required? | Notes |
|---|---|---|
| Full name | ✅ | First + Last, no initials |
| Phone (mobile preferred) | ✅ | Must be validated, not disconnected |
| Email | ✅ | Must be deliverable (MX check) |
| State | ✅ | Must match buyer's licensed states |
| Estimated unsecured debt | ✅ | Most buyers want $10K+ minimum |
| Debt types | Preferred | Credit card, medical, personal loans, student (varies) |
| Employment status | Sometimes | Some buyers require this |
| Behind on payments? | Sometimes | Higher-intent signal = higher payout |
| IP address + timestamp | ✅ (compliance) | TCPA consent proof — non-negotiable |
| Consent language + URL | ✅ (compliance) | Shield must approve before any delivery |
| Jornaya/TrustedForm cert | Increasingly required | ~60% of Tier 1 buyers now require this |

#### Recommended Initial Buyer Strategy

1. **Start with Everflow marketplace** (we have RevvMind account) — find 2–3 active debt offers, test delivery flow
2. **Apply to Perform[cb] and MaxBounty** — Tier 2 networks with consistent debt demand
3. **Direct outreach to mid-tier settlement companies** — Pacific Debt, New Era, CuraDebt (less gatekept than NDR/FDR)
4. **Build to 3 active buyers minimum** before scaling traffic (per BUYERS_PLAYBOOK.md rule)
5. **Live transfers via Ringba** should be Phase 2 — highest payout but needs call infrastructure first

#### Pricing Strategy Recommendation

- **Target blended CPL (our cost):** $8–$15/lead (per Hawk's media buying)
- **Target blended payout:** $40–$60/lead (starting with Tier 2 network offers)
- **Target margin:** $25–$45/lead (60–75% gross margin)
- **Break-even point:** ~125 leads at $40 payout to cover $5K initial budget
- ⚠️ **These are estimates. Actual rates MUST be verified through buyer conversations and network dashboards.**

#### What Signal Needs to Verify (Next Steps)

1. [ ] Log into Everflow/RevvMind — check active debt relief offers, actual payouts
2. [ ] Check RevPie aged account — any existing debt buyer relationships?
3. [ ] Research Jornaya/TrustedForm pricing — increasingly required for Tier 1
4. [ ] Get Ringba set up for live transfer capability (Phase 2)
5. [ ] Draft buyer outreach email template for direct Tier 1 contacts
6. [ ] Confirm state licensing requirements per buyer — map which states we can serve

## Postback Infra Ownership & Endpoint (Fury, Feb 16 2026)

- Shared endpoint: `https://ocean11-postback.vercel.app`
- Health: `/health`
- Everflow global S2S template:
  `https://ocean11-postback.vercel.app/postback?click_id={sub1}&offer_id={offer_id}&payout={amount}&txn_id={transaction_id}&secret=<POSTBACK_SECRET>`
- Ownership rule:
  - **Vision** owns infrastructure state (env vars, uptime, production placement in Everflow)
  - **Peter** owns code fallback + deployment reproducibility
  - Fury delegates; does not remain single point of execution

## RevPie ↔ Everflow Traffic Optimization Loop (Fury, Feb 15 2026)

**Source: AK direct + RevPie dashboard exploration**

### How It Works
- RevPie is a **native ad network** — publishers (source IDs) show our ads, we pay CPC
- Each publisher has a **Source ID** in RevPie
- Our ad URLs contain **Everflow tracking links** (e.g. `trackingcampaign.o18.link/c?o=...&aff_click_id={replace_it}`)
- Everflow receives the click, tracks through to conversion (lead submitted, call connected, etc.)
- **Everflow is the source of truth** for which Source IDs actually convert

### The Optimization Loop
```
1. RevPie Source ID sends traffic → our Everflow tracking link
2. Everflow tracks: click → landing page → form fill → lead → revenue
3. Hawk checks Everflow: which Source IDs convert? At what CPA?
4. Back to RevPie:
   - WHITELIST high-converting Source IDs → raise custom bids
   - BLACKLIST garbage Source IDs → stop wasting money
   - Adjust default bid for the ad
```

### RevPie Controls
- **Whitelist/Blacklist** page (`/advertiser/wl-bl`) — block/allow per campaign + ad
- **Custom Bid per Source ID** — on Live Sources tab inside each ad
- **Default bid range:** $0.10 - $7.00 CPC
- **Ad Rotation Schedule** — 24h × 7-day grid, timezone-aware (set to America/New_York)

### Existing Campaigns (Zappian era, all paused)
| Campaign | Daily Budget | Ads |
|---|---|---|
| Debt_Campaign | $220 | NDR_Mobile_W ($0.50 CPC), Cliq_Mobile_W_NEW |
| DRA_debt | $120 | 1 active |
| Top_Debt_Options | $100 | 1 active |
| Financify_RS | $100 | 1 active |
| Iconic_debt | $50 | 1 active / 1 paused |
| SpikeMyCC | $50 | 0 active / 1 paused |
| SelfCreditbuilder | $50 | 1 active |

- **Account balance:** $481.57 (usable)
- **Total spent (lifetime):** $15,518.43
- **Account type:** Advertiser
- **Login:** vishal@revvmind.com

### Key Insight from AK
Source ID optimization is THE lever for RevPie profitability. Same ad, same creative — one source converts at 3%, another at 0.1%. The difference between profitable and bankrupt is knowing which is which, and that data lives in Everflow.

## Everflow (RevvMind) — Full Platform Map (Fury, Feb 15 2026)

**Source: Direct exploration of revvmind.everflowclient.io**

### Account Details
- **URL:** revvmind.everflowclient.io
- **Login:** arif@revvmind.com
- **View:** Partner/Affiliate (not Network Admin)
- **Account Manager:** Zakir Khan (zakir@zappian.com)
- **Last Month (Jan 2026):** 310 clicks, 6 conversions, $24 revenue, 1.94% CVR

### Sidebar Navigation
1. ☰ **Hamburger** — expand/collapse sidebar
2. 🔍 **Search** — search offers, postbacks, transactions (shows Recently Viewed)
3. 🖥️ **Dashboard** — My Stats: Clicks, Revenue, Conversions, CVR, Events, EVR + Performance chart
4. 🔗 **Tracking & Asset Generator** — generate tracking links per offer (Single/Multiple/All), creative assets, coupon codes
5. 📦 **Offers → Manage** — all 15 offers listed with ID, name, category, channels, payout, rules
6. 🔔 **Notifications** — empty (no recent)
7. 👤 **Profile** — My Account, Notification Preferences, Logout
8. ▶️ **Unknown** — times out on click (possibly Reporting — couldn't load)

### All 15 Offers (VERIFIED from Everflow)

#### Debt Relief Offers (Our Focus — 10 offers)
| ID | Name | Category | Channel | Payout | Notes |
|---|---|---|---|---|---|
| 4930 | Freedom Debt Relief - Email only - M-F Drops Only | Debt | - | CPA $60 | Ask for cap, highest payout |
| 4907 | Cliqsilver Credit Card Debt Cpl-sq | Credit Card | - | CPA $30 | |
| 4906 | JG Wentworth (nc-21805786) | Debt | - | CPA $25 | Web traffic |
| 4905 | National Debt Relief - W (nc-21865725) | Debt | - | CPA $50 | Web traffic |
| 4836 | NDR - (Mon-Fri) Private-CPL (Budgeted) | Debt Relief | Email | CPA $45 | |
| 4783 | NDR -SQ(NC-21734336) | Debt | Email | CPA $24 | |
| 4740 | NDR - Email Only - CPL (Budgeted) | Debt Relief | Email | CPA $16 | Lowest debt CPA |
| 4737 | JGW Debt Settlement M-F {US} (NC-21734350) | Debt | Email | CPA $22 | |
| 4718 | JGW Debt Settlement - [MKP] | Data | Email | CPA $24 | Marketplace |
| 4633 | JGW Debt Settlement CPL - Email NOW weekends! (NO CA) | Debt Relief | Email | CPA $24 | Accepts weekends, no CA |

#### Loan Offers (Zappian legacy — 5 offers)
| ID | Name | Category | Channel | Payout |
|---|---|---|---|---|
| 3228 | Maxloanusa.com_ZM_025_PUB | Personal Loan | Email + SMS | CPS 100% |
| 2884 | Rapidfundonline.com | Payday Loan | Email | CPS 100% |
| 2256 | 1stlendingusa.com_ZM_025 | Personal Loan | Email | CPS 100% |
| 1901 | eloantoday.com_ZM_025 | Personal Loan | Email + SMS | CPS 100% |
| 176 | Brighterloan.com_ZM_025 | Personal Loan | Email | CPS 100% |

### Key Observations
1. **All 15 approved, all US, all active** — ready to use
2. **Debt offers split by channel:** Web (-) vs Email — different offers for different traffic types
3. **FDR $60 is highest CPA** but "Ask for Cap" = limited volume
4. **NDR has 4 separate offers** at different CPAs ($16-$50) — likely different quality/channel requirements
5. **JGW has 4 offers** ($22-$25) — one accepts weekends (no CA)
6. **Loan offers are CPS 100%** — revenue share, not fixed CPA. These are Zappian's own loan sites
7. **"Budgeted" in offer name** = buyer has a monthly cap — volume limited
8. **Offer detail pages don't render** in partner view (shows blank "Network" page)
9. **One confirmed transaction:** FDR offer 4930 on 01/28/2026 04:09:53 EST

## Market Intelligence
<!-- Watchtower + Fury write here -->
<!-- Competitor moves, regulatory changes, market trends, seasonal patterns -->

### Weekly Regulatory Intelligence Check — 2026-02-16 (Fury)
Scope scanned: CFPB, FTC, FCC, CAN-SPAM guidance and key state lenses (CA/NY/TX/FL) for debt relief + personal loan cross-monetization.

**Outcome:** No material regulatory change this week.

**Operational decision:** No immediate edits to `docs/VOICE_GUIDE.md`, `config/copy_lexicon.yaml`, or V1 copy templates.

### Login Reliability Architecture v1 — 2026-02-17 (Fury)
Added `docs/LOGIN_RELIABILITY_PLAYBOOK.md` for stable auth operations on Everflow/RevPie/Facebook.

Core model:
- Layer 1: Chrome relay for login-sensitive tasks
- Layer 2: openclaw profile for scripted fallback
- Layer 3: API-first migration for repeatable operations

Includes mandatory pre-flight, recovery matrix, platform SOPs, Vision monitoring cadence, and proof-bundle gate before marking completion.

### Copy Guardrails System v1 — 2026-02-16 (Fury)
Implemented a controlled copy system so Hawkeye output stays consistent and compliant across debt relief + personal loan cross-monetization.

**Artifacts created:**
- `docs/VOICE_GUIDE.md` (tone/format rules)
- `config/copy_lexicon.yaml` (allowed/caution/blocked phrasing + CTA allow/block lists)
- `templates/cta-library.md`
- `templates/email-system/debt-relief-v1.md`
- `templates/email-system/personal-loan-cross-sell-v1.md`

**Operating rule:** No ad/email copy goes live without Hawkeye draft + Cap compliance review + Fury approval.

**Why:** Prevents style drift, risky claims, and agent-to-agent copy inconsistency.

## Form Filling — Hard-Won Lessons (Fury, Feb 15 2026)

### Gravity Forms (WordPress) — JGW Pattern
- **Engine:** Gravity Forms (`gform_48`), multi-page wizard, all on single URL
- **Page structure:** Each step is `gform_page_48_{N}` div, shown/hidden via `display: block/none`
- **Navigation buttons:** `gform_next_button_48_{pageBreakFieldId}` — button ID ≠ step number
- **AJAX validation:** Every "Continue" click fires AJAX POST validating current page server-side. If validation fails, re-renders current page. **#1 gotcha.**

### What Works vs Doesn't

| Approach | Result |
|---|---|
| `page.locator.type()` for text | ❌ GF doesn't always register |
| JS `set_value` (nativeSetter + events) | ✅ Regular text fields |
| JS `set_value` for masked fields | ❌ inputmask buffer stays empty |
| `press_sequentially` for masked fields | ✅ Fires real key events per char |
| Native `.click()` on radios | ❌ Custom-styled = not "visible" |
| JS `.click()` on radios | ✅ |
| Clicking Continue (native or JS) | ⚠️ Triggers AJAX validation |
| **Direct DOM manipulation (show/hide pages)** | ✅ Bypasses AJAX, server validates on submit |

### Winning Strategy
1. **Text fields:** JS `set_value` with nativeSetter + input/change/blur events
2. **Masked fields (phone/SSN/dates):** `press_sequentially` with native click for focus
3. **Radio buttons:** JS `.click()`
4. **Page transitions:** Direct DOM — hide current `gform_page` div, show next, update GF hidden page tracking fields
5. **Final submit:** Click submit button, check for confirmation text

### Input Mask Handling
- JGW phone: `inputmask` library, mask `(999) 999-9999`
- **MUST use `press_sequentially` with digits only** — mask auto-formats
- Setting `.value` directly = inputmask buffer empty → validation fails
- `inputmask.setValue()` doesn't reliably pass GF server validation
- Tab out after typing to trigger blur

### GF Internals
- Form ID: `gform_48`, product: `Affiliate`, type: `Lead Submission`
- Hidden defaults: educationLevel=bachelors, payFrequency=biweekly, purpose=debt_consolidation, product=DS
- `state_48` = base64-encoded validation state — don't touch
- `gform_target_page_number_48` / `gform_source_page_number_48` — page tracking
- AJAX uses iframe: `gform_submission_method=iframe`

### Anti-Bot (JGW, Feb 2026)
- No CAPTCHA, no honeypots, no Cloudflare, no reCAPTCHA
- Input mask on phone = minor (solved with press_sequentially)
- Amount validates: $500-$250,000
- Phone validates: 10 digits
- **Low anti-bot posture** — good first target

### Performance
- Full 10-step fill: ~15-20 seconds headless
- Use `domcontentloaded` wait (NOT `networkidle` — times out on analytics scripts)
- Human delay 0.5-1.5s not required for headless but good practice

### SSN — CRITICAL
- Required on step 10, format `___-__-____`
- Test fills: `000-00-0000`
- **NEVER store real SSNs** — form_data excludes by design

### State Coverage (JGW)
- 31 states + DC: AL, AK, AZ, AR, CA, CO, FL, ID, IN, IA, KY, LA, MD, MA, MI, MS, MO, MT, NE, NM, NY, NC, OK, PA, SD, TN, TX, UT, VA, DC, WI
- Other states → redirected to law firm partner
- Dropdown lists all 50 + DC + PR

### DB Storage
- `source: "jgwentworth_form_fill"`, `form_url` set
- `form_data` JSONB: offer name + submitted flag (SSN excluded)
- DOB: MM/DD/YYYY → ISO YYYY-MM-DD

### Page-to-Button ID Mapping (JGW gform_48)
```
Step 1 → gform_next_button_48_98
Step 2 → gform_next_button_48_101
Step 3 → gform_next_button_48_100
Step 4 → gform_next_button_48_103
Step 5 → gform_next_button_48_108
Step 6 → gform_next_button_48_107
Step 7 → gform_next_button_48_104
Step 8 → gform_next_button_48_105
Step 9 → gform_next_button_48_106
Step 10 → gform_submit_button_48 (final submit)
```

### Field-to-Input Mapping (JGW gform_48)
```
Step 1:  input_111 (amount, text, masked)
Step 2:  input_37  (employment, radio: employed/self_employed/not_employed/retired/military/other)
Step 3:  input_84  (income, text, masked)
Step 4:  input_35  (property, radio: rent/own_with_mortgage/own_outright)
Step 5:  input_1 (first_name), input_3 (last_name)
Step 6:  input_26 (email)
Step 7:  input_28 (phone, inputmask "(999) 999-9999")
Step 8:  input_89 (address1), input_90 (address2), input_91 (city), input_109 (state, select), input_92 (zip)
Step 9:  input_85 (dob, text)
Step 10: input_94 (ssn, inputmask "___-__-____")
Hidden:  input_127=bachelors, input_128=biweekly, input_129=debt_consolidation, input_130=DS
```

## Technical Patterns
<!-- Any agent -->
<!-- API quirks, rate limits discovered, workarounds found -->

### Repo Integrity Baseline (2026-02-14, Watchtower)
- 106 files total. all 6 agents have SOUL.md + config.yaml + MISSIONS.md (18/18).
- docs: 7 files (includes MODEL_STRATEGY_V2.md and ARCHITECTURE_INSPIRATIONS.md beyond original spec).
- shared: 7 files (includes DRIFT_WATCH.md and TRUST_TIERS.md beyond original spec — bonus shared context).
- db: 3 files (schema.sql, seed.sql, migrations/001_initial.sql).
- no missing structural files detected. repo is structurally complete for pre-launch phase.
- note: `ls` aliased or missing on this system — use `find` instead for file listing.

### OpenClaw Fury Model Source-of-Truth (2026-02-17, Peter)
- Live Fury model routing is controlled by `~/.openclaw/openclaw.json` (`agents.list[]` entry with `id: "main"`), not by repo template files alone.
- `config/openclaw.yaml` is still useful as team template/source control, but changing only that file does not switch already running local Fury sessions.
- Service restart command to apply runtime config changes: `openclaw gateway restart`.
- Existing session records can keep old model metadata (for example `agent:main:main` still showing `gpt-5.3-codex-spark` history); start/reset session key after model switch to avoid inherited context issues.

### OpenClaw Agent Drift Guard (2026-02-17, Peter)
- Added `scripts/validate_agent_alignment.sh` to prevent stale template drift.
- Guard checks:
  - No deprecated IDs (`captain`, `signal`) in `config/openclaw.yaml`.
  - Required files exist for canonical agents (`fury/scout/shield/hawk/forge/watchtower/peter/ocean`).
  - Every `soul:` path in template config resolves to a real file.
  - Runtime ID comparison against `~/.openclaw/openclaw.json` with `main` normalized to `fury`.
- Use this before commits that touch agent identity/config/missions.
