# HEARTBEAT.md — Hawk

Every 6 hours:
1. Pull campaign metrics (spend, leads, CPL) from active sources
2. Identify winners and losers
3. Recommend budget shifts if data supports it
4. Check A/B test status for statistical significance
5. Report daily optimization summary to Fury

## Memory Vault
6. **Recall** — Before optimizing, search vault for past campaign patterns:
   `python3 scripts/memory-search.py "campaign performance" --agent hawk --limit 3`
7. **Record** — After analysis, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If nothing needs adjustment, reply HEARTBEAT_OK.
