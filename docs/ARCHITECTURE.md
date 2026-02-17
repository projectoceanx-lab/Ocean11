# Project Ocean — Architecture

## 4-Layer Hybrid Architecture

### Layer 1: Pipelines (Deterministic Workflows)
Structured YAML workflows define the core business processes. Each workflow is a sequence of steps with clear inputs, outputs, and error handling. Agents execute these workflows but can adapt within guardrails.

**Workflows:**
- `lead-acquisition.yaml` — Scout's form → enrich → score pipeline
- `compliance-check.yaml` — Shield's regulatory validation
- `buyer-delivery.yaml` — Signal's matching and routing
- `campaign-optimization.yaml` — Hawk's analytics and budget optimization
- `content-growth-loop.yaml` — Hawk + Shield dual-track content loop (draft → gate → publish → learn)
- `daily-standup.yaml` — Fury's daily orchestration

### Layer 2: Autonomy (Agent Intelligence)
Each agent has a SOUL.md defining its personality, expertise, and decision-making authority. Agents can:
- Make tactical decisions within their domain
- Escalate uncertain situations to Fury
- Adapt workflows based on real-time conditions
- Learn from outcomes (quality scores, delivery rates, buyer feedback)

**Decision Authority:**
| Agent | Can Decide | Must Escalate |
|-------|-----------|---------------|
| Fury | Strategy changes, buyer relationships | Budget > $500/day, new verticals |
| Scout | Form selection, enrichment priority | New data sources, quality threshold changes |
| Shield | Block/flag leads | Regulatory ambiguity, new state rules |
| Hawk | Budget shifts < 20%, pause campaigns | Budget shifts > 20%, new channels |
| Signal | Routing priority, delivery timing | New buyers, pricing changes |
| Watchtower | Alert severity, monitoring frequency | System-wide issues |

### Layer 3: Visibility (Observability)
Every action is logged and traceable:
- **agent_activity** table — All agent actions with JSONB details
- **compliance_log** — Full audit trail for regulatory compliance
- **pnl_daily** — Financial tracking with cost breakdown
- **Watchtower** — Real-time monitoring with alert thresholds
- **LangSmith** (optional) — LLM trace debugging and cost tracking

### Layer 4: Security (Compliance & Access Control)
- **Shield** has veto power over all lead deliveries
- **Supabase RLS** — Row-level security on all tables
- **API keys** — Stored in `.env`, never in code or logs
- **Proxy rotation** — No direct IP exposure for form filling
- **Audit trail** — Every compliance check logged with timestamp and reason

## Data Flow

```
[Traffic Sources]                    [Buyers]
  Facebook Ads ─┐                  ┌─ Debt Solutions Inc
  RevPie ───────┤                  ├─ Freedom Financial
  Email ────────┤                  └─ (more buyers)
  Organic ──────┘                       ↑
        ↓                               │
   ┌─────────┐   ┌──────────┐   ┌──────────┐
   │  SCOUT  │──→│  SHIELD  │──→│  SIGNAL  │
   │ Acquire │   │ Comply   │   │ Deliver  │
   │ Enrich  │   │ Validate │   │ Route    │
   │ Score   │   │ Approve  │   │ Confirm  │
   └─────────┘   └──────────┘   └──────────┘
        ↑              ↑              │
        │              │              ↓
   ┌─────────┐   ┌──────────┐   ┌──────────┐
   │  HAWK   │   │ CAPTAIN  │←──│   P&L    │
   │ Optimize│──→│ Strategy │   │ Revenue  │
   │ Analyze │   │ Decide   │   │ Costs    │
   └─────────┘   └──────────┘   └──────────┘
                      ↑
                 ┌──────────┐
                 │WATCHTOWER│
                 │ Monitor  │
                 │ Alert    │
                 └──────────┘
```

## Technology Stack

| Component | Technology | Cost (Phase 1) |
|-----------|-----------|----------------|
| Orchestration | OpenClaw | Free |
| Database | Supabase (PostgreSQL) | Free tier |
| AI Models | OpenRouter → Kimi, DeepSeek, GLM, GPT-5-nano | ~$50-100/mo |
| Browser | Camoufox | Free (open source) |
| Proxies | Smartproxy / Bright Data | ~$50-100/mo |
| Call Routing | Ringba | Pay per call |
| Ad Tracking | Everflow | ~$200/mo |
| Email | SendGrid / Mailgun | Free tier → $20/mo |
| Enrichment | Fast Debt API | ~$0.10-0.50/call |

## Phase 1 → Phase 2 Migration Path

**Phase 1 (Local Laptop):**
- All agents run locally via OpenClaw
- Supabase free tier (10K rows, 500MB)
- Small test budgets ($50-100/day)
- Manual buyer onboarding

**Phase 2 (Cloud):**
- Agents on cloud VPS (Railway / Fly.io / dedicated)
- Supabase Pro ($25/mo, 8GB, no row limits)
- Scaled budgets ($500-1000/day)
- Automated buyer matching and delivery
- Multiple verticals (tax debt, student loans)
