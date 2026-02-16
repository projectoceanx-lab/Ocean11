# MEMORY.md — Project Ocean Knowledge Base

_Everything Mr. Ocean needs to know. Read this every session._

---

## What is Project Ocean?

US debt relief lead generation — the full Zappian playbook rebuilt with AI agents. We acquire leads (form filling, traffic, email), enrich & score them, compliance-check them, and deliver to buyers for payout. The delta between acquisition cost (CPL) and buyer payout is our margin.

This is NOT a startup experiment. Arif ran this exact business model at Zappian Media for 7.5 years with 3,100+ publishers generating leads in personal loans, insurance, auto finance, and debt for the US market. We're digitizing a proven playbook.

## Why Now?

Arif's other ventures (Home Away STR, HostAI SaaS) are 6+ months out — needs visa, bank loan (requires 6mo salary history), and summer is STR low season. Ocean bridges the income gap with a business model Arif already knows cold.

## Budget

- **$5K testing budget** — tight, every dollar tracked
- **Subscriptions:** Claude Max (Opus 4.6 for Captain) + ChatGPT Max (GPT-5.2 for Shield) — both unlimited, $0 marginal cost
- **Phase 1:** Local (laptop/Mac mini), ~$20-50/mo in API costs (only worker agents: Scout, Signal, Hawk, Watchtower)
- **Phase 2:** Cloud (Railway/Vercel) when unit economics proven, ~$200-500/mo
- Zero cloud spend until we PROVE the system works locally

## Architecture — 4-Layer Hybrid

Built by synthesizing patterns from 4 real-world multi-agent systems:

1. **Pipelines (from Antfarm by Ryan Carson)** — Deterministic YAML workflows. Same steps, same order, every time. No hoping agents coordinate loosely. Each workflow is defined step-by-step with verification gates.

2. **Autonomy (from VoxYZ by Vox)** — Closed-loop autonomy within guardrails. Agents can self-heal, retry, and adapt — but within defined cap gates (spend limits, volume limits). Triggers + reaction matrix pattern.

3. **Visibility (from Mission Control by Bhanu Teja)** — Full observability. LangSmith traces every agent action in Phase 1. PostHog tracks user/lead events in Phase 2. Daily standup workflow aggregates all agent reports.

4. **Security (from SHIELD.md by Thomas Roccia)** — Per-agent security policies. Shield has veto power on compliance. Each agent has defined allowed/blocked actions. Threat matching on suspicious patterns.

**Key tech decisions:**
- **Supabase** over Convex/SQLite — real-time, multi-agent concurrent access, free tier, scales to Pro
- **LangSmith** for Phase 1 observability — tracks agent events (right for no-user phase)
- **PostHog** added Phase 2 — tracks user/lead events
- **OpenClaw** as the orchestration layer — agents are sessions, heartbeats drive polling, skills provide tools

## The 6 Agents

