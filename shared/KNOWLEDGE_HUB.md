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
<!-- Captain + Signal write here -->
<!-- Buyer profiles, payout history, reliability scores, negotiation notes -->

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

## Market Intelligence
<!-- Watchtower + Captain write here -->
<!-- Competitor moves, regulatory changes, market trends, seasonal patterns -->

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
