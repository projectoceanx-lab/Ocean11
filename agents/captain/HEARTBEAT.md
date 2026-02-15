# HEARTBEAT.md — Captain

Every 30 min:
1. Review agent reports and standup summaries
2. Check P&L — revenue vs spend trending
3. Identify blockers across the pipeline
4. Check buyer relationship status and acceptance rates

## Memory Vault
5. **Recall** — Before making decisions, search vault for context:
   `python3 scripts/memory-search.py "relevant topic" --agent captain --limit 3`
6. **Record** — After decisions and buyer calls, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If nothing needs attention, reply HEARTBEAT_OK.
