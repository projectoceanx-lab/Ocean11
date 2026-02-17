# Fury — Active Missions

_You own the P&L. Every mission below either makes money or protects money. Nothing else qualifies._

## 🎯 Current Phase: PHASE 1 — Prove the Loop

**The only question that matters:** Can we acquire a lead, comply it, deliver it to a buyer, and get paid?

Until the answer is YES with proof, nothing else exists. No scaling, no optimization, no new channels. Prove the loop.

### Mission 1: First Paid Conversion (CRITICAL PATH)
_Target: First Everflow postback confirmation = first revenue_

| Step | Owner | Status | Deadline |
|------|-------|--------|----------|
| Form filler working with residential proxy | Scout | ✅ Done | — |
| Everflow tracking URLs integrated in fill flow | Scout | ✅ Done | — |
| DB logging on submission | Peter/Watchtower | 🔧 Fix needed | Feb 18 |
| Live test submission on NDR 4905 ($50) | Scout | ⏳ Waiting AK go-ahead | — |
| Verify Everflow registers the click + conversion | Watchtower | ⏳ Blocked by above | — |
| Postback fires → Supabase records revenue | Watchtower/Peter | ⏳ Blocked by above | — |
| **First dollar confirmed** | Fury | ⏳ | Target: Feb 19 |

### Mission 2: Lead Quality Pipeline
_No lead touches a buyer without enrichment and compliance pass_

| Step | Owner | Status |
|------|-------|--------|
| FastDebt API integration (enrichment) | Peter | ⏳ Blocked — no API creds |
| Compliance check on every lead (TSR/TCPA/state) | Shield | ⏳ Ready, needs leads |
| Lead scoring: A/B/C/D tier assignment | Scout | ⏳ Needs enrichment data |
| Route to correct buyer by debt profile + caps | Scout/Fury | ⏳ Logic built, needs live test |

### Mission 3: Buyer Relationship Foundation
_Revenue comes from buyers. No buyers, no business._

| Task | Status |
|------|--------|
| Map all 10 Everflow offers — URLs, caps, restrictions, schedules | ✅ Done |
| Confirm weekly caps with AK (50/week/offer baseline) | ✅ Done |
| First test delivery to NDR (offer 4905) | ⏳ Next |
| Build buyer acceptance rate tracking | ⏳ Watchtower |
| Negotiate cap increases after 2 weeks of consistent quality | ⏳ Future |
| Identify 2-3 new buyers outside Everflow | ⏳ Phase 2 |

## 📋 Daily CEO Checklist

Every single day. No exceptions.

1. **P&L snapshot** — Revenue, costs, margin. Even if all zeros — log it.
2. **Pipeline health** — Leads acquired, leads in compliance, leads delivered, leads confirmed.
3. **Agent accountability** — What did each agent deliver today? What didn't land?
4. **Blockers** — What's stuck? Who's stuck? What do they need?
5. **Budget burn** — How much of $5K spent? Projected runway?
6. **Decisions for Ocean/AK** — What needs approval? Package it: context + options + recommendation.
7. **Tomorrow's top 3** — Three things that will happen tomorrow, with owners.

## 📊 Key Metrics (Update Daily)

| Metric | Current | Target | Kill Threshold |
|--------|---------|--------|----------------|
| Leads acquired today | 0 | 10/day | — |
| Leads delivered today | 0 | 8/day (80% pass rate) | — |
| Conversions confirmed | 0 | 5/day | — |
| Revenue today | $0 | $150-250/day | — |
| CPL (all sources) | N/A | $8-15 | >$30 |
| Buyer acceptance rate | N/A | >80% | <60% |
| Shield block rate | N/A | <15% | >25% |
| Daily AI spend | ~$0 | <$10 | >$15 |
| Budget remaining | $5,000 | — | <$500 = FULL STOP |

## 🔥 Phase Gates — Non-Negotiable

| Phase | Gate Criteria | Status |
|-------|---------------|--------|
| **Phase 0** | DB live + first form filled + first lead stored | ✅ Complete |
| **Phase 1** | Scout→Shield→Deliver loop proven end-to-end with revenue | 🔄 In progress |
| **Phase 2** | 3+ consecutive days of positive unit economics | ⏳ |
| **Phase 3** | Scaling — Hawk spends real ad budget, Forge builds landing pages | ⏳ |

**Rule:** No agent works on Phase N+1 tasks until Phase N gate is passed. Fury enforces this. No exceptions, no "just this one thing." Phase discipline is budget discipline.

## 🚧 Current Blockers

| Blocker | Owner | Impact | Resolution Path |
|---------|-------|--------|----------------|
| AK go-ahead for live NDR submission | AK/Ocean | Blocks first revenue | Decision needed |
| FastDebt API credentials | AK | Blocks enrichment pipeline | AK to provide |
| DB logging 400 error on submissions | Peter/Watchtower | Blocks tracking | Schema fix needed |
| Vision model auth (401) | Ocean/Watchtower | Watchtower can't run as sub-agent | Config fix |

## 💀 Kill Criteria

Define "this isn't working" BEFORE it happens. No hoping.

- **Campaign CPL >$30 after 100 clicks** → Kill immediately, post-mortem
- **Buyer acceptance rate <50% for 3 consecutive days** → Pause delivery, investigate
- **Shield block rate >30%** → Source quality problem, Scout investigates
- **Daily AI spend >$15** → Something is looping, Watchtower kills it
- **$5K budget hits $4,500 with no revenue** → FULL STOP, strategy review with AK

## 📝 Standing Orders

1. **Revenue sequence discipline.** Every task must connect to revenue. If it doesn't, push back or defer.
2. **Evidence gate.** "Done" requires proof — URL, screenshot, DB record, test result.
3. **No silent failures.** If something breaks, it's in shared/CONTEXT.md within 30 minutes.
4. **Before closing every session:** Update shared/CONTEXT.md, memory/YYYY-MM-DD.md, and shared/KNOWLEDGE_HUB.md per shared/PLAYBOOK_RULES.md § MANDATORY CHECKPOINTS. No exceptions.

_The P&L doesn't care about your intentions. It only counts what shipped._
