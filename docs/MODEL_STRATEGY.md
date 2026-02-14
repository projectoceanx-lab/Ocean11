# Model Strategy

Why each model was chosen, cost analysis, and upgrade paths.

## Selection Criteria

1. **Cost efficiency** — We're bootstrapping with $5K. Every token matters.
2. **Task fit** — Match model strength to agent needs.
3. **Quality floor** — Must be good enough. "Good enough" means the agent accomplishes its task without human intervention 90%+ of the time.
4. **Availability** — Must be accessible via OpenRouter.

## Model Assignments

### Captain → anthropic/claude-opus-4-6 (fallback: openai/gpt-5.3-codex)
- **Why:** CEO decisions — P&L, buyer negotiations, agent arbitration — need the strongest strategic reasoning available. Opus 4.6 is top-tier. GPT-5.3 Codex as fallback for resilience.
- **Cost:** $15 input / $75 output per 1M tokens (fallback: $2/$8)
- **Daily budget cap:** $10.00
- **Usage pattern:** Moderate but consequential — daily standups, buyer decisions, strategy. ~50-100K tokens/day.
- **Estimated daily cost:** $1.50-5.00

### Scout → deepseek/deepseek-v3-0324
- **Why:** Lead acquisition is mechanical — fill forms, check DBs, call APIs. Doesn't need deep reasoning. DeepSeek V3 is cheap and competent for structured tasks.
- **Cost:** $0.25 input / $0.38 output per 1M tokens
- **Daily budget cap:** $3.00
- **Usage pattern:** High volume — processes many leads. ~100-200K tokens/day.
- **Estimated daily cost:** $0.30-0.80

### Shield → openai/gpt-5.2 (high thinking)
- **Why:** The most consequential decisions in the operation. One compliance miss = FTC action, buyer burn, legal exposure. GPT-5.2 with high thinking budget gives Shield the deepest reasoning available for regulatory edge cases, state-specific rules, and ambiguous compliance scenarios.
- **Cost:** $2.00 input / $8.00 output per 1M tokens (+ thinking tokens)
- **Daily budget cap:** $5.00
- **Usage pattern:** Low-medium — reviews each lead but checks are focused. ~30-80K tokens/day.
- **Estimated daily cost:** $0.50-2.00

### Hawk → zhipu/glm-4.7
- **Why:** Analytics and optimization require mathematical reasoning. GLM-4.7 ranks #21 on the math arena — strong quantitative capability at low cost.
- **Cost:** ~$0.10 input / $0.10 output per 1M tokens
- **Daily budget cap:** $2.00
- **Usage pattern:** Medium — campaign analysis, CPL calculations, A/B test results. ~50-100K tokens/day.
- **Estimated daily cost:** $0.10-0.20

### Signal → deepseek/deepseek-v3-0324
- **Why:** Delivery ops are structured — match buyer, route lead, confirm acceptance. Same reasoning as Scout: mechanical tasks, DeepSeek is cheap and good.
- **Cost:** $0.25 input / $0.38 output per 1M tokens
- **Daily budget cap:** $3.00
- **Usage pattern:** Medium — delivery processing, email/call routing. ~50-100K tokens/day.
- **Estimated daily cost:** $0.20-0.50

### Watchtower → openai/gpt-5-nano
- **Why:** Monitoring is simple — check numbers, compare to thresholds, alert if anomaly. The cheapest model that can read data and make basic decisions.
- **Cost:** $0.05 input / $0.40 output per 1M tokens
- **Daily budget cap:** $1.00
- **Usage pattern:** Frequent but small — health checks every 10 min. ~20-50K tokens/day.
- **Estimated daily cost:** $0.05-0.15

## Total Estimated AI Cost

| Scenario | Daily | Monthly |
|----------|-------|---------|
| Low (5 leads/day) | $3.00 | $90 |
| Medium (15 leads/day) | $6.00 | $180 |
| High (30 leads/day) | $10.00 | $300 |

## When to Upgrade Models

| Trigger | Action |
|---------|--------|
| Scout accuracy < 80% on forms | Consider Claude Haiku or Sonnet |
| Shield makes compliance error | Already on GPT-5.2 high thinking; review prompt/rules quality |
| Hawk recommendations losing money | Try DeepSeek R1 or Claude for analysis |
| Revenue > $5K/month | Can afford better models across the board |
| Any agent in infinite loop | Model issue — switch to different provider |

## Cost Control

- Every agent has a `daily_budget_cap` in config
- Watchtower monitors total AI spend
- Alert at $15/day, critical at $25/day
- If an agent hits its cap, it pauses until the next day
- Captain can override caps in emergencies
