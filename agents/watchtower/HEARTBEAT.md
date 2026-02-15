# HEARTBEAT.md — Watchtower

Every 10 min:
1. Check all agent heartbeats — any silent > 1h?
2. Monitor daily AI spend across all agents
3. Check lead pipeline health (intake vs delivery rate)
4. Watch Shield block rate
5. Track Supabase usage against free tier limits

## Memory Vault
6. **Recall** — Check vault for historical anomaly patterns:
   `python3 scripts/memory-search.py "anomaly cost spike" --agent watchtower --limit 3`
7. **Record** — After detecting issues, write observations to `memory/vault/obs-YYYY-MM-DD-NNN.md`

If all systems nominal, reply HEARTBEAT_OK.
