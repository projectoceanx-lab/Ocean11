# Buyer's Playbook

How to find, onboard, negotiate with, and manage lead buyers for debt relief.

---

## Finding Buyers

### Where to Look
1. **Industry networks** — Debt relief companies, credit counseling agencies, debt settlement firms
2. **Affiliate networks** — ClickDealer, MaxBounty, Perform[cb], Everflow marketplace
3. **LinkedIn** — Search for "debt relief buyer", "lead buyer debt settlement"
4. **Industry events** — LeadsCon, Affiliate Summit, FinCon
5. **Direct outreach** — Cold email/call established debt relief companies
6. **RevPie/LeadPoint** — Marketplace platforms where buyers list their demand

### Ideal Buyer Profile
- Licensed debt relief / settlement company
- Active in 10+ states
- Daily cap of 25-100 leads
- Payout $40-100 per exclusive lead
- Net-15 or faster payment terms
- Responsive to delivery (accepts within 4 hours)

---

## Onboarding a New Buyer

### Step 1: Initial Contact
- Introduce Ocean as a quality-focused debt relief lead provider
- Share sample lead format (fields we deliver)
- Ask about their requirements:
  - Which states they're licensed in?
  - Minimum debt amount?
  - Preferred delivery method (email, call, API)?
  - Daily cap?
  - Payout per lead?

### Step 2: Test Batch
- Start with 5-10 test leads
- Track acceptance rate and feedback
- Adjust quality criteria based on their feedback

### Step 3: Go Live
- Set up in `buyers` table with agreed terms
- Configure delivery routing in Signal
- Start with conservative daily cap (50% of their stated cap)
- Monitor return rate for first 2 weeks

### Step 4: Scale
- Increase cap gradually based on acceptance rate
- Negotiate better payouts at volume milestones
- Build relationship score based on:
  - Payment reliability
  - Acceptance rate
  - Communication responsiveness
  - Return rate

---

## Payout Negotiation

### Factors That Affect Payout
| Factor | Higher Payout | Lower Payout |
|--------|--------------|--------------|
| Lead freshness | Real-time | Aged (30+ days) |
| Exclusivity | Exclusive | Shared |
| Verification | Fully verified | Self-reported only |
| Debt amount | $25K+ | Under $10K |
| State | CA, TX, FL, NY | Low-population states |
| Delivery method | Live transfer (call) | Email only |

### Payout Benchmarks (Debt Relief, 2026)
- **Email leads (exclusive):** $30-60/lead
- **Call transfers (live):** $50-150/call (duration-based)
- **Aged leads (30-90 days):** $5-15/lead
- **API delivery (real-time):** $40-80/lead

### Negotiation Tips
1. Start at market rate, don't lowball yourself
2. Offer volume discounts only after proving quality
3. Get payment terms in writing
4. Track everything — use data to negotiate raises
5. Have 2-3 buyers minimum (never be dependent on one)

---

## Managing Caps & Routing

### Daily Cap Management
- Signal checks `current_daily_count` vs `daily_cap` before every delivery
- If a buyer is at cap, route to next best buyer
- Reset caps daily at midnight (pg_cron or scheduled function)
- Respect `preferred_hours` — don't deliver at 2 AM

### Priority Routing Logic
1. Highest payout buyer that's under cap and in hours
2. If tie, prefer buyer with best relationship score
3. If all buyers at cap, queue lead for next day
4. If lead ages > 48h undelivered, flag for Captain review

---

## Handling Returns

Returns happen when a buyer rejects a lead after acceptance. Common reasons:
- **Bad contact info** — Phone disconnected, email bounced
- **Duplicate** — They already have this lead
- **Not qualified** — Debt too low, wrong state
- **TCPA issue** — On DNC list

### Return Rate Thresholds
| Rate | Action |
|------|--------|
| < 5% | Excellent — negotiate payout raise |
| 5-10% | Normal — monitor |
| 10-15% | Warning — review lead quality |
| 15-20% | Problem — Shield audit required |
| > 20% | Critical — pause buyer, investigate |

### Process
1. Buyer reports return with reason
2. Signal logs in `deliveries` (status → 'returned')
3. Revenue is reversed in `pnl_daily`
4. Scout reviews returned leads for pattern (bad source? enrichment gap?)
5. If return rate exceeds 15%, Captain is notified
