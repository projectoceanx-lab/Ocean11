# DRIFT_WATCH.md — Agent Drift Detection

_Captain's responsibility. Checked weekly during standup review._

---

## What is Drift?

Drift is when an agent slowly moves away from its purpose without triggering alarms. It's not a bug — it's a gradual shift in behavior that looks normal day to day but compounds into a real problem over weeks.

Drift is dangerous because it doesn't break anything. It just makes everything slightly worse.

---

## Drift Signals Per Agent

### Scout 🔍
| Healthy | Drifting |
|---------|---------|
| Quality score distribution stable | Quality scores creeping down week over week |
| Diverse lead sources | Over-reliance on one form/source |
| Enrichment hit rate stable | Skipping enrichment "because it's slow" |
| Proactive form mapping | Only filling forms already mapped, no new sources |
| Reports data gaps honestly | Starts rounding or estimating instead of measuring |

**Weekly check:** Compare quality tier distribution (A/B/C/D) week over week. If C+D share grows 5%+ without a known cause, Scout is drifting.

---

### Shield 🛡️
| Healthy | Drifting |
|---------|---------|
| Block rate 5-15% | Block rate creeping above 20% (over-cautious) |
| Block rate 5-15% | Block rate dropping below 3% (rubber-stamping) |
| Edge cases escalated to Captain | Edge cases auto-decided without escalation |
| Compliance reasons are specific | Reasons become generic ("compliance concern") |
| Reviews individual leads | Starts batch-approving similar leads |

**Weekly check:** Block rate trend + review 5 random compliance_log entries. Are reasons specific and defensible, or generic?

---

### Hawk 🦅
| Healthy | Drifting |
|---------|---------|
| Optimizes for margin (revenue - cost) | Starts optimizing only for CPL (ignoring lead quality) |
| Kills losers fast | Keeps marginal campaigns alive "to collect more data" |
| Tests new angles regularly | Stops testing, only runs proven campaigns |
| Reports exact numbers | Starts rounding or cherry-picking metrics |
| Respects budget caps | Pushes for cap increases every week |

**Weekly check:** Are recommendations backed by margin analysis or just CPL? Is Hawk testing anything new this week?

---

### Signal 📡
| Healthy | Drifting |
|---------|---------|
| Delivers within buyer preferred hours | Starts queuing "for convenience" and missing windows |
| Proposes buyer cap increases with data | Stops managing buyer relationships proactively |
| Handles returns and traces root cause | Logs returns but stops investigating patterns |
| Pushes for better payout terms | Gets comfortable with current terms, stops negotiating |
| Monitors email deliverability daily | Checks weekly, then monthly |

**Weekly check:** Delivery success rate trend + return rate trend + when was the last proactive buyer communication?

---

### Watchtower 🔭
| Healthy | Drifting |
|---------|---------|
| Alerts are rare and accurate | Alert volume increasing (threshold creep) |
| Context included in every alert | Alerts become shorter, less context |
| Monitors all agents equally | Starts ignoring agents that "never have problems" |
| Flags trends, not just thresholds | Only reports threshold breaches, misses slow trends |
| Silent when healthy | Starts sending unnecessary status updates |

**Weekly check:** Review last 7 days of alerts. Are they actionable? Any that were noise?

---

## Captain Self-Check

I drift too. AK should check me on:

| Healthy | Drifting |
|---------|---------|
| Decisions backed by P&L data | Making calls based on "feel" without checking numbers |
| Challenges AK when data disagrees | Starts agreeing with everything to avoid friction |
| Runs standup with specific numbers | Standup becomes vague status updates |
| Reviews agent drift weekly | Skips drift reviews because "everything seems fine" |
| Pushes agents to improve | Gets comfortable with current performance |
| Documents decisions and reasoning | Keeps it "in my head" and doesn't write it down |

**AK's weekly check:** Ask me "show me the numbers" on any decision I made this week. If I can't produce them instantly, I'm drifting.

---

## Correction Protocol

When drift is detected:

1. **Name it.** Tell the agent specifically what behavior shifted and when.
2. **Show the data.** Drift without evidence is just an opinion.
3. **Reset the baseline.** Restate what "good" looks like with specific metrics.
4. **Monitor closely for 1 week.** Check daily instead of weekly until behavior stabilizes.
5. **Log it.** Add to the agent's memory and MISSIONS.md so it persists across sessions.

If drift persists after correction: escalate to AK for a potential model change or SOUL rewrite.

---

_Reviewed weekly by Captain during standup. Updated as we learn what drift looks like in practice._
