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
| **CAPTAIN** | CEO — outreach, sales, P&L ownership, cost/spend analysis, strategy, ruthless executive | Claude Opus 4.6 (fallback: GPT-5.3 Codex) | $15 in / $75 out |
| **SCOUT** | Lead acquisition + DB verification + enrichment validation + quality scoring per vertical | DeepSeek V3.2 | $0.25 / $0.38 |
| **SHIELD** | Compliance — TSR, FTC, TCPA, state rules. Has VETO power. | GPT-5.2 (high thinking) | $2.00 / $8.00 |
| **HAWK** | Media buying + quant optimization + spend analysis. Gambler + quant + scientist. | GLM-4.7 | ~$0.50 / $1.00 |
| **SIGNAL** | CRO + offer wall + email deliverability + call routing + buyer handoff. Conversion obsessive. | DeepSeek V3.2 | $0.25 / $0.38 |
| **WATCHTOWER** | System monitoring, health checks, alerting. Nocturnal sentinel. | GPT-5-nano | $0.05 / $0.40 |

### Built-in Tensions (by design)
- **HAWK vs SHIELD** — Speed vs compliance. Hawk wants to scale spend, Shield wants to verify everything. This tension is healthy.
- **SIGNAL vs HAWK** — Signal protects sender reputation and buyer relationships. Hawk wants leads delivered NOW before they go cold.
- **CAPTAIN arbitrates** — When agents disagree, Captain decides based on P&L impact.

### Why These Models?
- **Claude Opus 4.6** — for Captain because CEO decisions need the best strategic reasoning; GPT-5.3 Codex as fallback
- **GPT-5.2 (high thinking)** — for Shield because compliance decisions are the most consequential in the operation; high thinking budget gives depth for regulatory edge cases and state-specific rules
- **DeepSeek V3.2** (#40 Arena) — for Scout & Signal because they need reliable execution at low cost
- **GLM-4.7** (#22 Arena, #21 math) — for Hawk because media buying is math-heavy
- **GPT-5-nano** (#129 Arena) — for Watchtower because monitoring just needs "good enough" at minimum cost
- **MiniMax M2.5 rejected** — M2.1 only #82 on Arena, M2.5 benchmarks self-reported/unverified
- This hybrid saves **95%+ vs using Claude Opus for everything**

## The 7 Pillars (Zappian Playbook Digitized)

1. **Websites** — Landing pages with debt relief forms, compliant disclaimers, trust signals
2. **FB/RevPie traffic** — Paid acquisition via Facebook Ads and RevPie aged leads
3. **Email triggers** — Welcome sequences, follow-ups, re-engagement (warmed domains required)
4. **Fast Debt API enrichment** — Income verification, employment status, debt validation
5. **Ringba call tracking** — Inbound/outbound call routing to buyers, IVR, recording
6. **Offer wall** — Personalized offers based on lead profile (debt amount, type, state)
7. **Lead delivery bot** — Automated handoff to buyers via API/email/call

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

## Domain Warming Strategy

New domains need 4-6 weeks warming before full volume:
- Week 1-2: 50 emails/day, increase 20% weekly
- Week 3-4: 500-1000/day
- Week 5-6: 5000+/day
- Monitor: bounce rate <2%, complaint rate <0.1%
- Kill switch: if complaint rate >0.3%, pause ALL sends

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
