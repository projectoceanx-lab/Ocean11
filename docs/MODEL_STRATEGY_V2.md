# Model Strategy V2 — Capability-Mapped Model Selection

_Updated Feb 14, 2026. Models chosen by matching agent capabilities to model strengths._

## Principle

Each agent has a unique job requiring specific capabilities. The best model is the one whose strengths align with the agent's core needs — not the cheapest, not the most expensive, but the most capable for that exact role.

---

## Model Assignments

### Captain → Kimi K2.5 Thinking
**Cost:** $0.45 / $2.25 per 1M tokens | **Context:** 262K

| Capability Needed | Kimi K2.5 Fit |
|-------------------|---------------|
| Strategic reasoning | ✅ #4 reasoning on Arena |
| P&L analysis | ✅ Strong analytical thinking |
| Buyer negotiation (drafting emails) | ✅ Good language generation |
| Multi-agent coordination | ✅ Complex planning |
| Decision-making under uncertainty | ✅ Explicit thinking chains |

**Why not upgrade?** Captain doesn't need vision, code, or massive context. Kimi K2.5's reasoning is top-tier at 10x less than Opus. The right model.

---

### Scout → Claude Sonnet 4.5
**Cost:** $3.00 / $15.00 per 1M tokens | **Context:** 1M

| Capability Needed | Sonnet 4.5 Fit |
|-------------------|----------------|
| Tool use / function calling | ✅ Best-in-class tool use |
| Code understanding (DOM, selectors, HTML) | ✅ Excellent code comprehension |
| Vision (form layouts, CAPTCHA, screenshots) | ✅ Native vision support |
| Structured output (JSON, consistent formats) | ✅ Highly reliable formatting |
| Fast adaptation (form changes, new sites) | ✅ Strong reasoning + speed |
| High reliability (97%+ accuracy needed) | ✅ Lowest error rate on structured tasks |

**Why Sonnet 4.5 over Haiku 4.5?** Scout is the revenue engine. Every form filled wrong = wasted money downstream. Sonnet's vision capability is critical — Scout needs to interpret form layouts, detect CAPTCHAs from screenshots, and understand page structure visually. Haiku can't do that.

**Why not GPT-5.1?** Sonnet 4.5 has better tool use reliability and lower hallucination rate on structured tasks. For form filling where precision matters more than creativity, Sonnet is the benchmark.

---

### Shield → Kimi K2.5 Thinking
**Cost:** $0.45 / $2.25 per 1M tokens | **Context:** 262K

| Capability Needed | Kimi K2.5 Fit |
|-------------------|---------------|
| Legal text interpretation | ✅ Deep reasoning chains |
| Multi-step compliance analysis | ✅ Explicit thinking process |
| Conservative judgment | ✅ Deliberate, not impulsive |
| State-specific rule application | ✅ Can hold 50-state rules in context |
| Structured decision output (pass/flag/block) | ✅ Consistent formatting |
| Edge case handling | ✅ Reasoning model excels here |

**Why Kimi over Sonnet/Opus?** Compliance is pure reasoning — no vision, no code, no tool use beyond database reads. Kimi K2.5 is #4 on reasoning benchmarks. Paying $3-25/M for capabilities Shield doesn't need is waste. Kimi at $0.45/$2.25 gives Shield everything it needs.

**Fallback:** For genuine legal edge cases Shield can't resolve, escalate to Captain (also Kimi K2.5) for a second opinion. If both are uncertain, escalate to AK.

---

### Hawk → GLM-4.7
**Cost:** $0.40 / $1.50 per 1M tokens | **Context:** 202K

| Capability Needed | GLM-4.7 Fit |
|-------------------|-------------|
| Statistical analysis (significance tests) | ✅ #21 math Arena |
| Financial modeling (CPL, ROI, margin) | ✅ Strong numerical reasoning |
| Multi-variable budget optimization | ✅ Analytical capability |
| Campaign data interpretation | ✅ Good with tabular data |
| Fast decisions | ✅ Efficient inference |
| Ad creative evaluation | ⚠️ Adequate, not exceptional |

**Why GLM-4.7?** Media buying is math. GLM-4.7 was built for analytical and mathematical tasks. It's the most capable math model at this price point. The only weakness is creative evaluation — but Hawk's creative decisions should be data-driven (test results), not gut-driven.

