# Project Ocean — Claude Code Instructions

## What This Is

Multi-agent lead generation system for **US debt relief** running on OpenClaw. 6 AI agents acquire, verify, comply, optimize, deliver, and monitor leads — all coordinated autonomously.

## Commands

```bash
# OpenClaw gateway
openclaw start          # Start all agents (reads config/openclaw.yaml)
openclaw stop           # Graceful shutdown
openclaw status         # Agent health + heartbeat status

# Docker (local dev)
docker compose up -d    # Start Supabase + services
docker compose down     # Stop everything

# Database
# Run db/schema.sql in Supabase SQL Editor to bootstrap
# Run db/seed.sql for test data
# Migrations go in db/migrations/
```

## Architecture

### Agent Roster

| Agent | Role | Model | Heartbeat | Key Tools |
|-------|------|-------|-----------|-----------|
| **Fury** | CEO — P&L, outreach, strategy | kimi-k2.5-thinking | 30m | web_search, supabase, everflow |
| **Scout** | Lead acquisition & enrichment | deepseek-v3 | 10m | stealth-browser, supabase, fast-debt-api |
| **Shield** | Compliance (TSR/FTC/TCPA) | kimi-k2.5-thinking | 5m | supabase |
| **Hawk** | Media buying & spend optimization | glm-4.7 | 15m | facebook-ads, everflow, revpie, supabase |
| **Signal** | CRO, delivery, call routing | deepseek-v3 | 5m | supabase, email-engine, ringba |
| **Watchtower** | System monitoring & alerting | gpt-5-nano | 10m | supabase |

### Hierarchy

- **Fury orchestrates** all agents and owns P&L decisions
- **Shield has compliance veto power** — no lead ships without Shield approval
- Don't scale spend without Fury's approval
- When in doubt, stop and ask Arif

### Model Routing

All models via **OpenRouter** (cost-optimized). Config in `config/openclaw.yaml` under `models.aliases`. Default model: `deepseek-v3-0324`.

## Key Files

```
SOUL.md                     # Top-level system persona (Mr. Ocean)
USER.md                     # Owner context (Arif Khan)
AGENTS.md                   # Team rules & safety protocols
HEARTBEAT.md                # Fury's standing orders per heartbeat
config/openclaw.yaml        # Agent config, models, tools, heartbeats
agents/<name>/SOUL.md       # Per-agent charter (personality + mission)
agents/<name>/IDENTITY.md   # Agent identity card
agents/<name>/TOOLS.md      # Agent-specific tool instructions
agents/<name>/HEARTBEAT.md  # Agent-specific heartbeat tasks
agents/<name>/memory/       # Per-agent memory files
db/schema.sql               # Full Supabase schema
db/seed.sql                 # Test seed data
db/migrations/              # Schema migrations
workflows/*.yaml            # YAML workflow definitions
skills/                     # Tool integrations (supabase, everflow, ringba, etc.)
```

## Database — Supabase PostgreSQL

### Core Tables

| Table | Purpose |
|-------|---------|
| `leads` | All acquired leads — source, PII, debt info, quality score/tier, status |
| `buyers` | Lead buyers — caps, payouts, terms, preferred hours |
| `campaigns` | Ad campaigns — source, spend, CPL (auto-calculated) |
| `deliveries` | Delivery attempts — lead→buyer, channel, payout, status |
| `pnl_daily` | Daily P&L — revenue, costs by category, gross profit, margin % |
| `compliance_log` | Audit trail — every compliance check with pass/flag/block |
| `agent_activity` | Agent action log — heartbeats, decisions, all agent events |

### Lead Pipeline States

`new` → `enriched` → `scored` → `delivered` or `rejected`

### Important

- All lead data stays in Supabase — nowhere else
- Agents use the **service role key** (full RLS bypass)
- Row Level Security enabled on all tables
- Buyer daily caps reset at midnight via cron

## Conventions

1. **SOUL.md = agent charter.** Each agent's personality, mission, and boundaries live in `agents/<name>/SOUL.md`. Read it before modifying any agent behavior.
2. **YAML workflows** define multi-step processes (lead acquisition, compliance check, buyer delivery, campaign optimization, daily standup).
3. **Personality-driven agents.** Agents have attitude, voice, and blind spots — this is intentional, not a bug.
4. **Cheap models via OpenRouter.** Budget is tight. Use the cheapest model that can do the job. Don't upgrade without justification.
5. **Memory files** track agent state and learnings across sessions. Always check `memory/` for context.
6. **Credentials live in `.env` only.** Never hardcode keys. Never share outside this workspace.

## Owner Context — Arif Khan

- **Non-technical founder.** Explain in dollars and margins, not APIs and endpoints.
- **$5K testing budget.** Every dollar needs ROI justification.
- **Thinks in:** CPL, margin %, conversion rates, revenue
- **Hates:** Fluff, excuses, vanity metrics
- **Loves:** Speed, directness, honesty, numbers
- **Timezone:** Asia/Kolkata (GMT+5:30)
- When he says "do it" — do it. Don't ask again.
- When he asks "what do you think?" — give a real opinion with numbers.
