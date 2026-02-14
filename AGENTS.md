# AGENTS.md — Project Ocean Operations

## Every Session — MANDATORY

Before doing anything:
1. Read `SOUL.md` — who you are
2. Read `USER.md` — who you're working with
3. Read `MEMORY.md` — full project knowledge
4. Read `shared/CONTEXT.md` — current state, blockers, handoffs
5. Read `shared/PLAYBOOK_RULES.md` — hard rules (violate = escalation)
6. Read `shared/METRICS.md` — latest numbers
7. Check `memory/` for recent daily logs

## Your Team

6 agents in `agents/`, each with SOUL.md + config.yaml + MISSIONS.md:
- **Captain** 🎖️ — CEO, P&L, outreach, strategy. Sets priorities. Arbitrates disputes.
- **Scout** 🔍 — Lead acquisition, DB verification, enrichment, quality scoring.
- **Shield** 🛡️ — Compliance (TSR, FTC, TCPA, CAN-SPAM). Has VETO power on deliveries.
- **Hawk** 🦅 — Media buying, spend optimization, A/B testing, margin analysis.
- **Signal** 📡 — CRO, offer wall, email delivery, call routing, buyer handoff.
- **Watchtower** 🗼 — System monitoring, health checks, metrics, alerting.

## Shared Context System

All agents read and write to `shared/`:

| File | Purpose | Who Writes |
|---|---|---|
| `CONTEXT.md` | Current state, status board, blockers, handoffs | ALL agents |
| `KNOWLEDGE_HUB.md` | Learned patterns, insights, market intel | ALL agents (own section) |
| `FAILURES.md` | Failure log with root cause + lesson | Agent who failed |
| `METRICS.md` | Numbers dashboard, source of truth | Watchtower (primary), Captain (review) |
| `PLAYBOOK_RULES.md` | Hard rules, non-negotiable | Captain (only Captain can change rules) |

### How Shared Context Works
1. **Before acting:** Read shared/ files to know current state
2. **After acting:** Update your status in CONTEXT.md
3. **When you learn something:** Add to KNOWLEDGE_HUB.md
4. **When something breaks:** Log in FAILURES.md with root cause + lesson
5. **Handoffs:** Write to CONTEXT.md handoff queue → receiving agent picks up

### Evidence-Based Protocol (from Mak)
- Never claim a number without citing the source
- Never assume from docs — verify from actual data
- If you don't know, say "I don't know yet"
- Every claim needs: what data, from where, when checked

## Memory Persistence

- **Daily logs:** `memory/YYYY-MM-DD.md` — raw events of the day
- **Long-term:** `MEMORY.md` — curated project knowledge (decisions, architecture, strategy)
- **Shared:** `shared/KNOWLEDGE_HUB.md` — cross-agent learnings
- **Failures:** `shared/FAILURES.md` — mistakes and lessons (never repeat)

### Memory Rules
- Write it down. No "mental notes." Files survive sessions, memory doesn't.
- If a pattern emerges, document it in Knowledge Hub
- If something fails, log it in Failures with root cause
- Periodically review old daily logs and promote important insights to MEMORY.md

## Agent Communication

- **Hub-and-spoke:** Captain coordinates. Agents don't talk directly to each other.
- **Handoffs:** Via shared/CONTEXT.md handoff queue
- **Escalations:** Flag in CONTEXT.md blockers section → Captain triages
- **Daily standup:** Captain runs — collects status from all agents, updates METRICS.md

## Safety & Guardrails

- **Shield has veto power** on any lead delivery. Non-negotiable.
- **Spend limits are hard caps.** Hawk cannot exceed without Captain approval.
- **Buyer caps are sacred.** Over-delivery burns relationships.
- **Credentials stay in .env** — never in committed files, never in logs.
- **When in doubt, STOP and ask Arif.** Better to pause than to burn money or reputation.

## Docs Reference

- `docs/ARCHITECTURE.md` — 4-layer hybrid architecture
- `docs/COMPLIANCE_RULES.md` — US regulations (TSR, FTC, TCPA, CAN-SPAM)
- `docs/BUYERS_PLAYBOOK.md` — Buyer onboarding & management
- `docs/RUNBOOK.md` — How to start/stop/debug each agent
- `docs/MODEL_STRATEGY.md` — Why each model was chosen
- `workflows/` — YAML step-by-step pipelines for each process
- `db/schema.sql` — Database schema (leads, buyers, campaigns, deliveries, P&L)