**Upgrade trigger:** If Hawk's recommendations lead to losses 3 times in a row, upgrade to GPT-5.1 ($1.25/$10.00) for stronger general reasoning.

---

### Signal → GPT-5.1
**Cost:** $1.25 / $10.00 per 1M tokens | **Context:** 400K

| Capability Needed | GPT-5.1 Fit |
|-------------------|-------------|
| Natural language generation (buyer emails) | ✅ Excellent writing quality |
| Personalization (per-buyer, per-lead messaging) | ✅ Strong contextual adaptation |
| Structured execution (routing logic) | ✅ Reliable function calling |
| Relationship memory (buyer prefs in context) | ✅ 400K context handles it |
| Email copy quality | ✅ Best-in-class generation |
| CRO analysis | ✅ Good analytical capability |

**Why GPT-5.1 over MiniMax M2.5?** Signal is the face of our operation to buyers. The quality of buyer-facing emails, delivery notifications, and relationship communications directly affects trust, acceptance rates, and payout negotiations. GPT-5.1's writing quality and personalization capability are significantly better than M2.5. When a buyer reads our delivery email, it needs to feel professional and human — not templated.

**Why not Sonnet 4.5?** Sonnet is better at tool use and code, which Signal doesn't need. GPT-5.1 is stronger at natural, personalized writing — which Signal needs most.

---

### Watchtower → GPT-5-nano
**Cost:** $0.05 / $0.40 per 1M tokens | **Context:** 400K

| Capability Needed | GPT-5-nano Fit |
|-------------------|----------------|
| Threshold comparison | ✅ Basic reasoning sufficient |
| Trend detection | ✅ Can identify simple patterns |
| Alert generation | ✅ Concise output |
| Fast checks (every 10 min) | ✅ Cheapest, fastest |
| Signal correlation | ⚠️ Limited — Captain handles complex correlation |

**Why nano?** Watchtower's job is simple: read numbers, compare to thresholds, report anomalies. It doesn't interpret, negotiate, write, or reason deeply. Nano is the right tool for the job. Spending $1+ per 1M on monitoring is waste.

---

## Final Lineup

| Agent | Model | Provider | Cost in/out | Key Strength |
|-------|-------|----------|-------------|--------------|
| **Captain** | Kimi K2.5 Thinking | Moonshot | $0.45/$2.25 | Reasoning |
| **Scout** | Claude Sonnet 4.5 | Anthropic | $3.00/$15.00 | Vision + Tool Use + Code |
| **Shield** | Kimi K2.5 Thinking | Moonshot | $0.45/$2.25 | Legal Reasoning |
| **Hawk** | GLM-4.7 | Zhipu | $0.40/$1.50 | Math + Analytics |
| **Signal** | GPT-5.1 | OpenAI | $1.25/$10.00 | Writing + Personalization |
| **Watchtower** | GPT-5-nano | OpenAI | $0.05/$0.40 | Speed + Cost |

## Model Diversity: 4 Providers

- **Moonshot** → Captain, Shield
- **Anthropic** → Scout
- **Zhipu** → Hawk
- **OpenAI** → Signal, Watchtower

Single provider outage: max 2 agents affected (Moonshot down = Captain + Shield). Scout, Hawk, Signal, Watchtower continue independently.

## Estimated Costs

| Scenario | Daily | Monthly |
|----------|-------|---------|
| Low (5 leads/day) | $3.00 | $90 |
| Medium (15 leads/day) | $7.00 | $210 |
| High (30 leads/day) | $12.00 | $360 |

## Daily Budget Caps

| Agent | Cap | Notes |
|-------|-----|-------|
| Captain | $5.00 | Strategy, standups, buyer outreach |
| Scout | $12.00 | Highest volume — Sonnet is expensive but worth it |
| Shield | $5.00 | Focused compliance reviews |
| Hawk | $3.00 | Periodic analytics, not continuous |
| Signal | $8.00 | Delivery processing + buyer communications |
| Watchtower | $1.00 | Simple monitoring |
| **Total** | **$34.00** | Alert at $25, critical at $34 |

---

_Model assignments are Tier 3 (AK approval). This is a proposal._