Consolidated from original 10 (Arif's decision: "more are tough to manage").

| Agent | Role | Model | Cost/M tokens |
|---|---|---|---|
| **CAPTAIN** 🎖️ | CEO — outreach, sales, P&L ownership, strategy. Directs, doesn't execute. | Claude Opus 4.6 (fallback: GPT-5.3 Codex) | $15 in / $75 out |
| **SCOUT** 🔍 | Lead acquisition + delivery. Operates form fillers, enriches, scores, delivers to buyers. Full pipeline. | DeepSeek V3.2 | $0.25 / $0.38 |
| **SHIELD** 🛡️ | Compliance — TSR, FTC, TCPA, state rules. Has VETO power. Reviews all copy + code before launch. | GPT-5.2 (high thinking) | $2.00 / $8.00 |
| **HAWK** 🦅 | Media buying (FB, RevPie) + email marketing (copy, sequences, deliverability) + spend optimization. | GLM-4.7 | ~$0.50 / $1.00 |
| **FORGE** 🔥 | CRO, funnel strategy, offer wall design, landing page copy, A/B test specs. Specs it, Peter builds it. | DeepSeek V3.2 | $0.25 / $0.38 |
| **PETER** 🛠️ | CTO — all engineering. Website building, API integrations, browser automation, deployment, data pipelines. Uses Codex/Claude CLI. | Codex CLI (local) | $0 (CLI) |
| **WATCHTOWER** 🗼 | System monitoring, health checks, alerting. Nocturnal sentinel. | GPT-5-nano | $0.05 / $0.40 |

### Built-in Tensions (by design)
- **HAWK vs SHIELD** — Speed vs compliance. Hawk wants to scale spend and blast emails, Shield wants to verify everything. This tension is healthy.
- **FORGE vs HAWK** — Forge protects buyer relationships and sender reputation. Hawk wants leads delivered NOW before they go cold.
- **HAWK (email) vs SHIELD** — Hawk pushes email volume, Shield enforces CAN-SPAM and complaint rate limits.
- **CAPTAIN arbitrates** — When agents disagree, Captain decides based on P&L impact.

### Why These Models?
- **Claude Opus 4.6** — for Captain because CEO decisions need the best strategic reasoning; GPT-5.3 Codex as fallback
- **GPT-5.2 (high thinking)** — for Shield because compliance decisions are the most consequential in the operation; high thinking budget gives depth for regulatory edge cases and state-specific rules
- **DeepSeek V3.2** (#40 Arena) — for Scout & Signal because they need reliable execution at low cost
- **GLM-4.7** (#22 Arena, #21 math) — for Hawk because media buying is math-heavy
- **GPT-5-nano** (#129 Arena) — for Watchtower because monitoring just needs "good enough" at minimum cost
- **MiniMax M2.5 rejected** — M2.1 only #82 on Arena, M2.5 benchmarks self-reported/unverified
- This hybrid saves **95%+ vs using Claude Opus for everything**

## The Lead Flow — How We Actually Make Money

**This is the real pipeline. Not theory — this is the Zappian playbook.**

```
RevPie (buy aged leads) → Our Website (landing/offer wall)
         ↓
   FastDebt API (enrich: debt type, amount, composition)
         ↓
   Quality Filter (unsecured debt? CC primary? $10K+?)
         ↓
   Offer Wall (show personalized offers on our site)
         ↓
   Scout Form Filler (fill buyer forms with TOP quality leads only)
         ↓
   Buyer (JGW $25, NDR $50, FDR $60) → Revenue
```

**Key insight:** We don't fill forms to GET leads. We fill forms to DELIVER leads. The form filler is the last mile — delivering pre-qualified, enriched leads to buyers.

**Key insight #2: Dedup + routing is the brain.** Most leads across RevPie and FB will overlap. Before every fill, check the `deliveries` table: has this lead already been sent to this buyer? If yes, route to the next eligible buyer who hasn't seen it. Without dedup, we're burning acquisition dollars sending duplicates that get rejected. The routing intelligence — which lead goes to which buyer, based on debt profile + delivery history — is what makes the difference between profitable and bankrupt.

## Lead Sources — Three Channels

### Source 1: RevPie (Aged Leads)
- Buy aged leads in bulk at low cost ($2-5 per lead)
- Land on our website → enrich → filter → deliver
- Volume play, lower quality, needs heavy enrichment/filtering

### Source 2: Facebook Ads
- Drive traffic to our website/landing pages
- Higher cost per lead ($15-35) but fresher
- Needs creative, compliance review, landing page optimization

### Source 3: OUR OWN Payday/Personal Loan Websites (ZERO COST)
- We own and operate payday + personal loan sites
- Applicants fill loan applications — some select "debt consolidation" as loan purpose
- **"Debt consolidation" = buying signal** — they have high debt, they're seeking solutions
- These leads are pre-qualified: they self-selected, we already have their data (name, phone, email, income)
- **Zero acquisition cost** — they're already in our system
- Backend feeds these leads directly into Ocean DB
- FastDebt enriches → Scout delivers to matching buyer
- **Caveat: quality is low.** Most payday borrowers want $200-$500, wrong debt type (payday loans, mortgages). Few will have qualifying CC debt.
- **Primary value: test volume.** Use these leads to validate dedup logic, enrichment pipeline, and routing before spending on RevPie/FB.
- When a qualifying lead DOES come through, it's pure margin ($0 CPL).

### Source Priority
1. **Own loan sites** (zero cost, pre-qualified, highest margin)
2. **RevPie** (low cost, aged, volume play)
3. **Facebook** (higher cost, needs optimization, scale channel)

## The 7 Pillars (Zappian Playbook Digitized)

1. **Websites** — OUR landing pages + offer wall. Leads land here first. Compliant disclaimers, trust signals.
2. **RevPie/FB traffic** — Buy aged leads from RevPie, drive FB traffic to our site
3. **FastDebt enrichment** — MANDATORY. Confirms debt type, amount, composition before any delivery
4. **Email triggers** — Welcome sequences, follow-ups, re-engagement (warmed domains required)
5. **Offer wall** — Personalized offers on OUR site based on enriched lead profile
6. **Scout form filler** — Automated delivery to buyers by filling THEIR forms with our best leads
7. **Ringba call tracking** — Inbound/outbound call routing to buyers, IVR, recording

## Existing Assets (Arif Already Has)

- **Everflow** — RevvMind account (offer tracking, conversion postbacks)
- **Salesforce/ESPs** — Warmed sender infrastructure
- **RevPie** — Aged account with traffic history
- **Facebook Ads** — Old account (established, not new)
- **Active buyer relationships** — From Zappian era
- **Domain portfolio** — Needs new domains for Ocean (warming required)

## Compliance — Non-Negotiable

Shield enforces these. No exceptions.

- **Telemarketing Sales Rule (TSR)** — FTC regulation on debt relief marketing. No upfront fees. Must disclose material terms.
- **FTC Act Section 5** — No unfair/deceptive practices. All claims must be substantiated.
- **TCPA** — Telephone Consumer Protection Act. Prior express consent required for calls/texts. Do-not-call compliance.
- **CAN-SPAM** — Every email must have unsubscribe link, physical address, honest subject lines.
- **State-level rules** — Some states (NY, CA, TX) have additional debt relief regulations. Shield checks per-state.

See `docs/COMPLIANCE_RULES.md` for full details.

## Phase 1 Strategy — Start Small, Prove It

**Start with Scout + Shield ONLY:**
1. Scout fills one test form → verifies DB storage → enriches → scores
2. Shield compliance-checks the lead
3. If that loop works clean, add Signal for delivery
4. Then Hawk for traffic optimization
5. Captain oversees everything
6. Watchtower monitors health

**Don't build all 6 agents at once.** Prove unit economics with the first 2, then scale.

## Key Files in This Repo

- `agents/` — Each agent's SOUL.md (personality), config.yaml (model + tools), MISSIONS.md (objectives)
- `db/schema.sql` — Full Supabase PostgreSQL schema (leads, buyers, campaigns, deliveries, P&L, compliance log)
- `db/seed.sql` — Test data to get started
- `workflows/` — YAML pipelines for each major process
- `skills/` — Tool integrations (stealth browser, Supabase, Everflow, Ringba, etc.)
- `docs/` — Architecture, compliance rules, buyer playbook, runbook, model strategy
- `templates/` — Landing page, offer wall, email sequences
- `config/credentials.md` — Checklist of all credentials needed (track what's provided vs pending)
- `.env.example` — All environment variables with placeholders

## Credentials Status

Track in `config/credentials.md`. As Arif provides each one, update the checklist and add to `.env`.

## Stealth Browser — Critical for Scout

Lead Bot needs stealth browsing (form filling on debt relief sites). Regular Playwright/Puppeteer gets detected.

**Solution:** Camoufox (Firefox-based anti-detection) + residential proxies
- NOT Playwright (detectable)
- NOT undetected-chromedriver (increasingly caught)
- Camoufox mimics real Firefox fingerprints
- Residential proxies rotate US IPs

### Human Behavior Simulation — MANDATORY (from AK, Feb 16 2026)

**Traffic to buyer offers MUST look human, not bot.** Buyers have fraud detection. Bot-pattern leads get flagged/rejected = $0 revenue.

Every form fill session must include randomized human-like behavior:
- **Typing:** Variable keystroke delays (burst typing + pauses, not uniform intervals)
- **Mouse:** Natural curved movements, not straight-line teleportation to fields
- **Scrolling:** Random scroll patterns — sometimes past the form, back up, variable speed
- **Navigation:** Occasionally click non-form elements (logo, nav links), browse around before filling
- **Hesitation:** Click a field, pause, maybe click another first, come back
- **Corrections:** Sometimes type wrong → backspace → retype (human error simulation)
- **Dwell time:** 30 seconds to 3+ minutes per page, randomized
- **Tab abandonment:** ~10-15% of sessions start but don't finish (mimics real user behavior)
- **Back/forth:** Sometimes go back a page, re-read, then proceed
- **Session uniqueness:** No two fills should have the same behavioral fingerprint — full entropy

This is NOT a nice-to-have. This is core to Scout's architecture. Build the behavioral randomizer FIRST, then the form filler on top of it.

## Domain Warming Strategy

New domains need 4-6 weeks warming before full volume:
- Week 1-2: 50 emails/day, increase 20% weekly
- Week 3-4: 500-1000/day
- Week 5-6: 5000+/day
- Monitor: bounce rate <2%, complaint rate <0.1%
- Kill switch: if complaint rate >0.3%, pause ALL sends

## Lead Quality & Debt Economics — FROM AK

**This is the single most important business logic in the operation.**

### Only Unsecured Debt Qualifies
- ✅ **Credit card debt** — primary component (~70-80% of what buyers want)
- ✅ **Personal loan debt** — secondary, accepted
- ❌ Mortgage, student loans, auto loans, medical debt — ALL rejected

### CPA = Quality Signal, Not Profit
- $60 CPA = buyer wants $30K+ unsecured debt leads
- $22-25 CPA = buyer accepts $10K+ unsecured debt leads
- **Don't chase highest CPA. Chase quality match.**
- A $25 CPA lead that converts > a $60 CPA lead that gets rejected

### FastDebt Enrichment is Mandatory
Every lead MUST be enriched before delivery to confirm:
1. Total unsecured debt amount
2. Debt composition (% credit card vs personal loan)
3. Number of accounts
**No enrichment = no delivery. No exceptions.**

### Lead Routing Logic
- Lead with $12K CC debt → JGW ($22-25 CPA tier)
- Lead with $35K CC debt → NDR/FDR ($50-60 CPA tier)
- Lead with mostly mortgage debt → REJECT (wrong debt type)

## Revenue Model

```
Revenue = (Leads delivered × Buyer payout) - (Traffic cost + Call cost + Enrichment cost + AI cost + Other)
```

Target metrics:
- CPL (cost per lead): $8-15
- Buyer payout: $20-40 per qualified lead
- Target margin: 15-25%
- Break-even: ~200 leads/month at 20% margin

---

_Updated: Feb 14, 2026. Update this file as decisions evolve._
