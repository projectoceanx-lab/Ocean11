# EBC CRO Sprint V1 — 48-Hour Implementation Plan

_Created: Feb 17, 2026 | Sprint Window: Feb 17–19, 2026_
_Source: docs/CRO_ANALYSIS_EBC.md | Owner: Forge 🔥 | Reviewer: Shield 🛡️_

---

## Sprint Goal

Ship 5 high-impact CRO changes to everybuckcounts.com/ebc-debt-relief/ in 48 hours. Target: **+40% lead completion rate** from existing traffic.

---

## 1. Quick Wins — Shipping Order

Changes ordered by impact:effort ratio. Each is independently deployable and rollback-safe.

### QW-1: Fix Typo + Tighten Copy (Hour 0–1)
**Change:** Fix "intrested" → "interested" on Step 2. Review all copy for grammar/spelling.
- **Effort:** 15 min
- **Deploy:** Direct HTML edit, no structural change
- **Why first:** Zero risk, instant trust improvement, unblocks screenshot refresh for ads

### QW-2: Add Progress Bar (Hour 1–4)
**Change:** Add numbered progress indicator ("Step X of Y") with visual fill bar above form.
- **Effort:** 2–3 hours (CSS + JS)
- **Spec:** Horizontal bar, filled segments, "Step 1 of 4" label. Matches brand blue (#1a73e8 or existing).
- **Deploy:** CSS/JS addition, no form logic change

### QW-3: Add Trust Badges + Social Proof Above Fold (Hour 4–8)
**Change:** Insert trust strip between hero and form:
- "Helped 50,000+ Americans reduce their debt" counter
- 4.5-star rating badge (Google Reviews style)
- Security badge row: TrustedForm seal, 256-bit encryption, "100% Free — No Obligation"
- **Effort:** 3–4 hours (HTML/CSS, static assets)
- **Deploy:** HTML insert above form container

### QW-4: Remove SSN from Main Flow (Hour 8–16)
**Change:** Remove Step 7 (SSN) from primary form. Lead is captured at current Step 6 (after name/phone/email). SSN moves to optional post-submit page ("Get a detailed savings estimate").
- **Effort:** 4–6 hours (form logic, backend validation, post-submit page)
- **Deploy:** Form step removal + new thank-you upsell page
- **Backend:** Ensure lead record is created at Step 6 submit, SSN is separate optional update

### QW-5: Reduce 7 Steps → 4 Steps (Hour 16–40)
**Change:** Restructure form:
  - **New Step 1:** Debt slider + Interest type (merge old 1+2)
  - **New Step 2:** Zip + Address + Employment + Income (merge old 3+5+6)
  - **New Step 3:** Name + Phone + Email + TCPA consent (old 4, lead capture point)
  - **New Step 4:** Thank you + offer wall + optional SSN upsell
- **Effort:** 12–16 hours (form restructure, validation, backend, QA)
- **Deploy:** Full form replacement behind A/B test flag

### Hour 40–48: QA, Cross-Browser, Mobile Test, Shield Compliance Review

---

## 2. Expected Impact

| Change | Metric Affected | Expected Lift | Confidence |
|--------|----------------|---------------|------------|
| QW-1: Fix typo | Trust / bounce rate | +2–5% form start | High (zero downside) |
| QW-2: Progress bar | Step completion rate | +10–15% completion | High (well-documented) |
| QW-3: Trust badges | Form start rate | +10–15% form start | Medium-High |
| QW-4: Remove SSN | Final step completion | +15–20% completion | High (industry standard) |
| QW-5: 7→4 steps | End-to-end conversion | +25–40% completion | High (compounding) |

**Combined conservative estimate:** +35–50% more completed leads from same traffic.
**Combined optimistic estimate:** +60–70% more completed leads.

> ⚠️ These are estimates based on industry benchmarks (Unbounce, HubSpot form optimization studies). Actual lift will be validated via A/B test. Do NOT report these as confirmed metrics.

---

## 3. Compliance Checks Per Change

### QW-1: Fix Typo
- ✅ No compliance impact
- Shield sign-off: **Not required** (cosmetic)

### QW-2: Progress Bar
- ✅ No compliance impact
- Shield sign-off: **Not required** (UI enhancement)

### QW-3: Trust Badges
- ⚠️ **"Helped 50,000+ Americans" claim must be substantiated** (FTC Act §5 — no unsubstantiated claims). Use real number or remove.
- ⚠️ **Star rating must link to real reviews** or be removed. Fabricated ratings = deceptive practice.
- ⚠️ **BBB badge only if actually accredited.** Unauthorized use = violation.
- ✅ "100% Free, No Obligation" is compliant if service is genuinely free to consumer
- ✅ Security badges (encryption, TrustedForm) are factual
- Shield sign-off: **REQUIRED before deploy.** Shield reviews all claims for FTC §5 compliance.

### QW-4: Remove SSN
- ✅ **Improves compliance posture** — less PII collected in primary flow reduces data breach exposure
- ⚠️ If SSN is required by downstream buyers → verify buyer contracts still accept leads without SSN
- ⚠️ Post-submit SSN page must have its own clear consent language
- ✅ TCPA consent unaffected (captured at Step 3)
- Shield sign-off: **Required** (data handling change)

### QW-5: Reduce Steps
- ⚠️ **TCPA consent must remain on the lead-capture step** (Step 3) — cannot be buried or auto-checked
- ⚠️ **TCPA consent checkbox must be separate from submit button** (not pre-checked)
- ⚠️ Merging steps must not hide or reduce visibility of consent language
- ⚠️ TSR required disclosures ("no upfront fees" language) must remain visible before form submission
- ⚠️ Verify "clear and conspicuous" standard is met after layout change
- Shield sign-off: **REQUIRED. Full review of new form flow before deploy.**

### Pre-Launch Compliance Checklist (all changes)
- [ ] TSR advance fee ban disclosure visible
- [ ] TCPA consent: separate checkbox, not pre-checked, clear language
- [ ] "Message and data rates may apply" present
- [ ] Privacy Policy and Terms of Service linked
- [ ] California "Do Not Sell" link prominent (CCPA)
- [ ] No unsubstantiated claims (savings amounts, timelines, success rates)
- [ ] TrustedForm certificate firing correctly on new form
- [ ] LeadID/Jornaya token captured on new form
- [ ] Shield 🛡️ sign-off documented in shared/CONTEXT.md

---

## 4. A/B Test Design

### Test Structure
- **Tool:** Google Optimize (if available) or custom JS split via URL parameter `?v=a|b`
- **Traffic split:** 50/50
- **Duration:** Minimum 7 days or 500 conversions per variant (whichever comes first)
- **Statistical significance threshold:** 95% (p < 0.05)

### Variants

| Variant | Description |
|---------|-------------|
| **Control (A)** | Current 7-step form, no changes except QW-1 typo fix (applied to both) |
| **Treatment (B)** | New 4-step form + progress bar + trust badges + SSN removed |

### Primary Metric
- **Lead completion rate** = (leads submitted at final step) / (unique visitors who saw Step 1)

### Secondary Metrics
- Step-by-step drop-off rate (per step)
- Form start rate (clicked into Step 1 / page visitors)
- Time to completion
- Post-submit SSN opt-in rate (Treatment only)
- Lead quality score from buyers (7-day lag metric)

### Segmentation
- Device: Mobile vs Desktop (expect bigger lift on mobile)
- Source: Facebook vs organic vs email (may respond differently)
- Debt amount: <$10K vs $10K–$50K vs >$50K

### Guardrails
- If Treatment shows **>20% drop in lead quality** (buyer rejection rate) → pause test, investigate
- If Treatment shows **>15% drop in revenue per lead** → pause test, investigate
- If any compliance issue surfaces → kill Treatment immediately, revert to Control

### Phased Rollout
1. **Day 1:** QW-1 + QW-2 + QW-3 → deploy to 100% (low risk, additive)
2. **Day 2:** QW-4 + QW-5 → deploy as Treatment (B) at 50% split
3. **Day 3–9:** Collect data, monitor daily
4. **Day 10:** Call winner at 95% confidence, roll out to 100% or revert

---

## 5. Rollback Plan

### Per-Change Rollback

| Change | Rollback Method | Time to Rollback |
|--------|----------------|-----------------|
| QW-1: Typo fix | Git revert single commit | < 2 min |
| QW-2: Progress bar | Remove CSS/JS include or toggle feature flag | < 5 min |
| QW-3: Trust badges | Remove HTML block or toggle feature flag | < 5 min |
| QW-4: SSN removal | Re-enable Step 7 via form config flag | < 10 min |
| QW-5: Step reduction | Switch A/B test to 100% Control | < 2 min |

### Full Rollback (Nuclear Option)
- **Trigger:** Any of: compliance violation found, conversion drops >30%, buyer rejects >20% of new-flow leads, Arif says stop
- **Action:** Revert to pre-sprint Git tag `pre-cro-sprint-v1`
- **Time:** < 5 minutes (Cloudflare cache purge + deploy)
- **Who:** Forge executes, Watchtower verifies, Fury notified

### Rollback Decision Tree
```
Conversion dropped?
├── >30% drop within 24h → FULL ROLLBACK immediately
├── 15-30% drop → Check by device/source segment
│   ├── Isolated to one segment → Investigate, don't rollback yet
│   └── Across all segments → FULL ROLLBACK
└── <15% drop → Monitor for 48h more, likely noise

Compliance issue found?
├── Critical (TCPA/TSR violation) → FULL ROLLBACK immediately + Shield incident report
└── Minor (copy tweak needed) → Fix forward, no rollback

Buyer quality complaints?
├── >20% rejection rate increase → Pause Treatment, investigate lead data
└── <20% → Monitor, may be normal variance
```

### Pre-Sprint Checklist
- [ ] Git tag `pre-cro-sprint-v1` created on current production
- [ ] Cloudflare cache purge tested
- [ ] Feature flags tested (on/off for each change)
- [ ] Monitoring dashboard set up (GA4 funnel, step drop-offs)
- [ ] Shield compliance review scheduled (Hour 40)
- [ ] Rollback tested in staging

---

## Timeline Summary

```
Hour 0–1:    QW-1  Typo fix                    → Ship immediately
Hour 1–4:    QW-2  Progress bar                → Ship to 100%
Hour 4–8:    QW-3  Trust badges + social proof  → Ship to 100% (after Shield review)
Hour 8–16:   QW-4  Remove SSN from main flow   → Behind A/B flag
Hour 16–40:  QW-5  7→4 step reduction          → Behind A/B flag
Hour 40–48:  QA + Shield compliance review + A/B test activation
```

## Owners

| Task | Owner | Reviewer |
|------|-------|----------|
| All HTML/CSS/JS changes | Forge 🔥 | Fury 🎖️ |
| Compliance review | Shield 🛡️ | Fury 🎖️ |
| A/B test setup + monitoring | Hawk 🦅 | Watchtower 🗼 |
| Backend / form logic | Forge 🔥 + Watchtower 🗼 | Shield 🛡️ |
| Rollback execution | Forge 🔥 | Watchtower 🗼 |
| Go/no-go decision | Fury 🎖️ | Arif |

---

_Sprint starts on Fury's go. Shield has veto at Hour 40. No deploy without compliance sign-off._
