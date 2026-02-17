# Compliance Rules — US Debt Relief

This document outlines the federal and state regulations that govern debt relief lead generation. Shield uses this as its primary reference for compliance checks.

---

## Federal Regulations

### FTC Telemarketing Sales Rule (TSR) — 16 CFR Part 310

The TSR is the primary federal regulation for debt relief services.

**Key Requirements:**
1. **Advance Fee Ban** — Debt relief companies cannot charge fees before settling or reducing a consumer's debt (§310.4(a)(5))
2. **Required Disclosures** — Before enrollment, companies must disclose:
   - How long it will take to get results
   - Cost to the consumer
   - Impact on credit score
   - If the company advises stopping payments, the consequences
3. **Dedicated Account** — If consumers set aside funds, they must be in a dedicated account the consumer controls
4. **No Misrepresentation** — Cannot make false claims about success rates, savings amounts, or speed of results

**Impact on Lead Gen:**
- Our landing pages must NOT make specific debt reduction promises
- We cannot guarantee timelines ("Reduce your debt in 90 days!" = violation)
- All disclaimers must be "clear and conspicuous"

### FTC Act Section 5 — Unfair or Deceptive Practices

- All advertising must be truthful and non-deceptive
- Claims must be substantiated
- Ads must be fair (not cause substantial injury to consumers)

### TCPA — Telephone Consumer Protection Act (47 U.S.C. § 227)

Governs phone-based outreach and lead delivery.

**Requirements:**
1. **Prior Express Written Consent** — Required before making calls/texts using an autodialer or prerecorded voice to cell phones
2. **DNC Compliance** — Check against National Do Not Call Registry before calling
3. **Calling Hours** — Only 8 AM - 9 PM in the consumer's local time zone
4. **Caller ID** — Must display accurate caller ID
5. **Opt-Out** — Must provide mechanism to opt out of future calls

**For Ocean:**
- Any lead delivered via call transfer MUST have documented consent
- Shield verifies TCPA consent exists before approving call-based delivery
- Log consent evidence (form submission timestamp, IP, consent language)

### CAN-SPAM Act (15 U.S.C. § 7701-7713)

Governs commercial email.

**Requirements:**
1. **Accurate Headers** — From, To, routing info must be accurate
2. **No Deceptive Subject Lines** — Subject must reflect email content
3. **Identify as Ad** — Clearly identify the message as an advertisement
4. **Physical Address** — Include sender's valid physical postal address
5. **Opt-Out Mechanism** — Provide clear way to opt out, honor within 10 business days
6. **No Purchased Lists** — Cannot email purchased lists without consent context

**For Ocean:**
- All marketing emails include unsubscribe link
- Physical address in footer
- Subject lines match content
- Honor opt-outs immediately (not 10 days — be better than minimum)

---

## State-Level Regulations

### High-Priority States (Large Markets)

#### California
- **Proact Financial Act (SB 100)** — Debt relief companies must be licensed with DFPI
- Additional disclosures required about consumer rights
- Cannot charge upfront fees under any circumstance
- 5-day right to cancel after enrollment

#### New York
- **Debt Collection Regulations** — NYC Consumer Affairs licensing required
- Additional protections for NYC residents
- Stricter advertising standards

#### Texas
- **Texas Finance Code Chapter 394** — Debt management services must be licensed
- Bond requirement for debt management companies
- Specific contract disclosure requirements

#### Florida
- **Florida Credit Counseling Act (§817.801)** — Registration required
- Trust account requirements for consumer funds
- 3-day right to cancel

#### Illinois
- **Debt Management Service Act (205 ILCS 665)** — License required
- Fee caps on debt management services
- Annual auditing requirements

### States with Specific Restrictions
| State | Key Restriction |
|-------|----------------|
| CO | Debt adjusting license required |
| GA | Cannot charge > 7.5% of monthly payment |
| MD | Requires licensing + bonding |
| MN | Registration + bond required |
| NJ | Debt adjuster license, fee caps |
| OH | License required, max fee caps |
| PA | License required for debt management |
| VA | License + bond, fee restrictions |

### States That Prohibit For-Profit Debt Management
Some states prohibit or heavily restrict for-profit debt adjustment services:
- Mississippi
- South Carolina (limited)
- Check current status — laws change

---

## Shield's Compliance Check Sequence

For every lead, Shield runs this sequence before approving delivery:

### Check 1: TSR Compliance
- [ ] No advance fee promises in the lead's acquisition context
- [ ] Required disclosures present on the source form/landing page
- [ ] No false claims about debt reduction amounts or timelines

### Check 2: State Regulations
- [ ] Lead's state allows debt relief lead generation
- [ ] State-specific disclosures included
- [ ] Buyer is licensed in the lead's state (if required)

### Check 3: TCPA (if call delivery)
- [ ] Prior express written consent documented
- [ ] Consent language covers the specific type of call
- [ ] Consumer's number not on DNC registry
- [ ] Delivery within allowed calling hours for consumer's timezone

### Check 4: CAN-SPAM (if email delivery)
- [ ] Email includes opt-out mechanism
- [ ] Sender's physical address included
- [ ] Subject line accurately reflects content
- [ ] Consumer has not previously opted out

### Check 5: Data Accuracy
- [ ] Phone number format valid
- [ ] State/zip code match
- [ ] Debt amount is plausible (not $0, not $10M)
- [ ] No obvious fake data patterns (test@test.com, 555-555-5555)

---

## Compliance Results

| Result | Meaning | Action |
|--------|---------|--------|
| **pass** | All checks passed | Approve for delivery |
| **flag** | Minor issues found | Deliver with caution, log concern |
| **block** | Compliance violation | Do NOT deliver, log reason, notify Fury |

---

## Record Keeping

- All compliance checks logged in `compliance_log` table
- Minimum retention: 3 years (FTC standard)
- Include: lead_id, check_type, result, reason, timestamp
- Shield has veto power — no agent can override a block

---

## References

- [FTC TSR Full Text](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-310)
- [TCPA Full Text](https://www.law.cornell.edu/uscode/text/47/227)
- [CAN-SPAM Act](https://www.law.cornell.edu/uscode/text/15/chapter-103)
- [FTC Debt Relief Resources](https://www.ftc.gov/business-guidance/resources/debt-relief-companies-ftc-telemarketing-sales-rule)
- [CFPB Debt Relief Info](https://www.consumerfinance.gov/consumer-tools/debt-relief/)
