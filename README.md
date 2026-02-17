# 🌊 Project Ocean

**US Debt Relief Lead Generation — Powered by 6 AI Agents on OpenClaw**

Project Ocean is an automated lead generation business for the US debt relief vertical. Six specialized AI agents handle everything from lead acquisition to buyer delivery, compliance checking, campaign optimization, and P&L tracking.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   CAPTAIN                        │
│         CEO / Orchestrator / Strategy            │
├────────┬────────┬────────┬────────┬─────────────┤
│ SCOUT  │ SHIELD │  HAWK  │ SIGNAL │ WATCHTOWER  │
│ Leads  │Comply  │ Media  │Deliver │  Monitor    │
└────────┴────────┴────────┴────────┴─────────────┘
         ↕            ↕         ↕
    [Supabase]   [Everflow]  [Ringba]
    [FastDebt]   [Facebook]  [ESP]
    [RevPie]     [Camoufox]
```

## Quick Start

### Prerequisites
- macOS or Linux
- [OpenClaw](https://openclaw.com) installed
- API keys (see `.env.example`)

### Setup

```bash
# 1. Clone this repo
git clone https://github.com/ak-eyther/project-ocean.git
cd project-ocean

# 2. Copy and fill in your credentials
cp .env.example .env
# Edit .env with your actual API keys

# 3. Set up the database
# Create a Supabase project at https://supabase.com
# Run db/schema.sql in the SQL editor

# 4. Start OpenClaw with Ocean config
openclaw gateway start
# Agents will initialize automatically
```

For detailed step-by-step instructions, see [SETUP.md](SETUP.md).

## Agents

| Agent | Role | Model | Cost (in/out per 1M tokens) |
|-------|------|-------|-----------------------------|
| **Fury** | CEO, strategy, P&L, outreach | kimi-k2.5-thinking | $0.45 / $2.25 |
| **Scout** | Lead acquisition, enrichment, scoring | deepseek-v3-0324 | $0.25 / $0.38 |
| **Shield** | Compliance (TSR, FTC, TCPA, state) | kimi-k2.5-thinking | $0.45 / $2.25 |
| **Hawk** | Media buying, CRO, analytics | glm-4.7 | ~$0.10 / $0.10 |
| **Signal** | Delivery, call routing, email, buyer handoff | deepseek-v3-0324 | $0.25 / $0.38 |
| **Watchtower** | Monitoring, alerts, observability | gpt-5-nano | $0.05 / $0.40 |

## Project Structure

```
ocean/
├── agents/          # Agent SOUL.md, configs, missions
├── config/          # OpenClaw config, credentials checklist
├── db/              # PostgreSQL schema, seeds, migrations
├── docs/            # Architecture, compliance, runbooks
├── memory/          # Agent memory (gitignored)
├── skills/          # Tool integrations (Supabase, Everflow, etc.)
├── templates/       # Landing pages, emails, offer walls
└── workflows/       # YAML pipeline definitions
```

## Phase Plan

- **Phase 1** (Current): Local laptop, $5K test budget, prove unit economics
- **Phase 2**: Cloud deployment, scale campaigns, expand verticals

## Budget

- AI costs: ~$50-100/month (cheap models via OpenRouter)
- Media: $3-4K test spend across Facebook + RevPie + email
- Tools: Supabase (free tier), Everflow, Ringba, FastDebt API
- Target: $15-25 CPL, $50-75 payout per lead → 2-3x ROI

## Docs

- [Architecture](docs/ARCHITECTURE.md)
- [Compliance Rules](docs/COMPLIANCE_RULES.md)
- [Buyer's Playbook](docs/BUYERS_PLAYBOOK.md)
- [Runbook](docs/RUNBOOK.md)
- [Model Strategy](docs/MODEL_STRATEGY.md)

## License

Private — All rights reserved.
