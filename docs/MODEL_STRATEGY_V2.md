# Model Strategy V2 — OpenRouter Only, No DeepSeek

_Updated Feb 14, 2026. All models via OpenRouter._

## Model Assignments

| Agent | Model | Cost (in/out per 1M) | Why |
|-------|-------|---------------------|-----|
| **Captain** | Kimi K2.5 Thinking | $0.50 / $2.80 | Strategic reasoning, P&L analysis, buyer negotiation. Needs to think deeply. |
| **Scout** | Llama 3.3 70B Instruct | $0.10 / $0.32 | Reliable execution at low cost. Form filling, enrichment, scoring are structured tasks. 131K context. |
| **Shield** | Gemini 2.5 Flash Lite | $0.10 / $0.40 | Fast compliance checks with 1M context window. Can hold all compliance rules + lead data in one pass. Cheap enough for high-volume reviews. |
| **Hawk** | GLM-4-32B | $0.10 / $0.10 | Math-heavy analytics at rock bottom cost. CPL calculations, budget optimization, A/B test analysis. |
| **Signal** | Mistral Small 3.1 24B | $0.03 / $0.11 | Delivery ops are structured — match buyer, route, confirm. Cheap, 131K context, good at following instructions. |
| **Watchtower** | GPT-4.1-nano | $0.10 / $0.40 | Monitoring just needs "good enough." OpenAI's smallest model. Check numbers, compare thresholds, alert. |

## Key Changes from V1

1. **No DeepSeek** — Replaced with Llama 3.3 70B (Scout) and Mistral Small 3.1 (Signal)
2. **Shield moved from Kimi to Gemini Flash Lite** — Shield doesn't need deep reasoning for most checks. Fast + cheap + 1M context = better fit. Shield can hold the entire COMPLIANCE_RULES.md in context with room to spare.
3. **Captain stays on Kimi K2.5** — Only agent that needs strategic reasoning. Worth the premium.
4. **Model diversity maintained** — 5 different providers (Moonshot, Meta, Google, Zhipu, Mistral, OpenAI) = resilience.

## Cost Comparison

| Scenario | V1 (Daily) | V2 (Daily) | Savings |
|----------|-----------|-----------|---------|
| Low (5 leads/day) | $1.50 | $0.80 | 47% |
| Medium (15 leads/day) | $3.00 | $1.50 | 50% |
| High (30 leads/day) | $5.00 | $2.50 | 50% |

## Monthly Estimates

| Scenario | Monthly Cost |
|----------|-------------|
| Low | ~$24 |
| Medium | ~$45 |
| High | ~$75 |

## Why These Specific Models

- **Llama 3.3 70B** — Meta's best open model. Strong instruction following. Proven reliable. $0.10/M in is exceptional for a 70B model.
- **Gemini 2.5 Flash Lite** — Google's speed-optimized model. 1M context means Shield never needs to chunk compliance rules. $0.10/$0.40 is cheaper than Kimi and fast enough for pass/flag/block decisions.
- **GLM-4-32B** — Same family as V1's GLM-4.7 but cheaper. Still strong on math. $0.10/$0.10 is the cheapest non-free model with decent capability.
- **Mistral Small 3.1 24B** — Mistral's efficient small model. Good at structured tasks. 131K context. $0.03/$0.11 is nearly free.
- **GPT-4.1-nano** — OpenAI's smallest. Perfect for Watchtower's simple monitoring checks.

## Risk: Shield on a Lighter Model

Moving Shield from Kimi K2.5 (strong reasoning) to Gemini Flash Lite (fast but lighter) is a calculated risk. Most compliance checks are pattern matching, not deep reasoning:
- Is the phone number valid? → Pattern match
- Is the state in the prohibited list? → Lookup
- Is the debt amount plausible? → Range check
- Does consent documentation exist? → Boolean check

For the 5% of cases that need genuine legal reasoning (state-level edge cases, ambiguous consent language), Shield should escalate to Captain (Kimi K2.5) instead of trying to reason it out on a lighter model.

If Shield's block accuracy drops below 95%, upgrade to Kimi K2.5 or Gemini 2.5 Flash (non-lite).

---

_This is a proposal. AK approves model assignments (Tier 3 trust)._
