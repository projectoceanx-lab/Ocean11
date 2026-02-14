# Model Strategy V2 — Quality Models via OpenRouter

_Updated Feb 14, 2026. No DeepSeek. Quality over penny-pinching._

## Principle

Bad model = bad output = no revenue. We're not optimizing for cheapest cost per token. We're optimizing for cost per successful outcome. A $1 model that gets it right is cheaper than a $0.10 model that gets it wrong and wastes everyone's time downstream.

## Model Assignments

| Agent | Model | Cost (in/out per 1M) | Why |
|-------|-------|---------------------|-----|
| **Captain** | Kimi K2.5 Thinking | $0.45 / $2.25 | Strategic reasoning, P&L analysis, buyer negotiation. Needs deep thinking. 262K context. |
| **Scout** | Claude Haiku 4.5 | $1.00 / $5.00 | Form filling needs precision and reliability. Haiku 4.5 is fast, accurate, follows instructions perfectly. 200K context. Scout processes the most volume — needs a model that doesn't make mistakes. |
| **Shield** | Kimi K2.5 Thinking | $0.45 / $2.25 | Compliance requires careful reasoning. Legal edge cases, state-specific rules, consent interpretation. Cannot afford mistakes here. Same model as Captain but different role — acceptable since they rarely run simultaneously. |
| **Hawk** | GLM-4.7 | $0.40 / $1.50 | Strong on math and analytics. #22 on Arena, #21 math. CPL calculations, budget optimization, A/B analysis. 202K context. |
| **Signal** | MiniMax M2.5 | $0.30 / $1.20 | Delivery ops need reliability and good instruction following. 204K context. Buyer matching, routing logic, email delivery — structured tasks where M2.5 excels. |
| **Watchtower** | GPT-5-nano | $0.05 / $0.40 | Monitoring is simple pattern matching. Check numbers, compare thresholds, alert. Cheapest capable model — this is the right place to save money. |

## Why These Models

### Scout → Claude Haiku 4.5
Scout is the start of every dollar we earn. If Scout fills a form wrong, the lead is garbage. If Scout scores incorrectly, Shield and Signal waste time on bad data. Haiku 4.5 is Anthropic's fast model — excellent instruction following, reliable output format, handles structured tasks with near-zero error rate. Worth $1/M in for Scout's volume.

### Shield → Kimi K2.5 Thinking
Shield makes legal decisions. The cost of a wrong compliance call isn't $2 in wasted tokens — it's a potential $50K+ FTC fine. Kimi K2.5's reasoning capability is essential for interpreting consent language, navigating state-specific rules, and making defensible pass/flag/block decisions. This is not the place to go cheap.

### Hawk → GLM-4.7
Media buying is math. GLM-4.7 ranks #21 on the math arena. It can analyze CPL trends, calculate statistical significance, and recommend budget shifts with precision. At $0.40/$1.50 it's the best value for quant work.

### Signal → MiniMax M2.5
Signal's tasks are structured — match lead to buyer, check caps, route via channel, log delivery. M2.5 is a strong instruction-following model with 204K context. It doesn't need to reason deeply — it needs to execute reliably. At $0.30/$1.20 it's the right balance.

### Watchtower → GPT-5-nano
This is where we save money. Watchtower checks: is this number above threshold? Has this agent been silent too long? Is cost on track? These are simple comparisons. GPT-5-nano at $0.05/$0.40 handles this perfectly. No reason to spend more.

## Model Diversity

6 agents, 5 different model providers:
- **Moonshot** (Kimi) — Captain, Shield
- **Anthropic** (Claude) — Scout
- **Zhipu** (GLM) — Hawk
- **MiniMax** — Signal
- **OpenAI** — Watchtower

If any single provider has an outage, maximum 2 agents are affected (Captain + Shield share Kimi). The rest keep running.

## Estimated Costs

| Scenario | Daily | Monthly |
|----------|-------|---------|
| Low (5 leads/day) | $1.50 | $45 |
| Medium (15 leads/day) | $3.50 | $105 |
| High (30 leads/day) | $6.00 | $180 |

## Budget Caps (Per Agent, Per Day)

| Agent | Daily Cap | Rationale |
|-------|-----------|-----------|
| Captain | $5.00 | Strategic work, moderate token volume |
| Scout | $8.00 | Highest volume agent — processes every lead |
| Shield | $5.00 | Reviews every lead but checks are focused |
| Hawk | $3.00 | Analytics runs, not continuous |
| Signal | $4.00 | Delivery processing, buyer comms |
| Watchtower | $1.00 | Frequent but small checks |
| **Total** | **$26.00** | Alert if exceeded |

## Upgrade Path

| Trigger | Action |
|---------|--------|
| Scout accuracy < 90% | Upgrade to Claude Sonnet 4.5 |
| Shield makes compliance error | Add Captain as backup reviewer |
| Hawk recommendations losing money | Try Gemini 3 Pro for deeper analysis |
| Revenue > $5K/month | Can afford premium models across the board |
| MiniMax M2.5 unreliable | Switch Signal to Haiku 4.5 |

---

_Model assignments are Tier 3 (AK approval). This is a proposal._
